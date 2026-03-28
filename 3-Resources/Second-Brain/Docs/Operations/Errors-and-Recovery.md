# Errors and Recovery

**Version: 2026-03**

Where errors are logged, how they are structured, and how to recover (restore from snapshot, Restore-Queue, fallbacks). Full protocol lives in the always rule [mcp-obsidian-integration](../../../../.cursor/rules/always/mcp-obsidian-integration.mdc).

---

## Where errors are logged

- **Single place:** `3-Resources/Errors.md`. Create if missing. Every pipeline failure should append one entry here and a one-line reference in the relevant pipeline log (Ingest-Log, Archive-Log, etc.).
- **Error Decision Wrappers:** Under `Ingest/Decisions/Errors/` with recovery-focused options (A–G). Created when appropriate; link to the Errors.md entry in the wrapper body.

---

## Error entry structure

- **Heading:** `### YYYY-MM-DD HH:MM — Short Title`
- **Metadata table:** pipeline, severity, approval, timestamp, error_type
- **#### Trace:** Sanitized trace (no API keys)
- **#### Summary:** Root cause, Impact, Suggested fixes, Recovery

**Recovery** should state, when applicable: "Rollback: restore from Backups/Per-Change/<snapshot>" or "Retry with dry_run only" or "No snapshot; backup at BACKUP_DIR may be used if available."

---

## Error Handling Protocol (summary)

On **any** pipeline or workflow step failure:

1. **Trace:** Timestamp (ISO 8601), pipeline name, stage/step, affected note path(s), sanitized error message.
2. **Summarize:** Error type (e.g. io-failure, mcp-api, confidence-below-threshold, state-inconsistent); root cause; impact; suggested fixes; recovery.
3. **Log:** One entry to `3-Resources/Errors.md`; one-line reference in the pipeline log.
4. **Error wrapper (when appropriate):** Create under `Ingest/Decisions/Errors/` with wrapper_type: error; link to Errors.md entry; options A–G for recovery (e.g. force backup then retry, use alternative path, pause note, manual move). Append Watcher-Result line for wrapper creation.
5. **Severity high:** Set approval pending, add #review-needed; skip destructive steps for that note; continue with next note.
6. **Fallbacks first:** Before writing an error entry, attempt fallbacks (e.g. obsidian_ensure_structure then retry move; propose_alternative_paths → calibrate → dry_run again). Only after exhausting fallbacks, log to Errors.md.

---

## Recovery options

| Situation | Action |
|-----------|--------|
| Destructive step failed but per-change snapshot exists | Restore from that snapshot. See [Backup-and-Restore](Backup-and-Restore.md) § RESTORE MODE. Document snapshot path in the error entry under Recovery. |
| No snapshot (e.g. failure before snapshot) | State in Recovery: "No snapshot; backup at BACKUP_DIR may be used if available." |
| Move failed (parent missing, dry_run risks) | ensure_structure for target parent → retry move; or propose_alternative_paths → calibrate_confidence → verify_classification → dry_run again. Log only after fallbacks exhausted. |
| Backup creation failed | Abort destructive steps for that note; do not proceed. Log with #review-needed. |
| Snapshot creation failed before destructive step | Skip the destructive action; log in Backup-Log.md with #review-needed; continue with next note. |

---

## Research and roadmap error types

- **Research:** Entries use heading pattern `### YYYY-MM-DD HH:MM — research-empty | research-failed | research-skipped`; metadata includes pipeline, linked_phase, project_id, error_type. Tags: #research-failed, #research-empty, #research-skipped.
- **Roadmap state:** Parse failure (invalid YAML, missing current_phase/status) → error_type #state-corrupt; abort roadmap pipeline; Decision Wrapper under Ingest/Decisions/Errors/ for "Fix state or revert?".

---

## See also

| Topic | Where |
|-------|--------|
| Full Error Handling Protocol, fallback table, severity | [mcp-obsidian-integration](../../../../.cursor/rules/always/mcp-obsidian-integration.mdc) |
| Backup and restore flow | [Backup-and-Restore](Backup-and-Restore.md) |
| Safety (confidence bands, snapshot gates) | [Safety-Invariants](../Safety-Invariants.md) |
| Log locations and Backup-Log | [Logs-and-Observability](Logs-and-Observability.md), [Logs](../../Logs.md) |
