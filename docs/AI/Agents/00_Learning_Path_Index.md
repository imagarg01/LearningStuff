# AI Agents: The Engineer's Learning Path

Welcome to the **AI Agents Learning Path**, designed specifically for traditional software engineers. This syllabus provides a structured, deep-dive transition from creating deterministic code (workflow execution) to probabilistic, agentic systems (goal-oriented managers).

## Table of Contents

### Core Foundations

[Mental Models and Core Concepts](01_Mental_Model_and_Concepts.md)

* The shift from Deterministic to Probabilistic.
* "Reasoning vs. Execution" in modern computing.
* State, Memory handling, and the ReAct architecture.

### System Design

[Problem Selection and Architecture](02_Problem_Selection_and_Architecture.md)

* Tool Calling APIs (JSON Schemas, Action Spaces).
* Designing state-machine agent orchestrators.
* Framework comparison (LangGraph, CrewAI, Autogen).
* Knowing when a workflow is better than an agent.

### Quality and Reliability

[Evaluation and Observability](03_Evaluation_and_Observability.md)

* Moving beyond `assertEquals`. Evals and Golden Datasets.
* LLM-as-a-judge mechanics.
* Full end-to-end Observability (LangSmith, LangFuse, Arize Phoenix).

### Operations

[Maintenance and Productionization](04_Maintenance_and_Productionization.md)

* Handling Model Drift and deprecations.
* Cost, rate-limits, and infinite loop prevention.
* Human-in-the-loop (HITL) and feedback mechanisms.

### Practical Engineering

[Practical Implementation](05_Practical_Implementation.md)

* Hands-on architectures.
* Multi-agent collaboration vs. Single-agent with massive toolsets.
* Pseudo-code templates and workflow patterns.

### The Frontier & Modern Engineering

[Advanced Concepts: DeepAgent and Beyond](06_Advanced_Concepts.md)

* Hierarchical Agent Orchestration.
* DeepAgent paradigms & Episodic Memory.
* Reinforcement Learning from Human Feedback (RLHF / DPO) loop integration.

[Modern Agentic Engineering: Loops, Graphs, and Discovery](07_Modern_Agentic_Engineering.md)

* Graph Engineering vs. Prompt Monoliths.
* Bounded Loop Engineering & Semantic Diffing.
* Progressive Discovery of Skills & MCP Servers (`SEP-2640`).

### Capstone: The Unified Production Architecture

[Production-Grade Agent Architecture: Taming Unbounded Input & The Generative Machine](08_Production_Grade_Agent_Architecture.md) *(New)*

* **The Two First-Principle Axioms:** *Unbounded Input* + *The Generative Machine*.
* **The Probabilistic-to-Deterministic Funnel:** Unifying **Agent + Skill (`SEP-2640`) + MCP (`2026-07-28`) + Eval (`SEP-414`)**.
* **The 5 Production Pillars:** Epistemic Humility ("Stop-and-Ask"), 3-Tier Progressive Skill Discovery & Cognitive Offloading, the Neuro-Symbolic Sandwich (Zero-Trust Argument Provenance), Runtime Blast-Radius Physics ($\text{TAF}$, `MRTR`), and the Closed-Loop OTel-to-Eval Flywheel.

[Deep-Dive: Decision Physics, Durable State, Cross-Run Memory, and Persona Architecture](09_Durable_State_Memory_and_Persona_Architecture.md) *(New — $n^{\text{th}}$-Level Deep Dive)*

* **The Mathematics of Multi-Decision Collapse ($p^N$):** Breaking the compounding error law with Step-Level Verifiers $\left(1-(1-p)^R\right)^N$ and isolating model-swap drift via **Markov Decision Cassettes**.
* **Durable Execution & Compensating Sagas:** Event-sourced checkpoint trees (`parent_checkpoint_id`), zero-recomputation `MRTR` resume, time-travel branch forking, and LIFO Saga compensation unwinding.
* **CoALA & Bi-Temporal Cross-Run Memory:** Working RAM vs. Episodic Run Receipts (`do_not_repeat`) vs. Bi-Temporal Knowledge Graphs (`valid_from` / `valid_until`).
* **Dual-Plane Caller Persona Resolution:** IETF `RFC 8693` On-Behalf-Of Cryptographic Authority (`sub` + `act`) + Cognitive Persona Contracts, plus 10 authoritative academic & RFC references.

[Deep-Dive: The Companion Primitives — BAML, KV-Cache Physics, Protocol Triad (MCP/A2A/A2UI), XPIA Defense, & DSPy](10_Companion_Primitives_BAML_KV_A2A_A2UI_Safety_DSPy.md) *(New — Complete 8-Primitive Stack)*

* **Constrained Decoding & Schema-Aligned Parsing (`BAML`):** FSM logit masking math, avoiding Format-First reasoning degradation, and zero-token fuzzy AST repair.
* **Transformer KV-Cache Physics & The 4-Zone Context Compiler:** Why prefix mutations bust GPU KV caches and how to achieve $>90\%$ cache hit rates across multi-turn loops.
* **The Protocol Triad (`MCP` vs. `A2A` vs. `A2UI` / `ui://`):** Vertical white-box tool actuation vs. horizontal opaque peer delegation vs. declarative human UI streaming.
* **Indirect Prompt Injection (XPIA) Defense & `DSPy` Compilation:** Cryptographic Spotlighting, the **CaMeL Dual-LLM Quarantined Reader**, Information-Flow Taint Tracking, and automatic prompt optimization against $\text{Pass}^3$.

---

## Connected Enterprise Stack Modules (The Complete 8-Primitive Ecosystem)

| Primitive | Focus Area | Entry Point |
| :--- | :--- | :--- |
| **1. Agent Graph & Durable State** | Bounded DAGs, Checkpointing, Time-Travel, Sagas, CoALA Memory, Dual-Plane Personas | [Module 08](08_Production_Grade_Agent_Architecture.md) & [Module 09](09_Durable_State_Memory_and_Persona_Architecture.md) |
| **2. Agent Skills (`SEP-2640`)** | Actuation Playbooks (`SKILL.md`), Token Efficiency ($\text{TAF}/\text{CAR}$), Model Dependency, 6-Stage Delivery Factory | [AI Agent Skills Guide](../Skills/skill.md) |
| **3. Model Context Protocol (`MCP`)** | `2026-07-28` Stateless HTTP, `SEP-2640` Skills Over MCP, `SEP-1303` Error Hints, `SEP-414` OTel, OAuth 2.1 & `MRTR` | [MCP Overview](../MCP/00_overview.md) |
| **4. AI Evals (`SEP-414` Flywheel)** | 4-Layer Contract Evals, Meta-Eval Mutation Testing, Rogan-Gladen Judge Calibration, Continuous OTel Flywheel | [AI Evals Overview](../Evals/00_overview.md) |
| **5. Constrained Decoding (`BAML` / `Pydantic`)** | Schema-Aligned Parsing (SAP), Think-Then-Parse, Fuzzy AST Repair, Type-Safe Decision Boundaries | [What Is BAML](../BAML/WhatIsBAML.md) & [Pydantic in AI](../Pydantic/PydanticInAI.md) |
| **6. Context & KV-Cache Engineering** | 4-Zone Prefix-Stable Context Compiler, Paged/Radix KV-Cache Physics, Bi-Temporal Context Graphs | [Context Engineering](../ContextEngineering.md) & [Context Graph](../Context_Graph/ContextGraph.md) |
| **7. Horizontal & UI Protocols (`A2A` & `A2UI`)** | Peer Agent Cards & Task Delegation (`A2A`), Declarative Native UI Streaming (`A2UI` & `MCP Apps ui://`) | [A2A Overview](../A2A/00_overview.md), [A2UI Overview](../A2UI/00_overview.md), & [MCP Apps](../MCP/06_mcp_app.md) |
| **8. XPIA Security Guardrails & `DSPy`** | Spotlighting, CaMeL Dual-LLM Privilege Separation, Taint Tracking, Programmatic Prompt Compilation | [AI Guardrails](../Safety/AI_Guardrails.md) & [DSPy Guide](../Advanced/DSPy_Intro.md) |

---
*Follow the numeric sequence above to build a robust, production-grade understanding of autonomous LLM architectures.*
