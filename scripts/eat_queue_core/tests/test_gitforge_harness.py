"""Tests for post_queue_gitforge harness."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from eat_queue_core.post_queue_gitforge import run_post_queue_gitforge


def _write_min_config(root: Path) -> Path:
    cfg = root / "Second-Brain-Config.md"
    cfg.write_text(
        """# Test config

```yaml
gitforge:
  enabled: true
  harness_enabled: true
  modes:
    balance:
      tag: true
      export_sync: false
  integration_branch: "iteration-2-roadmap-rules"
```

```yaml
parallel_execution:
  enabled: false
  gitforge:
    lock_timeout_seconds: 5
```
""",
        encoding="utf-8",
    )
    return cfg


class TestPostQueueGitforge(unittest.TestCase):
    def test_skip_queue_not_success(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            cfg = _write_min_config(t)
            handoff = {
                "agent": "GitForge",
                "mode": "balance",
                "queue_success": False,
                "changes_summary": "test",
                "vault_root": str(t),
            }
            r = run_post_queue_gitforge(t, handoff, cfg)
            self.assertEqual(r.exit_code, 0)
            self.assertEqual(r.payload.get("reason"), "queue_not_clean_success")

    def test_skip_harness_disabled(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            cfg = t / "c.md"
            cfg.write_text(
                """```yaml
gitforge:
  enabled: true
  harness_enabled: false
```
""",
                encoding="utf-8",
            )
            handoff = {
                "queue_success": True,
                "mode": "balance",
                "vault_root": str(t),
            }
            r = run_post_queue_gitforge(t, handoff, cfg)
            self.assertEqual(r.exit_code, 0)
            self.assertEqual(r.payload.get("reason"), "harness_disabled")

    def test_skip_fast_mode(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            cfg = _write_min_config(t)
            handoff = {"queue_success": True, "mode": "fast", "vault_root": str(t)}
            r = run_post_queue_gitforge(t, handoff, cfg)
            self.assertEqual(r.exit_code, 0)
            self.assertEqual(r.payload.get("reason"), "unexpected_fast_mode_handoff")

    def test_json_roundtrip_handoff(self) -> None:
        from eat_queue_core.post_queue_gitforge import load_handoff_json

        import tempfile

        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            p = t / "h.json"
            obj = {"queue_success": False, "mode": "balance"}
            p.write_text(json.dumps(obj), encoding="utf-8")
            got = load_handoff_json(p, None)
            self.assertEqual(got["queue_success"], False)


if __name__ == "__main__":
    unittest.main()
