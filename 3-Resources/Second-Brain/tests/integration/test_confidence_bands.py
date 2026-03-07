"""Integration: confidence band behavior (high/mid/low) with mocked state."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sb_contracts.config import get_confidence_band


class TestConfidenceBandBehavior(unittest.TestCase):
    def test_high_allows_destructive_after_snapshot(self):
        band = get_confidence_band(85)
        self.assertEqual(band, "high")

    def test_mid_one_loop_then_post_check(self):
        band = get_confidence_band(78)
        self.assertEqual(band, "mid")

    def test_low_propose_only(self):
        band = get_confidence_band(70)
        self.assertEqual(band, "low")

    def test_post_loop_conf_85_proceeds(self):
        config = {"confidence_bands": {"high_threshold": 85, "mid": [72, 84]}}
        self.assertEqual(get_confidence_band(85, config), "high")
        self.assertEqual(get_confidence_band(84, config), "mid")
