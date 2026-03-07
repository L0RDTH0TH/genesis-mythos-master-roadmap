---
name: log-rotate
description: Rotate pipeline logs (Ingest-Log, Archive-Log, etc.) to an archive path and truncate or start fresh. Trigger monthly or by "Rotate logs" command. Reduces log file size; preserves history in Logs-Archive.
---

# log-rotate

- **Trigger**: Monthly or "Rotate logs" command. **Scope**: Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log (optional Backup-Log) in `3-Resources/`.
- **Instructions**: (1) Copy current content to `3-Resources/Logs-Archive/<LogName>-YYYY-MM.md`. (2) Ensure Logs-Archive exists (obsidian_ensure_structure). (3) Truncate or minimal header on original. (4) Append line to Backup-Log that rotation ran.
- **MCP**: obsidian_read_note, obsidian_update_note, obsidian_ensure_structure. **Reference**: Logs.md, pipeline reference.
