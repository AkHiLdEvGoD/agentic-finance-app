from enum import Enum
from typing import List, Optional
from pydantic import BaseModel,Field

class UserIntent(str,Enum):
    ANALYSIS = "analysis"
    EXPLANATION = "explanation"
    RECOMMENDATION = "recommendation"
    RISK = "risk"
    NEWS = "news"
    COMPARE = "compare"
    CLARIFICATION = "clarification"

class ConfidenceMode(str,Enum):
    EXPLANATION="explanation_confidence"
    ACTION="action_confidence"

class ToolName(str,Enum):
    FUNDAMENTAL = "fundamental_analysis"
    TECHNICAL = "technical_analysis"
    RISK = "risk_analysis"
    NEWS = "news_sentiment"

class ToolInvocation(BaseModel):
    tool_name : ToolName = Field(
        ...,
        description='Tools to invoke'
    )
    required: bool = Field(
        ...,
        description='If true, downstream aggregation must fail if this tool fails'
    )

class AggregationConstraints(BaseModel):
    allow_contradictions: bool = Field(
        ...,
        description='Whether conflicting tool signals are acceptable'
    )

    require_risk_alignment: bool = Field(
        ...,
        description='Whether risk must align with other signals'
    )
    
    allow_recommendation: bool = Field(
        ...,
        description="Whether buy/sell/hold style outputs are allowed"
    )

    comparison_mode: Optional[str] = Field(
        default=None,
        description="Relative comparison mode for COMPARE intent"
    )

    require_data_parity: bool = Field(
        default=False,
        description="Whether all tickers must have equivalent tool coverage"
    )

    output_style: str = Field(
        ...,
        description="Narrative constraint for aggregator (explanatory, decisive, comparative)"
    )

class PlannerOutput(BaseModel):
    """
    Output of the Planner Agent.
    This schema is the execution contract for the entire system.
    """
    intent: UserIntent = Field(
        ...,
        description="Parsed user intent"
    )

    tickers: List[str] = Field(
        ...,
        description="One or more stock tickers involved in the query"
    )

    tools_to_invoke: List[ToolInvocation] = Field(
        ...,
        description="Ordered list of tools to invoke per ticker"
    )

    aggregation_constraints: AggregationConstraints = Field(
        ...,
        description="Rules the aggregator must follow"
    )

    confidence_mode: ConfidenceMode = Field(
        ...,
        description="Which confidence computation path to use"
    )

    explanation_only: bool = Field(
        ...,
        description="If true, system must not output action labels"
    )
