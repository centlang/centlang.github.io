import os
import asyncio
import tempfile
import psutil
import shutil

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

TIMEOUT_SECONDS = 5

OS_USAGE_MB = 700
CONTAINER_LIMIT_MB = 256

app = FastAPI()

class RunRequest(BaseModel):
    code: str
    mode: str

def get_container_limit():
    ram_limit = (
        psutil.virtual_memory().available - OS_USAGE_MB * 1024 * 1024
    ) // (CONTAINER_LIMIT_MB * 1024 * 1024)

    return max(1, ram_limit)

semaphore = asyncio.Semaphore(get_container_limit())

async def run_code(request: RunRequest):
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

@app.post("/run")
async def run_route(request: RunRequest):
    async with semaphore:
        return await run_code(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://centlang.org", "https://www.centlang.org"],
    allow_methods=["*"],
    allow_headers=["*"],
)
