from typing import TypedDict
from app.schemas.planner import PlannerOutput

class State(TypedDict):
    user_query : str
    planner_output : PlannerOutput|None