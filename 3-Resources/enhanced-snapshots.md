---
title: Enhanced Snapshots — Backup Integration
created: 2026-02-25
para-type: Resource
status: active
tags: [snapshots, backups, safety, cursor, obsidian, pipelines]
links: ["[[3-Resources/Second-Brain/Docs/Operations/Backup-and-Restore]]", "[[3-Resources/Backup-Log]]"]
---

# Enhanced Snapshots — Backup Integration

Short reference for **including in-vault snapshots in external backups** and where to get paths. Full backup/snapshot/restore doc: [[3-Resources/Second-Brain/Docs/Operations/Backup-and-Restore]].

## External backups should include snapshot dirs

**External backups** (e.g. rsync, restic, Obsidian Local Backup, or any vault-wide backup) **SHOULD** include `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` for full point-in-time recovery. Without them, you can restore the vault from `BACKUP_DIR` and live notes, but not the in-vault per-change and batch snapshot history used for rollbacks and restore flows.

- **Where the paths are defined**: `~/.cursor/mcp.json` → `mcpServers` → `obsidian-para-zettel-autopilot` → `env`:
  - `SNAPSHOT_DIR` — e.g. `<VAULT_PATH>/Backups/Per-Change`
  - `BATCH_SNAPSHOT_DIR` — e.g. `<VAULT_PATH>/Backups/Batch`
- Backup scripts or tools can read these same values from that config to include in vault backups (or use the vault root and ensure `Backups/Per-Change` and `Backups/Batch` are not excluded).

## Tool suggestions

- If you use **naive full backups** (e.g. plain rsync/cp), snapshot directories will grow over time; consider **incremental or deduplicating** tools (e.g. **restic**, **Borg**, **rclone** with versioning, or Obsidian plugins that do incremental backup) so that repeated snapshot runs do not bloat storage.
- Ensure backup schedules run after pipeline runs if you want the latest snapshots in each backup window.

## Rule reference

- `.cursor/rules/always/mcp-obsidian-integration.mdc` — documents snapshot roots and the "Integrate snapshots into external backups" subsection with the same guidance.
