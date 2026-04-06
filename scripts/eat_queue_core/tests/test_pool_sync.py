"""Tests for central pool → track PQ hydration and dual cleanup."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[2]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.full_cycle import apply_queue_cleanup_dual_track  # noqa: E402
from eat_queue_core.pool_sync import hydrate_track_pq_from_pool  # noqa: E402


def _line(obj: dict) -> str:
    return json.dumps(obj, separators=(",", ":"))


@pytest.fixture
def mini_vault(tmp_path: Path) -> Path:
    (tmp_path / ".technical").mkdir(parents=True)
    (tmp_path / ".technical" / "parallel" / "sandbox").mkdir(parents=True)
    return tmp_path


def test_hydrate_filters_lane_and_shared(mini_vault: Path) -> None:
    pool = mini_vault / ".technical" / "prompt-queue.jsonl"
    pool.write_text(
        "\n".join(
            [
                _line(
                    {
                        "id": "a",
                        "mode": "RESUME_ROADMAP",
                        "queue_lane": "sandbox",
                        "project_id": "sandbox-genesis-mythos-master",
                    }
                ),
                _line(
                    {
                        "id": "b",
                        "mode": "RESUME_ROADMAP",
                        "queue_lane": "godot",
                        "project_id": "godot-genesis-mythos-master",
                    }
                ),
                _line(
                    {
                        "id": "c",
                        "mode": "RESUME_ROADMAP",
                        "queue_lane": "shared",
                        "project_id": "x",
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    target = Path(".technical/parallel/sandbox/prompt-queue.jsonl")
    res = hydrate_track_pq_from_pool(
        vault_root=mini_vault,
        lane_filter="sandbox",
        target_pq=target,
    )
    assert res.ok
    assert res.copied_count == 2
    assert set(res.copied_ids) == {"a", "c"}

    out = (mini_vault / target).read_text(encoding="utf-8").strip().splitlines()
    assert len(out) == 2


def test_apply_queue_cleanup_dual_track(mini_vault: Path) -> None:
    track = mini_vault / ".technical" / "parallel" / "sandbox" / "prompt-queue.jsonl"
    pool = mini_vault / ".technical" / "prompt-queue.jsonl"
    track.parent.mkdir(parents=True, exist_ok=True)
    track.write_text(_line({"id": "x", "mode": "RESUME_ROADMAP"}) + "\n", encoding="utf-8")
    pool.write_text(_line({"id": "x", "mode": "RESUME_ROADMAP"}) + "\n", encoding="utf-8")
    tc, pc = apply_queue_cleanup_dual_track(track, pool, {"x"})
    assert tc is True and pc is True
    assert track.read_text(encoding="utf-8").strip() == ""
    assert pool.read_text(encoding="utf-8").strip() == ""
