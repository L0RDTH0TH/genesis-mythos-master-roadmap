"""Lane-effective queue scalars from Second-Brain-Config (parallel_execution.tracks[].queue_overrides)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config_loader import max_inline_a5b_repair_generations, parse_queue_config, resolve_config_path
from .gitforge_config import merge_yaml_blocks_from_config


def _queue_overrides_for_lane(merged: dict[str, Any], lane: str | None) -> dict[str, Any]:
    if not lane or not str(lane).strip():
        return {}
    lane_l = str(lane).strip().lower()
    pe = merged.get("parallel_execution")
    if not isinstance(pe, dict):
        return {}
    tracks = pe.get("tracks")
    if not isinstance(tracks, list):
        return {}
    for t in tracks:
        if not isinstance(t, dict):
            continue
        if str(t.get("lane") or "").strip().lower() == lane_l:
            qo = t.get("queue_overrides")
            return qo if isinstance(qo, dict) else {}
    return {}


def effective_max_inline_a5b(vault_root: Path, lane: str | None) -> int:
    """
    Merge global ``queue:`` max_inline with ``parallel_execution.tracks[].queue_overrides``
    for the given lane (e.g. godot).
    """
    cfg_path = resolve_config_path(vault_root, None)
    flat = parse_queue_config(cfg_path)
    base = max_inline_a5b_repair_generations(flat)
    merged = merge_yaml_blocks_from_config(cfg_path)
    overrides = _queue_overrides_for_lane(merged, lane)
    v = overrides.get("max_inline_a5b_repair_generations_per_run")
    if isinstance(v, int) and v >= 0:
        return v
    return base


def watcher_canonical_path(vault_root: Path) -> Path:
    """Resolve ``parallel_execution.watcher.canonical_path`` or default Watcher-Result path."""
    root = vault_root.resolve()
    default = root / "3-Resources" / "Watcher-Result.md"
    cfg_path = resolve_config_path(root, None)
    merged = merge_yaml_blocks_from_config(cfg_path)
    pe = merged.get("parallel_execution")
    if not isinstance(pe, dict):
        return default
    w = pe.get("watcher")
    if not isinstance(w, dict):
        return default
    p = w.get("canonical_path")
    if isinstance(p, str) and p.strip():
        return (root / p.strip()).resolve()
    return default
