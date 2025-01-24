import argparse
import sqlite3
from pathlib import Path

from app.utils import srt_to_transcript

dbFile = "transcripts.db"


def insert(file_path, show_name, episode_number, episode_title, episode_date):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS lines (
            id integer primary key,
            filename text,
            showname text,
            episode text,
            title text,
            date text,
            idx integer,
            start real,
            end real,
            duration real,
            speaker text,
            speech text
            )"""
    )
    conn.commit()

    lines = srt_to_transcript(file_path)
    filename = Path(file_path).name

    for line in lines:
        idx, start, end, speaker, speech = line
        duration = round(float(end) - float(start), 3)
        c.execute(
            "INSERT INTO lines VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                filename,
                show_name,
                episode_number,
                episode_title,
                episode_date,
                idx,
                start,
                end,
                duration,
                speaker,
                speech,
            ),
        )
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to srt file")
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

    insert(file_path, show_name, episode_number, episode_title, episode_date)


if __name__ == "__main__":
    main()
