#!/usr/bin/env python3
"""
Online Q&A: retrieve → augment → generate.

Usage:
    python ask.py "How does multiplayer rejoin work?"
    python ask.py   # interactive mode
"""

import sys

from dotenv import load_dotenv

from rag.generate import build_user_message
from rag.query import answer_question

load_dotenv()


def main() -> None:
    show_prompt = "--show-prompt" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--show-prompt"]

    if args:
        question = " ".join(args)
        response = answer_question(question, include_prompt=show_prompt)
        print(response.answer)
        if response.sources:
            print("\nSources:", ", ".join(response.sources))
        if show_prompt and response.prompt:
            print("\n--- Prompt sent to LLM (user message) ---\n")
            print(response.prompt)
            print("\n--- End prompt ---\n")
        return

    print("BNH Rules Assistant (type 'quit' to exit)")
    print("Tip: run with --show-prompt to see the full RAG prompt")
    print("Web UI: streamlit run app.py\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not question:
            continue
        if question.lower() in {"quit", "exit", "q"}:
            break

        print("\nAssistant:")
        response = answer_question(question, include_prompt=show_prompt)
        print(response.answer)
        if response.sources:
            print("Sources:", ", ".join(response.sources))
        print()


if __name__ == "__main__":
    main()
