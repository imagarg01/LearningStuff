import asyncio
import os
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

# --- 1. State Definition ---
class ResearchState(TypedDict):
    topic: str
    plan: List[str]
    content: List[str]
    report: str

# Models
llm = ChatOpenAI(model="gpt-3.5-turbo")

# --- 2. Nodes ---

def planner_node(state: ResearchState):
    print("--- Planner ---")
    topic = state["topic"]
    # Ask LLM to generate search queries
    msg = [
        SystemMessage(content="You are a research planner. Generate 3 short search queries for the topic."),
        HumanMessage(content=topic)
    ]
    response = llm.invoke(msg)
    # Naive parsing: split by newline
    plan = [line.strip("- ") for line in response.content.split("\n") if line.strip()]
    return {"plan": plan}

def researcher_node(state: ResearchState):
    print("--- Researcher ---")
    plan = state["plan"]
    content = []
    # Mocking search execution for this example
    for query in plan:
        print(f"  > Searching for: {query}")
        # In a real app, use Tavily or generic search tool here
        content.append(f"Results for {query}: Some relevant info about {query}.")
    return {"content": content}

def writer_node(state: ResearchState):
    print("--- Writer ---")
    topic = state["topic"]
    content = "\n".join(state["content"])
    
    msg = [
        SystemMessage(content="You are a report writer. Summarize the research into a short report."),
        HumanMessage(content=f"Topic: {topic}\n\nResearch:\n{content}")
    ]
    response = llm.invoke(msg)
    return {"report": response.content}

# --- 3. Graph Construction ---

builder = StateGraph(ResearchState)
builder.add_node("planner", planner_node)
builder.add_node("researcher", researcher_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", END)

graph = builder.compile()

# --- 4. Execution ---

async def run_research():
    topic = "The integration of AI agents in 2025"
    print(f"Starting research on: {topic}")
    
    # Notice we initialize state with just the topic
    result = await graph.ainvoke({"topic": topic})
    
    print("\n\n=== Final Report ===")
    print(result["report"])

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
         print("Please set OPENAI_API_KEY to run this example.")
    else:
        asyncio.run(run_research())
