import pytest
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage
# Note: In a real project you might use `unittest.mock` or `FakeListLLM`
# Here we simulate an LLM for testing purposes without external deps
class MockLLM:
    def invoke(self, messages):
        return AIMessage(content="Mock response")

# 1. Define Code to be Tested (usually imported)
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot_node(state: State):
    # Dependency injection pattern is better, but here we just use a global/local mock
    llm = MockLLM()
    return {"messages": [llm.invoke(state["messages"])]}

# 2. Unit Test for Node
def test_chatbot_node_logic():
    print("\n--- Running Unit Test ---")
    initial_state = {"messages": [HumanMessage(content="Hello")]}
    
    # Call the node function directly
    result = chatbot_node(initial_state)
    
    # Assertions
    assert len(result["messages"]) == 1
    assert isinstance(result["messages"][0], AIMessage)
    assert result["messages"][0].content == "Mock response"
    print("Unit Test Passed!")

# 3. Integration Test for Graph
def test_graph_execution():
    print("\n--- Running Integration Test ---")
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot_node)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    graph = builder.compile()
    
    input_state = {"messages": [("user", "Hello")]}
    result = graph.invoke(input_state)
    
    final_msg = result["messages"][-1]
    assert final_msg.content == "Mock response"
    print("Integration Test Passed!")

if __name__ == "__main__":
    # Barebones runner if pytest is not installed
    try:
        test_chatbot_node_logic()
        test_graph_execution()
        print("\nAll tests passed successfully.")
    except AssertionError as e:
        print(f"\nTest failed: {e}")
