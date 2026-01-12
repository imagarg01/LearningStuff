# Module 11: Testing

Reliability is key for agents. You should test your graph at multiple levels.

## 1. Unit Testing Nodes

Nodes are just Python functions. You can test them individually by passing a dummy `State` and asserting the output.

```python
def test_chatbot_node():
    # Setup
    initial_state = {"messages": [("user", "hi")]}
    # Execute (assuming you mocked the LLM inside or use a real one)
    output = chatbot(initial_state)
    # Assert
    assert len(output["messages"]) == 1
```

## 2. Mocking

To test the graph logic without calling expensive APIs, use mocking.

### Mocking Tool Responses

You can use a `MockTool` or simply override the tool node behavior.

### Mocking LLM Responses

Use `langchain_core.language_models.fake.FakeListLLM` to return deterministic responses.

```python
from langchain_core.language_models.fake import FakeListLLM

fake_llm = FakeListLLM(responses=["I am a mock response"])
```

## 3. Integration Testing

Test the full graph flow using a generic `MemorySaver` to inspect the state at the end.

```python
from langgraph.checkpoint.memory import MemorySaver

def test_full_graph():
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    result = graph.invoke(
        {"messages": [("user", "run test")]}, 
        config={"configurable": {"thread_id": "test-1"}}
    )
    
    assert "I am a mock response" in result["messages"][-1].content
```
