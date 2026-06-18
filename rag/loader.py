"""Step 0 (offline): Load markdown files from the Better Not Hundred repo."""

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

import config


def _existing_doc_dirs() -> list[Path]:
    return [d for d in config.DOC_DIRS if d.is_dir()]


def load_markdown_docs() -> list[Document]:
    """Load all .md files from configured BNH documentation folders."""
    dirs = _existing_doc_dirs()
    if not dirs:
        raise FileNotFoundError(
            "No documentation folders found. Check BNH_REPO in config.py:\n"
            + "\n".join(f"  - {d}" for d in config.DOC_DIRS)
        )

    all_docs: list[Document] = []
    for doc_dir in dirs:
        loader = DirectoryLoader(
            str(doc_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
            use_multithreading=True,
        )
        all_docs.extend(loader.load())

    if not all_docs:
        raise ValueError(f"No .md files found under: {[str(d) for d in dirs]}")

    return all_docs
