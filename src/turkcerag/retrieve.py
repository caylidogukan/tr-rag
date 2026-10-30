from functools import lru_cache

import chromadb

from turkcerag.llm import EMBED_MODEL, get_client


@lru_cache
def _collection(name: str):
    return chromadb.PersistentClient(path="data/chroma").get_collection(name)


def search(query: str, k: int = 5, size: int = 512) -> list[dict]:
    vec = (
        get_client()
        .embeddings.create(model=EMBED_MODEL, input=[query])
        .data[0]
        .embedding
    )
    r = _collection(f"azure-{size}").query(query_embeddings=[vec], n_results=k)
    ids = r["ids"][0]
    metas = (r["metadatas"] or [[]])[0]
    dists = (r["distances"] or [[]])[0]
    docs = (r["documents"] or [[]])[0]
    return [
        {"chunk_id": cid, "doc_id": meta["doc_id"], "score": 1 - dist, "text": doc}
        for cid, meta, dist, doc in zip(ids, metas, dists, docs)
    ]
