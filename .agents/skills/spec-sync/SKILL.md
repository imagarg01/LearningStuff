---
name: spec-sync
description: Reconciles State Drift by taking structural code changes (AST diffs) and reverse-engineering the intent to update the Delta Spec.
---

# spec-sync

This skill acts as the "Synchronization Layer" (Stage 4) of Spec-Driven Development (SDD). When a human developer or an AI Agent alters a contract in the codebase (e.g., changes an API signature or database schema) that deviates from the approved Delta Spec, this skill reverse-engineers the code change back into the Spec to prevent State Drift.

## Usage

This skill is typically invoked by a CI pipeline, pre-commit hook, or manually by a developer/agent when they realize the technical implementation must diverge from the approved Spec.

### Parameters (JSON Schema)

```json
{
  "type": "object",
  "properties": {
    "current_delta_spec_path": {
      "type": "string",
      "description": "Path to the current feature's Delta Spec Markdown file."
    },
    "structural_diff_json": {
      "type": "string",
      "description": "A JSON array representing structural semantic changes (e.g., AST tree-sitter output). Raw git diffs are STRICTLY FORBIDDEN."
    }
  },
  "required": ["current_delta_spec_path", "structural_diff_json"]
}
```

## Execution Instructions (For the LLM Agent)

When this tool is invoked, you MUST strictly adhere to the following rules:

1. **The AST Diffing Mandate:** You MUST verify that the `structural_diff_json` contains semantic contract changes (e.g., "Function signature modified", "New Database column added"). If you are passed a raw `git diff` containing implementation details (e.g., `+ let x = 5;`), you MUST reject the request and return an error demanding structural AST diffs.
2. **Reverse-Engineering Intent:** Analyze the structural code changes. Why did the developer or AI agent make this change? Does it invalidate an existing Gherkin scenario in the QA View? Does it require an updated OpenAPI contract in the Dev View?
3. **No Silent Approvals:** You are explicitly forbidden from silently overwriting the Spec. You MUST format the output as a proposed update and flag it for human review.

### The Output Format

You MUST generate the output as a structured Markdown document explicitly demanding human review.

```markdown
> [!WARNING]
> **NEEDS_HUMAN_APPROVAL:** A structural code change has been detected that deviates from the approved Delta Spec. Please review the reverse-engineered intent below to ensure this technical change does not violate business rules.

### Detected State Drift
* **Code Change:** [Describe the structural change detected, e.g., 'Added optional `timeout` parameter to `fetchData` API']
* **Reverse-Engineered Intent:** [Why you believe the developer/agent made this change]

### Proposed Updates to Delta Spec

#### [MODIFY] Dev View (API Contracts)
```diff
-  fetchData(userId: string)
+  fetchData(userId: string, timeout?: number)
```

#### [MODIFY] QA View (Gherkin Scenarios)
[If applicable, propose new Gherkin edge-cases that this code change implies, e.g., "Scenario: Timeout occurs during fetch"]
```

### Action After Generation

Once generated, present this output to the user (Product Owner / QA) for explicit verification. If approved, the pipeline will formally patch the Delta Spec.
