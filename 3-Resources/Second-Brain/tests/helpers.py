"""
Test helpers for Second Brain automated tests.
No pyyaml dependency; simple frontmatter parser and mock vault/MCP.
"""

import os

# Optional pytest for parametrize/fixtures when available
try:
    import pytest  # noqa: F401
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML-like frontmatter from note content (no pyyaml).
    If content does not start with '---\\n', return ({}, content).
    Else split on '---\\n', parse first block into key/value dict (split on first ':' per line),
    return (frontmatter_dict, body).
    """
    if not content.startswith("---\n"):
        return {}, content
    parts = content.split("---\n", 2)
    if len(parts) < 2:
        return {}, content
    fm_lines = parts[1].strip().split("\n")
    fm = {}
    for line in fm_lines:
        if ":" in line:
            idx = line.index(":")
            key = line[:idx].strip()
            value = line[idx + 1 :].strip()
            fm[key] = value
    body = parts[2] if len(parts) > 2 else ""
    return fm, body


# Watcher-protected paths (embed as strings to avoid hardcoding elsewhere)
WATCHER_PROTECTED_PATHS = frozenset({
    "Ingest/watched-file.md",
    "3-Resources/Watcher-Signal.md",
    "3-Resources/Watcher-Result.md",
})


def is_excluded_path(path: str, frontmatter: dict | None = None) -> bool:
    """
    Return True if path should be excluded from pipeline processing.
    Rules: Backups/, **/Log*.md, **/* Hub.md, Watcher paths, 4-Archives/**, Templates/**,
    and notes with watcher-protected: true in frontmatter.
    """
    path_norm = path.replace("\\", "/").strip("/")
    # Fixed Watcher paths
    if path_norm in WATCHER_PROTECTED_PATHS:
        return True
    if path_norm.startswith("Ingest/watched-file") or path_norm.startswith("3-Resources/Watcher-"):
        return True
    # Backups/
    if path_norm.startswith("Backups/") or "/Backups/" in path_norm:
        return True
    # **/Log*.md
    if "Log" in path_norm and path_norm.endswith(".md"):
        return True
    # **/* Hub.md
    if " Hub.md" in path_norm or path_norm.endswith(" Hub.md"):
        return True
    # 4-Archives/**
    if path_norm.startswith("4-Archives/") or "/4-Archives/" in path_norm:
        return True
    # Templates/**
    if path_norm.startswith("Templates/") or "/Templates/" in path_norm:
        return True
    # 3-Resources/Second-Brain/tests/** (test suite; not pipeline input; Vault-Layout)
    if "Second-Brain/tests/" in path_norm or path_norm.startswith("Second-Brain/tests/"):
        return True
    # watcher-protected frontmatter
    if frontmatter and frontmatter.get("watcher-protected") in (True, "true", "yes"):
        return True
    return False


class MockVault:
    """Dict-based mock vault: {path: content}. Optional mtime for 'created' frontmatter."""

    def __init__(self, initial: dict[str, str] | None = None, mtimes: dict[str, float] | None = None):
        self.notes = dict(initial or {})
        self.mtimes = dict(mtimes or {})

    def get(self, path: str) -> str | None:
        return self.notes.get(path)

    def set(self, path: str, content: str, mtime: float | None = None):
        self.notes[path] = content
        if mtime is not None:
            self.mtimes[path] = mtime


class MockMCP:
    """
    Mock MCP for integration/E2E; no real MCP calls.
    classify_para returns fixture dicts; other methods can be extended.
    """

    def __init__(self, classify_results: dict[str, dict] | None = None):
        self.classify_results = dict(classify_results or {})
        self.call_log = []

    def classify_para(self, path: str, content: str | None = None) -> dict:
        self.call_log.append(("classify_para", path))
        return self.classify_results.get(path, {"para-type": "Resource", "confidence": 85})
