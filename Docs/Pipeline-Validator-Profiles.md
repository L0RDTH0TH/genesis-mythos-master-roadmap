---
title: Pipeline validator profiles (speed / quality tiers)
created: 2026-03-29
tags: [second-brain, validator, queue, roadmap, config]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Parameters|Parameters]]"
  - "[[3-Resources/Second-Brain-Config|Second-Brain-Config]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference|Subagent-Layers-Reference]]"
---

# Pipeline validator profiles

## Purpose

`pipeline_mode` selects a **validator profile**: a small bundle of policies for **Layer 1** post–little-val validation, **Layer 2** nested Validator→IRA→compare behavior, and **research synthesis** depth. One Config knob (with optional per-queue `params.pipeline_mode`) replaces scattered booleans.

**Canonical spec:** profile rows use only the keys in §2. **Machine merge:** Queue resolves the profile and emits **`effective_profile_snapshot`** inside **`layer1_resolver_hints`** (RESUME_ROADMAP / chains) or **`## effective_pipeline_profile`** (ROADMAP_MODE). Roadmap and Research subagents **must** honor the snapshot; they must not re-interpret Config independently.

**Hard invariants (all modes):** Little-val structural gate remains mandatory where the pipeline contract requires it; **Validator-Tiered-Blocks-Spec** hard blocks (`state_hygiene_failure`, `contradictions_detected`, `incoherence`, `safety_critical_ambiguity`, `severity: high`, `recommended_action: block_destructive`) are never ignored; backups, snapshots, and the ≥85% destructive gate per core guardrails stay in force.

---

## 1. Resolution order

1. If merged queue entry has valid **`params.pipeline_mode`** ∈ `quality` | `balance` | `speed`, use it.
2. Else use top-level **`pipeline_mode`** from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] (default **`balance`**).
3. Else treat as **`balance`**.
4. Load **`validator_profiles[pipeline_mode]`** from Config. If the key is missing, use **`validator_profiles.balance`**.

---

## 2. Canonical profile keys

| Key | Values | Meaning |
|-----|--------|---------|
| **`l1_post_lv_policy`** | `always` | After every successful roadmap-class pipeline return with `little_val_ok` and valid `validator_context`, Queue runs Layer 1 post–little-val **`Task(validator)`** (existing A.5 b1), including Pass 3 inline / inline_forward. |
| | `conditional_nonhard_skip` | On **`queue_pass_phase`** `inline` or `inline_forward` only: **skip** L1 post–little-val if the **prior** L1 outcome for the same `project_id` **in this EAT-QUEUE run** was **non-hard** (needs-work-only). If there was no prior L1 for that project in the run, **run** L1. If prior L1 was **hard**, **run** L1. |
| | `minimal` | **Skip** L1 post–little-val on any follow-on roadmap dispatch for that `project_id` in the run **unless** the prior L1 was **hard** **or** this is the **first** completed roadmap dispatch for that `project_id` in the run. |
| **`nested_ira_policy`** | `always` | After first nested `roadmap_handoff_auto` when the nested cycle applies: always run Validator → IRA → little val → second Validator (compare), even if the first pass is clean `log_only`. |
| | `clean_skip` | **Legacy / balance:** If the first nested pass is clean `log_only` with no actionable gaps, **skip** IRA and second validator; otherwise full cycle. Equivalent to **`nested_validator.ira_after_first_pass: false`** when no finer policy exists. |
| | `medium_or_higher` | **Speed:** Run IRA and second/compare **only** if the first nested validator has `severity` ≥ `medium`, or `recommended_action` ≠ `log_only`, or non-empty actionable `reason_codes` / gaps (not clean advisory-only). |
| **`research_synthesis_depth`** | `full` | Full `research_synthesis` cycle when synthesis exists (Validator → IRA → second compare per Research agent contract). |
| | `light` | Narrower first-pass hand-off (consistency + key facts); escalate to full per §4 when triggers fire. |
| | `fast` | Lightest hand-off; full cycle only on safety escalation (§5) or explicit param. |
| **`target_nested_validator_passes`** | int | Soft budget / telemetry expectation (e.g. 4 / 2 / 2). **Does not** override §5. |

**Balance-only optional keys** (under `validator_profiles.balance` in Config; copied into `effective_profile_snapshot`):

- **`research_full_every_n_runs`** — force full research synthesis every Nth successful research run per `project_id` (default **3**; **4** in `speed` profile for slightly fewer deep passes).
- **`research_full_if_run_confidence_below`** — force full when run/hand-off confidence is **strictly below** this integer percent (default **80** balance, **75** speed profile table).
- **`research_full_if_prior_roadmap_validator_stronger_than_log_only`** — when **true**, force full if the preceding roadmap nested or L1 validator was stronger than `log_only` (e.g. `needs_work`, `medium`, actionable `next_artifacts`).

Numeric thresholds are duplicated for operator visibility in [[3-Resources/Second-Brain/Parameters|Parameters]] § Pipeline validator profiles.

---

## 3. Mode → default row

| `pipeline_mode` | `l1_post_lv_policy` | `nested_ira_policy` | `research_synthesis_depth` | `target_nested_validator_passes` |
|-----------------|---------------------|---------------------|-----------------------------|----------------------------------|
| **quality** | `always` | `always` | `full` | 4 |
| **balance** | `conditional_nonhard_skip` | `clean_skip` | `light` | 2 |
| **speed** | `minimal` | `medium_or_higher` | `fast` | 2 |

---

## 4. Balance — force **full** research synthesis

When **`research_synthesis_depth`** is `light`, escalate to the **full** nested `research_synthesis` cycle if **any** of:

1. Run / hand-off confidence **&lt;** `research_full_if_run_confidence_below` (from snapshot).
2. Context or prior validator output includes **`safety_unknown_gap`** or **`safety_critical_ambiguity`** in a way that applies to this synthesis (per Research agent).
3. Successful research run count for `project_id` is a multiple of **`research_full_every_n_runs`** (counter: append-only **`.technical/research-synthesis-run-tally.jsonl`** — one JSON object per successful synthesis run with **`project_id`**, **`outcome`**, **`iso_timestamp`**, **`queue_entry_id`**; Research subagent maintains read/count/append per **research.md**).
4. **`research_full_if_prior_roadmap_validator_stronger_than_log_only`** is true and the prior roadmap validator pass was stronger than `log_only`.

---

## 5. Safety escalation (all modes, mandatory)

If **any** nested or Layer 1 validator in the dispatch chain returns **`severity: high`**, **`recommended_action: block_destructive`**, or a **hard** **`primary_code`** / matching **`reason_codes`** per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]], **do not** continue on a shortened profile path:

- **Layer 2 (Roadmap / Research):** Run the **full** nested re-validation path (IRA + second/compare as required by the tiered contract for that verdict).
- **Layer 1:** **Run** L1 post–little-val even when `l1_post_lv_policy` would skip (Roadmap subagent may set **`validator_context.force_layer1_post_lv: true`** when it emits escalation from nested hard signals).
- **Watcher-Result:** Use a prominent, parse-safe message prefix such as **`profile_escalation_full_validation:`** (include `pipeline_mode_used`, `primary_code`, `queue_entry_id`).

---

## 6. Observability

- **`nested_subagent_ledger`:** include **`pipeline_mode_used`** and echo **`effective_profile_snapshot`** (or subset) when present.
- **Queue Watcher-Result:** when L1 post–little-val is skipped for profile reasons, include in **`message`** or **`trace`**: `suppress_reason: l1_post_lv_skipped_profile`, `pipeline_mode_used`, `l1_post_lv_policy`.

---

## 7. Attestation allowlists

When **`strict_nested_return_gates`** is true, profile-driven skips must use allowlisted **`detail.reason_code`** values documented in [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] (e.g. `legacy_clean_log_only_no_ira`, `pipeline_mode_medium_or_higher_ira_skipped`, `profile_escalation_full_validation`).

---

## 8. References

- [[.cursor/rules/agents/queue.mdc|queue.mdc]] — A.5 (b1) profile gate, run memory for prior L1 hard/non-hard.
- [[.cursor/agents/roadmap.md|roadmap.md]], [[.cursor/agents/research.md|research.md]] — nested policy + research depth.
- [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] — hand-off structure, nested helpers.
