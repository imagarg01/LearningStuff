# AI Agent Skills — Runnable Engineering & Delivery Factory Examples

This directory contains runnable Python implementations covering the four core engineering challenges of Enterprise MCP Agent Skills (`SEP-2640` + `SEP-414` + `SEP-1303`). Zero external API keys or third-party dependencies are required.

## Quick Start

From `docs/AI/Skills/`:

```bash
make all          # Run all 4 examples in sequence
make validate     # Byte-compile and validate all Python scripts
```

## Overview of Scripts

| Script | Make Target | Question Addressed | Key Concepts Demonstrated |
| :--- | :--- | :--- | :--- |
| [`01_token_efficiency_analyzer.py`](./01_token_efficiency_analyzer.py) | `make efficiency` | **1. How to make skills token-efficient & check efficiency?** | • Static Token Budget Linter (`frontmatter <= 60`, `SKILL.md <= 1200`, `inputSchema <= 250`, schema nesting depth $\le 2$)<br/>• Runtime OTel (`SEP-414`) metrics: **Tokens-per-Successful-Actuation ($T_{\text{success}}$)**, **Token Amplification Factor ($\text{TAF}$)**, and **Context-to-Action Ratio ($\text{CAR}$)** |
| [`02_model_dependency_benchmark.py`](./02_model_dependency_benchmark.py) | `make dependency` | **2. How much does a skill depend on model quality?** | • **Cognitive Load Score** calculator (`0–100`)<br/>• Cross-Tier Benchmark (`frontier` vs. `flash` vs. `slm`)<br/>• **Cognitive Offloading**: Refactoring prompt branching, date math, and micro-tool chains into deterministic MCP handlers |
| [`03_model_agnostic_test_harness.py`](./03_model_agnostic_test_harness.py) | `make agnostic` | **3. How to do model-agnostic testing?** | • **Canonical Tool-Call AST Normalizer** (unifying Gemini `function_call`, Claude `tool_use`, OpenAI `tool_calls`, and MCP `tools/call`)<br/>• **Stateful MCP Sandbox** (asserting on final world-state post-conditions rather than brittle tool trajectories)<br/>• **`SEP-1303` Self-Correction Loop** & **$\text{Pass}^k$ ($\text{Pass}^3$)** consistency scoring |
| [`04_skill_delivery_factory.py`](./04_skill_delivery_factory.py) | `make factory` | **4. How to build a testable Skill Delivery Factory pipeline?** | • **Gate 1:** Static Contract, MCP Annotations & Token Budget<br/>• **Gate 2:** Property-Based Fuzzing (`SEP-1303` zero raw exceptions)<br/>• **Gate 3:** Catalog Semantic Routing & Anti-Shadowing Confusion Matrix<br/>• **Gate 4:** Model-Agnostic Behavioral Matrix ($\text{Pass}^3 \ge 0.95$, $\text{TAF} \le 1.25$)<br/>• **Gate 5:** Cryptographic `SEP-2640` SHA-256 Manifest Signing<br/>• **Gate 6:** OTel (`SEP-414`) Canary Auto-Rollback Monitor |
