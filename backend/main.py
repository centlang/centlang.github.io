import os
import subprocess
import tempfile

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

TIMEOUT_SECONDS = 5

app = FastAPI()

class RunRequest(BaseModel):
    code: str
    mode: str

@app.post("/api/run")
async def run_code(request: RunRequest):
    tmp_dir = tempfile.mkdtemp()
    extra_flags = []

    match request.mode:
        case "release":
            extra_flags.append("-O")
        case "debug":
            pass
        case _:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid compilation mode")

    with open(os.path.join(tmp_dir, "main.cn"), "w") as file:
        file.write(request.code)

    process = subprocess.Popen(
        [
            "docker",
            "run",
            "--rm",
            "--init",
            "--network=none",
            "-v",
            f"{tmp_dir}:/play:rw",
            "centc",
            "--run",
            "/play/main.cn",
            *extra_flags,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        stdout, stderr = process.communicate(timeout=TIMEOUT_SECONDS)

        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "exit": process.returncode,
        }
    except subprocess.TimeoutExpired:
        process.terminate()
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, "Time limit exceeded")

app.mount("/", StaticFiles(directory="frontend/build", html=True))
