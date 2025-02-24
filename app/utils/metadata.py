from pathlib import Path
from typing import List, NamedTuple
from pydantic import BaseModel


class ShowMetadata(NamedTuple):
    showname: str
    dates_filepath: Path
    titles_filepath: Path


class ShowMetadataList(BaseModel):
    shows: List[ShowMetadata]


def meta_dict(file_path):
    file = open(file_path, "r").read().splitlines()
    return {
        key: value
        for key, value in [
            (line.split(" - ")[0], line.split(" - ")[1]) for line in file
        ]
    }


def metadata_to_dict(metadata: ShowMetadataList):
    metadata_dict = {}
    for show in metadata.shows:
        showname, dates_filepath, titles_filepath = show
        metadata_dict[showname] = {
            "dates": meta_dict(dates_filepath),
            "titles": meta_dict(titles_filepath),
        }
    return metadata_dict


data = ShowMetadataList(
    shows=[
        ShowMetadata(
            "rotl",
            Path("../files/meta/rotl_dates.txt"),
            Path("../files/meta/rotl_titles.txt"),
        ),
        ShowMetadata(
            "roadwork",
            Path("../files/meta/roadwork_dates.txt"),
            Path("../files/meta/roadwork_titles.txt"),
        ),
    ]
)

dates_titles = metadata_to_dict(data)


def get_meta(file):
    file_name = file.name
    episode_number = file_name.split("_-_")[0]
    episode_date = dates_titles["rotl"]["dates"][episode_number]
    episode_title = dates_titles["rotl"]["titles"][episode_number]
    return (file_name, episode_number, episode_date, episode_title)
