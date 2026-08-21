"""Cheap keyword-based document type classification — no LLM call needed
for this step, keeps the pipeline fast and deterministic.
"""

LABOUR_KEYWORDS = [
    "epf", "uan", "esi", "provident fund", "shops and establishment",
    "labour", "labor", "employer", "establishment", "gratuity",
    "minimum wage", "factory license", "contractor",
]

TAXATION_KEYWORDS = [
    "gstin", "goods and services tax", "pan", "tan", "income tax",
    "tds", "gst return", "assessment year", "financial year",
    "input tax credit", "challan",
]


def classify_document(raw_text: str) -> str:
    """Returns 'labour', 'taxation', or 'unknown' based on keyword hits."""
    text = raw_text.lower()

    labour_score = sum(1 for kw in LABOUR_KEYWORDS if kw in text)
    taxation_score = sum(1 for kw in TAXATION_KEYWORDS if kw in text)

    if labour_score == 0 and taxation_score == 0:
        return "unknown"
    return "labour" if labour_score >= taxation_score else "taxation"
