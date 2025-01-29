import os
import argparse
from dotenv import load_dotenv
from pathlib import Path

from app.utils import merge_srt

load_dotenv()

ROOT = os.getcwd()


def chunk(file_path, subdir=None):
    chunkedDir = (
        os.path.join(ROOT, "files", "chunked", subdir)
        if subdir
        else os.path.join(ROOT, "files", "chunked")
    )
    os.makedirs(chunkedDir, exist_ok=True)
    transcript = merge_srt(file_path)
    content_with_speaker = [
        f"{idx}|{speaker}: {speech} " for idx, start, end, speaker, speech in transcript
    ]
    text = "\n".join(content_with_speaker)
    filename = Path(file_path).stem
    outpath = os.path.join(chunkedDir, filename + ".txt")
    f = open(outpath, "w")
    f.write(text)
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to labeled .srt file")
    parser.add_argument("--subdir", type=str, help="Optional chunked sub directory")
    args = parser.parse_args()
    if args.subdir:
        file_path = args.input
        subdir = args.subdir
        chunk(file_path, subdir)
    else:
        file_path = args.input
        chunk(file_path, None)


if __name__ == "__main__":
    main()
