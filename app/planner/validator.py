from typing import Set

from app.schemas.planner import (
    PlannerOutput,
    UserIntent,
    ToolName,
    ConfidenceMode
)


class PlannerValidationError(Exception):
    """Raised when planner output violates system invariants."""


# -------------------------
# Core Validator
# -------------------------

def validate_plan(plan: PlannerOutput) -> PlannerOutput:
    """
    Validates and enforces invariants on PlannerOutput.
    This function may MODIFY the plan to enforce safety.
    """

    _enforce_confidence_mode(plan)
    _enforce_tool_sanity(plan)
    _enforce_risk_requirement(plan)
    _enforce_explanation_only(plan)
    _enforce_compare_rules(plan)
    _enforce_clarification_rules(plan)

    return plan


# -------------------------
# Individual Rules
# -------------------------

def _enforce_confidence_mode(plan: PlannerOutput) -> None:
    """Confidence mode is derived from intent, not LLM choice."""

    if plan.intent == UserIntent.RECOMMENDATION:
        plan.confidence_mode = ConfidenceMode.ACTION
    else:
        plan.confidence_mode = ConfidenceMode.EXPLANATION


def _enforce_risk_requirement(plan: PlannerOutput) -> None:
    """Risk analysis is mandatory for recommendations."""

    if plan.intent != UserIntent.RECOMMENDATION:
        return

    for tool in plan.tools_to_invoke:
        if tool.tool_name == ToolName.RISK and tool.required:
            return

    raise PlannerValidationError(
        "Recommendation intent requires mandatory risk_analysis tool"
    )


def _enforce_explanation_only(plan: PlannerOutput) -> None:
    """Non-recommendation intents must never allow actions."""

    if plan.intent == UserIntent.RECOMMENDATION:
        return

    plan.explanation_only = True
    if plan.aggregation_constraints is not None:
        plan.aggregation_constraints.allow_recommendation = False

def _enforce_compare_rules(plan: PlannerOutput) -> None:
    """Compare intent must involve multiple tickers."""

    if plan.intent != UserIntent.COMPARE:
        return

    if not plan.tickers or len(plan.tickers) < 2:
        raise PlannerValidationError(
            "Compare intent requires two or more tickers"
        )


def _enforce_tool_sanity(plan: PlannerOutput) -> None:
    """Ensure tools are unique and valid."""

    seen: Set[ToolName] = set()

    for tool in plan.tools_to_invoke:
        if tool.tool_name in seen:
            raise PlannerValidationError(
                f"Duplicate tool detected: {tool.tool_name}"
            )
        seen.add(tool.tool_name)

def _enforce_clarification_rules(plan:PlannerOutput)->None:
    """
    If intent requires a ticker but none is explicitly present,
    force clarification instead of guessing.
    """

    if plan.intent == UserIntent.CLARIFICATION:
        plan.tools_to_invoke = []
        plan.tickers=[]
        plan.aggregation_constraints=None
        plan.explanation_only = True
        plan.confidence_mode = ConfidenceMode.EXPLANATION

