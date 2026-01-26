from typing import List,Optional
from pydantic import BaseModel,Field
from datetime import datetime

class BaseToolOutput(BaseModel):
    """
    Base schema that every tool output must extend.
    This enforces consistency, confidence tracking, and auditability.
    """

    tool_name : str = Field(
        ...,
        description="Name of the tool producing the output"
    )

    ticker: str = Field(
        ...,
        description="Stock ticker symbol used for the analysis"
    )

    data_timestamp: datetime = Field(
        ...,
        description="Timestamp of the underlying data used"
    )

    tool_confidence = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score produced by this tool (0 to 1)"
    )

    warnings: Optional[List[str]] = Field(
        default=None,
        description="Non-fatal issues (missing data, partial coverage, etc.)"
    )


class ConfidenceSchema(BaseModel):
    """
    Final confidence produced by the system after aggregating all tools.
    """

    final_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Aggregated confidence score for the final recommendation"
    )

    confidence_breakdown: dict = Field(
        ...,
        description="Per-tool confidence contributions and penalties"
    )

    refusal_reason: Optional[str] = Field(
        default=None,
        description="Reason for refusal if confidence is below threshold"
    )
