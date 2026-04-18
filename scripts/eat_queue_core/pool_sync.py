"""Central pool (.technical/prompt-queue.jsonl) → per-track PQ hydration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .a5b_dedupe import dedupe_entries, repair_enqueue_eligible
from .config_loader import origin_dedupe_window_hours, parse_queue_config, resolve_config_path
from .lanes import entry_in_lane_dispatch_subset, filter_entries_by_lane
from .models import QueueEntry


DEFAULT_POOL_REL = Path(".technical/prompt-queue.jsonl")
CONFIG_REL = Path("3-Resources/Second-Brain/Second-Brain-Config.md")


class PoolSyncResult(BaseModel):
    """JSON-serializable summary for Layer 1 / PQAUD."""

    ok: bool = True
    lane_filter: str
    pool_path: str
    target_pq: str
    copied_count: int = 0
    copied_ids: list[str] = Field(default_factory=list)
    preserved_lane_only_count: int = 0
    preserved_lane_only_ids: list[str] = Field(default_factory=list)
    skipped_cross_lane_lines: int = 0
    written_line_count: int = 0
    strict_central_only: bool = False
    skipped_malformed_lines: int = 0
    dry_run: bool = False
    dedupe_suppressed_count: int = 0
    messages: list[str] = Field(default_factory=list)


def read_central_pool_fanout_enabled(vault_root: Path) -> bool:
    """Best-effort: read `central_pool_fanout_enabled: true` from Second-Brain-Config.md."""
    cfg = (vault_root / CONFIG_REL).resolve()
    if not cfg.is_file():
        return False
    try:
        text = cfg.read_text(encoding="utf-8")
    except OSError:
        return False
    m = re.search(
        r"(?m)^\s*central_pool_fanout_enabled:\s*(true|false)\s*$",
        text,
    )
    if not m:
        return False
    return m.group(1).lower() == "true"


def read_pool_sync_strict_central_only(vault_root: Path) -> bool:
    """When true, A.0.4 overwrites track PQ with central subset only (legacy; drops lane-only)."""
    cfg = (vault_root / CONFIG_REL).resolve()
    if not cfg.is_file():
        return False
    try:
        text = cfg.read_text(encoding="utf-8")
    except OSError:
        return False
    m = re.search(r"(?m)^\s*pool_sync_strict_central_only:\s*(true|false)\s*$", text)
    if not m:
        return False
    return m.group(1).lower() == "true"


def read_tracking_intent_receipts_enabled(vault_root: Path) -> bool:
    """Default true when key absent (Queue-Sources / Second-Brain-Config)."""
    cfg = (vault_root / CONFIG_REL).resolve()
    if not cfg.is_file():
        return True
    try:
        text = cfg.read_text(encoding="utf-8")
    except OSError:
        return True
    m = re.search(r"(?m)^\s*intent_receipts_enabled:\s*(true|false)\s*$", text)
    if not m:
        return True
    return m.group(1).lower() == "true"


def read_queue_rationale_enforcement_enabled(vault_root: Path) -> bool:
    cfg = (vault_root / CONFIG_REL).resolve()
    if not cfg.is_file():
        return False
    try:
        text = cfg.read_text(encoding="utf-8")
    except OSError:
        return False
    m = re.search(r"(?m)^\s*rationale_enforcement_enabled:\s*(true|false)\s*$", text)
    if not m:
        return False
    return m.group(1).lower() == "true"


def _entry_skipped_as_failed(obj: dict[str, Any]) -> bool:
    if obj.get("queue_failed") is True:
        return True
    tags = obj.get("tags")
    return isinstance(tags, list) and "queue-failed" in tags


def _raw_lines_for_lane(
    pool_path: Path,
    lane_filter: str,
) -> tuple[list[str], list[str], int]:
    if not pool_path.is_file():
        return [], [], 0
    text = pool_path.read_text(encoding="utf-8")
    matched_raw: list[str] = []
    copied_ids: list[str] = []
    malformed = 0
    entries_for_filter: list[QueueEntry] = []
    line_meta: list[tuple[str, str]] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            obj: Any = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if not isinstance(obj, dict):
            malformed += 1
            continue
        if _entry_skipped_as_failed(obj):
            continue
        if "id" not in obj or "mode" not in obj:
            malformed += 1
            continue
        try:
            qe = QueueEntry.model_validate(obj)
        except Exception:
            malformed += 1
            continue
        line_meta.append((line, qe.id))
        entries_for_filter.append(qe)

    filtered = filter_entries_by_lane(entries_for_filter, lane_filter)
    allowed_ids = {e.id for e in filtered}

    for raw_stripped, eid in line_meta:
        if eid in allowed_ids:
            matched_raw.append(raw_stripped)
            copied_ids.append(eid)

    return matched_raw, copied_ids, malformed


def _parse_track_entries_for_merge(
    text: str,
) -> tuple[list[tuple[str, QueueEntry]], int]:
    """Return (raw_line, entry) pairs in file order; malformed line count."""
    out: list[tuple[str, QueueEntry]] = []
    bad = 0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            obj: Any = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue
        if not isinstance(obj, dict):
            bad += 1
            continue
        if _entry_skipped_as_failed(obj):
            continue
        if "id" not in obj or "mode" not in obj:
            bad += 1
            continue
        try:
            qe = QueueEntry.model_validate(obj)
        except Exception:
            bad += 1
            continue
        out.append((line, qe))
    return out, bad


def _merge_preserving_lane_only(
    *,
    lane_filter: str,
    central_lines: list[str],
    central_ids: list[str],
    target_path: Path,
    strict_central_only: bool,
) -> tuple[list[str], list[str], int, int, list[str]]:
    """Build final line list. Returns merged lines, preserved ids, cross_lane_skips, track_malformed, messages."""
    msgs: list[str] = []
    if strict_central_only:
        return central_lines, [], 0, 0, msgs

    central_id_set = set(central_ids)
    if not target_path.is_file():
        return central_lines, [], 0, 0, msgs

    try:
        track_text = target_path.read_text(encoding="utf-8")
    except OSError:
        return central_lines, [], 0, 0, msgs

    pairs, track_bad = _parse_track_entries_for_merge(track_text)
    preserved_ids: list[str] = []
    cross_lane = 0
    seen: set[str] = set()

    preserved_raw: list[str] = []
    for raw, qe in pairs:
        if qe.id in central_id_set:
            continue
        if qe.id in seen:
            continue
        if not entry_in_lane_dispatch_subset(lane_filter, qe):
            cross_lane += 1
            continue
        seen.add(qe.id)
        preserved_raw.append(raw)
        preserved_ids.append(qe.id)

    merged = list(central_lines) + preserved_raw
    if preserved_ids:
        msgs.append(
            f"pool_sync: preserved {len(preserved_ids)} lane-only id(s) not in central pool "
            f"for lane {lane_filter}: {preserved_ids}"
        )
    if cross_lane:
        msgs.append(
            f"pool_sync: skipped {cross_lane} track line(s) (queue_lane mismatch for lane {lane_filter})"
        )
    if track_bad:
        msgs.append(f"skipped_malformed_track_lines: {track_bad}")

    return merged, preserved_ids, cross_lane, track_bad, msgs


def _append_jsonl_audit(audit_path: Path, record: dict[str, Any]) -> None:
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False) + "\n"
    prev = audit_path.read_text(encoding="utf-8") if audit_path.is_file() else ""
    audit_path.write_text(prev + line, encoding="utf-8")


def _dedupe_merged_queue_lines(
    merged_lines: list[str],
    *,
    origin_window_hours: float,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Drop later duplicate-equivalent A.5b repair lines; keep order for non-suppressed."""
    parsed: list[tuple[str, QueueEntry | None]] = []
    for raw in merged_lines:
        line = raw.strip()
        if not line:
            continue
        try:
            qe = QueueEntry.model_validate(json.loads(line))
            parsed.append((line, qe))
        except Exception:
            parsed.append((line, None))

    entries_order = [e for _, e in parsed if e is not None]
    kept, supp = dedupe_entries(entries_order, origin_window_hours=origin_window_hours)
    kept_ids = {e.id for e in kept}
    out_lines: list[str] = []
    for raw, e in parsed:
        if e is None:
            out_lines.append(raw)
            continue
        if not repair_enqueue_eligible(e):
            out_lines.append(raw)
            continue
        if e.id in kept_ids:
            out_lines.append(raw)
    return out_lines, supp


def hydrate_track_pq_from_pool(
    *,
    vault_root: Path,
    lane_filter: str,
    target_pq: Path,
    pool_path: Path | None = None,
    dry_run: bool = False,
    strict_central_only: bool | None = None,
) -> PoolSyncResult:
    root = vault_root.resolve()
    pool = (root / (pool_path or DEFAULT_POOL_REL)).resolve()
    target = (root / target_pq).resolve()
    try:
        target.relative_to(root)
        pool.relative_to(root)
    except ValueError:
        return PoolSyncResult(
            ok=False,
            lane_filter=lane_filter,
            pool_path=str(pool),
            target_pq=str(target),
            messages=["pool_sync: paths must stay under vault_root"],
        )

    if strict_central_only is None:
        strict = read_pool_sync_strict_central_only(root)
    else:
        strict = strict_central_only

    lines, ids, bad = _raw_lines_for_lane(pool, lane_filter)
    msgs: list[str] = []
    if bad:
        msgs.append(f"skipped_malformed_or_non_entry_lines: {bad}")

    merged, preserved_ids, cross_skip, track_bad, merge_msgs = _merge_preserving_lane_only(
        lane_filter=lane_filter,
        central_lines=lines,
        central_ids=ids,
        target_path=target,
        strict_central_only=strict,
    )
    msgs.extend(merge_msgs)

    cfg_path = resolve_config_path(root, None)
    oh = origin_dedupe_window_hours(parse_queue_config(cfg_path))
    merged, dedupe_supp = _dedupe_merged_queue_lines(merged, origin_window_hours=oh)
    if dedupe_supp:
        msgs.append(f"pool_sync_dedupe: suppressed {len(dedupe_supp)} duplicate-equivalent line(s)")
    if not dry_run:
        from datetime import datetime, timezone

        audit_path = target.parent / "prompt-queue-audit.jsonl"
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        for row in dedupe_supp:
            _append_jsonl_audit(
                audit_path,
                {
                    "record_type": "pool_sync_dedupe",
                    "iso_timestamp": now_iso,
                    "lane_filter": lane_filter,
                    **row,
                },
            )

    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        body = "\n".join(merged) + ("\n" if merged else "")
        target.write_text(body, encoding="utf-8")

    try:
        pool_rel = str(pool.relative_to(root))
    except ValueError:
        pool_rel = str(pool)
    try:
        target_rel = str(target.relative_to(root))
    except ValueError:
        target_rel = str(target)

    return PoolSyncResult(
        ok=True,
        lane_filter=lane_filter,
        pool_path=pool_rel,
        target_pq=target_rel,
        copied_count=len(lines),
        copied_ids=ids,
        preserved_lane_only_count=len(preserved_ids),
        preserved_lane_only_ids=preserved_ids,
        skipped_cross_lane_lines=cross_skip,
        written_line_count=len(merged),
        strict_central_only=strict,
        skipped_malformed_lines=bad + track_bad,
        dry_run=dry_run,
        dedupe_suppressed_count=len(dedupe_supp),
        messages=msgs,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Hydrate per-track PQ from central prompt-queue pool")
    p.add_argument("--vault-root", type=Path, default=None, help="Vault root (default: cwd)")
    p.add_argument("--lane", type=str, required=True, help="queue_lane_filter (e.g. sandbox, godot)")
    p.add_argument("--target-pq", type=Path, required=True, help="Track prompt-queue.jsonl path (vault-relative)")
    p.add_argument(
        "--pool",
        type=Path,
        default=None,
        help="Central pool path (default: .technical/prompt-queue.jsonl under vault root)",
    )
    p.add_argument(
        "--strict-central-only",
        action="store_true",
        help="Overwrite track PQ with central subset only (ignore lane-only lines in track file)",
    )
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    root = (args.vault_root or Path.cwd()).resolve()
    res = hydrate_track_pq_from_pool(
        vault_root=root,
        lane_filter=args.lane.strip().lower(),
        target_pq=args.target_pq,
        pool_path=args.pool,
        dry_run=args.dry_run,
        strict_central_only=True if args.strict_central_only else None,
    )

    print(res.model_dump_json(indent=2))
    return 0 if res.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
