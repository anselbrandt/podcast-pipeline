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


def chunk(file_path, show_name, episode_number, episode_title, episode_date):
    chunkedDir = os.path.join(ROOT, "files", "chunked")
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
    filename = Path(file_path).name
    outpath = os.path.join(chunkedDir, filename + ".txt")
    f = open(outpath, "w")
    f.write(text)
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to labeled .srt file")
    parser.add_argument("--show", type=str, help="Show name")
    parser.add_argument("--episode", type=str, help="Episode number")
    parser.add_argument("--title", type=str, help="Episode title")
    parser.add_argument("--date", type=str, help="Episode date")
    args = parser.parse_args()
    file_path = args.input
    show_name = args.show
    episode_number = args.episode
    episode_title = args.title
    episode_date = args.date

    chunk(file_path, show_name, episode_number, episode_title, episode_date)


if __name__ == "__main__":
    main()
