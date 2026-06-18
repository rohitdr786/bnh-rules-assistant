"""Step 2 (offline): Embed chunks and persist in ChromaDB."""

import shutil
import time

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

import config
from rag.ollama_utils import ensure_ollama_running


def _embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=config.EMBEDDING_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )


def _add_batch_with_retry(
    vectorstore: Chroma | None,
    batch: list[Document],
    embeddings: OllamaEmbeddings,
) -> Chroma:
    """Embed one batch; retry on transient Ollama connection errors."""
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            if vectorstore is None:
                return Chroma.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    collection_name=config.COLLECTION_NAME,
                    persist_directory=str(config.CHROMA_DIR),
                )
            vectorstore.add_documents(batch)
            return vectorstore
        except Exception as exc:
            last_error = exc
            wait = 2**attempt
            print(f"    Batch failed (attempt {attempt}/3): {exc}")
            print(f"    Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"Failed to embed batch after 3 attempts: {last_error}") from last_error


def build_vector_store(chunks: list[Document]) -> Chroma:
    """
    Embed each chunk and save vectors locally via Ollama.

    Processes in small batches so Ollama doesn't time out on ~2800 chunks.
    """
    ensure_ollama_running()
    embeddings = _embeddings()

    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)
    config.CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    total = len(chunks)
    batch_size = config.EMBED_BATCH_SIZE
    vectorstore: Chroma | None = None

    print(f"  Embedding in batches of {batch_size} ({total} chunks total)...")

    for start in range(0, total, batch_size):
        batch = chunks[start : start + batch_size]
        vectorstore = _add_batch_with_retry(vectorstore, batch, embeddings)
        done = min(start + batch_size, total)
        print(f"  Progress: {done}/{total} chunks ({100 * done // total}%)")

    if vectorstore is None:
        raise ValueError("No chunks to embed.")

    return vectorstore


def load_vector_store() -> Chroma:
    """Load an existing Chroma index (run ingest.py first)."""
    if not config.CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"No vector store at {config.CHROMA_DIR}. Run: python ingest.py"
        )

    ensure_ollama_running()
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=_embeddings(),
        persist_directory=str(config.CHROMA_DIR),
    )
