from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Type

load_dotenv()

_MODELS = {
    "planner": ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.0,
        model_kwargs={'response_format':{"type": "json_object"}},
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
    messages: list[BaseMessage],
    schema: Type[BaseModel] | None = None,
):
    """
    role: planner | aggregator | response
    """

    if role not in _MODELS:
        raise ValueError(f"Unknown LLM role: {role}")

    model = _MODELS[role]

    # ---- Planner / Aggregator: JSON MODE + SCHEMA VALIDATION ----
    if role in ("planner", "aggregator"):
        raw = model.invoke(messages).content

        if schema is None:
            raise ValueError(f"Schema required for role: {role}")

        try:
            return schema.model_validate_json(raw)
        except Exception as e:
            raise RuntimeError(
                f"{role} returned invalid JSON.\nRaw output:\n{raw}"
            ) from e

    # ---- Response: free-form text ----
    return model.invoke(messages).content