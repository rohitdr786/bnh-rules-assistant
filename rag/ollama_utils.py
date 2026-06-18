"""Helpers to verify Ollama is running before we call it."""

import urllib.error
import urllib.request

import config


def ensure_ollama_running() -> None:
    """Raise a clear error if Ollama is not reachable."""
    try:
        urllib.request.urlopen(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=3)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ConnectionError(
            "Ollama is not running.\n\n"
            "1. Install: https://ollama.com/download (or: brew install ollama)\n"
            "2. Start the Ollama app (menu bar icon on Mac), or run: ollama serve\n"
            "3. Pull models: ./setup_local.sh\n"
        ) from exc
