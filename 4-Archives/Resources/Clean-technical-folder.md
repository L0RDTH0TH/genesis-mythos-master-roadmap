---
title: Clean technical folder
created: 2026-03-01
tags: [pkm, second-brain, technical, cleanup]
para-type: Resource
status: active
---

# Clean technical folder

Manual steps for maintaining the `.technical/` (machine-only) bin.

1. **Obsidian**: Ensure `.technical` is in **Settings → Files & Links → Excluded files** so the folder stays hidden from explorer/search/graph.
2. **Stalled queue**: If `.technical/prompt-queue.jsonl` has old or stuck entries, open it in Cursor and either delete failed lines or copy `.technical/prompt-queue.sample.jsonl` to reset (back up first if needed).
3. **Old logs**: Clear or rotate `.technical/*.log`, `mcp-setup-log.md`, or other one-off logs when they grow large; keep pipeline logs (Ingest-Log, etc.) in `3-Resources/`.
4. **When to nuke vs rotate**: Nuke (empty the queue file) when you want a fresh start; rotate (e.g. archive `prompt-queue.done.*.jsonl` elsewhere) if you need to keep history. Watcher plugin may write `prompt-queue.done.<timestamp>.jsonl` into `.technical/` on clear — move or delete those as needed.

Do NOT place human-authored notes in `.technical/` — use PARA or 3-Resources.
