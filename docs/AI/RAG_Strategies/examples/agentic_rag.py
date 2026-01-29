# agentic_rag.py
import random

# --- Components ---

def retrieval_node(query):
    """
    Simulates retrieving documents.
    """
    print(f"   [Retrieve] Searching for: '{query}'")
    # Simulate partial failure
    if "latest" in query:
        return ["Old news from 2021 about AI."]
    elif "weather" in query:
        return ["It is sunny today."]
    else:
        return ["General knowledge text."]

def grader_node(query, context):
    """
    Simulates an 'Evaluator' LLM checking relevance.
    """
    print("   [Grade] Checking relevance...")
    # Mock logic: if "Old" is in text and query asks for "latest", it's irrelevant.
    if "latest" in query and "Old" in context[0]:
        return "irrelevant"
    return "relevant"

def web_search_node(query):
    """
    Simulates a Fallback Web Search tool.
    """
    print(f"   [Web Search] Fallback search for: '{query}'")
    return ["New York Times 2024: AI has evolved."]

def generate_node(query, context):
    """
    Simulates Final Answer Generation.
    """
    print(f"   [Generate] Answering '{query}' using {context}")

# --- The Agentic Workflow (Corrective RAG) ---

def agentic_rag_pipeline(query):
    print(f"\n--- Running CRAG Pipeline for: '{query}' ---")
    
    # 1. Retrieve
    context = retrieval_node(query)
    
    # 2. Grade / Evaluate
    grade = grader_node(query, context)
    
    # 3. self-Correct
    if grade == "irrelevant":
        print("   [Decision] Context was irrelevant. Triggering Web Search.")
        # Corrective action: Ignore bad context, get new context
        context = web_search_node(query)
    else:
        print("   [Decision] Context is good. Proceeding.")
    
    # 4. Generate
    generate_node(query, context)

# --- Test ---
agentic_rag_pipeline("What is the weather?")
agentic_rag_pipeline("What is the latest AI news?")
