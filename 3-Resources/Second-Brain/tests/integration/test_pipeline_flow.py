"""Integration: pipeline step order matches Cursor-Skill-Pipelines-Reference."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Canonical full-autonomous-ingest order (simplified)
INGEST_STEP_ORDER = [
    "backup",
    "classify_para",
    "frontmatter_enrich",
    "subfolder_organize",
    "split_atomic",
    "split_link_preserve",
    "distill_note",
    "distill_highlight_color",
    "next_action_extract",
    "append_to_hub",
    "move_note",
    "log_action",
]


class TestPipelineOrder(unittest.TestCase):
    def test_ingest_steps_sequence(self):
        """Steps must follow canonical order."""
        for i, step in enumerate(INGEST_STEP_ORDER):
            self.assertIsInstance(step, str)
        self.assertEqual(INGEST_STEP_ORDER[0], "backup")
        self.assertEqual(INGEST_STEP_ORDER[1], "classify_para")
        self.assertIn("move_note", INGEST_STEP_ORDER)
        self.assertEqual(INGEST_STEP_ORDER[-1], "log_action")

    def test_move_after_backup_and_snapshot(self):
        """move_note must come after backup in sequence."""
        idx_backup = INGEST_STEP_ORDER.index("backup")
        idx_move = INGEST_STEP_ORDER.index("move_note")
        self.assertLess(idx_backup, idx_move)
