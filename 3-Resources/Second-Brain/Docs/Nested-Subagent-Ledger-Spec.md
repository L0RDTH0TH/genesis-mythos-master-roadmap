---
title: Nested Subagent Ledger Spec
created: 2026-03-22
tags: [second-brain, subagents, observability, roadmap]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]]"
  - "[[3-Resources/Second-Brain/Logs|Logs]]"
---

# Nested subagent ledger (spec)

**Version:** `ledger_schema_version: 1`

**Purpose:** Forensic, verbose trace of **Layer 2** nested `Task` calls (Validator, Internal Repair Agent, Research) and contract skips so operators can distinguish **Task tool rejection** (e.g. invalid `subagent_type`), **resource_exhausted**, **contract skip**, and **success** without inferring from missing validator files alone.

**Normative for:** Every **queue-dispatched** Layer 2 pipeline subagent that may invoke nested helpers (**Validator**, **IRA**, **Research**): **`ROADMAP_MODE`**, **`RESUME_ROADMAP`**, **`INGEST_MODE`**, **`ARCHIVE MODE`**, **`ORGANIZE MODE`**, **`DISTILL_MODE`** / **`BATCH_DISTILL`**, **`EXPRESS MODE`** / **`BATCH_EXPRESS`**, **`RESEARCH_AGENT`** / **`RESEARCH_GAPS`**. On **every** final return for those modes, include a fenced YAML block **`nested_subagent_ledger:`** per this spec — **never omit** when claiming **Success** with **`little_val_ok: true`** (unless a documented exempt subcase below uses explicit **`not_applicable`** rows).

**Exempt / explicit skip (still requires a ledger):** e.g. **Research** with **zero synthesized notes** — emit a single step with **`outcome: not_applicable`**, **`detail.reason_code: no_synthesis_skip_validator`**, and honest top-level flags; do **not** omit the block.

**Full schema reference:** This note. **Queue / Watcher behavior:** [[.cursor/rules/agents/queue.mdc|queue.mdc]] (embed ledger in `Watcher-Result` `trace`; soft `Errors.md` when missing on gated success).

---

## Sanitization (`host_error_raw`)

- Strip API keys, bearer tokens, long base64, and **optional** home-directory paths if your environment policy requires it.
- Preserve **Cursor / tool verbatim text** otherwise (enum error messages, `resource_exhausted`, etc.).

---

## Top-level object (`nested_subagent_ledger`)

| Field | Type | Required |
|-------|------|----------|
| `ledger_schema_version` | int | yes (currently `1`) |
| `pipeline` | string | yes — effective queue mode string, e.g. `ROADMAP_MODE` \| `RESUME_ROADMAP` \| `INGEST_MODE` \| `ARCHIVE MODE` \| `ORGANIZE MODE` \| `DISTILL_MODE` \| `BATCH_DISTILL` \| `EXPRESS MODE` \| `BATCH_EXPRESS` \| `RESEARCH_AGENT` \| `RESEARCH_GAPS` |
| `params_action` | string | yes — for Roadmap: effective action after smart-dispatch; for other pipelines: use **`-`** or the canonical mode / sub-action string when applicable |
| `material_state_change_asserted` | `true` \| `false` \| `unknown` | yes |
| `little_val_final_ok` | boolean | yes |
| `little_val_attempts` | int | yes |
| `ira_after_first_pass_effective` | boolean | yes |
| `nested_cycle_applicable` | boolean | yes |
| `steps` | array of step records | yes — ordered by execution |
| `pipeline_mode_used` | string | optional — `quality` \| `balance` \| `speed` from Layer 1 hand-off |
| `effective_profile_snapshot` | object | optional — echo of canonical profile keys for operator/debug |

---

## Step record (`steps[]`)

| Field | Type | Required |
|-------|------|----------|
| `step` | string | yes — stable id (see below) |
| `ordinal` | int | yes — 1-based |
| `started_iso` | string | yes — UTC ISO8601 |
| `ended_iso` | string | recommended |
| `duration_ms` | int | optional |
| `subagent_type` | string | yes — `research` \| `validator` \| `internal-repair-agent` \| `none` |
| `task_tool_invoked` | boolean | yes |
| `outcome` | string | yes — `invoked_ok` \| `skipped` \| `task_error` \| `not_applicable` \| `invoked_empty_ok` |
| `host_error_raw` | string | when `outcome: task_error` |
| `host_error_class` | string | when task_error — e.g. `invalid_enum`, `resource_exhausted`, `timeout`, `nested_task_unavailable`, `unknown` |
| `handoff_summary` | object | recommended — see below |
| `return_summary` | object | when `invoked_ok` or `invoked_empty_ok` — see below |
| `report_path` | string | optional — `-` when none |
| `detail` | object | yes — always; see below |

### Stable `step` ids (non-exhaustive)

- `research_pre_deepen` — nested Research before deepen (when applicable).
- `chain_research_consumed` — research from chain hand-off (no separate Task).
- `little_val_main` — structural little val for the run (skill; `subagent_type: none`).
- `little_val_post_ira` — little val after IRA apply in nested cycle.
- `little_val_driven_ira_N` — IRA on little-val failure path (N = 1..3 as applicable).
- `nested_validator_first` — first nested Validator pass (e.g. `roadmap_handoff_auto`, `ingest_classification`, `distill_readability`, `research_synthesis`, etc.).
- `ira_post_first_validator` — IRA after first nested validator when protocol runs.
- `nested_validator_second` — second nested pass with `compare_to_report_path`.
- `nested_cycle_exempt` — single row when entire nested Validator→IRA cycle is N/A with reason.
- `nested_validator_skipped_material_gate` — little val ok but nested cycle skipped for material-update policy.

### `handoff_summary` object

- `chars` — approximate hand-off character count passed to `Task`.
- `subagent_type_requested` — e.g. `validator`, `research`, `internal-repair-agent`.
- `validation_type` — when validator (e.g. `roadmap_handoff_auto`).
- `compare_to_report_path` — when second validator pass.
- `linked_phase` — when research.
- `model_passed_to_task` — Record what was passed to Cursor **Task**: **`omitted`** (no `model` key — parent session model), **`fast`** (`model: "fast"`), or the **explicit string** from Second-Brain-Config when supplied (e.g. validator). **Do not** use the literal `inherit` here as an API value — that string is invalid on Task calls (see Subagent-Safety-Contract § Cursor Task tool: `model` parameter).

### `return_summary` object (by helper)

- **Validator:** `severity`, `recommended_action`, `primary_code`, `report_path`.
- **IRA:** `suggested_fixes_count`, `ira_report_path`, `status`.
- **Research:** `synth_note_paths_count`, `injection_block_present` (bool).

### `detail` object (always)

- **`reason_code`** (machine): e.g. `contract_skip_material_gate`, `research_disabled_param`, `research_skipped_util_gate`, `legacy_clean_log_only_no_ira`, `little_val_failed_before_nested`, `task_enum_rejected`, `task_resource_exhausted`, `not_applicable_action`, `no_synthesis_skip_validator`, `ledger_invalid_invoked_ok_without_task`, `nested_helper_skip_without_task_attempt` (**invalid** — use only in strict-gate / operator diagnostics when a **required** step used **`skipped`** + **`task_tool_invoked: false`** without a real nested **`Task`** attempt; Layer 2 should instead emit **`task_error`** with **`host_error_class`** such as **`nested_task_unavailable`**).
- **`human_readable`** (1–3 sentences).
- Optional: `contract_citation`, `inputs_considered` (paths[]), `follow_up_effect`.

---

## Attestation invariants (mandated nested helpers)

These rules align the ledger with [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]]: Validator, IRA, and (when applicable) Research run as **nested Cursor `Task`** calls inside the pipeline subagent, not as silent “inline” simulation.

**Mandated helper `step` ids** — when the row is **not** a documented skip or N/A path below, the pipeline **must** have invoked the **`Task`** tool for the matching helper (`subagent_type` on the step record should match):

| `step` | Expected nested helper |
|--------|-------------------------|
| `nested_validator_first`, `nested_validator_second` | ValidatorSubagent (`validator`) |
| `ira_post_first_validator` | Internal Repair Agent (`internal-repair-agent`) |
| `research_pre_deepen` | ResearchSubagent (`research`) **only when** pre-deepen research is **attempted** this run and the run is **not** using chain hand-off consumables (use `chain_research_consumed` instead). |

**Forbidden (invalid attestation):** `outcome` is `invoked_ok` or `invoked_empty_ok` **and** `task_tool_invoked: false` **for any mandated helper `step` above** when that step was **required** for the branch (e.g. top-level `nested_cycle_applicable: true` and the nested Validator→IRA cycle ran). Operators and Layer 1 strict gates must treat this as **non-compliant**, not success.

**Forbidden (invalid attestation — skip without attempt):** `outcome` is **`skipped`** **and** `task_tool_invoked: false` on **`nested_validator_first`**, **`nested_validator_second`**, **`ira_post_first_validator`**, or **`research_pre_deepen`** when that step was **required** for this run and **`detail.reason_code`** is **not** on the allowlist below. Inspecting host **`available_functions`** (or equivalent) and emitting **`skipped`** without calling **`Task`** is **non-compliant**; the correct record is **`outcome: task_error`** with **`host_error_raw`** and **`host_error_class`** (e.g. **`nested_task_unavailable`**). **`nested_task_unavailable`** is a **`host_error_class`** value on **`task_error`** rows — **not** a free-form excuse on **`skipped`** rows.

**Allowlist for honest `skipped` + `task_tool_invoked: false` (non-exhaustive — must match pipeline contract):** e.g. **`legacy_clean_log_only_no_ira`**, **`pipeline_mode_medium_or_higher_ira_skipped`**, **`research_synthesis_light_skip`**, **`contract_skip_material_gate`**, **`unfreeze_conceptual_frontmatter_only`** (and equivalent material-gate / unfreeze-only paths), **`no_synthesis_skip_validator`**, **`research_skipped_util_gate`**, **`research_disabled_param`**, **`not_applicable_action`** when the step was genuinely out of scope; use **`chain_research_consumed`** instead of **`research_pre_deepen`** when chain consumables apply. For escalation documentation (not a skip excuse): **`profile_escalation_full_validation`** in **`detail.reason_code`** or return metadata when Layer 2 forces full path per [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]] §5.

**Per-step “required this run” (Layer 1 / operators):**

| Step | Treat as required when (heuristic) |
|------|-------------------------------------|
| `nested_validator_first` | `nested_cycle_applicable: true` and, for roadmap-style material policy, `material_state_change_asserted: true` when that field is **`true`** (omit check when `false`/`unknown` if pipeline did not assert material change). |
| `nested_validator_second`, `ira_post_first_validator` | `nested_cycle_applicable: true` **and** the nested Validator→IRA protocol applies (`ira_after_first_pass_effective: true` or first pass was not legacy clean `log_only` skip — align with pipeline agent); if uncertain, prefer strict gate when `nested_cycle_applicable: true` and first validator row was **`invoked_ok`**. |
| `research_pre_deepen` | Pre-deepen research was in scope for this run (pipeline enabled research, not chain **`chain_research_consumed`**, not explicit opt-out); if research was **not** required, **`not_applicable`** with documented **`reason_code`** is valid instead of **`skipped`**. |

**Allowed `task_tool_invoked: false` without `task_error`** for helper-shaped work only in **documented** cases:

- **`chain_research_consumed`** — use this **`step` id** (not `research_pre_deepen`) when `dependency_consumables.research` from a chain hand-off was consumed without a separate Research `Task` in this run.
- **`nested_validator_skipped_material_gate`**, **`nested_cycle_exempt`**, legacy IRA skip rows (`outcome: skipped` with e.g. `legacy_clean_log_only_no_ira`).
- **`not_applicable`** / **`skipped`** with explicit `detail.reason_code` and optional `contract_citation`.

**When nested `Task` cannot be invoked** (tool unavailable, enum rejection, timeout, etc.): use **`outcome: task_error`**, fill **`host_error_raw`** and **`host_error_class`** (e.g. `invalid_enum`, `resource_exhausted`, `nested_task_unavailable`, `unknown`). The pipeline **must not** return **Success** with **`little_val_ok: true`** if the safety contract still **required** that helper for this run and no valid exempt path applies.

---

## Run-Telemetry body (normative pipelines)

In the **Run-Telemetry** note for the pipeline run (roadmap, ingest, archive, organize, distill, express, research), after the usual summary content, include:

1. `## Nested subagent ledger`
2. `### Summary` — bullets: counts of `task_error`, `skipped`, `invoked_ok`, `nested_cycle_applicable`.
3. `### Steps (ordered)` — for each step, `#### {ordinal} — {step}` then bullet list of all non-empty fields (flatten nested objects).
4. `### Raw YAML (copy-paste)` — fenced yaml with full top-level `nested_subagent_ledger` object. If body size is large, cap **only** this subsection at ~12k chars and set `truncated: true` in a footer line; **do not** truncate the `####` per-step sections first.

---

## Examples (valid vs forbidden patterns)

These minimal examples illustrate how the attestation and proof-of-attempt rules are expected to appear in real ledgers.

### Example A — Valid ledger with mandatory validator run

```yaml
nested_subagent_ledger:
  ledger_schema_version: 1
  pipeline: RESUME_ROADMAP
  params_action: deepen
  material_state_change_asserted: true
  little_val_final_ok: true
  little_val_attempts: 1
  ira_after_first_pass_effective: true
  nested_cycle_applicable: true
  pipeline_mode_used: balance
  steps:
    - step: little_val_main
      ordinal: 1
      started_iso: "2026-04-03T23:10:01.000Z"
      ended_iso: "2026-04-03T23:10:01.500Z"
      subagent_type: none
      task_tool_invoked: false
      outcome: invoked_ok
      detail:
        reason_code: structural_check_ok
        human_readable: "little val structural check passed for this run."
    - step: nested_validator_first
      ordinal: 2
      started_iso: "2026-04-03T23:10:01.500Z"
      ended_iso: "2026-04-03T23:10:02.200Z"
      subagent_type: validator
      task_tool_invoked: true
      outcome: invoked_ok
      host_error_raw: ""
      host_error_class: ""
      handoff_summary:
        validation_type: roadmap_handoff_auto
        model_passed_to_task: omitted
      return_summary:
        severity: low
        recommended_action: log_only
        primary_code: "-"
        report_path: ".technical/Validator/roadmap-auto-validation-20260403T231000Z.md"
      detail:
        reason_code: validator_first_pass_complete
        human_readable: "First nested roadmap_handoff_auto validator pass completed cleanly."
```

This ledger is **valid** because:

- The helper graph/profile made `nested_validator_first` mandatory (roadmap, balance mode, `nested_cycle_applicable: true`).
- The validator step has `task_tool_invoked: true` and `outcome: invoked_ok`; a real `Task(validator)` call is implied and documented.
- There are no `skipped` / `not_applicable` rows for required steps without allowlisted reason codes.

### Example B — Forbidden ledger (skip without attempt on required validator)

```yaml
nested_subagent_ledger:
  ledger_schema_version: 1
  pipeline: RESUME_ROADMAP
  params_action: deepen
  material_state_change_asserted: true
  little_val_final_ok: true
  little_val_attempts: 1
  ira_after_first_pass_effective: false
  nested_cycle_applicable: true
  pipeline_mode_used: balance
  steps:
    - step: little_val_main
      ordinal: 1
      started_iso: "2026-04-03T23:10:01.000Z"
      ended_iso: "2026-04-03T23:10:01.500Z"
      subagent_type: none
      task_tool_invoked: false
      outcome: invoked_ok
      detail:
        reason_code: structural_check_ok
        human_readable: "little val structural check passed for this run."
    - step: nested_validator_first
      ordinal: 2
      started_iso: "2026-04-03T23:10:01.500Z"
      ended_iso: "2026-04-03T23:10:01.600Z"
      subagent_type: validator
      task_tool_invoked: false
      outcome: skipped
      detail:
        reason_code: helper_unavailable_but_not_attempted
        human_readable: "Validator was assumed unavailable and skipped without attempting Task."
```

This ledger is **forbidden** under the attestation and proof-of-attempt rules because:

- `nested_validator_first` is a **mandated** helper step for this run (`nested_cycle_applicable: true`, roadmap, balance mode).
- The row has `task_tool_invoked: false` and `outcome: skipped` with a non-allowlisted `reason_code`.
- No `task_error` row exists documenting a real `Task(validator)` failure (`host_error_class` / `host_error_raw`).

When a pipeline produces a ledger like this, Layer 2 must not claim Success with `little_val_ok: true`, and Layer 1 strict nested return gates must not consume the queue entry as a successful run. The correct shape, when the helper really cannot be invoked, is a `task_error` row with `host_error_class` (e.g. `nested_task_unavailable`) plus a non-successful overall status.

