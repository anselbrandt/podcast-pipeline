import os
import argparse

from app.utils import sanitize


def rename(filepath):
    directory, filename = os.path.split(filepath)
    sanitized = sanitize(filename)
    new_filepath = os.path.join(directory, sanitized)
    os.rename(filepath, new_filepath)
    print(f"Renamed to {new_filepath}")
    return new_filepath


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str)
    args = parser.parse_args()
    filepath = args.filepath
    rename(filepath)


if __name__ == "__main__":
    main()
