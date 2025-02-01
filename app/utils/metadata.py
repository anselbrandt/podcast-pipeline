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
