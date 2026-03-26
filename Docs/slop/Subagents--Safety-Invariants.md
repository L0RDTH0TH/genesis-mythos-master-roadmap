# Safety Invariants

**Version: 2026-03 – post-subagent migration**

Exhaustive list of safety invariants all subagents and the Queue must obey: backups, snapshots, confidence bands, watcher contract, errors.

---

## Purpose

Consolidated reference so every subagent and the Queue rule honor the same backup, snapshot, confidence, and error rules without duplicating logic.

---

## Backups

- **Before any destructive operation** (move, rename, delete, large overwrite), ensure a recent backup: `obsidian_ensure_backup` (preferred) or `obsidian_create_backup` (when ensure indicates missing or stale).
- **If backup fails:** Abort destructive steps for that note; log with `#review-needed`; continue with next note in batch.
- **Reference:** core-guardrails.mdc, mcp-obsidian-integration.mdc.

---

## Per-change snapshots

- **Before:** move, rename, split, structural distill, append_to_hub — call obsidian-snapshot (or equivalent) with **type per-change** when **confidence ≥ 85%**.
- **If snapshot fails:** Skip the destructive action; log `#review-needed`.
- **Location:** `Backups/Per-Change/`; append-only; never edit or delete from pipelines.
- **Reference:** core-guardrails, mcp-obsidian-integration.

---

## Confidence bands

| Band | Range | Behavior |
|------|-------|----------|
| **High** | ≥ 85% | Destructive actions allowed **only after** per-change snapshot; dry_run then commit for moves. |
| **Mid** | 68–84% | At most **one** non-destructive refinement loop per note per run; proceed only if post_loop_conf ≥ 85%; else create Decision Wrapper (e.g. Ingest/Decisions/Refinements/). |
| **Low** | < 68% | No destructive action; create Decision Wrapper (e.g. Ingest/Decisions/Low-Confidence/); propose only. |

- **Decay rule:** If post_loop_conf ≤ pre_loop_conf, fall back to user decision: no destructive action for that note in this run; log #review-needed where appropriate.
- **Reference:** Parameters.md, confidence-loops.mdc.

---

## Critical invariant

**No destructive action** unless **both** (1) confidence in high band (≥ 85%) for that pipeline, and (2) a **per-change snapshot** for that note succeeded in the current run.

---

## No shell vault ops

- Never use shell `cp`, `mv`, or `rm` to mutate Obsidian vault contents.
- All moves/renames/deletes go through MCP tools with backup and snapshot gates.
- **Exception:** Documented, **user-invoked** attachment-move skill (e.g. Ingest → 5-Attachments/) only; backup and logging still apply.

---

## Structure before move

- Before any `obsidian_move_note`: call **obsidian_ensure_structure**(folder_path: parent of target); then **obsidian_move_note** with `dry_run: true`, review effects, then `dry_run: false` to commit.
- **Post-move:** Set para-type (and project-id when under 1-Projects/; status: archived when under 4-Archives/) on the note at the new path per mcp-obsidian-integration.

---

## Exclusions and protected paths

**Do not move, rename, or delete:** `Backups/**`, `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`, `Ingest/watched-file.md`, notes with `watcher-protected: true`, MCP backup dirs in `~/.cursor/mcp.json`.

**Do not process as primary input:** Notes under `Ingest/Decisions/**` (Decision Wrappers are consumed by Step 0 and path-apply, not as ingest/distill/archive targets).

- **Reference:** core-guardrails, Vault-Layout.md.

---

## Error Handling Protocol

On **any** pipeline or workflow step failure:

1. **Trace:** Timestamp (ISO 8601), pipeline name, stage/step name, affected path(s), sanitized error message (no secrets).
2. **Summary:** Error type; root cause; impact; suggested fixes; recovery (e.g. restore from Backups/Per-Change/).
3. **Log:** Append one entry to **`3-Resources/Errors.md`** (heading `### YYYY-MM-DD HH:MM — Short Title`; inline table with pipeline, severity, approval, timestamp, error_type; #### Trace; #### Summary with Root cause, Impact, Suggested fixes, Recovery).
4. **Pipeline log:** One-line reference in the relevant pipeline log (Ingest-Log, Distill-Log, etc.).
5. **Error Decision Wrapper:** When appropriate, create under **`Ingest/Decisions/Errors/`** (wrapper_type: error; options A–G recovery-focused); ensure CHECK_WRAPPERS exists; append Watcher-Result line for wrapper creation.
6. **Severity high:** Set approval pending, add #review-needed; skip destructive steps for that note; continue with next.
7. **Progressive fallbacks:** Before writing an error entry, attempt fallbacks (e.g. obsidian_ensure_structure then retry move); only after exhausting fallbacks, log to Errors.md.

- **Reference:** mcp-obsidian-integration § Error Handling Protocol.

---

## Watcher-Result contract

- On run finish (queue-based or direct), append **one line per requestId** to **`3-Resources/Watcher-Result.md`**:

  ```
  requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>
  ```

- Create file if missing; append only; do not overwrite existing content.
- **Reference:** watcher-result-append.mdc.

---

## Roadmap state

- **Before mutating:** Read `roadmap-state.md` and `workflow_state.md` under `1-Projects/<project_id>/Roadmap/`.
- **Snapshot:** Snapshot state **before and after** every update.
- **Parse failure:** If roadmap-state or workflow_state parse fails → abort roadmap pipeline; log to Errors.md with #state-corrupt; create Decision Wrapper under Ingest/Decisions/Errors/ as appropriate.
- **Reference:** mcp-obsidian-integration, Roadmap subagent.

---

## Restore

- **Restore** from snapshots is **user-triggered only**. No auto-restore.
- **Reference:** mcp-obsidian-integration (restore-queue mode).

---

<!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md -->
## Log format and backup path

Every pipeline that performs move/overwrite/delete must log with **backup path included**. Include the backup path in the **`changes`** string of `obsidian_log_action` or in the pipeline log line (e.g. `Backup: /path/to/backup/note.md`). **Log line format** (align with pipeline logs): timestamp, Excerpt, PARA type, Changes (list; include Backup when processing), Confidence, Proposed path or stay, Flag (none or #review-needed), Loop fields (loop_attempted, loop_type, pre/post_loop_conf, outcome, reason). See Cursor-Skill-Pipelines-Reference § Log format, backup path, and loops.
