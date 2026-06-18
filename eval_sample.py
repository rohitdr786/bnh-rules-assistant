#!/usr/bin/env python3
"""
Quick sanity check: run a few questions and verify expected keywords appear.

Usage:
    python eval_sample.py
"""

from dotenv import load_dotenv

from rag.query import answer_question

load_dotenv()

# (question, keywords that should appear if retrieval + generation worked)
SAMPLES = [
    (
        "How does multiplayer rejoin work after force-closing the app?",
        ["rejoin", "currentTurnPhase"],
    ),
    (
        "What was the Firebase listener architecture overhaul about?",
        ["listener", "ghost"],
    ),
    (
        "What happens when a player shows on their first turn?",
        ["show", "turn"],
    ),
]


def main() -> None:
    passed = 0
    for question, keywords in SAMPLES:
        print(f"\nQ: {question}")
        response = answer_question(question)
        answer = response.answer.lower()
        print(f"A: {answer[:200]}...")

        missing = [kw for kw in keywords if kw.lower() not in answer]
        if missing:
            print(f"  ⚠ Missing keywords: {missing}")
        else:
            print("  ✓ Keywords found")
            passed += 1

    print(f"\n{passed}/{len(SAMPLES)} samples passed keyword check")


if __name__ == "__main__":
    main()
