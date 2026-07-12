---
name: refine-intent
description: Analyzes a raw feature request (e.g., a Jira ticket) against the repository guidelines (agents.md) to produce a clarified, purely business-focused Intent document. Flags ambiguities and technical contradictions.
---

# refine-intent

This skill acts as the "Ingestion Layer" for Spec-Driven Development (SDD). It transforms untrusted, ambiguous human requests into a structured `Refined_Intent` object that can be safely used to generate a Multi-View Spec.

## Usage

Use this skill when the user asks you to analyze a new Jira ticket, feature request, or raw idea. Do not begin writing code or generating functional specs until this skill has run and the output has been validated by the user.

### Parameters (JSON Schema)

```json
{
  "type": "object",
  "properties": {
    "raw_request_text": {
      "type": "string",
      "description": "The raw text of the feature request or Jira ticket (Summary, Description, Acceptance Criteria)."
    },
    "repo_spec_path": {
      "type": "string",
      "description": "Optional. The path to the global repository guidelines (e.g., 'AGENTS.md'). Defaults to 'AGENTS.md' in the workspace root."
    }
  },
  "required": ["raw_request_text"]
}
```

## Execution Instructions (For the LLM Agent)

When this tool is invoked, you must perform the following steps:

1. **Locate Grounding Rules:** Read the `AGENTS.md` (or the provided `repo_spec_path`) in the repository root to understand the architectural constraints, coding guidelines, and domain rules.
2. **Analyze for Contradictions:** Compare the `raw_request_text` against the grounding rules. Flag any requests that mandate a technical solution violating the established architecture.
3. **Analyze for Ambiguities:** Identify any edge cases or missing context in the business logic (e.g., unhandled error states, missing user personas).
4. **Distill Pure Intent:** Strip away any prescriptive technical solutions from the request. Extract *only* what the business is trying to achieve.

### Output Validation (The Refined Intent Payload)

You must return your analysis as a structured JSON object exactly matching this schema. This ensures downstream agents can parse it deterministically.

```json
{
  "status": "success | needs_human_feedback | error",
  "message": "Human-readable summary of the result.",
  "refined_business_intent": {
    "core_goal": "String explaining the 'why' and 'what'.",
    "business_rules": ["List of extracted constraints."],
    "out_of_scope": ["List of things explicitly excluded."]
  },
  "flagged_contradictions": [
    "Example: The request asks for a new DB table, but AGENTS.md mandates reusing the existing generic store."
  ],
  "unresolved_ambiguities": [
    "Example: Question for PO: How should we handle the timeout scenario?"
  ]
}
```

### Semantic Error Handling & Guardrails

- **Missing Grounding:** If `AGENTS.md` cannot be found, do NOT fail silently or hallucinate rules. Return `{"status": "error", "message": "Could not find AGENTS.md to ground the request. Please provide the correct path."}`
- **The Stop-Gate:** If there are ANY `unresolved_ambiguities` or `flagged_contradictions`, you MUST set the status to `needs_human_feedback`. The pipeline must halt here. Output the specific questions back to the human (Product Owner) and wait for their response before proceeding to Spec Generation.
