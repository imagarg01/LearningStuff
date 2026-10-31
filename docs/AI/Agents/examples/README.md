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

### 4. The Production-Ready Agent Funnel (`04_production_ready_agent_funnel.py`) *(Zero API Keys Required)*
**Demonstrates Module 08 Capstone.** Connects **Agent + Skill (`SEP-2640`) + MCP (`2026-07-28`) + OTel/Eval (`SEP-414`)** inside the 5-Layer **Probabilistic-to-Deterministic Funnel** to tame *Unbounded Input* and *The Generative Machine*:
1. **Layer 1 (Epistemic Humility):** "Stop-and-Ask" missing-slot gate refuses to guess missing order IDs.
2. **Layer 2 (`SEP-2640` Skill Discovery):** Loads `SKILL.md` and verifies its SHA-256 manifest digest.
3. **Layer 3 (Neuro-Symbolic Provenance Guard):** Blocks hallucinated `order_id` arguments before they reach the MCP server.
4. **Layer 4 (Deterministic MCP Wall):** Demonstrates `SEP-1303` 1-turn self-correction, `MRTR` (`input_required`) human approval for high-value mutations, and the Semantic Loop Diffing Circuit Breaker.
5. **Layer 5 (`SEP-414` OTel Flywheel):** Captures blocked hallucinations and loop anomalies for the Continuous Eval Flywheel.
* **Execute:** `make run-prod-funnel` (or `python3 04_production_ready_agent_funnel.py`)

### 5. Stateful Decision Recovery, Cross-Run Memory & Persona Resolution (`05_stateful_decision_recovery_and_persona.py`) *(Zero API Keys Required)*
**Demonstrates Module 08 (§3).** Solves the four hardest multi-step agent engineering challenges:
1. **Decision-Node Cassette Pinning:** Tests each decision node (`D1`, `D2`, `D3`) against frozen input snapshots so a model-upgrade regression at `D2` is caught in isolation before poisoning `D3`.
2. **Checkpoint Time-Travel & Branch Forking:** Rewinds a bad decision at `cp_02_bad` back to `cp_01` (preserving `D1`'s work) and forks onto a patched `cp_02_fork` branch.
3. **Cross-Run 3-Tier Memory Consolidation:** Compiles Run #1's working state into a compact `<150-token` `EpisodicRunReceipt` + Semantic Entity fact and injects it cleanly into Run #2.
4. **Dual-Plane Caller Persona Resolution:** Separates Plane 1 (OAuth 2.1 cryptographic skill & `MRTR` authority) from Plane 2 (cognitive output adaptation across `End_Customer`, `SRE_OnCall`, and `Headless_CI_Bot`).
* **Execute:** `make run-stateful-persona` (or `python3 05_stateful_decision_recovery_and_persona.py`)

### 6. Companion Primitives Suite: BAML, KV-Cache Physics, XPIA CaMeL Defense, Triad & DSPy (`06_companion_primitives_suite.py`) *(Zero API Keys Required)*
**Demonstrates Module 10.** Implements the four companion primitives that complete the 8-primitive stack:
1. **Primitive 5 (`BAML` Schema-Aligned Parser):** Compares JSON Schema Draft 2020-12 token overhead against BAML compact types (60%+ savings) and repairs messy Think-Then-Parse LLM outputs in `<1ms` with zero retry tokens.
2. **Primitive 6 (4-Zone Prefix-Stable KV-Cache Compiler):** Proves how moving volatile timestamps/UUIDs from Zone 1 (top of prompt) to Zone 4 (tail) lifts multi-turn KV-cache hit rates from `0.6%` to `91%+`.
3. **Primitive 8A (3-Layer XPIA Indirect Prompt Injection Defense):** Uses Cryptographic Spotlighting, the **CaMeL Quarantined Reader LLM (`tools=[]`)**, and Taint-Tracked Provenance to neutralize a poisoned Jira ticket payload.
4. **Primitive 7 & 8B (Protocol Triad `A2A -> MCP -> A2UI` + `DSPy` Compilation):** Connects horizontal `A2A` task intake, vertical `MCP` tool execution, declarative `A2UI` `MRTR` approval cards, and a `DSPy` optimizer maximizing $\text{Pass}^3 / \text{TAF}$.
* **Execute:** `make run-companion-primitives` (or `python3 06_companion_primitives_suite.py`)
