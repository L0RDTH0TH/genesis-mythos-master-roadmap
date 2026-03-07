---
name: auto-pipelines-rules-and-quickadd
overview: Validate and tighten the autonomous distill/archive/express context rules and design QuickAdd entrypoints for ingest and downstream pipelines, with an emphasis on mobile-friendly triggers and safety invariants.
todos: []
isProject: false
---

# Auto-pipelines context rules + QuickAdd design

## Objective

Ensure the autonomous post-capture pipelines (ingest, distill, archive, express) are safely triggerable via clear natural-language context rules, and design a small, mobile-friendly QuickAdd surface that can kick off ingest and downstream processing.

**Time allocation**: 45 min rules review + confidence normalization | 45 min QuickAdd/mobile design | 30 min checklist + validation.

---

## 1. Rules review and tightening (45 min)

### 1.1. Confidence normalization (first sub-step)

- **Before any other rule edits**, run an explicit grep for confidence variants across all `.cursor/rules/**/*.mdc` (including ingest, snapshot, always-applied):
  - Search for: `90%`, `80%`, `75%`, `70%`, and any other numeric thresholds used for destructive or structural actions.
- **Normalize to Master Goal invariant**: Replace any threshold used for destructive actions (moves, rewrites, large appends, hub appends) with **85%**.
  - If a specific step is intentionally non-destructive (e.g. suggestion-only, or append-to-log only), add a short comment in the rule: e.g. *"Non-destructive; threshold may remain at 75%."*
- **Outcome**: All three context rules (distill, archive, express) and para-zettel-autopilot + snapshot rules state clearly: **≥85%** for any action that modifies note content or location; lower thresholds only where explicitly documented as non-destructive.

### 1.2. Re-read and tighten each context rule

- For `auto-distill.mdc`, `auto-archive.mdc`, `auto-express.mdc`:
  - Inspect metadata (`description`, `globs`), trigger phrases, pipeline steps, snapshot sections, logging requirements, exclusions, and safety notes.
  - Cross-check against the snapshot skill and `Cursor-Skill-Pipelines-Reference.md` (or equivalent pipelines reference).

### 1.3. Snapshot and fallback behavior

- Ensure in all three rules:
  - Snapshot calls reference the `obsidian-snapshot` skill with `type: "per-change"` and `type: "batch"` as in the skill.
  - **Critical invariant** stated: no destructive action unless confidence ≥85% **and** snapshot creation succeeded; otherwise skip and log `#review-needed`.
  - Fallback: backup/snapshot failure → skip destructive steps, log in pipeline log **and** `Backup-Log.md`; `obsidian_move_note` or version-file write failures → follow `obsidian_ensure_structure` from the always-applied MCP rule.

### 1.4. Triggers, globs, exclusions

- Confirm trigger phrases are short and unique; verify globs and exclusion lists so only `1-Projects/`**, `2-Areas/`**, `3-Resources/**` are processed; exclude `4-Archives/**`, `Backups/**`, `Templates/**`, logs, hubs, and `Versions/` where appropriate.

### 1.5. Harmonize logging formats

- Standardize required log fields (timestamp, pipeline, note path, confidence, actions taken/skipped, backup path, snapshot path(s), flag) and confirm each rule logs to its dedicated log plus `Backup-Log.md`.

---

## 2. QuickAdd design for autonomous pipelines (45 min)

### 2.1. Four primary QuickAdd entries (design only)

- **Ingest – Start Batch**
  - **Goal**: Append canonical ingest trigger (e.g. `"INGEST MODE – safe batch autopilot"` + timestamp) to `Ingest-Log.md`.
  - **Type**: Macro (default); optional Capture for simple append-only.
  - **Behavior**: Optionally prompt for short batch label; append timestamped trigger line to log; optional success notification.
  - **Mobile**: Name `Ingest Batch`; toolbar-suitable.
- **Process Ingest Now**
  - **Goal**: Stronger intent to run ingest immediately.
  - **Type**: Macro.
  - **Behavior**:
    - **Primary**: Append `"INGEST MODE – execute now"` (or similar) with scope to `Ingest-Log.md`.
    - **Automation option**: If Advanced URI plugin is installed, design an option to open Cursor with pre-filled prompt, e.g. `obsidian://advanced-uri?vault=Second-Brain&commandid=cursor:open-composer&prompt=DISTILL%20MODE...` (exact command ID and encoding to be confirmed against Obsidian/Cursor URI docs).
    - **Fallback**: If URI is not available or fails, log the trigger and show notification: *"Open Cursor manually to run pipeline."*
  - **Mobile**: Name `Run Ingest`; toolbar-suitable.
- **Distill Current Note**
  - **Goal**: Trigger autonomous-distill for the active note.
  - **Type**: Macro.
  - **Behavior**:
    - Capture current note path/title.
    - **Option A**: Append to `3-Resources/Distill-Log.md` with `"DISTILL MODE – safe batch autopilot"` + note reference.
    - **Option B (Advanced URI)**: Open Cursor with pre-filled instruction e.g. `"DISTILL MODE – safe batch autopilot on [[Note Title]]"`; fallback if URI fails: log + notification *"Open Cursor manually."*
  - **Mobile**: Name `Distill`; single-tap friendly.
- **Express / Quick Polish**
  - **Goal**: Trigger autonomous-express for the active note.
  - **Type**: Macro (default); optional Capture only if a simple append is sufficient.
  - **Behavior**: Capture current note; signal via log or Advanced URI with `"EXPRESS MODE – safe batch autopilot"` / `"express this note"`; fallback: log + *"Open Cursor manually."*
  - **Mobile**: Name `Express`; toolbar-friendly.

**Default**: Use **Macro** for all four; use Capture only where the sole action is a simple append to a log file. Document fallback (log + notification) whenever Advanced URI is part of the design.

### 2.2. QuickAdd configuration mapping

- For each entry, specify in the plan or a short doc: `name`, `type` (macro/capture), macro steps if Macro, and that these should be exposed as **commands** for Obsidian Mobile toolbar (Settings → Mobile → Manage toolbar options).
- **Ingest template chooser**: Remain a separate command/palette entry; do not put full template selection on the four toolbar buttons.

### 2.3. Mobile flow

- Document: Capture → tap `Ingest Batch` or `Run Ingest` → later run pipelines in Cursor; `Distill` / `Express` can either log-only or, with Advanced URI, open Cursor with pre-filled prompt for hands-off bridge from mobile.

---

## 3. Log existence check (in finalization)

- **Before finalizing logging formats (in step 5.1)**: Verify that the following files exist in the vault:
  - `3-Resources/Distill-Log.md`
  - `3-Resources/Archive-Log.md`
  - `3-Resources/Express-Log.md`
- If any are missing, add to the execution checklist: **create stub files** (e.g. minimal frontmatter + "Log for autonomous-distill/archive/express pipeline") so the rules and pipelines have a defined logging target. Document this in plan notes.

---

## 4. Visual Health Dataview (trimmed)

- **2–3 bullet sketch only** (low priority; full Dataview deferred to post-execution):
  - Single note (e.g. `3-Resources/Visual-Health.md`) with Dataview sections: counts by pipeline flags (`#review-needed`, `resurface-candidate`, `needs-simplify`) and by location (Ingest/, Projects, Archives).
  - Sections: "Items awaiting ingest", "Notes flagged for review", "Resurface candidates."
  - Full query design and maintenance after rules + QuickAdd execution are stable.

---

## 5. Sanity-check and execution checklist

### 5.1. Cross-check and log verification

- Cross-check refined rules against `Cursor-Skill-Pipelines-Reference` and snapshot skill; ensure snapshot triggers and confidence gates match.
- **Log existence check**: Confirm `Distill-Log.md`, `Archive-Log.md`, `Express-Log.md` exist; plan stub creation if missing (see section 3).

### 5.2. Execution checklist (tabular + validation)

Use this table during the execution phase; add a post-edit validation step at the end.


| File                                                | Section               | Change                                                                                                 |
| --------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------ |
| `.cursor/rules/context/auto-distill.mdc`            | Confidence thresholds | Normalize to ≥85% for destructive steps; add comment for any exception                                 |
| `.cursor/rules/context/auto-distill.mdc`            | Snapshots / Safety    | State critical invariant; fallback #review-needed + Backup-Log                                         |
| `.cursor/rules/context/auto-archive.mdc`            | Confidence thresholds | Same as above                                                                                          |
| `.cursor/rules/context/auto-archive.mdc`            | Snapshots / Safety    | Same as above                                                                                          |
| `.cursor/rules/context/auto-express.mdc`            | Confidence thresholds | Same as above                                                                                          |
| `.cursor/rules/context/auto-express.mdc`            | Snapshots / Safety    | Same as above                                                                                          |
| `.cursor/rules/context/para-zettel-autopilot.mdc`   | (if needed)           | Apply 85% normalization from grep                                                                      |
| `.cursor/rules/always/mcp-obsidian-integration.mdc` | (if needed)           | Apply 85% from grep                                                                                    |
| `3-Resources/Distill-Log.md`                        | —                     | Create stub if missing                                                                                 |
| `3-Resources/Archive-Log.md`                        | —                     | Create stub if missing                                                                                 |
| `3-Resources/Express-Log.md`                        | —                     | Create stub if missing                                                                                 |
| `.obsidian/plugins/quickadd/data.json`              | `choices`             | Add four Macro entries: Ingest Batch, Run Ingest, Distill, Express (with fallback/URI design from 2.1) |


**Post-edit validation**: Run a tiny ingest batch in Cursor (e.g. 1–2 notes from `Ingest/`) and confirm logs (Ingest-Log.md, Backup-Log.md) and snapshots (Per-Change, Batch) are written as expected; fix any mismatches before closing the session.

---

## Todos

- **confidence-normalize**: Grep all .mdc for 90%/80%/75%/70%; replace destructive-action thresholds with 85%; add comments for non-destructive exceptions.
- **rules-tighten**: Apply snapshot invariant, fallbacks, triggers, globs, exclusions, and logging format to auto-distill, auto-archive, auto-express (and ingest/snapshot if needed).
- **quickadd-design**: Finalize four choices (names, types, Macro steps, Advanced URI option + fallback); document for data.json.
- **log-stubs**: Verify Distill/Archive/Express log files exist; add stub-creation to checklist if missing.
- **checklist-and-validate**: Fill execution table; run small ingest batch and confirm logs/snapshots flow.

