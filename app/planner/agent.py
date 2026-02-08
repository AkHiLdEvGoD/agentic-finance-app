import json
from typing import TypedDict, Any
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from app.utils.llm_client import llm_chat
from app.schemas.planner import PlannerOutput
from app.planner.system_prompt import (
    PLANNER_SYSTEM_PROMPT,
    FEW_SHOT_EXAMPLES
)


def planner_node(state:dict)->PlannerOutput:
    """
    LangGraph node:
    Takes user_query → produces PlannerOutput
    """

    messages=[
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        # SystemMessage(content=f"JSON Schema:\n{PLANNER_JSON_SCHEMA}")
    ]
    for examples in FEW_SHOT_EXAMPLES:
        messages.append(HumanMessage(content=examples['user']))
        messages.append(
            AIMessage(content=json.dumps(examples['assistant'],indent=2))
        )
    messages.append(HumanMessage(content=(state['user_query'])))
    response=llm_chat('planner',messages,PlannerOutput)

    return response