import os
from pathlib import Path
from subprocess import Popen, PIPE, run

from app.rename import rename
from app.split import split
from app.label import label

reference_wav = "files/reference/john.wav"
hosts = ["John", "Merlin"]
input_dir = Path("files/input")
output_dir = Path("files/output")
output_dir.mkdir(parents=True, exist_ok=True)

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


for file in files:
    # safe_name = rename(file)
    # transcribe(safe_name)
    wav_dir = split(input_dir)
    # label(input_dir, output_dir, reference_wav, hosts)
