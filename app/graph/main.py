from langgraph.graph import StateGraph, START, END
from app.schemas.state import State
from app.planner.executor import execute_planner_node

def create_graph():
    g = StateGraph(State)
    g.add_node('planner',execute_planner_node)
    g.add_edge(START,'planner')
    g.add_edge('planner',END)
    app = g.compile()

    return app


