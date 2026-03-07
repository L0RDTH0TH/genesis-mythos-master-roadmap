"""Unit tests for log and error format."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sb_contracts.log_format import (
    validate_pipeline_log_line,
    validate_watcher_result_line,
    validate_errors_entry,
)


class TestPipelineLogLine(unittest.TestCase):
    def test_valid_line(self):
        line = "2026-03-01 14:30 | Excerpt: [snippet] | PARA: Project | Changes: TL;DR; Backup: /x.md | Confidence: 88% | Proposed MV: 1-Projects/X/Note.md | Flag: none | Loop: attempted: false, band: none"
        self.assertTrue(validate_pipeline_log_line(line))

    def test_missing_excerpt_invalid(self):
        line = "2026-03-01 14:30 | PARA: P | Changes: x | Confidence: 88% | Proposed MV: x | Flag: none | Loop: none"
        self.assertFalse(validate_pipeline_log_line(line))


class TestWatcherResultLine(unittest.TestCase):
    def test_valid_success(self):
        line = 'requestId: req-1 | status: success | message: "Moved" | trace: "" | completed: 2026-03-01T14:35:00.000Z'
        self.assertTrue(validate_watcher_result_line(line))

    def test_missing_completed_invalid(self):
        line = 'requestId: req-1 | status: success | message: "x" | trace: ""'
        self.assertFalse(validate_watcher_result_line(line))


class TestErrorsEntry(unittest.TestCase):
    def test_valid_entry(self):
        content = "### 2026-03-01 12:00 — Title\n\n#### Trace\n- Error\n\n#### Summary\n**Root cause**: x"
        self.assertTrue(validate_errors_entry(content))

    def test_missing_trace_invalid(self):
        self.assertFalse(validate_errors_entry("### Title\n\n#### Summary\nx"))


if __name__ == "__main__":
    unittest.main()
