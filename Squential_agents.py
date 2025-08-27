from langgraph.graph import StateGraph, START, END

# Define state
class State(dict):
    name: str
    age: int
    skills: list
    result: str
    greeting: str
    age_text: str
    skills_text: str

# Node 1: Greeting with name
def greet_node(state: State):
    state["greeting"] = f"{state['name']}, welcome to the system!"
    return state

# Node 2: Describe age
def age_node(state: State):
    state["age_text"] = f"You are {state['age']} years old!"
    return state

# Node 3: Format skills
def skills_node(state: State):
    skills = state["skills"]
    if len(skills) > 1:
        skills_str = ", ".join(skills[:-1]) + f", and {skills[-1]}"
    else:
        skills_str = skills[0]
    state["skills_text"] = f"You have skills in: {skills_str}"
    # Combine everything into result
    state["result"] = f"{state['greeting']} {state['age_text']} {state['skills_text']}"
    return state

# Build graph
workflow = StateGraph(State)
workflow.add_node("greet", greet_node)
workflow.add_node("age", age_node)
workflow.add_node("skills", skills_node)

workflow.add_edge(START, "greet")
workflow.add_edge("greet", "age")
workflow.add_edge("age", "skills")
workflow.add_edge("skills", END)

app = workflow.compile()

# Test input
input_data = {"name": "Advay ", "age": 24, "skills": ["Python", "Machine Learning", "LangGraph"]}
output = app.invoke(input_data)

print(output["result"])
