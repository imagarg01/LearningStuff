# GitHub Copilot SDK (Technical Preview)

The **GitHub Copilot SDK** allows developers to embed the powerful agentic capabilities of the GitHub Copilot CLI directly into their own applications. It provides programmatic access to the same engine that powers Copilot in the terminal, enabling you to build custom agents, tools, and workflows.

> [!NOTE]
> The GitHub Copilot SDK is currently in **Technical Preview**. APIs and features are subject to change.

## Key Features

- **Agentic Workflows**: Build applications where Copilot can plan and execute multi-step tasks.
- **Tool Use**: Define custom tools (Python functions) that the agent can invoke to interact with your specific domain or external APIs.
- **Memory & Context**: Supports multi-turn conversations with persistent context, allowing the agent to "remember" previous interactions.
- **Multi-Model Support**: Access various models available through GitHub Copilot (e.g., GPT-4o, Claude 3.5 Sonnet).
- **GitHub Integration**: Built-in authentication and integration with GitHub's ecosystem.
- **MCP Integration**: seamless integration with the Model Context Protocol (MCP) to connect to external data and tools.

## Architecture

The SDK revolves around a few core concepts:

1. **Client**: The entry point for interacting with the SDK. It handles authentication and connection to the Copilot backend.
2. **Session**: Represents a conversation or interaction context. All messages and state are scoped to a session.
3. **Agent**: The AI entity that processes user input, plans actions, calls tools, and generates responses.

## Installation

The SDK is available as a Python package.

```bash
pip install github-copilot-sdk
```

*Note: You must have an active GitHub Copilot subscription.*

## Core Concepts

### 1. Agents and Planning

Unlike simple chat completions, the Copilot SDK uses an "agentic" approach. When given a task, the agent can:

- **Think**: Analyze the request and plan a sequence of steps.
- **Act**: Call available tools to gather information or perform actions.
- **Observe**: Read the output of those tools.
- **Responde**: Synthesize the final answer for the user.

### 2. Tools

Tools are the hands of the agent. You can define any Python function as a tool.

```python
from copilot_sdk import tool

@tool
def get_weather(city: str) -> str:
    """Get the weather for a specific city."""
    # Custom logic here
    return f"The weather in {city} is sunny."
```

### 3. Structured Output

You can force the agent to return data in a specific JSON structure, which is crucial for integrating AI into programmatic workflows where you need reliable machine-readable output.

### 4. Streaming

For real-time user experiences, the SDK supports streaming responses, allowing you to display the agent's "thought process" and partial answers as they differ.

## Next Steps

Explore the examples in the `examples/` directory to see these concepts in action:

- **`hello_world.py`**: Basic setup and simple interaction.
- **`custom_tools_agent.py`**: How to define and use custom tools.
- **`multi_turn_agent.py`**: Managing conversation history.
- **`structured_output_agent.py`**: Extracting JSON data.
- **`streaming_agent.py`**: Handling real-time output.

## Troubleshooting

### Protocol Version Mismatch

If you see `RuntimeError: SDK protocol version mismatch`, it means your GitHub Copilot CLI is outdated.

**Solution 1: Update Extension**

```bash
gh extension upgrade gh-copilot
```

**Solution 2: Manual CLI Installation (Advanced)**
If the extension update doesn't work, install the standalone CLI via npm and point the SDK to it:

1. **Install CLI**:

    ```bash
    npm install -g @githubnext/github-copilot-cli
    ```

2. **Set Environment Variable**:

    ```bash
    export COPILOT_CLI_PATH=$(which github-copilot-cli)
    ```
