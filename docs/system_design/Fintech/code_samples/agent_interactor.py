# Mock AI Agent Service
import time
import json

class MockVectorDB:
    """Mock for Pinecone/Milvus"""
    def search(self, user_id, query):
        # In reality, this searches embeddings
        return [
            "User previously asked about high-risk stocks.",
            "User wants to save for a house."
        ]

class MockReadModel:
    """Mock for Redis"""
    def get_balance(self, user_id):
        return 2500.00
    
    def get_monthly_spend(self, user_id):
        return 1600.00

class FinancialAdvisorAgent:
    def __init__(self):
        self.memory = MockVectorDB()
        self.data_source = MockReadModel()

    def process_event(self, event):
        """
        Consumes a 'Conversation_Started' event.
        1. Context Injection (Search VectorDB)
        2. Real-time Data Fetch (Redis)
        3. LLM Generation (Mocked)
        """
        user_id = event['user_id']
        query = event['query']
        
        print(f"\n[Agent] Processing query for {user_id}: '{query}'")

        # 1. Retrieve Long-term Memory
        context = self.memory.search(user_id, query)
        print(f"[Agent] Retrieved Context: {context}")

        # 2. Retrieve Real-time Financial Data
        balance = self.data_source.get_balance(user_id)
        spend = self.data_source.get_monthly_spend(user_id)
        print(f"[Agent] Real-time Data - Balance: ${balance}, Spend: ${spend}")

        # 3. Construct Prompt (Concept)
        prompt = f"""
        System: You are a financial advisor.
        Context: {context}
        User Data: Balance={balance}, MonthlySpend={spend}
        User Query: {query}
        """

        # 4. Generate Response (Mocked LLM)
        advice = self.generate_llm_response(prompt, balance, spend)
        
        # 5. Emit 'Advice_Generated' event
        output_event = {
            "type": "Advice_Generated",
            "user_id": user_id,
            "payload": advice,
            "timestamp": time.time()
        }
        return output_event

    def generate_llm_response(self, prompt, balance, spend):
        # logic to simulate LLM decision
        if "afford" in prompt:
            disposable = balance - 800 # Assume $800 min balance
            if 500 < disposable:
                return "Yes, you can afford it, but it's tight."
            else:
                return f"No. You have ${balance} but spent ${spend} this month."
        return "I can help with that."

# Simulation
if __name__ == "__main__":
    agent = FinancialAdvisorAgent()
    
    # Incoming Event from Kafka
    incoming_event = {
        "user_id": "u123",
        "query": "Can I afford this $500 watch?"
    }
    
    response = agent.process_event(incoming_event)
    print(f"\n[Outcome] Emitted Event:\n{json.dumps(response, indent=2)}")
