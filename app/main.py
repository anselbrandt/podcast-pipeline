import os
from pathlib import Path
from subprocess import Popen, PIPE, run

from app.rename import rename

input_dir = Path("files/input")

files = [file for file in input_dir.iterdir() if ".mp3" in file.name]


def transcribe(file):
    command = [
        "docker",
        "run",
        "--privileged",
        "--rm",
        "--gpus",
        "all",
        "-v",
        f"{os.getcwd()}/files:/app/files",
        "-v",
        f"{os.getcwd()}/cache/huggingface:/root/.cache/huggingface",
        "whisper-nemo",
        str(file),
    ]
    with Popen(command, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end="")


for file in files[:1]:
    safe_name = rename(file)
    transcribe(safe_name)
