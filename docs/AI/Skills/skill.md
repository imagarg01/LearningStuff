# AI Agent Skills: Enterprise Architecture Guide

This document defines the architectural standard for AI Agent **Skills** (Tools/Functions), covering their role as the Actuation Layer, strict Non-Functional Requirements (NFRs), and enterprise-grade testing and maintainability lifecycles.

![Skills in Enterprise](./AI_Agent_Skills.png)

---

## Part I: Core Concepts (The Actuation Layer)

An **Agent Skill** is not just a script; it is the **Actuation Layer** of a Compound AI System. While LLMs excel at reasoning, they cannot natively execute code, verify real-time state, or guarantee deterministic calculations. A skill bridges this gap by wrapping deterministic code in a natural language interface.

### 1. Anatomy of a Skill
Every enterprise skill possesses a dual boundary:
1. **The Cognitive Interface (LLM-Facing):** The JSON Schema and natural language description (the `SKILL.md` prompt) that teaches the model *when* and *how* to invoke it.
2. **The Execution Runtime (System-Facing):** The deterministic code (Python, Bash, API calls) executed by the host runtime, fully isolated from the LLM.

### 2. Semantic Routing vs. Static Tool Calling
Skills drive multi-agent orchestration.
* **Static Tool Calling:** An agent is hardcoded with a fixed array of tool schemas. Best for narrow, highly specialized agents.
* **Semantic Routing (RAG for Tools):** In enterprise environments with hundreds of skills, loading all schemas overflows the context window. Instead, agents use a router skill to query a Vector Database of enterprise skills, dynamically injecting only the 3-5 necessary JSON schemas into their context window at runtime.

### 3. Skill Granularity
* **Micro-Skills (Flexible but Fragile):** Granular, single-purpose functions (e.g., `get_user`, `get_orders`). Requires the LLM to execute complex, multi-step reasoning loops. Increases latency, token costs, and the risk of hallucination mid-loop.
* **Macro-Skills (Rigid but Robust):** Compound functions (`get_full_user_dashboard`). Offloads orchestration to deterministic code. **Recommendation:** Default to Macro-Skills for known enterprise workflows to minimize LLM token usage and execution latency.

### 4. When NOT to use a Skill
* **A simple script is sufficient:** Do NOT wrap deterministic, single-purpose logic (like executing a `curl` command or regex) into an Agent Skill if a human or LLM can just run the raw bash script natively. Skills are architectural overhead; reserve them for context-aware orchestration.
* **LLM reasoning is sufficient:** Summarization, classification, or creative generation do not require skills.

---

## Part II: Execution Architecture (NFRs)

Skills that survive in production must strictly adhere to these architectural mandates.

### 5. Context Compression
**Rule:** A skill MUST NEVER return raw, unpaginated JSON dumps or raw HTML to the agent.
* **Why:** Returning a 50MB database payload will immediately blow out the LLM's context window.
* **Implementation:** The execution runtime must implement **Context Compression**. The script must parse, filter, and extract *only the semantic delta* needed by the agent before returning the payload.

### 6. Failing Forward (Semantic Error Hints)
**Rule:** A skill MUST NEVER return raw system stack traces (e.g., `NullPointerException at line 42`) to the LLM.
* **Why:** LLMs cannot debug your backend code. Raw errors cause them to loop infinitely or hallucinate fixes.
* **Implementation:** Skills must catch their own exceptions and return **Semantic Error Hints**. (e.g., `{"status": "error", "message": "Invalid date format. Expected YYYY-MM-DD. Please try again."}`). This teaches the LLM *how* to self-correct on the next turn.

### 7. Idempotency & The "Dry-Run" Pattern
**Rule:** Any skill that mutates state (Write, Update, Delete) MUST be strictly idempotent.
* **Why:** LLMs are non-deterministic and may accidentally invoke the same payload twice due to network retries or reasoning loops.
* **Implementation:** High-risk skills must support a `dry_run: boolean` parameter. This allows the Agent to simulate the mutation, observe the potential blast radius in the response, and verify intent *before* committing the actual state change.

### 8. Cryptographic Boundaries & HITL
**Rule:** Skills must operate on the Principle of Least Privilege.
* **Why:** Prompt injection allows external actors to hijack the LLM's tool-calling engine.
* **Implementation:** 
  * **Scoped Tokens:** Do not give the Agent global admin credentials. The Execution Runtime must inject scoped OAuth tokens just-in-time during the tool call.
  * **Human-in-the-Loop (HITL):** High-risk skills (e.g., `drop_table`, `deploy_prod`) must pause execution, page a human administrator via UI/Slack with the LLM's proposed parameters, and require cryptographic approval before the runtime executes the code.

---

## Part III: The Skill Testing Lifecycle

Testing AI skills requires bifurcating the deterministic code from the non-deterministic LLM.

### 9. Prompt-Isolation Testing
You must test the skill's *Description* (the prompt) independently of the execution code. 
Create an evaluation dataset of mock intents. Feed only the tool's JSON Schema to the LLM and assert that it accurately selects the tool and formats the parameters without actually running the backend code.

### 10. Property-Based Fuzzing
Because LLMs generate unpredictable outputs, standard mock testing is insufficient for the execution logic. Use property-based testing (e.g., the `Hypothesis` library in Python) to fuzz the deterministic script with massive ranges of edge-case inputs to ensure it gracefully returns semantic errors instead of crashing.

### 11. Fast CI vs. Nightly Evals
* **Fast CI Pipeline (Pull Requests):** Runs static analysis, schema linting, and property-based execution tests. Must complete in < 2 minutes.
* **Nightly Eval Suite:** Runs "End-to-End" (E2E) golden scenarios where the actual Agent is spun up to solve a problem using the skill. Uses "LLM-as-a-Judge" (e.g., GPT-4 or Gemini Pro) to evaluate the trace. Because LLMs are slow and expensive, this runs nightly, not on PRs.

---

## Part IV: Maintainability & Governance

Skills suffer from severe rot over time. Enterprise operations require strict governance.

### 12. Schema Synchronization (Preventing Skill Rot)
When backend APIs change (e.g., a required parameter is added), the LLM's JSON Schema for the skill immediately becomes outdated. The LLM will confidently pass invalid arguments, causing infinite error loops.
* **Mandate:** Agent Skill Schemas MUST be auto-generated or synchronized directly from the source of truth (e.g., OpenAPI specs, GraphQL schemas) via CI/CD pipelines. Never hand-maintain tool schemas if an API contract exists.

### 13. Tombstoning (Graceful Deprecation)
You cannot simply delete an Agent Skill from the registry. Long-running asynchronous agents, or cached system prompts, may still attempt to invoke it, leading to fatal runtime crashes.
* **Mandate:** To deprecate a skill, you must **Tombstone** it. Strip the backend execution logic, but leave the JSON Schema intact. Replace the runtime script with a semantic redirect:
  `{"status": "error", "message": "This tool is deprecated. Please use 'v2_search_tool' instead."}`
  This allows active agents to gracefully recover and adapt.

### 14. Telemetry-Driven Refactoring
If an Agent frequently fails to use a skill correctly (e.g., constantly hallucinating a parameter), the fault usually lies in the skill's natural language description, not the model.
* **Mandate:** Implement hierarchical tracing (e.g., LangSmith, Phoenix). Create dashboards tracking the "LLM Parsing Failure Rate" per skill. When a skill crosses a failure threshold, engineering must rewrite the `description` fields in the JSON schema to clarify constraints for the LLM.
