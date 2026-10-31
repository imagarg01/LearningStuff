"""
Skill Engineering 02: Model Quality Dependency & Cognitive Offloading Benchmark
===============================================================================
Addresses Question 2:
"How much does a skill depend upon the quality of the model?"

Demonstrates:
1. The Cognitive Load Analyzer:
   Quantifies a skill's Model Dependency Score based on:
   - Instruction branching depth (if/else rules inside SKILL.md)
   - In-prompt arithmetic / date math requirements
   - Micro-tool sequence length (multi-step state orchestration by the LLM)
   - JSON Schema nesting depth and polymorphism
2. Cross-Tier Degradation Benchmark (Frontier vs. Flash vs. Edge SLM):
   Shows why prompt-heavy micro-skills break on Flash/SLM models, and how refactoring via
   Cognitive Offloading (moving branching, date math, and state orchestration into the
   deterministic MCP tool handler) lifts Flash/SLM accuracy to ~100%.
"""

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class SkillArchitectureProfile:
    name: str
    declared_min_model_tier: str
    prompt_branching_conditions: int     # Number of if/else rules the LLM must evaluate in-prompt
    requires_mental_date_or_math: bool   # Whether LLM must calculate date windows / percentages itself
    sequential_micro_tools_required: int # Number of chained tool calls required to finish 1 task
    schema_nesting_depth: int            # JSON Schema object nesting depth
    has_sep1303_recovery_hints: bool     # Whether tool returns actionable self-correction hints


def compute_cognitive_load_score(profile: SkillArchitectureProfile) -> dict[str, Any]:
    """
    Calculate the Cognitive Load Score (0-100) and minimum recommended model tier.
    Higher score = heavier reliance on Frontier LLM reasoning.
    """
    score = 0
    score += profile.prompt_branching_conditions * 8
    score += 25 if profile.requires_mental_date_or_math else 0
    score += max(0, profile.sequential_micro_tools_required - 1) * 12
    score += max(0, profile.schema_nesting_depth - 1) * 10
    if not profile.has_sep1303_recovery_hints:
        score += 15

    score = min(100, score)
    if score >= 55:
        recommended_tier = "frontier"
    elif score >= 25:
        recommended_tier = "flash"
    else:
        recommended_tier = "slm"

    return {
        "skill": profile.name,
        "cognitive_load_score": score,
        "declared_min_tier": profile.declared_min_model_tier,
        "recommended_min_tier": recommended_tier,
        "tier_alignment_ok": profile.declared_min_model_tier == recommended_tier,
    }


@dataclass
class ModelTierSimulator:
    """
    Deterministic simulation of model capability limits across 3 tiers:
    - frontier (e.g., Gemini Pro / Claude Opus / GPT-4.5)
    - flash    (e.g., Gemini Flash / Claude Haiku / GPT-4o-mini)
    - slm      (e.g., Local 8B-14B open-weights model)
    """
    tier_name: str
    max_reliable_branching: int
    can_do_mental_date_math: bool
    max_reliable_tool_chain: int
    max_reliable_schema_depth: int
    can_recover_with_sep1303: bool
    relative_cost_per_1k_tokens: float


MODEL_TIERS = [
    ModelTierSimulator(
        tier_name="frontier",
        max_reliable_branching=8,
        can_do_mental_date_math=True,
        max_reliable_tool_chain=5,
        max_reliable_schema_depth=4,
        can_recover_with_sep1303=True,
        relative_cost_per_1k_tokens=10.0,
    ),
    ModelTierSimulator(
        tier_name="flash",
        max_reliable_branching=3,
        can_do_mental_date_math=False,
        max_reliable_tool_chain=2,
        max_reliable_schema_depth=2,
        can_recover_with_sep1303=True,
        relative_cost_per_1k_tokens=1.0,
    ),
    ModelTierSimulator(
        tier_name="slm",
        max_reliable_branching=1,
        can_do_mental_date_math=False,
        max_reliable_tool_chain=1,
        max_reliable_schema_depth=1,
        can_recover_with_sep1303=True,
        relative_cost_per_1k_tokens=0.15,
    ),
]


def evaluate_skill_across_models(
    profile: SkillArchitectureProfile, scenarios: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Evaluate a skill profile across all 3 model tiers on realistic enterprise scenarios."""
    results = {}
    for model in MODEL_TIERS:
        passed = 0
        failure_reasons = []
        for sc in scenarios:
            failed = False
            if sc["branches_active"] > model.max_reliable_branching and profile.prompt_branching_conditions > model.max_reliable_branching:
                failed = True
                failure_reasons.append(f"{sc['id']}: Failed deep prompt branching ({profile.prompt_branching_conditions} rules)")
            elif sc["needs_date_math"] and profile.requires_mental_date_or_math and not model.can_do_mental_date_math:
                failed = True
                failure_reasons.append(f"{sc['id']}: Hallucinated 30-day business-day window arithmetic")
            elif profile.sequential_micro_tools_required > model.max_reliable_tool_chain:
                failed = True
                failure_reasons.append(f"{sc['id']}: Dropped state mid-chain ({profile.sequential_micro_tools_required} micro-tools)")
            elif profile.schema_nesting_depth > model.max_reliable_schema_depth:
                failed = True
                failure_reasons.append(f"{sc['id']}: Malformed nested JSON schema (depth={profile.schema_nesting_depth})")

            if not failed:
                passed += 1

        pass_rate = passed / len(scenarios)
        # Pass^3 = (pass_rate)^3
        pass_power_3 = round(pass_rate ** 3, 3)
        results[model.tier_name] = {
            "single_run_accuracy": f"{round(pass_rate * 100, 1)}%",
            "pass_power_3": pass_power_3,
            "relative_cost_multiplier": f"{model.relative_cost_per_1k_tokens}x",
            "sample_failures": failure_reasons[:2],
        }
    return results


def run_demo():
    print("=" * 78)
    print("Skill Engineering 02: Model Quality Dependency & Cognitive Offloading")
    print("=" * 78)

    # Golden scenarios representing enterprise edge cases
    scenarios = [
        {"id": "SC-1 (Standard Refund)", "branches_active": 1, "needs_date_math": False},
        {"id": "SC-2 (Boundary 30-Day Leap Year Check)", "branches_active": 2, "needs_date_math": True},
        {"id": "SC-3 (VIP Partial Prorated Refund)", "branches_active": 4, "needs_date_math": True},
        {"id": "SC-4 (Cross-Border Tax + Restocking Fee)", "branches_active": 6, "needs_date_math": True},
    ]

    # Design A: Prompt-Heavy Micro-Skill Architecture (High Model Dependency)
    fragile_skill = SkillArchitectureProfile(
        name="Design A: Prompt-Heavy Micro-Skill (Logic in SKILL.md)",
        declared_min_model_tier="frontier",
        prompt_branching_conditions=6,
        requires_mental_date_or_math=True,
        sequential_micro_tools_required=4,  # get_user -> get_order -> calc_tax -> issue_refund
        schema_nesting_depth=3,
        has_sep1303_recovery_hints=False,
    )

    # Design B: Cognitively Offloaded Macro-Skill (Logic in Deterministic MCP Runtime)
    offloaded_skill = SkillArchitectureProfile(
        name="Design B: Cognitively Offloaded Macro-Skill (Logic in MCP Handler)",
        declared_min_model_tier="slm",
        prompt_branching_conditions=1,      # Only "Call process_refund; if disputed, read reference"
        requires_mental_date_or_math=False, # Python handler computes exact date delta & prorated math
        sequential_micro_tools_required=1,  # Single macro-tool: process_refund(order_id, reason_code)
        schema_nesting_depth=1,             # Flat 3-field schema
        has_sep1303_recovery_hints=True,
    )

    print("\n1️⃣  Cognitive Load & Model Dependency Analysis")
    print("-" * 78)
    for prof in (fragile_skill, offloaded_skill):
        analysis = compute_cognitive_load_score(prof)
        print(json.dumps(analysis, indent=2))

    print("\n2️⃣  Cross-Model Tier Benchmark (Frontier vs. Flash vs. Edge SLM)")
    print("-" * 78)
    for prof in (fragile_skill, offloaded_skill):
        print(f"\n📊 Evaluating: {prof.name}")
        matrix = evaluate_skill_across_models(prof, scenarios)
        print(json.dumps(matrix, indent=2))

    print("\n💡 Key Architectural Takeaway:")
    print("   • Design A forces you to pay 10x Frontier Model costs because date math, branching,")
    print("     and 4-step micro-tool chaining live in SKILL.md prose (failing on Flash & SLMs).")
    print("   • Design B moves date math, policy branching, and DB joins into deterministic Python")
    print("     inside the MCP Server, achieving 100% Pass^3 across Frontier, Flash, AND SLMs!")


if __name__ == "__main__":
    run_demo()
