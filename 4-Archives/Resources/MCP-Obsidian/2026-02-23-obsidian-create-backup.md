---
title: obsidian_create_backup (MCP tool)
created: 2026-02-23
tags: [ingest, raw-capture, mcp, obsidian-para-zettel-autopilot]
para-type: resource
status: reviewed
links: []
---
# Raw Capture — 2026-02-23

## What am I thinking?

**obsidian_create_backup** — Create timestamped backup copy of one or more vault files outside the vault. Required before any move/delete/overwrite. Aborts workflow on failure. Prerequisite for destructive operations (move_note, delete_note, rename_note, update_note overwrite, search_replace). Parameters: `paths` (array of vault-relative paths), optional `backup_dir_override`. Returns success + backup_path(s) and timestamp.

## What does this seem to mean?

Zero-manual safety: every ingest or destructive op must start here. Log returned backup_path(s) in Ingest-Log.md.

## TL;DR (add later or during review)

*Optional quick 1–2 sentence summary — fill this in when distilling/processing.*

## Images / Visuals

*Paste images directly here (drag-drop or Cmd/Ctrl+V), or add links.*

## Related Links / Sources

- [[Ingest/Ingest-Log]] — log backup_path
- obsidian-para-zettel-autopilot MCP server

## AI/Chat Appendices

*Paste full Grok, Cursor, Claude, etc. outputs here when you copy them in bulk.*

---
*No auto-filtering — manual review / Cursor Agent processing required. Keep in Ingest/ until confirmed move.*

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).