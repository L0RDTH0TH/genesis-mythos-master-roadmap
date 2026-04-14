#!/usr/bin/env python3
"""
Durable gate streak + pivot hints for Layer 1 EAT-QUEUE (anti-spin).
See 3-Resources/Second-Brain/Docs/Queue-Gate-State-Spec.md

Modes:
  report          -- JSON on stdout: gate_streak, gate_signature, need_class, pivot, threshold_met, ...
  validate-line   -- read one JSONL queue line from stdin; if pivot required, print mutated line
  record-outcome  -- read one JSON object from stdin; update gate state file (single writer)

Defaults for thresholds match Second-Brain-Config.md queue: section when parse fails.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_THRESHOLD = 2
DEFAULT_COOLDOWN = 1
DEFAULT_ORCHESTRATOR_PLAN = ".technical/eat_queue_run_plan.json"
TRACKS = frozenset({"conceptual", "execution"})
# Only these keys are read from Second-Brain-Config.md queue: block (ignore nested blocks like decisions_preflight).
CONFIG_QUEUE_KEYS = frozenset(
    {
        "gate_block_streak_threshold",
        "prefer_track_shift_on_gate_block",
        "gate_block_detection_enabled",
        "gate_state_path",
        "deterministic_gate_script_enabled",
        "deterministic_gate_script_path",
        "gate_block_same_track_cooldown_runs",
        "gate_key_includes_track",
        "python_orchestrator_enabled",
        "mutation_recovery_mode",
        "harness_validation_mode",
        "max_midrun_jsonl_appends_per_eat_queue_run",
    }
)


def _relative_to_vault(path: Path, vault: Path) -> str:
    try:
        return str(path.relative_to(vault))
    except ValueError:
        return str(path)


def opposite_track(track: str | None) -> str:
    t = (track or "").strip().lower()
    if t == "conceptual":
        return "execution"
    if t == "execution":
        return "conceptual"
    return "execution"


def parse_queue_config(config_path: Path) -> dict[str, Any]:
    """Extract queue.* scalars from Second-Brain-Config.md (markdown + yaml-like)."""
    out: dict[str, Any] = {}
    if not config_path.is_file():
        return out
    text = config_path.read_text(encoding="utf-8", errors="replace")
    in_queue = False
    indent_queue = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.match(r"^queue:\s*$", stripped):
            in_queue = True
            indent_queue = len(line) - len(line.lstrip())
            continue
        if in_queue:
            indent = len(line) - len(line.lstrip())
            if indent <= indent_queue and stripped and not stripped.startswith("#"):
                break
            m = re.match(r"^(\s*)([a-z_]+):\s*(.+?)\s*$", line)
            if m:
                key, val = m.group(2), m.group(3).strip()
                if key not in CONFIG_QUEUE_KEYS:
                    continue
                if val.startswith("#"):
                    val = val.split("#", 1)[0].strip()
                if val in ("true", "false"):
                    out[key] = val == "true"
                elif val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    out[key] = int(val)
                else:
                    out[key] = val.strip("\"'")
    return out


def warn_orchestrator_plan_missing(cfg: dict[str, Any], vault_root: Path) -> None:
    """If python orchestrator is enabled but the plan file is absent, warn on stderr (non-fatal)."""
    if cfg.get("python_orchestrator_enabled") is not True:
        print(
            "queue-gate-compute: warning: queue.python_orchestrator_enabled should be true "
            "(harness-only dispatch; see Docs/Queue-Harness-Architecture.md).",
            file=sys.stderr,
        )
        return
    plan_path = vault_root / DEFAULT_ORCHESTRATOR_PLAN
    if not plan_path.is_file():
        print(
            "queue-gate-compute: warning: queue.python_orchestrator_enabled is true but "
            f"eat_queue_run_plan.json is missing: {plan_path}",
            file=sys.stderr,
        )


def gate_state_path(vault_root: Path, cfg: dict[str, Any]) -> Path:
    rel = cfg.get("gate_state_path") or ".technical/queue-gate-state.json"
    return vault_root / rel


def load_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"version": 1, "entries": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"version": 1, "entries": {}}
    if not isinstance(data, dict):
        return {"version": 1, "entries": {}}
    data.setdefault("version", 1)
    data.setdefault("entries", {})
    if not isinstance(data["entries"], dict):
        data["entries"] = {}
    return data


def save_state(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_gate_key(
    project_id: str,
    gate_signature: str,
    *,
    effective_track: str | None = None,
    includes_track: bool = True,
) -> str:
    t = (effective_track or "conceptual").strip().lower()
    if t not in TRACKS:
        t = "conceptual"
    if includes_track:
        return f"{project_id}|{t}|{gate_signature}"
    return f"{project_id}|{gate_signature}"


def cmd_report(args: argparse.Namespace) -> int:
    vault = Path(args.vault_root).resolve()
    cfg_path = vault / "3-Resources" / "Second-Brain-Config.md"
    cfg = parse_queue_config(cfg_path)
    warn_orchestrator_plan_missing(cfg, vault)
    warn_advisory_queue_harness_keys(cfg)
    threshold = int(cfg.get("gate_block_streak_threshold", DEFAULT_THRESHOLD))
    prefer_pivot = cfg.get("prefer_track_shift_on_gate_block", True) is not False
    state_path = gate_state_path(vault, cfg)
    state = load_state(state_path)

    project_id = args.project_id or ""
    gate_sig = args.gate_signature or "unknown"
    inc = cfg.get("gate_key_includes_track", True) is not False
    etrack = (getattr(args, "effective_track", None) or "conceptual").strip().lower()
    if etrack not in TRACKS:
        etrack = "conceptual"
    gate_key = (
        make_gate_key(project_id, gate_sig, effective_track=etrack, includes_track=inc)
        if project_id
        else ""
    )
    entry = state["entries"].get(gate_key, {}) if gate_key else {}
    streak = int(entry.get("gate_streak", 0))
    blocked = entry.get("blocked_track") or args.blocked_track or "conceptual"
    pivot = opposite_track(str(blocked)) if prefer_pivot else str(blocked)
    threshold_met = bool(cfg.get("gate_block_detection_enabled", True)) and streak >= threshold
    need_class = "gate_block" if threshold_met else "unknown"

    out = {
        "gate_streak": streak,
        "gate_signature": gate_sig,
        "gate_key": gate_key,
        "blocked_track": blocked,
        "pivot_to_track": pivot,
        "threshold_met": threshold_met,
        "gate_block_streak_threshold": threshold,
        "need_class": need_class,
        "state_path": _relative_to_vault(state_path, vault),
        "entries_count": len(state["entries"]),
    }
    print(json.dumps(out, indent=2))
    return 0


def warn_advisory_queue_harness_keys(cfg: dict[str, Any]) -> None:
    """Log if canonical harness keys are absent from parsed queue: block (forks may omit)."""
    for key in ("mutation_recovery_mode", "harness_validation_mode"):
        if key not in cfg:
            print(
                f"queue-gate-compute: advisory: queue.{key} not set in Config queue: block "
                f"(defaults apply; see Docs/Core/Second-Brain-Config.md).",
                file=sys.stderr,
            )


def cmd_validate_line(args: argparse.Namespace) -> int:
    vault = Path(args.vault_root).resolve()
    cfg_path = vault / "3-Resources" / "Second-Brain-Config.md"
    cfg = parse_queue_config(cfg_path)
    warn_orchestrator_plan_missing(cfg, vault)
    warn_advisory_queue_harness_keys(cfg)
    threshold = int(cfg.get("gate_block_streak_threshold", DEFAULT_THRESHOLD))
    prefer_pivot = cfg.get("prefer_track_shift_on_gate_block", True) is not False
    state_path = gate_state_path(vault, cfg)
    state = load_state(state_path)

    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "empty_stdin"}), file=sys.stderr)
        return 2
    try:
        line = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "invalid_jsonl", "detail": str(e)}), file=sys.stderr)
        return 2

    params = line.get("params") or {}
    project_id = params.get("project_id") or line.get("project_id") or ""
    action = (params.get("action") or "").lower()
    cli_track = (getattr(args, "effective_track", None) or "").strip().lower()
    track = (
        params.get("effective_track")
        or line.get("effective_track")
        or (cli_track if cli_track in TRACKS else None)
        or params.get("roadmap_track")
        or "conceptual"
    )
    track = str(track).lower()
    if track not in TRACKS:
        track = "conceptual"

    gate_sig = args.gate_signature or "unknown"
    inc = cfg.get("gate_key_includes_track", True) is not False
    gate_key = make_gate_key(str(project_id), gate_sig, effective_track=track, includes_track=inc)
    entry = state["entries"].get(gate_key, {})
    streak = int(entry.get("gate_streak", 0))
    blocked = entry.get("blocked_track") or track
    pivot = opposite_track(str(blocked)) if prefer_pivot else str(blocked)
    threshold_met = bool(cfg.get("gate_block_detection_enabled", True)) and streak >= threshold

    if (
        threshold_met
        and action in ("deepen", "recal")
        and track == blocked
        and not params.get("roadmap_track_user_locked")
    ):
        params = dict(params)
        params["roadmap_track"] = pivot
        ug = params.get("user_guidance") or ""
        suffix = " [layer1_gate_pivot_override: same-track deepen/recal suppressed under gate_block streak; pivot_to_track=%s]" % pivot
        params["user_guidance"] = (ug + suffix).strip()
        line = dict(line)
        line["params"] = params

    print(json.dumps(line, ensure_ascii=False))
    return 0


def cmd_record_outcome(args: argparse.Namespace) -> int:
    vault = Path(args.vault_root).resolve()
    cfg_path = vault / "3-Resources" / "Second-Brain-Config.md"
    cfg = parse_queue_config(cfg_path)
    warn_orchestrator_plan_missing(cfg, vault)
    warn_advisory_queue_harness_keys(cfg)
    threshold = int(cfg.get("gate_block_streak_threshold", DEFAULT_THRESHOLD))
    cooldown = int(cfg.get("gate_block_same_track_cooldown_runs", DEFAULT_COOLDOWN))
    prefer_pivot = cfg.get("prefer_track_shift_on_gate_block", True) is not False
    state_path = gate_state_path(vault, cfg)

    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "empty_stdin"}), file=sys.stderr)
        return 2
    try:
        event = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "invalid_json", "detail": str(e)}), file=sys.stderr)
        return 2

    project_id = str(event.get("project_id") or "")
    if not project_id:
        print(json.dumps({"error": "project_id_required"}), file=sys.stderr)
        return 2

    state = load_state(state_path)
    entries: dict[str, Any] = state["entries"]
    completed_iso = str(event.get("completed_iso") or "")
    queue_entry_id = str(event.get("queue_entry_id") or "")
    hard_block = bool(event.get("hard_block"))
    gate_signature = str(event.get("gate_signature") or event.get("primary_code") or "unknown")
    blocked_track = str(
        event.get("blocked_track") or event.get("effective_track") or "conceptual"
    ).lower()
    if blocked_track not in TRACKS:
        blocked_track = "conceptual"
    track_lock = bool(event.get("track_lock_explicit"))
    inc = cfg.get("gate_key_includes_track", True) is not False

    gate_key = make_gate_key(
        project_id, gate_signature, effective_track=blocked_track, includes_track=inc
    )

    if hard_block and not track_lock:
        rec = entries.get(gate_key, {})
        streak = int(rec.get("gate_streak", 0)) + 1
        pivot = opposite_track(blocked_track) if prefer_pivot else blocked_track
        entries[gate_key] = {
            "gate_streak": streak,
            "last_queue_entry_id": queue_entry_id,
            "last_completed_iso": completed_iso,
            "blocked_track": blocked_track,
            "pivot_to_track": pivot,
        }
    else:
        # Decay all keys for this project
        prefix = project_id + "|"
        for k in list(entries.keys()):
            if k.startswith(prefix):
                rec = entries[k]
                streak = max(0, int(rec.get("gate_streak", 0)) - cooldown)
                if streak == 0:
                    del entries[k]
                else:
                    rec["gate_streak"] = streak
                    rec["last_completed_iso"] = completed_iso
                    entries[k] = rec

    save_state(state_path, state)

    rec = entries.get(gate_key, {})
    out = {
        "ok": True,
        "gate_key": gate_key,
        "gate_streak": int(rec.get("gate_streak", 0)),
        "threshold_met": bool(cfg.get("gate_block_detection_enabled", True))
        and int(rec.get("gate_streak", 0)) >= threshold,
    }
    print(json.dumps(out, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Queue gate streak / pivot helper")
    p.add_argument("--vault-root", default=".", help="Vault root (default: cwd)")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("report", help="Print JSON report for project/gate")
    pr.add_argument("--project-id", default="")
    pr.add_argument("--gate-signature", default="unknown")
    pr.add_argument("--blocked-track", default="")
    pr.add_argument(
        "--effective-track",
        default="conceptual",
        help="conceptual|execution for gate_key when gate_key_includes_track",
    )
    pr.set_defaults(func=cmd_report)

    pv = sub.add_parser("validate-line", help="Read one queue JSON line from stdin; apply pivot if needed")
    pv.add_argument("--gate-signature", default="unknown", help="Gate signature to look up streak for")
    pv.add_argument(
        "--effective-track",
        default="",
        help="Override track for gate_key when line omits params.effective_track",
    )
    pv.set_defaults(func=cmd_validate_line)

    po = sub.add_parser("record-outcome", help="Read JSON event from stdin; update gate state")
    po.set_defaults(func=cmd_record_outcome)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
