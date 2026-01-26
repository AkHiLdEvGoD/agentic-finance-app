from enum import Enum
from typing import List,Optional
from pydantic import BaseModel,Field

class OverallAssessment(str,Enum):
    STRONG_POSITIVE = "strong_positive"
    MODERATE_POSITIVE = "moderate_positive"
    NEUTRAL = "neutral"
    MODERATE_NEGATIVE = "moderate_negative"
    STRONG_NEGATIVE = "strong_negative"
    INSUFFICIENT_DATA = "insufficient_data"

class SignalDirection(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"
    UNKNOWN = "unknown"

class DimensionSignal(BaseModel):
    dimension: str = Field(
        ...,
        description="Analysis dimension (fundamental, technical, risk, news)"
    )

    signal: SignalDirection = Field(
        ...,
        description="Overall qualitative direction"
    )

    rationale: str = Field(
        ...,
        description="Natural language explanation for this signal"
    )

    data_freshness_issue: bool = Field(
        ...,
        description="Whether this dimension suffers from stale or partial data"
    )

class Conflict(BaseModel):
    dimensions: List[str] = Field(
        ...,
        description="Dimensions involved in the conflict"
    )

    description: str = Field(
        ...,
        description="Explanation of the conflicting signals"
    )

class DataGap(BaseModel):
    dimension: str = Field(
        ...,
        description="Affected dimension"
    )

    issue: str = Field(
        ...,
        description="Missing, stale, or incomplete data explanation"
    )

class RecommendationLabel(str, Enum):
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    AVOID = "avoid"

class AggregatorOutput(BaseModel):
    """
    Output of the Aggregator Agent.
    Contains qualitative synthesis only.
    """

    ticker: Optional[str] = Field(
        None,
        description="Ticker for single-asset analysis"
    )

    tickers: Optional[List[str]] = Field(
        None,
        description="Tickers involved in comparison"
    )

    overall_assessment: OverallAssessment = Field(
        ...,
        description="High-level qualitative conclusion"
    )

    dimension_signals: List[DimensionSignal] = Field(
        ...,
        description="Per-dimension qualitative signals"
    )

    conflicts: Optional[List[Conflict]] = Field(
        default=None,
        description="Detected contradictions between dimensions"
    )

    data_gaps: Optional[List[DataGap]] = Field(
        default=None,
        description="Missing or stale data issues"
    )

    recommendation: Optional[RecommendationLabel] = Field(
        default=None,
        description="Action label (only if allowed by planner constraints)"
    )
