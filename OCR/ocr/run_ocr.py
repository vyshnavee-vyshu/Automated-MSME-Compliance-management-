"""Phase 1 orchestrator: run OCR extraction over every file in
data/sample_docs and write per-document JSON to output/.

Usage:
    python -m ocr.run_ocr
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ocr.extract_text import extract_document

SAMPLE_DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_docs"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".bmp", ".tiff"}


def main():
    files = sorted(p for p in SAMPLE_DOCS_DIR.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS)
    if not files:
        print(f"No documents found in {SAMPLE_DOCS_DIR}")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    for path in files:
        print(f"\n--- Extracting {path.name} ---")
        result = extract_document(str(path))

        for page in result["pages"]:
            print(f"  page {page['page_num']}: {len(page['lines'])} lines")
            if page["low_confidence_lines"]:
                print(f"    ⚠ {len(page['low_confidence_lines'])} low-confidence line(s): "
                      f"{page['low_confidence_lines']}")
            preview = page["full_text"][:200].replace("\n", " | ")
            print(f"  preview: {preview}...")

        out_path = OUTPUT_DIR / f"{path.stem}.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"  saved -> {out_path}")


if __name__ == "__main__":
    main()
