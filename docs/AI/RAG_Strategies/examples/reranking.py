# reranking.py
from sentence_transformers import CrossEncoder

# 1. Load Cross-Encoder Model
# This model is trained to score the similarity between (Query, Document) pairs.
print("Loading Cross-Encoder model (this might take a moment)...")
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# 2. Sample Data
query = "What is the capital of France?"

# In a real scenario, these would be the top-K results from your Bi-Encoder (Dense) retrieval
retrieved_documents = [
    "Paris is the capital and most populous city of France.",  # Relevant
    "Lyon is a major city in France's Auvergne-Rhône-Alpes region.", # Related but wrong
    "France is a country in Western Europe.", # Too broad
    "Berlin is the capital of Germany.", # Irrelevant
    "The Eiffel Tower is located in Paris." # Relevant context but not direct answer
]

print(f"\nQuery: {query}")
print(f"Retrieved {len(retrieved_documents)} candidates.")

# 3. Create Pairs for Scoring
pairs = [[query, doc] for doc in retrieved_documents]

# 4. Score Pairs
scores = model.predict(pairs)

# 5. Rank and Display
scored_docs = zip(scores, retrieved_documents)
sorted_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)

print("\n--- Re-ranked Results ---")
for score, doc in sorted_docs:
    print(f"Score: {score:.4f} | {doc}")
