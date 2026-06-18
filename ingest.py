#!/usr/bin/env python3
"""
Offline ingestion: load docs → chunk → embed → store in ChromaDB.

Run once (or again when BNH docs change):
    python ingest.py
"""

from dotenv import load_dotenv

from rag.chunker import chunk_documents
from rag.loader import load_markdown_docs
from rag.store import build_vector_store

load_dotenv()


def main() -> None:
    print("Loading markdown from Better Not Hundred...")
    docs = load_markdown_docs()
    print(f"  Loaded {len(docs)} files")

    print("Chunking...")
    chunks = chunk_documents(docs)
    print(f"  Created {len(chunks)} chunks")

    print("Embedding and saving to ChromaDB...")
    build_vector_store(chunks)
    print("Done. Vector store ready. Run: python ask.py")


if __name__ == "__main__":
    main()
