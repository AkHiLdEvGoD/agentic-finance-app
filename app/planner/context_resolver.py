from app.schemas.context import ConversationContext, ResolvedQuery
from typing import List

def resolve_context(
    user_query: str,
    context: ConversationContext,
    extracted_tickers: List[str]  # from regex / symbol matcher
) -> ResolvedQuery:

    # Case 1: Explicit tickers mentioned
    if extracted_tickers:
        return ResolvedQuery(
            original_query=user_query,
            resolved_tickers=extracted_tickers
        )

    # Case 2: Referential language + previous tickers
    if uses_reference_language(user_query) and context.last_tickers:
        return ResolvedQuery(
            original_query=user_query,
            resolved_tickers=context.last_tickers
        )

    # Case 3: Comparison intent + partial tickers
    if is_comparison_query(user_query) and context.last_tickers:
        return ResolvedQuery(
            original_query=user_query,
            resolved_tickers=context.last_tickers,
            ambiguity=True,
            clarification_needed=True,
            clarification_reason="Comparison requires two tickers"
        )

    # Case 4: No signal
    return ResolvedQuery(
        original_query=user_query,
        resolved_tickers=[],
        ambiguity=True,
        clarification_needed=True,
        clarification_reason="No ticker context available"
    )


import re

TICKER_REGEX = re.compile(r"\b[A-Z]{2,10}\b")

def extract_tickers(text: str) -> list[str]:
    candidates = TICKER_REGEX.findall(text.upper())
    return list(set(candidates))

COMPARISON_KEYWORDS = [
    "compare",
    "vs",
    "versus",
    "difference",
    "differences",
    "better than",
    "which is better",
    "outperform",
    "relative",
    "comparison",
]

import re

def is_comparison_query(text: str) -> bool:
    text = text.lower()

    # Direct keyword match
    for kw in COMPARISON_KEYWORDS:
        if kw in text:
            return True

    # Symbolic "X vs Y"
    if re.search(r"\bvs\b", text):
        return True

    return False


import re

REFERENCE_PATTERNS = [
    r"\bit\b",
    r"\bthat stock\b",
    r"\bthis stock\b",
    r"\bthe stock\b",
    r"\bthe previous one\b",
    r"\bprevious stock\b",
    r"\bformer\b",
    r"\bthe same\b",
    r"\bone\b",
]

def uses_reference_language(text: str) -> bool:
    text = text.lower()
    return any(re.search(pattern, text) for pattern in REFERENCE_PATTERNS)
