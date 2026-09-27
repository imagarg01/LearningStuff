# 07. Modern Agentic Engineering: Loops, Graphs, and Discovery

As AI Systems evolve from single-turn chat interfaces into autonomous enterprise pipelines, the engineering paradigms required to build them have fundamentally shifted. **Prompt Engineering** is no longer the primary skill; it has been superseded by **Graph Engineering**, **Loop Engineering**, and **Progressive Discovery**.

This document outlines these architectural shifts, exactly when to use them, and how to govern them in production.

---

## 1. Graph Engineering (The End of CoT Monoliths)

Historically, complex tasks were solved by giving an LLM a massive prompt instructing it to "Think step-by-step" (Chain of Thought - CoT) and hoping it reached the end without losing context.

**Graph Engineering** abandons this in favor of explicit state machines (Directed Acyclic Graphs - DAGs), utilizing frameworks like **LangGraph** or **StateGraph**.

### The Core Paradigm
Instead of one prompt doing 10 things, Graph Engineering breaks the process down into discrete **Nodes** (specialized agents or tools) connected by **Conditional Edges** (routing logic). State is passed explicitly via a typed payload (e.g., `TypedDict`), eliminating context drift.

### When to Use
* **Multi-Persona Workflows:** E.g., A Spec-Driven Development (SDD) pipeline requiring a BA Agent, QA Agent, and Dev Agent.
* **Deterministic Routing:** When you must enforce strict compliance gates (e.g., "Do not proceed to execution until the `spec_approved` boolean is True").
* **Complex Data Transformations:** When the output of one LLM step must be programmatically verified before being passed to the next.

### When NOT to Use
* **Simple Q&A:** If the user just wants a summary of a document, a single LangChain/LlamaIndex call is sufficient. Spinning up a graph adds unnecessary latency and boilerplate.
* **Creative Writing:** Unstructured workflows do not benefit from rigid graphs.

### Observability & Failure Recovery
* **Observability:** Graphs allow you to inspect the exact `State` payload at any node. If the process fails at Node C, you don't have to guess what the LLM was thinking—you can dump the State payload exactly as it left Node B.
* **Failure Recovery:**
  * **Checkpoints:** Frameworks like LangGraph support thread-level checkpoints. If an API times out at Node C, you can resume the graph directly from Node C's checkpoint rather than starting over.
  * **Time-Travel:** If an agent hallucinated in a previous step, a human can literally rewind the graph to a previous state, manually edit the state payload, and resume.

---

## 2. Loop Engineering (Bounded Autonomous Execution)

**Loop Engineering** is the practice of designing iterative execution cycles where an agent acts, observes the result, and self-corrects until a condition is met.

### The Core Paradigm
Instead of asking an LLM to "write perfect code," you ask an LLM to "write code, compile it, read the errors, and fix them." 

### When to Use
* **TDD / Execution Swarms:** Red/Green/Refactor loops where the agent writes tests, writes implementation, and loops until the tests pass.
* **Self-Correction:** When parsing unstructured data into strict JSON, if the parser fails, the error is fed back to the LLM to try again.

### When NOT to Use
* **Open-Ended Research:** If the agent doesn't have a deterministic way to verify "success" (like a compiler passing), loops will often spiral out of control, endlessly searching the web without concluding.
* **High-Risk Mutations:** Do not put `DROP TABLE` or infrastructure provisioning commands inside an autonomous retry loop.

### Observability & Failure Recovery
* **The Infinite Loop Problem:** The biggest risk in Loop Engineering is an LLM receiving the same error, hallucinating the same fix, and looping forever until your API budget is drained.
* **Failure Recovery (Bounded Loops):** 
  * **Strict Counters:** EVERY loop must have a hard iteration cap (e.g., `if retries > 5: return human_escalation`).
  * **Semantic Diffing:** The execution engine must monitor the agent's proposed actions. If the agent proposes the exact same code fix twice in a row, the engine must forcefully terminate the loop and escalate, as the LLM is stuck in a local minimum.
* **Failing Forward:** Tools must return semantic hints (e.g., "Error: Cannot find module 'react'. Did you run npm install?") rather than raw stack traces.

---

## 3. Progressive Discovery of Skills & MCPs

Enterprise environments possess massive surfaces (thousands of APIs, databases, and microservices). A naive approach is to inject all 1,000 JSON Schemas or MCP connections into the Agent's system prompt.

### The Core Paradigm
**Progressive Discovery** treats tools and context as "just-in-time" dependencies. 

1. **The Registry:** All enterprise skills (API wrappers) and MCPs (secure data/tool servers) are registered in a central Vector Database or Semantic Registry.
2. **The Discovery Agent:** An agent starts with a very lean system prompt and only a few core tools (e.g., `search_registry`, `ask_human`).
3. **Dynamic Injection (RAG for Tools):** If the user asks the agent to "check Snowflake billing," the agent first queries the registry. The host application retrieves the JSON Schema for the Snowflake Skill or mounts the Snowflake MCP server.
4. **Context Collapse:** Once the task is completed, the agent unloads the Snowflake tool, freeing up its context window for the next task.

### Why it is Critical
* **Context Preservation:** Keeps the LLM focused on the current sub-task, vastly reducing hallucinations.
* **Security & Blast Radius:** The agent only has access to Snowflake *when it explicitly needs to access Snowflake*. If hijacked via prompt injection at a different stage, the agent lacks the tools to do damage.
* **Scalability:** It is the only way a single Agentic System can scale to an enterprise with hundreds of disparate data silos.
