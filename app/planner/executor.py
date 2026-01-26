# app/planner/executor.py

import json
from typing import Optional

from app.planner.agent import planner_node
from app.planner.validator import validate_plan, PlannerValidationError
from app.schemas.planner import PlannerOutput


class PlannerExecutionError(Exception):
    """Raised when planner fails after retries."""


MAX_RETRIES = 3


def run_planner_with_retries(
    user_query: str
) -> PlannerOutput:
    """
    Runs planner node with schema + semantic validation and retry logic.
    """

    last_error: Optional[Exception] = None

    # Initial LangGraph-style state
    state = {
        "user_query": user_query,
        "planner_output": None
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Run planner node (LLM call)
            state = planner_node(state)

            plan = state["planner_output"]
            if plan is None:
                raise PlannerExecutionError("Planner returned empty output")

            # Semantic validation (may modify plan)
            validated_plan = validate_plan(plan)

            return validated_plan  # ✅ SUCCESS

        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            _tighten_prompt_for_retry(attempt)

        except PlannerValidationError as e:
            last_error = e
            _tighten_prompt_for_retry(attempt)

    # If all retries failed
    raise PlannerExecutionError(
        f"Planner failed after {MAX_RETRIES} attempts"
    ) from last_error

def _tighten_prompt_for_retry(attempt: int) -> None:
    """
    Adjust planner behavior across retries.
    This mutates global planner instructions carefully.
    """

    from app.planner import system_prompt

    if attempt == 1:
        return  # first attempt already done

    if attempt == 2:
        system_prompt.PLANNER_SYSTEM_PROMPT += (
            "\n\nIMPORTANT: Your previous output was invalid. "
            "Output ONLY a single valid JSON object."
        )

    if attempt == 3:
        system_prompt.PLANNER_SYSTEM_PROMPT += (
            "\n\nIf you are unsure about intent or tools, "
            "choose the safest possible plan."
        )


queries = [
    # "Should I buy Tata Motors?",
    # "Fundamental analysis of Tata Motors",
    # "Based on latest news, should I buy Tata Motors?",
    # "Thoughts on Tata Motors?",
    "Compare Tata Motors and Mahindra & Mahindra"
]

for q in queries:
    plan = run_planner_with_retries(q)
    print(q)
    print(plan.model_dump(mode='json'), "\n")