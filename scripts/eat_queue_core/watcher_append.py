"""Append canonical Watcher-Result.md lines (single-line trace JSON)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .lane_queue_config import watcher_canonical_path


def append_watcher_telemetry_line(
    vault_root: Path,
    *,
    request_id: str,
    message: str,
    trace_payload: dict[str, Any],
) -> Path:
    """
    Read-then-append one line. ``trace`` field contains JSON with internal quotes escaped
    for the fixed ``requestId | status | message | trace | completed`` shape.
    """
    path = watcher_canonical_path(vault_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    trace_json = json.dumps(trace_payload, ensure_ascii=False)
    trace_esc = trace_json.replace("\\", "\\\\").replace('"', '\\"')
    msg_esc = message.replace("\\", "\\\\").replace('"', '\\"')
    line = (
        f'requestId: {request_id} | status: success | message: "{msg_esc}" | '
        f'trace: "{trace_esc}" | completed: {now}\n'
    )
    prev = path.read_text(encoding="utf-8") if path.is_file() else ""
    path.write_text(prev + line, encoding="utf-8")
    return path
