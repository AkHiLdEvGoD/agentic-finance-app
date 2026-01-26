import json
from app.schemas.planner import PlannerOutput

def build_json_schema()->str:
    """
    Converts PlannerOutput Pydantic model into JSON Schema
    and returns it as a formatted string for LLM prompting.
    """
    schema_dict = PlannerOutput.model_json_schema()
    return json.dumps(schema_dict, indent=2)

PLANNER_JSON_SCHEMA = build_json_schema()