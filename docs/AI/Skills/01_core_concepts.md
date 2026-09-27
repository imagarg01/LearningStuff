# Core Concepts (The Actuation Layer)

An **Agent Skill** is not just a script; it is the **Actuation Layer** of a Compound AI System. While LLMs excel at reasoning, they cannot natively execute code, verify real-time state, or guarantee deterministic calculations. A skill bridges this gap by wrapping deterministic code in a natural language interface.

## Anatomy of a Skill

Every enterprise skill possesses a dual boundary:

1. **The Cognitive Interface (LLM-Facing):** The JSON Schema and natural language description (the `SKILL.md` prompt) that teaches the model *when* and *how* to invoke it.
2. **The Execution Runtime (System-Facing):** The deterministic code (Python, Bash, API calls) executed by the host runtime, fully isolated from the LLM.

## Semantic Routing vs. Static Tool Calling

Skills drive multi-agent orchestration.

* **Static Tool Calling:** An agent is hardcoded with a fixed array of tool schemas. Best for narrow, highly specialized agents.
* **Semantic Routing (RAG for Tools):** In enterprise environments with hundreds of skills, loading all schemas overflows the context window. Instead, agents use a router skill to query a Vector Database of enterprise skills, dynamically injecting only the 3-5 necessary JSON schemas into their context window at runtime.

## Skill Granularity

* **Micro-Skills (Flexible but Fragile):** Granular, single-purpose functions (e.g., `get_user`, `get_orders`). Requires the LLM to execute complex, multi-step reasoning loops. Increases latency, token costs, and the risk of hallucination mid-loop.
* **Macro-Skills (Rigid but Robust):** Compound functions (`get_full_user_dashboard`). Offloads orchestration to deterministic code. **Recommendation:** Default to Macro-Skills for known enterprise workflows to minimize LLM token usage and execution latency.

## When NOT to use a Skill

* **A simple script is sufficient:** Do NOT wrap deterministic, single-purpose logic (like executing a `curl` command or regex) into an Agent Skill if a human or LLM can just run the raw bash script natively. Skills are architectural overhead; reserve them for context-aware orchestration.
* **LLM reasoning is sufficient:** Summarization, classification, or creative generation do not require skills.
