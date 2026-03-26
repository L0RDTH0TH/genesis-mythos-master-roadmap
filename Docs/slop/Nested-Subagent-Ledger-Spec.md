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

**Normative for:** **RoadmapSubagent** on every `ROADMAP_MODE` and `RESUME_ROADMAP` return. **Recommended** for other pipeline subagents in a future rollout.

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
| `pipeline` | string | yes — `ROADMAP_MODE` \| `RESUME_ROADMAP` |
| `params_action` | string | yes — effective action after smart-dispatch |
| `material_state_change_asserted` | `true` \| `false` \| `unknown` | yes |
| `little_val_final_ok` | boolean | yes |
| `little_val_attempts` | int | yes |
| `ira_after_first_pass_effective` | boolean | yes |
| `nested_cycle_applicable` | boolean | yes |
| `steps` | array of step records | yes — ordered by execution |

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
| `host_error_class` | string | when task_error — e.g. `invalid_enum`, `resource_exhausted`, `timeout`, `unknown` |
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
- `nested_validator_first` — first `roadmap_handoff_auto` nested pass.
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

- **`reason_code`** (machine): e.g. `contract_skip_material_gate`, `research_disabled_param`, `research_skipped_util_gate`, `legacy_clean_log_only_no_ira`, `little_val_failed_before_nested`, `task_enum_rejected`, `task_resource_exhausted`, `not_applicable_action`.
- **`human_readable`** (1–3 sentences).
- Optional: `contract_citation`, `inputs_considered` (paths[]), `follow_up_effect`.

---

## Run-Telemetry body (RoadmapSubagent)

In the roadmap Run-Telemetry note, after the usual summary content, include:

1. `## Nested subagent ledger`
2. `### Summary` — bullets: counts of `task_error`, `skipped`, `invoked_ok`, `nested_cycle_applicable`.
3. `### Steps (ordered)` — for each step, `#### {ordinal} — {step}` then bullet list of all non-empty fields (flatten nested objects).
4. `### Raw YAML (copy-paste)` — fenced yaml with full top-level `nested_subagent_ledger` object. If body size is large, cap **only** this subsection at ~12k chars and set `truncated: true` in a footer line; **do not** truncate the `####` per-step sections first.

---

## Layer 1 `dispatch_ledger` (recommended)

One record per Queue-initiated `Task` in the EAT-QUEUE run:

- `ordinal`, `started_iso`, `ended_iso`
- `role`: `dispatch_pipeline` \| `post_little_val_validator` \| `prompt_craft_a5b` \| `prompt_craft_a5d` \| `empty_queue_bootstrap`
- `queue_entry_id`
- `subagent_type_requested`
- `outcome`: `invoked_ok` \| `task_error`
- `host_error_raw`, `host_error_class` when failed
- Optional: `pipeline_return_excerpt` (first ~500 chars) or `return_had_nested_ledger: true`

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1 | 2026-03-22 | Initial schema (roadmap-first). |
