"""
Golden: full_cycle deepen → simulated A.5b repair → pass 2 plan + queue cleanup → empty queue.
PYTHONPATH=scripts python -m pytest scripts/eat_queue_core/tests/test_full_cycle_golden.py -q
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[2]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.full_cycle import queue_rewrite_ids, run_full_eat_queue_cycle  # noqa: E402
from eat_queue_core.plan import build_plan, load_queue_file  # noqa: E402


DEEPEN_ID = "golden-deepen-fullcycle-1"
REPAIR_ID = "golden-repair-fullcycle-1"
PROJECT = "genesis-mythos-master"


def _deepen_line() -> dict:
    return {
        "id": DEEPEN_ID,
        "mode": "RESUME_ROADMAP",
        "project_id": PROJECT,
        "params": {"action": "deepen", "project_id": PROJECT},
    }


def _repair_line() -> dict:
    return {
        "id": REPAIR_ID,
        "mode": "RESUME_ROADMAP",
        "project_id": PROJECT,
        "params": {"action": "deepen", "project_id": PROJECT},
        "queue_priority": "repair",
    }


class FullCycleGoldenTest(unittest.TestCase):
    def test_lane_filter_includes_only_matching_track(self) -> None:
        sandbox = {
            "id": "lane-sandbox-1",
            "mode": "RESUME_ROADMAP",
            "project_id": PROJECT,
            "queue_lane": "sandbox",
            "params": {"action": "deepen", "project_id": PROJECT},
        }
        godot = {
            "id": "lane-godot-1",
            "mode": "RESUME_ROADMAP",
            "project_id": PROJECT,
            "queue_lane": "godot",
            "params": {"action": "deepen", "project_id": PROJECT},
        }
        text = json.dumps(sandbox) + "\n" + json.dumps(godot) + "\n"
        entries = load_queue_file_from_text(text)
        plan_s, _ = build_plan(entries, "lane-test", lane_filter="sandbox")
        ids_s = {i.queue_entry_id for i in plan_s.intents}
        self.assertIn("lane-sandbox-1", ids_s)
        self.assertNotIn("lane-godot-1", ids_s)

        plan_g, _ = build_plan(entries, "lane-test", lane_filter="godot")
        ids_g = {i.queue_entry_id for i in plan_g.intents}
        self.assertIn("lane-godot-1", ids_g)
        self.assertNotIn("lane-sandbox-1", ids_g)

    def test_queue_rewrite_ids_includes_pass3(self) -> None:
        text = json.dumps(_deepen_line()) + "\n" + json.dumps(_repair_line()) + "\n"
        entries = load_queue_file_from_text(text)
        plan, _ = build_plan(entries, "golden-rewrite")
        rw = queue_rewrite_ids(plan)
        self.assertIn(DEEPEN_ID, rw)
        self.assertIn(REPAIR_ID, rw)

    def test_full_cycle_pass3_drains_queue_empty(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tech = root / ".technical"
            tech.mkdir(parents=True)
            qpath = tech / "prompt-queue.jsonl"
            qpath.write_text(json.dumps(_deepen_line()) + "\n", encoding="utf-8")

            def append_repair() -> None:
                lines = [json.dumps(_deepen_line()), json.dumps(_repair_line())]
                qpath.write_text("\n".join(lines) + "\n", encoding="utf-8")

            res = run_full_eat_queue_cycle(
                initial_action="deepen",
                initial_profile="balance",
                max_passes=2,
                strict_mode=True,
                vault_root=root,
                queue_path=qpath,
                plan_path=tech / "eat_queue_run_plan.json",
                decisions_path=tech / "eat-queue-decisions.jsonl",
                parent_run_id="golden-fullcycle",
                simulate_post_pass1_repair=append_repair,
                apply_cleanup=True,
            )
            self.assertEqual(res.passes_run, 2)
            self.assertTrue(res.queue_empty_after_cleanup)
            self.assertEqual(res.final_repair_lines_remaining, 0)
            final = load_queue_file(qpath) if qpath.is_file() else []
            self.assertEqual(len(final), 0)


def load_queue_file_from_text(text: str):
    """Parse JSONL without strict file semantics (test helper)."""
    from eat_queue_core.models import QueueEntry

    out: list = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(QueueEntry.model_validate(json.loads(line)))
    return out


if __name__ == "__main__":
    unittest.main()
