"""Parse a regulation source file into raw text + header metadata.

Supported inputs:
  - .txt files with a metadata header block (Key: Value lines) followed by
    a blank line and the document body.
  - .pdf files (raw text extraction only; no metadata header available,
    caller must supply metadata separately).
"""
from pathlib import Path

from pypdf import PdfReader

METADATA_KEYS = {
    "Source": "source_name",
    "Source URL": "source_url",
    "Applicable State": "applicable_state",
    "Applicable Industry": "applicable_industry",
    "Regulation Category": "regulation_category",
    "Last Verified Date": "last_verified_date",
    "Effective Date": "effective_date",
}


def parse_txt(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    metadata = {}
    body_start = 0
    for i, line in enumerate(lines):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            if key in METADATA_KEYS:
                metadata[METADATA_KEYS[key]] = value.strip()
                continue
        if line.strip() == "" and metadata:
            body_start = i + 1
            break

    metadata.setdefault("source_name", path.stem)
    metadata.setdefault("source_url", "")
    metadata.setdefault("applicable_state", "central")
    metadata.setdefault("applicable_industry", "all")
    metadata.setdefault("regulation_category", "industry_specific")

    # regulation_category and applicable_industry are used as exact-match
    # filter values (Section 4 schema), so normalize casing at parse time.
    metadata["applicable_industry"] = metadata["applicable_industry"].lower()
    metadata["regulation_category"] = metadata["regulation_category"].lower()

    body = "\n".join(lines[body_start:]).strip()
    return {"metadata": metadata, "text": body}


def parse_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    metadata = {
        "source_name": path.stem,
        "source_url": "",
        "applicable_state": "central",
        "applicable_industry": "all",
        "regulation_category": "industry_specific",
    }
    return {"metadata": metadata, "text": text.strip()}


def parse_document(path: Path) -> dict:
    if path.suffix.lower() == ".pdf":
        return parse_pdf(path)
    if path.suffix.lower() == ".txt":
        return parse_txt(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")
