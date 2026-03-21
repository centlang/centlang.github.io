import os
import asyncio
import secrets
import tempfile
import psutil
import shutil
import string

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from httpx import AsyncClient

TIMEOUT_SECONDS = 5
CONTAINER_LIMIT_MB = 256

NANOID_LENGTH = 6
NANOID_ALPHABET = string.ascii_letters + string.digits + "_-"
NANOID_FS_SPLIT = 2

SNIPPET_LIMIT_KB = 64
SNIPPETS_DIR = "snippets"

CF_TURNSTILE_KEY = os.getenv("CF_TURNSTILE_KEY")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_container_limit() -> int:
    ram_limit = psutil.virtual_memory().available // (
        CONTAINER_LIMIT_MB * 1024 * 1024
    )

    return max(1, ram_limit)

semaphore = asyncio.Semaphore(get_container_limit())

class RunRequest(BaseModel):
    code: str
    mode: str
    token: str

async def run_code(request: RunRequest) -> dict:
    tmp_dir = tempfile.mkdtemp()

    try:
        extra_flags = []

        match request.mode:
            case "release":
                extra_flags += ["-O", "--release"]
            case "debug":
                pass
            case _:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Invalid compilation mode"
                )

        with open(os.path.join(tmp_dir, "main.cn"), "w") as file:
            file.write(request.code)

        process = await asyncio.create_subprocess_exec(
            "docker",
            "run",
            "--rm",
            "--init",
            "--network=none",
            "-m",
            f"{CONTAINER_LIMIT_MB}m",
            "-v",
            f"{tmp_dir}:/play:rw",
            "centc",
            "--run",
            "--color",
            "/play/main.cn",
            *extra_flags,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            process.terminate()

            raise HTTPException(
                status.HTTP_504_GATEWAY_TIMEOUT, "Time limit exceeded"
            )

        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit": process.returncode,
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

async def verify_turnstile(token: str) -> bool:
    async with AsyncClient() as client:
        response = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": CF_TURNSTILE_KEY, "response": token},
        )

        result = response.json()

        return result.get("success", False)

@app.post("/run")
@limiter.limit("10/10seconds")
async def run_route(request: Request, data: RunRequest) -> dict:
    if not await verify_turnstile(data.token):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Cloudflare Turnstile verification failed",
        )

    async with semaphore:
        return await run_code(data)

def nanoid() -> str:
    return "".join(
        secrets.choice(NANOID_ALPHABET) for _ in range(NANOID_LENGTH)
    )

def is_nanoid(nanoid: str) -> bool:
    return len(nanoid) == NANOID_LENGTH and all(
        c in NANOID_ALPHABET for c in nanoid
    )

def get_snippet_path(nanoid: str) -> str:
    chunks = [
        nanoid[i : i + NANOID_FS_SPLIT]
        for i in range(0, len(nanoid) - NANOID_FS_SPLIT, NANOID_FS_SPLIT)
    ]

    return os.path.join(*chunks)

class SnippetCreate(BaseModel):
    code: str

@app.post("/s")
@limiter.limit("30/12seconds")
async def snippets_post(request: Request, data: SnippetCreate) -> dict:
    if len(data.code.encode("utf-8")) > SNIPPET_LIMIT_KB * 1024:
        raise HTTPException(
            status.HTTP_413_CONTENT_TOO_LARGE, "Snippet too large"
        )

    snippet = nanoid()

    dir = os.path.join(SNIPPETS_DIR, get_snippet_path(snippet))
    os.makedirs(dir, exist_ok=True)

    path = os.path.join(dir, snippet)

    while os.path.exists(path):
        snippet = nanoid()

        dir = os.path.join(SNIPPETS_DIR, get_snippet_path(snippet))
        os.makedirs(dir, exist_ok=True)

        path = os.path.join(dir, snippet)

    with open(path, "w") as file:
        file.write(data.code)

    return {"id": snippet}

@app.get("/s/{snippet}")
@limiter.limit("5/second")
async def snippets_get(request: Request, snippet: str) -> dict:
    if not is_nanoid(snippet):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid snippet ID")

    dir = os.path.join(SNIPPETS_DIR, get_snippet_path(snippet))
    path = os.path.join(dir, snippet)

    if not os.path.exists(path):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Snippet not found")

    with open(path) as file:
        return {"code": file.read()}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://centlang.org", "https://www.centlang.org"],
    allow_methods=["*"],
    allow_headers=["*"],
)
