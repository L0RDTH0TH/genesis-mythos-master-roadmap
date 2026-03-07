"""Unit tests for frontmatter-enrich contract."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import parse_frontmatter


def enrich_frontmatter_from_classification(content: str, classification: dict) -> str:
    """Reference implementation: add status, confidence, para-type, created, links."""
    fm, body = parse_frontmatter(content)
    fm["status"] = classification.get("status", "active")
    fm["confidence"] = str(classification.get("confidence", 85))
    fm["para-type"] = classification.get("para-type", "Resource")
    fm["created"] = classification.get("created", "2026-03-01")
    links = classification.get("links", ["[[Resources Hub]]"])
    fm["links"] = str(links) if isinstance(links, list) else links
    if classification.get("project-id"):
        fm["project-id"] = classification["project-id"]
    lines = ["---"] + [f"{k}: {v}" for k, v in fm.items()] + ["---", body.strip() or ""]
    return "\n".join(lines)


class TestFrontmatterEnrichContract(unittest.TestCase):
    def setUp(self):
        self.mock_content = "---\ntitle: Mock Note\n---\nThis is a test note."
        self.mock_classification = {
            "para-type": "Resource",
            "project-id": "test-project",
            "confidence": 90,
            "created": "2026-03-01",
            "links": ["[[Resources Hub]]", "[[Test-Project MOC]]"],
        }

    def test_enrich_basic(self):
        updated = enrich_frontmatter_from_classification(
            self.mock_content, self.mock_classification
        )
        self.assertIn("para-type: Resource", updated)
        self.assertIn("status: active", updated)
        self.assertIn("confidence: 90", updated)

    def test_links_array_format(self):
        classification = {"para-type": "Resource", "confidence": 85, "links": ["[[Resources Hub]]"]}
        updated = enrich_frontmatter_from_classification("---\ntitle: X\n---\nBody", classification)
        self.assertIn("links:", updated)
        self.assertIn("[[Resources Hub]]", updated)

    def test_project_id_set_when_provided(self):
        updated = enrich_frontmatter_from_classification(
            self.mock_content, self.mock_classification
        )
        self.assertIn("project-id: test-project", updated)

    def test_parse_frontmatter_no_dash_returns_empty_fm(self):
        fm, body = parse_frontmatter("No frontmatter here.")
        self.assertEqual(fm, {})
        self.assertEqual(body, "No frontmatter here.")

    def test_parse_frontmatter_with_dash_returns_fm_and_body(self):
        text = "---\ntitle: Test\ntags: [pkm, testing]\n---\nBody text"
        fm, body = parse_frontmatter(text)
        self.assertIn("title", fm)
        self.assertEqual(fm.get("title"), "Test")
        self.assertIn("Body text", body)


if __name__ == "__main__":
    unittest.main()
