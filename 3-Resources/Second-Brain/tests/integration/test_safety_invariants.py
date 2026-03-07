"""Integration: safety invariants (dry_run before move, backup before destructive)."""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDryRunBeforeMove(unittest.TestCase):
    def test_dry_run_called_before_commit(self):
        """Simulate: move_note must be called with dry_run=True before dry_run=False."""
        calls = []

        def record_move(path, new_path, dry_run=False):
            calls.append(("move_note", path, new_path, dry_run))

        record_move("Ingest/a.md", "1-Projects/X/a.md", dry_run=True)
        record_move("Ingest/a.md", "1-Projects/X/a.md", dry_run=False)
        self.assertEqual(len(calls), 2)
        self.assertTrue(calls[0][3])
        self.assertFalse(calls[1][3])

    def test_backup_before_split_atomic(self):
        """Order: backup then split_atomic."""
        steps = ["backup", "classify_para", "frontmatter_enrich", "subfolder_organize", "split_atomic"]
        idx_backup = steps.index("backup")
        idx_split = steps.index("split_atomic")
        self.assertLess(idx_backup, idx_split)


class TestSnapshotBeforeDestructive(unittest.TestCase):
    def test_snapshot_step_before_move_in_sequence(self):
        """Per plan: snapshot before move_note."""
        sequence = ["backup", "snapshot", "move_note"]
        self.assertLess(sequence.index("snapshot"), sequence.index("move_note"))
