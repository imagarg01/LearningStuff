# naive_rag.py
import chromadb
from chromadb.utils import embedding_functions

# 1. Setup ChromaDB and Embedding Function
# We use a default lightweight embedding model for this demo
client = chromadb.Client()
collection = client.create_collection(
    name="naive_rag_demo",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

# 2. Add Documents
documents = [
    "Apple is a technology company headquartered in Cupertino, California.",
    "A banana is an elongated, edible fruit – botanically a berry.",
    "The iPhone was first released in 2007 by Steve Jobs.",
    "Monkeys love eating bananas because they are sweet.",
    "Microsoft was founded by Bill Gates and Paul Allen."
]
ids = [f"id_{i}" for i in range(len(documents))]
metadatas = [{"category": "tech"} if "Apple" in d or "Microsoft" in d or "iPhone" in d else {"category": "fruit"} for d in documents]

print("Indexng documents...")
collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

# 3. Query
query = "Tell me about tech giants"
print(f"\nQuery: '{query}'")

results = collection.query(
    query_texts=[query],
    n_results=2
)

# 4. Display Results
print("\n--- Results ---")
for i, doc in enumerate(results['documents'][0]):
    print(f"Result {i+1}: {doc} (Distance: {results['distances'][0][i]:.4f})")
