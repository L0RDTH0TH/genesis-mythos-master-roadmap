---
name: little-val-structural-validator-integration
overview: Introduce a shared structural contract checker (little val) as a skill used by all pipeline subagents, then integrate the same logic into validator/audit subagents for post-hoc and quality-focused checks.
todos:
  - id: define-little-val-contract
    content: Define little val’s core contract (inputs, outputs, invariants) and per-pipeline structural checks.
    status: pending
  - id: wire-little-val-into-subagents
    content: Specify how each pipeline subagent calls little val, performs up to 3 repair attempts, and only returns Success when little val is satisfied.
    status: pending
  - id: design-structural-audit-flow
    content: Design a structural audit/validator subagent flow that reuses little val logic to diagnose unrepaired structural glitches.
    status: pending
  - id: integrate-with-quality-validator
    content: Describe how existing and future quality validators call little val first to ensure structural soundness before emitting quality judgments.
    status: pending
isProject: false
---

## Little val structural validation rollout

### Phase 1: Little val skill inside pipeline subagents

- **Define little val’s core contract**
  - **Purpose**: fast, read-only structural validation of a *single run* (artifacts vs claimed outcome), not content quality.
  - **Inputs** (from the caller subagent):
    - mode and params for the run (e.g. `RESUME_ROADMAP` + `action: deepen`).
    - IDs: `queue_entry_id`, `project_id`, optionally `parent_run_id` and a pointer to the Run-Telemetry draft or note.
    - Paths to pipeline-specific artifacts: e.g. for roadmap, `1-Projects/<project_id>/Roadmap/workflow_state.md`, `roadmap-state.md`; for others, their log files and target note paths.
  - **Output shape** (conceptual):
    - `ok: boolean` — whether the run’s structural artifacts match what a successful run must produce.
    - `missing: string[]` — human-readable descriptions of missing/incorrect artifacts.
    - `hint: string` — short guidance to the subagent on how to repair (e.g. "No workflow_state log row for this deepen"; "Snapshot missing before move").
- **Specify per-pipeline structural checks (first pass for roadmap, then general pattern)**
  - **Roadmap (RESUME-ROADMAP)**:
    - For `action: deepen` / `advance-phase`:
      - Verify a new `workflow_state` log row exists for this run (by timestamp / phase, not exact text).
      - When `enable_context_tracking !== false`, assert that the last log row has valid `Ctx Util %`, `Leftover %`, Threshold, Est. Tokens fields.
      - Optionally confirm roadmap-state snapshotting invariants (snapshot before/after phase/state changes).
    - For `revert-phase`, `sync-outputs`, `handoff-audit`, etc.:
      - Check expected state files or report notes exist and were updated (e.g. updated phase, new audit note).
  - **Other pipelines (Ingest, Archive, Organize, Distill, Express)**:
    - Ingest: note moved or processed as per mode; Ingest-Log line exists; snapshots/backups match destructive actions.
    - Archive: note under `4-Archives/` with status `archived`; Archive-Log/Backup-Log entries; snapshot before move.
    - Organize: note path/rename matches subfolder-organize outcome; Organize-Log reflects the change; snapshot before rename/move.
    - Distill: expected layers/TL;DR/readability callouts or Decision Wrapper present; Distill-Log line present.
    - Express: version snapshot written; related/outline/CTA appended as planned; Express-Log entry present.
- **Design the retry behaviour around little val**
  - **Single-run loop inside each subagent**:
    - Step 1: pipeline executes as usual and prepares to return.
    - Step 2: call the little val skill with the run context.
    - Step 3: if `ok: true`, subagent may return **Success**.
    - Step 4: if `ok: false`, treat it as a hallucinated completion / glitch, not an immediate failure:
      - Use `missing`/`hint` to attempt to repair the structural gap (e.g. append the missing log row, write metrics, record snapshot flag).
      - Call little val again to re-check.
    - Step 5: allow up to **3 total checks** (one initial + up to two repair cycles, or three full fix cycles depending on implementation detail) before giving up.
    - Step 6: only after the third failed check:
      - The subagent returns `#review-needed` or `failure` with an explicit structural-glitch reason (e.g. "Could not create consistent workflow_state row for this deepen run after 3 attempts").
  - **Invariant**: a pipeline subagent **must not** return `Success` if the last little val verdict is `ok: false`, but it should exhaust its 3 repair attempts first to avoid noisy false failures.
- **Integrate little val skill conceptually into each subagent**
  - **Roadmap subagent** (`.cursor/agents/roadmap.md`):
    - After performing the requested action and before writing final Run-Telemetry and returning a status string, run the little val skill with roadmap-specific checks.
    - Use its verdict to either:
      - Confirm `Success`, or
      - Trigger at most 3 self-repair attempts, then return `#review-needed`/`failure` if still inconsistent.
  - **Ingest, Distill, Express, Archive, Organize subagents** (`.cursor/agents/*.md`):
    - Add a final "contract-check" step using the little val skill before returning.
    - Each subagent translates `missing`/`hint` into a targeted fix (e.g. adding a missing log entry, snapshot, or wrapper) when possible.
  - **Subagent Safety Contract alignment**:
    - Clarify that little val as a **skill** is not a subagent; it runs inside the calling subagent and does not violate the "no subagent calls other subagents" rule.
    - Document that subagents are encouraged to self-repair based on little val hints before surfacing a non-success outcome.
- **Logging and observability for little val in Phase 1**
  - When little val detects a mismatch but repair succeeds on a subsequent attempt, the subagent may:
    - Add a short note to its pipeline log line (e.g. `contract_glitch_repaired: true`, `repair_attempts: 1`).
  - When repair fails after 3 attempts:
    - Include a clear `error_type` or flag (e.g. `contract_glitch_unrepaired`) in Errors.md and/or the pipeline log.
    - This will be the primary signal for Phase 2 audit runs.

### Phase 2: Validator / audit subagent integration using little val

- **Clarify the audit use case**
  - Target only **true failures** that little val couldn’t fix in Phase 1 (or runs tagged with structural-glitch flags).
  - Focus on **structural contract failures**, not content quality itself.
  - Auditor’s job:
    - Explain why the run could not be auto-repaired.
    - Suggest human or queued fixes.
    - Optionally create Decision Wrappers for your review.
- **Reuse little val’s core logic inside the audit/validator subagent**
  - Factor out little val’s checks into a shared conceptual core:
    - Given mode, params, IDs, and artifact paths, compute the same `ok/missing/hint` verdict.
  - In the **validator/audit subagent** (either a new mode or additional `validation_type`):
    - Use the same core to recompute the verdict **independently** of the original run.
    - Do not attempt auto-fixes here; treat this as diagnosis only.
- **Define a structural audit flow**
  - Entry criteria (for queue modes or manual audit runs):
    - Runs where:
      - The subagent returned `#review-needed` or `failure` with a structural-glitch flag, or
      - Run-Telemetry and pipeline logs indicate repeated little val failures.
  - Audit subagent steps:
    - Read the Run-Telemetry note(s) for the selected `queue_entry_id`.
    - Read relevant pipeline logs and state files for that run.
    - Invoke the shared little val logic to see what is still missing or inconsistent.
    - Produce a **structured report** note (e.g. under the project’s Roadmap folder or a dedicated audit area) that includes:
      - Summary of what the run attempted.
      - little val’s latest verdict (missing list + hint).
      - Suggested repairs (manual edits or queued actions).
    - Optionally create a **Decision Wrapper** that lets you choose between proposed fixes (e.g. "Re-run RESUME-ROADMAP from last safe", "Repair workflow_state manually", "Ignore this glitch").
- **Integrate quality-focused Validator with little val**
  - For existing or future quality validators (e.g. `ROADMAP_HANDOFF_VALIDATE`, `distill_readability`, `express_summary`):
    - Before judging quality, these validators may call the shared little val logic to:
      - Confirm that the underlying run is structurally sound.
      - If not structurally sound, they can:
        - Either defer quality judgment and mark the run as needing structural repair first, or
        - Include structural issues in their quality report (e.g. "handoff readiness blocked: missing recent workflow_state entries").
  - This ensures all validators treat **structural contract adherence** as a prerequisite lens on top of which quality is assessed.
- **Observability and safeguards for Phase 2**
  - Ensure that structural audit runs:
    - Are read-only on user content except for writing their report notes and optional Decision Wrappers.
    - Write their own Run-Telemetry notes with a distinct actor (e.g. `actor: structural-validator`).
  - Use Errors.md and pipeline logs to track patterns:
    - How often little val repairs succeed vs. escalate.
    - Which pipelines most frequently hit structural glitches.

### Overall invariants to maintain

- **No silent bogus successes**: a pipeline subagent may only return `Success` when the final little val verdict is `ok: true`, after up to 3 repair attempts.
- **Glitches are repair-first, not fail-first**: a structural mismatch is treated first as a prompt for self-correction; only escalates to a true failure when little val cannot get to `ok` after its allowed attempts.
- **Shared logic**: little val’s contract-checking brain is a single conceptual source of truth, reused both as:
  - A skill for in-run self-healing; and
  - A library used by validator/audit subagents for structural audits and for gating quality checks.
- **Validators respect structure before quality**: big validators (handoff, readability, express quality) should either refuse to pass a run that is structurally inconsistent, or clearly label structural issues in any quality report they emit.

