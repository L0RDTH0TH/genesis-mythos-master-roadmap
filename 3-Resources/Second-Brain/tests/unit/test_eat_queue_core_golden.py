"""
Golden: Phase 5.1.1 incident — forward deepen + appended A.5b-style repair line.
Run: pip install -r scripts/eat_queue_core/requirements.txt
     PYTHONPATH=scripts python -m pytest ...  OR  PYTHONPATH=scripts python -m unittest ...
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_FIXTURE = (
    Path(__file__).resolve().parent.parent / "fixtures" / "eat_queue" / "phase5_111_incident.jsonl"
)
_FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "eat_queue"
_SCRIPTS = Path(__file__).resolve().parents[4] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from eat_queue_core.plan import build_plan, parse_queue_jsonl  # noqa: E402


TRIGGER_ID = "followup-deepen-phase5-111-gmm-20260403T234800Z"
REPAIR_ID = "repair-l1postlv-phase5-111-gmm-20260403T235500Z"


class EatQueueCoreGoldenTest(unittest.TestCase):
    def test_phase5_111_plan_pass3_repair_consumed(self) -> None:
        text = _FIXTURE.read_text(encoding="utf-8")
        entries = parse_queue_jsonl(text)
        plan, decisions = build_plan(entries, parent_run_id="golden-phase5-111")

        self.assertEqual(plan.schema_version, 2)
        pass3 = [i for i in plan.intents if i.pass_id == "pass3"]
        self.assertTrue(any(i.queue_entry_id == REPAIR_ID for i in pass3), "Pass 3 must dispatch repair entry")
        repair_intents = [i for i in plan.intents if i.queue_entry_id == REPAIR_ID]
        self.assertEqual(len(repair_intents), 1)
        self.assertEqual(repair_intents[0].queue_pass_phase, "repair")
        self.assertEqual(
            repair_intents[0].micro_workflow,
            ["validator", "ira", "final_validator"],
        )
        self.assertTrue(repair_intents[0].strict_mode)
        deepen = [i for i in plan.intents if i.queue_entry_id == TRIGGER_ID]
        self.assertEqual(len(deepen), 1)
        from eat_queue_core.workflows import WORKFLOW_RESUME_ROADMAP_DEEPEN

        self.assertEqual(deepen[0].micro_workflow, WORKFLOW_RESUME_ROADMAP_DEEPEN)
        self.assertTrue(plan.inline_pass3_drain, "repair + forward in one plan must set inline_pass3_drain")
        self.assertFalse(
            plan.has_anticipatory_repair_slot,
            "snapshot already has repair line — Pass 3 binds to real id, not anticipatory",
        )
        self.assertEqual([i.pass_id for i in plan.intents], ["pass1", "pass3"])
        self.assertFalse(repair_intents[0].is_anticipatory_drain)
        self.assertEqual(set(plan.consumed_ids), {TRIGGER_ID, REPAIR_ID})
        self.assertGreaterEqual(len(decisions), 4, "each FSM transition should log")

    def test_anticipatory_deepen_only_two_intents_pass1_then_pass3(self) -> None:
        """One deepen line in snapshot → Pass 1 + anticipatory Pass 3 (repair id TBD until L1 appends)."""
        from eat_queue_core.workflows import (
            WORKFLOW_RESUME_ROADMAP_DEEPEN,
            WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT,
            anticipatory_repair_drain_queue_entry_id,
        )

        path = _FIXTURE_DIR / "deepen_only.jsonl"
        text = path.read_text(encoding="utf-8")
        entries = parse_queue_jsonl(text)
        plan, _ = build_plan(entries, parent_run_id="golden-anticipatory")

        self.assertEqual(len(plan.intents), 2)
        self.assertEqual([i.pass_id for i in plan.intents], ["pass1", "pass3"])
        self.assertTrue(plan.inline_pass3_drain)
        self.assertTrue(plan.has_anticipatory_repair_slot)
        p1, p3 = plan.intents
        self.assertEqual(p1.queue_entry_id, "only-deepen-gmm-20260403T120000Z")
        self.assertEqual(p1.micro_workflow, WORKFLOW_RESUME_ROADMAP_DEEPEN)
        self.assertTrue(p3.is_anticipatory_drain)
        self.assertEqual(
            p3.queue_entry_id,
            anticipatory_repair_drain_queue_entry_id("golden-anticipatory", "only-deepen-gmm-20260403T120000Z"),
        )
        self.assertEqual(p3.micro_workflow, WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT)
        self.assertEqual(p3.queue_pass_phase, "repair")

    def test_validation_result_model(self) -> None:
        from eat_queue_core.models import ValidationResult

        v = ValidationResult(
            primary_code="state_hygiene_failure",
            severity="high",
            recommended_action="repair_append",
            report_path=".technical/Validator/x.md",
            hygiene_issues=["skew"],
        )
        self.assertEqual(v.primary_code, "state_hygiene_failure")

    def test_validate_ledger_steps_executed_ok(self) -> None:
        from eat_queue_core.ledger_validate import validate_ledger_steps_executed
        from eat_queue_core.workflows import WORKFLOW_RESUME_ROADMAP_DEEPEN

        text = (_FIXTURE_DIR / "ledger_ok.yaml").read_text(encoding="utf-8")
        ok, err = validate_ledger_steps_executed(WORKFLOW_RESUME_ROADMAP_DEEPEN, text)
        self.assertTrue(ok, err)

    def test_validate_ledger_steps_executed_missing_step_fails(self) -> None:
        from eat_queue_core.ledger_validate import validate_ledger_steps_executed
        from eat_queue_core.workflows import WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT

        text = (_FIXTURE_DIR / "ledger_missing_validator_second.yaml").read_text(encoding="utf-8")
        ok, err = validate_ledger_steps_executed(WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT, text)
        self.assertFalse(ok)
        self.assertIn("mismatch", err)

    def test_validate_executed_micro_workflow(self) -> None:
        from eat_queue_core.ledger_validate import validate_executed_micro_workflow
        from eat_queue_core.workflows import WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT

        yaml_text = """
executed_micro_workflow:
  - validator
  - ira
  - final_validator
"""
        ok, err = validate_executed_micro_workflow(WORKFLOW_RESUME_ROADMAP_REPAIR_HANDOFF_AUDIT, yaml_text)
        self.assertTrue(ok, err)


if __name__ == "__main__":
    unittest.main()
