"""Step 4 (online): Build the prompt and call the LLM."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

import config
from rag.ollama_utils import ensure_ollama_running
from rag.retriever import format_context


def build_user_message(question: str, context: str) -> str:
    """
    AUGMENT (part 2): The concrete prompt body from our walkthrough.

    Structure:
      CONTEXT:  ← retrieved chunks (from vector search)
      QUESTION: ← user's actual question
    """
    return f"CONTEXT:\n\n{context}\n\nQUESTION:\n{question}"


def generate_answer(question: str, context: str) -> str:
    """
    GENERATE step: send system + augmented user message to local Ollama.

    The model does NOT search your docs — it only reads what we put in the prompt.
    """
    ensure_ollama_running()

    llm = ChatOllama(
        model=config.LLM_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        temperature=config.LLM_TEMPERATURE,
    )

    messages = [
        SystemMessage(content=config.SYSTEM_PROMPT),
        HumanMessage(content=build_user_message(question, context)),
    ]

    response = llm.invoke(messages)
    return response.content
