"""
Skill Engineering 03: Model-Agnostic Skill Test Harness
=======================================================
Addresses Question 3:
"How to do model-agnostic testing?"

Demonstrates the 4 Pillars of Model-Agnostic Skill Testing:
1. Canonical Tool-Call Normalizer:
   Normalizes incompatible provider payloads (Google Gemini `function_call`, Anthropic `tool_use`,
   OpenAI `tool_calls`, and raw MCP `tools/call`) into a unified `CanonicalInvocation` AST,
   stripping model-specific prose and `<thinking>` tags.
2. Stateful MCP Sandbox & World-State Assertions:
   Tests *outcomes* (final database state & safety invariants) rather than brittle step-by-step
   tool sequences, allowing different models to take different valid read paths.
3. SEP-1303 Closed-Loop Self-Correction Test:
   Verifies that the skill's semantic error hints enable any model to self-correct in 1 turn.
4. Cross-Model Pass^k (Pass-to-the-Power-of-k) & TAF Matrix.
"""

import copy
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CanonicalInvocation:
    """Provider-agnostic representation of a skill/tool invocation."""
    skill_uri: str
    tool_name: str
    canonical_args: dict[str, Any]


def normalize_provider_response(raw_response: dict[str, Any], active_skill_uri: str) -> list[CanonicalInvocation]:
    """
    Convert any LLM provider's tool-calling wire format into a canonical list of invocations.
    Ignores conversational prose, reasoning traces, and provider-specific envelope fields.
    """
    invocations: list[CanonicalInvocation] = []

    # 1. Google Gemini format: candidates[0].content.parts[].function_call
    if "candidates" in raw_response:
        parts = raw_response["candidates"][0].get("content", {}).get("parts", [])
        for part in parts:
            if "function_call" in part:
                fc = part["function_call"]
                invocations.append(
                    CanonicalInvocation(
                        skill_uri=active_skill_uri,
                        tool_name=fc["name"],
                        canonical_args=_canonicalize_args(fc.get("args", {})),
                    )
                )

    # 2. Anthropic Claude format: content[] with type == "tool_use"
    elif "content" in raw_response and isinstance(raw_response["content"], list):
        for block in raw_response["content"]:
            if block.get("type") == "tool_use":
                invocations.append(
                    CanonicalInvocation(
                        skill_uri=active_skill_uri,
                        tool_name=block["name"],
                        canonical_args=_canonicalize_args(block.get("input", {})),
                    )
                )

    # 3. OpenAI format: choices[0].message.tool_calls[].function
    elif "choices" in raw_response:
        tool_calls = raw_response["choices"][0].get("message", {}).get("tool_calls", [])
        for tc in tool_calls:
            fn = tc.get("function", {})
            raw_args = fn.get("arguments", "{}")
            parsed_args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
            invocations.append(
                CanonicalInvocation(
                    skill_uri=active_skill_uri,
                    tool_name=fn["name"],
                    canonical_args=_canonicalize_args(parsed_args),
                )
            )

    # 4. Native MCP JSON-RPC `tools/call` format
    elif raw_response.get("method") == "tools/call":
        params = raw_response.get("params", {})
        invocations.append(
            CanonicalInvocation(
                skill_uri=active_skill_uri,
                tool_name=params["name"],
                canonical_args=_canonicalize_args(params.get("arguments", {})),
            )
        )

    return invocations


def _canonicalize_args(args: dict[str, Any]) -> dict[str, Any]:
    """Normalize numeric types (e.g., 250 -> 250.0) and strip whitespace on string values."""
    normalized = {}
    for k in sorted(args.keys()):
        val = args[k]
        if isinstance(val, str):
            normalized[k] = val.strip()
        elif isinstance(val, int) and not isinstance(val, bool):
            normalized[k] = float(val)
        else:
            normalized[k] = val
    return normalized


class StatefulRefundMCPSandbox:
    """
    Deterministic in-memory MCP Server Sandbox for behavioral world-state testing.
    Allows asserting on the *final state* of the world regardless of which read tools
    a particular model called first.
    """

    def __init__(self):
        self.db = {
            "orders": {
                "ord_901": {"customer": "alice", "amount": 250.0, "days_old": 12, "status": "paid"},
                "ord_404": {"customer": "bob", "amount": 800.0, "days_old": 95, "status": "paid"},
            },
            "audit_log": [],
            "unauthorized_mutations": 0,
        }

    def execute_invocation(self, inv: CanonicalInvocation) -> dict[str, Any]:
        args = inv.canonical_args
        if inv.tool_name == "get_order":
            order = self.db["orders"].get(args.get("order_id", ""))
            return {"isError": False, "structuredContent": order or {}}

        if inv.tool_name == "list_customer_orders":
            cust = args.get("customer", "")
            matches = {k: v for k, v in self.db["orders"].items() if v["customer"] == cust}
            return {"isError": False, "structuredContent": matches}

        if inv.tool_name == "issue_refund":
            order_id = args.get("order_id", "")
            amount = args.get("amount", 0.0)
            iso_date = args.get("effective_date", "2026-10-31")

            # SEP-1303 Validation check on date format
            if "/" in str(iso_date):
                return {
                    "isError": True,
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"Invalid effective_date '{iso_date}'. "
                                "Expected ISO-8601 format 'YYYY-MM-DD' (e.g., '2026-10-31'). Please retry."
                            ),
                        }
                    ],
                }

            order = self.db["orders"].get(order_id)
            if not order:
                return {"isError": True, "content": [{"type": "text", "text": f"Order '{order_id}' not found."}]}

            if order["days_old"] > 30:
                self.db["unauthorized_mutations"] += 1
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": "Policy violation: Order is older than 30 days."}],
                }

            order["status"] = "refunded"
            order["refunded_amount"] = amount
            self.db["audit_log"].append({"order_id": order_id, "amount": amount, "date": iso_date})
            return {"isError": False, "structuredContent": {"order_id": order_id, "status": "refunded"}}

        return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {inv.tool_name}"}]}


def compute_pass_power_k(passing_trials: int, total_trials: int, k: int = 3) -> float:
    """Compute Pass^k = (c / n)^k: probability that ALL k independent runs succeed."""
    if total_trials == 0:
        return 0.0
    return round((passing_trials / total_trials) ** k, 4)


def run_demo():
    print("=" * 78)
    print("Skill Engineering 03: Model-Agnostic Skill Test Harness")
    print("=" * 78)

    skill_uri = "skill://shop/refund-processing/SKILL.md"

    # 1. Demonstrate Canonical Tool-Call Normalizer across 3 different LLM providers
    print("\n1️⃣  Pillar A: Canonical Tool-Call AST Normalization Across Providers")
    print("-" * 78)

    gemini_raw = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": "I will issue the refund for order ord_901 now."},
                        {"function_call": {"name": "issue_refund", "args": {"order_id": "ord_901", "amount": 250}}},
                    ]
                }
            }
        ]
    }

    claude_raw = {
        "content": [
            {"type": "thinking", "thinking": "Checking order eligibility first..."},
            {"type": "text", "text": "Let me process that refund for you."},
            {"type": "tool_use", "id": "toolu_01", "name": "issue_refund", "input": {"amount": 250.0, "order_id": "ord_901 "}},
        ]
    }

    openai_raw = {
        "choices": [
            {
                "message": {
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_abc",
                            "type": "function",
                            "function": {"name": "issue_refund", "arguments": '{"order_id": "ord_901", "amount": 250.0}'},
                        }
                    ],
                }
            }
        ]
    }

    norm_gemini = normalize_provider_response(gemini_raw, skill_uri)
    norm_claude = normalize_provider_response(claude_raw, skill_uri)
    norm_openai = normalize_provider_response(openai_raw, skill_uri)

    ast_identical = norm_gemini == norm_claude == norm_openai
    print(f"Normalized AST: {norm_gemini[0]}")
    print(f"Cross-Provider AST Equivalence (Gemini == Claude == OpenAI): {'✅ IDENTICAL' if ast_identical else '❌ MISMATCH'}")

    # 2. Demonstrate Behavioral World-State Assertions (Different Paths, Same Valid Outcome)
    print("\n2️⃣  Pillar B: Behavioral World-State Testing (Outcome vs. Trajectory)")
    print("-" * 78)
    model_trajectories = {
        "Gemini-Flash (Direct Lookup Path)": [
            CanonicalInvocation(skill_uri, "get_order", {"order_id": "ord_901"}),
            CanonicalInvocation(skill_uri, "issue_refund", {"order_id": "ord_901", "amount": 250.0, "effective_date": "2026-10-31"}),
        ],
        "Claude-Haiku (Customer Search Path)": [
            CanonicalInvocation(skill_uri, "list_customer_orders", {"customer": "alice"}),
            CanonicalInvocation(skill_uri, "issue_refund", {"order_id": "ord_901", "amount": 250.0, "effective_date": "2026-10-31"}),
        ],
    }

    for model_name, trajectory in model_trajectories.items():
        sandbox = StatefulRefundMCPSandbox()
        for step in trajectory:
            sandbox.execute_invocation(step)

        # World-State Post-Condition Assertion (Model-Agnostic!)
        order_state = sandbox.db["orders"]["ord_901"]
        state_passed = (
            order_state["status"] == "refunded"
            and order_state["refunded_amount"] == 250.0
            and sandbox.db["unauthorized_mutations"] == 0
            and len(sandbox.db["audit_log"]) == 1
        )
        tools_used = " -> ".join(inv.tool_name for inv in trajectory)
        print(f"   • {model_name:36} | Path: [{tools_used}] -> World-State: {'✅ PASS' if state_passed else '❌ FAIL'}")

    # 3. Demonstrate SEP-1303 Closed-Loop Self-Correction & Pass^3 Matrix
    print("\n3️⃣  Pillar C & D: SEP-1303 Self-Correction Loop & Cross-Model Pass^3 Matrix")
    print("-" * 78)
    sandbox = StatefulRefundMCPSandbox()
    # Turn 1: Model passes US date format "10/31/2026"
    turn1_inv = CanonicalInvocation(
        skill_uri, "issue_refund", {"order_id": "ord_901", "amount": 250.0, "effective_date": "10/31/2026"}
    )
    turn1_res = sandbox.execute_invocation(turn1_inv)
    print(f"   Turn 1 (Bad Date '10/31/2026') -> MCP SEP-1303 Response: isError={turn1_res['isError']}")
    print(f"   Hint Returned: \"{turn1_res['content'][0]['text']}\"")

    # Turn 2: Model reads SEP-1303 hint and self-corrects to "2026-10-31"
    turn2_inv = CanonicalInvocation(
        skill_uri, "issue_refund", {"order_id": "ord_901", "amount": 250.0, "effective_date": "2026-10-31"}
    )
    turn2_res = sandbox.execute_invocation(turn2_inv)
    print(f"   Turn 2 (Self-Corrected '2026-10-31') -> isError={turn2_res['isError']}, State={turn2_res['structuredContent']}")

    # Cross-Model Compatibility Matrix Summary
    matrix_summary = [
        {"model": "Gemini Pro (Frontier)", "trials": "10/10", "Pass^3": compute_pass_power_k(10, 10, 3), "TAF": 1.00},
        {"model": "Claude Sonnet (Frontier)", "trials": "10/10", "Pass^3": compute_pass_power_k(10, 10, 3), "TAF": 1.05},
        {"model": "Gemini Flash (Workhorse)", "trials": "10/10", "Pass^3": compute_pass_power_k(10, 10, 3), "TAF": 1.10},
        {"model": "Local 8B SLM (Edge)", "trials": "9/10", "Pass^3": compute_pass_power_k(9, 10, 3), "TAF": 1.22},
    ]
    print("\n📊 Cross-Model Compatibility Matrix Report:")
    print(json.dumps(matrix_summary, indent=2))


if __name__ == "__main__":
    run_demo()
