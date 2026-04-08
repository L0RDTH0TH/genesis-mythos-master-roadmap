#!/usr/bin/env python3
"""Serialize GitForge across parallel EAT-QUEUE tracks via .technical/.gitforge.lock.

Usage (from vault root):
  python3 scripts/gitforge_lock.py acquire --vault-root /path/to/vault --track sandbox --timeout 30
  python3 scripts/gitforge_lock.py release --vault-root /path/to/vault

Acquire: O_EXCL create lock JSON; poll until success or timeout (seconds).
Release: remove lock only if pid in file matches this process (best-effort stale cleanup).
Exit codes: 0 = acquired / released; 1 = acquire timeout; 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone


def _lock_path(vault_root: str) -> str:
    return os.path.join(vault_root, ".technical", ".gitforge.lock")


def acquire(vault_root: str, track: str | None, timeout_s: float) -> int:
    os.makedirs(os.path.join(vault_root, ".technical"), exist_ok=True)
    path = _lock_path(vault_root)
    payload = {
        "parallel_track": track or "unknown",
        "pid": os.getpid(),
        "started_iso": datetime.now(timezone.utc).isoformat(),
    }
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    deadline = time.monotonic() + max(0.1, timeout_s)
    while time.monotonic() < deadline:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            try:
                os.write(fd, raw)
            finally:
                os.close(fd)
            return 0
        except FileExistsError:
            time.sleep(0.15)
    return 1


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def release(vault_root: str) -> int:
    """Remove lock if holder process has exited (acquire was a subprocess) or pid matches us."""
    path = _lock_path(vault_root)
    if not os.path.isfile(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        holder = int(data.get("pid", 0))
        me = os.getpid()
        if holder == me or not _pid_alive(holder):
            os.remove(path)
            return 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError):
        return 0
    return 1


def main() -> int:
    p = argparse.ArgumentParser(description="GitForge parallel lock helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("acquire", help="Exclusive lock (poll until timeout)")
    a.add_argument("--vault-root", required=True)
    a.add_argument("--track", default=None, help="parallel_track label (sandbox|godot|...)")
    a.add_argument("--timeout", type=float, default=30.0)

    r = sub.add_parser("release", help="Release lock if owned by this pid")
    r.add_argument("--vault-root", required=True)

    args = p.parse_args()
    if args.cmd == "acquire":
        return acquire(args.vault_root, args.track, args.timeout)
    if args.cmd == "release":
        return release(args.vault_root)
    return 2


if __name__ == "__main__":
    sys.exit(main())
