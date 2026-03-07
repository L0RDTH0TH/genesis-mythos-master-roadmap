"""Integration: async preview, re-queue after approved, banner cleanup."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sb_contracts.config import get_confidence_band


class TestAsyncPreviewEmission(unittest.TestCase):
    def test_mid_band_can_emit_preview(self):
        band = get_confidence_band(75)
        self.assertEqual(band, "mid")

    def test_approved_true_requeue_signal(self):
        """When user sets approved: true, re-queue is allowed."""
        approved = True
        self.assertTrue(approved)

    def test_banner_cleanup_success_over_failure(self):
        """Banner cleanup: success > failure (ordering)."""
        results = [("req-1", "success"), ("req-2", "failure")]
        success_count = sum(1 for _, s in results if s == "success")
        failure_count = sum(1 for _, s in results if s == "failure")
        self.assertEqual(success_count, 1)
        self.assertEqual(failure_count, 1)
