import json
import re
from collections import Counter

from turkcerag.text import tr_lower


def norm(s: str) -> str:
    norm_text = re.sub(r"\s+", " ", s).strip()
    return tr_lower(norm_text)


def check_unique_ids(filename, id_field="id") -> bool:
    seen_ids = set()
    duplicate_ids = set()

    with open(filename, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue  # Skip empty lines
            try:
                record = json.loads(line)
                record_id = record.get(id_field)

                if record_id is not None:
                    if record_id in seen_ids:
                        duplicate_ids.add(record_id)
                        print(f"Duplicate ID '{record_id}' found on line {line_num}")
                    else:
                        seen_ids.add(record_id)
            except json.JSONDecodeError:
                print(f"Invalid JSON syntax on line {line_num}")

    if not duplicate_ids:
        print(f"Success: All {len(seen_ids)} IDs are completely unique!")
        return True
    else:
        print(
            f"Total unique IDs: {len(seen_ids)}. Total duplicate IDs found: {len(duplicate_ids)}"
        )
        return False


# TODO 1: docs.jsonl'dan {doc_id: norm(text)} sözlüğü kur
doc_dict = {}

with open("data/processed/docs.jsonl", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        doc = json.loads(line)

        # Use .get() to avoid KeyErrors if a field is missing
        doc_id = doc.get("doc_id")
        text = doc.get("text", "")

        if doc_id is not None:
            doc_dict[doc_id] = norm(text)
# TODO 2: questions.jsonl'ı satır satır oku ve şunları kontrol et:
#   - id'ler benzersiz mi
#   - answerable ise: doc_id var mı, norm(evidence) o dokümanın metninde geçiyor mu
#   - answerable değilse: evidence boş mu
if not check_unique_ids("eval/questions.jsonl", "id"):
    print("Unique id'ler benzersiz değil")

types = Counter()
errors = []
with open("eval/questions.jsonl", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        question = json.loads(line)
        types[question.get("type")] += 1
        question_doc_id = question.get("doc_id")
        if question.get("answerable") == True:
            doc_text = doc_dict[question_doc_id]
            norm_evidence = norm(question.get("evidence"))

            if norm_evidence not in doc_text:
                errors.append(f"{question.get('id')}: evidence metinde geçmiyor")
        else:
            print("Evidence boş") if question.get("evidence") else None

# TODO 3: type dağılımını ve bulunan hataları yazdır
print(sum(types.values()), "soru", dict(types))
print("\n".join(errors) or "Hata yok")