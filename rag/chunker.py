"""Step 1 (offline): Split documents into retrieval-sized chunks."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Split long markdown files into smaller chunks.

    Why: A 50-page doc won't match a specific question well. Chunks let us
    retrieve the paragraph about "rejoin" instead of the whole project status.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    return splitter.split_documents(documents)
