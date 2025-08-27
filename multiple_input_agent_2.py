from langgraph.graph import StateGraph, START, END

# Define the state
class State(dict):
    name: str
    values: list
    operation: str
    result: str

# Single node: process input
def process(state: State):
    values = state["values"]
    op = state["operation"]

    if op == "+":
        ans = sum(values)
    elif op == "*":
        ans = 1
        for v in values:
            ans *= v
    else:
        ans = "Invalid operation"

    state["result"] = f"Hi {state['name']}, your answer is: {ans}"
    return state

# Build graph
workflow = StateGraph(State)
workflow.add_node("process", process)
workflow.add_edge(START, "process")
workflow.add_edge("process", END)
app = workflow.compile()

# Run
input_data = {"name": "Advay", "values": [1, 2, 3, 4], "operation": "*"}
output = app.invoke(input_data)
print(output["result"])
