import tiktoken

ENC = tiktoken.get_encoding("cl100k_base")


def n_tokens(s: str) -> int:
    return len(ENC.encode(s))


def split_long(line: str, size: int) -> list[str]:
    """size'tan uzun tek bir satırı kelime sınırından parçalara böler."""
    parts, cur = [], []
    for w in line.split():
        if cur and n_tokens(" ".join(cur + [w])) > size:
            parts.append(" ".join(cur))
            cur = []
        cur.append(w)
    if cur:
        parts.append(" ".join(cur))
    return parts


def chunk_text(text: str, size: int = 512, overlap: int = 64) -> list[str]:
    # TODO 1: metni satırlara böl, boş satırları at. size'tan uzun satırları
    #         split_long ile parçala. Sonuç: units listesi
    units = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if n_tokens(line) > size:
            units.extend(split_long(line, size))
        else:
            units.append(line)
    chunks, cur, cur_tok = [], [], 0
    for u in units:
        t = n_tokens(u)
        # TODO 2: cur doluysa ve cur_tok + t > size ise:
        #   - "\n".join(cur) değerini chunks'a ekle
        #   - cur'un sonundan geriye doğru giderek toplamı overlap'i geçmeyen
        #     satırları tail listesine al (sıralarını koru)
        #   - tail + u yine size'ı aşıyorsa tail'i boşalt
        #   - cur, cur_tok = tail, tail'in token toplamı
        if cur and cur_tok + t > size:
            chunks.append("\n".join(cur))
            tail, tail_tok = [], 0
            for prev in reversed(cur):
                pt = n_tokens(prev)
                if tail_tok + pt > overlap:
                    break
                tail.insert(0, prev)
                tail_tok += pt

            if tail_tok + t > size:
                tail, tail_tok = [], 0
            cur, cur_tok = tail, tail_tok
        # TODO 3: u'yu cur'a ekle, cur_tok'u güncelle
        cur.append(u)
        cur_tok += t

    # TODO 4: döngü bitince cur'da kalanı da chunks'a ekle
    if cur:
        chunks.append("\n".join(cur))
    return chunks
