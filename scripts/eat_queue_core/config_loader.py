"""Parse `queue:` scalars from Second-Brain-Config.md for harness / Layer 1."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# Paths tried in order (first existing wins when --config omitted).
DEFAULT_CONFIG_CANDIDATES: tuple[str, ...] = (
    "3-Resources/Second-Brain/Docs/Core/Second-Brain-Config.md",
    "3-Resources/Second-Brain-Config.md",
    "3-Resources/Second-Brain/Second-Brain-Config.md",
)

# Keys consumed by harness, queue-gate-compute, and pool_sync (single parser).
HARNESS_QUEUE_KEYS = frozenset(
    {
        "python_orchestrator_enabled",
        "central_pool_fanout_enabled",
        "pool_sync_strict_central_only",
        "harness_validation_mode",
        "mutation_recovery_mode",
        "max_midrun_jsonl_appends_per_eat_queue_run",
        "gate_block_streak_threshold",
        "prefer_track_shift_on_gate_block",
        "gate_block_detection_enabled",
        "gate_state_path",
        "deterministic_gate_script_enabled",
        "deterministic_gate_script_path",
        "gate_block_same_track_cooldown_runs",
        "gate_key_includes_track",
    }
)


def resolve_config_path(vault_root: Path, explicit: Path | None) -> Path:
    """Return config file path; prefer explicit when provided and exists."""
    root = vault_root.resolve()
    if explicit is not None:
        p = explicit if explicit.is_absolute() else (root / explicit)
        return p.resolve()
    for rel in DEFAULT_CONFIG_CANDIDATES:
        cand = root / rel
        if cand.is_file():
            return cand.resolve()
    return (root / DEFAULT_CONFIG_CANDIDATES[0]).resolve()


def parse_queue_config(config_path: Path) -> dict[str, Any]:
    """Extract queue.* scalars from Second-Brain-Config.md (markdown + yaml-like block)."""
    out: dict[str, Any] = {}
    if not config_path.is_file():
        return out
    text = config_path.read_text(encoding="utf-8", errors="replace")
    in_queue = False
    indent_queue: int | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.match(r"^queue:\s*$", stripped):
            in_queue = True
            indent_queue = len(line) - len(line.lstrip())
            continue
        if in_queue:
            assert indent_queue is not None
            indent = len(line) - len(line.lstrip())
            if indent <= indent_queue and stripped and not stripped.startswith("#"):
                break
            m = re.match(r"^(\s*)([a-z_]+):\s*(.+?)\s*$", line)
            if m:
                key, val = m.group(2), m.group(3).strip()
                if key not in HARNESS_QUEUE_KEYS:
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


def default_mutation_recovery_mode(cfg: dict[str, Any]) -> str:
    raw = (cfg.get("mutation_recovery_mode") or "restart_plan") or "restart_plan"
    s = str(raw).strip().lower()
    if s in ("hard_stop", "restart_plan", "continue_best_effort"):
        return s
    return "restart_plan"


def max_midrun_appends(cfg: dict[str, Any]) -> int:
    v = cfg.get("max_midrun_jsonl_appends_per_eat_queue_run")
    if isinstance(v, int) and v >= 0:
        return v
    return 5
