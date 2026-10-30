import argparse
import json
from pathlib import Path

from turkcerag.text import is_relevant

p = argparse.ArgumentParser()
p.add_argument("--size", type=int, default=512)
args = p.parse_args()

chunks_list_path = Path(f"data/processed/chunks_{args.size}.jsonl")
questions_list_path = Path("eval/questions.jsonl")

chunks = [json.loads(l) for l in chunks_list_path.open(encoding="utf-8")]
questions = [json.loads(l) for l in questions_list_path.open(encoding="utf-8")]

missing = []
for q in questions:
    if not q["answerable"]:
        continue
    hits = [c for c in chunks if is_relevant(c, q)]
    if not hits:
        missing.append(q["id"])

print(len(chunks), "chunk ·", len(questions), "soru")
print("kanıt hiçbir chunk'ta yok:", len(missing), missing)
