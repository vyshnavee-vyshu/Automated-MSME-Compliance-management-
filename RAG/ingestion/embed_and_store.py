"""Embed chunks with OpenAI text-embedding-3-small and store them in Chroma
with the required citation/filter metadata attached.
"""
import os
import uuid

import chromadb
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "regulations"


def get_chroma_collection():
    persist_dir = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_db")
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def store_chunks(collection, chunks: list[str], doc_metadata: dict, source_file: str):
    if not chunks:
        return

    embeddings = embed_texts(chunks)

    ids = []
    metadatas = []
    for chunk_text in chunks:
        chunk_id = f"{source_file}-{uuid.uuid4().hex[:8]}"
        ids.append(chunk_id)
        metadatas.append(
            {
                "chunk_id": chunk_id,
                "source_name": doc_metadata["source_name"],
                "source_url": doc_metadata.get("source_url", ""),
                "last_verified_date": doc_metadata.get("last_verified_date", ""),
                "effective_date": doc_metadata.get("effective_date", ""),
                "regulation_category": doc_metadata.get("regulation_category", "industry_specific"),
                "applicable_state": doc_metadata.get("applicable_state", "central"),
                "applicable_industry": doc_metadata.get("applicable_industry", "all"),
            }
        )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
