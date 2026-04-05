from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .lanes import filter_entries_by_lane
from .models import DispatchIntent, EatQueueRunPlan, QueueEntry, ValidationResult


class _FsmState(str, Enum):
    START = "start"
    PARTITIONED = "partitioned"
    PASS1_DONE = "pass1_done"
    PASS3_DONE = "pass3_done"
    EMITTED = "emitted"


def _pid(e: QueueEntry) -> str:
    if e.project_id:
        return e.project_id
    if e.params and isinstance(e.params, dict):
        p = e.params.get("project_id")
        if isinstance(p, str) and p.strip():
            return p
    return "_none"


def _is_repair(e: QueueEntry) -> bool:
    return e.queue_priority == "repair" or e.validator_repair_followup is True


def _is_roadmap(e: QueueEntry) -> bool:
    u = (e.mode or "").upper()
    return "RESUME_ROADMAP" in u


def parse_queue_jsonl(text: str) -> list[QueueEntry]:
    out: list[QueueEntry] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        raw = json.loads(line)
        if not isinstance(raw, dict):
            continue
        if raw.get("queue_failed") is True:
            continue
        tags = raw.get("tags")
        if isinstance(tags, list) and "queue-failed" in tags:
            continue
        if "id" not in raw or "mode" not in raw:
            continue
        out.append(QueueEntry.model_validate(raw))
    return out


def load_queue_file(path: Path) -> list[QueueEntry]:
    """Strict load for CLI: file must exist; each non-empty line must be valid JSON + QueueEntry."""
    if not path.is_file():
        raise FileNotFoundError(f"Queue file does not exist or is not a file: {path.resolve()}")
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise OSError(f"Could not read queue file {path}: {e}") from e
    out: list[QueueEntry] = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"Queue file {path}: line {lineno}: invalid JSON: {e}") from e
        if not isinstance(raw, dict):
            raise ValueError(
                f"Queue file {path}: line {lineno}: expected a JSON object, got {type(raw).__name__}"
            )
        if raw.get("queue_failed") is True:
            continue
        tags = raw.get("tags")
        if isinstance(tags, list) and "queue-failed" in tags:
            continue
        if "id" not in raw or "mode" not in raw:
            raise ValueError(
                f"Queue file {path}: line {lineno}: queue entry must include 'id' and 'mode'"
            )
        try:
            out.append(QueueEntry.model_validate(raw))
        except ValidationError as e:
            raise ValueError(
                f"Queue file {path}: line {lineno}: invalid queue entry schema: {e}"
            ) from e
    return out


def print_plan_success_summary(plan: EatQueueRunPlan, decisions_log_path: Path) -> None:
    num_repair = sum(1 for i in plan.intents if i.queue_pass_phase == "repair")
    n = len(plan.intents)
    print(f"✅ eat_queue_run_plan.json generated successfully for parent_run_id: {plan.parent_run_id}")
    print(f"   Intents: {n} total ({num_repair} repair)")
    print(f"   Consumed IDs: {plan.consumed_ids}")
    print(f"   Decisions appended to: {decisions_log_path.resolve()}")


def route_post_lv(v: ValidationResult) -> str:
    """Map L1 post–little-val verdict to orchestration hint (deterministic)."""
    if v.recommended_action == "hard_block":
        return "stall_or_fail"
    if v.recommended_action == "repair_append":
        return "append_repair_line"
    return "inline_repair"


def _transition(
    state: _FsmState, event: str, decisions: list[dict[str, Any]], parent_run_id: str
) -> _FsmState:
    nxt = {
        (_FsmState.START, "partition"): _FsmState.PARTITIONED,
        (_FsmState.PARTITIONED, "plan_pass1"): _FsmState.PASS1_DONE,
        (_FsmState.PASS1_DONE, "plan_pass3"): _FsmState.PASS3_DONE,
        (_FsmState.PASS3_DONE, "emit"): _FsmState.EMITTED,
    }.get((state, event))
    if nxt is None:
        raise ValueError(f"invalid transition {state!s} + {event!r}")
    decisions.append(
        {
            "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "parent_run_id": parent_run_id,
            "rule_id": f"fsm:{state.value}->{nxt.value}",
            "from_state": state.value,
            "to_state": nxt.value,
            "queue_entry_id": None,
            "reason": event,
        }
    )
    return nxt


def build_plan(
    entries: list[QueueEntry],
    parent_run_id: str,
    *,
    lane_filter: str | None = None,
) -> tuple[EatQueueRunPlan, list[dict[str, Any]]]:
    decisions: list[dict[str, Any]] = []
    st = _FsmState.START
    st = _transition(st, "partition", decisions, parent_run_id)

    entries = filter_entries_by_lane(entries, lane_filter)

    by: dict[str, dict[str, list[QueueEntry]]] = defaultdict(lambda: {"forward": [], "repair": []})
    order: list[str] = []
    for e in entries:
        p = _pid(e)
        if p not in order:
            order.append(p)
        kind = "repair" if _is_repair(e) else "forward"
        by[p][kind].append(e)

    st = _transition(st, "plan_pass1", decisions, parent_run_id)
    intents: list[DispatchIntent] = []
    consumed: list[str] = []
    ordinal = 0

    for proj in order:
        b = by[proj]
        forwards = [e for e in b["forward"] if _is_roadmap(e)]
        repairs = [e for e in b["repair"] if _is_roadmap(e)]
        if forwards:
            f0 = forwards[0]
            ordinal += 1
            intents.append(
                DispatchIntent(
                    queue_entry_id=f0.id,
                    project_id=proj if proj != "_none" else _pid(f0),
                    queue_pass_phase="initial",
                    pass_id="pass1",
                    dispatch_ordinal=ordinal,
                )
            )
        if repairs and forwards:
            consumed.append(forwards[0].id)

    st = _transition(st, "plan_pass3", decisions, parent_run_id)
    for proj in order:
        repairs = [e for e in by[proj]["repair"] if _is_roadmap(e)]
        for r in repairs:
            ordinal += 1
            intents.append(
                DispatchIntent(
                    queue_entry_id=r.id,
                    project_id=proj if proj != "_none" else _pid(r),
                    queue_pass_phase="repair",
                    pass_id="pass3",
                    dispatch_ordinal=ordinal,
                )
            )

    plan = EatQueueRunPlan(parent_run_id=parent_run_id, intents=intents, consumed_ids=consumed)
    st = _transition(st, "emit", decisions, parent_run_id)
    assert st == _FsmState.EMITTED
    return plan, decisions


def append_decisions(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def emit_plan_json(plan: EatQueueRunPlan, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(plan.model_dump_json(indent=2) + "\n", encoding="utf-8")
