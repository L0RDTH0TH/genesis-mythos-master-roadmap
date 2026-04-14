"""Harness snapshot/verify: mutation detection and exit codes."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

_VAULT = Path(__file__).resolve().parents[3]


def _run_harness(args: list[str]) -> tuple[int, str]:
    cmd = [sys.executable, "-m", "scripts.eat_queue_core.harness", *args]
    env = {"PYTHONPATH": str(_VAULT)}
    p = subprocess.run(
        cmd,
        cwd=str(_VAULT),
        capture_output=True,
        text=True,
        env={**dict(__import__("os").environ), **env},
        check=False,
    )
    # Harness JSON goes to stdout; merge stderr for error messages on failure.
    return p.returncode, (p.stdout or "") + (p.stderr or "")


class HarnessVerifyTest(unittest.TestCase):
    def test_verify_ok_when_unchanged(self) -> None:
        snap_path = _VAULT / ".technical" / "_harness_verify_test_snapshot.json"
        try:
            rc, out = _run_harness(
                ["snapshot", "--vault-root", str(_VAULT), "--queue", ".technical/prompt-queue.jsonl"]
            )
            self.assertEqual(rc, 0, out)
            snap = json.loads(out)
            snap_path.write_text(json.dumps(snap), encoding="utf-8")
            rc2, out2 = _run_harness(
                [
                    "verify",
                    "--vault-root",
                    str(_VAULT),
                    "--queue",
                    ".technical/prompt-queue.jsonl",
                    "--expected-snapshot",
                    str(snap_path),
                ]
            )
            self.assertEqual(rc2, 0, out2)
            body = json.loads(out2.strip())
            self.assertTrue(body.get("ok"), body)
        finally:
            if snap_path.is_file():
                snap_path.unlink()

    def test_verify_fails_after_mutation(self) -> None:
        pq = _VAULT / ".technical" / "_harness_verify_mutation_pq.jsonl"
        cfg = _VAULT / "3-Resources" / "Second-Brain" / "Second-Brain-Config.md"
        snap_path = _VAULT / ".technical" / "_harness_verify_mutation_snapshot.json"
        line = json.dumps(
            {"id": "verify-test-1", "mode": "INGEST_MODE", "prompt": "x", "source_file": ""}
        )
        try:
            pq.parent.mkdir(parents=True, exist_ok=True)
            pq.write_text(line + "\n", encoding="utf-8")
            rc, out = _run_harness(
                [
                    "snapshot",
                    "--vault-root",
                    str(_VAULT),
                    "--config",
                    str(cfg),
                    "--queue",
                    str(pq.relative_to(_VAULT)),
                ]
            )
            self.assertEqual(rc, 0, out)
            snap_path.write_text(out.strip(), encoding="utf-8")
            pq.write_text(line + "\n" + line + "\n", encoding="utf-8")
            rc2, out2 = _run_harness(
                [
                    "verify",
                    "--vault-root",
                    str(_VAULT),
                    "--config",
                    str(cfg),
                    "--queue",
                    str(pq.relative_to(_VAULT)),
                    "--expected-snapshot",
                    str(snap_path),
                ]
            )
            self.assertEqual(rc2, 2, out2)
            body = json.loads(out2.strip())
            self.assertFalse(body.get("ok"))
            self.assertIn("mutation_recovery_mode", body)
            self.assertEqual(body.get("recovery_hint"), "rerun_full_cycle_from_disk")
        finally:
            for p in (pq, snap_path):
                if p.is_file():
                    p.unlink()


if __name__ == "__main__":
    unittest.main()
