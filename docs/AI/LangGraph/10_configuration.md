# Module 10: Configuration

Often you need to change the behavior of your graph at runtime without rebuilding it. For example, you might want to:

* Switch between different LLMs (GPT-4 vs GPT-3.5).
* Toggle specific features (e.g., "Verbose Mode").
* Pass a `user_id` for personalization.

LangGraph allows you to pass a `config` object to every node.

## 1. Using `configurable` fields

You can define parameters that can be overridden at runtime using the `configurable` dictionary inside configuration.

### Definition in Node

Access the config argument in your node function:

```python
from langchain_core.runnables import RunnableConfig

def my_node(state: State, config: RunnableConfig):
    # Access configurable fields
    user_id = config.get("configurable", {}).get("user_id")
    model_name = config.get("configurable", {}).get("model_name", "gpt-3.5-turbo")
    
    # Use these in your logic
    ...
```

### Passing at Runtime

When invoking the graph, pass the `config` dictionary:

```python
graph.invoke(
    {"messages": [...]}, 
    config={"configurable": {"user_id": "123", "model_name": "gpt-4"}}
)
```

## 2. Standard Configuration Keys

Besides `configurable`, the config object contains standard LangChain keys:

* `callbacks`: specialized callbacks for monitoring.
* `recursion_limit`: max number of steps (default 25) to prevent infinite loops.
* `thread_id`: used for checkpointing (memory).
