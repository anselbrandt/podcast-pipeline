import os
import re
import argparse


def sanitize_filename(filename):
    sanitized = filename.replace(" ", "_")
    sanitized = re.sub(r"[^\w\d._-]", "", sanitized)
    sanitized = sanitized.lower()
    return sanitized


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str)
    args = parser.parse_args()
    filepath = args.filepath
    directory, filename = os.path.split(filepath)
    sanitized = sanitize_filename(filename)
    new_filepath = os.path.join(directory, sanitized)
    os.rename(filepath, new_filepath)
    print(f"Renamed to {new_filepath}")


if __name__ == "__main__":
    main()
