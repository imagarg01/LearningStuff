# query_expansion.py
import random

def mock_llm_generate(prompt):
    """
    Simulates an LLM call for demonstration purposes.
    In production, replace this with OpenAI/Anthropic/Gemini API calls.
    """
    if "synonyms" in prompt.lower():
        # User asked for synonyms/variations
        return [
            "How to fix a flat tire",
            "Repairing a punctured tyre",
            "Steps to change a car tire",
            "Fixing a flat on a bicycle"
        ]
    elif "sub-questions" in prompt.lower():
        # User asked for decomposition
        return [
            "What is the population of Tokyo?",
            "What is the population of New York?",
            "Compare the two populations."
        ]
    return []

# --- Strategy 1: Multi-Query Expansion ---
def multi_query_expansion(query):
    print(f"\n--- Strategy: Multi-Query Expansion for '{query}' ---")
    
    # 1. Generate variations using LLM
    prompt = f"Generate 4 variations of this query for search retrieval: {query}"
    variations = mock_llm_generate(prompt)
    
    print("Generated Variations:")
    for v in variations:
        print(f" - {v}")
    
    # 2. In a real app, you would retrieve documents for ALL variations
    # results = []
    # for v in variations:
    #     results.extend(collection.query(v))
    # unique_results = deduplicate(results)
    print("Action: Aggregating search results from all variations...")

# --- Strategy 2: Query Decomposition ---
def query_decomposition(complex_query):
    print(f"\n--- Strategy: Query Decomposition for '{complex_query}' ---")
    
    # 1. Break down the complex query
    prompt = f"Break this complex question into sub-questions: {complex_query}"
    sub_questions = mock_llm_generate(prompt)
    
    print("Sub-questions:")
    for sq in sub_questions:
        print(f" - {sq}")
        # 2. In a real app, answer each sub-question sequentially or in parallel
        # answer = rag_pipeline(sq)
        # print(f"   -> Found answer for '{sq}'")

# Test Run
multi_query_expansion("How do I fix a flat?")
query_decomposition("Compare the population of Tokyo and New York")
