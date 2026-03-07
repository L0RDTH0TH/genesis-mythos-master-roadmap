---
title: obsidian_ensure_backup (MCP tool)
created: 2026-02-23
tags: [ingest, raw-capture, mcp, obsidian-para-zettel-autopilot]
para-type: resource
status: reviewed
links: []
---
# Raw Capture — 2026-02-23

## What am I thinking?

**obsidian_ensure_backup** — Verify a recent backup exists for the file. Called automatically by destructive tools (move_note, delete_note, rename_note, update_note overwrite, search_replace). Use to check before a destructive op, or let the destructive tool call it internally. Parameters: `path` (required), optional `max_age_minutes` (default 15). Returns success, backup_path, age_minutes; on failure suggests running obsidian_create_backup first.

## What does this seem to mean?

Internal safety gate; usually no need to call explicitly unless auditing.

## TL;DR (add later or during review)

*Optional quick 1–2 sentence summary — fill this in when distilling/processing.*

## Images / Visuals

*Paste images directly here (drag-drop or Cmd/Ctrl+V), or add links.*

## Related Links / Sources

- [[Ingest/Ingest-Log]]
- obsidian-para-zettel-autopilot MCP server

## AI/Chat Appendices

*Paste full Grok, Cursor, Claude, etc. outputs here when you copy them in bulk.*

---
*No auto-filtering — manual review / Cursor Agent processing required. Keep in Ingest/ until confirmed move.*

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).