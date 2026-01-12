# Module 9: Streaming

Streaming is essential for building responsive AI applications. LangGraph provides first-class support for streaming updates from your graph as they happen.

## 1. Streaming Modes

When you call `.stream()` or `.astream()`, you can control *what* gets streamed back using `stream_mode`:

* **`"values"`**: Emits the **full state** every time it changes. Good for debugging or simple chat UIs where you just want the latest massive history.
* **`"updates"`** (Default): Emits only the **delta** (what changed) from the last step. Efficient and preferred for most apps.
* **`"debug"`**: Emits detailed metadata about every step, including input, output, and timestamps.

```python
async for chunk in graph.astream(inputs, stream_mode="updates"):
    for node, values in chunk.items():
        print(f"Update from {node}: {values}")
```

## 2. Streaming Tokens (`astream_events`)

For a chat experience where you see the message appearing character-by-character, you need to stream **events** from within the LLM, not just graph state updates.

Use `.astream_events(inputs, version="v2")`.

This enables you to filter for specific types of events, such as:

* `on_chat_model_stream`: Tokens being generated.
* `on_tool_start` / `on_tool_end`: Tool usage indicators.

```python
async for event in graph.astream_events(inputs, version="v2"):
    kind = event["event"]
    if kind == "on_chat_model_stream":
        # Print tokens as they arrive
        print(event["data"]["chunk"].content, end="", flush=True)
```

## 3. Streaming Tool Calls

You can also stream when a tool is being called and when it completes. This helps build UIs that show "Reading file..." or "Searching web..." status indicators.

* Filter for `event["event"] == "on_tool_start"` to show a loading spinner.
* Filter for `event["event"] == "on_tool_end"` to hide it and show the result.
