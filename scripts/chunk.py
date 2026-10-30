import argparse
import json
from pathlib import Path

from turkcerag.chunking import chunk_text, n_tokens

p = argparse.ArgumentParser()
p.add_argument("--size", type=int, default=512)
p.add_argument("--overlap", type=int, default=64)
args = p.parse_args()

docs = [json.loads(l) for l in Path("data/processed/docs.jsonl").open(encoding="utf-8")]
out = Path(f"data/processed/chunks_{args.size}.jsonl")

rows = []
for d in docs:
    for i, c in enumerate(chunk_text(d["text"], args.size, args.overlap)):
        rows.append(
            {
                "chunk_id": f"{d['doc_id']}#{i:03d}",
                "doc_id": d["doc_id"],
                "title": d["title"],
                "url": d["url"],
                "date": d["date"],
                "doc_type": d["doc_type"],
                "text": c,
                "n_tokens": n_tokens(c),
            }
        )

with out.open("w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "chunk · en büyük:", max(r["n_tokens"] for r in rows), "token")
