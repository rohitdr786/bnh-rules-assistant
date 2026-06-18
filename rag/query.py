"""High-level RAG query: retrieve → augment → generate with structured output."""

from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document

from rag.generate import build_user_message, generate_answer
from rag.retriever import format_context, retrieve_relevant_chunks
from rag.store import load_vector_store

load_dotenv()


@dataclass
class RAGResponse:
    answer: str
    sources: list[str] = field(default_factory=list)
    chunks: list[Document] = field(default_factory=list)
    prompt: str | None = None


def source_label(path: str) -> str:
    """Show a short filename instead of the full path."""
    return Path(path).name


def answer_question(question: str, *, include_prompt: bool = False) -> RAGResponse:
    vectorstore = load_vector_store()
    chunks = retrieve_relevant_chunks(vectorstore, question)
    context = format_context(chunks)
    answer = generate_answer(question, context)

    sources = []
    seen = set()
    for doc in chunks:
        label = source_label(doc.metadata.get("source", "unknown"))
        if label not in seen:
            seen.add(label)
            sources.append(label)

    prompt = None
    if include_prompt:
        prompt = build_user_message(question, context)

    return RAGResponse(
        answer=answer,
        sources=sources,
        chunks=chunks,
        prompt=prompt,
    )
