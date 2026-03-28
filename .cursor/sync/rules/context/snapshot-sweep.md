---
description: Trigger-based snapshot sweep rule for moving or pruning aged snapshots according to retention guidelines, without automatic deletion.
globs: "Backups/Per-Change/*.md.bak"
---

# Snapshot sweep (retention helper)

This rule defines how to **manually trigger** a sweep over per-change snapshots to manage storage growth, while preserving safety and review.

## When to run

Only when the user explicitly asks for cleanup, e.g.:

- **"SNAPSHOT SWEEP"**
- **"Clean old snapshots"**
- **"Apply snapshot retention"**

This rule is not cron-based and must not run automatically on note edits.

## Retention guidelines

- Use configuration values (conceptual; documented in skills/docs):
  - `SNAPSHOT_MAX_DAYS` — e.g. keep per-change snapshots from the last 30 days.
  - `SNAPSHOT_MAX_PER_NOTE` — e.g. keep the most recent 100 snapshots per `original_path`.
- The sweep should:
  - Identify snapshots under `Backups/Per-Change/` whose frontmatter `snapshot_created` is older than `SNAPSHOT_MAX_DAYS`, **or**
  - Notes where the count of snapshots for a given `original_path` exceeds `SNAPSHOT_MAX_PER_NOTE`.

## Actions

1. **Scan**
   - Use vault search / Dataview-like reasoning to find candidate snapshots based on `snapshot_created` and `original_path`.

2. **Move, don’t delete (default)**
   - For most cases, **move** aged or excess snapshots into `Backups/Archives/` (ensuring the folder exists via `obsidian_ensure_structure` or manual creation).
   - This preserves history while decluttering the primary `Backups/Per-Change/` view.

3. **Log**
   - For every sweep run, append a summary section to `3-Resources/Backup-Log.md` including:
     - Timestamp.
     - Number of snapshots scanned, moved, and left untouched.
     - Criteria used (e.g. `>30 days`, `>100 per note`).
     - Any manual deletion recommendations, marked with `#review-needed`.

4. **Deletion (optional, explicit)**

- Actual deletion of snapshot files should only occur when the user explicitly requests it in the prompt (e.g. “delete all snapshots older than 1 year”) and after:
  - Confirming that relevant external backups (`BACKUP_DIR`) are healthy, and
  - Logging the planned deletions in `Backup-Log.md` with `#review-needed`.

## Exclusions

- Do not run this rule on:
  - Current working notes outside `Backups/`.
  - `Backups/Batch/` or `Backups/Archives/` unless explicitly requested; those can have their own, separate retention logic if needed.

