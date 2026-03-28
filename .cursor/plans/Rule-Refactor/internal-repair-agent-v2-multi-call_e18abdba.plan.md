---
name: internal-repair-agent-v2-multi-call
overview: Refine the Internal Repair Agent design to support up to three separate IRA calls per pipeline run, each followed by little val retries, under Cursor’s single-call subagent model.
todos:
  - id: ira-v2-limits
    content: "Codify per-run limits: up to three IRA calls and four little val cycles, each with three internal attempts."
    status: completed
  - id: ira-v2-interface
    content: Specify the precise IRA v2 input/output schema including history and risk levels for suggested fixes.
    status: completed
  - id: ira-v2-reports
    content: Define the structure and location of IRA v2 report notes and how pipelines/ audits will use them.
    status: completed
  - id: ira-v2-pipeline-integration
    content: Describe how each pipeline subagent sequences little val cycles and up to three IRA calls within a single run.
    status: completed
isProject: false
---

## Internal Repair Agent v2 (multi-call) Design

### Core idea

Adapt the Internal Repair Agent (IRA) to Cursor’s **single-call, single-return** subagent model by allowing **up to three separate IRA calls per pipeline run**, each followed by a fresh little val repair cycle, while maintaining strict safety and clear outcome categories.

### Tiered repair flow per pipeline run

- **Step 1 – Pipeline execution**
  - Pipeline subagent (roadmap, ingest, archive, organize, distill, express) runs its normal logic for the run (e.g. RESUME_ROADMAP deepen, ARCHIVE MODE sweep).
- **Step 2 – Little val cycle #1 (self-repair)**
  - Pipeline invokes **little val** as a skill:
    - Up to **3 internal attempts**:
      - Each attempt inspects structural artifacts vs claimed outcome.
      - On `ok: false`, little val returns `missing[]` + `hint` and pipeline attempts a targeted repair.
    - If any attempt yields `ok: true` → pipeline may safely return `Success`.
    - If, after 3 attempts, `ok` is still false → escalate to IRA call #1.
- **Step 3 – IRA call #1**
  - Pipeline calls IRA once with:
    - Mode, params, IDs (`queue_entry_id`, `project_id`, optional `parent_run_id`).
    - Paths to artifacts (logs, state files, target note, snapshots).
    - Summary of what it did and the last little val verdict (missing/hint, attempts used).
  - **IRA responsibilities on call #1**:
    - Re-evaluate structure using shared little val core logic.
    - Produce a **repair report** note plus a structured **repair plan**:
      - Low-risk edits pipeline may auto-apply (e.g. add missing workflow_state row; recompute metrics; insert missing log line).
      - Medium/high-risk suggestions that should not be auto-applied.
- **Step 4 – Little val cycle #2 (after IRA #1)**
  - Pipeline reads IRA #1’s plan and:
    - Applies only low-risk, precise fixes under existing safety gates (backups, snapshots).
    - Skips or marks for human review any higher-risk recommendations.
  - Pipeline runs little val again (up to 3 internal attempts):
    - If `ok: true` at any attempt → return `Success`.
    - If still `ok: false` after 3 attempts → eligible to call **IRA #2**.
- **Step 5 – IRA call #2 and little val cycle #3**
  - **IRA call #2**:
    - Same contract as #1, but IRA sees: prior plan, what was applied, updated artifacts, and new little val verdicts.
    - Produces a second repair report and refined plan (may now suggest more cautious or alternative repairs).
  - Pipeline again applies low-risk parts of plan #2 and runs little val (up to 3 attempts):
    - If `ok: true` → `Success`.
    - If not → proceed to **IRA call #3**.
- **Step 6 – IRA call #3 and final little val cycle #4**
  - **IRA call #3** (final):
    - Receives full history: initial state, prior IRA plans, what was applied, and all little val verdicts.
    - Produces a final repair report and plan.
  - Pipeline applies safe portions, then runs little val again (up to 3 attempts):
    - If `ok: true` → `Success`.
    - If still `ok: false` → run is classified as **true failure / unrepairable**.

### Attempt and call limits

- **little val**
  - Per cycle: up to **3 attempts** (check → hint → repair attempt) before escalation.
  - Per run: may be invoked after initial pipeline work and after each IRA call (up to 4 cycles total), but each cycle respects the **3-attempt** internal limit.
- **IRA**
  - Per pipeline run: up to **3 separate IRA calls** (IRA #1, #2, #3), each invoked only when prior little val cycle has exhausted its 3 attempts and still returns `ok: false`.
  - Each IRA call returns once with its report and plan; no in-run back-and-forth.

### Outcome taxonomy (per run)

- **Success**
  - Little val’s final verdict for the run is `ok: true` (whether achieved after self-repair only or after one/two/three IRA-assisted loops).
- **Review needed**
  - Optional intermediate outcome if you want to surface runs that:
    - Were structurally repaired to `ok: true`, but only via IRA plans that included medium/high-risk suggestions you chose not to auto-apply; or
    - Need human approval for some of IRA’s proposed changes, even though the current structure is minimally `ok`.
- **True failure / unrepairable**
  - After:
    - little val cycle #1 (3 attempts) → IRA #1 → little val #2 (3 attempts) → IRA #2 → little val #3 (3 attempts) → IRA #3 → little val #4 (3 attempts),
    - the final little val still returns `ok: false`.
  - Pipeline must mark the run as **true failure / unrepairable structural contract**, attach references to all IRA reports and last little val verdicts, and avoid further automated repair attempts for that run.

### IRA v2 contract details

- **Inputs per call**
  - `pipeline`, `mode`, `params`, `queue_entry_id`, `project_id`, optional `parent_run_id`.
  - Paths to relevant artifacts: logs, state files, target note path, known snapshots.
  - History snapshot:
    - Which IRA call this is (`1`, `2`, or `3`).
    - What earlier IRA calls recommended and what was applied.
    - little val’s previous attempts and their `missing`/`hint` arrays.
- **Outputs per call**
  - `status`: `"repair_plan"` | `"unrepairable"` (per IRA call’s perspective).
  - `suggested_fixes`: structured steps grouped by risk level (`low`, `medium`, `high`).
  - `rationale`: why these fixes should address the mismatch.
  - `patterns`: optional observations for system improvement (e.g. recurring missing metrics for a given mode).
  - IRA report note path (so pipeline and later audits can reference it).
- **Hard invariants**
  - Read-only on user artifacts (notes, logs, state files, snapshots) except writing its own report note(s).
  - No queue or wrapper changes; no Watcher-Result writes.
  - No nested subagent calls from IRA; may call skills (including little val core) internally.

### Reporting and system improvement

- **Per-call reports**
  - Every IRA invocation writes a report note containing:
    - Context: pipeline, mode, ids, call index (1–3).
    - Structural discrepancies detected (from little val core).
    - Proposed fixes and their risk levels.
    - Whether this plan was fully applied, partially applied, or skipped.
    - Observed outcome (based on subsequent little val checks when available).
- **Telemetry and logging**
  - Each IRA call writes a Run-Telemetry entry (`actor: internal-repair-agent`, `attempt_index: 1–3`, `final_status: repair_plan|unrepairable`).
  - Pipelines annotate their own logs with:
    - `ira_calls: 0–3`, `ira_reports: [paths]`, `ira_final_outcome: repaired|unrepairable`.
- **Feedback loop for system tuning**
  - You can periodically:
    - Scan IRA reports to see recurring structural issues.
    - Adjust pipeline logic and little val’s checks to prevent them.
    - Refine what is considered low vs medium vs high risk in IRA plans.

### Relationship to little val and big Validator

- **little val**
  - Remains the **first structural gate** and self-repair helper.
  - Is the only authority that can say "structure is now ok"; Success is gated on little val’s final `ok: true`.
- **Internal Repair Agent v2**
  - Steps in only when little val’s 3 attempts per cycle cannot reach `ok: true`.
  - Can be invoked up to 3 times per run, each time after a failed little val cycle.
  - Does not directly change user artifacts; only proposes fixes.
- **Big Validators (quality)**
  - Continue to run via queue as separate subagents.
  - May consult little val’s core logic to ensure structural soundness before quality evaluation, but do not participate in the repair loops.

This v2 design respects Cursor’s call-once subagent model, gives you up to three IRA-assisted repair opportunities per run, and ensures every attempt is observable and learnable via structured reports and telemetry.