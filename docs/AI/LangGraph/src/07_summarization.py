import uuid
from typing import TypedDict, Annotated, List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Setup
llm = ChatOllama(model="llama3.2")

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    summary: str

def call_model(state: State):
    summary = state.get("summary", "")
    messages = state["messages"]
    
    # Inject summary if it exists
    if summary:
        system_msg = SystemMessage(content=f"Summary of conversation so far: {summary}")
        # Note: We don't want to persist this specific system message forever in the list 
        # normally, but for simplicity here we just prepend it to the context sent to LLM.
        response = llm.invoke([system_msg] + messages)
    else:
        response = llm.invoke(messages)
    
    return {"messages": [response]}

def summarize_conversation(state: State):
    print("--- Summarizing Conversation ---")
    summary = state.get("summary", "")
    messages = state["messages"]
    
    # Create the prompt for summarization
    if summary:
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above:"
    
    messages_to_summarize = messages + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages_to_summarize)
    new_summary = response.content
    
    # We want to keep the last 2 messages (usually the latest Q & A) so the context isn't lost abruptly
    delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]]
    
    return {"summary": new_summary, "messages": delete_messages}

def should_summarize(state: State):
    """Return either 'summarize_conversation' or END"""
    messages = state["messages"]
    if len(messages) > 4: # Simple threshold logic for demo
        return "summarize_conversation"
    return END

# Build Graph
builder = StateGraph(State)
builder.add_node("conversation", call_model)
builder.add_node("summarize_conversation", summarize_conversation)

builder.add_edge(START, "conversation")
builder.add_conditional_edges("conversation", should_summarize)
builder.add_edge("summarize_conversation", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Demo
if __name__ == "__main__":
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("--- Chat (summarizes after 4 msgs) ---")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]: break
        
        events = graph.stream(
            {"messages": [HumanMessage(content=user_input)]}, 
            config=config
        )
        for event in events:
            if "conversation" in event:
                print(f"Bot: {event['conversation']['messages'][-1].content}")
            if "summarize_conversation" in event:
                print(f"[System]: Summarized history. New Summary: {event['summarize_conversation']['summary'][:50]}...")
