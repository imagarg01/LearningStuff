import os
from typing import Annotated, Sequence, TypedDict
import operator

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# -----------------------------------------------------
# Pattern 1: Single-Agent Baseline Architecture
# Mapped to Agent Learning Path: Module 05.1
# -----------------------------------------------------

# 1. Define the tools
@tool
def get_weather(location: str):
    """Call to get the current weather for a specific location."""
    print(f"\n[TOOL EXECUTION] Fetching weather for {location}...")
    if location.lower() == "seattle":
        return "45 degrees and raining."
    return "72 degrees and sunny."

tools = [get_weather]

# 2. Define the State
class AgentState(TypedDict):
    # The `operator.add` reducer ensures new messages are APPENDED to the log array
    messages: Annotated[Sequence[BaseMessage], operator.add]

# 3. Define the LLM Model Node
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

def agent_reasoner_node(state: AgentState):
    print("\n[NODE] Agent_Reasoner is thinking...")
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# 4. Define the routing logic (The explicit workflow rules)
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    
    # If the LLM requested an action (tool_calls), route to the Tool Executor
    if getattr(last_message, "tool_calls", None):
        print("\n[ROUTE] LLM requested a tool. Routing state to ToolNode.")
        return "tools"
    
    # If the LLM just generated a text response, end the Loop
    print("\n[ROUTE] LLM provided final string. Terminating loop.")
    return END

# 5. Build the DAG Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_reasoner_node)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

# Compile the Graph
print("Compiling Single Agent DAG...")
graph = builder.compile()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\n[ERROR] Missing environment variable: OPENAI_API_KEY")
        print("Please run: export OPENAI_API_KEY='sk-...'")
        exit(1)
        
    print("\n--- RUNNING SINGLE AGENT PATTERN ---")
    user_input = "Should I wear a jacket in Seattle today?"
    print(f"User Request: {user_input}")
    
    initial_state = {"messages": [HumanMessage(content=user_input)]}
    
    # Run the compiled graph (streaming prevents the terminal from hanging)
    for event in graph.stream(initial_state):
        pass # Nodes print their own execution traces
        
    final_message = event["agent"]["messages"][-1].content
    print(f"\n[FINAL RESPONSE]: {final_message}")
