import os
import argparse
import json
import sqlite3

import chromadb
from chromadb.utils import embedding_functions

ROOT = os.getcwd()

chromadb_dir = os.path.join(ROOT, "chromadb")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-mpnet-base-v2", device="cuda"
)

chroma_client = chromadb.PersistentClient(path=chromadb_dir)

try:
    collection = chroma_client.get_collection(
        name="podcasts", embedding_function=sentence_transformer_ef
    )
except:
    collection = chroma_client.create_collection(
        name="podcasts", embedding_function=sentence_transformer_ef
    )

chunked_dir = os.path.join(ROOT, "files", "chunked")


def embed(
    file_path: str,
    show_name: str,
    episode_number: str,
    episode_title: str,
    episode_date: str,
    hosts: list[str],
):
    conn = sqlite3.connect("transcripts.db")
    c = conn.cursor()
    c.execute(
        """SELECT idx, wavefile FROM lines WHERE showname LIKE ? AND episode LIKE ?""",
        (show_name, episode_number),
    )
    results = c.fetchall()
    conn.commit()
    conn.close()
    wav_dict = {str(idx): filepath for idx, filepath in results}
    file = open(file_path).read().split("\n\n")
    chunks = []
    all_wavfiles = []
    for chunk in file:
        lines = [
            (
                line.split("|")[0],
                line.split("|")[1].split(": ")[0],
                line.split("|")[1].split(": ")[1].strip(),
            )
            for line in chunk.split("\n")
        ]
        wavfiles = [
            {"speaker": speaker, "speech": speech, "wavfile": wav_dict[idx]}
            for idx, speaker, speech in lines
        ]

        chunk_speech = " ".join([speech for idx, speaker, speech in lines])
        chunks.append(chunk_speech)
        all_wavfiles.append(wavfiles)
    documents = chunks
    metadatas = [
        {
            "podcast": show_name,
            "hosts": ",".join(hosts),
            "episode": episode_number,
            "title": episode_title,
            "date": episode_date,
            "wavfiles": json.dumps(all_wavfiles[i]),
        }
        for i, chunk in enumerate(chunks)
    ]
    ids = [f"{show_name}_{episode_number}_{i}" for i, chunk in enumerate(chunks)]
    collection.add(documents=documents, metadatas=metadatas, ids=ids)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to labeled .srt file")
    parser.add_argument("--show", type=str, help="Show name")
    parser.add_argument("--episode", type=str, help="Episode number")
    parser.add_argument("--title", type=str, help="Episode title")
    parser.add_argument("--date", type=str, help="Episode date")
    parser.add_argument("--hosts", nargs="+", help="Space separated hosts")
    args = parser.parse_args()
    file_path = args.input
    show_name = args.show
    episode_number = args.episode
    episode_title = args.title
    episode_date = args.date
    hosts = args.hosts

    embed(file_path, show_name, episode_number, episode_title, episode_date, hosts)


if __name__ == "__main__":
    main()
