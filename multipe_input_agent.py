from typing import TypedDict, List
from langgraph.graph import StateGraph
from IPython.display import Image, display

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:
    """This functn handles multiple different inputs"""

    state["result"] = f'Hi there {state["name"]}! Your sum = {sum(state["values"])}'

    return state

workflow = StateGraph(AgentState)

workflow.add_node("processor", process_values)
workflow.set_entry_point('processor')
workflow.set_finish_point('processor')

app = workflow.compile()

display(Image(app.get_graph().draw_mermaid_png()))

result = app.invoke({"name": "Advay", "values": [1, 2, 3,234]})

print(result["result"]) 