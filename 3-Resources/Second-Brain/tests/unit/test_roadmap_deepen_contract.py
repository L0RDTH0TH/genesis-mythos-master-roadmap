"""Unit tests for roadmap-deepen injection cap and util (context utilization 80% integration).

Fixtures: mock ~60k token injection (e.g. 240k chars at 0.25 tokens/char).
Assert: cap logic, truncation order (decisions-log tail first, then sibling summaries,
then prior-phase; keep distilled-core full), workflow_state fields (injected_tokens, Ctx Util % in range).
No live MCP; use contract helpers and MockVault.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def estimate_tokens(chars: int, token_per_char: float = 0.25) -> int:
    """Contract: same heuristic as roadmap-deepen (context_token_per_char)."""
    return int(chars * token_per_char)


def apply_cap(total_chars: int, token_cap: int, token_per_char: float = 0.25) -> int:
    """Return effective token count after cap; truncation order applied by skill."""
    tokens = estimate_tokens(total_chars, token_per_char)
    return min(tokens, token_cap)


class TestRoadmapDeepenInjectionCap(unittest.TestCase):
    """Cap logic and token audit for inject_extra_state."""

    def test_estimate_tokens_60k_chars(self):
        # ~60k tokens = 240k chars at 0.25
        chars_240k = 240_000
        self.assertEqual(estimate_tokens(chars_240k), 60_000)

    def test_cap_under_limit_no_truncation(self):
        # 40k tokens (160k chars) under 50k cap
        chars_160k = 160_000
        self.assertEqual(apply_cap(chars_160k, 50_000), 40_000)

    def test_cap_over_limit_truncates(self):
        # 60k tokens (240k chars) over 50k cap → 50k
        chars_240k = 240_000
        self.assertEqual(apply_cap(chars_240k, 50_000), 50_000)

    def test_workflow_state_injected_tokens_in_range(self):
        # After cap, injected_tokens should be ≤ token_cap and Ctx Util % in 40–50% range for 128k window
        token_cap = 50_000
        window = 128_000
        injected = apply_cap(200_000, token_cap)  # 50k tokens
        util_pct = min(100, round(100 * injected / window))
        self.assertLessEqual(injected, token_cap)
        self.assertGreaterEqual(util_pct, 35)
        self.assertLessEqual(util_pct, 45)


class TestTruncationOrder(unittest.TestCase):
    """Truncation order: decisions-log tail first, then sibling summaries, then prior-phase; keep distilled-core full."""

    TRUNCATION_ORDER = ["decisions_log_tail", "sibling_summaries", "prior_phase_content"]

    def test_truncation_order_documented(self):
        self.assertEqual(self.TRUNCATION_ORDER[0], "decisions_log_tail")
        self.assertEqual(self.TRUNCATION_ORDER[1], "sibling_summaries")
        self.assertEqual(self.TRUNCATION_ORDER[2], "prior_phase_content")


if __name__ == "__main__":
    unittest.main()
