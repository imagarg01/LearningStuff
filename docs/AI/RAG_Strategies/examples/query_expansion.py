from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import logging

# Setup logging to see the generated queries
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

DOCS = [
    Document(page_content="Capital One offers credit cards with cash back rewards."),
    Document(page_content="Interest rates for savings accounts are rising."),
    Document(page_content="Applying for a mortgage requires a credit check."),
]

def main():
    print("--- Setting up Query Expansion (Multi-Query) ---")
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(DOCS, embeddings, collection_name="multiquery_test")
    
    # NOTE: This requires Ollama running locally (or OpenAI API key)
    # Falling back to a mock LLM for demonstration if no server found would be ideal,
    # but for this code to be 'real' we assume an LLM is available.
    # User might need to run `ollama run llama3`
    try:
        llm = ChatOllama(model="llama3") 
        
        retriever = MultiQueryRetriever.from_llm(
            retriever=vectorstore.as_retriever(), 
            llm=llm
        )
        
        query = "How to get money for a house?"
        print(f"\nOriginal Query: '{query}'")
        print("(Generating alternative queries... check logs/output)")
        
        results = retriever.invoke(query)
        for doc in results:
            print(f"- {doc.page_content}")
            
    except Exception as e:
        print(f"\n[!] Error: Could not connect to LLM (Ollama). Ensure it's running.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    main()
