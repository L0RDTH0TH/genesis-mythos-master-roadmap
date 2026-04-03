from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ValidationResult(BaseModel):
    primary_code: str
    severity: Literal["high", "medium", "low"]
    recommended_action: Literal["repair_append", "inline_repair", "hard_block"]
    report_path: str | None = None
    hygiene_issues: list[str] = Field(default_factory=list)


class QueueEntry(BaseModel):
    """One JSONL object; extra keys allowed for forward compatibility."""

    model_config = ConfigDict(extra="allow")

    id: str
    mode: str
    project_id: str | None = None
    params: dict | None = None
    queue_priority: str | None = None
    validator_repair_followup: bool | None = None


class DispatchIntent(BaseModel):
    op: Literal["dispatch"] = "dispatch"
    subagent_type: str = "roadmap"
    queue_entry_id: str
    project_id: str
    queue_pass_phase: str
    pass_id: Literal["pass1", "pass3"]
    dispatch_ordinal: int
    micro_workflow: list[str]
    allowed_sub_steps: dict[str, list[str]] | None = None
    strict_mode: bool = True
    # True when Pass 3 is pre-allocated before any repair line exists (L1 will append it during/after Pass 1). queue_entry_id is synthetic — resolve from queue after Pass 1.
    is_anticipatory_drain: bool = False


class EatQueueRunPlan(BaseModel):
    schema_version: int = 2
    parent_run_id: str
    intents: list[DispatchIntent]
    consumed_ids: list[str]
    # True when the plan schedules Pass 3 repair dispatches in the same manifest as Pass 1 — Layer 1 must run all intents before returning (same EAT-QUEUE iteration).
    inline_pass3_drain: bool = False
    # True when at least one intent is an anticipatory repair drain slot (Pass 3 before repair line exists in snapshot).
    has_anticipatory_repair_slot: bool = False
