import argparse
import os
from pathlib import Path

from app.rename import sanitize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir", type=str, help="Directory containing files to be renamed."
    )
    args = parser.parse_args()
    target_dir = Path(args.dir)
    files = sorted(
        [filepath for filepath in target_dir.iterdir() if filepath.is_file()]
    )
    for filepath in files:
        directory, filename = os.path.split(filepath)
        sanitized = sanitize(filename)
        new_filepath = os.path.join(directory, sanitized)
        os.rename(filepath, new_filepath)
        print(f"Renamed to {new_filepath}")


if __name__ == "__main__":
    main()
