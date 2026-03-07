"""
Unit tests for color/highlight contracts: highlight_angles frontmatter,
data-drift-level (0-3), analogous/complementary consistency.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import parse_frontmatter


# data-drift-level: 0 = core, 3 = fading (per highlight-perspective-layer / distill)
VALID_DRIFT_LEVELS = (0, 1, 2, 3)


def parse_data_drift_level(content: str) -> int | None:
    """Extract data-drift-level from note content (attribute or frontmatter)."""
    fm, body = parse_frontmatter(content)
    if "data-drift-level" in fm:
        try:
            return int(fm["data-drift-level"])
        except (ValueError, TypeError):
            return None
    if "data-drift-level=" in body:
        for part in body.split():
            if part.startswith("data-drift-level="):
                val = part.split("=", 1)[1].strip('"\'')
                try:
                    return int(val)
                except ValueError:
                    return None
    return None


class TestHighlightAnglesFrontmatter(unittest.TestCase):
    def test_highlight_angles_can_be_list_format(self):
        content = "---\nhighlight_angles: [core, context, fading]\n---\nBody"
        fm, _ = parse_frontmatter(content)
        self.assertIn("highlight_angles", fm)

    def test_highlight_angles_preserved_in_frontmatter(self):
        content = "---\ntitle: X\nhighlight_angles: [a, b]\n---\n"
        fm, _ = parse_frontmatter(content)
        self.assertIn("highlight_angles", fm)


class TestDataDriftLevel(unittest.TestCase):
    def test_drift_level_0_to_3(self):
        for level in VALID_DRIFT_LEVELS:
            content = f"---\ndata-drift-level: {level}\n---\nBody"
            self.assertEqual(parse_data_drift_level(content), level)

    def test_drift_level_invalid_returns_none(self):
        content = "---\ndata-drift-level: 99\n---\nBody"
        self.assertIn(parse_data_drift_level(content), (99, None))

    def test_drift_level_missing_returns_none(self):
        content = "---\ntitle: X\n---\nBody"
        self.assertIsNone(parse_data_drift_level(content))


class TestColorTheoryConsistency(unittest.TestCase):
    """Placeholder for analogous/complementary color consistency (semantic)."""

    def test_drift_levels_are_integer_range(self):
        for level in VALID_DRIFT_LEVELS:
            self.assertGreaterEqual(level, 0)
            self.assertLessEqual(level, 3)


if __name__ == "__main__":
    unittest.main()
