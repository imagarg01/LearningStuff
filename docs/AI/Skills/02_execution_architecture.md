# Execution Architecture (NFRs)

Skills that survive in production must strictly adhere to these architectural mandates.

## Context Compression

**Rule:** A skill MUST NEVER return raw, unpaginated JSON dumps or raw HTML to the agent.

* **Why:** Returning a 50MB database payload will immediately blow out the LLM's context window.
* **Implementation:** The execution runtime must implement **Context Compression**. The script must parse, filter, and extract *only the semantic delta* needed by the agent before returning the payload.

## Failing Forward (Semantic Error Hints)

**Rule:** A skill MUST NEVER return raw system stack traces (e.g., `NullPointerException at line 42`) to the LLM.

* **Why:** LLMs cannot debug your backend code. Raw errors cause them to loop infinitely or hallucinate fixes.
* **Implementation:** Skills must catch their own exceptions and return **Semantic Error Hints**. (e.g., `{"status": "error", "message": "Invalid date format. Expected YYYY-MM-DD. Please try again."}`). This teaches the LLM *how* to self-correct on the next turn.

## Idempotency & The "Dry-Run" Pattern

**Rule:** Any skill that mutates state (Write, Update, Delete) MUST be strictly idempotent.

* **Why:** LLMs are non-deterministic and may accidentally invoke the same payload twice due to network retries or reasoning loops.
* **Implementation:** High-risk skills must support a `dry_run: boolean` parameter. This allows the Agent to simulate the mutation, observe the potential blast radius in the response, and verify intent *before* committing the actual state change.

## Cryptographic Boundaries & HITL

**Rule:** Skills must operate on the Principle of Least Privilege.

* **Why:** Prompt injection allows external actors to hijack the LLM's tool-calling engine.
* **Implementation:**
  * **Scoped Tokens:** Do not give the Agent global admin credentials. The Execution Runtime must inject scoped OAuth tokens just-in-time during the tool call.
  * **Human-in-the-Loop (HITL):** High-risk skills (e.g., `drop_table`, `deploy_prod`) must pause execution, page a human administrator via UI/Slack with the LLM's proposed parameters, and require cryptographic approval before the runtime executes the code.
