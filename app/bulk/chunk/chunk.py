import argparse
from pathlib import Path

from app.chunk import chunk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir", type=str, help="Directory containing files to be chunked."
    )
    parser.add_argument("subdir", type=str, help="Chunked sub directory")
    args = parser.parse_args()
    target_dir = Path(args.dir)
    subdir = args.subdir
    files = sorted(
        [
            filepath
            for filepath in target_dir.iterdir()
            if filepath.is_file() and filepath.suffix == ".srt"
        ]
    )
    for file_path in files:
        chunk(file_path, subdir)


if __name__ == "__main__":
    main()
