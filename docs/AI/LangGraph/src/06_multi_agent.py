import operator
from typing import TypedDict, Annotated, List
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

# Setup
llm = ChatOllama(model="llama3.2")

# 1. State
class State(TypedDict):
    topic: str
    # aggregated results from parallel workers
    jokes: Annotated[List[str], operator.add] 

# 2. Worker Node (The Map Step)
def joke_generator(state: dict):
    # Notice this node receives a dict with just the payload needed: {"subject": ...}
    subject = state["subject"]
    print(f"--- Generating joke about {subject} ---")
    response = llm.invoke(f"Tell me a one-line joke about {subject}.")
    return {"jokes": [f"{subject.upper()}: {response.content}"]}

# 3. Router logic (The Split)
def continue_to_jokes(state: State):
    # We take the main topic and split it into sub-tasks
    # Let's say we want jokes about 3 related sub-topics
    print(f"--- Mapping sub-topics for {state['topic']} ---")
    
    subjects = [f"{state['topic']} {xsd}" for xsd in ["puns", "situational", "dark"]]
    
    # We return a list of Send objects
    # Each Send object targets a node ("generate_joke") with a specific payload
    return [Send("generate_joke", {"subject": s}) for s in subjects]

# 4. Reducer Logic (Auto-handled by State annotation)
# The 'jokes' key uses operator.add, so results from parallel nodes are merged into the list.

# 5. Build Graph
builder = StateGraph(State)
builder.add_node("generate_joke", joke_generator)

# Edge: Start -> Map Logic
builder.add_conditional_edges(START, continue_to_jokes)

# Edge: Workers -> END
builder.add_edge("generate_joke", END)

graph = builder.compile()

# 6. Run
if __name__ == "__main__":
    print("--- Map-Reduce Joke Generator ---")
    user_topic = "Programming"
    
    # This will trigger 3 parallel calls to 'generate_joke'
    # And the final state will contain 3 jokes in the list
    result = graph.invoke({"topic": user_topic})
    
    print("\n--- Final Results ---")
    for joke in result["jokes"]:
        print(joke)
