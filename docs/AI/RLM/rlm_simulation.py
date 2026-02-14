import time

class MockLLM:
    """
    Simulates an LLM (Like GPT-4) that can reason and break down tasks.
    In a real app, this would be an API call to OpenAI/Claude/Gemini.
    """
    def think(self, prompt):
        # HARDCODED: Simulating the 'thought process' for specific prompts
        
        if "Compare battery life" in prompt:
            return {
                "thought": "I need to find the phones first, then get their specs, then compare.",
                "action": "PLAN",
                "steps": [
                    "Find top 3 Android phones of 2024",
                    "Get battery size for Phone 1",
                    "Get battery size for Phone 2",
                    "Get battery size for Phone 3",
                    "Compare and conclude"
                ]
            }
        
        elif "Find top 3" in prompt:
            return {
                "thought": "I need to search for this list.",
                "action": "TOOL_CALL",
                "tool": "search_google",
                "query": "top 3 android phones 2024"
            }
        
        elif "Get battery size" in prompt:
            phone_name = prompt.split("for")[-1].strip()
            return {
                "thought": f"I need to look up specs for {phone_name}.",
                "action": "TOOL_CALL",
                "tool": "search_spec_sheet",
                "query": f"{phone_name} battery capacity"
            }
            
        else:
             return {
                "thought": "I have all the info. I can answer now.",
                "action": "FINAL_ANSWER",
                "content": "Based on the search, the S24 Ultra has the longest lasting battery due to optimization."
            }

class Tools:
    """
    Your 'Helper Utils' class.
    """
    def search_google(self, query):
        print(f"    [Tool] Googling: '{query}'...")
        time.sleep(0.5) # Simulate latency
        return ["Samsung S24 Ultra", "Pixel 9 Pro", "OnePlus 12"]

    def search_spec_sheet(self, query):
        print(f"    [Tool] Reading Spec Sheet for: '{query}'...")
        time.sleep(0.5)
        if "S24" in query: return "5000 mAh, 15h screen time"
        if "Pixel" in query: return "5050 mAh, 12h screen time"
        if "OnePlus" in query: return "5400 mAh, 14h screen time"
        return "Unknown"

# --- The Recursive Agent (The "Controller") ---

class RecursiveAgent:
    def __init__(self):
        self.llm = MockLLM()
        self.tools = Tools()
        self.memory = {} # "Short-term context"

    def execute_task(self, task, depth=0):
        indent = "  " * depth
        print(f"{indent}➤ [Agent Depth {depth}] Recieved Task: '{task}'")
        
        # 1. Ask LLM what to do
        response = self.llm.think(task)
        print(f"{indent}  [Thinking]: {response['thought']}")
        
        # 2. Handle Plan (Recursion!)
        if response['action'] == 'PLAN':
            print(f"{indent}  [Decision]: Complex task detected. Breaking down...")
            results = []
            for step in response['steps']:
                # RECURSIVE CALL: The agent calls itself for each sub-step!
                print(f"{indent}  --> Spawning sub-agent for: '{step}'")
                result = self.execute_task(step, depth + 1)
                results.append(result)
            
            # Synthesize final answer after introspection
            return f"Comparison Complete: Found {results}"

        # 3. Handle Tool Call (Action)
        elif response['action'] == 'TOOL_CALL':
            tool_name = response['tool']
            if tool_name == 'search_google':
                return self.tools.search_google(response['query'])
            elif tool_name == 'search_spec_sheet':
                return self.tools.search_spec_sheet(response['query'])
        
        # 4. Base Case (Answer)
        elif response['action'] == 'FINAL_ANSWER':
            return response['content']

import sys

# --- Main Execution ---

if __name__ == "__main__":
    print("--- Starting Recursive Language Model (RLM) Simulation ---")
    agent = RecursiveAgent()
    
    # Default query
    default_query = "Compare battery life of top 3 Android phones released in 2024"
    
    # Check for command line argument
    if len(sys.argv) > 1:
        # Join arguments to form the full query string
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = default_query

    final_answer = agent.execute_task(user_query)
    
    print("\n--- Final Output ---")
    print(final_answer)
