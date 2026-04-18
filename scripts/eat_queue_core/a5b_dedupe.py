"""
A.5b.0z enqueue-time HANDOFF dedupe (read-before-append).

Normative behavior matches .cursor/rules/agents/queue.mdc A.5b.0z:
same origin_request_id + same-intent guidance via normalized text and fuzzy gates.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Any, Literal

from .models import QueueEntry

SuppressedBy = Literal["origin_id", "fuzzy_guidance", "both", "none"]

# Stable strings for audit / Watcher (queue-churn-guard alignment)
AUDIT_SUPPRESSED_JACCARD_ORIGIN = "a5b_dedupe_jaccard_origin"
AUDIT_SUPPRESSED_ORIGIN_WINDOW = "a5b_dedupe_origin_window"


@dataclass(frozen=True)
class DedupeDecision:
    dedupe_attempted: bool
    dedupe_suppressed: bool
    suppressed_by: SuppressedBy
    suppressing_entry_id: str | None
    normalized_guidance_prefix: str
    """Machine-stable label for audit rows when suppressed."""
    audit_suppressed_by: str | None = None


def _primary_mode(mode: str | None) -> str:
    if not mode:
        return ""
    return mode.split("-")[0].strip().upper()


def repair_enqueue_eligible(entry: QueueEntry) -> bool:
    """True when this line is subject to A.5b.0z dedupe."""
    primary = _primary_mode(entry.mode)
    p = entry.params if isinstance(entry.params, dict) else {}
    oid = p.get("origin_request_id")
    if not isinstance(oid, str) or not oid.strip():
        return False
    if primary == "HANDOFF_AUDIT_REPAIR":
        return True
    if primary == "RESUME_ROADMAP":
        act = str(p.get("action") or "").strip().lower().replace("_", "-")
        return act in ("handoff-audit", "handoff_audit")
    return False


_TS = re.compile(r"\b20\d{2}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?Z?\b", re.I)
_PHASE = re.compile(r"\bphase\s*[\d.]+", re.I)
_REQSUF = re.compile(r"followup[-\w]*-\d{4,}", re.I)
_ID_COMPACT_TS = re.compile(r"(\d{8}T\d{6}Z)")


def normalize_guidance(raw: str | None) -> str:
    """Lowercase, collapse whitespace, strip volatile substrings; compare first 200 chars in-contract."""
    if not raw:
        return ""
    s = raw.strip().lower()
    s = _TS.sub(" ", s)
    s = _PHASE.sub(" ", s)
    s = _REQSUF.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:200]


def _guidance_from_entry(entry: QueueEntry) -> str:
    data = entry.model_dump()
    p = entry.params if isinstance(entry.params, dict) else {}
    for k in ("user_guidance", "prompt"):
        v = p.get(k) if isinstance(p, dict) else None
        if isinstance(v, str) and v.strip():
            return v
    for k in ("user_guidance", "prompt"):
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


def _jaccard_tokens(a: str, b: str) -> float:
    sa = set(a.split())
    sb = set(b.split())
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def _lev_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def jaccard_fuzzy_match(a: str, b: str, threshold: float = 0.85) -> bool:
    """
    Public API: same-intent check on normalized first-200 slices.
    True if identical, or Jaccard token similarity >= threshold, or ratio >= threshold.
    """
    na = normalize_guidance(a)
    nb = normalize_guidance(b)
    same, _ = _same_intent_guidance(na, nb, threshold=threshold)
    return same


def _same_intent_guidance(
    norm_a: str,
    norm_b: str,
    *,
    threshold: float = 0.85,
) -> tuple[bool, bool]:
    """
    Return (is_same_intent, identical_200_prefix).
    Fuzzy: Jaccard >= threshold or SequenceMatcher ratio >= threshold on first-200 slice.
    """
    ca = norm_a[:200]
    cb = norm_b[:200]
    if ca == cb:
        return True, True
    if not ca and not cb:
        return True, True
    if _jaccard_tokens(ca, cb) >= threshold:
        return True, False
    if _lev_ratio(ca, cb) >= threshold:
        return True, False
    return False, False


def _parse_iso_timestamp(raw: str) -> datetime | None:
    s = raw.strip()
    if not s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass
    m = _ID_COMPACT_TS.search(raw)
    if m:
        frag = m.group(1).replace("Z", "")
        try:
            dt = datetime.strptime(frag, "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            return None
    return None


def parse_entry_datetime(entry: QueueEntry) -> datetime | None:
    """
    Best-effort entry time for origin window. Returns None if unparseable — callers
    treat None as in-window (conservative; avoids false-negative suppression on legacy lines).
    """
    d: dict[str, Any] = entry.model_dump()
    for key in ("timestamp", "created", "iso_timestamp"):
        v = d.get(key)
        if isinstance(v, str) and v.strip():
            dt = _parse_iso_timestamp(v)
            if dt:
                return dt
    p = d.get("params")
    if isinstance(p, dict):
        v = p.get("timestamp")
        if isinstance(v, str) and v.strip():
            dt = _parse_iso_timestamp(v)
            if dt:
                return dt
    m = _ID_COMPACT_TS.search(entry.id)
    if m:
        dt = _parse_iso_timestamp(m.group(0))
        if dt:
            return dt
    return None


def pair_in_origin_window(
    a: datetime | None,
    b: datetime | None,
    *,
    origin_window_hours: float,
) -> bool:
    """If either time is missing, treat as in-window (conservative)."""
    if a is None or b is None:
        return True
    delta = abs((a - b).total_seconds())
    return delta <= origin_window_hours * 3600.0


def decide_append(
    candidate: QueueEntry,
    existing_disk: list[QueueEntry],
    pending_same_run: list[QueueEntry],
    *,
    origin_window_hours: float = 24.0,
    reference_now: datetime | None = None,
) -> DedupeDecision:
    """
    Decide whether to suppress append. ``pending_same_run`` = lines already appended in this
    harness invocation (after disk snapshot).

    ``reference_now`` defaults to UTC now; used with candidate/other timestamps for window checks.
    """
    if not repair_enqueue_eligible(candidate):
        return DedupeDecision(False, False, "none", None, "", None)

    cand_norm = normalize_guidance(_guidance_from_entry(candidate))
    prefix = cand_norm[:50] if cand_norm else ""

    p = candidate.params if isinstance(candidate.params, dict) else {}
    oid = p.get("origin_request_id")
    assert isinstance(oid, str) and oid.strip()
    oid_key = oid.strip()

    dedupe_attempted = True
    full_view = list(existing_disk) + list(pending_same_run)
    cand_ts = parse_entry_datetime(candidate)

    for other in full_view:
        if other.id == candidate.id:
            continue
        op = other.params if isinstance(other.params, dict) else {}
        o_oid = op.get("origin_request_id")
        if not isinstance(o_oid, str) or o_oid.strip() != oid_key:
            continue
        other_ts = parse_entry_datetime(other)
        if not pair_in_origin_window(cand_ts, other_ts, origin_window_hours=origin_window_hours):
            continue
        o_norm = normalize_guidance(_guidance_from_entry(other))
        same, identical_200 = _same_intent_guidance(cand_norm, o_norm)
        if not same:
            continue
        if identical_200:
            sb: SuppressedBy = "origin_id"
        else:
            sb = "fuzzy_guidance"
        return DedupeDecision(
            dedupe_attempted,
            True,
            sb,
            other.id,
            prefix,
            AUDIT_SUPPRESSED_JACCARD_ORIGIN,
        )

    return DedupeDecision(dedupe_attempted, False, "none", None, prefix, None)


def dedupe_entries(
    entries: list[QueueEntry],
    *,
    origin_window_hours: float = 24.0,
    reference_now: datetime | None = None,
) -> tuple[list[QueueEntry], list[dict[str, Any]]]:
    """
    Ordered batch dedupe: for repair-eligible lines with same origin_request_id, keep first
    in-window duplicate chain; drop later equivalent-intent lines.

    Returns (kept_entries, suppressed_telemetry_rows).
    """
    now = reference_now or datetime.now(timezone.utc)
    kept: list[QueueEntry] = []
    suppressed: list[dict[str, Any]] = []

    for cand in entries:
        if not repair_enqueue_eligible(cand):
            kept.append(cand)
            continue
        d = decide_append(cand, kept, [], origin_window_hours=origin_window_hours, reference_now=now)
        if d.dedupe_suppressed:
            suppressed.append(
                {
                    "queue_entry_id": cand.id,
                    "suppressing_queue_entry_id": d.suppressing_entry_id,
                    "dedupe_attempted": True,
                    "dedupe_suppressed": True,
                    "suppressed_by": d.suppressed_by,
                    "audit_suppressed_by": d.audit_suppressed_by or AUDIT_SUPPRESSED_JACCARD_ORIGIN,
                }
            )
            continue
        kept.append(cand)

    return kept, suppressed


def parse_queue_entry_line(line: str) -> QueueEntry:
    raw = json.loads(line)
    if not isinstance(raw, dict):
        raise ValueError("expected JSON object")
    return QueueEntry.model_validate(raw)
