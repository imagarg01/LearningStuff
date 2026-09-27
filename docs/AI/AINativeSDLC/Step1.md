This transition redefines how an enterprise ships software. Instead of developers writing code from scratch, the process evolves into a Cognitive Pipeline where specialized AI agents orchestrate the entire lifecycle, governed by the decentralized .ai/CONTEXT.md acting as the enterprise rulebook.

Here is what that fully native agentic ecosystem looks like in practice.

## The Cognitive Pipeline

Enterprise Cognitive SDLC Engine: Detailed Architecture & Workflow

Document Owner: Platform Engineering / Product
Status: Architectural Blueprint
Objective: Define the nth-level procedural workflow for the LangGraph-based Cognitive SDLC Engine, transitioning the enterprise to Spec-Driven Development (SDD).

The Core State Machine (LangGraph Schema)

The engine relies on a strictly typed state payload passed between nodes. This prevents context loss and ensures deterministic execution.

class SDLCState(TypedDict):
    ticket_id: str
    jira_intent: str
    blast_radius_files: List[str]
    context_payload: str          # The Repomix packed XML
    generated_spec: str           # The proposed SPEC.md
    spec_approved: bool           # Human-in-the-loop gate
    execution_status: str         # "pending", "tests_failed", "success"
    pr_url: str
    telemetry_status: str         # "monitoring", "stable", "rollback"

Step 1: Context Assembly & Ingestion (The Sandbox)

Goal: Create a mathematically precise context window to prevent LLM hallucination in undocumented brownfield code.

1.1 Intent Extraction Node

Input: Webhook payload from Jira (Epic or Story transitions to "In Refinement").

Process: A fast, low-cost LLM (e.g., Claude 3.5 Haiku) parses the Jira description.

Output: Generates a structured JSON of keywords, domain entities, and likely file paths. (e.g., {"entities": ["UserChurn", "LegacyBilling"], "keywords": ["calc_metrics_v2"]}).

1.2 Infrastructure Locator Node (MCP)

Process: The node calls a local shell MCP server equipped with fd and ripgrep.

Execution:

fd CONTEXT.md: Finds all domain boundary rules.

rg "calc_metrics_v2": Locates the exact files containing the target legacy code.

Output: An initial list of seed files.

1.3 AST Blast-Radius Expansion Node

Process: The agent passes the seed files to the AST Code Index MCP (powered by Tree-sitter).

Execution: The MCP parses the legacy code into an Abstract Syntax Tree. The node executes structural queries:

Find Callees: What database calls or external services does this seed function touch?

Find Callers: What downstream services rely on the return payload of this seed function? (Search depth = 2).

Output: blast_radius_files list is finalized. The agent now knows exactly what will break if this code changes.

1.4 Repomix Packer Node

Process: The engine invokes Repomix via CLI/MCP.

Execution: Repomix is instructed to pack only the blast_radius_files and all .ai/CONTEXT.md files located in their parent directories.

Output: context_payload is generated as an optimized XML string.

Step 2: The Planning Agent (Spec Generation)

Goal: Translate ambiguous human intent into a deterministic, machine-readable contract that complies with enterprise architecture.

2.1 The Constraint Resolution Engine

Process: The Planning Agent is prompted to act as a Principal Architect. It compares jira_intent against the rules defined in the .ai/CONTEXT.md section of the context_payload.

Conflict Handling: If the Jira ticket asks for a UI change in a microservice defined in CONTEXT.md as "Headless/Backend Only," the Planning Agent must override the Jira request and draft an API-only specification.

2.2 Spec Drafting Node

Process: The agent generates the SPEC.md.

Strict Schema Enforcement: The output MUST follow this format:

## 1. Scope Boundaries: Explicit list of files the swarm is permitted to edit

## 2. Contract Changes: Exact OpenAPI, AsyncAPI, or Protobuf diffs

## 3. Execution Tasks: A sequential list of atomic tasks (e.g., "1. Extract pure function, 2. Write tests, 3. Inject dependency")

Step 3: Human-in-the-Loop Gate (Global Architectural Authority)

Goal: Shift human effort from typing syntax to validating architecture.

3.1 LangGraph Interrupt

Process: The state machine reaches the human_review node and executes a standard LangGraph interrupt (__end__ state or breakpoint).

Action: The engine updates the SDLC Console UI (the web dashboard) flagging the ticket as "Awaiting Architectural Approval."

3.2 Human Review & Locking

Process: The Principal Engineer views the SPEC.md alongside the constraint resolution logs (showing why the AI made certain choices).

Action: The engineer modifies the spec if needed, then clicks "Approve."

Output: The SPEC.md is committed to git (e.g., feature/JIRA-1234-spec). LangGraph state spec_approved is set to True, and the graph resumes.

Step 4: The Execution Swarm (Code Generation)

Goal: Implement the spec using a multi-agent Red/Green/Refactor loop.

4.1 Sub-Agent Orchestration

Process: The main LangGraph node spins up a sub-graph for execution. It reads the Execution Tasks from SPEC.md and assigns them sequentially.

4.2 Test-Driven Generation (Test Agent)

Process: A specialized Test Agent reads the SPEC.md and generates unit and integration tests. In brownfield repos, it also generates "characterization tests" to lock in current behavior.

Output: Fails initially (Red phase).

4.3 Implementation (Coding Agent)

Process: The Coding Agent reads the SPEC.md and the failing tests. It modifies the files listed in the Scope Boundaries.

Output: Code changes.

4.4 The Validation Loop (Compiler/Linter)

Process: A tool node runs npm test, mvn clean test, or pytest.

Feedback: If the build fails, the stderr stack trace is captured and routed back to the Coding Agent.

Constraint: This loop is capped at 5 iterations. If it fails 5 times, the agent must ask for human help, preventing infinite API token burn.

Step 5: Governance & Universal Deployment

Goal: Ensure compliance, generate the PR, and execute a safe, monitored rollout.

5.1 The Governance Review Node

Process: Before PR creation, a separate Governance Agent (using a different LLM for adversarial checking, e.g., GPT-4o checking Claude 3.5) reads the final code diff.

Validation: It strictly checks the diff against .ai/CONTEXT.md. (e.g., Did the coding agent sneak in a raw SQL query despite the spec?)

Output: If passed, the engine opens a Pull Request.

5.2 Universal Deployment Agent (UDA)

Trigger: Human merges the PR to main.

Infrastructure (MCP): The UDA connects to a Terraform MCP server. It runs terraform plan to ensure any required infrastructure (e.g., new Kafka topics) is provisioned.

Deployment: The UDA triggers the deployment pipeline (e.g., ArgoCD or GitHub Actions).

5.3 The Telemetry Fallback (Observability MCP)

Process: Because brownfield tests are untrustworthy, the UDA monitors the release in production.

Execution: It connects to the Observability MCP (Datadog/Logfire). It runs a continuous query for 15 minutes, comparing error rates and latency metrics on the modified endpoints against historical baselines.

Output: If anomalies exceed a 5% deviation threshold, the UDA autonomously triggers a deployment rollback and alerts the engineering team via Slack. If stable, the Jira ticket is moved to "Done".
