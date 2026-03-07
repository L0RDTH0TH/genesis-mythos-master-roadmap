"""
Queue processor contract: parse, validate, dedup, sort.
Canonical order: INGEST MODE (1) -> ... -> ASYNC-LOOP (12).
"""

import json

KNOWN_MODES = [
    "INGEST MODE",
    "ORGANIZE MODE",
    "TASK-ROADMAP",
    "DISTILL MODE",
    "EXPRESS MODE",
    "ARCHIVE MODE",
    "TASK-COMPLETE",
    "ADD-ROADMAP-ITEM",
    "SEEDED-ENHANCE",
    "BATCH-DISTILL",
    "BATCH-EXPRESS",
    "ASYNC-LOOP",
]

CANONICAL_ORDER = {m: i for i, m in enumerate(KNOWN_MODES, start=1)}


def parse_queue_line(line: str) -> tuple[dict | None, bool]:
    """
    Parse a single JSONL line. Return (parsed_obj, is_valid).
    Invalid JSON or missing 'mode' (string) -> (None, False).
    """
    line = line.strip()
    if not line:
        return None, False
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        return None, False
    if not isinstance(obj, dict):
        return None, False
    mode = obj.get("mode")
    if not isinstance(mode, str) or not mode.strip():
        return None, False
    return obj, True


def validate_entry(entry: dict) -> bool:
    """Entry must have 'mode' (string). Filter out queue_failed true or tags containing queue-failed."""
    if not isinstance(entry, dict):
        return False
    if not isinstance(entry.get("mode"), str):
        return False
    if entry.get("queue_failed") is True:
        return False
    tags = entry.get("tags")
    if isinstance(tags, list) and "queue-failed" in tags:
        return False
    if isinstance(tags, str) and "queue-failed" in tags:
        return False
    return True


def dedup_entries(entries: list[dict]) -> list[dict]:
    """Same (mode, prompt, source_file) -> keep first by timestamp."""
    seen = set()
    result = []
    for e in entries:
        key = (e.get("mode"), e.get("prompt"), e.get("source_file"))
        if key in seen:
            continue
        seen.add(key)
        result.append(e)
    return result


def canonical_sort_key(entry: dict) -> tuple[int, str]:
    """Sort key: (order_index, timestamp or ''). Unknown mode sorts last."""
    mode = entry.get("mode") or ""
    order = CANONICAL_ORDER.get(mode, 999)
    ts = entry.get("timestamp") or entry.get("id") or ""
    return (order, str(ts))
