import argparse
from pathlib import Path

from app.embed import embed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=str, help="Directory containing chunked files.")
    parser.add_argument("show_name", type=str, help="Show name")
    parser.add_argument("dates_meta", type=str, help="Path to dates metadata .txt file")
    parser.add_argument(
        "titles_meta", type=str, help="Path to titles metadata .txt file"
    )
    parser.add_argument("hosts", nargs="+", help="Space separated hosts")
    args = parser.parse_args()
    target_dir = Path(args.dir)
    show_name = args.show_name
    hosts = args.hosts
    titles_meta = open(args.titles_meta).read().splitlines()
    titles = titles = {
        title: episode
        for title, episode in [
            (line.split(" - ")[0], line.split(" - ")[1]) for line in titles_meta
        ]
    }
    dates_meta = open(args.dates_meta).read().splitlines()
    dates = dates = {
        date: episode
        for date, episode in [
            (line.split(" - ")[0], line.split(" - ")[1]) for line in dates_meta
        ]
    }
    files = sorted(
        [
            filepath
            for filepath in target_dir.iterdir()
            if filepath.is_file() and filepath.suffix == ".txt"
        ]
    )
    for file_path in files:
        file_name = file_path.name
        episode_number = file_name.split("_-_")[0]
        episode_title = titles[episode_number]
        episode_date = dates[episode_number]
        embed(file_path, show_name, episode_number, episode_title, episode_date, hosts)


if __name__ == "__main__":
    main()
