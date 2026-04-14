"""
Unified EAT-QUEUE harness CLI (single writer for PQ bytes).

Run from vault root::

    PYTHONPATH=scripts python3 -m eat_queue_core.harness snapshot --vault-root .
    PYTHONPATH=. python3 -m scripts.eat_queue_core.harness snapshot --vault-root .

See 3-Resources/Second-Brain/Docs/Queue-Harness-Architecture.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from .config_loader import (
    default_mutation_recovery_mode,
    max_midrun_appends,
    parse_queue_config,
    resolve_config_path,
)
from .full_cycle import apply_queue_cleanup, apply_queue_cleanup_dual_track, run_full_eat_queue_cycle
from .lanes import FALLBACK_ALLOWED_LANES, validate_lane_filter_token
from .plan import append_decisions, build_plan, emit_plan_json, load_queue_file, print_plan_success_summary
from .pool_sync import hydrate_track_pq_from_pool


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


def resolve_parallel_context(
    vault_root: Path,
    parallel_file: Path | None,
    parallel_yaml: str | None,
) -> dict[str, Any]:
    if parallel_file is not None:
        return _read_json_or_yaml_file(parallel_file.resolve())
    if parallel_yaml:
        raw = parallel_yaml.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            try:
                import yaml  # type: ignore[import-untyped]

                out = yaml.safe_load(raw)
            except ImportError as e:
                raise SystemExit(
                    "harness: parallel-context-yaml must be JSON unless PyYAML is installed"
                ) from e
            if not isinstance(out, dict):
                raise ValueError("parallel context must be an object")
            return out
    return {}


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
        vault_root, args.parallel_context_file, args.parallel_context_yaml
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
        vault_root, args.parallel_context_file, args.parallel_context_yaml
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
        vault_root, args.parallel_context_file, args.parallel_context_yaml
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


def cmd_append_entries(vault_root: Path, args: argparse.Namespace) -> int:
    parallel = resolve_parallel_context(
        vault_root, args.parallel_context_file, args.parallel_context_yaml
    )
    qpath, _ = resolve_queue_and_plan_paths(vault_root, queue=args.queue, parallel=parallel)
    cfg = parse_queue_config(args.resolved_config)
    max_a = max_midrun_appends(cfg)
    current = int(args.current_midrun_count)
    if args.lines_file:
        raw = Path(args.lines_file).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    nlines = len(lines)
    if current + nlines > max_a:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "queue_midrun_append_cap",
                    "max_midrun_jsonl_appends_per_eat_queue_run": max_a,
                    "current_midrun_count": current,
                    "requested_lines": nlines,
                }
            ),
            file=sys.stderr,
        )
        return 1
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
    qpath.parent.mkdir(parents=True, exist_ok=True)
    with open(qpath, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(
        json.dumps(
            {
                "ok": True,
                "appended": len(lines),
                "path": str(qpath),
                "midrun_count_after": current + len(lines),
            },
            indent=2,
        )
    )
    return 0


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
        vault_root, args.parallel_context_file, args.parallel_context_yaml
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
        vault_root, args.parallel_context_file, args.parallel_context_yaml
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
    if args.lane is not None:
        token = args.lane.strip().lower()
        if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
            print(f"harness full_cycle: invalid lane {token!r}", file=sys.stderr)
            return 1
        lane_filter = token

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
        )
    except (OSError, ValueError) as e:
        print(f"harness full_cycle error: {e}", file=sys.stderr)
        return 1
    print(result.model_dump_json(indent=2))
    return 0


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

    ap = sub.add_parser(
        "append_entries",
        help="Append JSONL lines to PQ with mid-run cap check (Step 0 / A.5x)",
        parents=[common],
    )
    add_parallel(ap)
    ap.add_argument(
        "--current-midrun-count",
        type=int,
        default=0,
        help="Appends already done this EAT-QUEUE run (default 0)",
    )
    ap.add_argument("--lines-file", type=Path, default=None, help="Path to JSONL lines (alternative to stdin)")
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
    pl.add_argument("--lane", type=str, default=None)
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
    fc.add_argument("--lane", type=str, default=None)
    fc.add_argument("--central-pool-fanout", action="store_true")
    fc.add_argument("--no-central-pool-fanout", action="store_true")
    fc.set_defaults(func=cmd_full_cycle)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = build_parser()
    args = p.parse_args(argv)
    vault_root = Path(args.vault_root or Path.cwd()).resolve()
    args.resolved_config = resolve_config_path(vault_root, getattr(args, "config", None))

    fn = args.func
    return int(fn(vault_root, args))


if __name__ == "__main__":
    raise SystemExit(main())
