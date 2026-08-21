"""Orchestrates Phase 2 for a single OCR result: classify document type,
call the LLM against the matching schema, validate with Pydantic.
"""
from pydantic import ValidationError

from structuring.classify import classify_document
from structuring.llm_client import extract_fields
from structuring.schemas import SCHEMAS


def _coerce_to_strings(raw_fields: dict) -> dict:
    """LLMs routinely return JSON numbers/booleans for fields like
    number_of_employees or turnover despite the string schema. Coerce
    scalars to str rather than failing validation over a type mismatch —
    the goal is not to discard a correctly-extracted value.
    """
    coerced = {}
    for key, value in raw_fields.items():
        if value is None or isinstance(value, str):
            coerced[key] = value
        else:
            coerced[key] = str(value)
    return coerced


def structure_ocr_result(ocr_result: dict) -> dict:
    """ocr_result is one document's Phase 1 output (from ocr/run_ocr.py):
    {"source_file": str, "page_count": int, "pages": [...]}
    """
    full_text = "\n".join(page["full_text"] for page in ocr_result["pages"])
    doc_type = classify_document(full_text)

    if doc_type == "unknown":
        return {
            "source_file": ocr_result["source_file"],
            "document_type": "unknown",
            "fields": None,
            "error": "Could not classify document as labour or taxation — no matching keywords found.",
        }

    schema_cls = SCHEMAS[doc_type]
    schema_fields = {name: None for name in schema_cls.model_fields}

    try:
        raw_fields = extract_fields(full_text, schema_fields)
    except Exception as e:
        return {
            "source_file": ocr_result["source_file"],
            "document_type": doc_type,
            "fields": None,
            "error": f"LLM extraction failed: {e}",
        }

    try:
        validated = schema_cls(**_coerce_to_strings(raw_fields))
        return {
            "source_file": ocr_result["source_file"],
            "document_type": doc_type,
            "fields": validated.model_dump(),
            "error": None,
        }
    except ValidationError as e:
        return {
            "source_file": ocr_result["source_file"],
            "document_type": doc_type,
            "fields": None,
            "error": f"Validation failed: {e}",
        }
