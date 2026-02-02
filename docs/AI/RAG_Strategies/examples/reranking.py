from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# Sample Data: Ambiguous query "Jaguar"
DOCS = [
    Document(page_content="The jaguar is a large cat species native to the Americas."),
    Document(page_content="Jaguar Cars is a luxury vehicle brand of Jaguar Land Rover."),
    Document(page_content="The Jacksonville Jaguars are a professional football team."),
    Document(page_content="Jaguar speed is impressive in the wild."),
    Document(page_content="The new Jaguar F-Type hits 60mph in 3.5 seconds."),
]

def main():
    print("--- Setting up Re-ranking (Vector -> CrossEncoder) ---")
    
    # 1. Base Retrieval (High recall, low precision)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(DOCS, embeddings, collection_name="rerank_test")
    
    # Retrieve top 5 (likely mix of Car, Animal, Football)
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # 2. Re-ranker (High precision, slower)
    # Using a small BAAI reranker model for demo
    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    compressor = CrossEncoderReranker(model=model, top_n=2)
    
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=base_retriever
    )
    
    # Query specifying intent
    query = "What is the top speed of the british car brand?"
    print(f"\nQuery: '{query}'")
    
    print("\n--- Without Re-ranking (Top 2) ---")
    base_results = base_retriever.invoke(query)
    for doc in base_results[:2]:
        print(f"- {doc.page_content}")

    print("\n--- With Re-ranking (Top 2) ---")
    reranked_results = compression_retriever.invoke(query)
    for doc in reranked_results:
        print(f"- {doc.page_content}")

if __name__ == "__main__":
    main()
