"""Central pool (.technical/prompt-queue.jsonl) → per-track PQ hydration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .lanes import filter_entries_by_lane
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
    skipped_malformed_lines: int = 0
    dry_run: bool = False
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
    line_meta: list[tuple[str, str | None]] = []

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
        if obj.get("queue_failed") is True:
            continue
        tags = obj.get("tags")
        if isinstance(tags, list) and "queue-failed" in tags:
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


def hydrate_track_pq_from_pool(
    *,
    vault_root: Path,
    lane_filter: str,
    target_pq: Path,
    pool_path: Path | None = None,
    dry_run: bool = False,
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

    lines, ids, bad = _raw_lines_for_lane(pool, lane_filter)
    msgs: list[str] = []
    if bad:
        msgs.append(f"skipped_malformed_or_non_entry_lines: {bad}")

    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        body = "\n".join(lines) + ("\n" if lines else "")
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
        skipped_malformed_lines=bad,
        dry_run=dry_run,
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
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    root = (args.vault_root or Path.cwd()).resolve()
    res = hydrate_track_pq_from_pool(
        vault_root=root,
        lane_filter=args.lane.strip().lower(),
        target_pq=args.target_pq,
        pool_path=args.pool,
        dry_run=args.dry_run,
    )
    print(res.model_dump_json(indent=2))
    return 0 if res.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
