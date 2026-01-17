import re
import random

# --- Mock Agent ---
def mock_code_agent(query: str) -> str:
    """
    A mock agent that generates python code (sometimes successfully, sometimes not).
    """
    if "fibonacci" in query.lower():
        return """
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
"""
    elif "hello world" in query.lower():
        return 'print("Hello World")'
    else:
        return "Sorry, I don't know how to code that."

# --- Mock LLM Judge ---
# In reality, this would call OpenAI/Anthropic API
def mock_llm_judge(prompt: str) -> str:
    """
    Simulates an LLM evaluating the response.
    Returns a string containing a score/reasoning.
    """
    # Simple heuristic to simulate an LLM's "reasoning"
    if "def " in prompt and "return" in prompt:
        return "Score: 5/5. Reasoning: The code looks syntactically correct and efficient."
    elif "print" in prompt:
        return "Score: 4/5. Reasoning: Correct simple script."
    else:
        return "Score: 1/5. Reasoning: No code provided or incorrect format."

# --- Eval Logic ---

def run_llm_judge_eval():
    print("Running LLM-as-a-Judge Evals...")
    
    test_cases = [
        "Write a python function for fibonacci sequence.",
        "Write a python script to print hello world.",
        "Make me a sandwich."
    ]
    
    for query in test_cases:
        # 1. Run the Agent
        agent_output = mock_code_agent(query)
        
        # 2. Construct the Evaluation Prompt for the Judge
        eval_prompt = f"""
        You are a senior code reviewer. Rate the following code snippet on a scale of 1-5.
        
        User Query: {query}
        Agent Response: {agent_output}
        
        Output format: "Score: X/5. Reasoning: ..."
        """
        
        # 3. Call the Judge
        judge_response = mock_llm_judge(eval_prompt)
        
        # 4. Parse the score (Metric Extraction)
        # Regex to find "Score: X/5"
        match = re.search(r"Score:\s*(\d)/5", judge_response)
        score = int(match.group(1)) if match else 0
        
        status = "PASS" if score >= 4 else "FAIL"
        
        print(f"\nQuery: {query}")
        print(f"Agent Output: {agent_output.strip()[:50]}...")
        print(f"Judge Output: {judge_response}")
        print(f"Result: {status} (Score: {score})")

if __name__ == "__main__":
    run_llm_judge_eval()
