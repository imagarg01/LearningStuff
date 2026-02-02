import os
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# Sample Data
DOCS = [
    Document(page_content="The iPhone 15 Pro features a titanium design.", metadata={"source": "apple"}),
    Document(page_content="Apples are rich in fiber and vitamin C.", metadata={"source": "nutrition"}),
    Document(page_content="Apple Inc. reported record revenue in Q3.", metadata={"source": "finance"}),
    Document(page_content="How to bake an apple pie with cinnamon.", metadata={"source": "cooking"}),
]

def main():
    print("--- Setting up Hybrid Search (BM25 + Dense) ---")
    
    # 1. Sparse Retriever (BM25)
    # Good for keyword matches like "iPhone" or "Vitamin"
    bm25_retriever = BM25Retriever.from_documents(DOCS)
    bm25_retriever.k = 2
    
    # 2. Dense Retriever (Vector Search)
    # Good for semantic matches like "Tech company earnings" -> "Apple Inc revenue"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(DOCS, embeddings, collection_name="hybrid_test")
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # 3. Ensemble (Hybrid)
    # Weights: 0.5 BM25 + 0.5 Dense
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]
    )
    
    # Test Query 1: Keyword heavy
    query1 = "iPhone titanium"
    results1 = ensemble_retriever.invoke(query1)
    print(f"\nQuery: '{query1}'")
    for doc in results1:
        print(f"- {doc.page_content}")
        
    # Test Query 2: Semantic heavy
    query2 = "Fruit health benefits"
    results2 = ensemble_retriever.invoke(query2)
    print(f"\nQuery: '{query2}'")
    for doc in results2:
        print(f"- {doc.page_content}")

if __name__ == "__main__":
    main()
