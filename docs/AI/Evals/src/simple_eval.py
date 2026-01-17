import json
import re
from typing import List, Dict, Any

# --- Mock Agent ---
# in a real scenario, this would import your actual agent code
def mock_agent_travel_tool(user_query: str) -> str:
    """
    A mock agent that simulates calling a travel booking tool.
    It returns a JSON string representing the tool call.
    """
    # simulating some logic
    if "Paris" in user_query:
        return '{"tool": "book_flight", "destination": "CDG", "date": "2023-10-10"}'
    elif "Tokyo" in user_query:
        return '{"tool": "book_flight", "destination": "HND", "date": "2024-04-01"}'
    else:
        # returns plain text on failure/unknown
        return "I can't help with that."

# --- Eval Logic ---

def run_deterministic_evals():
    """
    Runs a suite of deterministic tests (Exact Match, JSON Validity).
    """
    print("Running Deterministic Evals...")
    
    test_cases = [
        {
            "id": 1,
            "input": "Book a flight to Paris on Oct 10th",
            "expected_key": "destination",
            "expected_value": "CDG"
        },
        {
            "id": 2,
            "input": "I want to go to Tokyo in April",
            "expected_key": "destination",
            "expected_value": "HND"
        }
    ]

    passed = 0
    total = len(test_cases)

    for case in test_cases:
        output = mock_agent_travel_tool(case["input"])
        
        # Metric 1: Valid JSON Check
        try:
            data = json.loads(output)
            is_json = True
        except json.JSONDecodeError:
            is_json = False
        
        # Metric 2: Content verification
        success = False
        if is_json:
            if data.get(case["expected_key"]) == case["expected_value"]:
                success = True
        
        status = "PASS" if success else "FAIL"
        if success:
            passed += 1
            
        print(f"Test {case['id']}: [{status}] Input='{case['input'][:30]}...' -> Output='{output}'")

    print(f"\nResult: {passed}/{total} passed.")

if __name__ == "__main__":
    run_deterministic_evals()
