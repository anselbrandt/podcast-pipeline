# Ollama

### curl

```
curl http://localhost:11434/api/generate -d '{
  "model": "gemma2:27b",
  "prompt": "Why is the sky blue?"
}'
```

```
curl https://mlkyway.anselbrandt.net/ollama/api/generate -d '{
  "model": "gemma2:27b",
  "prompt": "Why is the sky blue?"
}'
```

### ollama python

```
from ollama import Client

client = Client(host="https://mlkyway.anselbrandt.net/ollama")

context = "text to be inlcuded"
query = "user query"
content = f"{context}\n\n{query}"
response = client.chat(
    model="gemma2:27b",
    messages=[
        {
            "role": "user",
            "content": content,
        },
    ],
)
content = response["message"]["content"]
```

### GLiNER Named Entity Recognition

- Extract entities

```
from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

entities = model.predict_entities(text, ["Person"], threshold=0.5)
for entity in entities:
    print(entity["text"])
```

### Use LLM to Categorize Entities

- Personal names
- Bands and musical groups
- Fictional characters
- Songs or musical references
- Literature references

### Test Files

```
eleanor = [
   "030",
   "051",
   "061",
   "069",
   "098",
   "118",
   "186",
   "240",
   "298",
   "398",
   "405",
   "430",
]
```

```
ariella = [
   "152",
   "321",
   "509",
   "551",
   "562",
   "525",
   "291",
   "554",
   "421",
   "556",
   "511",
   "256",
   "373",
]
```

### Notebook Imports

```
from pathlib import Path
import sys

parent_dir = str(Path().resolve().parents[0])
sys.path.insert(0, parent_dir)
```

### Cleanup Chat Response

```
import re

def clean_response(text):
    lines = re.sub(r"\n+", "\n", text).splitlines()
    clean_lines = [line for line in lines if "Let me know if you" not in line]
    return "\n".join(clean_lines)
```

### List Comprehension Filtering

Where `episodes` is a list containing

```
if any(item in string for item in items_to_be_matches)
```

### Sqlite3

```
from pathlib import Path
import sqlite3

dbFile = "sqlite.db"


def create_db():
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
            speaker text,
            speech text
            )"""
    )
    conn.commit()
    conn.close()


create_db()


def insert(file_path, show_name, episode_number, episode_title, episode_date):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    lines = open(file_path, "r").read().splitlines()
    filename = Path(file_path).name
    for line in lines:
        speaker, speech = line
        c.execute(
            "INSERT INTO lines VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
            (
                filename,
                show_name,
                episode_number,
                episode_title,
                episode_date,
                speaker,
                speech,
            ),
        )
    conn.commit()
    conn.close()
```

### Chroma Query

```
import chromadb

client = chromadb.PersistentClient(path="../chromadb")
collection = client.get_or_create_collection("podcasts")

result = collection.query(
    query_texts=["mid-century modern"],
    n_results=10,
)

documents = result["documents"][0]
metadatas = result["metadatas"]
```

### Podcast Metadata

```
from pathlib import Path
import sys

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
```

### Chunking

```
from chonkie import LateChunker

chunker = LateChunker(
    embedding_model="all-MiniLM-L6-v2",
    mode="sentence",
    chunk_size=512,
    min_sentences_per_chunk=1,
    min_characters_per_sentence=12,
    delim="\n",
)

chunks = chunker(text)
```

### Persist to Chroma

```
import chromadb

client = chromadb.PersistentClient(path="../chromadb")
collection = client.get_or_create_collection("podcasts")

metadatas = [{"episode": episode} for i, chunk in enumerate(chunks)]
ids = [str(i) for i, chunk in enumerate(chunks)]
collection.add(documents=chunks, metadatas=metadatas, ids=ids)
```
