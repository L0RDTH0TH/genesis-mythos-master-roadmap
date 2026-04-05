from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

from .lanes import FALLBACK_ALLOWED_LANES, validate_lane_filter_token
from .plan import (
    append_decisions,
    build_plan,
    emit_plan_json,
    load_queue_file,
    print_plan_success_summary,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="eat_queue_core")
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan", help="Emit eat_queue_run_plan.json from prompt-queue JSONL")
    pl.add_argument("--queue", type=Path, required=True, help="Path to prompt-queue.jsonl")
    pl.add_argument("--emit", type=Path, required=True, help="Output eat_queue_run_plan.json")
    pl.add_argument(
        "--decisions-log",
        type=Path,
        default=None,
        help="Append FSM transitions to this JSONL (default: .technical/eat-queue-decisions.jsonl under cwd)",
    )
    pl.add_argument("--parent-run-id", default="eatq-local", help="Telemetry parent_run_id")
    pl.add_argument(
        "--lane",
        type=str,
        default=None,
        help="queue_lane_filter (sandbox/godot/core ∪ shared; shared only; default only). Must be in allowed_lanes.",
    )
    pl.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print full plan JSON after success summary",
    )
    args = p.parse_args(argv)

    if args.cmd != "plan":
        return 1

    dlog = args.decisions_log
    if dlog is None:
        dlog = Path(".technical/eat-queue-decisions.jsonl")

    try:
        lane_filter: str | None = None
        if args.lane is not None:
            token = args.lane.strip().lower()
            if not validate_lane_filter_token(token, FALLBACK_ALLOWED_LANES):
                print(
                    f"eat_queue_core plan error: lane {token!r} not in allowed_lanes "
                    f"({sorted(FALLBACK_ALLOWED_LANES)})",
                    file=sys.stderr,
                )
                return 1
            lane_filter = token
        entries = load_queue_file(args.queue)
        plan, decisions = build_plan(entries, args.parent_run_id, lane_filter=lane_filter)
        emit_plan_json(plan, args.emit)
        append_decisions(dlog, decisions)
    except (OSError, ValueError) as e:
        print(f"eat_queue_core plan error: {e}", file=sys.stderr)
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"eat_queue_core plan failed: {e}", file=sys.stderr)
        traceback.print_exc()
        return 1

    print_plan_success_summary(plan, dlog)
    if args.verbose:
        print(plan.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
