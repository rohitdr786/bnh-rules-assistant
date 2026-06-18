# BNH Rules Assistant

A **local RAG (Retrieval-Augmented Generation)** chatbot that answers questions about the [Better Not Hundred](https://github.com/rohitdr786/BetterNotHundred) iOS card game using its technical documentation.

Built as a learning/portfolio project to demonstrate: document ingestion, vector search, prompt augmentation, and grounded LLM generation — all running **free on your machine** via [Ollama](https://ollama.com).

## Features

- Indexes 110+ markdown files from the BNH `docs/` and `Documentation/` folders
- **CLI** (`ask.py`) and **Streamlit web UI** (`app.py`)
- Source-cited answers with retrieved excerpt preview
- 100% local — no OpenAI key, no cloud cost
- Batched embedding ingest with retry (handles ~2,800 chunks reliably)

## Will it run automatically on GitHub?

**No.** Pushing to GitHub only stores the **source code**. It does not host or run the app.

| What GitHub gives you | What you run locally |
|-----------------------|----------------------|
| Public repo + README for portfolio | Ollama (LLM + embeddings) |
| Clone instructions for others | `python ingest.py` (build search index) |
| | `streamlit run app.py` (web UI) |

Anyone who clones this repo must install Ollama, point `BNH_REPO_PATH` at the game repo, run ingest, then start the UI on **their** machine.

For a **live public demo URL**, you'd need a separate deploy step (e.g. Hugging Face Spaces with a cloud API instead of local Ollama) — that's Phase 4, not included here.

## Architecture

```
Markdown docs (BNH repo)
        ↓  ingest.py
   Chunk → Embed (Ollama) → ChromaDB (local)
        ↓  ask.py / app.py
   Question → Retrieve top-k chunks → Build prompt → Generate (Ollama)
```

## Prerequisites

- **Python 3.11+**
- **[Ollama](https://ollama.com/download)** installed and running
- **[Better Not Hundred](https://github.com/rohitdr786/BetterNotHundred)** cloned locally (for documentation source files)

Recommended folder layout (sibling repos — works with zero config):

```
~/Documents/GitHub/
├── Better Not Hundred/      ← game repo (docs source)
└── bnh-rules-assistant/     ← this repo
```

## Quick start

### 1. Install Ollama and pull models

```bash
# Install from https://ollama.com/download, then:
chmod +x setup_local.sh
./setup_local.sh
```

Downloads `nomic-embed-text` (embeddings) and `llama3.2:3b` (chat).

### 2. Python environment

```bash
cd bnh-rules-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional; edit BNH_REPO_PATH if needed
```

### 3. Configure doc path (if not using sibling layout)

Edit `.env`:

```bash
BNH_REPO_PATH=/full/path/to/Better Not Hundred
```

### 4. Index documentation

```bash
python ingest.py
```

First run embeds ~2,877 chunks in batches — expect **10–15 minutes**.

### 5. Run

**Web UI (recommended):**

```bash
streamlit run app.py
```

Open http://localhost:8501

**CLI:**

```bash
python ask.py "What was fixed in BNH-14 for rejoin?"
python ask.py --show-prompt "How does multiplayer rejoin work?"
```

## Project structure

```
bnh-rules-assistant/
├── app.py              Streamlit web chat UI
├── ask.py              CLI Q&A
├── ingest.py           Build vector index from BNH docs
├── config.py           Paths, models, RAG settings
├── setup_local.sh      Pull Ollama models
├── eval_sample.py      Simple keyword sanity checks
├── rag/
│   ├── loader.py       Load markdown files
│   ├── chunker.py      Split into chunks
│   ├── store.py        ChromaDB + batched Ollama embeddings
│   ├── retriever.py    Semantic search
│   ├── generate.py     Ollama LLM call
│   ├── query.py        End-to-end RAG with sources
│   └── ollama_utils.py Connection checks
└── data/chroma/        Local vector index (gitignored)
```

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `BNH_REPO_PATH` | `../Better Not Hundred` | Path to game repo |
| `OLLAMA_LLM_MODEL` | `llama3.2:3b` | Chat model |
| `OLLAMA_EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server |

For better answer quality (more RAM): set `OLLAMA_LLM_MODEL=llama3.2` in `.env`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Ollama is not running` | Open Ollama app or run `ollama serve` |
| `No vector store` | Run `python ingest.py` |
| `No documentation folders found` | Set `BNH_REPO_PATH` in `.env` |
| Ingest timeout | Restart Ollama: `brew services restart ollama` |
| Slow first answer | Normal — model loads into RAM once |

## Tech stack

- Python, LangChain, ChromaDB, Streamlit
- Ollama (`llama3.2:3b`, `nomic-embed-text`)
- Source docs from [Better Not Hundred](https://github.com/rohitdr786/BetterNotHundred)

## License

MIT (or adjust as you prefer)

## Related

- Game repo: [BetterNotHundred](https://github.com/rohitdr786/BetterNotHundred)
- Built by [Rohit Raul](https://github.com/rohitdr786) as a Gen AI / RAG learning project
