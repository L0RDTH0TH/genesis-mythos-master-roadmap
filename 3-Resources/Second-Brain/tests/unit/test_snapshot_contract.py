"""
Unit tests for obsidian-snapshot contract: snapshot frontmatter must contain
original_path, snapshot_type, snapshot_created, snapshot_hash, etc.
"""

import unittest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def build_snapshot_frontmatter(
    original_path: str,
    original_title: str,
    pipeline: str,
    snapshot_type: str,
    snapshot_hash: str,
    confidence: int,
    flag: str = "none",
) -> dict:
    """Build snapshot frontmatter dict per obsidian-snapshot SKILL required keys."""
    return {
        "original_path": original_path,
        "original_title": original_title,
        "pipeline": pipeline,
        "snapshot_type": snapshot_type,
        "snapshot_created": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "snapshot_hash": snapshot_hash,
        "confidence": confidence,
        "flag": flag,
        "immutable": True,
        "para-type": "Archive",
        "status": "frozen",
    }


REQUIRED_SNAPSHOT_KEYS = {
    "original_path",
    "original_title",
    "pipeline",
    "snapshot_type",
    "snapshot_created",
    "snapshot_hash",
    "confidence",
    "flag",
    "immutable",
    "para-type",
    "status",
}


class TestSnapshotContract(unittest.TestCase):
    def test_build_snapshot_frontmatter_has_all_required_keys(self):
        fm = build_snapshot_frontmatter(
            original_path="1-Projects/X/Note.md",
            original_title="Note",
            pipeline="ingest",
            snapshot_type="per-change",
            snapshot_hash="abc123",
            confidence=88,
        )
        for key in REQUIRED_SNAPSHOT_KEYS:
            self.assertIn(key, fm, msg=f"Missing required key: {key}")

    def test_snapshot_type_per_change_or_batch(self):
        for st in ("per-change", "batch"):
            fm = build_snapshot_frontmatter(
                "a.md", "a", "distill", st, "h1", 85
            )
            self.assertEqual(fm["snapshot_type"], st)

    def test_immutable_and_status_frozen(self):
        fm = build_snapshot_frontmatter(
            "a.md", "a", "archive", "per-change", "h", 90
        )
        self.assertTrue(fm["immutable"])
        self.assertEqual(fm["status"], "frozen")
        self.assertEqual(fm["para-type"], "Archive")


if __name__ == "__main__":
    unittest.main()
