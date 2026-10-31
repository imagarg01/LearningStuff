# AI Agent Skills: Enterprise Architecture Guide

This documentation defines the architectural standard for AI Agent **Skills** (Tools/Functions), covering their role as the Actuation Layer, strict Non-Functional Requirements (NFRs), enterprise-grade testing, maintainability lifecycles, and distribution mechanisms.

![Skills in Enterprise](./AI_Agent_Skills.png)

## Table of Contents

1. **[Core Concepts (The Actuation Layer)](./01_core_concepts.md)**
   * Anatomy of a Skill, Semantic Routing, and Granularity.
2. **[Execution Architecture, Token Economics & Model Dependency (NFRs)](./02_execution_architecture.md)**
   * Context Compression, Failing Forward (`SEP-1303`), Idempotency, Cryptographic Boundaries (`SEP-2640`), **Token Efficiency & Measurement ($\text{TAF}$, $\text{CAR}$)**, and **Model Quality Dependency & Cognitive Offloading**.
3. **[The Skill Testing Lifecycle & Model-Agnostic Testing](./03_testing_lifecycle.md)**
   * Prompt-Isolation Testing, Property-Based Fuzzing, **Canonical Tool-Call AST Normalization**, **Stateful Sandbox World-State Assertions**, **$\text{Pass}^k$ Reliability**, and **Cross-Model Compatibility Matrices**.
4. **[Maintainability & Governance](./04_maintainability_governance.md)**
   * Schema Synchronization, Tombstoning, and Telemetry-Driven Refactoring (`SEP-414` OpenTelemetry).
5. **[Implementation, Structure, & Discovery](./05_implementation_discovery.md)**
   * Directory structure, Progressive Disclosure, Workspace Roots, and Remote Skills over MCP (`SEP-2640`).
6. **[The Skill Delivery Factory (CI/CD Pipeline)](./06_skill_delivery_factory.md)** *(New)*
   * The 6-Stage automated CI/CD factory: Static Token Budget Linting, Property Fuzzing, Catalog Confusion Matrix, Model-Agnostic Behavioral Matrix, `SEP-2640` Manifest Signing, and `SEP-414` OTel Canary Auto-Rollback.
7. **[Runnable Python Examples & Factory Suite (`src/`)](./src/README.md)** *(New)*
   * Hands-on executable tools for Token Efficiency Analysis, Model Dependency Benchmarking, Model-Agnostic Testing, and the 6-Stage Skill Delivery Factory (`make all`).
8. **[The Unified Puzzle: Agent + Skill + MCP + Eval Pipeline](../Evals/05_unified_agent_mcp_skill_eval_pipeline.md)** *(Cross-Module Guide)*
   * How Agent, Skill (`SEP-2640`), MCP (`2026-07-28`), and Evals (`SEP-414` + Meta-Eval Mutation Testing + Continuous OTel Flywheel) fit together into one end-to-end architecture.
