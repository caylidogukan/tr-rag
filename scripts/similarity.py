import numpy as np

from turkcerag.llm import EMBED_MODEL, get_client

cumleler = [
    "Kişisel verilerin silinmesi",
    "Veri imha politikası",
    "Bugün hava çok güzel",
]

client = get_client()

resp = client.embeddings.create(model=EMBED_MODEL, input=cumleler)

vecs = [np.array(d.embedding) for d in resp.data]

def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
  
print("1-2:", round(cosine(vecs[0], vecs[1]), 3))
print("1-3:", round(cosine(vecs[0], vecs[2]), 3))
print("2-3:", round(cosine(vecs[1], vecs[2]), 3))