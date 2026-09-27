# Maintainability & Governance

Skills suffer from severe rot over time. Enterprise operations require strict governance.

## Schema Synchronization (Preventing Skill Rot)

When backend APIs change (e.g., a required parameter is added), the LLM's JSON Schema for the skill immediately becomes outdated. The LLM will confidently pass invalid arguments, causing infinite error loops.

* **Mandate:** Agent Skill Schemas MUST be auto-generated or synchronized directly from the source of truth (e.g., OpenAPI specs, GraphQL schemas) via CI/CD pipelines. Never hand-maintain tool schemas if an API contract exists.

## Tombstoning (Graceful Deprecation)

You cannot simply delete an Agent Skill from the registry. Long-running asynchronous agents, or cached system prompts, may still attempt to invoke it, leading to fatal runtime crashes.

* **Mandate:** To deprecate a skill, you must **Tombstone** it. Strip the backend execution logic, but leave the JSON Schema intact. Replace the runtime script with a semantic redirect:
  `{"status": "error", "message": "This tool is deprecated. Please use 'v2_search_tool' instead."}`
  This allows active agents to gracefully recover and adapt.

## Telemetry-Driven Refactoring

If an Agent frequently fails to use a skill correctly (e.g., constantly hallucinating a parameter), the fault usually lies in the skill's natural language description, not the model.

* **Mandate:** Implement hierarchical tracing (e.g., LangSmith, Phoenix). Create dashboards tracking the "LLM Parsing Failure Rate" per skill. When a skill crosses a failure threshold, engineering must rewrite the `description` fields in the JSON schema to clarify constraints for the LLM.
