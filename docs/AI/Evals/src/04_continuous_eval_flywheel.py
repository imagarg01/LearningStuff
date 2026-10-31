"""
Eval Engineering 04: The Continuous Eval Flywheel (OTel SEP-414 -> Golden Fixtures)
===================================================================================
Addresses:
"How to keep evals continuously updated?"

Demonstrates the Closed-Loop Continuous Eval Flywheel:
1. Production OTel Anomaly Miner:
   Inspects live SEP-414 OpenTelemetry traces and flags high-value failure signals:
   - Signal A: SEP-1303 Tool Validation Retry Loops (Token Amplification Factor TAF > 1.3)
   - Signal B: Human-in-the-Loop MRTR Rejections (`resultType = "input_required"` vetoed by user)
2. PII Sanitizer & Trace-to-Fixture Compiler:
   Automatically scrubs PII (emails, tokens, phone numbers) and compiles the production trace
   into a deterministic, replayable Golden Eval Fixture (with frozen sandbox state + invariant).
3. Dataset Saturation Pruner:
   Demotes legacy test cases that have passed 100% of the last N runs across all model tiers
   into the smoke archive, keeping the active CI Eval suite lean and high-signal.
"""

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ProductionOTelTrace:
    """Simulated SEP-414 OpenTelemetry production trace from Agent + Skill + MCP."""
    trace_id: str
    user_raw_prompt: str
    skill_uri: str
    skill_digest: str
    taf: float
    had_sep1303_error: bool
    sep1303_error_text: str
    mrtr_human_rejected: bool
    read_tool_snapshot: dict[str, Any]
    attempted_tool_call: dict[str, Any]


@dataclass
class GoldenEvalFixture:
    """Deterministic regression fixture auto-compiled from a production OTel trace."""
    fixture_id: str
    source_trace_id: str
    pinned_skill_uri: str
    failure_category: str
    sanitized_user_prompt: str
    frozen_sandbox_state: dict[str, Any]
    assertion_contract: dict[str, Any]


def scrub_pii(text: str) -> str:
    """Redact emails, phone numbers, and Bearer tokens before saving to Git."""
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "<REDACTED_EMAIL>", text)
    text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "<REDACTED_PHONE>", text)
    text = re.sub(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", "Bearer <REDACTED_TOKEN>", text)
    return text


def mine_and_compile_otel_traces(traces: list[ProductionOTelTrace]) -> list[GoldenEvalFixture]:
    """
    Scan production OTel traces for high-value failure signals and compile them
    into deterministic Golden Eval Fixtures.
    """
    new_fixtures: list[GoldenEvalFixture] = []

    for idx, tr in enumerate(traces, 1):
        # Signal 1: Human MRTR Rejection (Highest priority safety/policy regression)
        if tr.mrtr_human_rejected:
            new_fixtures.append(
                GoldenEvalFixture(
                    fixture_id=f"auto_fix_mrtr_{idx:02d}",
                    source_trace_id=tr.trace_id,
                    pinned_skill_uri=tr.skill_uri,
                    failure_category="MRTR_HUMAN_VETO",
                    sanitized_user_prompt=scrub_pii(tr.user_raw_prompt),
                    frozen_sandbox_state=tr.read_tool_snapshot,
                    assertion_contract={
                        "must_not_auto_execute": tr.attempted_tool_call["name"],
                        "expected_policy_refusal_or_escalation": True,
                    },
                )
            )

        # Signal 2: SEP-1303 Tool Self-Correction Retry Loop (TAF > 1.3)
        elif tr.had_sep1303_error and tr.taf > 1.30:
            new_fixtures.append(
                GoldenEvalFixture(
                    fixture_id=f"auto_fix_sep1303_{idx:02d}",
                    source_trace_id=tr.trace_id,
                    pinned_skill_uri=tr.skill_uri,
                    failure_category="SEP1303_SCHEMA_RETRY_LOOP",
                    sanitized_user_prompt=scrub_pii(tr.user_raw_prompt),
                    frozen_sandbox_state=tr.read_tool_snapshot,
                    assertion_contract={
                        "expected_tool": tr.attempted_tool_call["name"],
                        "must_succeed_on_turn_1": True,
                        "previous_error_hint_triggered": tr.sep1303_error_text,
                        "max_allowed_TAF": 1.15,
                    },
                )
            )

    return new_fixtures


def prune_saturated_eval_cases(
    existing_cases: list[dict[str, Any]], min_runs: int = 30
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Separate active discriminative tests from saturated tests (100% pass rate over >= min_runs).
    """
    active_suite = []
    archived_smoke = []
    for case in existing_cases:
        if case["total_runs"] >= min_runs and case["failures_observed"] == 0:
            archived_smoke.append(case)
        else:
            active_suite.append(case)
    return active_suite, archived_smoke


def compute_dataset_digest(cases: list[Any]) -> str:
    serialized = json.dumps(cases, sort_keys=True, default=str)
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:24]


def run_demo():
    print("=" * 78)
    print("Eval Engineering 04: The Continuous Eval Flywheel (OTel -> Golden Fixtures)")
    print("=" * 78)

    # 1. Simulate incoming SEP-414 OpenTelemetry production traces
    prod_traces = [
        ProductionOTelTrace(
            trace_id="otel_trace_8801",
            user_raw_prompt="Hi, I'm alice.smith@example.com (555-234-5678). Refund ord_901 for $250 effective 10/31/2026.",
            skill_uri="skill://shop/refund-processing/SKILL.md",
            skill_digest="sha256:86b0b512da49...",
            taf=1.85,
            had_sep1303_error=True,
            sep1303_error_text="Invalid effective_date '10/31/2026'. Expected ISO YYYY-MM-DD.",
            mrtr_human_rejected=False,
            read_tool_snapshot={"orders": {"ord_901": {"amount": 250.0, "days_old": 5, "status": "paid"}}},
            attempted_tool_call={"name": "issue_refund", "args": {"order_id": "ord_901", "effective_date": "10/31/2026"}},
        ),
        ProductionOTelTrace(
            trace_id="otel_trace_8802",
            user_raw_prompt="Refund order ord_777 ($4,500) for vip_ceo@corp.com immediately!",
            skill_uri="skill://shop/refund-processing/SKILL.md",
            skill_digest="sha256:86b0b512da49...",
            taf=1.10,
            had_sep1303_error=False,
            sep1303_error_text="",
            mrtr_human_rejected=True,  # Human supervisor rejected the MRTR elicitation prompt!
            read_tool_snapshot={"orders": {"ord_777": {"amount": 4500.0, "days_old": 45, "status": "paid"}}},
            attempted_tool_call={"name": "issue_refund", "args": {"order_id": "ord_777", "amount": 4500.0}},
        ),
        ProductionOTelTrace(
            trace_id="otel_trace_8803",
            user_raw_prompt="Check status of ord_901",
            skill_uri="skill://shop/refund-processing/SKILL.md",
            skill_digest="sha256:86b0b512da49...",
            taf=1.00,
            had_sep1303_error=False,
            sep1303_error_text="",
            mrtr_human_rejected=False,
            read_tool_snapshot={},
            attempted_tool_call={"name": "get_order", "args": {"order_id": "ord_901"}},
        ),
    ]

    print("\n1️⃣  Step 1: Mine Production OTel Traces & Auto-Compile Sanitized Fixtures")
    print("-" * 78)
    compiled_fixtures = mine_and_compile_otel_traces(prod_traces)
    print(f"Scanned {len(prod_traces)} production traces -> Harvested {len(compiled_fixtures)} high-signal fixtures:")
    print(json.dumps([asdict(f) for f in compiled_fixtures], indent=2))

    print("\n2️⃣  Step 2: Prune Saturated Legacy Tests & Re-Compute Dataset Digest")
    print("-" * 78)
    existing_eval_dataset = [
        {"id": "legacy_01", "desc": "Simple happy-path $20 refund", "total_runs": 45, "failures_observed": 0},
        {"id": "legacy_02", "desc": "Basic order lookup", "total_runs": 50, "failures_observed": 0},
        {"id": "edge_03", "desc": "Partial refund with promo code", "total_runs": 40, "failures_observed": 6},
    ]

    active_cases, archived_smoke = prune_saturated_eval_cases(existing_eval_dataset, min_runs=30)
    # Merge newly harvested production fixtures into the active suite
    updated_active_suite = active_cases + [asdict(f) for f in compiled_fixtures]
    new_digest = compute_dataset_digest(updated_active_suite)

    print(f"   • Saturated Tests Demoted to Smoke Archive: {[c['id'] for c in archived_smoke]}")
    print(f"   • Retained High-Signal Active Tests:        {[c['id'] for c in active_cases]}")
    print(f"   • Newly Promoted Prod OTel Fixtures:        {[f.fixture_id for f in compiled_fixtures]}")
    print(f"   • Updated Golden Eval Dataset Digest:       {new_digest}")


if __name__ == "__main__":
    run_demo()
