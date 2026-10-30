import json

MOJIBAKE = set("ýþðÝÞÐ")

# TODO 1: docs.jsonl'ı listeye yükle ve doküman sayısını yazdır

docs = [
    json.loads(line) for line in open("data/processed/docs.jsonl", encoding="utf-8")
]
print(len(docs))


# TODO 2: ortalama karakter sayısını ve en kısa 3 dokümanı yazdır
#         (çok kısa = muhtemelen taranmış PDF, metin yok)

lengths = [len(d["text"]) for d in docs]
print(f"ortalama karakter: {sum(lengths) / len(lengths):.0f}")

print("en kısa 3 doküman:")
for d in sorted(docs, key=lambda d: len(d["text"]))[:3]:
    print(f"  {len(d['text']):>7}  {d['doc_id']}")


# TODO 3: her dokümanda MOJIBAKE karakterlerini say, varsa uyar
for d in sorted(docs, key=lambda d: len(d["text"])):
    contains_any = bool(set(d["text"]) & MOJIBAKE)
    mojibake_count = sum(1 for char in d["text"] if char in MOJIBAKE)
    if contains_any:
        print(f"MOJIBAKE karakterlerinden var {d['doc_id']}")
    if mojibake_count > 0:
        print(f"Doc ID: {d['doc_id']} | Toplam Mojibake sayısı: {mojibake_count}")
