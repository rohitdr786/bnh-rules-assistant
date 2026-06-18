#!/usr/bin/env python3
"""
Streamlit chat UI for the BNH Rules Assistant.

Run:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from rag.query import RAGResponse, answer_question, source_label
from rag.store import load_vector_store

load_dotenv()

EXAMPLE_QUESTIONS = [
    "What was fixed in BNH-14 for force-close rejoin?",
    "How does the stale discard race condition work?",
    "What is the Firebase listener architecture overhaul?",
    "How does single-player AI difficulty work?",
    "What happens when a player shows on their first turn?",
]

st.set_page_config(
    page_title="BNH Rules Assistant",
    page_icon="🃏",
    layout="centered",
)


@st.cache_resource(show_spinner="Loading search index…")
def get_vector_store():
    return load_vector_store()


def render_sources(response: RAGResponse) -> None:
    if not response.sources:
        return

    st.caption("Sources")
    for name in response.sources:
        st.markdown(f"- `{name}`")

    with st.expander("Retrieved excerpts"):
        for i, doc in enumerate(response.chunks, start=1):
            st.markdown(f"**Chunk {i}** — `{source_label(doc.metadata.get('source', 'unknown'))}`")
            st.text(doc.page_content.strip()[:600] + ("…" if len(doc.page_content) > 600 else ""))


def main() -> None:
    st.title("Better Not Hundred — Rules Assistant")
    st.markdown(
        "Ask questions about game rules, multiplayer, Firebase, and implementation docs. "
        "Answers are grounded in project documentation via **RAG** (retrieval-augmented generation)."
    )

    # Warm up vector store early so first question is faster
    try:
        get_vector_store()
    except FileNotFoundError:
        st.error("Search index not found. Run `python ingest.py` first, then refresh this page.")
        st.stop()
    except ConnectionError as exc:
        st.error(str(exc))
        st.stop()

    with st.sidebar:
        st.header("Settings")
        show_prompt = st.checkbox("Show RAG prompt (debug)", value=False)
        st.divider()
        st.header("Try asking")
        for q in EXAMPLE_QUESTIONS:
            if st.button(q, use_container_width=True, key=f"example_{q[:30]}"):
                st.session_state.pending_question = q

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                st.caption("Sources: " + ", ".join(f"`{s}`" for s in msg["sources"]))

    question = st.chat_input("Ask about Better Not Hundred…")

    pending = st.session_state.pop("pending_question", None)
    if pending:
        question = pending

    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching docs and generating answer…"):
            try:
                response = answer_question(question, include_prompt=show_prompt)
            except ConnectionError as exc:
                st.error(str(exc))
                return
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                return

        st.markdown(response.answer)
        render_sources(response)

        if show_prompt and response.prompt:
            with st.expander("RAG prompt sent to LLM"):
                st.code(response.prompt, language="text")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "sources": response.sources,
        }
    )


if __name__ == "__main__":
    main()
