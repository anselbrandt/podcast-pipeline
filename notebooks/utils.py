from pathlib import Path
import sys
import re
import sqlite3

dbFile = "podcasts.db"

from gliner import GLiNER

gliner_model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
import tiktoken
from chonkie import SDPMChunker

parent_dir = str(Path().resolve().parents[0])
sys.path.insert(0, parent_dir)

from app.utils import ShowMetadataList, ShowMetadata, metadata_to_dict

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


def get_entities(transcript):
    names = set()
    for line in transcript.splitlines():
        speaker, text = line.split(": ")
        entities = gliner_model.predict_entities(text, ["Person"], threshold=0.5)
        for entity in entities:
            names.add(entity["text"])
    return sorted(list(names))


def clean(text):
    chunks = text.split("\n\n")
    response = chunks[1]
    return re.sub(r"\*", "", response)


chunker = SDPMChunker(
    embedding_model="minishlab/potion-base-8M",
    threshold=0.5,
    chunk_size=512,
    min_sentences=1,
    skip_window=1,
    delim="\n",
)


def num_tokens(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def clean_name_response(text):
    if "\n" in text:
        lines = re.sub(r"\n+", "\n", text).splitlines()
        clean_lines = [line for line in lines if "Let me know if" not in line]
        return "\n".join(clean_lines)
    else:
        return text


def clean_transcript(file):
    lines = open(file).read().split("\n\n")
    return "\n".join([line for line in lines if len(line.split(": ")) == 2])


def get_names(transcript):
    named_entities = get_entities(transcript)
    entities_query = "Which of these are people's names? Only return results if they are people's names."
    entities_context = f"{entities_query}\n\n{named_entities}"
    entities_response = ask_llm(entities_context)
    names = clean(entities_response)
    return [name.strip() for name in names.splitlines()]


def create_chunks_db():
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS chunks (
        id integer primary key,
        filename text,
        showname text,
        episode text,
        title text,
        date text,
        idx integer,
        chunk text
        )"""
    )
    conn.commit()
    conn.close()


def create_names_db():
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS names (
        id integer primary key,
        filename text,
        showname text,
        episode text,
        title text,
        date text,
        name integer,
        text text
        )"""
    )
    conn.commit()
    conn.close()


def insert_chunks(
    chunks, file_name, show_name, episode_number, episode_title, episode_date
):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    filename = file_name
    for idx, chunk in enumerate(chunks):
        c.execute(
            "INSERT INTO chunks VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
            (
                filename,
                show_name,
                episode_number,
                episode_title,
                episode_date,
                idx,
                chunk,
            ),
        )
    conn.commit()
    conn.close()


def insert_name(
    name, text, file_name, show_name, episode_number, episode_title, episode_date
):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    filename = file_name
    c.execute(
        "INSERT INTO names VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
        (
            filename,
            show_name,
            episode_number,
            episode_title,
            episode_date,
            name,
            text,
        ),
    )
    conn.commit()
    conn.close()
