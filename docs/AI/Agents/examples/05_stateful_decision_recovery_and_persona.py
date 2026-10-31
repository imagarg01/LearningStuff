"""
Pattern 5 (Deep-Dive): Decision Physics, Saga Checkpoints, Bi-Temporal Memory & RFC 8693 Personas
=================================================================================================
Mapped to Agent Learning Path: Module 09 (09_Durable_State_Memory_and_Persona_Architecture.md)

Demonstrates nth-level implementations of the 4 multi-step agent engineering pillars:
1. Compounding Decision Math (p^N Collapse vs. Step Verifier Recovery) & Markov Decision Cassettes:
   - Computes trajectory reliability with and without local SEP-1303 step verifiers
   - Evaluates per-node Markov Decision Cassettes to isolate exact node drift on model upgrades
2. Event-Sourced Checkpoint Tree, Time-Travel Forking, & LIFO Saga Compensation:
   - Persists parent-linked checkpoints (`parent_checkpoint_id`) with deterministic idempotency keys
   - Unwinds external side-effects via a LIFO Saga `compensation_stack` before forking a clean branch
3. CoALA / Zep 4-Store Cross-Run Memory (Episodic Receipts + Bi-Temporal Knowledge Graph):
   - Writes structured Episodic Run Receipts with `do_not_repeat` guards
   - Maintains Bi-Temporal Semantic Triples (`valid_from`, `valid_until`) so changing user facts
     across runs never cause contradictory RAG retrievals
4. Dual-Plane Caller Persona Architecture (IETF RFC 8693 OBO Token + Cognitive Persona Contract):
   - Enforces Plane-1 Cryptographic Authority (skill namespace filtering, row-level scoping, MRTR limits)
   - Applies Plane-2 Cognitive Persona formatting across Customer, Product Owner, SRE, and CI Bot callers
"""

import copy
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Any


# ============================================================================
# 1. DECISION COLLAPSE PHYSICS (p^N) & MARKOV DECISION CASSETTES
# ============================================================================

def compute_trajectory_reliability(single_step_p: float, num_steps: int, max_verifier_attempts: int = 3) -> dict[str, Any]:
    """
    Compare unguarded trajectory reliability p^N against locally verified trajectory reliability:
        P_verified = (1 - (1 - p)^R)^N
    """
    unguarded = single_step_p ** num_steps
    effective_step_p = 1.0 - ((1.0 - single_step_p) ** max_verifier_attempts)
    locally_verified = effective_step_p ** num_steps
    return {
        "steps_N": num_steps,
        "single_step_accuracy_p": single_step_p,
        "unguarded_p_power_N": f"{round(unguarded * 100, 1)}%",
        "with_step_verifiers_and_sep1303_R3": f"{round(locally_verified * 100, 1)}%",
        "reliability_gain": f"+{round((locally_verified - unguarded) * 100, 1)}%",
    }


@dataclass
class MarkovDecisionCassette:
    """Frozen checkpoint state s_{k-1}^* entering decision node D_k."""
    node_id: str
    frozen_pre_state: dict[str, Any]
    expected_action: dict[str, Any]


def evaluate_markov_cassettes(
    cassettes: list[MarkovDecisionCassette],
    baseline_pass3: dict[str, float],
    candidate_pass3: dict[str, float],
) -> dict[str, Any]:
    """Compute per-node Pass^3 delta between Model_v1 and Model_v2 in parallel."""
    deltas = {}
    drifted_nodes = []
    for cas in cassettes:
        nid = cas.node_id
        p1 = baseline_pass3.get(nid, 1.0)
        p2 = candidate_pass3.get(nid, 1.0)
        delta = round(p2 - p1, 3)
        deltas[nid] = {"Model_v1_Pass^3": p1, "Model_v2_Pass^3": p2, "delta": delta}
        if delta < -0.05:
            drifted_nodes.append(nid)

    return {
        "per_node_pass3_comparison": deltas,
        "isolated_regression_nodes": drifted_nodes,
        "gate_verdict": "✅ SAFE TO SWAP MODEL" if not drifted_nodes else f"🛑 BLOCK: Fix drifted node(s) {drifted_nodes}",
    }


# ============================================================================
# 2. DURABLE CHECKPOINT TREE, TIME-TRAVEL FORKING & LIFO SAGA COMPENSATION
# ============================================================================

@dataclass
class CheckpointNode:
    thread_id: str
    checkpoint_id: str
    parent_checkpoint_id: str
    node_name: str
    channel_values: dict[str, Any]
    compensation_stack: list[dict[str, Any]]
    idempotency_key: str


class DurableSagaCheckpointer:
    """
    Event-sourced checkpoint tree supporting:
    - Deterministic idempotency keys per (thread_id, checkpoint_id, node_name)
    - LIFO Saga compensation unwinding when rewinding across external side-effects
    - Non-destructive branch forking
    """

    def __init__(self):
        self.tree: dict[str, CheckpointNode] = {}
        self.compensated_log: list[dict[str, Any]] = []

    def commit_checkpoint(
        self,
        thread_id: str,
        checkpoint_id: str,
        parent_id: str,
        node_name: str,
        state: dict[str, Any],
        compensating_action: dict[str, Any] | None = None,
    ) -> CheckpointNode:
        parent_stack = (
            copy.deepcopy(self.tree[parent_id].compensation_stack) if parent_id in self.tree else []
        )
        if compensating_action:
            parent_stack.append(compensating_action)

        idem_raw = f"{thread_id}:{checkpoint_id}:{node_name}"
        idem_key = "idem_" + hashlib.sha256(idem_raw.encode("utf-8")).hexdigest()[:16]

        node = CheckpointNode(
            thread_id=thread_id,
            checkpoint_id=checkpoint_id,
            parent_checkpoint_id=parent_id,
            node_name=node_name,
            channel_values=copy.deepcopy(state),
            compensation_stack=parent_stack,
            idempotency_key=idem_key,
        )
        self.tree[checkpoint_id] = node
        return node

    def rewind_unwind_saga_and_fork(
        self,
        failed_checkpoint_id: str,
        target_good_checkpoint_id: str,
        new_fork_checkpoint_id: str,
        state_patch: dict[str, Any],
    ) -> CheckpointNode:
        """
        1. Unwind any external mutations registered between `target_good_checkpoint_id`
           and `failed_checkpoint_id` in LIFO order.
        2. Fork a new checkpoint branch from `target_good_checkpoint_id` with `state_patch`.
        """
        failed_node = self.tree[failed_checkpoint_id]
        target_node = self.tree[target_good_checkpoint_id]

        # Calculate compensating actions that must be executed to undo failed branch side-effects
        target_depth = len(target_node.compensation_stack)
        to_unwind = failed_node.compensation_stack[target_depth:]
        for comp in reversed(to_unwind):
            self.compensated_log.append({"executed_compensation": comp, "from_checkpoint": failed_checkpoint_id})

        patched_state = copy.deepcopy(target_node.channel_values)
        patched_state.update(state_patch)
        return self.commit_checkpoint(
            thread_id=target_node.thread_id,
            checkpoint_id=new_fork_checkpoint_id,
            parent_id=target_good_checkpoint_id,
            node_name=f"{target_node.node_name}_fork_recovery",
            state=patched_state,
        )


# ============================================================================
# 3. CoALA / ZEP 4-STORE CROSS-RUN MEMORY (EPISODIC + BI-TEMPORAL GRAPH)
# ============================================================================

@dataclass
class EpisodicReceipt:
    episode_id: str
    thread_id: str
    decisions_committed: list[str]
    open_blocker: str
    do_not_repeat_calls: list[str]


@dataclass
class BiTemporalSemanticEdge:
    subject: str
    predicate: str
    object_val: str
    valid_from: str
    valid_until: str | None = None


class CoALACrossRunMemoryEngine:
    """
    Manages Cross-Run Episodic Receipts and a Bi-Temporal Semantic Knowledge Graph
    so changing facts across runs never pollute or contradict future prompts.
    """

    def __init__(self):
        self.episodes: dict[str, list[EpisodicReceipt]] = {}
        self.knowledge_graph: list[BiTemporalSemanticEdge] = []

    def upsert_temporal_fact(self, subject: str, predicate: str, new_val: str, timestamp: str):
        """Invalidate any existing active edge for (subject, predicate) and insert new active edge."""
        for edge in self.knowledge_graph:
            if edge.subject == subject and edge.predicate == predicate and edge.valid_until is None:
                edge.valid_until = timestamp
        self.knowledge_graph.append(
            BiTemporalSemanticEdge(
                subject=subject,
                predicate=predicate,
                object_val=new_val,
                valid_from=timestamp,
                valid_until=None,
            )
        )

    def record_episodic_receipt(self, user_id: str, receipt: EpisodicReceipt):
        self.episodes.setdefault(user_id, []).append(receipt)

    def compile_cross_run_context(self, user_id: str) -> dict[str, Any]:
        """Return ONLY currently valid semantic facts (`valid_until is None`) + recent episodic receipts."""
        active_facts = {
            f"{e.subject}.{e.predicate}": e.object_val
            for e in self.knowledge_graph
            if e.subject == user_id and e.valid_until is None
        }
        archived_facts = [
            f"{e.predicate}={e.object_val} (expired {e.valid_until})"
            for e in self.knowledge_graph
            if e.subject == user_id and e.valid_until is not None
        ]
        recent_episodes = [asdict(ep) for ep in self.episodes.get(user_id, [])[-3:]]
        return {
            "active_bi_temporal_facts": active_facts,
            "superseded_historical_facts_excluded": archived_facts,
            "recent_episodic_receipts": recent_episodes,
        }


# ============================================================================
# 4. DUAL-PLANE CALLER PERSONA RESOLUTION (RFC 8693 OBO + COGNITIVE CONTRACT)
# ============================================================================

@dataclass
class RFC8693CallerPersona:
    """
    Plane 1: Cryptographic OAuth 2.1 / RFC 8693 On-Behalf-Of Claims (`sub`, `act`, `scope`)
    Plane 2: Cognitive Persona Contract (Model Tier, Output Schema, Escalation Policy)
    """
    sub: str
    act_agent: str
    roles: list[str]
    allowed_skill_namespaces: list[str]
    max_autonomous_refund_usd: float
    persona_name: str
    trigger_channel: str
    recommended_model_tier: str
    output_mode: str


ALL_ENTERPRISE_SKILLS = [
    "skill://shop/refund-processing/SKILL.md",
    "skill://devops/k8s-rollback/SKILL.md",
    "skill://sdd/refine-intent/SKILL.md",
]


def resolve_and_execute_for_persona(persona: RFC8693CallerPersona, refund_amount: float) -> dict[str, Any]:
    # Plane 1 Enforcement: Filter visible skills by cryptographic namespace scope
    visible_skills = [
        s for s in ALL_ENTERPRISE_SKILLS if any(s.startswith(ns) for ns in persona.allowed_skill_namespaces)
    ]
    requires_mrtr_approval = refund_amount > persona.max_autonomous_refund_usd

    # Plane 2 Adaptation: Format output according to the caller's Cognitive Persona Contract
    if persona.output_mode == "customer_empathetic_markdown":
        rendered = (
            f"Hi! I've submitted your ${refund_amount:.2f} refund request for supervisor approval. "
            "You'll receive an email confirmation shortly."
        )
    elif persona.output_mode == "sre_diagnostic_telemetry":
        rendered = (
            f"[SRE-OPS] sub={persona.sub} act={persona.act_agent} "
            f"auto_exec={not requires_mrtr_approval} amount=${refund_amount:.2f}"
        )
    else:
        rendered = json.dumps(
            {
                "caller_sub": persona.sub,
                "autonomous_execution": not requires_mrtr_approval,
                "amount_usd": refund_amount,
            }
        )

    return {
        "persona": persona.persona_name,
        "plane1_visible_skills": visible_skills,
        "plane1_mrtr_gate_triggered": requires_mrtr_approval,
        "plane2_model_tier_routed": persona.recommended_model_tier,
        "plane2_rendered_output": rendered,
    }


def run_demo():
    print("=" * 80)
    print("Module 09 Deep-Dive: Decision Physics, Saga Checkpoints, Memory & Personas")
    print("=" * 80)

    # 1. Mathematical p^N Collapse vs. Step-Verifier Recovery + Markov Cassettes
    print("\n1️⃣  Deep-Dive 1: Compounding Decision Physics (p^N) & Markov Node Cassettes")
    print("-" * 80)
    math_comparison = compute_trajectory_reliability(single_step_p=0.85, num_steps=10, max_verifier_attempts=3)
    print("10-Step Trajectory Math (when single-step model accuracy p = 85%):")
    print(json.dumps(math_comparison, indent=2))

    cassettes = [
        MarkovDecisionCassette("D1_ClassifyIntent", {"q": "Refund ord_901"}, {"skill": "refund"}),
        MarkovDecisionCassette("D2_VerifyWindow", {"days": 12}, {"eligible": True}),
        MarkovDecisionCassette("D3_ComputeTax", {"region": "EU"}, {"vat_refund": True}),
    ]
    cassette_eval = evaluate_markov_cassettes(
        cassettes,
        baseline_pass3={"D1_ClassifyIntent": 1.0, "D2_VerifyWindow": 0.98, "D3_ComputeTax": 0.97},
        candidate_pass3={"D1_ClassifyIntent": 1.0, "D2_VerifyWindow": 0.99, "D3_ComputeTax": 0.71},
    )
    print("\nMarkov Decision Cassette Shadow Eval (Model_v1 vs. Model_v2):")
    print(json.dumps(cassette_eval, indent=2))

    # 2. Event-Sourced Checkpoint Tree & LIFO Saga Compensation Unwinding
    print("\n2️⃣  Deep-Dive 2: Durable Checkpoint Tree, Saga Compensation & Branch Forking")
    print("-" * 80)
    saga = DurableSagaCheckpointer()
    cp1 = saga.commit_checkpoint(
        thread_id="wf_800",
        checkpoint_id="cp_01",
        parent_id="root",
        node_name="D1_VerifyOrder",
        state={"order_id": "ord_901", "verified": True},
    )
    cp2_bad = saga.commit_checkpoint(
        thread_id="wf_800",
        checkpoint_id="cp_02_bad",
        parent_id="cp_01",
        node_name="D2_ReserveReplacementStock",
        state={"order_id": "ord_901", "verified": True, "reserved_sku": "SKU-WRONG-99"},
        compensating_action={"tool": "release_inventory_reservation", "args": {"sku": "SKU-WRONG-99"}},
    )
    cp3_fork = saga.rewind_unwind_saga_and_fork(
        failed_checkpoint_id="cp_02_bad",
        target_good_checkpoint_id="cp_01",
        new_fork_checkpoint_id="cp_02_fork",
        state_patch={"action": "issue_monetary_refund_only"},
    )
    print(f"   • Committed {cp1.checkpoint_id} (idem_key={cp1.idempotency_key})")
    print(f"   • Bad branch {cp2_bad.checkpoint_id} mutated inventory -> Unwound LIFO Saga:")
    print(f"     {json.dumps(saga.compensated_log)}")
    print(f"   • Forked clean branch {cp3_fork.checkpoint_id} from parent={cp3_fork.parent_checkpoint_id}:")
    print(f"     State={cp3_fork.channel_values}")

    # 3. CoALA / Zep Bi-Temporal Cross-Run Memory
    print("\n3️⃣  Deep-Dive 3: CoALA Episodic Receipts & Bi-Temporal Semantic Graph")
    print("-" * 80)
    mem = CoALACrossRunMemoryEngine()
    mem.upsert_temporal_fact("user:alice", "shipping_city", "Seattle", timestamp="2025-01-10")
    mem.upsert_temporal_fact("user:alice", "shipping_city", "Austin", timestamp="2026-10-31")
    mem.record_episodic_receipt(
        "user:alice",
        EpisodicReceipt(
            episode_id="ep_mon_01",
            thread_id="run_101",
            decisions_committed=["Verified ord_901 (12d old)", "Issued RMA-7741"],
            open_blocker="Awaiting carrier scan on RMA-7741",
            do_not_repeat_calls=["create_return_label(ord_901)"],
        ),
    )
    compiled_ctx = mem.compile_cross_run_context("user:alice")
    print(json.dumps(compiled_ctx, indent=2))

    # 4. Dual-Plane RFC 8693 Caller Persona Resolution
    print("\n4️⃣  Deep-Dive 4: Dual-Plane Caller Persona Resolution (RFC 8693 + Cognitive)")
    print("-" * 80)
    personas = [
        RFC8693CallerPersona(
            sub="user:alice",
            act_agent="agent:support-v2",
            roles=["customer"],
            allowed_skill_namespaces=["skill://shop/"],
            max_autonomous_refund_usd=100.0,
            persona_name="End_Customer (Web Chat)",
            trigger_channel="web_widget",
            recommended_model_tier="flash",
            output_mode="customer_empathetic_markdown",
        ),
        RFC8693CallerPersona(
            sub="sre:bob",
            act_agent="agent:ops-v2",
            roles=["sre_oncall"],
            allowed_skill_namespaces=["skill://devops/", "skill://shop/"],
            max_autonomous_refund_usd=1000.0,
            persona_name="SRE_OnCall (Slack Ops)",
            trigger_channel="slack_incident",
            recommended_model_tier="flash",
            output_mode="sre_diagnostic_telemetry",
        ),
        RFC8693CallerPersona(
            sub="bot:github_ci",
            act_agent="agent:ci-runner",
            roles=["ci_pipeline"],
            allowed_skill_namespaces=["skill://sdd/", "skill://devops/"],
            max_autonomous_refund_usd=0.0,
            persona_name="Headless_CI_Pipeline (Webhook)",
            trigger_channel="github_actions",
            recommended_model_tier="frontier",
            output_mode="strict_json_schema",
        ),
    ]
    for p in personas:
        res = resolve_and_execute_for_persona(p, refund_amount=250.0)
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    run_demo()
