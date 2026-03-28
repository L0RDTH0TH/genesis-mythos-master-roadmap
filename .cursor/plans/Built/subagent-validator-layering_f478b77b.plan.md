---
name: subagent-validator-layering
overview: Refactor subagent layering so hostile Validator runs both nested inside pipeline subagents after little val passes and again from the queue after pipeline success, while preserving safety contracts and documenting the behavior.
todos:
  - id: update-contracts
    content: Tighten Subagent-Safety-Contract and Subagent-Layers-Reference to allow nested validator plus queue-level validator calls.
    status: completed
  - id: define-validator-io
    content: Centralize validation_type input/output schemas and models in Validator-Reference, Parameters, and Second-Brain-Config.
    status: completed
  - id: wire-nested-validator
    content: Modify each pipeline subagent to call ValidatorSubagent after little val passes and gate Success on its verdict.
    status: completed
  - id: wire-queue-double-check
    content: Adjust queue.mdc to run a second validator pass on pipeline Success using validator_context.
    status: completed
  - id: docs-and-sync
    content: Update docs (Queue-Sources, Subagent-Layers-Reference, Validator-Reference) and sync copies to reflect new layering and validator behavior.
    status: completed
isProject: false
---

### Goal

Align subagent layering so that:

- Pipeline subagents (Layer 3) **call ValidatorSubagent (Layer 4) before returning Success**, immediately after little val passes.
- The **Queue/Dispatcher (Layer 2)** also calls ValidatorSubagent once on pipeline success (using the pipeline’s reported context) to catch validator hallucinations.
- All of this stays consistent with Subagent-Safety-Contract (explicit nesting exceptions only) and the new Subagent-Layers-Reference doc.

### Key Files to Touch

- Contracts & architecture:
  - `3-Resources/Second-Brain/Subagent-Safety-Contract.md`
  - `3-Resources/Second-Brain/Docs/Subagent-Layers-Reference.md`
- Queue orchestration:
  - `.cursor/rules/agents/queue.mdc`
  - `3-Resources/Second-Brain/Queue-Sources.md`
- Validator configuration & reference:
  - `3-Resources/Second-Brain/Second-Brain-Config.md`
  - `3-Resources/Second-Brain/Parameters.md`
  - `3-Resources/Second-Brain/Validator-Reference.md`
- Pipeline subagents (Layer 3):
  - `.cursor/agents/ingest.md`
  - `.cursor/agents/roadmap.md`
  - `.cursor/agents/distill.md`
  - `.cursor/agents/express.md`
  - `.cursor/agents/archive.md`
  - `.cursor/agents/organize.md`
  - `.cursor/agents/research.md`
- Validator subagent:
  - `.cursor/rules/agents/validator.mdc`

### Plan

- **Step 1 – Finalize layering model and contracts**
  - Update `Subagent-Safety-Contract.md` to:
    - Explicitly define **Layer 1–4** as in `Subagent-Layers-Reference.md`.
    - Add **ValidatorSubagent as a second allowed nested exception** (alongside IRA) for Layer 3: pipelines may call Validator exactly once per run *after* little val passes, to gate Success.
    - Clarify that Validator remains read-only on inputs and terminal (no further subagents), both for queue-driven and nested usage.
    - Define the combined success gate: a pipeline may only return Success when **(a) little val final `ok: true` and (b) nested validator verdict is not “block_destructive” / equivalent severity.
  - Sync those semantics into `Subagent-Layers-Reference.md` so it names Validator as a Layer 4 helper usable from both Layer 2 and Layer 3.
- **Step 2 – Define validator input/outputs and models centrally**
  - In `Validator-Reference.md` and `Parameters.md`, for each validation_type (`ingest_classification`, `organize_path`, `express_summary`, `archive_candidate`, `roadmap_handoff_auto`, `distill_readability`, `research_synthesis`):
    - Document **required input fields** (e.g. `source_file`, `proposed_path`, `para_type`, `path_conf`, `archive_conf`, `project_id`, `state_paths`, `synth_note_paths`).
    - Document **output contract**: `severity` (high/medium/low), `recommended_action` (`block_destructive`, `create_wrapper`, `log_only`), `report_path`.
  - In `Second-Brain-Config.md` → `validator` block:
    - Ensure **all** these types have a `model` entry and clarify that models apply to both nested and queue-driven validator calls.
    - Clarify that `global_max_per_run` and `global_sampling_rate` apply **only** to standalone `VALIDATE` / `ROADMAP_HANDOFF_VALIDATE` queue entries, not to nested pipeline calls or post-pipeline queue calls.
- **Step 3 – Wire nested validator inside each pipeline subagent (Layer 3)**
  - For each pipeline agent (`ingest.md`, `roadmap.md`, `distill.md`, `express.md`, `archive.md`, `organize.md`, `research.md`):
    - Locate the place where **little val** is called and the final little val verdict is interpreted.
    - Insert a **ValidatorSubagent call** immediately after “little val final `ok: true`”, passing the appropriate **validation_type** and input params defined in Step 2.
      - Example: In `ingest.md`, call ValidatorSubagent with `validation_type: "ingest_classification"` and the current note’s `source_file`, `proposed_path`, `para_type`, and `ingest_conf`.
      - In `distill.md`, call `distill_readability` on the distilled note when note length exceeds configured threshold.
      - In `roadmap.md`, call `roadmap_handoff_auto` with `project_id` and state file paths appropriate for the current action.
    - Implement simple decision logic on the validator verdict:
      - If `severity` maps to `block_destructive` (or equivalent), **do not** return Success; instead return `#review-needed` or `failure` and include validator summary in the return text.
      - Otherwise, allow Success and include a concise summary and validator report path in the return.
    - Update each agent’s **Return** section to state they perform a nested validator call and that Success means "little val ok + validator ok".
- **Step 4 – Keep pipeline return metadata for queue double-check**
  - Keep (or add) a light-weight `**validator_context`** in pipeline returns so that the Queue subagent can re-run validator if desired:
    - Include `validation_type`, `project_id`, and the same input fields used for the nested validator call.
    - Optionally include `validator_first_pass` metadata (e.g. severity, recommended_action, report_path) so the queue can compare the second run to the first.
  - Document this in `Subagent-Safety-Contract.md` as a **return-only advisory** field (used by the queue for cross-checks, not required for pipeline correctness).
- **Step 5 – Adjust queue behavior to run a second validator pass**
  - In `queue.mdc` under the “Dispatch via Task” section’s `(4) When the Task call returns` block:
    - **Retain** the existing post-pipeline validator call, but reframe it as an **independent verification pass**:
      - When a pipeline entry returns Success **and** includes `validator_context` with `validation_type`, the queue:
        - Builds a validator hand-off from `validator_context` + telemetry.
        - Calls ValidatorSubagent via Task (this is the **second** validator run).
        - Logs the verdict and optionally compares it with `validator_first_pass` metadata; inconsistencies can be written to `Errors.md` or flagged as `#review-needed` while still leaving the queue entry processed.
      - Explicitly document that this queue-driven validator **does not** change whether the pipeline entry is cleared from the queue (unless you decide to upgrade inconsistent cases to `failure`), but serves as a **hallucination guard** and audit trail.
    - Make it clear in comments/docstrings that nested validator (inside pipelines) is the primary gate for Success; the queue-level validator is a secondary independent hostile pass.
- **Step 6 – Update docs and sync**
  - Update:
    - `Subagent-Layers-Reference.md` to describe the **two validator touchpoints**:
      - Nested in pipelines (Layer 3 → Layer 4) as a gate.
      - Queue-level double-check (Layer 2 → Layer 4) after pipeline Success.
    - `Queue-Sources.md` to describe the **post-pipeline validator** and how it differs from explicit `VALIDATE` entries.
    - `Validator-Reference.md` with a short section on **"Nested vs Queue-driven validator"**.
  - Ensure `.cursor/sync/rules/always` and `.cursor/sync/rules/agents` copies are updated to match the new behavior for future tooling.
- **Step 7 – Testing / sanity checks (manual)**
  - Craft a small set of queue entries for each pipeline (INGEST_MODE, DISTILL_MODE, EXPRESS_MODE, ARCHIVE_MODE, ORGANIZE_MODE, RESUME_ROADMAP, RESEARCH_AGENT) and run EAT-QUEUE to verify:
    - Pipelines:
      - Run little val, then nested ValidatorSubagent, and only then return Success.
      - Return fields include `validator_context` (and optionally validator_first_pass) in their summary.
    - Queue:
      - On Success, invokes ValidatorSubagent a second time using `validator_context`.
      - Writes two distinct validation reports (one nested, one queue-driven) and Run-Telemetry with `actor: validator` for each.
      - Behaves correctly when nested vs queue-driven validator return conflicting severities (e.g., logs inconsistency, optionally marks run `#review-needed`).

