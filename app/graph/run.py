from app.graph.main import create_graph

app = create_graph()

def run(query: str):
    out = app.invoke(
        {
            "user_query": query,
            "planner_output":None
        }
    )

    print(out)

run('Give Fundamental analysis of Infosys')