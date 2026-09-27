# AI Agent Skills: Enterprise Architecture Guide

This documentation defines the architectural standard for AI Agent **Skills** (Tools/Functions), covering their role as the Actuation Layer, strict Non-Functional Requirements (NFRs), enterprise-grade testing, maintainability lifecycles, and distribution mechanisms.

![Skills in Enterprise](./AI_Agent_Skills.png)

## Table of Contents

1. **[Core Concepts (The Actuation Layer)](./01_core_concepts.md)**
   * Anatomy of a Skill, Semantic Routing, and Granularity.
2. **[Execution Architecture (NFRs)](./02_execution_architecture.md)**
   * Context Compression, Failing Forward, Idempotency, and Cryptographic Boundaries.
3. **[The Skill Testing Lifecycle](./03_testing_lifecycle.md)**
   * Prompt-Isolation Testing, Fuzzing, and CI pipelines.
4. **[Maintainability & Governance](./04_maintainability_governance.md)**
   * Schema Synchronization, Tombstoning, and Telemetry-Driven Refactoring.
5. **[Implementation, Structure, & Discovery](./05_implementation_discovery.md)** *(New)*
   * Directory structure, Progressive Disclosure, Workspace Roots, and Plugins for enterprise sharing.
