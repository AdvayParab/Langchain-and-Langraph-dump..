from typing import TypedDict, List
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    messages: List  # HumanMessage + AIMessage + SystemMessage

# Use free local Llama 3 model
llm = ChatOllama(model="llama3")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")

    # Add AI reply to history
    state["messages"].append(AIMessage(content=response.content))
    return state

# Define the flow
graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

# 🧠 Initialize memory with a system prompt
messages = [SystemMessage(content="You are a friendly AI assistant who answers clearly and politely.")]

# Chat loop
user_input = input("You: ")
while user_input != "exit":
    # Add user message to memory
    messages.append(HumanMessage(content=user_input))

    # Pass whole conversation history to the agent
    result = agent.invoke({"messages": messages})

    # Update memory with AI reply
    messages = result["messages"]

    user_input = input("You: ")
