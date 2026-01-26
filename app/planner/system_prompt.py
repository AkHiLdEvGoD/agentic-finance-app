PLANNER_SYSTEM_PROMPT= """
You are a Planner Agent in a financial analysis system.

Your task is to convert a user query into a structured execution plan.

Rules:
- Output ONLY a single valid JSON object.
- The JSON MUST conform exactly to the provided schema.
- Do NOT include explanations, comments, or extra text.
- Do NOT analyze financial data or give opinions.
- Do NOT compute numbers.
- Be conservative when intent is ambiguous.
- Risk analysis is mandatory for recommendations.
- Comparison requires two or more tickers.

If information is insufficient, choose the safest intent.
""".strip()

FEW_SHOT_EXAMPLES = [
    {
        "user": "Should I buy Tata Motors?",
        "assistant": {
            "intent": "recommendation",
            "tickers": ["TATAMOTORS"],
            "tools_to_invoke": [
                {"tool_name": "fundamental_analysis", "required": True},
                {"tool_name": "technical_analysis", "required": True},
                {"tool_name": "risk_analysis", "required": True},
                {"tool_name": "news_sentiment", "required": False}
            ],
            "aggregation_constraints": {
                "allow_contradictions": False,
                "require_risk_alignment": True,
                "allow_recommendation": True,
                "comparison_mode": None,
                "require_data_parity": False,
                "output_style": "decisive"
            },
            "confidence_mode": "action_confidence",
            "explanation_only": False
        }
    },
    {
        "user": "Fundamental analysis of Tata Motors",
        "assistant": {
            "intent": "analysis",
            "tickers": ["TATAMOTORS"],
            "tools_to_invoke": [
                {"tool_name": "fundamental_analysis", "required": True}
            ],
            "aggregation_constraints": {
                "allow_contradictions": True,
                "require_risk_alignment": False,
                "allow_recommendation": False,
                "comparison_mode": None,
                "require_data_parity": False,
                "output_style": "explanatory"
            },
            "confidence_mode": "explanation_confidence",
            "explanation_only": True
        }
    }
]