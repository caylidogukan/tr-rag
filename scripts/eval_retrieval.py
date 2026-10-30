import json
from pathlib import Path

from turkcerag.retrieve import search
from turkcerag.text import is_relevant

K = 10
SIZE = 512
COLLECTION = f"azure-{SIZE}"

qs = [json.loads(l) for l in Path("eval/questions.jsonl").open(encoding="utf-8")]
rows = []
for q in qs:
    hits = search(q["question"], k=K, size=SIZE)
    rank = None
    if q["answerable"]:
        # TODO 1: hits içinde is_relevant olan İLK sonucun sırasını bul (1'den başlayarak).
        #         Hiçbiri değilse rank None kalır.

        for index, hit in enumerate(hits, start=1):
            if is_relevant(hit, q):
                rank = index
                break

    rows.append(
        {
            "id": q["id"],
            "type": q["type"],
            "answerable": q["answerable"],
            "rank": rank,
            "top1_score": hits[0]["score"],
            "top1_doc": hits[0]["doc_id"],
        }
    )


# TODO 2: cevaplanabilir sorular için recall@5 ve MRR hesapla, yazdır
def metrics(rs):
    rs = [r for r in rs if r["answerable"]]
    return {
        "n": len(rs),
        "recall@5": round(
            sum(1 for r in rs if r["rank"] and r["rank"] <= 5) / len(rs), 3
        ),
        "mrr": round(sum(1 / r["rank"] for r in rs if r["rank"]) / len(rs), 3),
    }


# TODO 3: aynı iki metriği type bazında yazdır (dogrudan / parafraz / sayisal)
# TODO 4: ortalama top1_score'u cevaplanabilir ve cevapsız sorular için ayrı ayrı yazdır
# TODO 5: {"collection", "metrics", "rows"} yapısını results/{COLLECTION}.json'a kaydet
m = {"all": metrics(rows)}
for t in ("dogrudan", "parafraz", "sayisal"):
    m[t] = metrics([r for r in rows if r["type"] == t])
for name, v in m.items():
    print(f"{name:10} n={v['n']:2}  recall@5={v['recall@5']:.3f}  MRR={v['mrr']:.3f}")

for label, flag in (("cevaplanabilir", True), ("cevapsız", False)):
    s = [r["top1_score"] for r in rows if r["answerable"] is flag]
    print(f"ortalama top1 skoru · {label}: {sum(s) / len(s):.3f}")

out = Path(f"results/{COLLECTION}.json")
out.parent.mkdir(exist_ok=True)
out.write_text(
    json.dumps(
        {"collection": COLLECTION, "metrics": m, "rows": rows},
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
