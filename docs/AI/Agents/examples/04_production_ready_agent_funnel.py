"""
Pattern 4 (Capstone): The Production-Ready Agent Funnel
=======================================================
Mapped to Agent Learning Path: Module 08 (Production-Grade Agent Architecture)

Demonstrates how a Production Agent tames the two fundamental forces of the AI era:
1. Unbounded Input (ambiguous, missing context, out-of-distribution)
2. The Generative Machine (plausible-story bias, hallucinated IDs, infinite retry loops)

Connects all 5 layers of the Probabilistic-to-Deterministic Funnel in one executable script:
- Layer 1: Epistemic Humility ("Stop-and-Ask" Missing-Slot Gate + Deterministic Session Context)
- Layer 2: Progressive Skill Discovery (SEP-2640 3-Tier Funnel + SHA-256 Manifest Verification)
- Layer 3: The Neuro-Symbolic Sandwich (Zero-Trust Argument Provenance Guard)
- Layer 4: Deterministic MCP Wall (SEP-1303 Recovery Hints, MRTR High-Risk Approval, Loop Circuit Breaker)
- Layer 5: OpenTelemetry (SEP-414) Trace Emission -> Continuous Eval Fixture Flywheel
"""

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from typing import Any


def sha256_str(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


@dataclass
class SessionContext:
    """Verified deterministic context injected by the host (never guessed by the LLM)."""
    authenticated_user: str
    role: str
    trace_id: str


class ProductionAgentFunnel:
    """
    Wraps a generative model inside the 5-Layer Probabilistic-to-Deterministic Funnel.
    """

    def __init__(self):
        self.skill_uri = "skill://shop/refund-processing/SKILL.md"
        self.skill_md = (
            "---\n"
            "name: refund-processing\n"
            "description: Process customer order refunds within the 30-day eligibility window.\n"
            "min_model_tier: flash\n"
            "---\n"
            "# Refund Processing Playbook\n"
            "1. Invoke `process_refund(order_id, effective_date)`.\n"
            "2. Refunds > $1,000 require MRTR human supervisor approval.\n"
        )
        self.skill_digest = sha256_str(self.skill_md)
        self.max_turns = 3
        self.otel_anomaly_traces: list[dict[str, Any]] = []
        self.db = {
            "ord_901": {"amount": 250.0, "days_old": 10, "status": "paid"},
            "ord_500": {"amount": 2500.0, "days_old": 5, "status": "paid"},
        }

    # --- Layer 1: Ingestion & Epistemic Humility Gate ---
    def check_epistemic_humility_gate(self, user_prompt: str) -> tuple[bool, str, set[str]]:
        """
        Extract grounded entity IDs from the user prompt.
        If the user asks for a refund without providing an `ord_<id>`, STOP and ASK
        instead of letting the generative model guess!
        """
        found_orders = set(re.findall(r"\bord_[0-9]+\b", user_prompt))
        if not found_orders:
            return (
                False,
                "🛑 [Layer 1: Stop-and-Ask Gate] status='needs_human_feedback' -> "
                "Could you please provide your order ID (e.g., 'ord_901') so I can look up your refund?",
                set(),
            )
        return True, "OK", found_orders

    # --- Layer 3: Neuro-Symbolic Post-Condition Provenance Guard ---
    def verify_argument_provenance(
        self, proposed_args: dict[str, Any], allowlisted_ids: set[str]
    ) -> tuple[bool, str]:
        """
        Zero-Trust Provenance Check: Every entity identifier passed to a mutating tool
        MUST exist in the verified provenance set (user prompt or prior read-tool output).
        """
        proposed_order_id = str(proposed_args.get("order_id", ""))
        if proposed_order_id not in allowlisted_ids:
            return (
                False,
                f"🛡️ [Layer 3: Neuro-Symbolic Provenance Guard] BLOCKED hallucinated order_id='{proposed_order_id}'. "
                f"Allowed provenance set: {sorted(allowlisted_ids)}",
            )
        return True, "OK"

    # --- Layer 4: Deterministic MCP Server Boundary (SEP-1303 & MRTR) ---
    def execute_mcp_tool(self, args: dict[str, Any]) -> dict[str, Any]:
        order_id = args.get("order_id", "")
        eff_date = str(args.get("effective_date", "2026-10-31"))

        # SEP-1303 Semantic Validation Error Hint
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", eff_date):
            return {
                "resultType": "complete",
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": f"SEP-1303 Hint: Invalid effective_date '{eff_date}'. Expected ISO 'YYYY-MM-DD' (e.g., '2026-10-31').",
                    }
                ],
            }

        order = self.db.get(order_id)
        if not order:
            return {
                "resultType": "complete",
                "isError": True,
                "content": [{"type": "text", "text": f"Order '{order_id}' not found."}],
            }

        # Tiered Autonomy: High-value refunds (> $1,000) trigger MCP MRTR Human Approval Gate
        if order["amount"] > 1000.0:
            return {
                "resultType": "input_required",
                "isError": False,
                "requestState": "signed_state_token_9981",
                "elicitation": {
                    "mode": "form",
                    "message": f"High-value refund (${order['amount']:.2f} on {order_id}) requires supervisor approval.",
                },
            }

        order["status"] = "refunded"
        return {
            "resultType": "complete",
            "isError": False,
            "content": [{"type": "text", "text": f"Refund of ${order['amount']:.2f} completed for {order_id}."}],
            "structuredContent": {"order_id": order_id, "amount": order["amount"], "status": "refunded"},
        }

    # --- Full Funnel Orchestration Loop ---
    def handle_request(
        self,
        scenario_name: str,
        user_prompt: str,
        session: SessionContext,
        simulated_llm_proposals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        print(f"\n🔹 {scenario_name}")
        print(f"   User Input: \"{user_prompt}\"")

        # Layer 1: Epistemic Humility Check
        ok, msg, provenance_ids = self.check_epistemic_humility_gate(user_prompt)
        if not ok:
            print(f"   {msg}")
            return {"status": "needs_human_feedback", "reason": "missing_order_id"}

        # Layer 2: Progressive Skill Discovery & SEP-2640 Digest Verification
        digest_ok = sha256_str(self.skill_md) == self.skill_digest
        print(f"   ✅ [Layer 2: SEP-2640 Skill Loaded] {self.skill_uri} (SHA-256 Verified={digest_ok})")

        seen_call_hashes: set[str] = set()
        for turn_idx, proposed_args in enumerate(simulated_llm_proposals, 1):
            if turn_idx > self.max_turns:
                print("   ⚡ [Layer 4: Circuit Breaker] Max turns exceeded! Aborting.")
                break

            # Semantic Loop Diffing Circuit Breaker
            call_signature = json.dumps(proposed_args, sort_keys=True)
            if call_signature in seen_call_hashes:
                print(
                    f"   ⚡ [Layer 4: Semantic Loop Circuit Breaker] Turn {turn_idx}: Model proposed identical "
                    f"failing call {call_signature} twice! Terminating loop & emitting SEP-414 OTel anomaly."
                )
                self.otel_anomaly_traces.append(
                    {
                        "trace_id": session.trace_id,
                        "skill_digest": self.skill_digest[:24],
                        "anomaly": "STUCK_IDENTICAL_TOOL_CALL_LOOP",
                        "user_prompt": user_prompt,
                    }
                )
                return {"status": "aborted_by_circuit_breaker"}
            seen_call_hashes.add(call_signature)

            # Layer 3: Neuro-Symbolic Post-Condition Provenance Guard
            prov_ok, prov_msg = self.verify_argument_provenance(proposed_args, provenance_ids)
            if not prov_ok:
                print(f"   {prov_msg}")
                self.otel_anomaly_traces.append(
                    {
                        "trace_id": session.trace_id,
                        "skill_digest": self.skill_digest[:24],
                        "anomaly": "HALLUCINATED_ARG_BLOCKED",
                        "user_prompt": user_prompt,
                    }
                )
                return {"status": "blocked_by_provenance_guard"}

            # Layer 4: Execute Deterministic MCP Tool
            mcp_res = self.execute_mcp_tool(proposed_args)

            if mcp_res["resultType"] == "input_required":
                print(f"   ⏸️  [Layer 4: MCP MRTR Gate] {mcp_res['elicitation']['message']}")
                return {"status": "paused_for_mrtr_approval", "requestState": mcp_res["requestState"]}

            if mcp_res["isError"]:
                hint = mcp_res["content"][0]["text"]
                print(f"   ⚠️  [Layer 4: Turn {turn_idx} SEP-1303 Error] {hint}")
                continue

            print(f"   🎯 [Layer 4: Turn {turn_idx} MCP Actuation Success] {mcp_res['content'][0]['text']}")
            return {"status": "completed", "turns": turn_idx, "structuredContent": mcp_res["structuredContent"]}

        return {"status": "failed"}


def run_demo():
    print("=" * 78)
    print("Capstone Demo: The Production-Ready Agent Funnel (Module 08)")
    print("Taming Unbounded Input & The Generative Machine Across 5 Scenarios")
    print("=" * 78)

    funnel = ProductionAgentFunnel()

    # Scenario 1: Ambiguous / Unbounded Input (Missing order_id)
    funnel.handle_request(
        scenario_name="Scenario 1: Unbounded Ambiguous Input (Missing Required Slot)",
        user_prompt="Hi, my package arrived broken, please refund my order right now!",
        session=SessionContext("alice", "customer", "trace_001"),
        simulated_llm_proposals=[{"order_id": "ord_12345_guessed"}],
    )

    # Scenario 2: Generative Model Hallucinates an Unrelated Order ID
    funnel.handle_request(
        scenario_name="Scenario 2: Generative Hallucination Attempt (Zero-Trust Provenance Guard)",
        user_prompt="Can you check or refund order ord_901?",
        session=SessionContext("alice", "customer", "trace_002"),
        simulated_llm_proposals=[{"order_id": "ord_999_hallucinated", "effective_date": "2026-10-31"}],
    )

    # Scenario 3: Format Mistake -> SEP-1303 Self-Correction on Turn 2
    funnel.handle_request(
        scenario_name="Scenario 3: SEP-1303 Closed-Loop Self-Correction (Recovers in 1 Retry)",
        user_prompt="Please refund order ord_901.",
        session=SessionContext("alice", "customer", "trace_003"),
        simulated_llm_proposals=[
            {"order_id": "ord_901", "effective_date": "10/31/2026"},  # Turn 1: bad format
            {"order_id": "ord_901", "effective_date": "2026-10-31"},  # Turn 2: self-corrected via SEP-1303
        ],
    )

    # Scenario 4: High-Value Mutation -> Paused by MCP MRTR Human Approval Gate
    funnel.handle_request(
        scenario_name="Scenario 4: High-Blast-Radius Action ($2,500) -> MCP MRTR Human Approval Gate",
        user_prompt="Please refund enterprise order ord_500.",
        session=SessionContext("alice", "customer", "trace_004"),
        simulated_llm_proposals=[{"order_id": "ord_500", "effective_date": "2026-10-31"}],
    )

    # Scenario 5: Confused Generative Model Stuck Repeating Identical Invalid Call
    funnel.handle_request(
        scenario_name="Scenario 5: Stuck Generative Model -> Semantic Loop Diffing Circuit Breaker",
        user_prompt="Please refund order ord_901.",
        session=SessionContext("alice", "customer", "trace_005"),
        simulated_llm_proposals=[
            {"order_id": "ord_901", "effective_date": "31-10-2026"},
            {"order_id": "ord_901", "effective_date": "31-10-2026"},  # Identical bad retry!
        ],
    )

    print("\n" + "-" * 78)
    print("📡 Layer 5: SEP-414 OTel Anomalies Captured for Continuous Eval Flywheel:")
    print(json.dumps(funnel.otel_anomaly_traces, indent=2))
    print("=" * 78)


if __name__ == "__main__":
    run_demo()
