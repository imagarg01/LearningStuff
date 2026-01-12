import asyncio
import os
from typing import TypedDict, Annotated, Optional
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# 1. Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Define Node with Config
# Notice the second argument `config: RunnableConfig`
def flexible_chatbot(state: State, config: RunnableConfig):
    # Get runtime configuration
    configuration = config.get("configurable", {})
    model_name = configuration.get("model_name", "gpt-3.5-turbo")
    system_prompt = configuration.get("system_prompt", "You are a helpful assistant.")
    
    # Initialize model dynamically based on config
    print(f"--- Running with model: {model_name} ---")
    print(f"--- System Prompt: {system_prompt} ---")
    
    llm = ChatOpenAI(model=model_name)
    
    # Prepend system prompt to messages
    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    
    response = llm.invoke(messages)
    return {"messages": [response]}

# 3. Build Graph
builder = StateGraph(State)
builder.add_node("chatbot", flexible_chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

# 4. Run with different configs
async def main():
    inputs = {"messages": [("user", "Hello! Who are you?")]}

    print("\n\n=== Run 1: Default (Standard Assistant) ===")
    await graph.ainvoke(inputs)

    print("\n\n=== Run 2: Pirate Mode (GPT-4) ===")
    # We pass a config dictionary with "configurable" keys
    config = {
        "configurable": {
            "model_name": "gpt-4",
            "system_prompt": "You are a pirate. Answer everything with 'Arrr!'"
        }
    }
    result = await graph.ainvoke(inputs, config=config)
    print("Result:", result["messages"][-1].content)

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
         print("Please set OPENAI_API_KEY to run this example.")
    else:
        asyncio.run(main())
