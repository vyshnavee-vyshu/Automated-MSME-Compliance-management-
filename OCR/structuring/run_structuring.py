"""Phase 2 orchestrator: reads every Phase 1 OCR result JSON from
output/ and writes structured, schema-validated field extractions to
output/structured/.

Usage:
    python -m structuring.run_structuring
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

from structuring.structure_document import structure_ocr_result

OCR_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
STRUCTURED_OUTPUT_DIR = OCR_OUTPUT_DIR / "structured"


def main():
    ocr_files = sorted(OCR_OUTPUT_DIR.glob("*.json"))
    if not ocr_files:
        print(f"No OCR results found in {OCR_OUTPUT_DIR}. Run `python -m ocr.run_ocr` first.")
        return

    STRUCTURED_OUTPUT_DIR.mkdir(exist_ok=True)

    for path in ocr_files:
        ocr_result = json.loads(path.read_text())
        print(f"\n--- Structuring {ocr_result['source_file']} ---")

        result = structure_ocr_result(ocr_result)

        if result["error"]:
            print(f"  ⚠ {result['error']}")
        else:
            print(f"  document_type: {result['document_type']}")
            filled = {k: v for k, v in result["fields"].items() if v is not None}
            print(f"  {len(filled)}/{len(result['fields'])} fields filled")
            for k, v in filled.items():
                print(f"    {k}: {v}")

        out_path = STRUCTURED_OUTPUT_DIR / path.name
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"  saved -> {out_path}")


if __name__ == "__main__":
    main()
