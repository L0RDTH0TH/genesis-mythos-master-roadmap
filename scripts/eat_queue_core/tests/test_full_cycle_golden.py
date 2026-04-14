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

from eat_queue_core.full_cycle import (  # noqa: E402
    emit_intent_tracking_for_plan_pass,
    enrich_plan_dict,
    queue_rewrite_ids,
    read_queue_rationale_enforcement_enabled,
    read_tracking_intent_receipts_enabled,
    run_full_eat_queue_cycle,
    validate_option_evaluation_for_entry,
)
from eat_queue_core.models import DispatchIntent, EatQueueRunPlan, QueueEntry  # noqa: E402
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

    def test_full_cycle_bootstraps_empty_lane_with_project(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tech = root / ".technical"
            tech.mkdir(parents=True)
            qpath = tech / "prompt-queue.jsonl"
            qpath.write_text("", encoding="utf-8")
            # Create execution workflow cursor so bootstrap chooses execution track.
            wf = (
                root
                / "1-Projects"
                / PROJECT
                / "Roadmap"
                / "Execution"
                / "workflow_state-execution.md"
            )
            wf.parent.mkdir(parents=True, exist_ok=True)
            wf.write_text("---\ncurrent_subphase_index: 2.2.3\n---\n", encoding="utf-8")

            res = run_full_eat_queue_cycle(
                initial_action="deepen",
                initial_profile="balance",
                max_passes=1,
                strict_mode=True,
                vault_root=root,
                queue_path=qpath,
                plan_path=tech / "eat_queue_run_plan.json",
                decisions_path=tech / "eat-queue-decisions.jsonl",
                parent_run_id="golden-bootstrap-empty",
                apply_cleanup=False,
                lane_filter="godot",
                lane_project_id=PROJECT,
            )
            self.assertEqual(res.passes_run, 1)
            queue_text = qpath.read_text(encoding="utf-8")
            self.assertIn("empty-bootstrap-", queue_text)
            self.assertIn('"mode": "RESUME_ROADMAP"', queue_text)
            self.assertIn('"queue_lane": "godot"', queue_text)
            plan_text = (tech / "eat_queue_run_plan.json").read_text(encoding="utf-8")
            self.assertIn('"queue_entry_id"', plan_text)

    def test_option_evaluation_missing_under_enforcement(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg_dir = root / "3-Resources" / "Second-Brain"
            cfg_dir.mkdir(parents=True)
            (cfg_dir / "Second-Brain-Config.md").write_text(
                "queue:\n  rationale_enforcement_enabled: true\n",
                encoding="utf-8",
            )
            entry = QueueEntry(
                id="oe-1",
                mode="RESUME_ROADMAP",
                project_id=PROJECT,
                params={"action": "deepen", "roadmap_track": "execution", "project_id": PROJECT},
            )
            res = validate_option_evaluation_for_entry(
                entry, vault_root=root, rationale_enforcement=True
            )
            self.assertFalse(res.ok)
            self.assertIn("option_evaluation_missing", res.divergence_codes)

    def test_emit_intent_tracking_writes_receipt_jsonl(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tech = root / ".technical"
            tech.mkdir(parents=True)
            qpath = tech / "prompt-queue.jsonl"
            entry = QueueEntry(
                id="track-1",
                mode="RESUME_ROADMAP",
                project_id=PROJECT,
                queue_lane="sandbox",
                params={"action": "deepen", "roadmap_track": "execution", "project_id": PROJECT},
            )
            plan = EatQueueRunPlan(
                parent_run_id="pr-test",
                intents=[
                    DispatchIntent(
                        queue_entry_id="track-1",
                        project_id=PROJECT,
                        queue_pass_phase="initial",
                        pass_id="pass1",
                        dispatch_ordinal=1,
                    )
                ],
                consumed_ids=["track-1"],
            )
            enriched = enrich_plan_dict(
                plan,
                [entry],
                initial_action="deepen",
                initial_profile="balance",
                strict_mode=True,
                full_cycle_pass_index=1,
                full_cycle_passes_total=1,
            )
            msgs = emit_intent_tracking_for_plan_pass(
                vault_root=root,
                queue_path=qpath,
                enriched=enriched,
                entries_lane=[entry],
                lane_filter="sandbox",
            )
            comms = tech / "task-handoff-comms.jsonl"
            self.assertTrue(comms.is_file())
            text = comms.read_text(encoding="utf-8")
            self.assertIn("intent_snapshot", text)
            self.assertIn("intent_actual_receipt", text)
            self.assertIn("parallel_track", text)
            self.assertIn("sandbox", text)
            self.assertTrue(any("intent_snapshot" in m for m in msgs))

    def test_resume_deepen_phase1_receipt_provisional_when_no_goal_file(self) -> None:
        """RESUME_ROADMAP deepen + execution track + rationale on: valid OE shape but quote check may flag without goal file."""
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg_dir = root / "3-Resources" / "Second-Brain"
            cfg_dir.mkdir(parents=True)
            (cfg_dir / "Second-Brain-Config.md").write_text(
                "queue:\n  rationale_enforcement_enabled: true\n",
                encoding="utf-8",
            )
            tech = root / ".technical"
            tech.mkdir(parents=True)
            qpath = tech / "prompt-queue.jsonl"
            oe = {
                "master_goal_ref": "missing-goal.md",
                "alternatives": [
                    {"id": "a", "summary": "x", "alignment_score": 1.0},
                ],
                "chosen": "a",
                "rationale": "short",
            }
            line = {
                "id": "phase1-deepen",
                "mode": "RESUME_ROADMAP",
                "project_id": PROJECT,
                "params": {
                    "action": "deepen",
                    "roadmap_track": "execution",
                    "project_id": PROJECT,
                    "option_evaluation": oe,
                },
            }
            qpath.write_text(json.dumps(line) + "\n", encoding="utf-8")
            res = run_full_eat_queue_cycle(
                initial_action="deepen",
                initial_profile="balance",
                max_passes=1,
                strict_mode=True,
                vault_root=root,
                queue_path=qpath,
                plan_path=tech / "eat_queue_run_plan.json",
                decisions_path=tech / "eat-queue-decisions.jsonl",
                parent_run_id="golden-phase1",
                apply_cleanup=False,
            )
            self.assertEqual(res.passes_run, 1)
            comms = tech / "task-handoff-comms.jsonl"
            self.assertTrue(comms.is_file())
            lines = [json.loads(x) for x in comms.read_text(encoding="utf-8").splitlines() if x.strip()]
            receipts = [x for x in lines if x.get("record_type") == "intent_actual_receipt"]
            self.assertEqual(len(receipts), 1)
            self.assertEqual(receipts[0].get("queue_entry_id"), "phase1-deepen")
            self.assertIn(receipts[0].get("status_class"), ("success", "provisional_success"))


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
