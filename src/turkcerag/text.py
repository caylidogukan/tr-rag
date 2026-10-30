def tr_lower(s: str) -> str:
    translation_table = str.maketrans({"I": "ı", "İ": "i"})
    clean_text = s.translate(translation_table)
    return clean_text.lower()


def norm(s: str) -> str:
    return " ".join(tr_lower(s).split())


def is_relevant(chunk: dict, q: dict) -> bool:
    if chunk["doc_id"] == q["doc_id"] and norm(q["evidence"]) in norm(chunk["text"]):
        return True
    else:
        return False


assert tr_lower("İSTANBUL") == "istanbul"
assert tr_lower("ISPARTA") == "ısparta"
