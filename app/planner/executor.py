import json
from typing import Optional

from app.planner.agent import planner_node
from app.planner.validator import validate_plan, PlannerValidationError
from app.schemas.state import State

class PlannerExecutionError(Exception):
    """Raised when planner fails after retries."""

MAX_RETRIES = 3
def execute_planner_node(state: State) -> dict:
    """
    Runs planner node with schema + semantic validation and retry logic.
    """

    last_error: Optional[Exception] = None


    for attempt in range(1, MAX_RETRIES + 1):
        try:

            plan = planner_node(state)
            if plan is None:
                raise PlannerExecutionError("Planner returned empty output")

            # Semantic validation (may modify plan)
            validated_plan = validate_plan(plan)

            return {
                **state,
                'planner_output':validated_plan
            }

        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            _tighten_prompt_for_retry(attempt)

        except PlannerValidationError as e:
            last_error = e
            _tighten_prompt_for_retry(attempt)

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