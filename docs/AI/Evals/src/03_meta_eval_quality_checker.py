"""
Eval Engineering 03: Measuring the Quality of an Eval (Meta-Evaluation)
=======================================================================
Addresses:
"How to measure the quality of an eval?"

Demonstrates two core Meta-Evaluation mechanisms ("Testing the Tests"):
1. Mutation Testing for Evals (Defect Injection Score):
   Injects 5 realistic failure mutants (wrong skill routed, hallucinated order_id,
   policy violation, ignored tool error, ungrounded final prose) and compares:
   - A Naive "Vanity Eval" (catches only 20% of bugs -> dangerous false confidence)
   - An Enterprise 4-Layer Contract Eval (catches 100% of injected bugs)
2. LLM Judge Calibration & Rogan-Gladen Mathematical Bias Correction:
   Computes True Positive Rate (TPR / Sensitivity), True Negative Rate (TNR / Specificity),
   Cohen's Kappa (inter-rater agreement vs. Human Gold Set), and corrects raw Judge pass rates
   for known judge bias.
"""

import json
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class AgentExecutionTrace:
    """Represents a captured end-to-end execution across Agent + Skill + MCP."""
    trace_id: str
    mutant_description: str
    is_actually_defective: bool
    user_query: str
    expected_skill_uri: str
    activated_skill_uri: str
    tool_called: str
    tool_args: dict[str, Any]
    tool_result: dict[str, Any]
    sandbox_order_age_days: int
    final_agent_response: str


# --- Evaluators Under Meta-Test ---

def naive_vanity_evaluator(trace: AgentExecutionTrace) -> bool:
    """
    Anti-Pattern Evaluator: Only checks if the tool arguments are valid dict/JSON
    and if the agent's final response sounds polite.
    Returns True (PASS) or False (FAIL).
    """
    has_dict_args = isinstance(trace.tool_args, dict) and len(trace.tool_args) > 0
    sounds_polite = any(w in trace.final_agent_response.lower() for w in ["refund", "happy", "processed", "help"])
    return has_dict_args and sounds_polite


def enterprise_layered_evaluator(trace: AgentExecutionTrace) -> bool:
    """
    4-Layer Contract Evaluator across Agent + Skill + MCP:
    - Layer 1: Did the agent activate the expected Skill URI?
    - Layer 2: Provenance check (was `order_id` actually grounded in the user query?)
    - Layer 3: Policy & SEP-1303 check (no refund if days_old > 30)
    - Layer 4: Grounded synthesis check (agent cannot claim success if tool returned isError=True)
    """
    # Layer 1: Skill routing check
    if trace.activated_skill_uri != trace.expected_skill_uri:
        return False

    # Layer 2: Argument provenance (prevent hallucinated IDs)
    order_id = str(trace.tool_args.get("order_id", ""))
    if order_id not in trace.user_query:
        return False

    # Layer 3: Business invariant / policy check
    if trace.tool_called == "issue_refund" and trace.sandbox_order_age_days > 30:
        return False

    # Layer 4: Faithfulness / Grounded synthesis check
    tool_failed = trace.tool_result.get("isError", False)
    claims_success = "processed" in trace.final_agent_response.lower() or "approved" in trace.final_agent_response.lower()
    if tool_failed and claims_success:
        return False

    return True


def run_eval_mutation_testing(
    evaluator_fn: Callable[[AgentExecutionTrace], bool], mutants: list[AgentExecutionTrace]
) -> dict[str, Any]:
    """
    Inject known-bad mutants into an Evaluator.
    An evaluator KILLS a mutant if it accurately marks the defective trace as FAIL (False).
    """
    killed = 0
    missed_mutants = []
    for m in mutants:
        eval_passed = evaluator_fn(m)
        if m.is_actually_defective and not eval_passed:
            killed += 1
        elif m.is_actually_defective and eval_passed:
            missed_mutants.append(m.mutant_description)

    kill_rate = killed / max(1, len(mutants))
    return {
        "mutants_injected": len(mutants),
        "mutants_killed": killed,
        "mutation_kill_score": f"{round(kill_rate * 100, 1)}%",
        "missed_defects": missed_mutants,
        "verdict": "✅ TRUSTWORTHY EVAL (>= 90%)" if kill_rate >= 0.90 else "❌ VANITY EVAL (Blind to real bugs!)",
    }


def calibrate_judge_against_human_gold(
    gold_labels: list[bool], judge_predictions: list[bool], raw_unlabeled_pass_rate: float
) -> dict[str, Any]:
    """
    Compute TPR (Sensitivity), TNR (Specificity), Cohen's Kappa, and the
    Rogan-Gladen bias-corrected true pass rate:
        p_true = clip((p_obs + TNR - 1) / (TPR + TNR - 1), 0, 1)
    """
    tp = sum(1 for g, j in zip(gold_labels, judge_predictions) if g and j)
    fn = sum(1 for g, j in zip(gold_labels, judge_predictions) if g and not j)
    tn = sum(1 for g, j in zip(gold_labels, judge_predictions) if not g and not j)
    fp = sum(1 for g, j in zip(gold_labels, judge_predictions) if not g and j)

    total = len(gold_labels)
    tpr = tp / max(1, tp + fn)
    tnr = tn / max(1, tn + fp)

    # Cohen's Kappa
    p_o = (tp + tn) / total
    p_yes_gold = (tp + fn) / total
    p_yes_judge = (tp + fp) / total
    p_e = (p_yes_gold * p_yes_judge) + ((1 - p_yes_gold) * (1 - p_yes_judge))
    kappa = (p_o - p_e) / max(1e-9, (1 - p_e))

    # Rogan-Gladen Bias Correction
    denom = tpr + tnr - 1.0
    if denom > 0:
        corrected_pass_rate = max(0.0, min(1.0, (raw_unlabeled_pass_rate + tnr - 1.0) / denom))
    else:
        corrected_pass_rate = raw_unlabeled_pass_rate

    return {
        "calibration_set_size": total,
        "TPR_sensitivity": round(tpr, 3),
        "TNR_specificity": round(tnr, 3),
        "cohens_kappa": round(kappa, 3),
        "raw_observed_pass_rate": f"{round(raw_unlabeled_pass_rate * 100, 1)}%",
        "rogan_gladen_true_pass_rate": f"{round(corrected_pass_rate * 100, 1)}%",
        "calibration_status": "✅ CALIBRATED (Kappa >= 0.80)" if kappa >= 0.80 else "⚠️ UNCALIBRATED JUDGE",
    }


def build_synthetic_mutants() -> list[AgentExecutionTrace]:
    expected_uri = "skill://shop/refund-processing/SKILL.md"
    return [
        AgentExecutionTrace(
            trace_id="mut_01",
            mutant_description="Mutant 1 (Skill Routing Bug): Activated 'cancel-subscription' instead of 'refund-processing'",
            is_actually_defective=True,
            user_query="Please refund order ord_901 for $250",
            expected_skill_uri=expected_uri,
            activated_skill_uri="skill://shop/cancel-subscription/SKILL.md",
            tool_called="cancel_sub",
            tool_args={"order_id": "ord_901"},
            tool_result={"isError": False},
            sandbox_order_age_days=10,
            final_agent_response="I would be happy to help! Your refund request is processed.",
        ),
        AgentExecutionTrace(
            trace_id="mut_02",
            mutant_description="Mutant 2 (Hallucinated Arg): Invented order_id 'ord_999' not in user query",
            is_actually_defective=True,
            user_query="Please refund my recent order for $250",
            expected_skill_uri=expected_uri,
            activated_skill_uri=expected_uri,
            tool_called="issue_refund",
            tool_args={"order_id": "ord_999", "amount": 250.0},
            tool_result={"isError": False},
            sandbox_order_age_days=10,
            final_agent_response="Your refund for ord_999 has been processed!",
        ),
        AgentExecutionTrace(
            trace_id="mut_03",
            mutant_description="Mutant 3 (Policy Breach): Issued refund on 95-day-old order (violates 30-day rule)",
            is_actually_defective=True,
            user_query="Please refund order ord_404",
            expected_skill_uri=expected_uri,
            activated_skill_uri=expected_uri,
            tool_called="issue_refund",
            tool_args={"order_id": "ord_404", "amount": 800.0},
            tool_result={"isError": False},
            sandbox_order_age_days=95,
            final_agent_response="Happy to help, your refund for ord_404 has been processed.",
        ),
        AgentExecutionTrace(
            trace_id="mut_04",
            mutant_description="Mutant 4 (Ungrounded Hallucination): Tool returned isError=True, but Agent claimed refund succeeded",
            is_actually_defective=True,
            user_query="Please refund order ord_901",
            expected_skill_uri=expected_uri,
            activated_skill_uri=expected_uri,
            tool_called="issue_refund",
            tool_args={"order_id": "ord_901", "amount": 250.0},
            tool_result={"isError": True, "content": [{"type": "text", "text": "Payment gateway timeout"}]},
            sandbox_order_age_days=10,
            final_agent_response="Your refund for ord_901 has been processed and approved!",
        ),
        AgentExecutionTrace(
            trace_id="mut_05",
            mutant_description="Mutant 5 (Empty Tool Call): Agent skipped calling MCP tool and replied with empty args",
            is_actually_defective=True,
            user_query="Please refund order ord_901",
            expected_skill_uri=expected_uri,
            activated_skill_uri=expected_uri,
            tool_called="none",
            tool_args={},
            tool_result={"isError": True},
            sandbox_order_age_days=10,
            final_agent_response="Your refund has been processed!",
        ),
    ]


def run_demo():
    print("=" * 78)
    print("Eval Engineering 03: Measuring Eval Quality (Meta-Evaluation)")
    print("=" * 78)

    mutants = build_synthetic_mutants()

    print("\n1️⃣  Meta-Eval Mechanism 1: Mutation Testing (Defect Injection Score)")
    print("-" * 78)
    vanity_report = run_eval_mutation_testing(naive_vanity_evaluator, mutants)
    layered_report = run_eval_mutation_testing(enterprise_layered_evaluator, mutants)

    print("A. Naive 'Vanity Evaluator' (Checks only JSON format & polite keywords):")
    print(json.dumps(vanity_report, indent=2))

    print("\nB. Enterprise 4-Layer Contract Evaluator (Checks Routing, Provenance, Policy, Grounding):")
    print(json.dumps(layered_report, indent=2))

    print("\n2️⃣  Meta-Eval Mechanism 2: Judge Calibration & Rogan-Gladen Bias Correction")
    print("-" * 78)
    # 20 human-labeled gold traces (10 True Pass, 10 True Fail)
    human_gold = [True] * 10 + [False] * 10
    # Judge has 90% TPR (9/10 true passes) and 90% TNR (9/10 true fails)
    calibrated_judge_preds = [True] * 9 + [False] * 1 + [False] * 9 + [True] * 1

    calibration = calibrate_judge_against_human_gold(
        gold_labels=human_gold,
        judge_predictions=calibrated_judge_preds,
        raw_unlabeled_pass_rate=0.82,
    )
    print(json.dumps(calibration, indent=2))


if __name__ == "__main__":
    run_demo()
