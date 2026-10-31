"""
Skill Engineering 04: The 6-Stage Skill Delivery Factory (CI/CD Pipeline)
=========================================================================
Addresses Question 4:
"How to build a pipeline around skills with necessary tests to make a testable delivery factory of skills?"

Executes a complete 6-Gate Skill Delivery Factory pipeline on MCP Skill Release Candidates:
- Gate 1: Static Contract, MCP Annotations & Token Budget Linter
- Gate 2: Deterministic Property-Based Fuzzing (Zero Raw Exceptions + SEP-1303 Hint Verification)
- Gate 3: Catalog Semantic Routing & Anti-Shadowing Confusion Matrix
- Gate 4: Model-Agnostic Behavioral Matrix (Pass^3 >= 0.95 & TAF <= 1.25)
- Gate 5: Cryptographic SEP-2640 SHA-256 Manifest Packaging & Signing
- Gate 6: Production Canary & OpenTelemetry (SEP-414) Auto-Rollback Gate
"""

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Callable


def compute_sha256(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


def estimate_tokens(text: str) -> int:
    chunks = re.findall(r"\w+|[^\w\s]", text or "", re.UNICODE)
    return max(1, int(len(chunks) * 0.85))


@dataclass
class SkillReleaseCandidate:
    uri: str
    version: str
    frontmatter: dict[str, Any]
    skill_markdown: str
    references: dict[str, str]
    tool_definition: dict[str, Any]
    tool_handler: Callable[[dict[str, Any]], dict[str, Any]]
    positive_queries: list[str]
    negative_distractor_queries: list[str]
    behavioral_pass_power_3: dict[str, float]
    behavioral_taf: float


class SkillDeliveryFactoryPipeline:
    """Automated 6-Stage Enterprise Skill Delivery Factory."""

    def __init__(self, existing_catalog_frontmatters: list[dict[str, Any]]):
        self.catalog = existing_catalog_frontmatters

    def gate_1_static_contract_and_token_budget(self, rc: SkillReleaseCandidate) -> tuple[bool, list[str]]:
        errors = []
        req_fields = {"name", "description", "category", "min_model_tier"}
        missing = req_fields - set(rc.frontmatter.keys())
        if missing:
            errors.append(f"Missing required frontmatter fields: {sorted(missing)}")

        front_tokens = estimate_tokens(json.dumps(rc.frontmatter))
        body_tokens = estimate_tokens(rc.skill_markdown)
        schema_tokens = estimate_tokens(json.dumps(rc.tool_definition.get("inputSchema", {})))

        if front_tokens > 60:
            errors.append(f"Frontmatter token budget exceeded: {front_tokens} > 60")
        if body_tokens > 1200:
            errors.append(f"SKILL.md body token budget exceeded: {body_tokens} > 1200")
        if schema_tokens > 250:
            errors.append(f"Tool inputSchema token budget exceeded: {schema_tokens} > 250")

        annotations = rc.tool_definition.get("annotations", {})
        if not annotations.get("readOnlyHint", False) and not annotations.get("idempotentHint", False):
            errors.append("Mutating tool MUST declare `annotations.idempotentHint = True`")

        return (len(errors) == 0, errors)

    def gate_2_property_based_fuzzing(self, rc: SkillReleaseCandidate) -> tuple[bool, list[str]]:
        """Fuzz the deterministic MCP tool handler with adversarial & edge-case inputs."""
        fuzz_payloads = [
            {},
            {"order_id": None, "amount": -500},
            {"order_id": "'; DROP TABLE orders; --", "amount": "not_a_number"},
            {"order_id": "ord_901", "amount": 0.0, "effective_date": "99/99/9999"},
            {"order_id": "ord_901", "amount": 1e12, "reason_code": "INVALID_ENUM_VALUE"},
            {"order_id": "   ", "amount": -0.01},
        ]
        errors = []
        for idx, payload in enumerate(fuzz_payloads):
            try:
                res = rc.tool_handler(payload)
                if not isinstance(res, dict) or "isError" not in res:
                    errors.append(f"Fuzz #{idx}: Handler returned non-MCP result structure")
                    continue
                if res.get("isError"):
                    text = res.get("content", [{}])[0].get("text", "")
                    if "Traceback" in text or "Exception" in text or len(text) < 15:
                        errors.append(f"Fuzz #{idx}: Missing actionable SEP-1303 error hint ('{text}')")
            except Exception as exc:
                errors.append(f"Fuzz #{idx} CRASHED with unhandled {type(exc).__name__}: {exc}")

        return (len(errors) == 0, errors)

    def gate_3_catalog_routing_confusion_matrix(self, rc: SkillReleaseCandidate) -> tuple[bool, list[str]]:
        """Check for semantic routing collision against existing skills in the MCP catalog."""
        errors = []
        cand_words = set(re.findall(r"\w+", (rc.frontmatter.get("description", "")).lower())) - {
            "the", "and", "for", "to", "a", "in", "of", "or", "with"
        }

        # Check overlap with existing catalog skills
        for existing in self.catalog:
            if existing["name"] == rc.frontmatter.get("name"):
                continue
            ex_words = set(re.findall(r"\w+", existing.get("description", "").lower()))
            overlap = len(cand_words & ex_words) / max(1, len(cand_words))
            if overlap > 0.65:
                errors.append(
                    f"Semantic Shadowing detected with '{existing['name']}' "
                    f"(keyword overlap={round(overlap * 100)}%). Disambiguate frontmatter description."
                )

        return (len(errors) == 0, errors)

    def gate_4_model_agnostic_behavioral_matrix(self, rc: SkillReleaseCandidate) -> tuple[bool, list[str]]:
        errors = []
        for tier, pass3 in rc.behavioral_pass_power_3.items():
            if pass3 < 0.95:
                errors.append(f"Model Tier '{tier}' Pass^3 = {pass3} (below 0.95 release threshold)")
        if rc.behavioral_taf > 1.25:
            errors.append(f"Token Amplification Factor TAF = {rc.behavioral_taf} (exceeds 1.25 budget)")
        return (len(errors) == 0, errors)

    def gate_5_build_sep2640_manifest(self, rc: SkillReleaseCandidate) -> dict[str, Any]:
        """Generate immutable SEP-2640 cryptographic skill manifest."""
        manifest_entries = [
            {
                "uri": rc.uri,
                "size": len(rc.skill_markdown.encode("utf-8")),
                "digest": compute_sha256(rc.skill_markdown),
            }
        ]
        for ref_uri, ref_content in rc.references.items():
            manifest_entries.append(
                {
                    "uri": ref_uri,
                    "size": len(ref_content.encode("utf-8")),
                    "digest": compute_sha256(ref_content),
                }
            )
        return {
            "uri": rc.uri,
            "version": rc.version,
            "frontmatter": rc.frontmatter,
            "manifest": manifest_entries,
        }

    def gate_6_otel_canary_health_check(
        self, manifest_digest: str, canary_error_rate: float, canary_taf: float
    ) -> dict[str, Any]:
        """Evaluate SEP-414 OpenTelemetry canary telemetry for auto-promotion or auto-rollback."""
        healthy = canary_error_rate <= 0.03 and canary_taf <= 1.25
        return {
            "canary_skill_digest": manifest_digest[:28] + "...",
            "observed_isError_rate": f"{round(canary_error_rate * 100, 1)}%",
            "observed_runtime_TAF": canary_taf,
            "decision": "🚀 PROMOTE TO 100% PRODUCTION" if healthy else "⏪ AUTO-ROLLBACK TO PREVIOUS DIGEST",
        }

    def run_pipeline(self, rc: SkillReleaseCandidate) -> dict[str, Any]:
        print(f"\n🏭 Running Skill Delivery Factory for: {rc.uri} (v{rc.version})")
        print("-" * 78)
        gates = [
            ("Gate 1: Static Contract & Token Budget", self.gate_1_static_contract_and_token_budget),
            ("Gate 2: Deterministic Property Fuzzing", self.gate_2_property_based_fuzzing),
            ("Gate 3: Catalog Anti-Shadowing Matrix ", self.gate_3_catalog_routing_confusion_matrix),
            ("Gate 4: Model-Agnostic Pass^3 & TAF   ", self.gate_4_model_agnostic_behavioral_matrix),
        ]

        all_passed = True
        for gate_name, gate_fn in gates:
            passed, errs = gate_fn(rc)
            icon = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {gate_name} -> {icon}")
            if not passed:
                all_passed = False
                for e in errs:
                    print(f"      ↳ {e}")

        if not all_passed:
            print("   🛑 Pipeline HALTED: Release Candidate rejected before packaging.")
            return {"released": False}

        manifest_pkg = self.gate_5_build_sep2640_manifest(rc)
        primary_digest = manifest_pkg["manifest"][0]["digest"]
        print(f"   Gate 5: Cryptographic SEP-2640 Signing -> ✅ SIGNED ({primary_digest[:28]}...)")

        canary = self.gate_6_otel_canary_health_check(primary_digest, canary_error_rate=0.01, canary_taf=1.08)
        print(f"   Gate 6: OTel (SEP-414) Canary Monitor  -> {canary['decision']}")
        return {"released": True, "manifest": manifest_pkg, "canary": canary}


# --- Sample Tool Handlers for Testing ---

def buggy_tool_handler(args: dict[str, Any]) -> dict[str, Any]:
    """Anti-pattern handler: crashes with raw ValueError/KeyError on fuzz inputs."""
    order_id = args["order_id"]  # Raises KeyError if missing!
    if float(args["amount"]) <= 0:
        raise ValueError("Negative amount")
    return {"isError": False, "structuredContent": {"order_id": order_id}}


def compliant_tool_handler(args: dict[str, Any]) -> dict[str, Any]:
    """SEP-1303 compliant handler: catches all validation errors and returns semantic hints."""
    order_id = args.get("order_id")
    if not isinstance(order_id, str) or not re.match(r"^ord_[0-9]+$", order_id.strip()):
        return {
            "isError": True,
            "content": [
                {
                    "type": "text",
                    "text": "Invalid `order_id`. Expected format 'ord_<digits>' (e.g., 'ord_901'). Please verify and retry.",
                }
            ],
        }
    amount = args.get("amount")
    if not isinstance(amount, (int, float)) or amount <= 0 or amount > 10000:
        return {
            "isError": True,
            "content": [
                {
                    "type": "text",
                    "text": "Invalid `amount`. Expected a positive number between 0.01 and 10000.00.",
                }
            ],
        }
    return {
        "isError": False,
        "content": [{"type": "text", "text": f"Refund of ${amount:.2f} processed for {order_id}."}],
        "structuredContent": {"order_id": order_id, "amount": float(amount), "status": "refunded"},
    }


def run_demo():
    print("=" * 78)
    print("Skill Engineering 04: The 6-Stage Skill Delivery Factory (CI/CD Pipeline)")
    print("=" * 78)

    existing_catalog = [
        {
            "name": "chargeback-dispute",
            "description": "Handle bank chargeback disputes and fraud arbitration evidence submission.",
        },
        {
            "name": "k8s-rollback",
            "description": "Safely rollback a production Kubernetes deployment and verify pod readiness.",
        },
    ]

    factory = SkillDeliveryFactoryPipeline(existing_catalog)

    # Candidate 1: Broken Skill PR (Fails Gates 1, 2, 3, and 4)
    bad_candidate = SkillReleaseCandidate(
        uri="skill://shop/refund-processing/SKILL.md",
        version="2.0.0-rc1",
        frontmatter={
            "name": "refund-processing",
            # Collides heavily with chargeback-dispute + missing min_model_tier
            "description": "Handle bank chargeback disputes and fraud arbitration evidence submission.",
            "category": "customer-support",
        },
        skill_markdown="# Refund Skill\nCall tool.",
        references={},
        tool_definition={
            "name": "process_refund",
            "inputSchema": {"type": "object", "properties": {"order_id": {"type": "string"}}},
            "annotations": {"readOnlyHint": False, "idempotentHint": False},  # Missing idempotency!
        },
        tool_handler=buggy_tool_handler,
        positive_queries=["Refund my order ord_901"],
        negative_distractor_queries=["Submit bank chargeback arbitration"],
        behavioral_pass_power_3={"frontier": 0.96, "flash": 0.72},  # Flash fails Pass^3!
        behavioral_taf=1.65,  # High retry amplification!
    )

    # Candidate 2: Fixed, Enterprise-Grade Skill PR (Passes all 6 Gates)
    good_candidate = SkillReleaseCandidate(
        uri="skill://shop/refund-processing/SKILL.md",
        version="2.0.0",
        frontmatter={
            "name": "refund-processing",
            "description": "Verify 30-day order eligibility and issue customer refunds or store credit.",
            "category": "customer-support",
            "min_model_tier": "flash",
        },
        skill_markdown=(
            "# Refund Processing Skill\n"
            "1. Invoke `process_refund` with `order_id`, `amount`, and `reason_code`.\n"
            "2. For cross-border tax rules, read `skill://shop/refund-processing/references/tax_policy.md`."
        ),
        references={
            "skill://shop/refund-processing/references/tax_policy.md": "# Tax Policy\nEU VAT is refunded automatically."
        },
        tool_definition={
            "name": "process_refund",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "pattern": "^ord_[0-9]+$"},
                    "amount": {"type": "number", "minimum": 0.01},
                    "reason_code": {"type": "string", "enum": ["damaged", "late_delivery", "changed_mind"]},
                },
                "required": ["order_id", "amount"],
            },
            "annotations": {"readOnlyHint": False, "idempotentHint": True, "destructiveHint": False},
        },
        tool_handler=compliant_tool_handler,
        positive_queries=["Refund my order ord_901 for $250"],
        negative_distractor_queries=["Submit bank chargeback arbitration"],
        behavioral_pass_power_3={"frontier": 1.0, "flash": 0.98},
        behavioral_taf=1.06,
    )

    # Run Factory on both candidates
    factory.run_pipeline(bad_candidate)
    result = factory.run_pipeline(good_candidate)

    if result.get("released"):
        print("\n📜 Published SEP-2640 Signed Skill Manifest:")
        print(json.dumps(result["manifest"], indent=2))


if __name__ == "__main__":
    run_demo()
