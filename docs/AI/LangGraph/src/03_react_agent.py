import json
from typing import TypedDict, Annotated, List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

# 0. Setup
llm = ChatOllama(model="llama3.2")

# 1. Define Tools (Best Practice: Use Pydantic for schema control)

class MultiplyInput(BaseModel):
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

@tool("multiply", args_schema=MultiplyInput)
def multiply(a: int, b: int) -> int:
    """Multiplies two integers."""
    return a * b

class WeatherInput(BaseModel):
    city: str = Field(..., description="The city name to check weather for")

@tool("get_weather", args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    if "San Francisco" in city:
        return "It's 60F and foggy."
    elif "New York" in city:
        return "It's 90F and sunny."
    return "Unknown weather."

tools = [multiply, get_weather]

# 2. Bind Tools
llm_with_tools = llm.bind_tools(tools)

# 3. State
class State(TypedDict):
    # The add_messages reducer is critical for chat history
    messages: Annotated[List[BaseMessage], add_messages]

# 4. Nodes
def agent_node(state: State):
    """The 'Brain' node."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 5. Build Graph
builder = StateGraph(State)
builder.add_node("agent", agent_node)
# LangGraph's prebuilt ToolNode handles tool execution automatically
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")

# 6. Conditional Logic (The ReAct Loop)
# If the agent requests a tool => go to tools
# If the agent replies with text => go to END
def should_continue(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

builder.add_conditional_edges("agent", should_continue, ["tools", END])

# 7. Close the Loop
# After tools run, go back to agent to interpret the result
builder.add_edge("tools", "agent")

graph = builder.compile()

# 8. Run
if __name__ == "__main__":
    print("--- Math Test ---")
    res = graph.invoke({"messages": [HumanMessage(content="What is 11 * 11?")]})
    print(res["messages"][-1].content)

    print("\n--- Weather Test ---")
    res = graph.invoke({"messages": [HumanMessage(content="Weather in NY?")]})
    print(res["messages"][-1].content)
