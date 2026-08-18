"""Structure-aware chunking: split on section/clause headers first,
fall back to paragraph splitting when a section is too large.

Token counts are approximated by word count (close enough for the
300-500 token / ~50 token overlap targets at MVP stage; avoids adding
a tokenizer dependency).
"""
import re

MIN_TOKENS = 300
MAX_TOKENS = 500
OVERLAP_TOKENS = 50

SECTION_HEADER_RE = re.compile(r"(?m)^(Section \d+[:.].*)$")


def _word_count(text: str) -> int:
    return len(text.split())


def _split_into_sections(text: str) -> list[str]:
    matches = list(SECTION_HEADER_RE.finditer(text))
    if not matches:
        return [text]

    sections = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append(text[start:end].strip())
    return sections


def _split_paragraphs_with_overlap(text: str) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return []

    chunks = []
    current_words: list[str] = []
    for para in paragraphs:
        para_words = para.split()
        if current_words and len(current_words) + len(para_words) > MAX_TOKENS:
            chunks.append(" ".join(current_words))
            overlap = current_words[-OVERLAP_TOKENS:] if len(current_words) > OVERLAP_TOKENS else current_words
            current_words = overlap + para_words
        else:
            current_words.extend(para_words)

    if current_words:
        chunks.append(" ".join(current_words))
    return chunks


def chunk_document(text: str) -> list[str]:
    """Split on section headers; further split any section exceeding MAX_TOKENS."""
    sections = _split_into_sections(text)

    chunks: list[str] = []
    for section in sections:
        if _word_count(section) <= MAX_TOKENS:
            chunks.append(section)
        else:
            chunks.extend(_split_paragraphs_with_overlap(section))

    return [c for c in chunks if c.strip()]
