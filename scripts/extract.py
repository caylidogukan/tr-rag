import csv
import json
import re
import unicodedata
from pathlib import Path

import pymupdf
from bs4 import BeautifulSoup

RAW = Path("data/raw")
OUT = Path("data/processed/docs.jsonl")


def pdf_to_text(path: Path) -> str:
    with pymupdf.open(path) as doc:
        return "\n".join(str(page.get_text("text")) for page in doc)


def html_to_text(path: Path) -> str:
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    main = soup.select_one(".news__detail-article") or soup
    return main.get_text("\n")


def clean(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with (
        open("data/sources.csv", encoding="utf-8") as f,
        open(OUT, "w", encoding="utf-8") as out,
    ):
        for row in csv.DictReader(f):
            path = RAW / row["file"]
            raw = pdf_to_text(path) if path.suffix == ".pdf" else html_to_text(path)
            row["text"] = clean(raw)
            out.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
