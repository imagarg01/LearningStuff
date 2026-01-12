import os
from typing import TypedDict, Literal
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

# Setup
llm = ChatOllama(model="llama3.2")

# 1. State
class State(TypedDict):
    question: str
    answer: str

# 2. Structured Output Schema (Best Practice)
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["math", "general"] = Field(
        ..., 
        description="Given a user question, choose to route it to 'math' or 'general'."
    )

# 3. Nodes
def classification_node(state: State):
    """
    Uses Structured Output to reliably determine the next step.
    This replaces fragile string parsing.
    """
    question = state["question"]
    print(f"--- Classifying: {question} ---")
    
    # Enable structured output on the LLM
    structured_llm = llm.with_structured_output(RouteQuery)
    
    # Invoking it returns a Pydantic object, not a Message
    decision = structured_llm.invoke(question)
    
    # valid_decision will be 'math' or 'general'
    return {"classification": decision.datasource}

def math_node(state: State):
    print("--- Executing Math Node ---")
    return {"answer": "42 (Math Expert)"}

def general_node(state: State):
    print("--- Executing General Node ---")
    return {"answer": "I am a general assistant."}

# 4. Routing Logic
def route_decision(state: State):
    # The state now might not even need 'classification' stored if we ran this logic 
    # directly in the conditional edge, but storing it is fine too.
    # Here we assume the classification_node stored something in a temporary key 
    # or we can pass the result directly if this function runs the classification.
    # 
    # For this example, let's assume classification_node isn't a node but the 
    # logic happens inside the edge OR we store the intent in the state.
    # Let's stick to the previous pattern: Node -> Update State -> Edge Check.
    
    # We need to update State TypedDict to hold this if we use this pattern
    # But wait, conditional edges can access the state.
    pass

# ALTERNATIVE PATTERN: The "Router" IS the Conditional Edge
# This is often cleaner. Let's demonstrate that.

def router_edge(state: State) -> Literal["math_node", "general_node"]:
    print("--- Router Edge ---")
    question = state["question"]
    structured_llm = llm.with_structured_output(RouteQuery)
    decision = structured_llm.invoke(question)
    
    if decision.datasource == "math":
        return "math_node"
    else:
        return "general_node"

# 5. Build Graph
builder = StateGraph(State)

builder.add_node("math_node", math_node)
builder.add_node("general_node", general_node)

# Conditional Edge from START
builder.add_conditional_edges(
    START,
    router_edge,
    # Optional Path Map for clarity
    {
        "math_node": "math_node", 
        "general_node": "general_node"
    }
)

builder.add_edge("math_node", END)
builder.add_edge("general_node", END)

graph = builder.compile()

# 6. Run
if __name__ == "__main__":
    print(graph.invoke({"question": "What is 2 + 2?"}))
    print(graph.invoke({"question": "How are you?"}))
