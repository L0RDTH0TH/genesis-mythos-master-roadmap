"""Reactive multi-pass EAT-QUEUE plan generation (Python nervous system).

``run_full_eat_queue_cycle`` may run up to ``max_passes`` plan builds, re-reading the
queue from disk between passes. In the same OS process, the queue only changes if another
actor writes it, or if ``simulate_post_pass1_repair`` is used (tests / dry-run).

Production use: emit plan, Layer 1 dispatches all intents in order (Pass 1 + Pass 3 in one
manifest when ``build_plan`` lists both). **A.7 queue rewrite** must remove
``queue_rewrite_ids`` (``consumed_ids`` ∪ all Pass 3 ``queue_entry_id`` values), not only
``consumed_ids``, so repairs do not leak to the next EAT-QUEUE run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, Field

from .lanes import FALLBACK_ALLOWED_LANES, filter_entries_by_lane, validate_lane_filter_token
from .plan import append_decisions, build_plan, emit_plan_json, load_queue_file
from .workflows import micro_workflow_for_entry
from .models import (
    EatQueueRunPlan,
    OptionEvaluation,
    OptionEvaluationValidationResult,
    QueueEntry,
)
from .a5b_dedupe import DedupeDecision
from .config_loader import max_inline_a5b_repair_generations, parse_queue_config, resolve_config_path
from .lane_queue_config import effective_max_inline_a5b
from .watcher_append import append_watcher_telemetry_line
from .pool_sync import (
    hydrate_track_pq_from_pool,
    read_central_pool_fanout_enabled,
    read_pool_sync_strict_central_only,
    read_queue_rationale_enforcement_enabled,
    read_tracking_intent_receipts_enabled,
)


def parallel_track_for_lane(lane_filter: str | None) -> str:
    if lane_filter in ("sandbox", "godot"):
        return lane_filter
    return "-"


def effective_queue_lane(entry: QueueEntry) -> str:
    return (entry.queue_lane or "default").strip().lower()


def entry_needs_option_evaluation(entry: QueueEntry, rationale_enforcement: bool) -> bool:
    if not rationale_enforcement:
        return False
    mode = (entry.mode or "").upper()
    primary = mode.split("-")[0].strip()
    if primary != "RESUME_ROADMAP":
        return False
    p = entry.params or {}
    return p.get("roadmap_track") == "execution"


def resolve_goal_file(vault_root: Path, master_goal_ref: str) -> Path | None:
    ref = master_goal_ref.strip().strip('"').strip("'")
    if not ref or ".." in ref or ref.startswith("/"):
        return None
    root = vault_root.resolve()
    cand = (root / ref).resolve()
    try:
        cand.relative_to(root)
    except ValueError:
        return None
    return cand if cand.is_file() else None


def validate_option_evaluation_for_entry(
    entry: QueueEntry,
    *,
    vault_root: Path,
    rationale_enforcement: bool,
) -> OptionEvaluationValidationResult:
    if not entry_needs_option_evaluation(entry, rationale_enforcement):
        return OptionEvaluationValidationResult(ok=True)
    raw = (entry.params or {}).get("option_evaluation")
    if raw is None:
        return OptionEvaluationValidationResult(
            ok=False,
            divergence_codes=["option_evaluation_missing"],
            errors=["missing params.option_evaluation"],
        )
    try:
        oe = OptionEvaluation.model_validate(raw)
    except Exception as e:
        return OptionEvaluationValidationResult(
            ok=False,
            divergence_codes=["option_evaluation_invalid"],
            errors=[str(e)],
        )
    errors: list[str] = []
    codes: list[str] = []
    ids = {a.id for a in oe.alternatives}
    if oe.chosen not in ids:
        errors.append("chosen id not in alternatives")
        codes.append("option_evaluation_invalid")
    scores = [a.alignment_score for a in oe.alternatives]
    if scores and all(x is not None for x in scores):
        chosen_o = next(x for x in oe.alternatives if x.id == oe.chosen)
        assert chosen_o.alignment_score is not None
        mx = max(s for s in scores if s is not None)
        if chosen_o.alignment_score + 1e-9 < mx:
            errors.append("chosen alignment_score is not tied for max")
            codes.append("alignment_score_mismatch")
    goal = resolve_goal_file(vault_root, oe.master_goal_ref)
    if goal is not None and oe.rationale.strip():
        blob = goal.read_text(encoding="utf-8", errors="replace")
        snippet = oe.rationale.strip()
        chunk = snippet[: min(80, len(snippet))]
        if len(chunk) >= 12 and chunk not in blob:
            errors.append("rationale missing verbatim substring from master_goal_ref file")
            codes.append("rationale_quote_missing")
    return OptionEvaluationValidationResult(ok=len(errors) == 0, divergence_codes=codes, errors=errors)


def _params_fingerprint(params: dict | None) -> str:
    if not params:
        return "empty"
    try:
        b = json.dumps(params, sort_keys=True, ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError):
        return "unhashable"
    return hashlib.sha256(b).hexdigest()[:16]


def append_task_handoff_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(obj, ensure_ascii=False) + "\n"
    prev = path.read_text(encoding="utf-8") if path.is_file() else ""
    path.write_text(prev + line, encoding="utf-8")


def build_intent_snapshot_row(
    *,
    vault_root: Path,
    parent_run_id: str,
    entry: QueueEntry,
    parallel_track: str,
    params_hash: str,
) -> dict[str, Any]:
    rid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    lane = effective_queue_lane(entry)
    return {
        "schema_version": 1,
        "task_correlation_id": rid,
        "parent_task_correlation_id": None,
        "record_type": "intent_snapshot",
        "iso_timestamp": now,
        "timestamp": now,
        "from_actor": "eat_queue_core",
        "to_actor": "intent_tracking",
        "subagent_type": "intent_tracking",
        "queue_entry_id": entry.id,
        "parent_run_id": parent_run_id,
        "project_id": entry.project_id or "-",
        "vault_root": str(vault_root),
        "parallel_track": parallel_track,
        "queue_lane": lane,
        "mode": entry.mode,
        "params_hash": params_hash,
        "body": json.dumps({"params_hash": params_hash}, ensure_ascii=False),
        "sanitization_rules_applied": [],
    }


def build_intent_receipt_row(
    *,
    vault_root: Path,
    parent_run_id: str,
    entry: QueueEntry,
    parallel_track: str,
    oe_res: OptionEvaluationValidationResult,
    intent_snapshot_task_correlation_id: str | None,
    inline_drain_budget_remaining: int | None = None,
    dedupe_attempted: bool = False,
    dedupe_suppressed: bool = False,
    suppressed_by: str = "none",
) -> dict[str, Any]:
    rid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    lane = effective_queue_lane(entry)
    status_class = "success" if oe_res.ok else "provisional_success"
    div = list(dict.fromkeys(oe_res.divergence_codes))
    planned = (entry.params or {}).get("action") if isinstance(entry.params, dict) else None
    planned_action = str(planned) if planned is not None else "dispatch"
    body_obj: dict[str, Any] = {
        "status_class": status_class,
        "divergence_codes": div,
        "planned_action": planned_action,
        "actual_action": "eat_queue_plan_emitted",
        "ledger_ref": [rid],
        "dedupe_attempted": dedupe_attempted,
        "dedupe_suppressed": dedupe_suppressed,
        "suppressed_by": suppressed_by,
    }
    if inline_drain_budget_remaining is not None:
        body_obj["inline_drain_budget_remaining"] = inline_drain_budget_remaining
    if not oe_res.ok and div:
        body_obj["provisional_reason"] = div[0]
    out: dict[str, Any] = {
        "schema_version": 1,
        "task_correlation_id": rid,
        "parent_task_correlation_id": None,
        "record_type": "intent_actual_receipt",
        "iso_timestamp": now,
        "timestamp": now,
        "from_actor": "eat_queue_core",
        "to_actor": "intent_tracking",
        "subagent_type": "intent_tracking",
        "queue_entry_id": entry.id,
        "parent_run_id": parent_run_id,
        "project_id": entry.project_id or "-",
        "vault_root": str(vault_root),
        "parallel_track": parallel_track,
        "queue_lane": lane,
        "mode": entry.mode,
        "status_class": status_class,
        "status": "ok" if oe_res.ok else "provisional",
        "divergence_codes": div,
        "planned_action": planned_action,
        "actual_action": "eat_queue_plan_emitted",
        "ledger_ref": body_obj["ledger_ref"],
        "retryable": not oe_res.ok,
        "intent_snapshot_id": intent_snapshot_task_correlation_id,
        "dedupe_attempted": dedupe_attempted,
        "dedupe_suppressed": dedupe_suppressed,
        "suppressed_by": suppressed_by,
        "body": json.dumps(body_obj, ensure_ascii=False),
        "sanitization_rules_applied": [],
    }
    if inline_drain_budget_remaining is not None:
        out["inline_drain_budget_remaining"] = inline_drain_budget_remaining
    return out


def build_a5b_append_intent_receipt_row(
    *,
    vault_root: Path,
    parent_run_id: str,
    entry: QueueEntry,
    decision: DedupeDecision,
    parallel_track: str,
    inline_drain_budget_remaining: int | None = None,
    provisional_reason: str | None = None,
) -> dict[str, Any]:
    """Receipt for harness ``append_entries`` A.5b.0z dedupe (merge into Watcher trace by Layer 1)."""
    rid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    lane = effective_queue_lane(entry)
    p = entry.params if isinstance(entry.params, dict) else {}
    oid = p.get("origin_request_id")
    oid_s = oid.strip() if isinstance(oid, str) else None
    body_obj: dict[str, Any] = {
        "status_class": "success",
        "actual_action": "harness_append_entries",
        "dedupe_attempted": decision.dedupe_attempted,
        "dedupe_suppressed": decision.dedupe_suppressed,
        "suppressed_by": decision.suppressed_by,
        "normalized_guidance_prefix": decision.normalized_guidance_prefix,
        "ledger_ref": [rid],
    }
    if decision.audit_suppressed_by:
        body_obj["audit_suppressed_by"] = decision.audit_suppressed_by
    if inline_drain_budget_remaining is not None:
        body_obj["inline_drain_budget_remaining"] = inline_drain_budget_remaining
    if provisional_reason:
        body_obj["provisional_reason"] = provisional_reason
    if oid_s:
        body_obj["origin_request_id"] = oid_s
    if decision.dedupe_suppressed:
        body_obj["dedupe_suppressed_handoff_repair"] = True
    if decision.suppressing_entry_id:
        body_obj["suppressing_queue_entry_id"] = decision.suppressing_entry_id
    rec: dict[str, Any] = {
        "schema_version": 1,
        "task_correlation_id": rid,
        "parent_task_correlation_id": None,
        "record_type": "intent_actual_receipt",
        "iso_timestamp": now,
        "timestamp": now,
        "from_actor": "eat_queue_core",
        "to_actor": "intent_tracking",
        "subagent_type": "intent_tracking",
        "queue_entry_id": entry.id,
        "parent_run_id": parent_run_id,
        "project_id": entry.project_id or "-",
        "vault_root": str(vault_root),
        "parallel_track": parallel_track,
        "queue_lane": lane,
        "mode": entry.mode,
        "dedupe_attempted": decision.dedupe_attempted,
        "dedupe_suppressed": decision.dedupe_suppressed,
        "suppressed_by": decision.suppressed_by,
        "body": json.dumps(body_obj, ensure_ascii=False),
        "sanitization_rules_applied": [],
    }
    if inline_drain_budget_remaining is not None:
        rec["inline_drain_budget_remaining"] = inline_drain_budget_remaining
    return rec


def emit_intent_tracking_for_plan_pass(
    *,
    vault_root: Path,
    queue_path: Path,
    enriched: dict[str, Any],
    entries_lane: list[QueueEntry],
    lane_filter: str | None,
    emit_watcher_result: bool = True,
) -> list[str]:
    if not read_tracking_intent_receipts_enabled(vault_root):
        return []
    comms_path = queue_path.parent / "task-handoff-comms.jsonl"
    by_id = {e.id: e for e in entries_lane}
    rationale_enf = read_queue_rationale_enforcement_enabled(vault_root)
    parallel_track = parallel_track_for_lane(lane_filter)
    pr = str(enriched.get("parent_run_id", "-"))
    inline_rem = enriched.get("inline_drain_budget_remaining")
    inline_arg = inline_rem if isinstance(inline_rem, int) else None
    msgs: list[str] = []
    for intent in enriched.get("intents") or []:
        qeid = intent.get("queue_entry_id")
        if not isinstance(qeid, str):
            continue
        e = by_id.get(qeid)
        if e is None:
            continue
        ph = _params_fingerprint(e.params if isinstance(e.params, dict) else None)
        snap = build_intent_snapshot_row(
            vault_root=vault_root,
            parent_run_id=pr,
            entry=e,
            parallel_track=parallel_track,
            params_hash=ph,
        )
        append_task_handoff_jsonl(comms_path, snap)
        msgs.append(f"intent_snapshot {qeid}")
        oe_res = validate_option_evaluation_for_entry(
            e, vault_root=vault_root, rationale_enforcement=rationale_enf
        )
        rec = build_intent_receipt_row(
            vault_root=vault_root,
            parent_run_id=pr,
            entry=e,
            parallel_track=parallel_track,
            oe_res=oe_res,
            intent_snapshot_task_correlation_id=snap["task_correlation_id"],
            inline_drain_budget_remaining=inline_arg,
        )
        append_task_handoff_jsonl(comms_path, rec)
        msgs.append(f"intent_actual_receipt {qeid} {rec['status_class']}")
        if emit_watcher_result:
            try:
                body_p = json.loads(rec.get("body", "{}"))
            except json.JSONDecodeError:
                body_p = {}
            trace_payload: dict[str, Any] = {
                "source": "eat_queue_core_full_cycle",
                "record_type": "intent_actual_receipt",
                "queue_entry_id": qeid,
                "parent_run_id": pr,
                "status_class": rec.get("status_class"),
                "parallel_track": parallel_track,
                "dedupe_attempted": body_p.get("dedupe_attempted", False),
                "dedupe_suppressed": body_p.get("dedupe_suppressed", False),
            }
            idr = rec.get("inline_drain_budget_remaining")
            if idr is None:
                idr = body_p.get("inline_drain_budget_remaining")
            if idr is not None:
                trace_payload["inline_drain_budget_remaining"] = idr
            if "provisional_reason" in body_p:
                trace_payload["provisional_reason"] = body_p["provisional_reason"]
            append_watcher_telemetry_line(
                vault_root,
                request_id=f"harness-plan-{qeid}",
                message="eat_queue_plan telemetry",
                trace_payload=trace_payload,
            )
            msgs.append(f"watcher_result {qeid}")
    return msgs


def _entry_action(e: QueueEntry) -> str:
    p = e.params or {}
    if not isinstance(p, dict):
        return ""
    a = p.get("action")
    return str(a).strip().lower() if a else ""


def queue_rewrite_ids(plan: EatQueueRunPlan) -> list[str]:
    """IDs to remove after a full successful orchestrated cycle (fixes Pass 3 drain leak)."""
    seen: set[str] = set()
    out: list[str] = []
    for x in plan.consumed_ids:
        if x not in seen:
            seen.add(x)
            out.append(x)
    for i in plan.intents:
        if i.pass_id == "pass3" and i.queue_entry_id not in seen:
            seen.add(i.queue_entry_id)
            out.append(i.queue_entry_id)
    return out


def _entries_by_id(entries: list[QueueEntry]) -> dict[str, QueueEntry]:
    return {e.id: e for e in entries}


def _is_repair_entry(e: QueueEntry) -> bool:
    return e.queue_priority == "repair" or e.validator_repair_followup is True


def execute_roadmap_with_plan(plan: EatQueueRunPlan) -> dict[str, Any]:
    """Stub: Layer 1 performs real Task(roadmap) dispatches. Used for counts / tracing."""
    return {
        "intents": len(plan.intents),
        "consumed_ids": list(plan.consumed_ids),
        "rewrite_ids": queue_rewrite_ids(plan),
    }


class LedgerValidationResult(BaseModel):
    ok: bool
    errors: list[str] = Field(default_factory=list)


def run_ledger_validation(plan_dict: dict[str, Any], *, strict_mode: bool) -> LedgerValidationResult:
    """Ensure Pass 3 / repair intents expose nested validator + IRA ledger steps."""
    from .workflows import ledger_steps_from_micro

    errors: list[str] = []
    exp_repair = {"nested_validator_first", "ira_post_first_validator", "nested_validator_second"}
    for intent in plan_dict.get("intents") or []:
        if intent.get("pass_id") != "pass3" and intent.get("queue_pass_phase") != "repair":
            continue
        micro = intent.get("micro_workflow") or []
        steps = set(ledger_steps_from_micro(micro))
        if steps != exp_repair:
            errors.append(
                f"queue_entry_id={intent.get('queue_entry_id')!r}: "
                f"expected ledger steps {sorted(exp_repair)}, got {sorted(steps)} "
                f"(micro_workflow={micro})"
            )
    if strict_mode and errors:
        return LedgerValidationResult(ok=False, errors=errors)
    return LedgerValidationResult(ok=len(errors) == 0, errors=errors)


def enrich_plan_dict(
    plan: EatQueueRunPlan,
    entries: list[QueueEntry],
    *,
    initial_action: str,
    initial_profile: str,
    strict_mode: bool,
    full_cycle_pass_index: int,
    full_cycle_passes_total: int,
    vault_root: Path | None = None,
    lane_filter: str | None = None,
) -> dict[str, Any]:
    by_id = _entries_by_id(entries)
    base = plan.model_dump()
    base["strict_mode"] = strict_mode
    base["effective_pipeline_mode"] = initial_profile
    base["full_cycle_pass_index"] = full_cycle_pass_index
    base["full_cycle_passes_total"] = full_cycle_passes_total
    base["queue_rewrite_ids"] = queue_rewrite_ids(plan)
    base["inline_pass3_drain"] = any(i.pass_id == "pass3" for i in plan.intents)
    base["has_anticipatory_repair_slot"] = any(
        i.queue_entry_id.startswith("anticipatory-repair-drain::") for i in plan.intents
    )
    max_gen = 4
    if vault_root is not None:
        if lane_filter:
            max_gen = effective_max_inline_a5b(vault_root, lane_filter)
        else:
            cfg = parse_queue_config(resolve_config_path(vault_root, None))
            max_gen = max_inline_a5b_repair_generations(cfg)
    used_pass3_repair = sum(
        1
        for i in plan.intents
        if i.pass_id == "pass3" and i.queue_pass_phase == "repair"
    )
    base["inline_drain_budget_remaining"] = max(0, max_gen - used_pass3_repair)

    intents_out: list[dict[str, Any]] = []
    for intent in plan.intents:
        row = intent.model_dump()
        e = by_id.get(intent.queue_entry_id)
        is_repair_dispatch = intent.pass_id == "pass3" or intent.queue_pass_phase == "repair"
        act0 = initial_action.strip().lower()
        if (e is not None and _entry_action(e) == "pass3_repair_drain") or (
            act0 == "pass3_repair_drain" and is_repair_dispatch
        ):
            synth = e or QueueEntry(
                id=intent.queue_entry_id,
                mode="RESUME_ROADMAP",
                params={"action": "pass3_repair_drain"},
            )
            micro, allowed = micro_workflow_for_entry(synth, is_repair_dispatch=True)
        elif e is not None:
            micro, allowed = micro_workflow_for_entry(e, is_repair_dispatch=is_repair_dispatch)
        else:
            # Synthetic anticipatory id — treat as repair dispatch
            micro, allowed = micro_workflow_for_entry(
                QueueEntry(id=intent.queue_entry_id, mode="RESUME_ROADMAP", params={"action": "deepen"}),
                is_repair_dispatch=True,
            )
        row["micro_workflow"] = micro
        if allowed is not None:
            row["allowed_sub_steps"] = allowed
        if intent.queue_entry_id.startswith("anticipatory-repair-drain::"):
            row["is_anticipatory_drain"] = True
        intents_out.append(row)
    base["intents"] = intents_out
    return base


def emit_enriched_plan(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class FullCycleResult(BaseModel):
    """Outcome of ``run_full_eat_queue_cycle``."""

    parent_run_id: str
    passes_run: int
    plans: list[dict[str, Any]] = Field(default_factory=list)
    ledger_validation: LedgerValidationResult | None = None
    execute_summaries: list[dict[str, Any]] = Field(default_factory=list)
    final_repair_lines_remaining: int = 0
    queue_empty_after_cleanup: bool = False
    messages: list[str] = Field(default_factory=list)


def _count_repair_roadmap(entries: list[QueueEntry]) -> int:
    def is_roadmap(e: QueueEntry) -> bool:
        return "RESUME_ROADMAP" in (e.mode or "").upper()

    return sum(1 for e in entries if is_roadmap(e) and _is_repair_entry(e))


def _workflow_track_for_project(vault_root: Path, project_id: str) -> tuple[str, Path]:
    """Resolve preferred workflow cursor path and roadmap_track for bootstrap."""
    exec_path = (
        vault_root
        / "1-Projects"
        / project_id
        / "Roadmap"
        / "Execution"
        / "workflow_state-execution.md"
    )
    if exec_path.is_file():
        return "execution", exec_path
    conceptual = vault_root / "1-Projects" / project_id / "Roadmap" / "workflow_state.md"
    return "conceptual", conceptual


def _append_empty_queue_bootstrap(
    *,
    vault_root: Path,
    queue_path: Path,
    project_id: str,
    lane_filter: str | None,
) -> dict[str, Any]:
    """Append one deterministic RESUME_ROADMAP line when queue is empty for this lane."""
    roadmap_track, workflow_path = _workflow_track_for_project(vault_root, project_id)
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    eid = f"empty-bootstrap-{project_id}-{stamp}"
    rel_source = str(workflow_path.relative_to(vault_root)) if workflow_path.exists() else ""
    entry: dict[str, Any] = {
        "id": eid,
        "mode": "RESUME_ROADMAP",
        "project_id": project_id,
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "idempotency_key": eid,
        "source_file": rel_source,
        "params": {
            "action": "deepen",
            "roadmap_track": roadmap_track,
            "queue_next": True,
            "user_guidance": (
                f"Automatic empty-queue bootstrap for {project_id} "
                f"({roadmap_track} track). Continue from last successful cursor."
            ),
        },
    }
    if lane_filter:
        entry["queue_lane"] = lane_filter
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    with queue_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def apply_queue_cleanup(queue_path: Path, ids_to_remove: set[str]) -> bool:
    """Remove lines whose ``id`` is in ``ids_to_remove`` (read–filter–write). Returns True if file changed."""
    if not queue_path.is_file():
        return False
    text = queue_path.read_text(encoding="utf-8")
    lines_out: list[str] = []
    changed = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            lines_out.append(raw)
            continue
        if isinstance(obj, dict) and obj.get("id") in ids_to_remove:
            changed = True
            continue
        lines_out.append(raw)
    if changed:
        queue_path.write_text("\n".join(lines_out) + ("\n" if lines_out else ""), encoding="utf-8")
    return changed


def apply_queue_cleanup_dual_track(
    track_pq: Path,
    central_pool: Path,
    ids_to_remove: set[str],
) -> tuple[bool, bool]:
    """Remove ids from track PQ and central pool (A.7 dual removal). Returns (track_changed, pool_changed)."""
    return (
        apply_queue_cleanup(track_pq, ids_to_remove),
        apply_queue_cleanup(central_pool, ids_to_remove),
    )


def run_full_eat_queue_cycle(
    *,
    initial_action: str,
    initial_profile: str,
    max_passes: int = 2,
    strict_mode: bool = True,
    vault_root: Path | None = None,
    queue_path: Path | None = None,
    plan_path: Path | None = None,
    decisions_path: Path | None = None,
    parent_run_id: str | None = None,
    simulate_post_pass1_repair: Callable[[], None] | None = None,
    apply_cleanup: bool = False,
    lane_filter: str | None = None,
    central_pool_fanout: bool | None = None,
    lane_project_id: str | None = None,
    emit_watcher_result: bool = True,
) -> FullCycleResult:
    """
    Build up to ``max_passes`` plans, re-reading the queue between passes.

    When ``simulate_post_pass1_repair`` is set, it is invoked after pass 1 plan emit to
    model A.5b-style repair append before pass 2 (tests).

    When ``apply_cleanup`` is True, after each pass ``execute_roadmap_with_plan`` summary,
    ``queue_rewrite_ids`` are removed from the queue file (simulates A.7 with leak fix).

    When ``lane_filter`` is set, ``build_plan`` and ``enrich_plan_dict`` use the same subset
    as ``eat_queue_core plan --lane`` (track ∪ shared; ``shared`` / ``default`` only).
    """
    root = (vault_root or Path.cwd()).resolve()
    qpath = (queue_path or (root / ".technical" / "prompt-queue.jsonl"))
    if not qpath.is_absolute():
        qpath = (root / qpath).resolve()
    else:
        qpath = qpath.resolve()
    ppath = plan_path or (qpath.parent / "eat_queue_run_plan.json")
    dpath = decisions_path or (qpath.parent / "eat-queue-decisions.jsonl")
    prid = parent_run_id or f"eatq-fullcycle-{uuid.uuid4().hex[:12]}"

    pool_default = (root / ".technical" / "prompt-queue.jsonl").resolve()
    if central_pool_fanout is None:
        use_fanout = read_central_pool_fanout_enabled(root)
    else:
        use_fanout = central_pool_fanout
    dual_pool_cleanup = bool(
        lane_filter and use_fanout and qpath != pool_default
    )
    if dual_pool_cleanup:
        try:
            rel_target = qpath.relative_to(root)
        except ValueError:
            rel_target = qpath
        hr = hydrate_track_pq_from_pool(
            vault_root=root,
            lane_filter=lane_filter,  # type: ignore[arg-type]
            target_pq=rel_target,
            strict_central_only=read_pool_sync_strict_central_only(root),
        )
        if not hr.ok:
            raise ValueError(hr.messages[0] if hr.messages else "pool_sync hydrate failed")
        messages = [
            f"pool_hydrate: copied {hr.copied_count} id(s) from {hr.pool_path} to {hr.target_pq}"
            + (
                f"; preserved_lane_only={hr.preserved_lane_only_count}"
                if hr.preserved_lane_only_count
                else ""
            )
        ]
        if hr.messages:
            messages.extend(hr.messages)
    else:
        messages = []
    plans_out: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    passes = 0

    bootstrap_appended = False
    for pass_idx in range(max(1, max_passes)):
        entries = load_queue_file(qpath) if qpath.is_file() else []
        if (
            pass_idx == 0
            and not bootstrap_appended
            and lane_project_id
            and len(filter_entries_by_lane(entries, lane_filter)) == 0
        ):
            b = _append_empty_queue_bootstrap(
                vault_root=root,
                queue_path=qpath,
                project_id=lane_project_id,
                lane_filter=lane_filter,
            )
            bootstrap_appended = True
            messages.append(
                "empty_queue_bootstrap_appended: "
                f"{b.get('id')} project_id={lane_project_id} lane={lane_filter or 'default'}"
            )
            entries = load_queue_file(qpath) if qpath.is_file() else []
        plan, decisions = build_plan(entries, prid, lane_filter=lane_filter)
        append_decisions(dpath, decisions)

        entries_lane = filter_entries_by_lane(entries, lane_filter)
        enriched = enrich_plan_dict(
            plan,
            entries_lane,
            initial_action=initial_action,
            initial_profile=initial_profile,
            strict_mode=strict_mode,
            full_cycle_pass_index=pass_idx + 1,
            full_cycle_passes_total=max_passes,
            vault_root=root,
            lane_filter=lane_filter,
        )
        lv = run_ledger_validation(enriched, strict_mode=strict_mode)
        if not lv.ok:
            messages.append("ledger_validation_failed: " + "; ".join(lv.errors))
            if strict_mode:
                emit_enriched_plan(ppath, enriched)
                return FullCycleResult(
                    parent_run_id=prid,
                    passes_run=pass_idx + 1,
                    plans=[enriched],
                    ledger_validation=lv,
                    execute_summaries=summaries,
                    final_repair_lines_remaining=_count_repair_roadmap(entries),
                    messages=messages,
                )

        emit_enriched_plan(ppath, enriched)
        plans_out.append(enriched)
        it_msgs = emit_intent_tracking_for_plan_pass(
            vault_root=root,
            queue_path=qpath,
            enriched=enriched,
            entries_lane=entries_lane,
            lane_filter=lane_filter,
            emit_watcher_result=emit_watcher_result,
        )
        if it_msgs:
            messages.extend(it_msgs)
        summaries.append(execute_roadmap_with_plan(plan))
        passes = pass_idx + 1

        if apply_cleanup:
            removed = set(queue_rewrite_ids(plan))
            if dual_pool_cleanup:
                tc, pc = apply_queue_cleanup_dual_track(qpath, pool_default, removed)
                messages.append(
                    f"pass{pass_idx + 1}: queue cleanup removed {sorted(removed)} "
                    f"(track_pq={tc}, central_pool={pc})"
                )
            else:
                apply_queue_cleanup(qpath, removed)
                messages.append(f"pass{pass_idx + 1}: queue cleanup removed {sorted(removed)}")

        if pass_idx == 0 and simulate_post_pass1_repair is not None:
            simulate_post_pass1_repair()
            messages.append("simulated post-pass1 repair append")
            continue

        if pass_idx >= max_passes - 1:
            break

        has_pass3 = any(i.pass_id == "pass3" for i in plan.intents)
        if has_pass3:
            messages.append(
                "plan includes pass3; single manifest covers Pass 1 + inline Pass 3 drain in one Layer 1 run"
            )
            break

        messages.append(
            "no pass3 in queue snapshot and no simulate hook — stop reactive loop; "
            "re-invoke full_cycle after Layer 1 appends repair (or use tests/simulation)"
        )
        break

    final_entries = load_queue_file(qpath) if qpath.is_file() else []
    return FullCycleResult(
        parent_run_id=prid,
        passes_run=passes,
        plans=plans_out,
        ledger_validation=run_ledger_validation(plans_out[-1], strict_mode=strict_mode) if plans_out else None,
        execute_summaries=summaries,
        final_repair_lines_remaining=_count_repair_roadmap(final_entries),
        queue_empty_after_cleanup=len(final_entries) == 0,
        messages=messages,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Reactive full EAT-QUEUE plan cycle (eat_queue_core)")
    p.add_argument("--vault-root", type=Path, default=None, help="Vault root (default: cwd)")
    p.add_argument("--queue", type=Path, default=None, help="prompt-queue.jsonl path")
    p.add_argument(
        "--emit",
        type=Path,
        default=None,
        help="eat_queue_run_plan.json path (default: dirname(--queue)/eat_queue_run_plan.json)",
    )
    p.add_argument(
        "--decisions-log",
        type=Path,
        default=None,
        help="eat-queue-decisions.jsonl path (default: dirname(--queue)/eat-queue-decisions.jsonl)",
    )
    p.add_argument("--parent-run-id", default=None)
    p.add_argument("--action", default="deepen", help="Initial queue semantic action (e.g. deepen, pass3_repair_drain)")
    p.add_argument("--profile", default="balance", help="effective_pipeline_mode hint (balance|quality|speed)")
    p.add_argument("--max-passes", type=int, default=2)
    p.add_argument("--strict-mode", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument(
        "--apply-cleanup",
        action="store_true",
        help="Remove queue_rewrite_ids from queue after each pass (simulated A.7; use with care)",
    )
    p.add_argument(
        "--lane",
        type=str,
        default=None,
        help="queue_lane_filter for build_plan (must be in allowed_lanes)",
    )
    p.add_argument(
        "--central-pool-fanout",
        action="store_true",
        help="Force central pool → track PQ hydrate when lane + track PQ (overrides Config)",
    )
    p.add_argument(
        "--no-central-pool-fanout",
        action="store_true",
        help="Disable central pool fanout for this run (overrides Config)",
    )
    args = p.parse_args(argv)

    root = (args.vault_root or Path.cwd()).resolve()
    lane_filter: str | None = None
    if args.lane is not None:
        token = args.lane.strip().lower()
        if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
            print(
                f"full_cycle error: lane {token!r} not in allowed_lanes "
                f"({sorted(FALLBACK_ALLOWED_LANES)})",
                file=sys.stderr,
            )
            return 1
        lane_filter = token

    cpf: bool | None = None
    if getattr(args, "no_central_pool_fanout", False):
        cpf = False
    elif getattr(args, "central_pool_fanout", False):
        cpf = True

    try:
        result = run_full_eat_queue_cycle(
            initial_action=args.action,
            initial_profile=args.profile,
            max_passes=args.max_passes,
            strict_mode=args.strict_mode,
            vault_root=root,
            queue_path=args.queue,
            plan_path=args.emit,
            decisions_path=args.decisions_log,
            parent_run_id=args.parent_run_id,
            lane_filter=lane_filter,
            apply_cleanup=args.apply_cleanup,
            central_pool_fanout=cpf,
        )
    except (OSError, ValueError) as e:
        print(f"full_cycle error: {e}", file=sys.stderr)
        return 1

    print(result.model_dump_json(indent=2))
    if result.final_repair_lines_remaining > 0:
        print(
            f"note: {result.final_repair_lines_remaining} repair-class RESUME_ROADMAP line(s) still in queue",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
