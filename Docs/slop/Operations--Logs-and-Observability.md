# Logs and Observability

**Version: 2026-03**

Where to find pipeline logs, backup/snapshot events, errors, and dashboards. Full field definitions and formats are in the canonical [Logs](../../Logs.md) doc.

---

## Log locations (quick reference)

| Log | Path | Purpose |
|-----|------|---------|
| Ingest-Log | `3-Resources/Ingest-Log.md` | One line per note processed (Phase 1/2, backup/snapshot paths, loop_*). |
| Distill-Log | `3-Resources/Distill-Log.md` | Autonomous-distill; coverage_adapted, lens, heuristic. |
| Archive-Log | `3-Resources/Archive-Log.md` | Archive moves; backup and snapshot paths. |
| Express-Log | `3-Resources/Express-Log.md` | Autonomous-express; version-snapshot path when created. |
| Organize-Log | `3-Resources/Organize-Log.md` | Re-organize; backup and snapshot paths. |
| Backup-Log | `3-Resources/Backup-Log.md` | All backup/snapshot/restore events; per-change and batch paths. |
| Feedback-Log | `3-Resources/Feedback-Log.md` | Loop outcomes, re-try cap, queue analytics; create if missing. |
| Prompt-Log | `3-Resources/Prompt-Log.md` | Crafted params, validation, merge trace (craft/EAT-QUEUE). |
| Research-Log | `3-Resources/Research-Log.md` | Research runs: project_id, linked_phase, outcome, note_count. |
| Errors | `3-Resources/Errors.md` | Single place for pipeline errors; Error Handling Protocol. |
| Watcher-Result | `3-Resources/Watcher-Result.md` | One line per requestId (success/failure); wrapper creation lines. |
| Name-Review-Log | `3-Resources/Name-Review-Log.md` | NAME-REVIEW queue mode; suggested_name, applied, confidence. |
| Wrapper-Sync-Log | `3-Resources/Wrapper-Sync-Log.md` | Watcher plugin: wrapper path, action, reason. |

Machine-only / queue data: `.technical/prompt-queue.jsonl`; task list: `3-Resources/Task-Queue.md`.

---

## What to include in pipeline log lines

- **Timestamp**, **pipeline**, **note path**, **confidence**, **actions** (and proposed path when relevant).
- **Backup path** and **snapshot path** when a backup or per-change/batch snapshot was created.
- **Loop fields** when applicable: `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type`, `loop_reason`.
- **Flag**: `none` or `#review-needed` (+ reason). See [Logs](../../Logs.md) for full format and example line.

---

## Backup-Log

- **Location:** `3-Resources/Backup-Log.md`.
- **Contents:** Per-change and batch snapshot paths; `backup_path` from `create_backup`; restore events (type, note, from snapshot, result).
- **Use:** Find recent snapshots for a note; verify backup/snapshot creation; follow restore flow. See [Backup-and-Restore](Backup-and-Restore.md).

---

## Errors.md

- **Location:** `3-Resources/Errors.md`.
- **Contents:** One entry per failure. Heading: `### YYYY-MM-DD HH:MM — Short Title`. Metadata table: pipeline, severity, approval, timestamp, error_type. Sections: #### Trace, #### Summary (Root cause, Impact, Suggested fixes, Recovery).
- **Use:** Diagnose failures; recovery often points to restoring from `Backups/Per-Change/` or `BACKUP_DIR`. See [Errors-and-Recovery](Errors-and-Recovery.md).

---

## Restore-Queue

- **Location:** `3-Resources/Restore-Queue.md` (or a table in Errors.md).
- **Format:** One snapshot path per line, or columns `snapshot_path`, `original_path`. User-maintained list for batch restore; processor runs restore one-by-one. No auto-restore. See [Logs](../../Logs.md) § Restore-queue and [Backup-and-Restore](Backup-and-Restore.md).

---

## Unified dashboard (Vault-Change-Monitor)

- **Location:** `3-Resources/Vault-Change-Monitor.md` — MOC for last N entries, timelines, health.
- **Includes:** Links to all pipeline logs; optional Dataview blocks (Plan Evolution, Pending Re-Tries, context utilization for roadmap); Errors and Backup-Log for recovery.
- **Watcher-Result:** Last 1–3 success lines can be used as session_success_hint for re-queue payloads.

---

## Log rotation

- **Skill:** [log-rotate](../../../../.cursor/skills/log-rotate/SKILL.md). Trigger: monthly or **"Rotate logs"** (or equivalent).
- **Action:** Copy current Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, Feedback-Log to `3-Resources/Logs-Archive/<name>-YYYY-MM.md`; truncate or start fresh. Research-Log can be included when extended.
- Preserves history and keeps active log size manageable.

---

## Health check

- Optional: call **health_check** (e.g. every N notes in a batch or on first error). Log result to `3-Resources/MCP-Health-YYYY-MM.md` (monthly rotation) or Backup-Log. When status is non-OK, call **obsidian_ensure_backup** before continuing.

---

## See also

| Topic | Where |
|-------|--------|
| Full log table, example line, Error entry structure, research error format | [Logs](../../Logs.md) |
| Backup/snapshot/restore | [Backup-and-Restore](Backup-and-Restore.md) |
| Error Handling Protocol and recovery | [Errors-and-Recovery](Errors-and-Recovery.md) |
| Snapshot triggers by pipeline | [Safety-Invariants](../Safety-Invariants.md) § Snapshot triggers |
