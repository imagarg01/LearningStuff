# AI Agent Python Sandbox

This directory contains executable Python scripts demonstrating the foundational local LangGraph architectures discussed in the **Agent Learning Path** (Module 05).

## Prerequisites
1. Ensure you have Python 3.10+ installed.
2. Run `make setup` to install dependencies (LangGraph, LangChain, Pydantic).
3. You must set your OpenAI API key either in your terminal or in a `.env` file in this directory:
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

## Included Architectures

### 1. The Monolithic Baseline (`01_single_agent.py`)
**Demonstrates Pattern 1.** A single LLM equipped with a mock tool. Watch how it reasons, executes the tool, reads the output, and returns the final string autonomously.
* **Execute:** `make run-single`

### 2. The Evaluator-Optimizer (`02_reflection_agent.py`)
**Demonstrates Pattern 2.** A rigorous two-node architecture (`Generator` -> `Critic`). Watch the AI write a draft, score its own draft against strict rules natively using a Pydantic schema, and recursively iterate until the draft passes validation.
* **Execute:** `make run-reflection`

### 3. Orchestrator-Workers (`03_multi_agent_orchestrator.py`)
**Demonstrates Pattern 3.** (Hierarchical Multi-Agent). A central Supervisor LLM categorizes the user intent and strictly routes the query to isolated Worker Personas (Finance vs Support).
* **Execute:** `make run-multi`
