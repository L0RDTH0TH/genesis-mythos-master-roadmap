"""Tests for A.5b.0z dedupe helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from eat_queue_core.a5b_dedupe import (
    AUDIT_SUPPRESSED_JACCARD_ORIGIN,
    decide_append,
    dedupe_entries,
    jaccard_fuzzy_match,
    normalize_guidance,
    repair_enqueue_eligible,
)
from eat_queue_core.models import QueueEntry


def _entry(
    eid: str,
    mode: str,
    *,
    origin: str | None = "origin-1",
    guidance: str = "repair the handoff",
    action: str | None = None,
) -> QueueEntry:
    params: dict = {}
    if origin:
        params["origin_request_id"] = origin
    if guidance:
        params["user_guidance"] = guidance
    if action:
        params["action"] = action
    return QueueEntry(id=eid, mode=mode, params=params or None)


def test_not_eligible_without_origin():
    e = QueueEntry(id="a", mode="HANDOFF_AUDIT_REPAIR", params={"user_guidance": "x"})
    assert repair_enqueue_eligible(e) is False
    assert decide_append(e, [], []).dedupe_attempted is False


def test_handoff_repair_eligible():
    e = _entry("1", "HANDOFF_AUDIT_REPAIR", origin="o1")
    assert repair_enqueue_eligible(e) is True


def test_resume_handoff_audit_eligible():
    e = _entry("1", "RESUME_ROADMAP", origin="o1", action="handoff-audit")
    assert repair_enqueue_eligible(e) is True


def test_suppress_same_origin_identical_guidance():
    existing = [_entry("e1", "HANDOFF_AUDIT_REPAIR", origin="o1", guidance="fix rollup")]
    cand = _entry("c1", "HANDOFF_AUDIT_REPAIR", origin="o1", guidance="fix rollup")
    d = decide_append(cand, existing, [])
    assert d.dedupe_attempted is True
    assert d.dedupe_suppressed is True
    assert d.suppressed_by == "origin_id"
    assert d.suppressing_entry_id == "e1"


def test_suppress_fuzzy_guidance():
    existing = [_entry("e1", "HANDOFF_AUDIT_REPAIR", origin="o1", guidance="fix the rollup gate block")]
    cand = _entry(
        "c1",
        "HANDOFF_AUDIT_REPAIR",
        origin="o1",
        guidance="fix rollup gate block",
    )
    d = decide_append(cand, existing, [])
    assert d.dedupe_suppressed is True
    assert d.suppressed_by in ("fuzzy_guidance", "origin_id", "both")


def test_allow_different_origin():
    existing = [_entry("e1", "HANDOFF_AUDIT_REPAIR", origin="o1", guidance="a")]
    cand = _entry("c1", "HANDOFF_AUDIT_REPAIR", origin="o2", guidance="a")
    d = decide_append(cand, existing, [])
    assert d.dedupe_suppressed is False


def test_pending_same_run_blocks_duplicate():
    first = _entry("c1", "HANDOFF_AUDIT_REPAIR", origin="o1", guidance="same text")
    existing: list = []
    pending: list = []
    d1 = decide_append(first, existing, pending)
    assert d1.dedupe_suppressed is False
    pending.append(first)
    second = _entry("c2", "HANDOFF_AUDIT_REPAIR", origin="o1", guidance="same text")
    d2 = decide_append(second, existing, pending)
    assert d2.dedupe_suppressed is True


def test_normalize_strips_noise():
    a = normalize_guidance("Phase 2.3 fix 2026-04-15T12:00:00Z")
    b = normalize_guidance("phase 2.3 fix")
    assert a == b


def test_jaccard_fuzzy_match_public_api():
    # Mirrors test_suppress_fuzzy_guidance: normalized overlap crosses Jaccard / ratio threshold.
    assert jaccard_fuzzy_match(
        "fix the rollup gate block",
        "fix rollup gate block",
        threshold=0.85,
    )
    assert not jaccard_fuzzy_match(
        "completely different topic here xyz",
        "unrelated guidance text abcdef",
        threshold=0.85,
    )


def test_dedupe_entries_shape():
    a = _entry("k1", "HANDOFF_AUDIT_REPAIR", origin="o9", guidance="same handoff text")
    b = _entry("k2", "HANDOFF_AUDIT_REPAIR", origin="o9", guidance="same handoff text")
    kept, supp = dedupe_entries([a, b], origin_window_hours=24.0)
    assert [e.id for e in kept] == ["k1"]
    assert len(supp) == 1
    assert supp[0]["queue_entry_id"] == "k2"
    assert supp[0]["audit_suppressed_by"] == AUDIT_SUPPRESSED_JACCARD_ORIGIN


def test_origin_window_allows_after_25h():
    """Same origin + same intent but timestamps >24h apart: do not suppress."""
    t0 = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(hours=25)

    def _e(eid: str, ts: datetime) -> QueueEntry:
        return QueueEntry.model_validate(
            {
                "id": eid,
                "mode": "HANDOFF_AUDIT_REPAIR",
                "timestamp": ts.isoformat().replace("+00:00", "Z"),
                "params": {
                    "origin_request_id": "same-o",
                    "user_guidance": "fix rollup",
                },
            }
        )

    existing = [_e("old", t0)]
    cand = _e("new", t1)
    d = decide_append(cand, existing, [], origin_window_hours=24.0)
    assert not d.dedupe_suppressed


def test_missing_timestamp_treated_in_window_suppresses():
    """Legacy lines without ts still participate in fuzzy dedupe (conservative in-window)."""
    e1 = QueueEntry.model_validate(
        {
            "id": "l1",
            "mode": "HANDOFF_AUDIT_REPAIR",
            "params": {"origin_request_id": "leg", "user_guidance": "fix gate"},
        }
    )
    e2 = QueueEntry.model_validate(
        {
            "id": "l2",
            "mode": "HANDOFF_AUDIT_REPAIR",
            "params": {"origin_request_id": "leg", "user_guidance": "fix  gate"},
        }
    )
    d = decide_append(e2, [e1], [], origin_window_hours=24.0)
    assert d.dedupe_suppressed
