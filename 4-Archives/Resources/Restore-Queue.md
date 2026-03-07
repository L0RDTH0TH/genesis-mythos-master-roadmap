---
title: Restore Queue
created: 2026-03-01
tags: [second-brain, restore, snapshots]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Logs]]"]
---

# Restore Queue

User-maintained list of snapshot paths to restore. **Restore is always user-triggered**; no auto-restore. See [[3-Resources/Second-Brain/Logs#Restore-queue|Logs § Restore-queue]] and [[.cursor/rules/always/mcp-obsidian-integration#Restore-queue mode|mcp-obsidian-integration]].

## Format

- **One path per line**, or
- **Table** with columns: `snapshot_path`, `original_path` (optional).

Processor reads this list and runs restore steps one-by-one: read snapshot content → write to original path (or specified target).

## Example (table)

| snapshot_path | original_path |
|---------------|---------------|
| Backups/Per-Change/Note--abc123--20260301-120000.md.bak | 1-Projects/MyProject/Note.md |

## Example (one per line)

```
Backups/Per-Change/Note--abc123--20260301-120000.md.bak
```

Add lines or rows as needed; remove or mark done after restore.
