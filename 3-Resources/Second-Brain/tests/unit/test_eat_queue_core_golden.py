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

        pass3 = [i for i in plan.intents if i.pass_id == "pass3"]
        self.assertTrue(any(i.queue_entry_id == REPAIR_ID for i in pass3), "Pass 3 must dispatch repair entry")
        repair_intents = [i for i in plan.intents if i.queue_entry_id == REPAIR_ID]
        self.assertEqual(len(repair_intents), 1)
        self.assertEqual(repair_intents[0].queue_pass_phase, "repair")
        self.assertIn(TRIGGER_ID, plan.consumed_ids)
        self.assertGreaterEqual(len(decisions), 4, "each FSM transition should log")

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


if __name__ == "__main__":
    unittest.main()
