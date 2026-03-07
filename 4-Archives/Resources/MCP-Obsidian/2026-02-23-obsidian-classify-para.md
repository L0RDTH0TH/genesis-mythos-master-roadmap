---
title: obsidian_classify_para (MCP tool)
created: 2026-02-23
tags: [ingest, raw-capture, mcp, obsidian-para-zettel-autopilot]
para-type: resource
status: reviewed
links: []
---
# Raw Capture — 2026-02-23

## What am I thinking?

**obsidian_classify_para** — Classify a note into PARA type (Project | Area | Resource | Archive | Ingest). Parameters: `path`, `para_type`. Used in ingest pipeline to decide target folder before move.

## What does this seem to mean?

Determines proposed_mv and frontmatter para-type; feeds into confidence and Ingest-Log.

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