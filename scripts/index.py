import argparse
import json
from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from turkcerag.llm import EMBED_MODEL, get_client

BATCH = 64
META = {"doc_id", "title", "url", "date", "doc_type"}

p = argparse.ArgumentParser()
p.add_argument("--size", type=int, default=512)
args = p.parse_args()

chunks = [
    json.loads(l)
    for l in Path(f"data/processed/chunks_{args.size}.jsonl").open(encoding="utf-8")
]
client = get_client()
db = chromadb.PersistentClient(path="data/chroma")
name = f"azure-{args.size}"


# TODO 1: aynı isimli koleksiyon varsa sil (script'i tekrar çalıştırınca kayıtlar
#         ikilenmesin). Yoksa Chroma NotFoundError fırlatır; try/except ile yut.
#         Sonra metadata={"hnsw:space": "cosine"} ile yeniden oluştur.
try:
    collection = db.get_collection(name=name)
    print(f"Collection '{name}' exists.")
    db.delete_collection(name=name)
    print("Deleted")

except NotFoundError:
    print(f"Collection '{name}' does not exist.")

col = db.create_collection(name, metadata={"hnsw:space": "cosine"})
metadata = {"hnsw:space": "cosine"}
# TODO 2: chunk'ları BATCH'lik gruplar halinde embed et:
#         client.embeddings.create(model=EMBED_MODEL, input=[...metinler...])

# TODO 3: col.add(ids=..., embeddings=..., documents=..., metadatas=...) ile ekle.
#         metadatas her chunk için META alanlarından oluşan bir dict.
#         Her batch'ten sonra "128/344" gibi ilerleme yazdır.

for i in range(0, len(chunks), BATCH):
    batch = chunks[i : i + BATCH]
    resp = client.embeddings.create(model=EMBED_MODEL, input=[c["text"] for c in batch])
    col.add(
        ids=[c["chunk_id"] for c in batch],
        embeddings=[d.embedding for d in resp.data],
        documents=[c["text"] for c in batch],
        metadatas=[{k: c[k] for k in META} for c in batch],
    )
    print(f"{min(i + BATCH, len(chunks))}/{len(chunks)}")

print("koleksiyon:", name, "·", col.count(), "chunk")
