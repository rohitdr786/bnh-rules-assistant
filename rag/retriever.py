"""Step 3 (online): Retrieve the most relevant chunks for a question."""

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

import config


def retrieve_relevant_chunks(
    vectorstore: Chroma,
    question: str,
    k: int | None = None,
) -> list[Document]:
    """
    RETRIEVE step: embed the question, find top-k similar chunks.

    This is semantic search — "ghost rejoin" can match "listener duplicate session"
    even if the words differ.
    """
    top_k = k or config.TOP_K
    return vectorstore.similarity_search(question, k=top_k)


def format_context(chunks: list[Document]) -> str:
    """
    AUGMENT (part 1): Format retrieved chunks for the prompt.

    Each chunk is labeled with its source file so the LLM (and user) can cite it.
    """
    sections: list[str] = []
    for i, doc in enumerate(chunks, start=1):
        source = doc.metadata.get("source", "unknown")
        sections.append(f"--- Chunk {i} (source: {source}) ---\n{doc.page_content.strip()}")
    return "\n\n".join(sections)
