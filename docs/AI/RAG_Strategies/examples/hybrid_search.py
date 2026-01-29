# hybrid_search.py
import chromadb
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
import numpy as np

# Ensure punkt is downloaded for tokenization
nltk.download('punkt', quiet=True)

# --- Sample Data ---
documents = [
    "The python programming language is great for data science.",
    "A python is a large constricting snake.",
    "Java is popular for enterprise backend development.",
    "The Amazon rainforest is home to many snakes.",
    "Pandas is a python library for data manipulation."
]
ids = [f"id_{i}" for i in range(len(documents))]

# --- 1. Dense Retrieval Setup (Vector Search) ---
client = chromadb.Client()
collection = client.create_collection(name="hybrid_demo")
collection.add(documents=documents, ids=ids)

# --- 2. Sparse Retrieval Setup (BM25) ---
tokenized_corpus = [word_tokenize(doc.lower()) for doc in documents]
bm25 = BM25Okapi(tokenized_corpus)

def hybrid_search(query, alpha=0.5, k=3):
    """
    Perform hybrid search using weighted sum of Dense and Sparse scores.
    Args:
        alpha: Weight for Dense Search (0.0 to 1.0). 1.0 = Pure Vector, 0.0 = Pure Keyword.
    """
    print(f"\n--- Hybrid Search (Alpha={alpha}) for: '{query}' ---")
    
    # A. Dense Search Results
    dense_results = collection.query(query_texts=[query], n_results=len(documents))
    dense_ids = dense_results['ids'][0]
    # In Chroma, smaller distance = better. Convert to similarity score (approx).
    # Simple inversion for demo: score = 1 / (1 + distance)
    dense_distances = dense_results['distances'][0]
    dense_scores = {id_: 1 / (1 + d) for id_, d in zip(dense_ids, dense_distances)}
    
    # Normalize Dense Scores (0-1)
    max_dense = max(dense_scores.values()) if dense_scores else 1
    dense_scores = {k: v / max_dense for k, v in dense_scores.items()}

    # B. Sparse Search Results (BM25)
    tokenized_query = word_tokenize(query.lower())
    sparse_raw_scores = bm25.get_scores(tokenized_query)
    # Map index to ID
    sparse_scores_dict = {ids[i]: score for i, score in enumerate(sparse_raw_scores)}
    
    # Normalize Sparse Scores (0-1)
    max_sparse = max(sparse_scores_dict.values()) if sparse_scores_dict.values() and max(sparse_scores_dict.values()) > 0 else 1
    if max_sparse == 0: max_sparse = 1
    sparse_scores_dict = {k: v / max_sparse for k, v in sparse_scores_dict.items()}

    # C. Combine Scores
    final_scores = []
    for doc_id, doc_text in zip(ids, documents):
        d_score = dense_scores.get(doc_id, 0.0)
        s_score = sparse_scores_dict.get(doc_id, 0.0)
        final_score = (alpha * d_score) + ((1 - alpha) * s_score)
        final_scores.append((doc_text, final_score, d_score, s_score))
    
    # Sort by Final Score
    final_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Print Top K
    for i in range(min(k, len(final_scores))):
        doc, score, d_s, s_s = final_scores[i]
        print(f"{i+1}. {doc} \n   (Score: {score:.4f} | Dense: {d_s:.4f} | Sparse: {s_s:.4f})")

# Test Cases
# 1. "python snake" -> Semantic match for snake, keyword match for python
hybrid_search("python snake", alpha=0.5)

# 2. "data science library" -> Strong semantic signal
hybrid_search("data science library", alpha=0.8)

# 3. "Java" -> Exact keyword match
hybrid_search("Java", alpha=0.2)
