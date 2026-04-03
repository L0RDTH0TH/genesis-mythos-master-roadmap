"""Deterministic EAT-QUEUE plan builder (Phase 1–2 milestone)."""

__version__ = "0.1.0"

from .ledger_validate import (
    validate_executed_micro_workflow,
    validate_ledger_steps_executed,
)
from .models import DispatchIntent, EatQueueRunPlan, ValidationResult
from .plan import append_decisions, build_plan, parse_queue_jsonl
from .workflows import (
    WORKFLOW_RESUME_ROADMAP_DEEPEN,
    WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT,
    anticipatory_repair_drain_queue_entry_id,
    ledger_steps_from_micro,
    micro_workflow_for_entry,
)

__all__ = [
    "__version__",
    "DispatchIntent",
    "EatQueueRunPlan",
    "ValidationResult",
    "WORKFLOW_RESUME_ROADMAP_DEEPEN",
    "WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT",
    "anticipatory_repair_drain_queue_entry_id",
    "append_decisions",
    "build_plan",
    "ledger_steps_from_micro",
    "micro_workflow_for_entry",
    "parse_queue_jsonl",
    "validate_executed_micro_workflow",
    "validate_ledger_steps_executed",
]
