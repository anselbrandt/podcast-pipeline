import os
import argparse
import json
import chromadb
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import (
    SentenceTransformerEmbeddingFunction,
)


ROOT = os.getcwd()

chromadb_dir = os.path.join(ROOT, "chromadb")


def retrieve(query_string, number_chunks="10"):
    chroma_client = chromadb.PersistentClient(path=chromadb_dir)
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-mpnet-base-v2", device="cuda"
    )
    collection = chroma_client.get_collection(
        name="podcasts", embedding_function=embedding_function
    )
    raw_results = collection.query(
        query_texts=[query_string],
        n_results=int(number_chunks),
        include=["documents", "metadatas"],
    )
    results = list(zip(raw_results["metadatas"][0], raw_results["documents"][0]))
    metas = [json.loads(metadatas["timestamps"]) for metadatas, text in results]
    text = [f"{line["speaker"]}: {line["speech"]}" for chunk in metas for line in chunk]
    response = "\n".join(text)
    print(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="Query string")
    parser.add_argument(
        "--chunks", type=str, required=False, help="Number of chunks to be returned"
    )
    args = parser.parse_args()
    query_string = args.query
    if args.chunks is not None:
        number_chunks = args.chunks
        retrieve(query_string, number_chunks)
    else:
        retrieve(query_string)


if __name__ == "__main__":
    main()
