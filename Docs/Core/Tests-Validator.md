---
title: Validator Tests
created: 2026-03-16
tags: [pkm, second-brain, validator, tests]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Validator-Reference]]","[[3-Resources/Second-Brain/Queue-Sources]]","[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec]]"]
---

## Phase 1 — contract tests

- **VALIDATE(research_synthesis)**:
  - **Given** a queue line in `.technical/prompt-queue.jsonl`:
    - `{"mode":"VALIDATE","id":"val-1","params":{"validation_type":"research_synthesis","project_id":"test-project","synth_note_paths":["Ingest/Agent-Research/Synth-1.md"]}}`
  - **When** EAT-QUEUE dispatches the entry:
    - It must route to the ValidatorSubagent with `validation_type: "research_synthesis"` and model from `validator.research_synthesis.model`.
    - Validator must write a report under `.technical/Validator/research-validation-<timestamp>.md`.
    - The report (and return payload) must include:
      - `severity` and `recommended_action`,
      - non-empty `reason_codes`,
      - non-empty `next_artifacts`,
      - required `potential_sycophancy_check`,
      - `gap_citations` with mandatory verbatim snippets supporting each `reason_code`.

- **VALIDATE(distill_readability)**:
  - **Given** a queue line:
    - `{"mode":"VALIDATE","id":"val-2","source_file":"1-Projects/Test/Note.md","params":{"validation_type":"distill_readability"}}`
  - **When** EAT-QUEUE dispatches the entry:
    - It must route to the ValidatorSubagent with `validation_type: "distill_readability"` and model from `validator.distill_readability.model`.
    - Validator must write a report under `.technical/Validator/distill-validation-<timestamp>.md`.
    - The report (and return payload) must include:
      - `severity` and `recommended_action`,
      - non-empty `reason_codes`,
      - non-empty `next_artifacts`,
      - required `potential_sycophancy_check`,
      - `gap_citations` with mandatory verbatim snippets supporting each `reason_code`.

- **VALIDATE(roadmap_handoff_auto) — coherent but underspecified → needs_work (non-blocking)**:
  - **Given** a queue line:
    - `{"mode":"VALIDATE","id":"val-3","params":{"validation_type":"roadmap_handoff_auto","project_id":"test-project","roadmap_level":"tertiary"}}`
  - **And** the test project’s Phase 1 artifacts are coherent but missing concrete handoff artifacts (ports/schemas/worked example/task decomposition).
  - **When** EAT-QUEUE dispatches the entry:
    - It must route to the ValidatorSubagent with `validation_type: "roadmap_handoff_auto"` and model from `validator.roadmap_handoff_auto.model`.
    - The report (and return payload) must include:
      - `severity: medium`
      - `recommended_action: needs_work`
      - non-empty `reason_codes`
      - non-empty `next_artifacts`
      - required `potential_sycophancy_check`
      - `gap_citations` with verbatim snippets for each `reason_code`

- **VALIDATE(roadmap_handoff_auto) — anti-dulling final pass regression guard**:
  - **Given** two validator report notes for the same project:
    - an initial validator report at `compare_to_report_path`
    - the current artifacts/state after a “repair attempt”
  - **When** a validator run is invoked with `compare_to_report_path` present in the hand-off:
    - the final pass must compare directly to the initial report
    - if it omits/reduces any initial `reason_codes`, or weakens/shortens `next_artifacts`, it must force `recommended_action: needs_work` (or higher severity)
    - the final report must include explicit evidence of “dulling/softening” via verbatim gap citations

- **VALIDATE(roadmap_handoff_auto) — true block → block_destructive**:
  - **Given** a queue line:
    - `{"mode":"VALIDATE","id":"val-4","params":{"validation_type":"roadmap_handoff_auto","project_id":"test-project","roadmap_level":"tertiary"}}`
  - **And** the artifacts include contradictions or safety-critical ambiguity (plan is not reliably restatable / multiple incompatible truth sources with no reconciliation path).
  - **When** EAT-QUEUE dispatches the entry:
    - The report must set:
      - `severity: high`
      - `recommended_action: block_destructive`
    - The report must include `reason_codes` containing at least one of:
      - `contradictions_detected`
      - `state_hygiene_failure`
      - `safety_critical_ambiguity`
    - The report must also include `potential_sycophancy_check` and `gap_citations`.

## Phase 1 — end-to-end tests

- **Research pipeline → VALIDATE(research_synthesis)**:
  - Run a RESEARCH_AGENT queue entry for a test project/phase.
  - Confirm:
    - `research-agent-run` created synthesis notes under `Ingest/Agent-Research/`.
    - EAT-QUEUE appended and then processed a VALIDATE entry with `validation_type: "research_synthesis"` when Config `validator.research_synthesis.enabled` is true and `min_notes` is satisfied.
    - A `.technical/Validator/research-validation-<timestamp>.md` report exists with `severity` and `recommended_action`, and includes `reason_codes`, `next_artifacts`, `gap_citations`, and `potential_sycophancy_check`.

- **Distill pipeline → VALIDATE(distill_readability)**:
  - Run DISTILL MODE on a sufficiently long note (word count > `validator.distill_readability.min_words`) with `validator.distill_readability.enabled: true`.
  - Confirm:
    - DistillSubagent completed normally (highlight, TL;DR, readability-flag).
    - A VALIDATE(distill_readability) queue entry was appended.
    - After EAT-QUEUE, a `.technical/Validator/distill-validation-<timestamp>.md` report exists with `severity` and `recommended_action`, and includes `reason_codes`, `next_artifacts`, `gap_citations`, and `potential_sycophancy_check`.

- **Validator-to-IRA single-cycle enforcement (default `ira_after_first_pass: true`)**:
  - **Case A — non-clean first pass:** **Given** a known-gap artifact for one of: `INGEST_MODE`, `ARCHIVE_MODE`, `ORGANIZE_MODE`, `DISTILL_MODE`, `EXPRESS_MODE`, `RESUME_ROADMAP`, or `RESEARCH_AGENT` that triggers the pipeline’s nested hostile validator to return **any non–clean** first pass (e.g. `needs_work`, `high`, `block_destructive`, or actionable gaps — not a clean `log_only` with no gaps). **When** EAT-QUEUE processes the entry: the pipeline must invoke IRA exactly once, apply one repair cycle (any `risk_level` when gates allow), run the nested validator a second time with `compare_to_report_path`, and must not invoke IRA again even if the final pass still returns `needs_work`. **Confirm:** one `...-ira-call-1-<queue_entry_id>.md` for the validator branch (not `ira-call-2`/`ira-call-3` for that cycle); final report notes regression/softening vs initial.
  - **Case B — clean first pass with default policy:** **Given** an artifact where the **first** nested validator returns clean `log_only` with no actionable gaps, with Config `nested_validator.ira_after_first_pass: true` and no `params.ira_after_first_pass: false`. **Expect** the pipeline still runs **one** IRA invocation (may produce empty `suggested_fixes`), then second validator with `compare_to_report_path` (and little val between them for CODE pipelines). **Legacy:** with effective `ira_after_first_pass: false`, clean first pass **skips** IRA and second validator.

- **Queue continues after light-success**:
  - Ensure that when final nested validator still returns `needs_work`, the queue processing continues to subsequent entries (i.e. the original entry is cleared from `.technical/prompt-queue.jsonl` and later ids are processed).

## Phase 2 — tiered blocks and Layer 1 pivot

- **`primary_code` precedence:** When the validator emits multiple `reason_codes`, confirm the report and return payload set **`primary_code`** per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] §2 (e.g. `state_hygiene_failure` wins over `safety_unknown_gap`).
- **`safety_unknown_gap` vs `safety_critical_ambiguity`:** Fixture where scope is merely underspecified → `needs_work` / medium / `safety_unknown_gap` allowed; fixture where automation would compound dual-truth → high / `block_destructive` / `safety_critical_ambiguity`.
- **Tiered nested Success:** With **`validator.tiered_blocks_enabled: true`**, pipeline may return **Success** after final nested pass when verdict is **`needs_work`** without high/block; must **not** return Success when **`severity: high`** or **`recommended_action: block_destructive`** or hard-block **`primary_code`** set.
- **Post–little-val hard block → repair line:** Run **RESUME_ROADMAP** deepen (or chain primary) until post–little-val returns hard block with `contradictions_detected`; confirm **queue.mdc A.5b** appends a line with **`queue_priority: "repair"`** or **`validator_repair_followup: true`**, **`params.action`** in `recal` / `handoff-audit`, and that the **original** entry id is in **`processed_success_ids`** while the new line remains in the file.
- **Repair-before-deepen sort:** Queue two lines for the same **`project_id`**: one **`deepen`**, one **repair** (flags as above). After sort (**A.4**), **repair** must be ordered **before** **deepen** for that project in the same pass (unless per-project serialism keeps one undispatchable).

