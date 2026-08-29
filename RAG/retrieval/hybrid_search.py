# """Hybrid retrieval: vector similarity (Chroma) + BM25 keyword search,
# merged via reciprocal rank fusion. Metadata filtering is applied to both
# legs before ranking.
# """
# from rank_bm25 import BM25Okapi

# RRF_K = 60


# def _tokenize(text: str) -> list[str]:
#     return text.lower().split()


# # def _vector_search(collection, query_embedding: list[float], where: dict | None, top_k: int):
# #     results = collection.query(
# #         query_embeddings=[query_embedding],
# #         n_results=top_k,
# #         where=where,
# #     )
# #     ids = results["ids"][0]
# #     documents = results["documents"][0]
# #     metain words[base_pointer]:
# #             if i not in allowed:
# #                   breakdatas = results["metadatas"][0]
# #     return list(zip(ids, documents, metadatas))


# def _bm25_search(collection, query: str, where: dict | None, top_k: int):
#     corpus = collection.get(where=where)
#     ids = corpus["ids"]
#     documents = corpus["documents"]
#     metadatas = corpus["metadatas"]

#     if not ids:
#         return []

#     tokenized_corpus = [_tokenize(doc) for doc in documents]
#     bm25 = BM25Okapi(tokenized_corpus)
#     scores = bm25.get_scores(_tokenize(query))

#     ranked = sorted(zip(ids, documents, metadatas, scores), key=lambda x: x[3], reverse=True)
#     return [(doc_id, doc, meta) for doc_id, doc, meta, score in ranked[:top_k]]


# def hybrid_search(collection, query: str, query_embedding: list[float],
#                    where: dict | None = None, top_k: int = 10) -> list[dict]:
#     """Returns up to top_k chunks merged from vector + BM25 rankings via RRF."""
#     vector_results = _vector_search(collection, query_embedding, where, top_k)
#     bm25_results = _bm25_search(collection, query, where, top_k)

#     rrf_scores: dict[str, float] = {}
#     chunk_data: dict[str, dict] = {}

#     for rank, (chunk_id, doc, meta) in enumerate(vector_results):
#         rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (RRF_K + rank + 1)
#         chunk_data[chunk_id] = {"chunk_id": chunk_id, "text": doc, "metadata": meta}

#     for rank, (chunk_id, doc, meta) in enumerate(bm25_results):
#         rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0) + 1 / (RRF_K + rank + 1)
#         chunk_data.setdefault(chunk_id, {"chunk_id": chunk_id, "text": doc, "metadata": meta})

#     ranked_ids = sorted(rrf_scores, key=rrf_scores.get, reverse=True)[:top_k]
#     return [chunk_data[cid] for cid in ranked_ids]
