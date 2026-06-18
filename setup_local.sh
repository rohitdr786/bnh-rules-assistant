#!/bin/bash
# One-time setup: ensure .env exists and download Ollama models.
set -e

cd "$(dirname "$0")"

echo "=== BNH Rules Assistant — local setup ==="

if ! command -v ollama &>/dev/null; then
  echo ""
  echo "Ollama is NOT installed."
  echo "  Option A: Download the Mac app → https://ollama.com/download"
  echo "  Option B: brew install ollama"
  echo ""
  echo "After installing, open the Ollama app (or run: ollama serve), then run this script again."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
else
  echo ".env already exists (good)"
fi

echo ""
echo "Downloading models (first time only — may take a few minutes)..."
ollama pull nomic-embed-text
ollama pull llama3.2:3b

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  python ingest.py"
echo "  python ask.py \"How does multiplayer rejoin work?\""
