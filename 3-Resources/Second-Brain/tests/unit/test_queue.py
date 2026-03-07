"""
Unit tests for queue processor contract: parse, validate, dedup, sort.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sb_contracts.queue import (
    parse_queue_line,
    validate_entry,
    dedup_entries,
    canonical_sort_key,
    KNOWN_MODES,
    CANONICAL_ORDER,
)


class TestParseQueueLine(unittest.TestCase):
    def test_valid_line(self):
        line = '{"mode":"DISTILL MODE","source_file":"1-Projects/X/Note.md","id":"req-1"}'
        obj, ok = parse_queue_line(line)
        self.assertTrue(ok)
        self.assertEqual(obj["mode"], "DISTILL MODE")
        self.assertEqual(obj["source_file"], "1-Projects/X/Note.md")

    def test_invalid_json_skipped(self):
        obj, ok = parse_queue_line("not json at all")
        self.assertFalse(ok)
        self.assertIsNone(obj)

    def test_missing_mode_invalid(self):
        obj, ok = parse_queue_line('{"source_file":"x.md"}')
        self.assertFalse(ok)
        self.assertIsNone(obj)

    def test_mode_required_string(self):
        obj, ok = parse_queue_line('{"mode": 123}')
        self.assertFalse(ok)

    def test_commander_fields_preserved(self):
        line = '{"mode":"INGEST MODE","commander_source":true,"commander_macro":"Queue Ingest"}'
        obj, ok = parse_queue_line(line)
        self.assertTrue(ok)
        self.assertTrue(obj.get("commander_source"))
        self.assertEqual(obj.get("commander_macro"), "Queue Ingest")


class TestValidateEntry(unittest.TestCase):
    def test_valid_entry(self):
        self.assertTrue(validate_entry({"mode": "INGEST MODE"}))

    def test_queue_failed_filtered(self):
        self.assertFalse(validate_entry({"mode": "INGEST MODE", "queue_failed": True}))

    def test_tags_queue_failed_filtered(self):
        self.assertFalse(validate_entry({"mode": "INGEST MODE", "tags": ["queue-failed"]}))

    def test_unknown_mode_still_valid_for_parse(self):
        self.assertTrue(validate_entry({"mode": "CUSTOM MODE"}))


class TestDedupEntries(unittest.TestCase):
    def test_same_mode_prompt_source_keeps_first(self):
        entries = [
            {"mode": "INGEST MODE", "prompt": "p", "source_file": "a.md", "timestamp": "1"},
            {"mode": "INGEST MODE", "prompt": "p", "source_file": "a.md", "timestamp": "2"},
        ]
        out = dedup_entries(entries)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["timestamp"], "1")

    def test_different_modes_same_file_kept(self):
        entries = [
            {"mode": "INGEST MODE", "source_file": "x.md"},
            {"mode": "DISTILL MODE", "source_file": "x.md"},
        ]
        out = dedup_entries(entries)
        self.assertEqual(len(out), 2)


class TestCanonicalSortKey(unittest.TestCase):
    def test_ingest_before_distill(self):
        a = {"mode": "INGEST MODE"}
        b = {"mode": "DISTILL MODE"}
        self.assertLess(canonical_sort_key(a)[0], canonical_sort_key(b)[0])

    def test_order_matches_canonical(self):
        for i, mode in enumerate(KNOWN_MODES, start=1):
            self.assertEqual(CANONICAL_ORDER.get(mode), i)


class TestFastPath(unittest.TestCase):
    def test_single_valid_entry_no_dedup_needed(self):
        entries = [{"mode": "EXPRESS MODE", "source_file": "a.md"}]
        out = dedup_entries(entries)
        self.assertEqual(len(out), 1)


if __name__ == "__main__":
    unittest.main()
