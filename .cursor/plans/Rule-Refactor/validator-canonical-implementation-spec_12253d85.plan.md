---
name: validator-canonical-implementation-spec
overview: Define a canonical, two-phase implementation plan for the Validator subagent, including types, queue modes, schemas, safety contracts, and wiring across pipelines.
todos:
  - id: baseline-audit
    content: Audit current validator implementation and docs for roadmap_handoff and research_synthesis to ensure they match this spec’s baseline assumptions.
    status: completed
  - id: queue-mode-validate
    content: Extend Queue-Sources and queue dispatcher to add VALIDATE mode and route it to the validator subagent using validation_type and model from config.
    status: completed
  - id: validator-branch-updates-phase1
    content: Update validator agent to emit severity and recommended_action for existing types and to add the distill_readability branch following the canonical schema.
    status: completed
  - id: config-and-docs-phase1
    content: Add Phase 1 validator config keys (global limits and distill_readability) and update Validator-Reference plus related docs to describe Phase 1 behavior.
    status: completed
  - id: pipeline-triggers-phase1
    content: Wire research and distill pipelines to enqueue VALIDATE entries for research_synthesis and distill_readability under the configured conditions.
    status: completed
  - id: tests-phase1
    content: Create contract and end-to-end tests for VALIDATE(research_synthesis) and VALIDATE(distill_readability) and their pipeline triggers.
    status: completed
  - id: types-and-schemas-phase2
    content: Implement remaining validation types (ingest_classification, organize_path, express_summary, archive_candidate, roadmap_handoff_auto) with schemas, config, and validator branches.
    status: completed
  - id: pipeline-triggers-phase2
    content: Wire ingest, organize, express, archive, and roadmap pipelines to use VALIDATE for the new types, applying cost controls and sampling.
    status: completed
  - id: docs-and-observability-phase2
    content: Expand Validator-Reference and add telemetry/Dataview views for validator runs by type, pipeline, severity, and cost.
    status: completed
isProject: false
---

### Validator canonical implementation spec

### 1. Align with current reality and constraints

- **Confirm baseline types and behavior**: Verify existing `roadmap_handoff` and `research_synthesis` behavior in the Validator subagent and docs, including:
  - `ROADMAP_HANDOFF_VALIDATE` queue mode and its fixed Grok model from `validator.roadmap_handoff.model`.
  - `research_synthesis` activation from validator subagent (no queue mode yet), model from `validator.research_synthesis.model`, and output sink under `.technical/Validator/`.
- **Document non-negotiable invariants**: Re-state in this spec and cross-check that:
  - Validator is read-only on all inputs except its explicit output notes.
  - `roadmap_handoff` remains manual-only and high-stakes, with no auto-enqueue.

### 2. Define validator type model and taxonomy

- **Axis 1 — auto vs high-stakes**:
  - **Auto/liberal types**: Use `model: "auto"`, cost-controlled, safe to run frequently.
  - **High-stakes types**: Use fixed, strong model (Grok via `validator.<type>.model`), manual-only.
- **Axis 2 — existing vs future types**:
  - **Implemented today**: `roadmap_handoff` (high-stakes), `research_synthesis` (auto/liberal).
  - **Target set (canonical)**:
    - Roadmap-layered: `roadmap_handoff_final` (alias `roadmap_handoff`), `roadmap_handoff_auto`.
    - Research: `research_synthesis`.
    - Ingest/organize/distill/express/archive: `ingest_classification`, `organize_path`, `distill_readability`, `express_summary`, `archive_candidate`.
- **Lock the canonical list**: Treat this spec as the authoritative list of validation types; any new type must be added here first.

### 3. Queue modes and routing contract

- **Normalize to two modes**:
  - `**ROADMAP_HANDOFF_VALIDATE`** (existing):
    - Dedicated to `roadmap_handoff_final` / `roadmap_handoff` type.
    - Manual-only, fixed model from `validator.roadmap_handoff.model`.
  - `**VALIDATE`** (new):
    - General validator mode.
    - **Requires** `params.validation_type`.
    - Used for all auto/liberal types, including `research_synthesis`, `distill_readability`, `ingest_classification`, `organize_path`, `express_summary`, `archive_candidate`, and `roadmap_handoff_auto`.
- **Routing in queue processor** (queue/dispatcher agent and Queue-Sources):
  - `ROADMAP_HANDOFF_VALIDATE` → call subagent_type `validator` with `validation_type: "roadmap_handoff"` and `model` from config.
  - `VALIDATE` → call subagent_type `validator` with `validation_type` from params and `model` from `validator.<validation_type>.model` in config.
- **No additional validator-specific queue modes**: All validator behavior must flow through these two modes.

### 4. Canonical hand-off schemas per validation type

- **Generic schema fields per type**:
  - `required_params`: minimal required entries in queue `params`.
  - `required_inputs`: concrete note paths the validator must be able to read.
  - `output_sink`: deterministic path pattern for the report/verdict note.
- **Concrete schemas (authoritative)**:
  - `**roadmap_handoff_final` / `roadmap_handoff` (existing)**:
    - `required_params`: `{ project_id, roadmap_dir?, phase_range? }`.
    - `required_inputs`: `[roadmap-state, workflow_state, phase_notes, decisions_log?]`.
    - `output_sink`: `1-Projects/<project_id>/Roadmap/handoff-validation-report-<date>.md`.
  - `**research_synthesis` (existing)**:
    - `required_params`: `{ project_id?, source_file? }`.
    - `required_inputs`: `[synth_note_paths]` (explicit list from queue params).
    - `output_sink`: `.technical/Validator/research-validation-<timestamp>.md`.
  - `**distill_readability` (Phase 1)**:
    - `required_params`: `{ source_file }`.
    - `required_inputs`: `[source_file]` (distilled note path).
    - `output_sink`: `.technical/Validator/distill-validation-<timestamp>.md`.
  - `**ingest_classification` (Phase 2)**:
    - `required_params`: `{ source_file, para_type, proposed_path, ingest_conf }`.
    - `required_inputs`: `[source_file]`.
    - `output_sink`: `.technical/Validator/ingest-validation-<timestamp>.md`.
  - `**organize_path` (Phase 2)**:
    - `required_params`: `{ source_file, proposed_path, para_type, project_id, path_conf }`.
    - `required_inputs`: `[source_file]`.
    - `output_sink`: `.technical/Validator/organize-validation-<timestamp>.md`.
  - `**express_summary` (Phase 2)**:
    - `required_params`: `{ source_file, publish_flag? }`.
    - `required_inputs`: `[source_file]`.
    - `output_sink`: `.technical/Validator/express-validation-<timestamp>.md`.
  - `**archive_candidate` (Phase 2)**:
    - `required_params`: `{ source_file, archive_conf }`.
    - `required_inputs`: `[source_file]`.
    - `output_sink`: `.technical/Validator/archive-validation-<timestamp>.md`.
  - `**roadmap_handoff_auto` (Phase 2)**:
    - `required_params`: `{ project_id, phase?, phase_range? }`.
    - `required_inputs`: `[roadmap-state, workflow_state, phase_notes, decisions_log?]`.
    - `output_sink`: `.technical/Validator/roadmap-auto-validation-<timestamp>.md`.
- **Schema invariants**:
  - Queue-Sources, validator agent implementation, and Validator-Reference docs must all consume the same schemas from this spec.

### 5. Severity and behavior contract

- **Standard report envelope** (all types):
  - Every validator run must emit `severity: high|medium|low` and `recommended_action: string` (e.g. `"block_destructive"`, `"create_wrapper"`, `"log_only"`).
- **Pipeline behavior mapping**:
  - `**severity: high`**:
    - Treat as **failed refinement** for that note in that run.
    - Do **not** perform destructive actions (move/rename/archive/split/large overwrite).
    - Create or update a Decision Wrapper **or** mark the note `#review-needed` and log to Errors/Logs.
  - `**severity: medium`**:
    - May proceed with destructive actions only if all existing gates (confidence bands, snapshot, dry_run) are satisfied.
    - Must log the validator result and mark the note for review (e.g. `#review-needed` or equivalent frontmatter flag).
  - `**severity: low`**:
    - Informational; pipelines may record the result but are **not** required to change behavior.
- **Documentation alignment**:
  - Parameters, Validator-Reference, and pipeline docs must all describe this mapping and treat validator output as an additional safety signal layered on top of confidence-loops.

### 6. Safety integration with core guardrails

- **Non-bypassable safety**:
  - Validator **never bypasses** `core-guardrails` (backup, snapshot, dry_run) or `confidence-loops` (bands and refinement loop behavior).
- **Interaction rules**:
  - For a given pipeline + note + run:
    - A `high`-severity validator result is treated exactly like a refinement failure: no destructive step for that note in that run; Decision Wrapper or review flag is mandatory.
    - `medium`/`low` severities can influence routing and review but **cannot** downgrade confidence or skip snapshot/dry_run.
- **Spec propagation**:
  - Update `core-guardrails.mdc`, `confidence-loops.mdc`, and `Subagent-Safety-Contract.md` to reference validator as an input signal and to codify the `high/medium/low` handling.

### 7. Phase 1: minimal, implementable wiring

- **7.1 Types in scope (Phase 1)**:
  - Keep existing high-stakes: `roadmap_handoff_final` / `roadmap_handoff` via `ROADMAP_HANDOFF_VALIDATE`.
  - Keep existing liberal: `research_synthesis`.
  - Add one new auto/liberal content type: `distill_readability`.
- **7.2 Config changes (Phase 1)** in `3-Resources/Second-Brain/Second-Brain-Config.md`:
  - Ensure `validator.roadmap_handoff.model` and `validator.research_synthesis.model` exist and match current behavior.
  - Add global controls:
    - `validator.global_max_per_run` (e.g. 10–20).
    - `validator.global_sampling_rate` (e.g. 1.0 initially).
  - Add per-type config:
    - `validator.distill_readability = { model: "auto", enabled: false|true, min_words: 500 }`.
- **7.3 Queue-Sources changes (Phase 1)** in `3-Resources/Second-Brain/Queue-Sources.md`:
  - Add `VALIDATE` as a documented mode:
    - Require `params.validation_type`.
    - For Phase 1, only fully document schemas for `research_synthesis` and `distill_readability`.
  - Keep `ROADMAP_HANDOFF_VALIDATE` definition unchanged but confirm alignment with this spec.
- **7.4 Validator agent changes (Phase 1)** (e.g. `.cursor/rules/agents/validator.mdc` or equivalent):
  - Ensure existing branches for `roadmap_handoff` and `research_synthesis` include `severity` and `recommended_action` in their structured outputs.
  - Add a new `distill_readability` branch that:
    - Enforces the schema above.
    - Produces a readability-focused report and `severity` + `recommended_action`.
- **7.5 Pipeline triggers (Phase 1)**:
  - **Research pipeline**:
    - After `research-agent-run` writes synthesized notes to `Ingest/Agent-Research/`, when `validator.research_synthesis.enabled` (if present) and `num_synth_notes ≥ min_notes`, append a `VALIDATE` queue entry with `validation_type: "research_synthesis"`.
  - **Distill pipeline**:
    - After `autonomous-distill` completes, when `validator.distill_readability.enabled` and `word_count > min_words` (and/or optional mid-band conf gate), append `VALIDATE(distill_readability)`.
  - No other pipelines should enqueue `VALIDATE` in Phase 1.
- **7.6 Docs and tests (Phase 1)**:
  - Create/update `3-Resources/Second-Brain/Validator-Reference.md` to cover:
    - Types: `roadmap_handoff_final`, `research_synthesis`, `distill_readability`.
    - Their schemas, sinks, severity mapping, and examples.
  - Add minimal tests:
    - Contract tests for `VALIDATE(research_synthesis)` and `VALIDATE(distill_readability)` queue → validator → report flow.
    - One end-to-end test per Phase 1 pipeline (research, distill) verifying `VALIDATE` dispatch and correct report emission.

### 8. Phase 2: full general-use validator

- **8.1 New types (Phase 2 scope)**:
  - Add config, validator branches, schema docs, and examples for:
    - `ingest_classification`.
    - `organize_path`.
    - `express_summary`.
    - `archive_candidate`.
    - `roadmap_handoff_auto`.
- **8.2 Pipeline triggers (Phase 2)**:
  - Implement mode-appropriate triggers for all remaining pipelines (ingest, organize, express, archive, roadmap), using the schemas and severity mapping from this spec and the dedicated Phase 2 wiring plan (`validator_wiring_phase2_*.plan.md`).
  - Ensure all triggers enqueue `VALIDATE` with the correct `validation_type` and required params.
- **8.3 Cost controls and sampling (Phase 2)**:
  - Enforce `validator.global_max_per_run` in the queue dispatcher so that at most N `VALIDATE` entries are processed per EAT-QUEUE run.
  - Apply global and per-type sampling when appending `VALIDATE` entries (e.g. probability-based, threshold-based on confidence or size).
- **8.4 Docs and observability**:
  - Expand `Validator-Reference` to cover the full type set, with severity examples and sample reports.
  - Add Telemetry/Dataview slices for validator runs by type, pipeline, severity, and cost usage (e.g. total runs, high-severity rate, tokens per type).

### 9. Usage of this spec

- **Implementation sequence**:
  - Phase 1: implement exactly Section 7 (config additions, `VALIDATE` mode for `research_synthesis` and `distill_readability`, validator branches, pipeline triggers, tests, docs) while preserving current high-stakes behavior.
  - Phase 2: once Phase 1 is stable and validated, implement Section 8 to extend validator across all pipelines.
- **Documentation source of truth**:
  - Treat this plan as the canonical blueprint for Validator.
  - Keep `Validator-Reference` synchronized with it.
  - Ensure `Queue-Sources`, `Parameters`, `Rules`, and pipeline references are updated whenever Validator behavior or types change here.

