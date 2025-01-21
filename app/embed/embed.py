import argparse


def embed(file_path, show_name, episode_number, episode_title, episode_date):
    print(file_path, show_name, episode_number, episode_title, episode_date)


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

    embed(file_path, show_name, episode_number, episode_title, episode_date)


if __name__ == "__main__":
    main()
