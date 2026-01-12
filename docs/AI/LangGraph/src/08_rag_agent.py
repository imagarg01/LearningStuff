from typing import TypedDict, List
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# Setup
llm = ChatOllama(model="llama3.2")

# 1. Setup Dummy Vector Store
# In reality, use langchain_chroma or similar
KNOWLEDGE_BASE = {
    "langgraph": "LangGraph is a library for building stateful, multi-actor applications with LLMs.",
    "ollama": "Ollama is a tool for running open weights LLMs locally.",
    "react": "ReAct is a pattern where models Reason and Act by using tools."
}

def retrieve_docs(query: str) -> List[str]:
    """Simple keyword matching for demo."""
    query = query.lower()
    docs = []
    for key, content in KNOWLEDGE_BASE.items():
        if key in query:
            docs.append(content)
    return docs

# 2. State
class State(TypedDict):
    question: str
    context: List[str]
    answer: str

# 3. Nodes
def retrieve_node(state: State):
    question = state["question"]
    print(f"--- Retrieving Docs for: {question} ---")
    docs = retrieve_docs(question)
    return {"context": docs}

def generate_node(state: State):
    print("--- Generating Answer ---")
    question = state["question"]
    context = state["context"]
    
    if not context:
        context_str = "No specific knowledge found."
    else:
        context_str = "\n".join(context)
    
    # Context Engineering: Constructing the prompt
    system_prompt = (
        "You are a helpful assistant. Use the following context to answer the user's question.\n\n"
        f"Context:\n{context_str}"
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]
    
    response = llm.invoke(messages)
    return {"answer": response.content}

# 4. Build Graph
builder = StateGraph(State)

builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()

# 5. Run
if __name__ == "__main__":
    print("--- Test 1: Known Topic ---")
    result = graph.invoke({"question": "Tell me about LangGraph."})
    print(f"Bot: {result['answer']}")
    
    print("\n--- Test 2: Unknown Topic ---")
    result = graph.invoke({"question": "What is quantum mechanics?"})
    print(f"Bot: {result['answer']}")
