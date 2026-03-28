---
name: Complete validation wiring
overview: Design wiring so the Validator subagent can run often and liberally in auto mode across all main pipelines (ingest, organize, distill, express, archive, research, roadmap), while keeping roadmap_handoff as a protected high-stakes path.
todos:
  - id: wire-validate-mode
    content: Wire generic VALIDATE mode and validation_type-driven model selection in queue.mdc + Queue-Sources.md
    status: pending
  - id: extend-validator-branches
    content: Extend validator.mdc with branches for research_synthesis and other liberal validation types (ingest_classification, organize_path, distill_readability, express_summary, archive_candidate)
    status: pending
  - id: config-and-parameters-validator
    content: Update Second-Brain-Config.md and Parameters.md validator sections to list all validation types, models, and safety classes
    status: pending
  - id: pipeline-append-points
    content: Define where each main pipeline appends VALIDATE entries and gate with config flags
    status: pending
  - id: dev-docs-update
    content: Update dev docs (Queue-Sources, Cursor-Skill-Pipelines-Reference, Skills, Rules, Logs, Vault-Layout, Subagent-Safety-Contract) for complete Validator wiring
    status: pending
  - id: docs-subagent-list-entry
    content: Add a concise Validator entry to Docs/Subagents/Subagent-List.md without wiring details
    status: pending
isProject: false
---

# Complete validation wiring

## Goal and scope

- **Goal**: Treat Validator as a **cross-cutting quality layer** that can be invoked across **all main pipelines** — ingest, organize, distill, express, archive, research, roadmap — running **often** and **liberally** in **auto** mode where cost allows, while **protecting** high-stakes passes (e.g. roadmap handoff) as manual, fixed-model sweeps.
- **Scope**: Plan only. No edits yet. Focus on:
  - Validation **types** per pipeline.
  - **Queue modes** and when pipelines append them.
  - **Config** knobs (per-type model, aggressiveness, enable/disable flags).
  - **Outputs** and logging (where reports go).
  - Keeping user-facing `[3-Resources/Second-Brain/Docs]` clean; all wiring lives in dev docs and rules.

---

## 1. Validation types across pipelines (phased + layered roadmap)

Define a small, named set of `validation_type`s that map to concrete pipelines and outputs. All live under `validator.<validation_type>` in `[3-Resources/Second-Brain/Second-Brain-Config.md]` and in a Validator section of `[3-Resources/Second-Brain/Parameters.md]`.

- **Phase 1 (MVP, wire first)**:
  - `roadmap_handoff_auto` (new): auto-model validation of roadmap handoff readiness and structure, run **by the agent** during/after roadmap deepen/advance steps.
  - `research_synthesis` (liberal, auto; research pipeline).
  - One content-pipeline type, recommended: `distill_readability` (distill pipeline).
- **Phase 2 (follow-up wiring)**:
  - `ingest_classification`, `organize_path`, `express_summary`, `archive_candidate` and any later liberal types.
- **Roadmap (layered: auto + final)**:
  - `roadmap_handoff_auto`: auto-level validation; **Model**: `auto`; invoked via `VALIDATE` from the roadmap pipeline to keep roadmap state honest as it evolves.
  - `roadmap_handoff_final` (corresponds to today’s `roadmap_handoff` and `ROADMAP_HANDOFF_VALIDATE`): final, high-stakes sweep across the roadmap for user-triggered handoff validation; **Model**: fixed (`grok-code`); **manual-only** via `ROADMAP_HANDOFF_VALIDATE`.
- **Research (liberal, auto)**
  - `research_synthesis` (partially designed): hostile check over synthesized research notes.
  - **Model**: `auto`.
  - **Goal**: flag sourcing weakness, contradictions, overclaim, coverage gaps.
- **Ingest / organize (path + classification)**
  - `ingest_classification` (new): validate PARA classification and proposed path for an ingest note.
  - `organize_path` (new): validate organize moves/renames for non-Ingest notes.
  - **Model**: `auto` for both.
  - **Goal**: catch obviously wrong PARA type or path, or risky moves.
- **Distill (clarity / coverage)**
  - `distill_readability` (new): validate the distillation layers + TL;DR (clarity, coverage, readability).
  - **Model**: `auto`.
  - **Goal**: flag unreadable summaries, missing key points, overlong TL;DR, etc.
- **Express (messaging / structure)**
  - `express_summary` (new): validate express output (outline + call-to-action) for coherence and correctness.
  - **Model**: `auto`.
  - **Goal**: flag muddled narrative, mismatched CTA, misaligned audience.
- **Archive (safety / readiness)**
  - `archive_candidate` (new): validate that an archive move is safe (no open tasks, summary preserved, links sane).
  - **Model**: `auto`.
  - **Goal**: catch premature or unsafe archiving.

Each type gets:

- A **description** (Parameters, Config).
- A **default model** (`auto` vs fixed) and a **safety class** (high-stakes vs liberal).
- A **sink** (where Validator writes: report note vs log line).
- A **minimal hand-off schema** (see §3 and §5): required params, required input paths, and a clearly defined output sink.

---

## 2. Queue modes and wiring

Use two queue modes to keep things simple and explicit:

- `**ROADMAP_HANDOFF_VALIDATE` (existing)**
  - Dedicated to `validation_type: "roadmap_handoff"`.
  - Manual-only; fixed model; report path documented in Vault-Layout.
- `**VALIDATE` (general mode)**
  - **Always requires** `params.validation_type`.
  - Used for *all other* types: `research_synthesis`, `ingest_classification`, `organize_path`, `distill_readability`, `express_summary`, `archive_candidate`, and any future types.
  - For a queue entry `{ mode: "VALIDATE", params: { validation_type: "X", ... } }`:
    - Queue resolves **model** from `validator.X.model` in Config and passes it to the **Task** subagent tool for the validator subagent.
    - Queue builds a type-specific **hand-off**: validation_type, input paths, output sink, telemetry block.

**Queue rules to encode in `[3-Resources/Second-Brain/Queue-Sources.md]` and `[.cursor/rules/agents/queue.mdc]`:**

- Pipelines **MAY append `VALIDATE`** entries for any **liberal** type (`research_synthesis`, `ingest_classification`, `organize_path`, `distill_readability`, `express_summary`, `archive_candidate`).
- Pipelines **MUST NOT** append `ROADMAP_HANDOFF_VALIDATE` (manual-only) or `VALIDATE` with `validation_type: "roadmap_handoff"`.
- Canonical order in queue.mdc A.4 already has `ROADMAP_HANDOFF_VALIDATE` and `VALIDATE`; keep VALIDATE in the same “high-priority but not blocking” neighborhood.
- Known-mode list in auto-eat-queue includes **VALIDATE** so VALIDATE entries are never dropped as unknown.

---

## 3. Validator subagent behavior per type (schemas + severity)

Extend `[.cursor/rules/agents/validator.mdc]` (and legacy/sync equivalents) with branches matching the validation types. For each branch, define a **hand-off schema** and a **severity / action contract** that downstream pipelines can react to.

- Shared invariants:
  - **Read-only** on all inputs; one explicit **output sink** per type (report note or log line).
  - Hand-off parsing: `validation_type`, type-specific params, input paths, output sink, telemetry.
  - Return format: one-paragraph summary, output path (if any), explicit `Success` / `failure` / `#review-needed`.
  - **Severity + suggested action**: each report includes:
    - `severity: high | medium | low`.
    - `recommended_action: <short string>` (e.g. `create_wrapper`, `block_destructive`, `log_only`).
- Branches:
  - `roadmap_handoff`:
    - Existing roadmap report behavior (no change to logic), but make severity explicit (e.g. severity: high when handoff readiness is not met).
  - `research_synthesis`:
    - Inputs: project_id (when available) and explicit synthesized note paths (or a source_file from which they are derived).
    - Checks: sourcing strength, contradictions, overclaim, coverage.
    - Output: `.technical/Validator/research-validation-<timestamp>.md` (Phase 1 sink), plus severity + action suggestion (e.g. high / re-run research).
  - `ingest_classification` (Phase 2):
    - Inputs: original Ingest note path, proposed PARA type/path, competing candidates, ingest_conf.
    - Checks: PARA fit, path fit, high-risk moves (e.g. out-of-project moves).
    - Output: `.technical/Validator/ingest-validation-<timestamp>.md` + severity/action.
  - `organize_path` (Phase 2):
    - Inputs: note path, proposed new path, para-type, project-id, path_conf.
    - Checks: path coherence, hub/PMG/root protection, link impact.
    - Output: `.technical/Validator/organize-validation-<timestamp>.md` + severity/action.
  - `distill_readability` (Phase 1 content type):
    - Inputs: note path, distill layers and TL;DR (or the note from which they can be derived).
    - Checks: clarity, redundancy, missing obvious sections, reading difficulty; consider using existing readability metrics.
    - Output: `.technical/Validator/distill-validation-<timestamp>.md` + severity/action (e.g. medium / add #needs-simplify).
  - `express_summary` (Phase 2):
    - Inputs: express output (outline, CTA, Related section), note path and publishability signals.
    - Checks: messaging coherence, audience match, CTA quality.
    - Output: `.technical/Validator/express-validation-<timestamp>.md` + severity/action.
  - `archive_candidate` (Phase 2):
    - Inputs: note about to be archived (content, frontmatter, tasks, links, status, archive_conf).
    - Checks: open tasks, status flags, summary presence, potential sensitivity.
    - Output: `.technical/Validator/archive-validation-<timestamp>.md` + severity/action (e.g. high / block archive and create wrapper).

For each branch, specify in **Queue-Sources** and **Logs/Vault-Layout**:

- **Inputs** (paths, params) — required and optional.
- **Output path** and naming pattern — under `.technical/Validator/` or a well-defined log.
- Expected **severity + recommended_action** values so pipelines can map them to behavior.

---

## 4. When pipelines append VALIDATE (aggressive but controlled)

Wire Validator **per pipeline** with an “aggressive but bounded” strategy, governed by config flags per type and by a small central rate limiter.

### 4.1 Global rate limiting and profiles

- Add central Config knobs in `validator` block:
  - `validator.global_max_per_run` (e.g. max N VALIDATE entries appended per EAT-QUEUE pass).
  - `validator.global_sampling_rate` (e.g. validate 1 of every K eligible runs per type).
  - Optional per-project `validator_profile: "strong" | "normal" | "minimal"` that maps to:
    - strong → validate all eligible runs (subject to global_max_per_run).
    - normal → validate a sampled subset and/or only high-impact actions.
    - minimal → only run validator when explicitly queued by user/wrapper.

### 4.2 Ingest

- **Trigger (concrete)**: After Phase 2 apply-mode has computed `ingest_conf` and **before** move/rename:
  - If `validator.ingest_classification.enabled` AND `ingest_conf ≥ validator.ingest_classification.min_conf` AND no Decision Wrapper is being created, enqueue:
    - `mode: "VALIDATE"`, `params.validation_type: "ingest_classification"`, plus source_file, proposed_path, para_type, ingest_conf, candidate list.
- This is a **Phase 2** wiring (not required for MVP; see §1).

### 4.3 Organize

- **Trigger**: After autonomous-organize proposes a target path and `path_conf` AND before committing move:
  - If `validator.organize_path.enabled` AND
    - either note is a hub/PMG/root OR move crosses PARA root OR `validator.organize_path.scope == "all_high_conf"`,
    - append `VALIDATE` with `validation_type: "organize_path"`.

### 4.4 Distill (MVP content pipeline)

- **Trigger (Phase 1 MVP)**: After autonomous-distill completes and writes distill layers/TL;DR:
  - If `validator.distill_readability.enabled` AND
    - (`word_count > validator.distill_readability.min_words` OR `distill_conf` (if present) in a mid band),
    - append `VALIDATE` with `validation_type: "distill_readability"`.

### 4.5 Express

- **Trigger**: After autonomous-express writes outline/CTA:
  - If `validator.express_summary.enabled` AND note has `publish: true` **or** `approved: true`,
    - append `VALIDATE` with `validation_type: "express_summary"`.

### 4.6 Archive

- **Trigger**: Just before autonomous-archive moves a note to `4-Archives/` at high confidence:
  - If `validator.archive_candidate.enabled` AND `archive_conf ≥ validator.archive_candidate.min_conf`,
    - append `VALIDATE` with `validation_type: "archive_candidate"`.

### 4.7 Research (MVP liberal type)

- **Trigger (Phase 1 MVP)**: After `research-agent-run` writes synthesized notes:
  - If `validator.research_synthesis.enabled` AND `num_synthesis_notes ≥ validator.research_synthesis.min_notes`,
    - append `VALIDATE` with `validation_type: "research_synthesis"` and explicit synth note paths.

### 4.8 Roadmap (auto + final)

- **Auto layer (`roadmap_handoff_auto`)**:
  - Trigger: after roadmap-deepen or roadmap-advance-phase has updated phase notes and before marking phases complete or advancing `current_phase`.
  - If `validator.roadmap_handoff_auto.enabled`:
    - append `VALIDATE` with `validation_type: "roadmap_handoff_auto"` and inputs:
      - `project_id`, roadmap-state/workflow_state paths,
      - current phase number and its note paths,
      - decisions-log path when present.
  - Roadmap pipeline consumes validator severity + recommended_action:
    - **high** → treat like a failed refinement / recal signal: do not advance phase; create or update a Decision Wrapper or queue RECAL-ROAD as appropriate.
    - **medium** → log + `#handoff-needed` or similar flag; allow continuation if other gates pass.
    - **low** → informational only.
- **Final layer (`roadmap_handoff_final`)**:
  - No change to queue semantics: user (or Crafter/Commander) explicitly appends `ROADMAP_HANDOFF_VALIDATE` for final validation.
  - Internally, this continues to use the existing `roadmap_handoff` branch with fixed `grok-code` model and a single handoff-readiness report built over already auto-validated roadmap state.
  - Strictly **forbid** pipelines from appending `ROADMAP_HANDOFF_VALIDATE` or VALIDATE with `validation_type: "roadmap_handoff_final"` (the final sweep remains user-triggered only).

---

## 5. Config and Parameters

Update and centralize configuration in:

- `[3-Resources/Second-Brain/Second-Brain-Config.md]` → `validator` block:
  - Add sub-entries for each `validation_type` with:
    - `model` ("auto" for liberal types; fixed id for high-stakes).
    - Optional `enabled` (bool) when gating pipeline appends, plus type-specific thresholds (e.g. `min_conf`, `min_words`, `min_notes`).
  - Add global controls:
    - `validator.global_max_per_run`, `validator.global_sampling_rate`, and optional per-project `validator_profile`.
  - Example:
    - `validator.research_synthesis = { model: "auto", enabled: true, min_notes: 1 }`.
    - `validator.distill_readability = { model: "auto", enabled: true, min_words: 500 }`.
- `[3-Resources/Second-Brain/Parameters.md]` → Validator section:
  - Explain high-stakes vs liberal categories and their queue modes.
  - List each `validation_type`, its model, its queue mode, which pipeline(s) may append it, and its sink under `.technical/Validator/` or logs.
  - Document global controls (max_per_run, sampling, profiles) and the concrete triggers per pipeline (summarized from §4).

---

## 6. Dev docs and references

Update dev-facing docs (no changes to high-level user-facing Docs beyond a short Subagent entry):

- `[3-Resources/Second-Brain/Queue-Sources.md]`:
  - Document `VALIDATE` mode, required `params.validation_type`, and **per-type hand-off schemas** (required params, input paths, sinks).
  - Keep `ROADMAP_HANDOFF_VALIDATE` manual-only.
- `[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md]`:
  - Add VALIDATE pipeline row.
  - Update Validator row to list main validation types, which pipelines invoke them, and how severity maps to pipeline behavior.
- `[3-Resources/Second-Brain/Skills.md]`:
  - Add an entry summarizing Validator and its types, plus severity/action semantics.
- `[3-Resources/Second-Brain/Rules.md]`:
  - Add VALIDATE row mapping to validator; clarify that ROADMAP_HANDOFF_VALIDATE is one specific validator use.
- `[3-Resources/Second-Brain/Logs.md]` and `[3-Resources/Second-Brain/Vault-Layout.md]`:
  - Document `.technical/Validator/`* report files and any log-line sinks (e.g. Research-Log for validation summaries) per validation_type.
- `[3-Resources/Second-Brain/Subagent-Safety-Contract.md]`:
  - Confirm that validator runs with explicit `model` from `validator.<validation_type>.model` and remains read-only.
  - Clarify that validator **does not bypass** confidence bands, and that `Success`/`failure`/`#review-needed` + severity feed into the existing Error Handling / Decision Wrapper flows.

---

## 7. User-facing Docs (minimal)

- Update `[3-Resources/Second-Brain/Docs/Subagents/Subagent-List.md]` with a short entry:
  - Validator is a **general-purpose hostile reviewer**.
  - Runs in auto mode for many checks (research, ingest/organize/distill/express/archive) and has a special manual-only roadmap handoff check.
  - No mode lists or wiring; those live in dev docs.

---

## 8. Optional future refinements

- Add richer **severity tiers** and **action suggestions** in validator reports per type (e.g. severity: high + suggested action: rerun distill with lens X), possibly with structured JSON blocks for tooling.
- Introduce more nuanced **per-project** profiles for validator usage (beyond strict/normal/minimal), e.g. content-type-specific preferences.
- Add a **Decision Wrapper** mode for “validator disputes” where the user can accept/override a validator finding and feed that back into future runs (e.g. update config or per-note guidance).
- Add unit and integration tests (see Testing.md):\n  - Unit: hand-off → validator → single report file, per validation_type.\n  - Integration: pipeline run → VALIDATE entry → EAT-QUEUE dispatch → validator report + Run-Telemetry entry; ensure rate limits and severity handling behave as expected.\n

