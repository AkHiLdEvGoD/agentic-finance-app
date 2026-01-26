from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv

load_dotenv()

_MODELS = {
    "planner": ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0
    ),
    "aggregator": ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2
    ),
    "response": ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.4
    )
}

def llm_chat(
    role: str,
    messages: list[BaseMessage]
) -> str:
    """
    role: planner | aggregator | response
    """
    if role not in _MODELS:
        raise ValueError(f"Unknown LLM role: {role}")

    response = _MODELS[role].invoke(messages)
    return response.content