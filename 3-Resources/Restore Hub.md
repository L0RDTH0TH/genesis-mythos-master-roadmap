---
title: Restore Hub
created: 2026-02-25
para-type: Resource
status: active
tags: [restore, snapshots, backups, safety, cursor, obsidian]
---

# Restore Hub

Central place to **inspect snapshots**, understand storage health, and drive **safe restores**.

- External backups: `BACKUP_DIR` (managed by `obsidian_create_backup` via MCP).
- In-vault snapshots: `Backups/Per-Change/`, `Backups/Batch/`, and `Backups/Archives/` (flattened filenames with frontmatter).
- Restore is **always user-triggered** via RESTORE MODE; nothing auto-rolls back without your explicit request.

## How snapshots work (layers)

- **Layer 1 – External backups**: Whole-note backups created in `BACKUP_DIR` before pipelines run. Store this folder on encrypted or otherwise protected storage when syncing/sharing.
- **Layer 2 – Per-change snapshots**: Hash-verified snapshots created before destructive actions, stored in `Backups/Per-Change/`. Each snapshot carries:
  - `original_path`, `original_title`, `pipeline`, `snapshot_type`, `snapshot_created`, `snapshot_hash`, `confidence`, `immutable: true`, `para-type: Archive`, `status: frozen`, and optional `flag`.
- **Layer 3 – Batch checkpoints**: Summary notes in `Backups/Batch/` listing multiple per-change snapshots for a run (e.g. every 5 ingest notes).

## Recent snapshots (Dataview idea)

Use a Dataview query (or similar) to list recent per-change snapshots, e.g.:

- Filter by `original_path` (current note).
- Sort by `snapshot_created` descending.
- Show `pipeline`, `confidence`, and `flag`.

This section is intentionally prose-only; implement the exact Dataview block to match your plugin configuration.

## Storage health

To monitor growth in `Backups/`:

- Count snapshots in:
  - `Backups/Per-Change/`
  - `Backups/Batch/`
  - `Backups/Archives/`
- Heuristic thresholds:
  - If `Backups/Per-Change/` exceeds ~500 files or your comfort level, consider running **SNAPSHOT SWEEP**:
    - Prompt: `SNAPSHOT SWEEP – apply retention`
    - See `.cursor/rules/context/snapshot-sweep.mdc` for behavior (move to Archives, log, avoid silent deletion).

## Recent failures

This section surfaces issues discovered during snapshot or restore attempts.

- Look for entries in `3-Resources/Backup-Log.md` with:
  - `flag: #review-needed`
  - Reasons like `SNAPSHOT_DIR unreachable`, `snapshot_hash mismatch`, or `restore aborted`.
- Before heavy changes or bulk restores, scan recent failures to ensure the safety net is healthy.

## Restore checklist

1. Open this hub and skim **Recent snapshots** and **Recent failures**.
2. Decide which note you want to roll back.
3. Use a Cursor prompt like:
   - `RESTORE MODE – rollback last change to [[Note Title]]`
4. In the restore flow:
   - Pick a snapshot from the presented list (usually the latest).
   - Let the system verify `snapshot_hash` integrity.
   - Confirm overwrite of the original note.
5. After restore:
   - The note frontmatter will record:
     - `restored_from_snapshot: <snapshot_path>`
     - `restored_at: <timestamp>`
   - Optionally add your own note on why the restore was needed.

## PARA / Zettelkasten alignment

- This hub is a **Resource** note in PARA, documenting how your Second Brain safeguards itself.
- Each snapshot is an **atomic state** of a note, aligning with Zettelkasten’s emphasis on small, self-contained units:
  - Use snapshot metadata (especially `original_path` and `snapshot_created`) to understand how ideas and projects evolved over time.

