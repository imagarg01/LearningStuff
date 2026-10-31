"""
Eval Engineering 05: The Unified Agent + Skill + MCP + Eval Pipeline
====================================================================
Addresses:
"Make it part of a comprehensive pipeline... Agent + MCP + Skill + Eval ... part of the same puzzle"

Demonstrates all 4 components working together in a single closed-loop execution & evaluation pipeline:
1. SKILL (SEP-2640): Hosted on the MCP Server (`skill://shop/refund-processing/SKILL.md`) with SHA-256 manifest.
2. MCP SERVER (2026-07-28): Serves `skills/list`, `resources/read`, and `tools/call` with SEP-1303 error hints
   and SEP-414 OpenTelemetry span recording.
3. AGENT ORCHESTRATOR: Discovers the skill, verifies the SHA-256 digest, executes the tool call with
   W3C `traceparent` + `baggage`, and synthesizes a grounded user response.
4. 4-LAYER UNIFIED EVAL ENGINE:
   - Layer 1: Skill Discovery & SHA-256 Integrity Check
   - Layer 2: Cognitive Argument Provenance & Schema Check
   - Layer 3: MCP Actuation & Token Amplification (TAF <= 1.25) Check
   - Layer 4: Stateful World-State Post-Condition & Grounded Synthesis Rubric Check
"""

import hashlib
import json
from dataclasses import dataclass
from typing import Any


def sha256_digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


# ============================================================================
# 1. SKILL + 2. MCP SERVER (SEP-2640 Skills + SEP-1303 Tools + SEP-414 OTel)
# ============================================================================

class UnifiedMCPServer:
    def __init__(self):
        self.version = "2.1.0"
        self.skill_uri = "skill://shop/refund-processing/SKILL.md"
        self.skill_content = (
            "---\n"
            "name: refund-processing\n"
            "description: Verify 30-day eligibility and process customer order refunds.\n"
            "min_model_tier: flash\n"
            "---\n"
            "# Refund Processing Skill\n"
            "1. Call `process_refund` with `order_id` and `reason_code`.\n"
            "2. Never promise a refund if `isError: true` is returned by the tool.\n"
        )
        self.skill_digest = sha256_digest(self.skill_content)
        self.otel_spans: list[dict[str, Any]] = []
        self.reset_sandbox()

    def reset_sandbox(self):
        self.db = {
            "ord_901": {"customer": "alice", "amount": 250.0, "days_old": 10, "status": "paid"},
            "ord_404": {"customer": "bob", "amount": 800.0, "days_old": 95, "status": "paid"},
        }

    def handle_jsonrpc(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        meta = params.get("_meta", {})
        self.otel_spans.append(
            {
                "mcp.method.name": method,
                "traceparent": meta.get("traceparent", ""),
                "baggage": meta.get("baggage", ""),
            }
        )

        if method == "skills/list":
            return {
                "skills": [
                    {
                        "uri": self.skill_uri,
                        "frontmatter": {
                            "name": "refund-processing",
                            "description": "Verify 30-day eligibility and process customer order refunds.",
                        },
                        "manifest": [
                            {
                                "uri": self.skill_uri,
                                "size": len(self.skill_content.encode("utf-8")),
                                "digest": self.skill_digest,
                            }
                        ],
                    }
                ]
            }

        if method == "resources/read":
            return {"contents": [{"uri": self.skill_uri, "text": self.skill_content}]}

        if method == "tools/call":
            args = params.get("arguments", {})
            order_id = args.get("order_id", "")
            order = self.db.get(order_id)
            if not order:
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": f"Order '{order_id}' not found. Verify order_id."}],
                }
            if order["days_old"] > 30:
                return {
                    "isError": True,
                    "content": [
                        {
                            "type": "text",
                            "text": f"Cannot refund {order_id}: order is {order['days_old']} days old (policy max is 30 days).",
                        }
                    ],
                    "structuredContent": {"order_id": order_id, "status": "declined_policy_window"},
                }

            order["status"] = "refunded"
            return {
                "isError": False,
                "content": [{"type": "text", "text": f"Refund of ${order['amount']:.2f} completed for {order_id}."}],
                "structuredContent": {"order_id": order_id, "refunded_amount": order["amount"], "status": "refunded"},
            }

        raise ValueError(f"Unknown MCP method: {method}")


# ============================================================================
# 3. AGENT ORCHESTRATOR (Discovers Skill -> Verifies Digest -> Calls MCP Tool)
# ============================================================================

class EnterpriseAgent:
    def __init__(self, model_name: str, mcp_server: UnifiedMCPServer):
        self.model_name = model_name
        self.mcp = mcp_server

    def run_turn(self, user_prompt: str, trace_id: str) -> dict[str, Any]:
        traceparent = f"00-{trace_id}-00f067aa0ba902b7-01"

        # Step 1: Discover skills via MCP `skills/list`
        catalog = self.mcp.handle_jsonrpc("skills/list", {"_meta": {"traceparent": traceparent}})
        selected_skill = catalog["skills"][0]
        expected_digest = selected_skill["manifest"][0]["digest"]

        # Step 2: Lazy-load `SKILL.md` via `resources/read` and verify SEP-2640 SHA-256 digest
        resource = self.mcp.handle_jsonrpc(
            "resources/read", {"uri": selected_skill["uri"], "_meta": {"traceparent": traceparent}}
        )
        downloaded_md = resource["contents"][0]["text"]
        digest_verified = sha256_digest(downloaded_md) == expected_digest

        # Step 3: Formulate tool call with SEP-414 lineage baggage
        order_id = "ord_901" if "ord_901" in user_prompt else "ord_404"
        baggage = f"skill.uri={selected_skill['uri']},skill.digest={expected_digest[:20]}"
        tool_call_args = {"order_id": order_id, "reason_code": "damaged"}

        tool_res = self.mcp.handle_jsonrpc(
            "tools/call",
            {
                "name": "process_refund",
                "arguments": tool_call_args,
                "_meta": {"traceparent": traceparent, "baggage": baggage},
            },
        )

        # Step 4: Synthesize grounded response strictly from MCP tool output
        if tool_res["isError"]:
            final_answer = f"I could not process the refund for {order_id}: {tool_res['content'][0]['text']}"
        else:
            sc = tool_res["structuredContent"]
            final_answer = f"Your refund of ${sc['refunded_amount']:.2f} for {order_id} has been processed."

        return {
            "trace_id": trace_id,
            "user_prompt": user_prompt,
            "selected_skill_uri": selected_skill["uri"],
            "skill_digest_verified": digest_verified,
            "tool_args": tool_call_args,
            "tool_result": tool_res,
            "final_answer": final_answer,
            "turns_taken": 1,
            "taf": 1.00,
        }


# ============================================================================
# 4. THE 4-LAYER UNIFIED EVAL ENGINE
# ============================================================================

@dataclass
class UnifiedEvalCase:
    case_id: str
    user_prompt: str
    expected_skill_uri: str
    expected_order_id: str
    expected_final_db_status: str
    expect_tool_error: bool


def evaluate_unified_trace(
    case: UnifiedEvalCase, trace: dict[str, Any], sandbox_db: dict[str, Any]
) -> dict[str, Any]:
    # Layer 1: Skill Discovery & Cryptographic Integrity (Agent <-> Skill)
    layer1_routing_ok = (
        trace["selected_skill_uri"] == case.expected_skill_uri and trace["skill_digest_verified"] is True
    )

    # Layer 2: Cognitive Schema & Argument Provenance (Agent <-> SKILL.md)
    arg_order_id = trace["tool_args"].get("order_id", "")
    layer2_cognitive_ok = arg_order_id == case.expected_order_id and arg_order_id in case.user_prompt

    # Layer 3: MCP Actuation & Token Efficiency (Agent <-> MCP Server)
    layer3_mcp_ok = (
        trace["tool_result"]["isError"] == case.expect_tool_error and trace["taf"] <= 1.25
    )

    # Layer 4: World-State Post-Condition & Grounded Response (End-to-End Outcome)
    actual_db_status = sandbox_db[case.expected_order_id]["status"]
    state_matches = actual_db_status == case.expected_final_db_status
    response_text = trace["final_answer"].lower()
    if case.expect_tool_error:
        grounded_text = "could not process" in response_text and "30 days" in response_text
    else:
        grounded_text = "has been processed" in response_text and case.expected_order_id in response_text
    layer4_outcome_ok = state_matches and grounded_text

    all_layers_passed = layer1_routing_ok and layer2_cognitive_ok and layer3_mcp_ok and layer4_outcome_ok
    return {
        "case_id": case.case_id,
        "Layer1_Skill_Routing_And_SHA256": "✅ PASS" if layer1_routing_ok else "❌ FAIL",
        "Layer2_Cognitive_Arg_Provenance": "✅ PASS" if layer2_cognitive_ok else "❌ FAIL",
        "Layer3_MCP_Actuation_And_TAF": "✅ PASS" if layer3_mcp_ok else "❌ FAIL",
        "Layer4_WorldState_And_Grounding": "✅ PASS" if layer4_outcome_ok else "❌ FAIL",
        "overall": "✅ PASS" if all_layers_passed else "❌ FAIL",
    }


def run_demo():
    print("=" * 78)
    print("Eval Engineering 05: The Unified Agent + Skill + MCP + Eval Pipeline")
    print("=" * 78)

    mcp_server = UnifiedMCPServer()
    agent = EnterpriseAgent(model_name="gemini-flash-latest", mcp_server=mcp_server)

    eval_suite = [
        UnifiedEvalCase(
            case_id="EVAL-01 (Eligible 10-Day Order Refund)",
            user_prompt="My item arrived damaged. Please refund order ord_901.",
            expected_skill_uri="skill://shop/refund-processing/SKILL.md",
            expected_order_id="ord_901",
            expected_final_db_status="refunded",
            expect_tool_error=False,
        ),
        UnifiedEvalCase(
            case_id="EVAL-02 (Out-of-Policy 95-Day Order Guardrail)",
            user_prompt="Please refund my old order ord_404.",
            expected_skill_uri="skill://shop/refund-processing/SKILL.md",
            expected_order_id="ord_404",
            expected_final_db_status="paid",  # Must NOT mutate to 'refunded'!
            expect_tool_error=True,
        ),
    ]

    lineage_header = {
        "gen_ai.agent.model": agent.model_name,
        "skill.uri": mcp_server.skill_uri,
        "skill.digest": mcp_server.skill_digest[:28] + "...",
        "mcp.server.version": mcp_server.version,
        "eval.suite.cases": len(eval_suite),
    }
    print("\n🔗 Unified 4-Part Lineage Context (Agent + Skill + MCP + Eval):")
    print(json.dumps(lineage_header, indent=2))

    print("\n🧪 Executing 4-Layer Unified Evaluation Matrix:")
    print("-" * 78)
    results = []
    for idx, case in enumerate(eval_suite, 1):
        mcp_server.reset_sandbox()
        trace = agent.run_turn(case.user_prompt, trace_id=f"4bf92f3577b34da6a3ce929d0e0e000{idx}")
        scorecard = evaluate_unified_trace(case, trace, mcp_server.db)
        results.append(scorecard)
        print(f"\n📌 {case.case_id}")
        print(f"   User Prompt:  \"{case.user_prompt}\"")
        print(f"   Agent Answer: \"{trace['final_answer']}\"")
        print(f"   4-Layer Eval: {json.dumps(scorecard, indent=6)}")

    passed_count = sum(1 for r in results if r["overall"] == "✅ PASS")
    print("\n" + "=" * 78)
    print(f"🏆 Unified Pipeline Gate Verdict: {passed_count}/{len(results)} Cases Passed Across All 4 Stack Layers!")
    print("=" * 78)


if __name__ == "__main__":
    run_demo()
