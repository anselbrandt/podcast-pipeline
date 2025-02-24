import tiktoken
from chonkie import SDPMChunker


def token_counter(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    token_count = len(encoding.encode(string))
    return token_count


chunker: SDPMChunker = SDPMChunker(
    embedding_model="minishlab/potion-base-8M",
    threshold=0.5,
    chunk_size=512,
    min_sentences=1,
    skip_window=1,
    delim="\n",
)
