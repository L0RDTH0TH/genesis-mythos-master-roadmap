"""Central micro_workflow tables for eat_queue_core (schema v2).

Inline Pass 3 drain: when the prompt-queue snapshot already contains both a forward
RESUME_ROADMAP line and a repair-class line for the same project, ``build_plan`` emits
Pass 1 then Pass 3 intents in one ``intents`` array and sets ``EatQueueRunPlan.inline_pass3_drain``.
Layer 1 must execute both in the **same** EAT-QUEUE invocation (no separate run for repair).
"""

from __future__ import annotations

from typing import Any

# Maps logical micro_workflow labels to nested_subagent_ledger step ids (None = no ledger row).
MICRO_TO_LEDGER_STEP: dict[str, str | None] = {
    "roadmap_core": None,
    "nested_validator_first": "nested_validator_first",
    "ira": "ira_post_first_validator",
    "nested_validator_second": "nested_validator_second",
    "l1_post_lv": None,
    "validator": "nested_validator_first",
    "final_validator": "nested_validator_second",
}

# Default RESUME_ROADMAP deepen (forward / initial pass).
WORKFLOW_RESUME_ROADMAP_DEEPEN: list[str] = [
    "roadmap_core",
    "nested_validator_first",
    "ira",
    "nested_validator_second",
    "l1_post_lv",
]

# Repair / handoff-audit (orchestrator strict — three nested steps).
WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT: list[str] = [
    "validator",
    "ira",
    "final_validator",
]

# Other RESUME_ROADMAP actions (recal, expand, etc.) — explicit default.
WORKFLOW_RESUME_ROADMAP_OTHER: list[str] = [
    "roadmap_core",
    "nested_validator_first",
    "ira",
    "nested_validator_second",
    "l1_post_lv",
]


def _action(e: Any) -> str:
    p = getattr(e, "params", None) or {}
    if not isinstance(p, dict):
        return ""
    a = p.get("action")
    return str(a).strip().lower() if a else ""


def micro_workflow_for_entry(e: Any, *, is_repair_dispatch: bool) -> tuple[list[str], dict[str, list[str]] | None]:
    """
    Return (micro_workflow, allowed_sub_steps) for a queue entry.
    is_repair_dispatch: True when this intent is the repair-class Pass 3 dispatch.
    """
    action = _action(e)
    if is_repair_dispatch:
        return (list(WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT), None)
    if action == "deepen":
        return (list(WORKFLOW_RESUME_ROADMAP_DEEPEN), None)
    if action in ("handoff-audit", "handoff_audit"):
        # Forward-slot handoff-audit (non-repair) uses full pipeline.
        return (list(WORKFLOW_RESUME_ROADMAP_DEEPEN), None)
    return (list(WORKFLOW_RESUME_ROADMAP_OTHER), None)


def ledger_steps_from_micro(micro: list[str]) -> list[str]:
    """Ordered ledger `step` ids expected from a micro_workflow (skips None)."""
    out: list[str] = []
    for label in micro:
        lid = MICRO_TO_LEDGER_STEP.get(label)
        if lid:
            out.append(lid)
    return out
