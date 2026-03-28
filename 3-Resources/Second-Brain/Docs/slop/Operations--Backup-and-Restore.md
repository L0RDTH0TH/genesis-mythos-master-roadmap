# Backup and Restore

**Version: 2026-03**

Single reference for backups, in-vault snapshots, retention, and restore in the Second Brain. Pipelines never run destructive actions without a backup/snapshot gate; restore is always user-triggered.

---

## Purpose

- **External backups** (`BACKUP_DIR`): last-resort, full-note copies before destructive ops; used by MCP `obsidian_create_backup` / `obsidian_ensure_backup`.
- **In-vault snapshots**: per-change and batch copies under `Backups/` for human-visible rollback and Dataview; created by the **obsidian-snapshot** skill before moves, renames, rewrites, cross-note appends.
- **Restore**: user-triggered only (RESTORE MODE or restore-queue); no auto-restore.

---

## Locations (where to look)

| What | Where | Notes |
|-----|--------|------|
| **External backups** | `BACKUP_DIR` | Set in `~/.cursor/mcp.json` (e.g. `Second-Brain-oops-Backups`). Full copies; include in external backup scripts. |
| **Per-change snapshots** | `Backups/Per-Change/` | Flattened names: `<slug>--<hash>--<timestamp>.md.bak`. One per destructive step when confidence ≥ 85%. |
| **Batch snapshots** | `Backups/Batch/` | Checkpoint summaries (e.g. every 5 ingest notes, every 3 distill, once per archive sweep). |
| **Archived snapshots** | `Backups/Archives/` | Older per-change snapshots moved here by **snapshot-sweep** (retention); not deleted by default. |
| **Backup log** | `3-Resources/Backup-Log.md` | All backup/snapshot/restore events; snapshot paths, pipeline, confidence, flags. |
| **Restore hub** | `3-Resources/Restore Hub.md` | User-facing list/Dataview of recent snapshots for a note (optional). |
| **Restore queue** | `3-Resources/Restore-Queue.md` | Optional list of snapshot paths to restore (one per line or table: `snapshot_path`, `original_path`). |

`SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` are set via MCP env (same paths as above). They live **inside the vault** and **outside** globbed rule scopes (e.g. not under `Ingest/`).

---

## When backups and snapshots happen

### External backup (before destructive work)

- **ensure_backup** (preferred): Call `obsidian_ensure_backup(path, max_age_minutes)` to confirm a recent backup exists. Use for long batches or after a gap (e.g. >15 min). Default `max_age_minutes: 1440` (24 h).
- **create_backup**: Call `obsidian_create_backup(path)` when ensure indicates missing or stale. Pipelines **must** have a successful backup before any destructive step for that note.
- **If backup creation fails:** Abort destructive steps for that note; log with `#review-needed`; continue with next note. See [Errors-and-Recovery](Errors-and-Recovery.md).

### Per-change snapshot (before each destructive step)

Required **before**: move, rename, split, structural distill, append_to_hub, task-reroute target append, roadmap-state/workflow_state update.

- **Confidence gate:** Only when confidence for that action is **≥ 85%**.
- **Skill:** [obsidian-snapshot](.cursor/skills/obsidian-snapshot/SKILL.md) (at vault root) with `type: "per-change"`.
- **If snapshot fails:** Skip the destructive action; log in `Backup-Log.md` with `#review-needed`; continue with next note.
- **Snapshot content:** Includes `original_path`, `snapshot_created`, `snapshot_hash`, `pipeline`, `confidence`; immutable, append-only.

### Batch snapshot

- When **batch size > `batch_size_for_snapshot`** (from [Second-Brain-Config](../../Second-Brain-Config.md), e.g. 5): one batch checkpoint under `Backups/Batch/` for the run.
- When **≤** threshold: per-change snapshots only (no batch file).
- Per-pipeline frequency: ingest ~every 5 notes; distill ~every 3; archive once per sweep; roadmap per phase/RECAL.

---

## Retention (snapshot sweep)

- **Trigger only:** User says e.g. **"SNAPSHOT SWEEP"**, **"Clean old snapshots"**, **"Apply snapshot retention"**. Not automatic.
- **Rule:** [snapshot-sweep](../../../../.cursor/rules/context/snapshot-sweep.mdc). Uses retention knobs (documented in skill/Logs):
  - `SNAPSHOT_MAX_DAYS` (e.g. 30) — keep per-change snapshots within last N days.
  - `SNAPSHOT_MAX_PER_NOTE` (e.g. 100) — keep last N snapshots per `original_path`.
- **Default action:** **Move** aged/excess snapshots to `Backups/Archives/`, do not delete. Log summary in `Backup-Log.md`. Deletion only if user explicitly requests and after confirming `BACKUP_DIR` is healthy; log with `#review-needed`.

---

## Restore (user-triggered only)

### RESTORE MODE (interactive)

1. Say e.g. **"RESTORE MODE – rollback last change to [[Note Title]]"** or **"restore from snapshot"**.
2. Rule [auto-restore](../../../../.cursor/rules/context/auto-restore.mdc) runs:
   - Resolve target note (from link or current note).
   - Read `Restore Hub.md` and `Backup-Log.md` for recent snapshots with matching `original_path`.
   - Present 3–5 candidates (path, timestamp, pipeline, confidence); ask which to restore or cancel.
   - For chosen snapshot: verify **snapshot_hash**; if mismatch, do not restore, log `#review-needed`, suggest `BACKUP_DIR`.
   - If OK: overwrite note at `original_path`, set `restored_from_snapshot`, `restored_at`; append to `Backup-Log.md`.
3. Snapshot files are **never** deleted by restore; they stay as history.

### Restore-queue (batch list)

- **List:** `3-Resources/Restore-Queue.md` (or table in Errors.md). Format: one path per line, or columns `snapshot_path`, `original_path`.
- **Processor:** Reads list and runs restore one-by-one: read snapshot → integrity check → write to `original_path` (or specified target). No auto-restore; user maintains the list. See [Logs](../../Logs.md) § Restore-queue and [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc) § Restore-queue mode.

---

## Integrate with external backups

- **External backup scripts** (rsync, restic, Obsidian Sync, etc.) **should** include `Backups/Per-Change/`, `Backups/Batch/`, and optionally `Backups/Archives/` for point-in-time recovery.
- Paths are in MCP env in `~/.cursor/mcp.json`. Use incremental/dedup tools to avoid bloat as snapshots accumulate.

---

## Security

- Snapshots are copies of note content. If the vault is synced or published, prefer encrypted storage or exclude `Backups/` and `BACKUP_DIR` from public repos. They are **not** an access-control boundary.

---

## See also

| Topic | Where |
|-------|--------|
| Safety (gates, no destructive without backup+snapshot) | [Safety-Invariants](../Safety-Invariants.md), [Core-Guardrails](../Rules/Core-Guardrails.md) |
| Snapshot triggers per pipeline | [Safety-Invariants](../Safety-Invariants.md) § Snapshot triggers (by pipeline) |
| MCP backup/snapshot config and fallbacks | [mcp-obsidian-integration](../../../../.cursor/rules/always/mcp-obsidian-integration.mdc) |
| obsidian-snapshot skill (naming, frontmatter, integrity) | [obsidian-snapshot SKILL](../../../../.cursor/skills/obsidian-snapshot/SKILL.md) |
| Log format and Backup-Log | [Logs](../../Logs.md), [Logs-and-Observability](Logs-and-Observability.md) |
| Errors and recovery | [Errors-and-Recovery](Errors-and-Recovery.md) |
| External backup integration (paths in MCP env, tool suggestions) | [3-Resources/enhanced-snapshots.md](../../../enhanced-snapshots.md) |
