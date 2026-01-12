import os
from typing import TypedDict, Annotated
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

# 0. Setup Model
llm = ChatOllama(model="llama3.2")

# 1. Define State (Best Practice: Use Annotated for reducers)
class State(TypedDict):
    # 'add_messages' ensures new messages are appended, not overwritten
    messages: Annotated[list, add_messages]

# 2. Define Nodes
def chatbot(state: State):
    print(f"--- History: {len(state['messages'])} messages ---")
    
    # LLM receives the full list of messages (context)
    response = llm.invoke(state["messages"])
    
    # We return a list containing just the *new* message
    # The reducer will append it to the state automatically
    return {"messages": [response]}

# 3. Build Graph
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

# 4. Run
if __name__ == "__main__":
    print("--- First Run ---")
    initial_input = {"messages": [HumanMessage(content="Explain Quantum Computing in one sentence.")]}
    result = graph.invoke(initial_input)
    print(f"Bot: {result['messages'][-1].content}")
    
    # 5. Show Reducer in Action (Simulated Conversation)
    print("\n--- Second Run (Simulating Continuation) ---")
    # In a real app, we'd pass the existing state. Here we simulate adding a new user msg.
    new_input = {"messages": [HumanMessage(content="What about AI?")]}
    
    # NOTE: Since we aren't using a checkpointer here, 'graph.invoke' starts fresh by default.
    # To see the reducer working across steps in a single run, we'd need a loop or checkpointer.
    # But for this simple example, we just show the structure validity.
