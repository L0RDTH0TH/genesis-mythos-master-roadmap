"""Unit tests for config and confidence bands (Second-Brain-Config, Parameters)."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sb_contracts.config import get_confidence_band, parse_config_snippet


class TestConfigSnippet(unittest.TestCase):
    def test_batch_size_for_snapshot(self):
        content = "batch_size_for_snapshot: 5"
        cfg = parse_config_snippet(content)
        self.assertEqual(cfg.get("batch_size_for_snapshot"), 5)

    def test_archive_age_days(self):
        content = "archive:\n  age_days: 90"
        cfg = parse_config_snippet(content)
        self.assertIn("age_days", cfg or {})

    def test_confidence_bands_override(self):
        content = "high_threshold: 90\nmid: [80, 89]"
        cfg = parse_config_snippet(content)
        self.assertEqual(cfg.get("high_threshold"), 90)


class TestConfidenceBands(unittest.TestCase):
    def test_default_high_85(self):
        self.assertEqual(get_confidence_band(85), "high")
        self.assertEqual(get_confidence_band(90), "high")

    def test_default_mid_72_84(self):
        self.assertEqual(get_confidence_band(72), "mid")
        self.assertEqual(get_confidence_band(84), "mid")
        self.assertEqual(get_confidence_band(78), "mid")

    def test_default_low(self):
        self.assertEqual(get_confidence_band(71), "low")
        self.assertEqual(get_confidence_band(0), "low")

    def test_tunable_high_threshold_90(self):
        config = {"confidence_bands": {"high_threshold": 90, "mid": [80, 89]}}
        self.assertEqual(get_confidence_band(85, config), "mid")
        self.assertEqual(get_confidence_band(90, config), "high")

    def test_fallback_when_config_missing(self):
        self.assertEqual(get_confidence_band(84, None), "mid")
        self.assertEqual(get_confidence_band(85, {}), "high")


if __name__ == "__main__":
    unittest.main()
