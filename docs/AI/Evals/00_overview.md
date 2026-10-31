# AI Evals: The Foundation of Reliable Agents

## What is Eval?

In the context of Large Language Models (LLMs) and AI Agents, an **Eval (Evaluation)** is a test case used to measure the performance, reliability, and safety of your system. Unlike traditional unit tests which typically assert binary outcomes (pass/fail based on exact logic), AI Evals often deal with probabilistic outputs and semantic correctness.

An eval consists of:

1. **Input**: The prompt or context provided to the agent.
2. **Expected Output (Ground Truth)**: What the ideal response should be (optional, depending on the metric).
3. **Metric**: A method to score the actual output against the expected output or defined criteria.

## Why We Need Evals

Building an AI demo is often easy; creating a production-ready agent is incredibly hard. Evals are the bridge between the two.

### 1. Regression Testing

LLMs are non-deterministic and can be sensitive to minor prompt changes. Fixing one bug might break another use case. Evals provide a safety net to ensure that improvements in one area don't degrade performance in others.

### 2. Model Selection & Optimization

When switching from GPT-4 to Claude 3.5 Sonnet, or quantizing a local model, how do you know if it's "good enough"? Evals quantify the trade-offs between cost, latency, and quality.

### 3. Safety and Alignment

Evals are crucial for detecting hallucinations, toxicity, or prompt injection vulnerabilities before they reach users.

### 4. Improving Performance

You cannot improve what you cannot measure. Evals provide a hill-climbing metric to optimize prompts, RAG retrieval strategies, and agent workflows.

## The Core Loop

The development lifecycle of an AI product should revolve around evals:

1. **Prototype**: Build a basic prompt/agent, skill (`SKILL.md`), and MCP tool.
2. **Verify the Eval (Meta-Eval)**: Run fault-injection mutation testing and judge calibration so you can trust your metrics.
3. **Gate CI/CD**: Run the 4-layer Eval Matrix across Routing, Canonical Tool AST, MCP Fuzzing, and Stateful World-State post-conditions.
4. **Capture Live Telemetry**: Stream production OpenTelemetry (`SEP-414`) spans correlated to `skill.digest` (`SEP-2640`).
5. **Auto-Compile Fixtures**: Turn production retry loops (`SEP-1303`) and human rejections (`MRTR`) into deterministic regression fixtures.

## Table of Contents

1. **[Types of Evals (The Evaluation Pyramid)](./01_types_of_evals.md)**
   * Unit, Integration, End-to-End, and Offline vs. Online Evals.
2. **[Building and Running Evals](./02_building_evals.md)**
   * Golden/Synthetic/Log Datasets, Deterministic vs. LLM-Judge Metrics, and Tooling.
3. **[Measuring Eval Quality (Meta-Evaluation) & Continuous Maintenance](./03_maintaining_evals.md)** *(Updated)*
   * **Mutation Testing for Evals** (Defect Injection Score), **Judge Calibration** ($\text{TPR}$, $\text{TNR}$, Cohen's $\kappa$, & **Rogan-Gladen Bias Correction**), **Eval Noise Floor**, **Saturation Pruning**, and the **Closed-Loop OTel (`SEP-414`) $\rightarrow$ Eval Fixture Flywheel**.
4. **[Measuring Semantic & Intent Coverage](./04_measuring_coverage.md)**
   * Intent Taxonomy Coverage, Embedding Drift, and Red-Teaming.
5. **[The Unified Puzzle: Agent + Skill + MCP + Eval Pipeline](./05_unified_agent_mcp_skill_eval_pipeline.md)** *(New)*
   * How **Agent**, **Skill (`SEP-2640`)**, **MCP (`2026-07-28`)**, and **Eval (`SEP-414`)** interlock as a single 4-layer control system with unified lineage keys and automated self-healing.

## See Also & Runnable Code (`src/`)

- **Agent Skills Architecture & Delivery Factory**: [AI Agent Skills Guide](../Skills/skill.md) & [The Skill Delivery Factory](../Skills/06_skill_delivery_factory.md)
- **Model Context Protocol (MCP)**: [MCP Overview](../MCP/00_overview.md)
- **RAG + Evals**: [RAG Evaluation Strategies & Tools](../RAG_Strategies/RAGEvaluation.md)
- **Runnable Examples (`make all` in `docs/AI/Evals/`)**:
  - [`src/simple_eval.py`](./src/simple_eval.py) — Basic deterministic JSON tool-call eval
  - [`src/llm_judge_eval.py`](./src/llm_judge_eval.py) — Basic LLM-as-a-Judge eval
  - [`src/03_meta_eval_quality_checker.py`](./src/03_meta_eval_quality_checker.py) — Measuring Eval Quality (Mutation Kill Rate, Judge Calibration $\text{TPR}/\text{TNR}/\kappa$, & Rogan-Gladen Bias Correction)
  - [`src/04_continuous_eval_flywheel.py`](./src/04_continuous_eval_flywheel.py) — Continuous Eval Updating (`SEP-414` OTel Anomaly Mining $\rightarrow$ PII Scrubbing $\rightarrow$ Golden Fixture Compilation & Saturation Pruning)
  - [`src/05_unified_agent_mcp_skill_eval_pipeline.py`](./src/05_unified_agent_mcp_skill_eval_pipeline.py) — Complete End-to-End `Agent + Skill + MCP + Eval` closed-loop pipeline
