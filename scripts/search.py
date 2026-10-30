import sys

from turkcerag.retrieve import search

for h in search(sys.argv[1], k=5):
    print(f"{h['score']:.3f}  {h['chunk_id']}")
    print("       ", h["text"][:120].replace("\n", " "), "...")
