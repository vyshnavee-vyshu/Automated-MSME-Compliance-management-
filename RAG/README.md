# MSME Compliance Copilot — RAG Chatbot

Answers MSME compliance questions grounded only in a curated regulation
database, filtered to the business's state/industry, with mandatory
source citations.

## Setup

```bash
cd RAG
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # already done — just fill in the keys below
```

Fill in `.env`:
- `OPENAI_API_KEY` — used for embeddings (`text-embedding-3-small`)
- `GROQ_API_KEY` — used for generation (Groq's OpenAI-compatible API)
- `GROQ_MODEL` — defaults to `llama-3.3-70b-versatile`

## Run ingestion (Phase 1)

Ingests every file in `data/raw_docs/` into the local Chroma store:

```bash
python -m ingestion.run_ingestion
```

The three sample regulation docs in `data/raw_docs/` are illustrative
demo content (labor, environmental/fire-safety, taxation for Tamil
Nadu/central), not scraped official filings — swap in real regulation
PDFs/text there for production use, keeping the same metadata header
format (see any `.txt` file for the convention).

## Run the API + demo UI (Phase 4)

```bash
uvicorn api.main:app --reload
```

- Chat UI: http://localhost:8000/
- API: `POST /chat` with `{"business_id": "biz_001", "question": "..."}`

Sample business profiles are in `profiles/sample_profiles.json`
(`biz_001`: Tamil Nadu manufacturer, `biz_002`: Tamil Nadu services, 8
employees) — retrieval filters by each profile's state/industry before
ranking.

## Notes

- Generation uses Groq (not Anthropic) per project decision — see
  `generation/llm_client.py`. Swap the client there if that changes.
- The reranker (`BAAI/bge-reranker-base`) downloads on first use.
