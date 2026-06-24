import os
from typing import Annotated, Sequence, TypedDict, Literal
import operator
from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# -----------------------------------------------------
# Pattern 3: Orchestrator-Workers Architecture
# Mapped to Agent Learning Path: Module 05.3
# -----------------------------------------------------

# 1. Define the Shared Swarm State
class SwarmState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str # Crucial explicitly tracked routing parameter

# 2. Define the LLMs
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# The structured output required from the Supervisor
class RouteSchema(BaseModel):
    destination: Literal["finance", "support", "finish"] = Field(
        description="Route to finance for billing/refunds. Route to support for tech issues/passwords. Route to finish if the user request has been fulfilled."
    )

supervisor_router = llm.with_structured_output(RouteSchema)

# 3. Define the Supervisor Node
def supervisor_node(state: SwarmState):
    print("\n[NODE: SUPERVISOR] Analyzing state dictionary...")
    
    # We pass the conversation history to the Supervisor so it knows what has been done
    route_decision = supervisor_router.invoke([
        {"role": "system", "content": "You are the central routing supervisor. Read the conversation below and decide the next node."},
    ] + list(state["messages"]))
    
    print(f"  -> Supervisor Decision: Route task to '{route_decision.destination.upper()}'")
    return {"next_node": route_decision.destination}

# 4. Define Specialized Worker Nodes
def finance_worker_node(state: SwarmState):
    print("\n[NODE: FINANCE WORKER] Executing localized state context...")
    
    # Note: A real implementation would bind Stripe/Billing API tools here.
    response = llm.invoke([
         {"role": "system", "content": "You are a Finance bot. Answer the billing query. Sign your response '- Finance Team'"}
    ] + list(state["messages"]))
    
    # Worker finishes its generation and hands control BACK to supervisor
    return {"messages": [response], "next_node": "supervisor"}

def support_worker_node(state: SwarmState):
    print("\n[NODE: SUPPORT WORKER] Executing localized state context...")
    
    # Note: A real implementation would bind Jira/Github tools here.
    response = llm.invoke([
         {"role": "system", "content": "You are a Tech Support bot. Answer the IT query. Sign your response '- IT Support'"}
    ] + list(state["messages"]))
    
    return {"messages": [response], "next_node": "supervisor"}

# 5. Build the Hierarchical DAG
builder = StateGraph(SwarmState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("finance", finance_worker_node)
builder.add_node("support", support_worker_node)

builder.set_entry_point("supervisor")

# The crucial Conditional Edges based on the explicit `next_node` string variable
def route_from_supervisor(state: SwarmState):
    if state["next_node"] == "finish":
        print("\n[ROUTE] Supervisor declared 'finish'. Terminating Swarm graph.")
        return END
    return state["next_node"]

builder.add_conditional_edges("supervisor", route_from_supervisor)

# Workers blindly loop back to the supervisor when done running their localized logic
builder.add_edge("finance", "supervisor")
builder.add_edge("support", "supervisor")

print("Compiling Orchestrator-Workers DAG...")
graph = builder.compile()

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("\n[ERROR] Missing environment variable: OPENAI_API_KEY")
        print("Please run: export OPENAI_API_KEY='sk-...'")
        exit(1)
        
    print("\n--- RUNNING MULTI-AGENT ORCHESTRATOR PATTERN ---")
    user_input = "Can you reset my router password?"
    print(f"User Request: {user_input}")
    
    initial_state = {"messages": [HumanMessage(content=user_input)], "next_node": ""}
    
    # Execute the graph
    final_state = graph.invoke(initial_state)
    final_message = final_state["messages"][-1].content
    print(f"\n[FINAL RESPONSE]:\n{final_message}")
