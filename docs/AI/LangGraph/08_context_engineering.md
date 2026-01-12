# Module 8: Context Engineering (RAG)

"Context Engineering" often refers to effectively retrieving and injecting relevant information into the LLM's context window. This is commonly known as **RAG** (Retrieval-Augmented Generation).

## 1. The RAG Flow

1. **Retrieve**: Based on the user query, fetch relevant documents from a store (Vector DB, or simple list).
2. **Augment**: Add these documents to the state (usually into a `context` key or directly into the message history).
3. **Generate**: The LLM answers using the retrieved context.

## 2. Dynamic System Prompts

In LangGraph, you can dynamically construct the system prompt in a node based on the current state.

```python
def augment_node(state):
    docs = retrieve(state["question"])
    context_str = "\n".join(docs)
    return {"context": context_str}

def generate_node(state):
    prompt = f"Answer using this context: {state['context']}"
    # ... call LLM
```

## 3. Query Analysis

Before retrieving, it is often useful to have a node that "analyzes" or "rewrites" the query to be more search-friendly.
