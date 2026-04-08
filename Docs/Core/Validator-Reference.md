---
title: Validator Reference
created: 2026-03-16
tags: [pkm, second-brain, validator]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Second-Brain-Config]]","[[3-Resources/Second-Brain/Queue-Sources]]","[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"]
---

## Validator types and queue modes

- **High-stakes (manual-only)**:
  - **roadmap_handoff_final** (alias: `roadmap_handoff`).
    - **Queue mode**: `ROADMAP_HANDOFF_VALIDATE`.
    - **Model**: `validator.roadmap_handoff.model` (fixed, e.g. `grok-code`).
- **Liberal / auto types (Phase 1)**:
  - **research_synthesis**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "research_synthesis"`.
    - **Model**: `validator.research_synthesis.model` (typically `"auto"`).
  - **distill_readability**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "distill_readability"`.
    - **Model**: `validator.distill_readability.model` (auto).
- **Liberal / auto types (Phase 2)**:
  - **ingest_classification**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "ingest_classification"`.
    - **Model**: `validator.ingest_classification.model` (auto).
  - **organize_path**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "organize_path"`.
    - **Model**: `validator.organize_path.model` (auto).
  - **express_summary**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "express_summary"`.
    - **Model**: `validator.express_summary.model` (auto).
  - **archive_candidate**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "archive_candidate"`.
    - **Model**: `validator.archive_candidate.model` (auto).
  - **roadmap_handoff_auto**.
    - **Queue mode**: `VALIDATE` with `params.validation_type: "roadmap_handoff_auto"`.
    - **Model**: `validator.roadmap_handoff_auto.model` (auto).
  - **roadmap_mirror_integrity** (optional / reserved).
    - **Queue mode**: `VALIDATE` with `params.validation_type: "roadmap_mirror_integrity"`.
    - **Model**: `validator.roadmap_mirror_integrity.model` when present in Second-Brain-Config (otherwise treat as **not yet implemented** — ValidatorSubagent may return advisory-only or `log_only`).
    - **Purpose**: Check **`conceptual_counterpart`** / **`execution_mirror`** pairs, folder shape under `Roadmap/Execution/`, and reverse-link consistency for dual-track projects. See [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
  - **recovery_outcome** (post–PromptCraft recovery).
    - **Queue mode**: `VALIDATE` with `params.validation_type: "recovery_outcome"`.
    - **Model**: `validator.recovery_outcome.model` (typically `"auto"`).
    - **When**: After Layer 1 has appended PromptCraft-suggested lines and EAT-QUEUE has run the recovery package — answers whether the **original failure** (before state vs after state) is resolved.

All validator runs are dispatched via either `ROADMAP_HANDOFF_VALIDATE` (roadmap_handoff_final) or `VALIDATE` (all other types).

## Hand-off schemas (canonical)

- **roadmap_handoff_final / roadmap_handoff**:
  - **required_params**: `{ project_id, roadmap_dir?, phase_range?, roadmap_level? }`.
  - **required_inputs**: `[roadmap-state, workflow_state, phase_notes, decisions_log?]`.
  - **output_sink**: `1-Projects/<project_id>/Roadmap/handoff-validation-report-<date>.md`.

- **research_synthesis**:
  - **required_params**: `{ project_id?, source_file? }`.
  - **required_inputs**: `[synth_note_paths]` (explicit list passed in hand-off).
  - **output_sink**: `.technical/Validator/research-validation-<timestamp>.md`.

- **distill_readability**:
  - **required_params**: `{ source_file }`.
  - **required_inputs**: `[source_file]` (distilled note).
  - **output_sink**: `.technical/Validator/distill-validation-<timestamp>.md`.

- **ingest_classification**:
  - **required_params**: `{ source_file, proposed_path, para_type, ingest_conf }`.
  - **required_inputs**: `[source_file]` (ingest note at its current or proposed location).
  - **output_sink**: `.technical/Validator/ingest-validation-<timestamp>.md`.

- **organize_path**:
  - **required_params**: `{ source_file, proposed_path, para_type, project_id?, path_conf }`.
  - **required_inputs**: `[source_file]` (note being organized).
  - **output_sink**: `.technical/Validator/organize-validation-<timestamp>.md`.

- **express_summary**:
  - **required_params**: `{ source_file, publish_flag? }`.
  - **required_inputs**: `[source_file]` (expressed note).
  - **output_sink**: `.technical/Validator/express-validation-<timestamp>.md`.

- **archive_candidate**:
  - **required_params**: `{ source_file, archive_conf }`.
  - **required_inputs**: `[source_file]` (note considered for archive).
  - **output_sink**: `.technical/Validator/archive-validation-<timestamp>.md`.

- **roadmap_handoff_auto**:
  - **required_params**: `{ project_id, roadmap_dir?, phase_range?, roadmap_level? }`.
  - **required_inputs**: `[roadmap-state, workflow_state, phase_notes, decisions_log?]` (same set as roadmap_handoff, but used in lighter-weight auto runs).
  - **output_sink**: `.technical/Validator/roadmap-auto-validation-<timestamp>.md`.

- **roadmap_mirror_integrity**:
  - **required_params**: `{ project_id, roadmap_dir?, execution_subfolder? }`.
  - **required_inputs**: Execution + conceptual phase notes as listed in hand-off; read-only.
  - **output_sink**: `.technical/Validator/roadmap-mirror-integrity-<timestamp>.md` (conventional; adjust when implementation lands).

- **recovery_outcome**:
  - **required_params**: `{ error_correlation_id, failure_envelope_ref | failure_envelope_inline, crafted_lines_ref | crafted_lines_inline, before_snapshot_paths[], after_state_paths[] }` — hand-off must carry enough to compare **before** vs **after** (paths to workflow_state, roadmap-state, Errors tail, validator reports, or inline excerpts). `crafted_lines_ref` may point at PromptCraft return / queue append log.
  - **required_inputs**: Read-only: artifacts listed in hand-off (no mutation).
  - **output_sink**: `3-Resources/Second-Brain/Validator-Reports/recovery_outcome/<correlation-id-or-slug>-<timestamp>.md`.
  - **Verdict question:** Did the recovery **clear** the original failure class (structural, validator hard block, missing artifact, etc.)? Emit `recovery_effective: true|false|partial`, `severity`, `recommended_action`, `reason_codes`, `next_artifacts`, `potential_sycophancy_check`, and explicit citations comparing before vs after.

## Roadmap altitude model (primary / secondary / tertiary)

Roadmap validations (`roadmap_handoff_final`/`roadmap_handoff` and `roadmap_handoff_auto`) are **altitude-aware**.

- **roadmap_level (canonical, optional)**: `"primary" | "secondary" | "tertiary"`.
  - **If provided in params**: validator uses it directly.
  - **If omitted**: validator attempts to infer it from the validated phase roadmap note frontmatter key `roadmap-level` (hyphen). If it still cannot determine level, it defaults conservatively (treat as `"secondary"` and explicitly notes it defaulted).

### What the validator demands at each altitude

- **primary**:
  - Demand decomposition and “secondary roadmap stubs” (named workstreams/subsystems), roll-up gates back to primary outcomes, and explicit decision anchors.
  - Avoid demanding tertiary artifacts (full interface specs / test plan) unless the primary phase explicitly claims implementation handoff readiness.
- **secondary**:
  - Demand subsystem boundary clarity, interface sketch, testable acceptance criteria, mapping to primary gates, and risk register v0.
- **tertiary**:
  - Demand executable artifacts: concrete interface specs, test plan, task breakdown, explicit decisions logged, and risk register v0.

Future extensions must be added here and in the canonical Validator implementation spec before use.

## Severity and recommended_action contract

Every validator run, for every validation_type, must produce:

- **severity**: one of `high`, `medium`, `low`.
- **recommended_action**: short string such as:
  - `"block_destructive"` — treat as failed refinement for this note in this run; do not perform destructive actions.
  - `"needs_work"` — coherent output, but not delegatable yet; proceed only with non-destructive next steps and produce missing artifacts.
  - `"create_wrapper"` — create/update a Decision Wrapper for this note.
  - `"log_only"` — record the finding, but no mandatory behavior change.

## Anti-sycophancy / anti-agreeability hardened schema (validator-to-IRA)

For validator runs that may participate in a validator-to-IRA repair cycle (including the pipeline’s final hardened post-IRA validator pass), the validator report and return payload must also include:

- **reason_codes**: closed-set list of canonical stable identifiers.
- **gap_citations**: mandatory verbatim short quote/snippet citations from the validated artifacts, mapped to each `reason_code`.
- **next_artifacts**: checklist of concrete artifacts with definition-of-done.
- **potential_sycophancy_check**: required field explicitly stating whether the validator felt tempted to downplay any gap (set `true` if any temptation/softening pressure was detected).

## Final-pass regression guard

When the hand-off includes `compare_to_report_path` (the first validator report), the final pass must compare directly and must NOT soften/regress:

- Any omitted/reduced `reason_codes`, weakened/shortened `next_artifacts`, or lower/lower-strictness `severity` / `recommended_action` must be treated as “dulling” and force `recommended_action: "needs_work"` (or higher severity if appropriate).

### Roadmap handoff: what is a true BLOCK?

For roadmap handoff validation types (`roadmap_handoff_final` / `roadmap_handoff` and `roadmap_handoff_auto`):

**Canonical feature spec:** [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] (definitions, `reason_codes`, `primary_code`, action matrix, scoped blocks, repair-first, chains).

- **`block_destructive` / severity: high** MUST be reserved for true block situations only:
  - **Contradictions** (`contradictions_detected`): phase vs phase, phase vs state, or phase vs master-goal — plan non-executable until reconciled.
  - **Safety-critical ambiguity** (`safety_critical_ambiguity`): risk of destructive thrash; not the same as **`safety_unknown_gap`** (floating deferrals / weak traceability → usually **medium** + `needs_work`).
  - **Incoherence** (`incoherence`): validator cannot reliably restate system boundaries and responsibilities without guessing (see spec §1.1).
  - **State hygiene failure** (`state_hygiene_failure`): conflicting canonical truth or severe hygiene invalidating automation decisions.

- **Missing artifacts alone** (ports/schemas/examples/task breakdown) is **not** a true block. It MUST be reported as:
  - **severity: medium** and **recommended_action: `needs_work`**, plus a concrete “what to write next” checklist.

**Tiered pipeline Success:** After the **final** nested validator pass, pipelines may return **Success** when the verdict is **`needs_work`** (and little val ok) **without** `severity: high` or `recommended_action: block_destructive`. Hard block only when high / `block_destructive` or primary_code in the block rows of the spec matrix.

### Roadmap handoff: required structure for actionable guidance

For roadmap handoff validation types, validator reports MUST include:

- **reason_codes**: stable identifiers (e.g. `missing_port_signatures`, `missing_message_flow_example`, `missing_command_event_schemas`, `missing_task_decomposition`, `contradictions_detected`, `state_hygiene_failure`, `safety_critical_ambiguity`, `safety_unknown_gap`, `incoherence`). When multiple codes apply, emit **`primary_code`** per Validator-Tiered-Blocks-Spec §2.
- **next_artifacts**: a checklist of concrete artifacts with definition-of-done (so the next deepen/audit knows exactly what to add).

### Pipeline behavior mapping

- **severity: high**:
  - Equivalent to a failed refinement for that note in that run.
  - **Do not** perform destructive actions (move/rename/split/archive/large overwrite).
  - Pipelines must either:
    - Create/update a Decision Wrapper, or
    - Mark the note `#review-needed` and log in the appropriate log + `Errors.md`.

- **severity: medium**:
  - Destructive actions may proceed **only** if existing gates pass (confidence bands, snapshot, dry_run).
  - Pipelines must log the validator result and mark the note for review (`#review-needed` or equivalent).

- **severity: low**:
  - Informational; pipelines may record the result but are not required to change behavior.

Validator never bypasses `core-guardrails.mdc` or `confidence-loops.mdc`; it only adds another safety signal. When invoked **nested inside a pipeline subagent**, its severity / recommended_action participate in that pipeline’s Success gate. When invoked **from the queue** (ROADMAP_HANDOFF_VALIDATE, VALIDATE, or post-pipeline double-check), it acts as an independent hostile reviewer and must remain read-only on inputs.

## Observability and Dataview hints

- **Run-Telemetry**:
  - Every validator run writes a Run-Telemetry note under `.technical/Run-Telemetry/` with `actor: validator`, `project_id`, `queue_entry_id`, `timestamp`, and (optionally) `model`, `validation_type`, `severity`, `recommended_action`.
  - Dataview tables can aggregate validator activity by type, model, and severity.

- **Suggested Dataview queries** (pseudo-code):
  - **Runs by type and severity**:
    - Table `validation_type`, `severity`, `recommended_action`, `model`, `file.link` over `.technical/Run-Telemetry/` where `actor = "validator"`.
  - **High-severity hotspots**:
    - List or table high-severity runs grouped by `validation_type` and `project_id` to see which projects or pipelines need attention.

Global cost controls:

- `validator.global_max_per_run` caps how many VALIDATE / ROADMAP_HANDOFF_VALIDATE entries EAT-QUEUE will dispatch in a single run.
- `validator.global_sampling_rate` governs how often pipelines append new VALIDATE entries; pipelines should treat it as a probability gate when deciding whether to enqueue a validator run.

