#!/usr/bin/env python3
"""
Generate EAT-QUEUE Run Telemetry Summary (canonical MD overwrite + optional archive).

Called by Layer 1 after A.7 when telemetry_summary gates pass (see queue.mdc A.7b),
or manually for testing / dry-run.

Does not use shell cp/mv/rm on vault paths — writes via pathlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_CANONICAL = "3-Resources/Second-Brain/Docs/Core/Run-Telemetry-Summary.md"
CONFIG_PATH = "3-Resources/Second-Brain/Second-Brain-Config.md"


def _parse_telemetry_summary_config(vault: Path) -> dict[str, Any]:
    """Best-effort parse of telemetry_summary: block from Second-Brain-Config.md."""
    cfg = vault / CONFIG_PATH
    out: dict[str, Any] = {}
    if not cfg.is_file():
        return out
    text = cfg.read_text(encoding="utf-8", errors="replace")
    in_block = False
    base_indent = 0
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.match(r"^telemetry_summary:\s*$", stripped):
            in_block = True
            base_indent = len(line) - len(line.lstrip())
            continue
        if in_block:
            indent = len(line) - len(line.lstrip())
            if indent <= base_indent and stripped and not stripped.startswith("#"):
                break
            m = re.match(r"^(\s*)([a-z_]+):\s*(.+?)\s*$", line)
            if m:
                key, val = m.group(2), m.group(3).strip()
                if val.lower() in ("true", "false"):
                    out[key] = val.lower() == "true"
                elif val.startswith('"') and val.endswith('"'):
                    out[key] = val[1:-1]
                else:
                    out[key] = val
    return out


def _tail_lines(path: Path, max_lines: int) -> list[str]:
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) <= max_lines:
        return lines
    return lines[-max_lines:]


def _load_jsonl_rows(path: Path, max_rows: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-max_rows:]


def _count_watcher_dispositions(lines: list[str]) -> tuple[int, int, int]:
    """Returns (primary_dispatches_approx, success_lines, failure_lines) from tail."""
    primary_ids: set[str] = set()
    success = failure = 0
    for ln in lines:
        if "status: success" in ln:
            success += 1
        elif "status: failure" in ln:
            failure += 1
        if "segment:" in ln and "VALIDATE" in ln:
            continue
        if "requestId:" not in ln:
            continue
        m = re.search(r"requestId:\s*([^\s|]+)", ln)
        if m:
            primary_ids.add(m.group(1).strip())
    dispatched = len(primary_ids) if primary_ids else min(success + failure, max(success, failure))
    return dispatched, success, failure


def _md_cell(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def build_markdown(
    *,
    iso_ts: str,
    lane: str,
    pipeline_mode: str,
    run_trigger: str,
    overview_extra: dict[str, Any],
    watcher_tail: list[str],
    decisions_rows: list[dict[str, Any]],
    audit_tail: list[str],
    jsonl_links: list[tuple[str, str]],
    raw_source_links: list[tuple[str, str]],
) -> str:
    day = iso_ts[:10]
    lines_out: list[str] = []
    lines_out.append("---")
    lines_out.append("title: EAT-QUEUE Run Telemetry Summary")
    lines_out.append(f"created: {day}")
    lines_out.append(f"updated: {day}")
    lines_out.append("tags: [ops, eat-queue, telemetry, second-brain]")
    lines_out.append("para-type: Resource")
    lines_out.append("status: active")
    lines_out.append("source: scripts/generate_telemetry_summary.py")
    lines_out.append("---")
    lines_out.append("")
    lines_out.append(
        f"# EAT-QUEUE Run Telemetry Summary — [{iso_ts}] [{lane}] [{pipeline_mode}]"
    )
    lines_out.append("")
    lines_out.append("## Overview")
    lines_out.append("")
    lines_out.append(f"- **Run trigger:** {run_trigger}")
    d, s, f = overview_extra.get("watcher_counts", (0, 0, 0))
    lines_out.append(
        f"- **Tasks (approx from Watcher tail):** dispatched ~{d}; success lines: {s}; failure lines: {f}"
    )
    if overview_extra.get("key_decisions"):
        lines_out.append(f"- **Key decisions / notes:** {overview_extra['key_decisions']}")
    if overview_extra.get("outcomes"):
        lines_out.append(f"- **Outcomes:** {overview_extra['outcomes']}")
    if overview_extra.get("errors_summary"):
        lines_out.append(f"- **Errors summary:** {overview_extra['errors_summary']}")
    lines_out.append("")
    lines_out.append("## Atomized Decisions")
    lines_out.append("")
    lines_out.append(
        "FSM / orchestration transitions from `eat-queue-decisions.jsonl` (most recent rows; colocated with active **PQ** bundle when parallel)."
    )
    lines_out.append("")
    if decisions_rows:
        lines_out.append("| ts | rule_id | from → to | queue_entry_id | reason |")
        lines_out.append("| --- | --- | --- | --- | --- |")
        for r in decisions_rows:
            ts = _md_cell(str(r.get("ts", ""))[:32])
            rid = _md_cell(str(r.get("rule_id", "")))
            fr = _md_cell(str(r.get("from_state", "")))
            to = _md_cell(str(r.get("to_state", "")))
            qid = _md_cell(str(r.get("queue_entry_id", ""))) if r.get("queue_entry_id") else "—"
            reason = _md_cell(str(r.get("reason", ""))[:160])
            lines_out.append(f"| {ts} | `{rid}` | {fr} → {to} | `{qid}` | {reason} |")
    else:
        lines_out.append("*No rows loaded (file missing or empty).*")
    lines_out.append("")
    lines_out.append("## Full Telemetry & Logs")
    lines_out.append("")
    lines_out.append("<details>")
    lines_out.append("<summary>Expand: Watcher-Result excerpt + JSONL references</summary>")
    lines_out.append("")
    lines_out.append("### Watcher-Result (tail excerpt)")
    lines_out.append("")
    lines_out.append("```text")
    lines_out.extend(watcher_tail if watcher_tail else ["(no lines read)"])
    lines_out.append("```")
    lines_out.append("")
    if audit_tail:
        lines_out.append("### prompt-queue-audit (tail excerpt)")
        lines_out.append("")
        lines_out.append("```text")
        lines_out.extend(audit_tail)
        lines_out.append("```")
        lines_out.append("")
    lines_out.append("### JSONL sources (vault-relative)")
    lines_out.append("")
    for label, rel in jsonl_links:
        lines_out.append(f"- **{label}:** `[[{rel}]]`")
    lines_out.append("")
    lines_out.append("</details>")
    lines_out.append("")
    lines_out.append("## Raw Sources")
    lines_out.append("")
    for title, rel in raw_source_links:
        lines_out.append(f"- **{title}:** `[[{rel}]]`")
    lines_out.append("")
    lines_out.append(
        "---\n*Generated by `scripts/generate_telemetry_summary.py` — idempotent overwrite of canonical summary; archive optional.*"
    )
    lines_out.append("")
    return "\n".join(lines_out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Run-Telemetry-Summary.md")
    ap.add_argument("--vault-root", type=Path, default=Path.cwd())
    ap.add_argument(
        "--canonical-path",
        help="Vault-relative output path (default: Config or built-in default)",
    )
    ap.add_argument("--lane", default="legacy", help="queue lane or legacy")
    ap.add_argument(
        "--pipeline-mode",
        default="balance",
        help="effective_pipeline_mode for this run (balance|quality|speed)",
    )
    ap.add_argument(
        "--technical-bundle-root",
        type=str,
        default="",
        help="e.g. .technical/parallel/godot — dirname for decisions + audit JSONL",
    )
    ap.add_argument("--watcher-path", type=str, default="")
    ap.add_argument("--watcher-tail-lines", type=int, default=48)
    ap.add_argument("--decisions-max-rows", type=int, default=40)
    ap.add_argument("--audit-tail-lines", type=int, default=24)
    ap.add_argument(
        "--run-trigger",
        default="EAT-QUEUE (Layer 1 Part A)",
        help="Human-readable trigger description",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print MD to stdout only")
    ap.add_argument(
        "--no-archive",
        action="store_true",
        help="Skip timestamped archive copy even if archive_enabled in config",
    )
    args = ap.parse_args()

    vault = args.vault_root.resolve()
    tc = _parse_telemetry_summary_config(vault)
    canonical_rel = args.canonical_path or tc.get("canonical_path") or DEFAULT_CANONICAL
    archive_enabled = tc.get("archive_enabled", False) and not args.no_archive
    archive_dir = tc.get("archive_dir", "3-Resources/Second-Brain/Docs/Core/Run-Telemetry-Archive")

    watcher_path = args.watcher_path or str(
        tc.get("watcher_canonical_path", "3-Resources/Watcher-Result.md")
    )
    wp = vault / watcher_path
    watcher_tail = _tail_lines(wp, args.watcher_tail_lines)

    bundle = (args.technical_bundle_root or ".technical").strip() or ".technical"
    dec_path = vault / bundle / "eat-queue-decisions.jsonl"
    aud_path = vault / bundle / "prompt-queue-audit.jsonl"
    decisions_rows = _load_jsonl_rows(dec_path, args.decisions_max_rows)
    audit_tail = _tail_lines(aud_path, args.audit_tail_lines)

    iso_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dcount, succ, fail = _count_watcher_dispositions(watcher_tail)
    overview = {
        "watcher_counts": (dcount, succ, fail),
        "key_decisions": f"{len(decisions_rows)} transition row(s) in decisions log tail.",
        "outcomes": f"Watcher tail: {succ} success / {fail} failure line(s) (includes stall-skips as success).",
        "errors_summary": "See Watcher excerpt and Errors.md if Layer 1 logged failures.",
    }

    jsonl_links = [
        ("eat-queue-decisions", str(dec_path.relative_to(vault))),
        ("prompt-queue-audit", str(aud_path.relative_to(vault))),
        (
            "task-handoff-comms",
            str((vault / bundle / "task-handoff-comms.jsonl").relative_to(vault)),
        ),
    ]

    raw_source_links = [
        ("Watcher-Result (canonical)", watcher_path),
        ("Watcher-Result-sandbox (mirror)", "3-Resources/Watcher-Result-sandbox.md"),
        ("Watcher-Result-godot (mirror)", "3-Resources/Watcher-Result-godot.md"),
        ("PQ bundle root", bundle),
    ]

    body = build_markdown(
        iso_ts=iso_ts,
        lane=args.lane,
        pipeline_mode=args.pipeline_mode,
        run_trigger=args.run_trigger,
        overview_extra=overview,
        watcher_tail=watcher_tail,
        decisions_rows=decisions_rows,
        audit_tail=audit_tail,
        jsonl_links=jsonl_links,
        raw_source_links=raw_source_links,
    )

    if args.dry_run:
        print(body)
        return 0

    out_path = vault / canonical_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")

    if archive_enabled:
        ad = vault / archive_dir
        ad.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        arc = ad / f"Run-Telemetry-Summary--{stamp}.md"
        arc.write_text(body, encoding="utf-8")

    print(f"Wrote {canonical_rel}", file=sys.stderr)
    if archive_enabled:
        print(f"Archived to {archive_dir}/Run-Telemetry-Summary--*.md", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
