import os
import argparse
from dotenv import load_dotenv
from pathlib import Path

from semantic_router.encoders import OpenAIEncoder
from semantic_router.splitters import RollingWindowSplitter

from app.utils import srt_to_transcript

load_dotenv()

ROOT = os.getcwd()

encoder = OpenAIEncoder(name="text-embedding-3-small")


def chunk(file_path, subdir=None):
    chunkedDir = (
        os.path.join(ROOT, "files", "chunked", subdir)
        if subdir
        else os.path.join(ROOT, "files", "chunked")
    )
    os.makedirs(chunkedDir, exist_ok=True)
    transcript = srt_to_transcript(file_path)
    content_with_speaker = [
        f"{idx}|{speaker}: {speech} " for idx, start, end, speaker, speech in transcript
    ]
    splitter = RollingWindowSplitter(
        encoder=encoder,
        dynamic_threshold=True,
        min_split_tokens=100,
        max_split_tokens=500,
        window_size=2,
        plot_splits=False,  # set this to true to visualize chunking
        enable_statistics=False,  # to print chunking stats
    )

    splits = splitter(content_with_speaker)
    chunks = ["\n".join(split.docs) for split in splits]
    text = "\n\n".join(chunks)
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
