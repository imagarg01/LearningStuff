import uuid
from typing import TypedDict, Annotated, List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Setup
llm = ChatOllama(model="llama3.2")

# 1. State
class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# 2. Nodes
def chatbot_node(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 3. Build Graph
builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# 4. Persistence
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 5. Run with Time Travel Demo
if __name__ == "__main__":
    thread_id = "demo_thread"
    config = {"configurable": {"thread_id": thread_id}}
    
    print("--- 1. First Message ---")
    graph.invoke({"messages": [HumanMessage(content="Hi, my name is Bob.")]}, config=config)
    
    print("\n--- 2. Second Message (Memory Test) ---")
    result = graph.invoke({"messages": [HumanMessage(content="What is my name?")]}, config=config)
    print(f"Bot: {result['messages'][-1].content}")
    
    print("\n--- 3. Time Travel (Inspect History) ---")
    # Get all snapshots for this thread
    snapshots = list(graph.get_state_history(config))
    for i, snapshot in enumerate(snapshots):
        print(f"Snapshot {i}: {snapshot.values['messages'][-1].content[:20]}...")
        
    print("\n--- 4. Getting Current State ---")
    current_state = graph.get_state(config)
    print(f"Current State ID: {current_state.config['configurable']['checkpoint_id']}")
