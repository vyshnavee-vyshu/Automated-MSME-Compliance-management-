"""Rerank the merged hybrid results with bge-reranker-base (local,
no extra API cost) and return the top N chunks to send to the LLM.
"""
from sentence_transformers import CrossEncoder

FINAL_TOP_N = 4

_model = None


def _get_model() -> CrossEncoder:
    global _model
    if _model is None:
        _model = CrossEncoder("BAAI/bge-reranker-base")
    return _model


def rerank(query: str, chunks: list[dict], top_n: int = FINAL_TOP_N) -> list[dict]:
    if not chunks:
        return []

    model = _get_model()
    pairs = [[query, chunk["text"]] for chunk in chunks]
    scores = model.predict(pairs)

    scored = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    return [chunk for chunk, score in scored[:top_n]]
