# 2. Problem Selection and Architecture

Taking an agent from a toy-script to a production system requires rigorous architectural decisions. We focus entirely on **Python** and **LangGraph** as the execution stack.

## 2.1 The Flowchart Test: Do you even need an Agent?

The biggest trap for a senior engineer is using an Agent to solve a deterministic problem. Agents are slow, expensive, and unpredictable.

```mermaid
graph TD
    A[Start Feature Design] --> B{Can I write a flowchart<br/>for 98% of edge cases?}
    B -->|Yes| C[Build Deterministic Code / Workflow]
    B -->|No - Path depends entirely<br/>on runtime data discovery| D[Build an Autonomous Agent]
```

## 2.2 Advanced Function Calling: The Parallel Paradigm

*Reference: OpenAI Function Calling Architecture*

When you initialize your LLM, you pass a JSON schema array defining your tools. The LLM does not execute code; it generates a payload requesting your backend to execute it.

```json
// LLM Response requesting Parallel Execution
"tool_calls": [
  {"id": "c1", "type": "function", "function": {"name": "get_weather", "arguments": "{\"city\": \"Seattle\"}"}},
  {"id": "c2", "type": "function", "function": {"name": "get_weather", "arguments": "{\"city\": \"SF\"}"}}
]
```
**Architecture Rule:** Your Python backend must execute these array items concurrently `asyncio.gather(*tool_tasks)` and return exactly 2 observations.

## 2.3 State Machines: Abstracting the Loop with LangGraph

You could write that interception loop yourself via endless `while` loops, but production architecture requires routing, retry bounds, and state persistence. **LangGraph** treats agents as **Directed Acyclic Graphs (DAGs)**.

### Architectural Diagram Mapping

```mermaid
stateDiagram-v2
    [*] --> Agent_Reasoner : Pass State Dictionary
    
    Agent_Reasoner --> Conditional_Edge : Evaluates String Output
    
    state Conditional_Edge {
        direction LR
        If_ToolCalls
        If_FinalAnswer
    }
    
    Conditional_Edge --> Tool_Executor : If_ToolCalls requested
    Tool_Executor --> Agent_Reasoner : Append Tool Result to State
    
    Conditional_Edge --> [*] : If_FinalAnswer provided
```

1.  **Node: `Agent_Reasoner`:** The LLM receives the State (RAM). It outputs a Tool Call request.
2.  **Conditional Edge: `evaluate_output`:** Your code inspects the LLM's output. 
    *   *If* output has `tool_calls` -> Route to **Tool_Executor**.
    *   *If* output is plain text -> Route to **End**.
3.  **Node: `Tool_Executor`:** Dynamically invokes the requested tool API, appends the result to the array, and loops back.

### Handling Failure States Natively (MCP `SEP-1303` Failing Forward)
> [!WARNING]
> **Anti-Pattern:** Never pass raw Python stack traces (`Traceback (most recent call last)...`) or unhandled HTTP 500 dumps back into the LLM's message array. Raw tracebacks waste tokens, leak internal implementation details, and cause smaller models to hallucinate or loop infinitely.

Instead, follow the **MCP `SEP-1303` Failing Forward** standard (detailed in [Skills Execution Architecture](../Skills/02_execution_architecture.md)):
1. Catch validation and execution errors inside the deterministic tool boundary.
2. Return a structured `CallToolResult` with **`isError: true`** and a concise **Semantic Recovery Hint** (e.g., `"Invalid date '10/31/2026'. Expected ISO-8601 format 'YYYY-MM-DD'. Please retry."`).
3. **Cognitive Offloading:** Keep tool `inputSchema` flat ($\le 2$ nesting levels) and push all date math, business `if/else` branching, and multi-table joins into the deterministic MCP tool handler rather than asking the LLM to orchestrate 4 micro-tools in a row.

## 2.4 Shortcomings of the LangGraph DAG Paradigm
While LangGraph provides safety, it has severe limitations:
1.  **State Bloat:** Passing massive dictionaries between nodes exponentially increases memory footprint for long-running swarms.
2.  **Rigidity overhead:** Replacing a simple ReAct loop with 14 distinct Python Nodes/Edges adds massive boilerplate.
3.  **False Autonomy:** Hardcoding conditional edges (`if tool == refund: goto_refund`) is fundamentally a deterministic Workflow, *not* an Agent.

> **Next Path:** Proceed to [Evaluation and Observability](03_Evaluation_and_Observability.md).
