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

## Telemetry-Driven Refactoring (`SEP-414` OpenTelemetry & `mcp.*` Conventions)

If an Agent frequently fails to use a skill correctly (e.g., constantly hallucinating a parameter), the fault usually lies in the skill's natural language description (`SKILL.md` or tool schema), not the model.

* **Mandate:** Implement distributed tracing using MCP's native **OpenTelemetry propagation (`SEP-414`)**—passing unprefixed `traceparent`, `tracestate`, and `baggage` (containing `skill.uri` and the manifest's `skill.digest=sha256:...`) inside `params._meta` alongside OpenTelemetry GenAI semantic conventions (`mcp.method.name`, `mcp.resource.uri`, `gen_ai.tool.name`).
* **Actionable Metrics:** Create dashboards tracking the **Tool Validation Error Rate (`isError: true`)** correlated with each `SKILL.md` `sha256` digest. When a skill crosses a failure threshold, engineering must refine the `SKILL.md` instructions or JSON Schema `description` fields and verify improvement against the new manifest digest.
