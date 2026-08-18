"""Orchestrates ingestion: parse -> chunk -> embed -> store for every
file in data/raw_docs.

Usage:
    python -m ingestion.run_ingestion
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
load_dotenv()

from ingestion.chunk import chunk_document
from ingestion.embed_and_store import get_chroma_collection, store_chunks
from ingestion.parse import parse_document

RAW_DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "raw_docs"


def main():
    files = sorted(list(RAW_DOCS_DIR.glob("*.txt")) + list(RAW_DOCS_DIR.glob("*.pdf")))
    if not files:
        print(f"No documents found in {RAW_DOCS_DIR}")
        return

    collection = get_chroma_collection()

    for path in files:
        print(f"\n--- Ingesting {path.name} ---")
        parsed = parse_document(path)
        chunks = chunk_document(parsed["text"])
        print(f"  {len(chunks)} chunks created")
        for i, c in enumerate(chunks[:2]):
            print(f"  [chunk {i}] ({len(c.split())} words): {c[:120]}...")

        store_chunks(collection, chunks, parsed["metadata"], source_file=path.stem)
        print(f"  Stored {len(chunks)} chunks with metadata: "
              f"state={parsed['metadata']['applicable_state']}, "
              f"industry={parsed['metadata']['applicable_industry']}, "
              f"category={parsed['metadata']['regulation_category']}")

    print(f"\nDone. Collection now has {collection.count()} chunks total.")


if __name__ == "__main__":
    main()
