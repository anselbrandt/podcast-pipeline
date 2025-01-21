import os
import argparse
from dotenv import load_dotenv

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
    print(content_with_speaker)


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
