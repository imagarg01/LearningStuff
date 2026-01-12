import asyncio
import os
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Define Nodes
llm = ChatOpenAI(model="gpt-3.5-turbo")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 3. Build Graph
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

# 4. Stream Execution
async def main():
    print("--- Streaming Tokens ---")
    inputs = {"messages": [("user", "Write a short haiku about AI.")]}
    
    # We use astream_events to get token-level updates from the LLM
    async for event in graph.astream_events(inputs, version="v1"):
        kind = event["event"]
        
        # 'on_chat_model_stream' event is emitted for every token generated
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(content, end="", flush=True)
                
    print("\n\n--- Done ---")

if __name__ == "__main__":
    if not os.environ.get("OPEN_OPENAI_API_KEY"):
        # Just a placeholder for the user to know they need a key
        # In a real run, this would probably fail or use a mock if we set one up
        print("Please set OPEN_OPENAI_API_KEY to run this example.")
    else:
        asyncio.run(main())
