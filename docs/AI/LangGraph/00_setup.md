# Module 0: Setup and & Prerequisites

Before diving into LangGraph, we need to set up our development environment. We will be using **Ollama** as our local LLM provider, which is free and privacy-focused.

## 1. Prerequisites

- **Python 3.9+**: Ensure you have Python installed.
- **Ollama**: Download and install from [ollama.com](https://ollama.com).

## 2. Environment Setup

We will use **uv** for fast Python package and environment management.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate

# Install dependencies directly from requirements.txt
uv pip install -r src/requirements.txt
```

*See `src/requirements.txt` for the exact versions.*

## 4. Setting up Ollama

1. **Start Ollama**: Run the Ollama application or `ollama serve` in your terminal.
2. **Pull a Model**: We will use `llama3.2` (or `llama3`, `mistral`) for this course. It's lightweight and capable.

```bash
ollama pull llama3.2
```

1. **Verify**:

```bash
ollama run llama3.2 "Hello, are you ready for LangGraph?"
```

If it replies, you are good to go!
