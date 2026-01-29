# test_deepeval.py
import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

# To run this:
# 1. pip install deepeval
# 2. export OPENAI_API_KEY=sk-...
# 3. pytest docs/AI/RAG_Strategies/examples/test_deepeval.py

# --- Mock Data ---
# In a real app, you would retrieve `actual_output` and `retrieval_context` from your RAG function.

def get_rag_response(query):
    # Simulating a RAG Pipeline response
    if "capital of France" in query:
        return {
            "output": "Paris is the capital of France.",
            "context": ["Paris is the capital and most populous city of France."]
        }
    elif "moon made of" in query:
        # Simulating a Hallucination (Context says rock, output says cheese)
        return {
            "output": "The moon is made of green cheese.",
            "context": ["The Moon is an astronomical body chiefly composed of rock and metal."]
        }
    return {"output": "I don't know.", "context": []}

# --- Test Cases ---

def test_answer_relevancy():
    """
    Check if the answer is relevant to the query.
    """
    query = "What is the capital of France?"
    response = get_rag_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response["output"],
        retrieval_context=response["context"]
    )
    
    # Threshold 0.5 means it must be at least 50% relevant
    metric = AnswerRelevancyMetric(threshold=0.5)
    
    # assert_test will make the pytest fail if the score is low
    assert_test(test_case, [metric])

def test_hallucination():
    """
    Check if the answer contradicts the context.
    This test serves as a 'Negative Test' - we expect it to fail if our model hallucinates.
    """
    query = "What is the moon made of?"
    response = get_rag_response(query)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=response["output"],
        retrieval_context=response["context"]
    )
    
    metric = HallucinationMetric(threshold=0.5)
    
    # This will PASS if there is NO hallucination.
    # Since our mock data HAS a hallucination (Cheese vs Rock), this assert should FAIL.
    # In a real suite, failure means "Found a bug".
    assert_test(test_case, [metric])
