---
name: log-rotate
description: Rotate pipeline logs (Ingest-Log, Archive-Log, etc.) to an archive path and truncate or start fresh. Trigger monthly or by "Rotate logs" command. Reduces log file size; preserves history in Logs-Archive.
---

# log-rotate

## When to use

- **Trigger**: Monthly, or when user runs "Rotate logs" (or equivalent command). Can be chained with snapshot-sweep or run standalone.
- **Reference**: [[3-Resources/Second-Brain/Logs|Logs]] and pipeline reference.

## Instructions

1. **Scope**: Target pipeline logs: Ingest-Log.md, Distill-Log.md, Archive-Log.md, Express-Log.md, Organize-Log.md, **Feedback-Log.md** (optional: Backup-Log.md). Location: `3-Resources/`. See Logs.md for rotation spec.

2. **Archive path**: Copy current content to `3-Resources/Logs-Archive/<LogName>-YYYY-MM.md` (e.g. `Ingest-Log-2026-02.md`). Use `obsidian_read_note` then write to the archive path (ensure `3-Resources/Logs-Archive/` exists via `obsidian_ensure_structure` or document that user creates it).

3. **Truncate or fresh**: After copy, either truncate the original log to a header only (e.g. "## Rotated YYYY-MM-DD; see Logs-Archive/Ingest-Log-YYYY-MM.md") or leave a minimal header and "Log continued below" so new entries append. Document choice in Logs.md.

4. **Log the rotation**: Append a line to Backup-Log or a dedicated Rotate-Log noting that rotation ran and which files were archived.

## MCP tools

- `obsidian_read_note`, `obsidian_update_note` (or create new file under Logs-Archive), `obsidian_ensure_structure` (for Logs-Archive folder).

## Optional

- **Retention**: Document in Logs.md how long to keep archived logs (e.g. 12 months) and whether a separate sweep deletes old archives.
