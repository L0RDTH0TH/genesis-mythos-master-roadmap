"""
Unified EAT-QUEUE harness CLI (single writer for PQ bytes).

Run from vault root::

    PYTHONPATH=scripts python3 -m eat_queue_core.harness snapshot --vault-root .
    PYTHONPATH=. python3 -m scripts.eat_queue_core.harness snapshot --vault-root .

See 3-Resources/Second-Brain/Docs/Queue-Harness-Architecture.md

Telemetry field reference: ``scripts/eat_queue_core/docs/TELEMETRY_CONTRACT.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .a5b_dedupe import decide_append
from ._lock import acquire_gitforge_lock, release_gitforge_lock
from .config_loader import (
    default_mutation_recovery_mode,
    max_midrun_appends,
    origin_dedupe_window_hours,
    parse_queue_config,
    resolve_config_path,
)
from .full_cycle import (
    append_task_handoff_jsonl,
    apply_queue_cleanup,
    apply_queue_cleanup_dual_track,
    build_a5b_append_intent_receipt_row,
    effective_queue_lane,
    parallel_track_for_lane,
    run_full_eat_queue_cycle,
)
from .lane_queue_config import effective_max_inline_a5b
from .watcher_append import append_watcher_telemetry_line
from .models import QueueEntry
from .lanes import FALLBACK_ALLOWED_LANES, validate_lane_filter_token
from .plan import append_decisions, build_plan, emit_plan_json, load_queue_file, print_plan_success_summary
from .pool_sync import hydrate_track_pq_from_pool
from .post_queue_gitforge import load_handoff_json, run_post_queue_gitforge


def _read_json_or_yaml_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    text = text.strip()
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore[import-untyped]

            data = yaml.safe_load(text)
        except ImportError:
            raise SystemExit(
                "harness: PyYAML required for .yaml parallel-context files "
                "(pip install pyyaml) or use .json"
            ) from None
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("parallel context must be a JSON/YAML object")
    return data


def synthetic_parallel_context_for_lane(lane: str) -> dict[str, Any]:
    """Default parallel bundle for a queue lane (matches queue.mdc A.0x layout)."""
    lane = lane.strip().lower()
    tb = f".technical/parallel/{lane}"
    return {
        "parallel_track": lane,
        "technical_bundle_root": tb,
        "resolved_prompt_queue_path": f"{tb}/prompt-queue.jsonl",
    }


def _infer_lane_from_context_path(path: Path) -> str | None:
    """If path is like .../parallel/<lane>/..., return lane when it is an allowed token."""
    parts = [p.lower() for p in path.parts]
    try:
        i = parts.index("parallel")
    except ValueError:
        return None
    if i + 1 >= len(parts):
        return None
    cand = parts[i + 1]
    return cand if validate_lane_filter_token(cand, FALLBACK_ALLOWED_LANES) else None


def _parse_parallel_inline(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    try:
        out = json.loads(raw)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore[import-untyped]

            out = yaml.safe_load(raw)
        except ImportError as e:
            raise SystemExit(
                "harness: parallel-context-yaml must be JSON unless PyYAML is installed"
            ) from e
    if not isinstance(out, dict):
        raise SystemExit("harness: parallel-context-yaml must be a JSON/YAML object")
    return out


def resolve_parallel_context(
    vault_root: Path,
    parallel_file: Path | None,
    parallel_yaml: str | None,
    *,
    lane: str | None = None,
) -> dict[str, Any]:
    """
    Resolve parallel hand-off dict. If ``--parallel-context-file`` is missing on disk,
    use ``--lane`` or infer lane from ``.../parallel/<lane>/...`` and apply
    :func:`synthetic_parallel_context_for_lane` (stderr notice).

    When a context file exists and loads successfully, ``--parallel-context-yaml`` is ignored
    (legacy behavior). Inline YAML merges when no file was loaded from disk.
    """
    root = vault_root.resolve()
    out: dict[str, Any] = {}
    loaded_from_file = False

    if parallel_file is not None:
        p = parallel_file.expanduser()
        p = p if p.is_absolute() else (root / p)
        p = p.resolve()
        if p.is_file():
            out = dict(_read_json_or_yaml_file(p))
            loaded_from_file = True
        else:
            chosen: str | None = None
            if lane and str(lane).strip():
                t = lane.strip().lower()
                if validate_lane_filter_token(t, FALLBACK_ALLOWED_LANES):
                    chosen = t
                else:
                    raise SystemExit(
                        f"harness: invalid --lane {t!r}; expected one of {sorted(FALLBACK_ALLOWED_LANES)}"
                    )
            if chosen is None:
                chosen = _infer_lane_from_context_path(p)
            if chosen:
                print(
                    f"harness: parallel context file missing; using synthetic defaults for lane {chosen!r} ({p})",
                    file=sys.stderr,
                )
                out = synthetic_parallel_context_for_lane(chosen)
            else:
                raise SystemExit(
                    f"harness: parallel context file not found: {p}\n"
                    "Fix: create the file, pass --lane <godot|sandbox|...>, "
                    "or use --queue / --parallel-context-yaml with a JSON object."
                )
    elif lane and str(lane).strip():
        t = lane.strip().lower()
        if not validate_lane_filter_token(t, FALLBACK_ALLOWED_LANES):
            raise SystemExit(
                f"harness: invalid --lane {t!r}; expected one of {sorted(FALLBACK_ALLOWED_LANES)}"
            )
        out = synthetic_parallel_context_for_lane(t)

    if parallel_yaml and not loaded_from_file:
        extra = _parse_parallel_inline(parallel_yaml)
        out = {**out, **extra}
    return out


def _rel_vault(vault_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(vault_root.resolve()))
    except ValueError:
        return str(path)


def resolve_queue_and_plan_paths(
    vault_root: Path,
    *,
    queue: Path | None,
    parallel: dict[str, Any],
) -> tuple[Path, Path]:
    """Return (prompt_queue_path, eat_queue_run_plan_path)."""
    root = vault_root.resolve()
    if queue is not None:
        q = queue if queue.is_absolute() else (root / queue)
        q = q.resolve()
    else:
        rp = parallel.get("resolved_prompt_queue_path")
        if isinstance(rp, str) and rp.strip():
            q = (root / rp.strip()).resolve()
        else:
            q = (root / ".technical" / "prompt-queue.jsonl").resolve()
    plan = q.parent / "eat_queue_run_plan.json"
    return q, plan.resolve()


def cmd_snapshot(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()
    out: dict[str, Any] = {"vault_root": str(vault_root.resolve())}
    targets: list[tuple[str, Path]] = [("prompt_queue", qpath)]
    if cfg.get("central_pool_fanout_enabled") is True and qpath.resolve() != pool_default.resolve():
        targets.append(("central_pool", pool_default))
    for label, path in targets:
        if path.is_file():
            data = path.read_bytes()
            lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
            out[label] = {
                "path": _rel_vault(vault_root, path),
                "sha256": hashlib.sha256(data).hexdigest(),
                "line_count": len(lines),
            }
        else:
            out[label] = {
                "path": _rel_vault(vault_root, path),
                "sha256": None,
                "line_count": 0,
                "missing": True,
            }
    print(json.dumps(out, indent=2))
    return 0


def cmd_verify(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    expected_path = Path(args.expected_snapshot)
    if not expected_path.is_file():
        print(json.dumps({"ok": False, "error": "expected_snapshot file missing"}), file=sys.stderr)
        return 1
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()

    def snap_one(label: str, path: Path) -> dict[str, Any]:
        if not path.is_file():
            return {"path": str(path), "sha256": None, "line_count": 0, "missing": True}
        data = path.read_bytes()
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        return {
            "path": str(path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "line_count": len(lines),
        }

    current_prompt = snap_one("prompt_queue", qpath)
    checks = [("prompt_queue", qpath, expected.get("prompt_queue"))]
    if cfg.get("central_pool_fanout_enabled") is True and qpath.resolve() != pool_default.resolve():
        checks.append(("central_pool", pool_default, expected.get("central_pool")))

    mismatches: list[str] = []
    for label, path, exp in checks:
        if exp is None and label != "prompt_queue":
            continue
        cur = snap_one(label, path)
        if exp and exp.get("sha256") and cur.get("sha256") != exp.get("sha256"):
            mismatches.append(label)

    recovery = default_mutation_recovery_mode(cfg)
    ok = len(mismatches) == 0
    result = {
        "ok": ok,
        "mismatches": mismatches,
        "mutation_recovery_mode": recovery,
        "recovery_hint": (
            "no_action"
            if ok
            else (
                "refuse_rewrite_log_errors"
                if recovery == "hard_stop"
                else (
                    "rerun_full_cycle_from_disk"
                    if recovery == "restart_plan"
                    else "rewrite_using_latest_snapshot_and_plan_ids"
                )
            )
        ),
    }
    print(json.dumps(result, indent=2))
    return 0 if ok else 2


def cmd_rewrite_consumed(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, plan_path = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    ids: set[str] = set()
    if args.ids:
        ids = {x.strip() for x in args.ids.split(",") if x.strip()}
    if args.plan:
        raw = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        rw = raw.get("queue_rewrite_ids")
        if isinstance(rw, list):
            ids |= {str(x) for x in rw}
        cons = raw.get("consumed_ids")
        if isinstance(cons, list):
            ids |= {str(x) for x in cons}
        # EatQueueRunPlan model uses consumed_ids on plan object
        if not ids and "consumed_ids" in raw:
            c2 = raw.get("consumed_ids")
            if isinstance(c2, list):
                ids = {str(x) for x in c2}
    if not ids:
        print(json.dumps({"ok": False, "error": "no ids to remove; pass --ids or --plan"}))
        return 1
    cfg = parse_queue_config(args.resolved_config)
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()
    dual = (
        cfg.get("central_pool_fanout_enabled") is True
        and qpath.resolve() != pool_default.resolve()
        and not args.single_pool
    )
    if dual:
        tc, pc = apply_queue_cleanup_dual_track(qpath, pool_default, ids)
        out = {"ok": True, "track_pq_changed": tc, "central_pool_changed": pc, "removed_ids": sorted(ids)}
    else:
        ch = apply_queue_cleanup(qpath, ids)
        out = {"ok": True, "queue_changed": ch, "removed_ids": sorted(ids)}
    print(json.dumps(out, indent=2))
    return 0


def _resolve_parallel_track(parallel: dict[str, Any]) -> str:
    pt = parallel.get("parallel_track")
    if isinstance(pt, str) and pt.strip():
        return parallel_track_for_lane(pt.strip().lower())
    return parallel_track_for_lane(None)


def _append_prompt_queue_audit(audit_path: Path, record: dict[str, Any]) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    prev = audit_path.read_text(encoding="utf-8") if audit_path.is_file() else ""
    audit_path.write_text(prev + line, encoding="utf-8")


def _snap_one_queue(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"sha256": None, "line_count": 0, "missing": True}
    data = path.read_bytes()
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "line_count": len(lines),
    }


def _verify_snapshot_for_append(
    vault_root: Path,
    qpath: Path,
    expected_path: Path,
    cfg: dict[str, Any],
) -> tuple[bool, list[str]]:
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    pool_default = (vault_root / ".technical" / "prompt-queue.jsonl").resolve()
    mismatches: list[str] = []
    cur_p = _snap_one_queue(qpath)
    exp_p = expected.get("prompt_queue") or {}
    if exp_p.get("sha256") and cur_p.get("sha256") != exp_p.get("sha256"):
        mismatches.append("prompt_queue")
    if cfg.get("central_pool_fanout_enabled") is True and qpath.resolve() != pool_default.resolve():
        cur_c = _snap_one_queue(pool_default)
        exp_c = expected.get("central_pool") or {}
        if exp_c.get("sha256") and cur_c.get("sha256") != exp_c.get("sha256"):
            mismatches.append("central_pool")
    return len(mismatches) == 0, mismatches


def _pass3_repair_count_from_plan(plan_path: Path) -> int:
    if not plan_path.is_file():
        return 0
    try:
        data = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    intents = data.get("intents")
    if not isinstance(intents, list):
        return 0
    n = 0
    for it in intents:
        if not isinstance(it, dict):
            continue
        if it.get("pass_id") == "pass3" and it.get("queue_pass_phase") == "repair":
            n += 1
    return n


def _lane_token_for_config(parallel: dict[str, Any], first_entry: QueueEntry | None) -> str | None:
    pt = parallel.get("parallel_track")
    if isinstance(pt, str) and pt.strip():
        return pt.strip().lower()
    if first_entry is not None:
        return effective_queue_lane(first_entry) or None
    return None


def cmd_append_entries(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    max_a = max_midrun_appends(cfg)
    current = int(args.current_midrun_count)
    oh = origin_dedupe_window_hours(cfg)
    if getattr(args, "origin_dedupe_window_hours", None) is not None:
        try:
            oh = float(args.origin_dedupe_window_hours)
        except (TypeError, ValueError):
            pass

    req_snap = getattr(args, "require_snapshot_json", None)
    if req_snap:
        ok_snap, miss = _verify_snapshot_for_append(
            vault_root.resolve(), qpath, Path(req_snap), cfg
        )
        if not ok_snap:
            print(
                json.dumps({"ok": False, "error": "snapshot_mismatch", "mismatches": miss}),
                file=sys.stderr,
            )
            return 2

    if args.lines_file:
        raw = Path(args.lines_file).read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "append_entries_stdin_required",
                        "hint": "Provide JSONL via stdin (pipe or heredoc) or use --lines-file PATH. "
                        "Refusing to read from an interactive empty terminal (would block).",
                    }
                ),
                file=sys.stderr,
            )
            return 1
        raw = sys.stdin.read()
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    nlines = len(lines)
    candidates: list[tuple[QueueEntry, str]] = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"line {i+1} invalid json: {e}"}), file=sys.stderr)
            return 1
        if not isinstance(obj, dict) or "id" not in obj or "mode" not in obj:
            print(
                json.dumps({"ok": False, "error": f"line {i+1} missing id/mode"}),
                file=sys.stderr,
            )
            return 1
        try:
            candidates.append((QueueEntry.model_validate(obj), line))
        except ValidationError as e:
            print(
                json.dumps({"ok": False, "error": f"line {i+1} invalid queue entry: {e}"}),
                file=sys.stderr,
            )
            return 1

    root = vault_root.resolve()
    first_entry = candidates[0][0] if candidates else None
    lane_tok = _lane_token_for_config(parallel, first_entry)
    pass3_manual = int(getattr(args, "inline_pass3_repair_count", 0) or 0)
    plan_path_arg = getattr(args, "eat_queue_run_plan", None)
    plan_path = (
        Path(plan_path_arg).resolve()
        if plan_path_arg
        else (qpath.parent / "eat_queue_run_plan.json").resolve()
    )
    pass3_from_plan = _pass3_repair_count_from_plan(plan_path)
    pass3_used = pass3_manual if pass3_manual > 0 else pass3_from_plan
    max_inline = effective_max_inline_a5b(root, lane_tok)
    inline_budget_rem = max(0, max_inline - pass3_used)

    existing = load_queue_file(qpath) if qpath.is_file() else []
    pending: list[QueueEntry] = []
    to_write: list[str] = []
    dedupe_events: list[dict[str, Any]] = []
    audit_path = qpath.parent / "prompt-queue-audit.jsonl"
    comms_path = qpath.parent / "task-handoff-comms.jsonl"
    parallel_track = _resolve_parallel_track(parallel)
    parent_run_id = str(getattr(args, "parent_run_id", "eatq-append"))
    emit_audit = getattr(args, "emit_audit", True)
    emit_intent_receipt = getattr(args, "emit_intent_receipt", True)
    emit_watcher = getattr(args, "emit_watcher_result", True)
    dry_run = getattr(args, "dry_run", False)
    use_lock = getattr(args, "use_gitforge_lock", False)
    lock_track = parallel_track if parallel_track != "-" else "default"

    if use_lock and not dry_run:
        if not acquire_gitforge_lock(root, lock_track, 30.0):
            print(json.dumps({"ok": False, "error": "gitforge_lock_not_acquired"}), file=sys.stderr)
            return 1
    try:
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        for cand, raw_line in candidates:
            decision = decide_append(
                cand,
                existing,
                pending,
                origin_window_hours=oh,
            )
            oid = (cand.params or {}).get("origin_request_id") if isinstance(cand.params, dict) else None
            oid_s = oid.strip() if isinstance(oid, str) else None
            ev: dict[str, Any] = {
                "queue_entry_id": cand.id,
                "dedupe_attempted": decision.dedupe_attempted,
                "dedupe_suppressed": decision.dedupe_suppressed,
                "suppressed_by": decision.suppressed_by,
                "inline_drain_budget_remaining": inline_budget_rem,
            }
            if decision.audit_suppressed_by:
                ev["audit_suppressed_by"] = decision.audit_suppressed_by
            if decision.suppressing_entry_id:
                ev["suppressing_queue_entry_id"] = decision.suppressing_entry_id
            dedupe_events.append(ev)

            if emit_audit and not dry_run:
                rec_a: dict[str, Any] = {
                    "record_type": "a5b_enqueue_dedupe",
                    "iso_timestamp": now_iso,
                    "queue_entry_id": cand.id,
                    "dedupe_attempted": decision.dedupe_attempted,
                    "dedupe_suppressed": decision.dedupe_suppressed,
                    "suppressed_by": decision.suppressed_by,
                    "parent_run_id": parent_run_id,
                    "inline_drain_budget_remaining": inline_budget_rem,
                    "max_inline_a5b_effective": max_inline,
                    "pass3_repair_count_used": pass3_used,
                }
                if decision.audit_suppressed_by:
                    rec_a["audit_suppressed_by"] = decision.audit_suppressed_by
                if oid_s:
                    rec_a["origin_request_id"] = oid_s
                if decision.dedupe_suppressed:
                    rec_a["dedupe_suppressed_handoff_repair"] = True
                _append_prompt_queue_audit(audit_path, rec_a)

            if emit_intent_receipt and not dry_run:
                receipt = build_a5b_append_intent_receipt_row(
                    vault_root=root,
                    parent_run_id=parent_run_id,
                    entry=cand,
                    decision=decision,
                    parallel_track=parallel_track,
                    inline_drain_budget_remaining=inline_budget_rem,
                )
                append_task_handoff_jsonl(comms_path, receipt)

            if emit_watcher and not dry_run:
                trace_payload: dict[str, Any] = {
                    "source": "eat_queue_core_append_entries",
                    "record_type": "harness_append_telemetry",
                    "queue_entry_id": cand.id,
                    "parent_run_id": parent_run_id,
                    "parallel_track": parallel_track,
                    "queue_lane": effective_queue_lane(cand),
                    "dedupe_attempted": decision.dedupe_attempted,
                    "dedupe_suppressed": decision.dedupe_suppressed,
                    "suppressed_by": decision.suppressed_by,
                    "inline_drain_budget_remaining": inline_budget_rem,
                    "max_inline_a5b_effective": max_inline,
                    "pass3_repair_count_used": pass3_used,
                }
                if decision.audit_suppressed_by:
                    trace_payload["audit_suppressed_by"] = decision.audit_suppressed_by
                append_watcher_telemetry_line(
                    root,
                    request_id=f"harness-append-{cand.id}",
                    message="harness append_entries telemetry",
                    trace_payload=trace_payload,
                )

            if not decision.dedupe_suppressed:
                to_write.append(raw_line)
                pending.append(cand)

        n_append = len(to_write)
        if current + n_append > max_a:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "queue_midrun_append_cap",
                        "max_midrun_jsonl_appends_per_eat_queue_run": max_a,
                        "current_midrun_count": current,
                        "requested_lines": nlines,
                        "would_append_after_dedupe": n_append,
                    }
                ),
                file=sys.stderr,
            )
            return 1

        if not dry_run:
            qpath.parent.mkdir(parents=True, exist_ok=True)
            with open(qpath, "a", encoding="utf-8") as f:
                for raw_line in to_write:
                    f.write(raw_line + "\n")

        out: dict[str, Any] = {
            "ok": True,
            "dry_run": dry_run,
            "appended": n_append,
            "requested_lines": nlines,
            "suppressed_count": nlines - n_append,
            "path": str(qpath),
            "midrun_count_after": current + (0 if dry_run else n_append),
            "dedupe_events": dedupe_events,
            "inline_drain_budget_remaining": inline_budget_rem,
            "max_inline_a5b_effective": max_inline,
            "pass3_repair_count_used": pass3_used,
        }
        print(json.dumps(out, indent=2))
        return 0
    finally:
        if use_lock and not dry_run:
            release_gitforge_lock(root)


def cmd_pool_sync(vault_root: Path, args: argparse.Namespace) -> int:
    lane = args.lane.strip().lower()
    target = args.target_pq
    if not target.is_absolute():
        target = (vault_root / target).resolve()
    res = hydrate_track_pq_from_pool(
        vault_root=vault_root.resolve(),
        lane_filter=lane,
        target_pq=target,
        pool_path=args.pool,
        dry_run=args.dry_run,
        strict_central_only=True if args.strict_central_only else None,
    )
    print(res.model_dump_json(indent=2))
    return 0 if res.ok else 1


def cmd_plan(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, emit = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    if args.emit:
        emit = args.emit if args.emit.is_absolute() else (vault_root / args.emit)
    dlog = args.decisions_log
    if dlog is None:
        dlog = qpath.parent / "eat-queue-decisions.jsonl"
    elif not dlog.is_absolute():
        dlog = vault_root / dlog
    lane_filter: str | None = None
    if args.lane is not None:
        token = args.lane.strip().lower()
        if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
            print(f"harness plan: invalid lane {token!r}", file=sys.stderr)
            return 1
        lane_filter = token
    try:
        entries = load_queue_file(qpath)
        plan, decisions = build_plan(entries, args.parent_run_id, lane_filter=lane_filter)
        emit_plan_json(plan, emit)
        append_decisions(dlog, decisions)
    except (OSError, ValueError) as e:
        print(f"harness plan error: {e}", file=sys.stderr)
        return 1
    print_plan_success_summary(plan, dlog)
    if args.verbose:
        print(plan.model_dump_json(indent=2))
    return 0


def cmd_full_cycle(vault_root: Path, args: argparse.Namespace) -> int:
    """Delegate to full_cycle.run_full_eat_queue_cycle; print JSON result."""
    parallel = resolve_parallel_context(
        vault_root,
        args.parallel_context_file,
        args.parallel_context_yaml,
        lane=getattr(args, "lane", None),
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    emit = args.emit
    if emit is None:
        emit = qpath.parent / "eat_queue_run_plan.json"
    elif not emit.is_absolute():
        emit = vault_root / emit
    dlog = args.decisions_log
    if dlog is None:
        dlog = qpath.parent / "eat-queue-decisions.jsonl"
    elif not dlog.is_absolute():
        dlog = vault_root / dlog

    lane_filter: str | None = None
    lane_project_id: str | None = None
    if args.lane is not None:
        token = args.lane.strip().lower()
        if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
            print(f"harness full_cycle: invalid lane {token!r}", file=sys.stderr)
            return 1
        lane_filter = token
    raw_lane_project_id = parallel.get("lane_project_id")
    if isinstance(raw_lane_project_id, str) and raw_lane_project_id.strip():
        lane_project_id = raw_lane_project_id.strip()

    cpf: bool | None = None
    if args.no_central_pool_fanout:
        cpf = False
    elif args.central_pool_fanout:
        cpf = True

    try:
        result = run_full_eat_queue_cycle(
            initial_action=args.action,
            initial_profile=args.profile,
            max_passes=args.max_passes,
            strict_mode=args.strict_mode,
            vault_root=vault_root.resolve(),
            queue_path=qpath,
            plan_path=emit,
            decisions_path=dlog,
            parent_run_id=args.parent_run_id,
            lane_filter=lane_filter,
            apply_cleanup=args.apply_cleanup,
            central_pool_fanout=cpf,
            lane_project_id=lane_project_id,
            emit_watcher_result=getattr(args, "emit_watcher_result", True),
        )
    except (OSError, ValueError) as e:
        print(f"harness full_cycle error: {e}", file=sys.stderr)
        return 1
    print(result.model_dump_json(indent=2))
    return 0


def cmd_post_queue_gitforge(vault_root: Path, args: argparse.Namespace) -> int:
    """Layer 1 post–A.7 deterministic GitForge (lock, vault git, optional export, audit)."""
    try:
        if getattr(args, "handoff_file", None) is not None:
            handoff = load_handoff_json(args.handoff_file, None)
        else:
            handoff = load_handoff_json(None, sys.stdin.read())
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"ok": False, "error": f"handoff: {e}"}), file=sys.stderr)
        return 1
    result = run_post_queue_gitforge(vault_root, handoff, args.resolved_config)
    print(result.to_json())
    return result.exit_code


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--vault-root", type=Path, default=None, help="Vault root (default: cwd)")
    common.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Second-Brain-Config.md path (default: Docs/Core or legacy paths)",
    )
    # Common flags live on each subparser only so ``harness snapshot --vault-root .`` works.
    p = argparse.ArgumentParser(
        prog="eat_queue_core.harness",
        description="EAT-QUEUE harness (PQ single writer)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_parallel(s: argparse.ArgumentParser) -> None:
        s.add_argument("--queue", type=Path, default=None, help="prompt-queue.jsonl (override parallel context)")
        s.add_argument(
            "--lane",
            type=str,
            default=None,
            help="Queue lane (godot, sandbox, …): synthetic parallel_track + PQ path when context file is missing",
        )
        s.add_argument(
            "--parallel-context-file",
            type=Path,
            default=None,
            help="JSON/YAML with resolved_prompt_queue_path / technical_bundle_root",
        )
        s.add_argument("--parallel-context-yaml", default=None, help="Inline JSON object string for parallel context")

    sp = sub.add_parser(
        "snapshot",
        help="SHA256 + line counts for PQ (and central pool when fanout)",
        parents=[common],
    )
    add_parallel(sp)
    sp.set_defaults(func=cmd_snapshot)

    vp = sub.add_parser(
        "verify",
        help="Compare current PQ bytes to a prior snapshot JSON",
        parents=[common],
    )
    add_parallel(vp)
    vp.add_argument("--expected-snapshot", type=Path, required=True, help="JSON file from harness snapshot")
    vp.set_defaults(func=cmd_verify)

    rp = sub.add_parser(
        "rewrite_consumed",
        help="Remove consumed ids from PQ (and central pool when dual-track)",
        parents=[common],
    )
    add_parallel(rp)
    rp.add_argument("--ids", default=None, help="Comma-separated queue entry ids to remove")
    rp.add_argument("--plan", type=Path, default=None, help="eat_queue_run_plan.json (queue_rewrite_ids / consumed_ids)")
    rp.add_argument(
        "--single-pool",
        action="store_true",
        help="Only rewrite the track PQ, not the central pool",
    )
    rp.set_defaults(func=cmd_rewrite_consumed)

    _APPEND_ENTRIES_EPILOG = """
Examples — JSONL must come from stdin (heredoc/pipe) or --lines-file:

  Dry-run + snapshot gate:
    PYTHONPATH=. python3 -m scripts.eat_queue_core.harness append_entries \\
      --vault-root . --lane godot --dry-run \\
      --require-snapshot-json /tmp/godot-pq-snapshot.json <<'EOF'
    {"id":"x","mode":"HANDOFF_AUDIT_REPAIR","params":{"origin_request_id":"o","user_guidance":"y"}}
    EOF

  Search eat_queue_core (run as its own command — never append grep to append_entries):
    grep -rE "dedupe|TELEMETRY_CONTRACT" scripts/eat_queue_core/ --include='*.py' --include='*.md'
"""

    ap = sub.add_parser(
        "append_entries",
        help="Append JSONL lines to PQ with A.5b.0z dedupe, audit + intent_actual_receipt telemetry (Step 0 / A.5x)",
        parents=[common],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_APPEND_ENTRIES_EPILOG,
    )
    add_parallel(ap)
    ap.add_argument(
        "--current-midrun-count",
        type=int,
        default=0,
        help="Appends already done this EAT-QUEUE run (default 0)",
    )
    ap.add_argument("--lines-file", type=Path, default=None, help="Path to JSONL lines (alternative to stdin)")
    ap.add_argument("--parent-run-id", default="eatq-append", help="Telemetry parent_run_id for audit/comms rows")
    ap.add_argument(
        "--emit-audit",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append a5b_enqueue_dedupe rows to prompt-queue-audit.jsonl (default: true)",
    )
    ap.add_argument(
        "--emit-intent-receipt",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append intent_actual_receipt rows to task-handoff-comms.jsonl (default: true)",
    )
    ap.add_argument(
        "--emit-watcher-result",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append harness telemetry lines to canonical Watcher-Result.md (default: true)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print JSON outcome only; do not write PQ, audit, comms, or Watcher",
    )
    ap.add_argument(
        "--require-snapshot",
        "--require-snapshot-json",
        dest="require_snapshot_json",
        type=Path,
        default=None,
        metavar="PATH",
        help="JSON from harness snapshot; refuse append if PQ/pool sha256 mismatch",
    )
    ap.add_argument(
        "--inline-pass3-repair-count",
        type=int,
        default=0,
        help="Pass3 repair intents already consumed this run (overrides eat-queue-run-plan when >0)",
    )
    ap.add_argument(
        "--eat-queue-run-plan",
        type=Path,
        default=None,
        help="eat_queue_run_plan.json to count pass3 repair rows (default: next to PQ)",
    )
    ap.add_argument(
        "--origin-dedupe-window-hours",
        type=float,
        default=None,
        help="Override config origin dedupe window (hours)",
    )
    ap.add_argument(
        "--use-gitforge-lock",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Acquire gitforge lock around PQ append (default: false)",
    )
    ap.set_defaults(func=cmd_append_entries)

    ps = sub.add_parser(
        "pool_sync",
        help="Central pool → track PQ hydration",
        parents=[common],
    )
    ps.add_argument("--lane", type=str, required=True)
    ps.add_argument("--target-pq", type=Path, required=True)
    ps.add_argument("--pool", type=Path, default=None)
    ps.add_argument("--strict-central-only", action="store_true")
    ps.add_argument("--dry-run", action="store_true")
    ps.set_defaults(func=cmd_pool_sync)

    pl = sub.add_parser("plan", help="Emit eat_queue_run_plan.json", parents=[common])
    add_parallel(pl)
    pl.add_argument("--emit", type=Path, required=True)
    pl.add_argument("--decisions-log", type=Path, default=None)
    pl.add_argument("--parent-run-id", default="eatq-local")
    pl.add_argument("--verbose", action="store_true")
    pl.set_defaults(func=cmd_plan)

    fc = sub.add_parser(
        "full_cycle",
        help="Reactive multi-pass plan (run_full_eat_queue_cycle)",
        parents=[common],
    )
    add_parallel(fc)
    fc.add_argument("--emit", type=Path, default=None)
    fc.add_argument("--decisions-log", type=Path, default=None)
    fc.add_argument("--parent-run-id", default=None)
    fc.add_argument("--action", default="deepen")
    fc.add_argument("--profile", default="balance")
    fc.add_argument("--max-passes", type=int, default=2)
    fc.add_argument("--strict-mode", action=argparse.BooleanOptionalAction, default=True)
    fc.add_argument("--apply-cleanup", action="store_true")
    fc.add_argument("--central-pool-fanout", action="store_true")
    fc.add_argument("--no-central-pool-fanout", action="store_true")
    fc.add_argument(
        "--emit-watcher-result",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Append plan-level telemetry to Watcher-Result when intent receipts enabled (default: true)",
    )
    fc.set_defaults(func=cmd_full_cycle)

    pg = sub.add_parser(
        "post_queue_gitforge",
        help="Post–A.7 GitForge: lock, vault git, optional export sync, audit log",
        parents=[common],
    )
    add_parallel(pg)
    pg.add_argument(
        "--handoff-file",
        type=Path,
        default=None,
        help="JSON hand-off (A.7a). If omitted, read JSON object from stdin.",
    )
    pg.set_defaults(func=cmd_post_queue_gitforge)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    # Catch common copy-paste: append_entries … --inline-grep … (grep is not a harness flag).
    if "append_entries" in argv and "--inline-grep" in argv:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "merged_grep_with_append_entries",
                    "hint": "Do not paste grep into the append_entries line. Run append_entries "
                    "with a heredoc, pipe, or --lines-file, then run grep as a separate command. "
                    "See: python3 -m scripts.eat_queue_core.harness append_entries --help",
                }
            ),
            file=sys.stderr,
        )
        return 2
    p = build_parser()
    args = p.parse_args(argv)
    vault_root = Path(args.vault_root or Path.cwd()).resolve()
    args.resolved_config = resolve_config_path(vault_root, getattr(args, "config", None))

    fn = args.func
    return int(fn(vault_root, args))


if __name__ == "__main__":
    raise SystemExit(main())
