from typing import Optional, Dict
from pydantic import BaseModel, Field

class ConfidenceSchema(BaseModel):
    """
    Final confidence produced by the system after aggregation.
    This is the ONLY numeric artifact exposed downstream.
    """

    final_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Final numeric confidence score"
    )

    confidence_mode: str = Field(
        ...,
        description="Confidence mode used (explanation_confidence or action_confidence)"
    )

    refusal: bool = Field(
        ...,
        description="Whether the system refused to give an actionable response"
    )

    refusal_reason: Optional[str] = Field(
        default=None,
        description="Reason for refusal if refusal is true"
    )

    penalties: Dict[str, str] = Field(
        ...,
        description="Structured penalties applied (conflicts, data gaps, risk misalignment)"
    )
