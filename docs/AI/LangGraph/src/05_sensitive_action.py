import uuid
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, Interrupt

# 1. State
class State(TypedDict):
    content: str
    status: str

# 2. Nodes
def write_draft(state: State):
    print("--- Step 1: Writing Draft ---")
    return {"content": "Draft: This is a generated email."}

def human_review_node(state: State):
    """
    This node dynamically interrupts execution to ask for human input.
    """
    print("--- Step 2: Human Review ---")
    
    # We raise an Interrupt to pause execution and return a value to the client
    # The client must provide a 'Command(resume=...)' to continue
    value = interrupt(f"Please review: {state['content']}")
    
    # When we resume, 'value' will contain whatever the user provided in Command(resume=value)
    print(f"--- Resumed with value: {value} ---")
    
    if value == "approve":
        return {"status": "approved"}
    elif value == "reject":
         # We can even modify state here or route differently
         return {"status": "rejected"}
    
    return {"status": "unknown"}

def send_email(state: State):
    if state["status"] == "approved":
        print(f"--- Step 3: Sending Email ---")
        print(f"EMAIL SENT: {state['content']}")
    else:
        print("--- Step 3: Skipped Sending (Rejected) ---")
    return {}

# 3. Build Graph
builder = StateGraph(State)
builder.add_node("writer", write_draft)
builder.add_node("reviewer", human_review_node)
builder.add_node("sender", send_email)

builder.add_edge(START, "writer")
builder.add_edge("writer", "reviewer")
builder.add_edge("reviewer", "sender")
builder.add_edge("sender", END)

# 4. Compile
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 5. Run Demo
if __name__ == "__main__":
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("--- Run 1: Start workflow ---")
    
    # We define a helper to handle the interrupt
    # This is a common pattern for running graphs that might pause
    current_input = {"content": ""}
    
    for _ in range(2): # Simple loop to handle the pause-resume cycle
        try:
            # invoke() will raise GraphInterrupt if using interrupt_before, 
            # BUT if using the dynamic 'interrupt()' function, it returns the interrupt payload 
            # and pauses. Wait, let's stick to the 'interrupt_before' or standard 'interrupt' function.
            # LangGraph v0.2 introduced 'interrupt()' function inside nodes.
            # But 'graph.stream' / 'invoke' will simply stop.
            
            result = graph.invoke(current_input, config=config)
            print("Graph finished!")
            break
            
        except Exception as e:
            # Check if it's an interrupt (in older versions) or just inspect state
            # For modern 'interrupt()', the invoke returns, but the property 'graph.get_state(config).tasks' is non-empty
            pass
            
        # Inspect state
        snapshot = graph.get_state(config)
        if snapshot.next:
            print("\n--- Paused at Node: Reviewer ---")
            # We can see the interrupt details if we used interrupt()
            if snapshot.tasks and snapshot.tasks[0].interrupts:
                print(f"Interrupt Prompt: {snapshot.tasks[0].interrupts[0].value}")
            
            decision = input("Approve? (yes/no): ")
            resume_value = "approve" if decision == "yes" else "reject"
            
            print(f"\n--- Resuming with '{resume_value}' ---")
            # We use Command to resume
            current_input = Command(resume=resume_value)
