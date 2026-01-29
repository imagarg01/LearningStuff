import os
import json
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ContextGraphBuilder:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def close(self):
        self.driver.close()

    def extract_graph_data(self, text):
        """
        Uses an LLM to extract entities and relationships from text.
        """
        prompt = f"""
        Extract key entities (Person, Organization, Location, Event, Concept) and relationships from the following text.
        Return a JSON object with two lists: 'nodes' and 'edges'.
        
        Node format: {{ "id": "unique_id", "label": "Type", "properties": {{ "name": "Name" }} }}
        Edge format: {{ "source": "source_id", "target": "target_id", "type": "RELATIONSHIP_TYPE", "properties": {{}} }}
        
        Text:
        {text}
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

    def populate_graph(self, data):
        """
        Writes the extracted nodes and edges to Neo4j.
        """
        with self.driver.session() as session:
            # Create constraints (optional, for performance)
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE")
            
            # 1. Create Nodes
            for node in data.get('nodes', []):
                query = f"""
                MERGE (n:Entity {{id: $id}})
                SET n:{node['label']}, n += $props
                """
                session.run(query, id=node['id'], props=node['properties'])
                print(f"Created Node: {node['properties'].get('name', node['id'])}")

            # 2. Create Edges
            for edge in data.get('edges', []):
                query = """
                MATCH (s:Entity {id: $source_id})
                MATCH (t:Entity {id: $target_id})
                MERGE (s)-[r:RELATION {type: $type}]->(t)
                SET r += $props
                WITH s, t, r
                CALL apoc.create.setRelType(r, $type) YIELD rel
                RETURN rel
                """
                # Dynamic relationship types require APOC or string interpolation (simplified here with interpolation)
                # Ideally use specific cypher statements for specific relation types or APOC.
                # For this simplified example, we use a slightly different approach to allow dynamic types safely:
                
                query = f"""
                MATCH (s:Entity {{id: $source_id}})
                MATCH (t:Entity {{id: $target_id}})
                MERGE (s)-[r:`{edge['type']}`]->(t)
                SET r += $props
                """
                session.run(query, source_id=edge['source'], target_id=edge['target'], props=edge['properties'])
                print(f"Created Edge: {edge['source']} -[{edge['type']}]-> {edge['target']}")

def main():
    if not OPENAI_API_KEY:
        print("Please set OPENAI_API_KEY in .env file")
        return

    builder = ContextGraphBuilder()
    
    text = """
    Elon Musk, the CEO of SpaceX and Tesla, was born in Pretoria, South Africa. 
    In 2002, he founded SpaceX with the goal of reducing space transportation costs.
    Tesla, headquartered in Austin, Texas, creates electric vehicles and clean energy generation.
    """
    
    print(f"Propagating Graph from text:\n{text}\n")
    
    try:
        data = builder.extract_graph_data(text)
        print("Extracted Data:", json.dumps(data, indent=2))
        builder.populate_graph(data)
        print("\nGraph population complete!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        builder.close()

if __name__ == "__main__":
    main()
