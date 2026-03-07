---
name: ""
overview: ""
todos: []
isProject: false
---

# Preliminary Plan: Enhanced Error Handling in Pipelines and Workflows

**Persona:** Obsidian PARA-Zettel-Autopilot Agent  
**Objective:** Update all relevant rule files to incorporate robust error handling (trace, summarize, log, notify, integrate with snapshots) without altering core pipeline logic.  
**Mode:** Plan approved; implementation completed 2026-02-26.

---

## 1. Audit Summary

### 1.1 Rules and pipelines in scope


| File                                                | Role                                                     | Error-relevant entry points                                                     |
| --------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `.cursor/rules/always/mcp-obsidian-integration.mdc` | Always-applied; MCP fallbacks, backup gate, health check | MCP call failures, backup failure, snapshot failure, move dry_run risks         |
| `.cursor/rules/context/para-zettel-autopilot.mdc`   | Master ingest rule for Ingest/*.md                       | Backup fail, classify/split/distill/hub/move failures, low confidence           |
| `.cursor/rules/context/ingest-processing.mdc`       | Ingest folder + non-MD + embedded normalization          | List/read/write failures, companion creation, image normalization               |
| `.cursor/rules/context/auto-distill.mdc`            | autonomous-distill                                       | Backup/snapshot/skill failures (distill layers, highlight, layer-promote, etc.) |
| `.cursor/rules/context/auto-archive.mdc`            | autonomous-archive                                       | Backup/snapshot/archive-check/subfolder-organize/move failures                  |
| `.cursor/rules/context/auto-express.mdc`            | autonomous-express                                       | Backup/version-snapshot/snapshot/append failures                                |
| `.cursor/rules/context/auto-organize.mdc`           | autonomous-organize                                      | Backup/snapshot/classify/subfolder-organize/rename/move failures                |
| `.cursor/rules/context/non-markdown-handling.mdc`   | Non-MD in Ingest                                         | Companion write, embed/link errors                                              |
| `3-Resources/Cursor-Skill-Pipelines-Reference.md`   | Canonical pipeline order and snapshot triggers           | Reference only; add error-handling subsection                                   |


### 1.2 Current state

- **Logging:** Pipeline-specific logs exist: `Ingest-Log.md`, `Distill-Log.md`, `Archive-Log.md`, `Express-Log.md`, `Organize-Log.md`, `Backup-Log.md` (all under `3-Resources/`). Failures are logged with `#review-needed` and short reason; no dedicated **error** log.
- **No `Errors.md`:** There is no `Vault/Logs/` folder; all logs live in `3-Resources/`. Plan uses `**3-Resources/Errors.md`** for the dedicated error log (Dataview-queryable).
- **Snapshots:** Per-change and batch snapshots are already required before destructive steps; rollback is user-triggered via restore rules. Error handling will **reference** existing snapshot paths in error entries and recommend rollback when severity is high.
- **Inbox Review:** No dedicated "Inbox Review" hub found in vault. Plan will "flag for user review" and optionally link from Errors.md so a future hub or Dataview can aggregate; no new plugin.

---

## 2. Error Handling Protocol (single source of truth)

Add a new **§ Error Handling Protocol** to `**mcp-obsidian-integration.mdc`** (always-applied) so every pipeline and the agent have one place to look. No code—only procedural instructions the agent follows when any step fails.

### 2.1 Proposed section text (to insert in mcp-obsidian-integration.mdc)

```markdown
## Error Handling Protocol (all pipelines)

When **any** pipeline or workflow step fails (MCP call error, classification failure, I/O or plugin error, heuristic/scoring exception, or unexpected state):

1. **Trace**
   - Capture: timestamp (ISO 8601), pipeline name, pipeline stage/step name, affected note path(s), raw error message or stack trace (sanitize: no API keys or secrets).
   - Optional context: Obsidian/MCP server status if available (e.g. from `health_check`), plugin state only if relevant (e.g. "Highlightr unavailable").

2. **Summarize**
   - Produce a short **summary** (2–4 sentences) with:
     - **Error type/category**: Quick classifier for filtering/grouping — one of: `io-failure`, `mcp-api`, `classification-empty`, `plugin-unavailable`, `confidence-below-threshold`, `state-inconsistent` (or similar; extend as needed).
     - **Root cause** (if detectable): e.g. "Parent directory missing", "Classification returned empty", "Backup write failed".
     - **Impact**: Which note(s) were partially processed; which steps were skipped.
     - **Suggested fixes**: From heuristics (e.g. "Run obsidian_ensure_structure for target parent"; "Retry after ensure_backup"; "Manual move required").
     - **Recovery**: e.g. "Rollback: restore from Backups/Per-Change/<snapshot>"; "Retry with dry_run only"; "No destructive action was taken."

3. **Log and notify**
   - Append a **single error entry** to **`3-Resources/Errors.md`** (create the note if it does not exist). Each entry uses **note-level frontmatter only**; per-entry metadata is in the body. Entry format:
     - Heading: `### YYYY-MM-DD HH:MM — Short Title`
     - Immediately below: a small **inline table** (or key-value lines) for metadata: `pipeline`, `severity`, `approval`, `timestamp`, and `error_type` (the category from Summarize).
     - Then **#### Trace** (bullet list or code block).
     - Then **#### Summary** with bold subheadings: **Root cause**, **Impact**, **Suggested fixes**, **Recovery**. No fenced YAML per entry (Dataview-friendly table parsing on note content; human-readable).
   - Also append a **one-line reference** to the same error in the **pipeline-specific log** (Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, or Backup-Log as appropriate), e.g. `Error logged: 3-Resources/Errors.md#entry-YYYY-MM-DD-HHMM`.
   - If **severity is high** or **confidence is low** and the error is **critical** (e.g. backup failed, snapshot failed before destructive step):
     - Set `approval: pending` and add tag `#review-needed` in Errors.md.
     - **Pause the pipeline for the current note**: skip all remaining destructive steps for that note, continue with the next note in the batch (do not halt the entire batch unless it is a global failure such as `obsidian_create_backup` at run start).

4. **Integrate with existing safeguards**
   - **Rollback**: Do **not** auto-restore. If a per-change snapshot was created **before** the failing step, document its path in the error entry under "Recovery" so the user can run RESTORE MODE. If no snapshot exists (e.g. failure before snapshot), state "No snapshot; backup at BACKUP_DIR may be used if available."
   - **Progressive fallbacks**: Before writing an error entry, the agent MUST have attempted the fallbacks already defined in this rule (e.g. `obsidian_ensure_structure` then retry move; `propose_alternative_paths` → calibrate → verify → dry_run again). Only after fallbacks are exhausted, log to Errors.md.
   - **Threshold**: Treat as **high severity** when: backup creation failed; snapshot creation failed immediately before a destructive step; move/rename/delete failed after dry_run was approved; or any error that could leave a note in an inconsistent state. Treat as **medium** when a non-destructive step failed (e.g. classify returned low confidence). Treat as **low** when the failure is cosmetic or recoverable without user action (e.g. optional step skipped).

This protocol does not replace pipeline-specific "On failure" bullets; it standardizes **what** to write to Errors.md and **when** to escalate. Each pipeline rule will reference this section and add pipeline-specific stage names.
```

### 2.2 Diff: mcp-obsidian-integration.mdc

- **Location:** After the "Health check and observability" subsection (before the final test path line).
- **Change:** Insert the full "## Error Handling Protocol (all pipelines)" section as above.
- **Backup:** Copy to `mcp-obsidian-integration.mdc.bak` before editing.

---

## 3. Per-file changes (diffs)

### 3.1 para-zettel-autopilot.mdc

- **Section to add:** "## Error handling (ingest)" after "## Batch and isolation".
- **Content:**
  - On any error during ingest (backup, classify_para, frontmatter-enrich, subfolder-organize, split_atomic, distill_note, append_to_hub, move_note, log_action, or embedded normalization):
    - Follow the **Error Handling Protocol** in `mcp-obsidian-integration.mdc` (§ Error Handling Protocol).
    - Capture pipeline stage (e.g. `classify_para`, `obsidian_move_note`), affected note path(s), and sanitized error.
    - Append trace + summary to `3-Resources/Errors.md`; append one-line reference to `Ingest-Log.md`.
    - If severity is high or critical (e.g. backup failed): pause this note, skip destructive steps, continue to next note; do not abort entire batch for single-note failure.
- **Backup:** `para-zettel-autopilot.mdc.bak`.

### 3.2 ingest-processing.mdc

- **Section to add:** "## Error handling" after "MCP SAFETY".
- **Content:**
  - If listing Ingest, non-MD handling, embedded image normalization, or full-autonomous-ingest fails for a file or note:
    - Follow the Error Handling Protocol in `mcp-obsidian-integration.mdc`.
    - Pipeline name: `ingest-processing` or `full-autonomous-ingest` as appropriate; stage: e.g. `non-md companion`, `embedded image normalization`, `ingest pipeline`.
    - Log to `3-Resources/Errors.md` and reference in `Ingest-Log.md`.
    - On backup or MCP failure for one item: skip that item, log, continue with the rest.
- **Backup:** `ingest-processing.mdc.bak`.

### 3.3 auto-distill.mdc

- **Section to add:** "## Error handling" after "Batch and isolation" (before "Snapshots and checkpoints").
- **Content:**
  - On failure of backup, snapshot, auto-layer-select, distill layers, distill-highlight-color, layer-promote, callout-tldr-wrap, or readability-flag:
    - Follow the Error Handling Protocol; pipeline: `autonomous-distill`; stage: e.g. `distill-highlight-color`, `layer-promote`.
    - Append to `3-Resources/Errors.md` and a one-line reference in `Distill-Log.md` (and Backup-Log.md when snapshots involved).
    - If severity high: skip remaining destructive steps for that note, continue to next.
- **Backup:** `auto-distill.mdc.bak`.

### 3.4 auto-archive.mdc

- **Section to add:** "## Error handling" after "Batch and isolation".
- **Content:**
  - On failure of backup, snapshot, archive-check, subfolder-organize, resurface-candidate-mark, summary-preserve, or move_note:
    - Follow the Error Handling Protocol; pipeline: `autonomous-archive`; stage as appropriate.
    - Log to `3-Resources/Errors.md` and reference in `Archive-Log.md` and `Backup-Log.md`.
    - If backup or snapshot fails: abort pipeline for that note, log, continue to next.
- **Backup:** `auto-archive.mdc.bak`.

### 3.5 auto-express.mdc

- **Section to add:** "## Error handling" after "Batch and isolation".
- **Content:**
  - On failure of backup, version-snapshot, per-change snapshot, related-content-pull, express-mini-outline, or call-to-action-append:
    - Follow the Error Handling Protocol; pipeline: `autonomous-express`.
    - Log to `3-Resources/Errors.md` and reference in `Express-Log.md` and `Backup-Log.md`.
    - If backup or version-snapshot fails: abort expressive appends for that note, continue to next.
- **Backup:** `auto-express.mdc.bak`.

### 3.6 auto-organize.mdc

- **Section to add:** "## Error handling" after "Batch and isolation".
- **Content:**
  - On failure of backup, snapshot, classify_para, frontmatter-enrich, subfolder-organize, rename_note, or move_note:
    - Follow the Error Handling Protocol; pipeline: `autonomous-organize`.
    - Log to `3-Resources/Errors.md` and reference in `Organize-Log.md` and `Backup-Log.md`.
    - If backup fails: abort organize for that note; skip rename/move on snapshot or move failure, continue to next.
- **Backup:** `auto-organize.mdc.bak`.

### 3.7 non-markdown-handling.mdc

- **Section to add:** "## Error handling" at end of file.
- **Content:**
  - If companion note creation or embed/link write fails:
    - Follow the Error Handling Protocol; pipeline: `non-markdown-handling`; stage: `companion creation` or `embed write`.
    - Log to `3-Resources/Errors.md`; reference in `Ingest-Log.md` if invoked from ingest flow.
    - Do not move or delete the original file; leave in Ingest/ with #needs-manual-move.
- **Backup:** `non-markdown-handling.mdc.bak`.

### 3.8 Cursor-Skill-Pipelines-Reference.md

- **Section to add:** "## Error handling (all pipelines)" after "Snapshot triggers (all pipelines)" and before "Dataview & dashboards".
- **Content:**
  - Short subsection stating:
    - On any pipeline or workflow error, the agent follows the **Error Handling Protocol** in `.cursor/rules/always/mcp-obsidian-integration.mdc`.
    - Trace and summary are appended to `**3-Resources/Errors.md`** (create if missing). Frontmatter per entry: `approval`, `timestamp`, `pipeline`, `severity`. Body: Trace (sanitized) and Summary (root cause, impact, suggested fixes, recovery).
    - Pipeline-specific logs get a one-line reference to the error entry. High severity or critical errors are tagged `#review-needed` and the current note is paused (no destructive steps); batch continues with next note unless it is a global failure (e.g. backup at run start).
    - Rollback remains user-triggered (RESTORE MODE); error entries document snapshot path when available for recovery.
- **Backup:** `Cursor-Skill-Pipelines-Reference.md.bak` (optional; under 3-Resources).

---

## 4. New note: 3-Resources/Errors.md

- **Create** with the following structure (no .bak needed for new file).

**Frontmatter (note-level):**

```yaml
---
title: Pipeline and Workflow Errors
created: YYYY-MM-DD
para-type: Resource
status: active
tags: [errors, pipelines, cursor, obsidian, review]
---
```

**Body:**

```markdown
# Pipeline and Workflow Errors

Central log for **traced errors** from ingest, distill, archive, express, organize, and supporting workflows. Each error entry includes a trace (sanitized), summary (root cause, impact, suggested fixes, recovery), and links to pipeline-specific logs.

- **Dataview:** Query by table columns `pipeline`, `severity`, `approval`, `timestamp`, `error_type` (or `#review-needed` in text) to surface pending review or high-severity items.
- **Recovery:** Use RESTORE MODE to rollback from a per-change snapshot when documented in the entry.

## Error entry format

Each new error is appended as follows (no fenced YAML per entry):

### YYYY-MM-DD HH:MM — Short Title

| Field | Value |
|-------|-------|
| pipeline | autonomous-distill |
| severity | high |
| approval | pending |
| timestamp | 2026-02-26T19:30:00Z |
| error_type | mcp-api |

#### Trace

- Timestamp, pipeline, stage, affected note path(s).
- Raw error message or stack (sanitized).

#### Summary

- **Root cause:** …
- **Impact:** …
- **Suggested fixes:** …
- **Recovery:** …

(Entries follow below, appended by the agent.)
```

---

## 5. Safety and testing

- **Backups:** Before editing any rule file, create a `.bak` copy in the same directory (e.g. `para-zettel-autopilot.mdc.bak`). No changes to YAML frontmatter schemas of existing notes except the new Errors.md.
- **Core logic:** No change to pipeline order, confidence gates, or snapshot trigger table; only additive "Error handling" sections and one new protocol section.
- **Test (after approval):** In a sandbox vault copy: simulate an error (e.g. invalid path, or a failing MCP response if possible) and verify (1) trace and summary are written to Errors.md, (2) pipeline log has a one-line reference, (3) no destructive action on the affected note when severity is high, (4) batch continues for next note.

---

## 6. Sync and commit (after application)

- Commit message: `enhance(rules): add error tracing and summarization to pipelines for improved reliability`
- Ensure local and synced copies of rules are updated (e.g. `.cursor/sync/rules/` if used).

---

## 7. Summary of changes


| Item                                  | Action                                                                               |
| ------------------------------------- | ------------------------------------------------------------------------------------ |
| `mcp-obsidian-integration.mdc`        | Add § Error Handling Protocol (trace, summarize, log, severity, rollback/fallback).  |
| `para-zettel-autopilot.mdc`           | Add § Error handling (ingest); reference protocol; Errors.md + Ingest-Log.           |
| `ingest-processing.mdc`               | Add § Error handling; reference protocol; Errors.md + Ingest-Log.                    |
| `auto-distill.mdc`                    | Add § Error handling; reference protocol; Errors.md + Distill-Log (+ Backup-Log).    |
| `auto-archive.mdc`                    | Add § Error handling; reference protocol; Errors.md + Archive-Log + Backup-Log.      |
| `auto-express.mdc`                    | Add § Error handling; reference protocol; Errors.md + Express-Log + Backup-Log.      |
| `auto-organize.mdc`                   | Add § Error handling; reference protocol; Errors.md + Organize-Log + Backup-Log.     |
| `non-markdown-handling.mdc`           | Add § Error handling; reference protocol; Errors.md (+ Ingest-Log when from ingest). |
| `Cursor-Skill-Pipelines-Reference.md` | Add § Error handling (all pipelines); point to protocol and Errors.md.               |
| `3-Resources/Errors.md`               | **Create** with frontmatter and entry format.                                        |
| All modified rule files               | Save `.bak` before editing.                                                          |


---

## 8. Ambiguities and choices

1. **Errors.md location:** User prompt mentioned `Vault/Logs/Errors.md`. Vault has no `Logs/`; all logs are in `3-Resources/`. Plan uses `**3-Resources/Errors.md`** for consistency and Dataview. If you prefer a new `Logs/` folder, say so and the plan can use `3-Resources/Logs/Errors.md` or a top-level `Logs/Errors.md`.
2. **Inbox Review hub:** No existing hub named "Inbox Review" was found. Plan uses "flag for user review" and `#review-needed` in Errors.md; a future note (e.g. "Inbox Review") can use Dataview to list `#review-needed` from Errors.md and pipeline logs. No new plugin.
3. **Per-entry frontmatter in Errors.md:** Standard Markdown does not support multiple YAML blocks per note. So either: (A) one YAML block per error **as a fenced block** in the body (e.g. `

```yaml ...

``` `) so Dataview can still query if it supports it, or (B) a single note-level frontmatter and each **entry** as a heading with a table or list for pipeline/severity/timestamp. Plan uses **(B)** with a table or structured list per entry (pipeline, severity, timestamp, approval) so the note stays one file and Dataview can query the note; for per-entry Dataview, we could add a table row per error. Clarification: I'll define each error entry as a `### YYYY-MM-DD HH:MM — title` with a **table** right below for `pipeline`, `severity`, `approval`, `timestamp` so Dataview (e.g. from file) can still be used; or we use a single frontmatter and list all entries in the body with explicit **pipeline:**, **severity:** lines in the entry text. Simplified: one note-level frontmatter; each entry = heading + table (pipeline | severity | approval | timestamp) + Trace + Summary. No multi-YAML in one file.
4. **Watcher/bridge workflows:** No explicit "watcher" or "bridge" rule files were found in `.cursor/rules`. If you have external watchers or bridge scripts that invoke the agent, they can be documented to append to the same Errors.md and follow the same protocol when they report errors; no rule file change needed unless you add a dedicated rule for them.

---

**Next step:** Please confirm approval (or request edits). After approval, I will: (1) create all `.bak` backups, (2) add the Error Handling Protocol to `mcp-obsidian-integration.mdc`, (3) add the error-handling subsection to each pipeline and supporting rule, (4) add the error-handling subsection to `Cursor-Skill-Pipelines-Reference.md`, (5) create `3-Resources/Errors.md`. I will not run destructive tests in your live vault; you can run a simulated error test in a copy if desired.
```

