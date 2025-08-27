from typing import TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display

class AgentState(TypedDict):
    message: str

def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state"""
    state["message"] = "Hello " + state["message"] + ", how was your day today?"
    return state

builder = StateGraph(AgentState)
builder.add_node('greeter', greeting_node)
builder.set_entry_point('greeter')
builder.set_finish_point('greeter')

app = builder.compile()

display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"message": "Advay"})
print(result["message"])
