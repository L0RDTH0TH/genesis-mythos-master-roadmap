"""
Unit tests for path exclusions: Backups/, Logs, Hub, Watcher paths, watcher-protected.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import is_excluded_path, WATCHER_PROTECTED_PATHS


class TestPathExclusions(unittest.TestCase):
    def test_backups_excluded(self):
        self.assertTrue(is_excluded_path("Backups/Per-Change/abc.md"))
        self.assertTrue(is_excluded_path("Backups/Batch/x.md"))
        self.assertTrue(is_excluded_path("1-Projects/X/Backups/note.md"))

    def test_log_files_excluded(self):
        self.assertTrue(is_excluded_path("3-Resources/Ingest-Log.md"))
        self.assertTrue(is_excluded_path("3-Resources/Distill-Log.md"))
        self.assertTrue(is_excluded_path("Some-Log.md"))

    def test_hub_files_excluded(self):
        self.assertTrue(is_excluded_path("3-Resources/Resources Hub.md"))
        self.assertTrue(is_excluded_path("Projects Hub.md"))

    def test_watcher_paths_excluded(self):
        self.assertTrue(is_excluded_path("Ingest/watched-file.md"))
        self.assertTrue(is_excluded_path("3-Resources/Watcher-Signal.md"))
        self.assertTrue(is_excluded_path("3-Resources/Watcher-Result.md"))

    def test_archives_excluded(self):
        self.assertTrue(is_excluded_path("4-Archives/Old/note.md"))

    def test_templates_excluded(self):
        self.assertTrue(is_excluded_path("Templates/Daily.md"))

    def test_tests_folder_excluded(self):
        self.assertTrue(is_excluded_path("3-Resources/Second-Brain/tests/unit/test_queue.py"))
        self.assertTrue(is_excluded_path("3-Resources/Second-Brain/tests/fixtures/sample_note_with_mark.md"))
        self.assertTrue(is_excluded_path("3-Resources/Second-Brain/tests/helpers.py"))

    def test_watcher_protected_frontmatter(self):
        self.assertTrue(is_excluded_path("1-Projects/X/Note.md", {"watcher-protected": True}))
        self.assertTrue(is_excluded_path("a.md", {"watcher-protected": "true"}))

    def test_para_paths_not_excluded(self):
        self.assertFalse(is_excluded_path("1-Projects/MyProject/Note.md"))
        self.assertFalse(is_excluded_path("2-Areas/Area/Note.md"))
        self.assertFalse(is_excluded_path("3-Resources/Config.md"))
        self.assertFalse(is_excluded_path("Ingest/Capture.md"))

    def test_normal_note_no_frontmatter_not_excluded(self):
        self.assertFalse(is_excluded_path("1-Projects/X/Note.md", None))
        self.assertFalse(is_excluded_path("1-Projects/X/Note.md", {}))


if __name__ == "__main__":
    unittest.main()
