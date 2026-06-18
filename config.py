"""Shared settings for the BNH Rules Assistant RAG pipeline."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- Where the Better Not Hundred iOS repo lives (read-only) ---
# Default: sibling folder if you cloned both repos under the same parent directory.
# Override with BNH_REPO_PATH in .env (see .env.example).
_DEFAULT_BNH_REPO = Path(__file__).resolve().parent.parent / "Better Not Hundred"
BNH_REPO = Path(os.getenv("BNH_REPO_PATH", str(_DEFAULT_BNH_REPO)))

DOC_DIRS = [
    BNH_REPO / "docs",
    BNH_REPO / "Documentation",
    BNH_REPO / "Better Not Hundred" / "docs",
]

# --- Local vector store (created by ingest.py; not committed to git) ---
PROJECT_ROOT = Path(__file__).parent
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
COLLECTION_NAME = "bnh_docs_ollama"

# --- RAG tuning ---
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3
EMBED_BATCH_SIZE = 32  # small batches avoid Ollama timeouts on bulk ingest

# --- Ollama (local, free — no API key) ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3.2:3b")
EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
LLM_TEMPERATURE = 0.1

SYSTEM_PROMPT = """You are a helpful assistant for the Better Not Hundred card game.

Rules:
- Answer ONLY using the CONTEXT provided in the user message.
- If the context does not contain the answer, say "I don't have that information in the docs."
- Do NOT invent features, file names, or bug fixes.
- Keep answers concise (3-5 sentences unless the user asks for detail).
- End with a line: Sources: <comma-separated filenames from the context headers>."""
