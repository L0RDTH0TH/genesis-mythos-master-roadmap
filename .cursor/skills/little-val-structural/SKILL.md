---
name: little-val-structural
description: "Shared structural contract checker (“little val”) used by all pipeline subagents and validators to detect false successes and structural glitches."
---

# little val – Structural Contract Skill

This skill implements the **Phase 1** contract from `little-val-structural-validator-integration`: a fast, read-only structural validation for a *single run* (artifacts vs claimed outcome), not content quality.

## Inputs (from callers)

Callers pass a single argument object with:

- `mode` (string, required): queue mode / action for this run (e.g. `RESUME_ROADMAP`, `ROADMAP_MODE`, `INGEST_MODE`, `ARCHIVE_MODE`, `ORGANIZE_MODE`, `DISTILL_MODE`, `EXPRESS_MODE`).
- `params` (object, required): **effective params** for this run after Config/profile merges and queue overrides.
- `ids` (object, required):
  - `queue_entry_id` (string) — queue id or synthetic id.
  - `project_id` (string) — project id or `"-"` when not applicable.
  - `parent_run_id` (string | null) — parent Run-Telemetry id when available.
- `artifacts` (object, required):
  - `pipeline` (string) — one of `"roadmap"`, `"ingest"`, `"archive"`, `"organize"`, `"distill"`, `"express"`.
  - `paths` (object) — pipeline-specific artifact paths:
    - For roadmap: `workflow_state`, `roadmap_state`, `decisions_log`, `distilled_core`, `moc`, plus any relevant phase notes or snapshots.
    - For ingest: original/target note path, `Ingest-Log`, `Backup-Log`, snapshots, wrapper path when relevant.
    - For archive: archived note path, `Archive-Log`, `Backup-Log`, snapshots.
    - For organize: note path, `Organize-Log`, `Backup-Log`, snapshots.
    - For distill: note path, `Distill-Log`, `Backup-Log`, snapshots/version markers.
    - For express: note path, `Express-Log`, `Backup-Log`, version snapshot paths.
  - `extra` (object | null) — any additional per-pipeline fields you want to use for checks.
- `attempt_index` (integer, optional): 1–3 for this run’s current little val check; echoed back for logging.

Validators/audits may reuse these fields but typically care only about `mode`, `params`, `ids`, and `artifacts.paths`.

## Output (to callers)

The skill returns:

- `ok` (boolean, required):
  - `true` when artifacts match what a **successful** run for this pipeline + mode must produce.
  - `false` when a required artifact is missing, malformed, or inconsistent.
- `missing` (string[], required when `ok: false`):
  - Human-readable descriptions of structural problems, e.g.:
    - `"workflow_state log row for this deepen run is missing or not updated"`.
    - `"snapshot before archive move not found in Backups/Per-Change"`.
    - `"Express-Log entry for this queue_entry_id not found"`.
    - `"distilled-core.md Phase 0 section missing for this project"`.
- `hint` (string, required when `ok: false`):
  - Short guidance on how the caller should repair the structure, e.g.:
    - `"Append a workflow_state row with updated Ctx Util %, Leftover %, Threshold, Est. Tokens for this deepen run"`.
    - `"Write an Archive-Log line and ensure a per-change snapshot exists before the move"`.
- `category` (string, optional): machine tag such as `"missing-log"`, `"missing-snapshot"`, `"broken-moc"`, `"state-mismatch"`.
- `attempt_index` (integer, optional): echo of the input `attempt_index`.

The implementation may add debug fields, but callers must not rely on them.

## Per-pipeline structural checks (first pass)

This section codifies the “first pass” checks from `little-val-structural-validator-integration`:

- **Roadmap (`pipeline: "roadmap"`)**
  - `RESUME-ROADMAP` with `action: deepen` / `advance-phase`:
    - Verify a new `workflow_state` row exists for this run (via id/timestamp/phase, not exact text).
    - When `enable_context_tracking !== false`, assert last row has valid `Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens`.
    - Optionally confirm roadmap-state snapshot invariants (snapshot before/after state changes).
  - Other actions (`revert-phase`, `sync-outputs`, `handoff-audit`, etc.):
    - Check expected state files / report notes exist and were updated (e.g. updated phase, new audit note).
  - `ROADMAP MODE` setup:
    - `roadmap-state.md`, `workflow_state.md`, `decisions-log.md`, `distilled-core.md`, and the roadmap MOC all exist.
    - `workflow_state.md` has the expected initial Phase 0 row(s).

- **Ingest (`pipeline: "ingest"`)**
  - Phase 1 (propose):
    - Ingest-Log has an entry for this run (by queue_entry_id).
    - Any destructive actions (cursor-agent direct moves) are mirrored in Backup-Log and snapshots.
  - Phase 2 (apply-mode):
    - Target note is at the selected path.
    - Ingest-Log + Backup-Log + snapshots reflect the move.
    - Wrapper (if any) is updated/marked processed as per ingest spec.

- **Archive (`pipeline: "archive"`)**
  - Note is under `4-Archives/` with `status: archived`.
  - Archive-Log and Backup-Log entries exist for this run.
  - A per-change snapshot exists for the move.

- **Organize (`pipeline: "organize"`)**
  - Note path and rename (if any) match the `subfolder-organize` outcome.
  - Organize-Log reflects the change.
  - Snapshots exist before rename/move when path_conf ≥85%.

- **Distill (`pipeline: "distill"`)**
  - Distilled note contains expected layers, TL;DR, and readability callout, or an appropriate Decision Wrapper is present instead.
  - Distill-Log has a line for this run; Backup-Log + snapshots exist for structural rewrites.

- **Express (`pipeline: "express"`)**
  - Version snapshot exists under `Versions/<slug>--<timestamp>.md`.
  - Related/outline/CTA are present or intentionally omitted based on confidence / wrapper decisions.
  - Express-Log + Backup-Log entries exist.

## How callers must use little val (single-run loop)

Pipeline subagents (roadmap, ingest, archive, organize, distill, express) must follow this pattern per run:

1. Execute normal pipeline steps for the queue entry (including backups, snapshots, moves/rewrites, logging).
2. Call `little-val-structural` once with `attempt_index: 1`.
3. If `ok: true` → the run may be returned as **Success**.
4. If `ok: false`:
   - Use `missing[]` + `hint` to attempt a **targeted structural repair** for this run only (e.g. append a missing log row, backfill metrics, add snapshot marker), obeying backup/snapshot + confidence gates.
   - Increment `attempt_index` and call `little-val-structural` again.
5. Allow up to **3 checks** per run (attempt_index 1–3).
6. After the third check, if `ok` is still `false`:
   - **Do not return Success.**
   - Return `#review-needed` or `failure` with a structural-glitch reason that includes the last `missing[]` + `hint`.
   - The caller may then escalate to the **Internal Repair Agent** per `internal-repair-agent-v2-multi-call` and `internal-repair-agent.md` (IRA calls 1–3, each followed by a fresh little val cycle). The pipeline applies IRA `suggested_fixes` at any `risk_level` when safety gates allow (see Subagent-Safety-Contract).

## Safety and validator integration

- This skill is **read-only** on user artifacts; it must not write notes, logs, or state files.
- All repairs are implemented by the calling subagent under existing backup/snapshot + confidence rules.
- Validator/audit subagents may reuse this same contract in **diagnostic** mode:
  - Given mode, params, ids, and artifact paths, recompute `ok/missing/hint` independently of the original run.
  - Use results to gate or annotate quality judgments (e.g. ROADMAP_HANDOFF_VALIDATE, distill_readability, express_summary), but do not auto-fix content.

