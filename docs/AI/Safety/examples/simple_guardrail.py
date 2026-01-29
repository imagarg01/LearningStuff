import re
import math

# Simple Custom Guardrail
# 1. PII Redaction (Regex)
# 2. Topical Guardrail (Semantic Similarity simulation)

def redact_pii(text):
    """
    Redacts email addresses from the input text.
    In production, use Microsoft Presidio for robust NER.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    redacted_text = re.sub(email_pattern, '<EMAIL_REDACTED>', text)
    return redacted_text

def topical_guardrail(query, allowed_topics, threshold=0.5):
    """
    Simulates a semantic guardrail.
    If the query semantically matches an 'allowed topic', pass.
    Otherwise, block.
    
    In reality, you would use:
    query_vec = embedding_model.encode(query)
    topic_vec = embedding_model.encode(topic)
    score = cos_sim(query_vec, topic_vec)
    """
    print(f"Checking Topic Safety for: '{query}'")
    
    # Naive keyword simulation for demo purposes
    query_words = set(query.lower().split())
    
    for topic in allowed_topics:
        topic_words = set(topic.lower().split())
        # Jaccard similarity as a proxy for cosine similarity
        intersection = query_words.intersection(topic_words)
        union = query_words.union(topic_words)
        score = len(intersection) / len(union) if union else 0.0
        
        if score > 0.1: # Low threshold for keyword match demo
            print(f" -> Matched Topic: '{topic}' (Score: {score:.2f}) -> PASS")
            return True, f"Proceed with query about {topic}"
            
    print(" -> No allowed topic matched -> BLOCK")
    return False, "I cannot answer questions outside of: " + ", ".join(allowed_topics)

def main():
    print("--- AI Guardrail Demo ---")
    
    # 1. PII Test
    raw_input = "My email is ashish@example.com, please contact me."
    print(f"\n[Input]: {raw_input}")
    clean_input = redact_pii(raw_input)
    print(f"[Guardrail - PII]: {clean_input}")
    
    # 2. Topical Test
    # Scenario: A customer support bot for a Bank
    allowed_topics = ["bank account balance", "credit card limit", "transaction history"]
    
    user_queries = [
        "What is my credit card limit?",
        "Who is the president of the US?",
        "Show me my bank account history"
    ]
    
    print("\n[Guardrail - Topic Filter]")
    for q in user_queries:
        is_safe, message = topical_guardrail(q, allowed_topics)
        print(f"   Action: {message}\n")

if __name__ == "__main__":
    main()
