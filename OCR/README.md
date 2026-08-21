# OCR + Structured Field Extraction (Document Auto-Extractor)

Two-phase pipeline: OCR raw text out of uploaded compliance documents,
then structure that text into the exact Labour/Taxation compliance
field schema, validated and never hallucinated.

## Setup

```bash
cd OCR
uv venv --python 3.12 .venv   # PaddlePaddle has no Python 3.14 wheels yet
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env          # fill in GROQ_API_KEY
```

## Phase 1 — OCR extraction

```bash
python scripts/make_sample_doc.py   # generates synthetic test docs (no real scans yet)
python -m ocr.run_ocr
```

Reads every image/PDF in `data/sample_docs/`, runs PaddleOCR PP-OCRv5
(mobile, CPU, doc-orientation + unwarping enabled for phone photos),
writes per-document JSON to `output/` — full text per page plus any
low-confidence (<0.5) lines flagged.

## Phase 2 — Structured field extraction

```bash
python -m structuring.run_structuring
```

Reads Phase 1's `output/*.json`, classifies each document as
`labour` or `taxation` (keyword heuristic, no LLM cost), then calls
Groq to fill the matching Pydantic schema
(`structuring/schemas.py` — 35 labour fields, 33 taxation fields).
Fields not found in the OCR text stay `null` — the model is
instructed never to guess. Output written to `output/structured/`.

## Notes

- OCR text is treated as untrusted data in the extraction prompt, never
  as instructions (prompt-injection defense).
- `enable_mkldnn` must stay `False` in `ocr/engine.py` — `True` crashes
  on this Paddle build (oneDNN PIR bug), see comment in that file.
- This module only produces structured JSON; storing it (PostgreSQL)
  and wiring it into the RAG chatbot's business profile is a later step.
