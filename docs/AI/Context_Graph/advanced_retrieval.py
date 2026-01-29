import os
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ContextGraphRetriever:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def close(self):
        self.driver.close()

    def get_embedding(self, text):
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def hybrid_retrieval(self, query, top_k=5):
        """
        Performs a hybrid search:
        1. Vector Index Search: Find relevant entry points.
        2. Graph Traversal: Expand 1-2 hops to get context.
        """
        query_vector = self.get_embedding(query)
        
        with self.driver.session() as session:
            # Note: This assumes a Vector Index named 'entity_embeddings' exists in Neo4j
            # For this example, we'll simulate the graph traversal part as if we found a start node.
            
            # Simulated Cypher query that would use a vector index
            # CALL db.index.vector.queryNodes('entity_embeddings', $top_k, $embedding) ...
            
            # Here we will just perform a keyword search on the 'name' property as a fallback for the example
            print(f"Searching for entities related to: '{query}'")
            
            result = session.run("""
            // 1. Find potential entry nodes (simulated with string match for demo)
            MATCH (n:Entity)
            WHERE toLower(n.name) CONTAINS toLower($keyword)
            
            // 2. Expand context (1-2 hops)
            CALL apoc.path.subgraphAll(n, {
                maxLevel: 2,
                relationshipFilter: '>'
            })
            YIELD nodes, relationships
            
            RETURN nodes, relationships
            """, keyword=query.split()[0]) # distinct keyword
            
            subgraph = result.single()
            if not subgraph:
                return None
            
            return {
                "nodes": [dict(node) for node in subgraph["nodes"]],
                "relationships": [
                    {
                        "source": rel.start_node["name"], 
                        "target": rel.end_node["name"], 
                        "type": rel.type
                    } 
                    for rel in subgraph["relationships"]
                ]
            }

    def generate_answer(self, query, context):
        """
        Uses the retrieved context to answer the user query.
        """
        if not context:
            return "I couldn't find any relevant information in the context graph."

        # Format context into a readable string
        context_str = "## Graph Context:\n"
        for rel in context['relationships']:
            context_str += f"- {rel['source']} is connected to {rel['target']} via {rel['type']}\n"
        
        for node in context['nodes']:
            props = ", ".join([f"{k}: {v}" for k, v in node.items() if k != 'embedding'])
            context_str += f"- Entity: {props}\n"

        prompt = f"""
        Answer the question based ONLY on the following context graph data.
        
        {context_str}
        
        Question: {query}
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content

def main():
    if not OPENAI_API_KEY:
        print("Please set OPENAI_API_KEY in .env file")
        return

    retriever = ContextGraphRetriever()
    query = "Where is Tesla located?"
    
    try:
        print(f"Querying: {query}")
        context = retriever.hybrid_retrieval(query)
        
        if context:
            print(f"Retrieved {len(context['nodes'])} nodes and {len(context['relationships'])} relationships.")
            answer = retriever.generate_answer(query, context)
            print("\nGenerated Answer:")
            print(answer)
        else:
            print("No context found.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        retriever.close()

if __name__ == "__main__":
    main()
