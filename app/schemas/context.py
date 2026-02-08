from pydantic import BaseModel
from typing import Optional, List

class ConversationContext(BaseModel):
    last_ticker = List[str] = []
    last_intent = Optional[str] = []
    last_analysis_scope : Optional[str]=None
    turn_id:int=0

class ResolvedQuery(BaseModel):
    original_query: str
    resolved_tickers: List[str]
    ambiguity: bool = False
    clarification_needed: bool = False
    clarification_reason: Optional[str] = None