"""Deterministic EAT-QUEUE plan builder (Phase 1–2 milestone)."""

__version__ = "0.1.0"

from .models import DispatchIntent, EatQueueRunPlan, ValidationResult
from .plan import append_decisions, build_plan, parse_queue_jsonl

__all__ = [
    "__version__",
    "DispatchIntent",
    "EatQueueRunPlan",
    "ValidationResult",
    "append_decisions",
    "build_plan",
    "parse_queue_jsonl",
]
