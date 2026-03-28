"""
Contract tests for Plan-mode prompt-crafter: expected-queue.jsonl shape and param validation.
Given A/B/C resolution (or fixture payload), assert resolved payload matches expected shape
and has no param leaks (params only contain allowed keys for that mode).
"""

import json
import os
import unittest

# Allow importing sb_contracts from parent
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sb_contracts.queue import validate_entry

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures", "prompt-crafter")
EXPECTED_QUEUE_PATH = os.path.join(FIXTURE_DIR, "expected-queue.jsonl")

# Allowed params per mode for param-leak assertion (subset; extend as needed)
ALLOWED_PARAMS_INGEST = {"context_mode", "max_candidates", "rationale_style", "user_guidance", "prompt", "source_file", "profile"}
ALLOWED_PARAMS_RESUME_ROADMAP = {"action", "project_id", "phase", "sectionOrTaskLocator", "enable_context_tracking", "enable_research", "research_queries", "async_research", "research_distill", "handoff_gate", "min_handoff_conf", "inject_extra_state", "token_cap", "max_depth", "branch_factor", "profile", "userText", "queue_next"}


def allowed_params_for_mode(mode: str) -> set:
    """Return allowed top-level param keys for mode (for param-leak check)."""
    if mode == "INGEST MODE":
        return ALLOWED_PARAMS_INGEST
    if mode == "RESUME-ROADMAP":
        return ALLOWED_PARAMS_RESUME_ROADMAP
    return set()  # unknown mode: no param check (or extend as needed)


class TestExpectedQueueFixture(unittest.TestCase):
    """expected-queue.jsonl exists and each line is valid queue payload."""

    def test_fixture_file_exists(self):
        self.assertTrue(os.path.isfile(EXPECTED_QUEUE_PATH), f"Fixture {EXPECTED_QUEUE_PATH} missing")

    def test_each_line_valid_json_and_required_fields(self):
        if not os.path.isfile(EXPECTED_QUEUE_PATH):
            self.skipTest("expected-queue.jsonl not found")
        with open(EXPECTED_QUEUE_PATH, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                with self.subTest(line=line[:80]):
                    obj = json.loads(line)
                    self.assertIsInstance(obj, dict, f"Line {i}: must be JSON object")
                    self.assertIn("mode", obj, f"Line {i}: must have 'mode'")
                    self.assertIsInstance(obj["mode"], str, f"Line {i}: mode must be string")
                    self.assertTrue(validate_entry(obj), f"Line {i}: must pass validate_entry")

    def test_ingest_mode_params_match_expected_shape(self):
        if not os.path.isfile(EXPECTED_QUEUE_PATH):
            self.skipTest("expected-queue.jsonl not found")
        with open(EXPECTED_QUEUE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("mode") != "INGEST MODE":
                    continue
                allowed = allowed_params_for_mode("INGEST MODE")
                params = obj.get("params") or {}
                for key in params:
                    self.assertIn(key, allowed, f"Param leak: '{key}' not in allowed INGEST params")
                # Fixture shape: context_mode, max_candidates, rationale_style
                self.assertIn("context_mode", params)
                self.assertIn("max_candidates", params)
                self.assertEqual(params["context_mode"], "strict-para")
                self.assertEqual(params["max_candidates"], 7)
                return
        self.fail("No INGEST MODE line in expected-queue.jsonl")


class TestResolvedPayloadShape(unittest.TestCase):
    """Resolved Plan-mode payload (simulated A/B/C outcome) matches expected shape."""

    def test_resolved_ingest_payload_has_required_keys(self):
        # Simulated resolved payload after A/B/C + manual text for INGEST MODE
        resolved = {
            "mode": "INGEST MODE",
            "id": "req-1",
            "params": {"context_mode": "strict-para", "max_candidates": 7, "rationale_style": "concise"},
        }
        self.assertTrue(validate_entry(resolved))
        self.assertIsInstance(resolved["mode"], str)
        self.assertTrue(len(resolved["mode"]) > 0)

    def test_resolved_payload_params_no_leak(self):
        resolved = {
            "mode": "INGEST MODE",
            "params": {"context_mode": "strict-para", "max_candidates": 7, "rationale_style": "concise"},
        }
        allowed = allowed_params_for_mode(resolved["mode"])
        for key in resolved.get("params") or {}:
            self.assertIn(key, allowed, f"Param leak: '{key}'")


if __name__ == "__main__":
    unittest.main()
