"""Turns raw PaddleOCR line output into a per-document, per-page text
structure — the input Phase 2 (LLM structured field extraction) will
consume.
"""
from pathlib import Path

from ocr.engine import run_ocr

LOW_CONFIDENCE_THRESHOLD = 0.5


def extract_document(file_path: str) -> dict:
    path = Path(file_path)
    pages = run_ocr(str(path))

    page_results = []
    for i, lines in enumerate(pages):
        full_text = "\n".join(line["text"] for line in lines)
        low_confidence_lines = [
            line["text"] for line in lines if line["confidence"] < LOW_CONFIDENCE_THRESHOLD
        ]
        page_results.append({
            "page_num": i + 1,
            "lines": lines,
            "full_text": full_text,
            "low_confidence_lines": low_confidence_lines,
        })

    return {
        "source_file": path.name,
        "page_count": len(page_results),
        "pages": page_results,
    }
