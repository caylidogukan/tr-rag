# TürkçeRAG

KVKK mevzuatı ve Kurul kararları üzerinde Türkçe RAG ve yayınlanmış bir değerlendirme.

## Sonuçlar

42 cevaplanabilir soru, retrieval metrikleri.

| Yöntem | chunk | recall@5 | MRR |
|---|---|---|---|
| Azure embedding (M3 baseline) | 512 | 0.571 | 0.401 |

## Nasıl çalıştırılır

Gereksinimler: [uv](https://docs.astral.sh/uv/) ve bir Azure OpenAI kaynağında chat ve embedding deployment'ları.

Bağımlılıkları kur:

```
uv sync
```

Proje klasöründe veya üst klasörlerinden birinde bir `.env` dosyası oluştur (git'e girmez):

```
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION=...
AZURE_OPENAI_CHAT_DEPLOYMENT=...
AZURE_OPENAI_EMBED_DEPLOYMENT=...
```

Komutları proje kökünden çalıştır:

```
uv run python scripts/validate_eval.py            # eval setini doğrula
uv run python scripts/chunk.py                    # docs.jsonl -> chunks_512.jsonl
uv run python scripts/check_chunks.py             # kanıtlar chunk'lara sığıyor mu
uv run python scripts/index.py                    # embedding + Chroma (Azure çağrısı yapar)
uv run python scripts/search.py "sorgunuz"        # tek sorguyla arama
uv run python scripts/eval_retrieval.py           # recall@5 ve MRR -> results/azure-512.json
```

Farklı chunk boyutu denemek için `chunk.py --size 256 --overlap 32`, ardından `check_chunks.py --size 256`.

Notlar:

- `data/processed/docs.jsonl` repoda hazır. Ham dosyalar (`data/raw/`) repoda yok; `scripts/extract.py` yalnızca ham dosyalar elindeyse çalışır. Kaynak listesi `data/sources.csv` içinde.
- `chunks_*.jsonl` ve `data/chroma/` repoda yok, yukarıdaki komutlarla yeniden üretilir.
- `index.py` 344 chunk için yaklaşık 140 bin token embed eder, maliyeti birkaç sent.
- Hata analizi için bkz. `notes/m3.md`.
