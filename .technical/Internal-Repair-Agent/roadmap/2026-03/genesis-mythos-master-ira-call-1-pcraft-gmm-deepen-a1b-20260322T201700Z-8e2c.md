---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c
ira_call_index: 1
status: repair_plan
parent_run_id: pr-eatq-20260322-pcraft-a1b-dispatch
validator_report_path: .technical/Validator/roadmap-auto-validation-20260322T201800Z-gmm-pcraft-a1b-deepen-first.md
risk_summary: { low: 4, medium: 4, high: 1 }
tags: [internal-repair-agent, roadmap, genesis-mythos-master, phase-3-4-9, validator-driven]
---

# IRA — genesis-mythos-master — `pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c` (call 1)

## Context

RoadmapSubagent completed **RESUME_ROADMAP** `deepen` on **Phase 3.4.9** (`pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c`). Nested **`roadmap_handoff_auto`** first pass returned **severity medium**, **`recommended_action: needs_work`**, **`primary_code: missing_roll_up_gates`**, with **`reason_codes`** **`missing_roll_up_gates`**, **`safety_unknown_gap`**, **`missing_task_decomposition`**. **`ira_after_first_pass: true`** — this IRA cycle runs **before** compare-final; findings from the validator report are treated as a **weak minimum** (likely under-counted gaps). **Little val** for this slice is not the driver; structural honesty in the vault is already strong (rollup **HR 92 < 93**, **HOLD** rows, **D-044**/**D-059** **TBD** are repeated in [[distilled-core]], [[roadmap-state]], [[decisions-log]], and the phase note). Residual work is **traceability**, **decomposition executability**, and **drift-methodology labeling** — **not** fabricating operator picks.

## Structural discrepancies

1. **Roll-up gates (primary):** Macro **advance-phase** ineligibility is documented in multiple places, but there is **no single machine-facing rollup authority index** keyed to **`queue_entry_id` `pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c`** linking all three secondary rollup notes + **HR** + **HOLD** ids. Second-pass validator may still flag **navigation friction** as **`missing_roll_up_gates`**.
2. **Safety / unknown:** **D-044** (**RegenLaneTotalOrder_v0** A/B) and **D-059** (**ARCH-FORK-01** vs **02**) remain **TBD** in [[decisions-log]] — correct. Gap: **no dated audit stub** on those rows tying this **nested** validator first pass to still open (reduces false resolved-by-prose reads).
3. **Task decomposition:** **GMM-HYG-01** / **GMM-DLG-01** / **GMM-TREE-01** checklists are **`[ ]`** — correct. **GMM-L1-01** documents L1 codes but does not spell **post-IRA** what to paste into Notes / ledger for each **GMM-** task when a run completes — validators may still emit **`missing_task_decomposition`** until **evidence strings** exist.
4. **Drift metrics:** **`drift_score_last_recal`** / **`handoff_drift_last_recal`** are **qualitative** until a versioned spec + input hash exists — compare-final may keep **`safety_unknown_gap`** until methodology is pinned or explicitly scoped as non-reproducible in a dedicated stub.
5. **D-060 / recal:** Policy is already on the phase note and [[workflow_state]]; gap is **explicit citation** of **this** validator path in **Notes** so Layer-1 / compare-final can close the loop without rereading the full log table.

## Proposed fixes (see structured suggested_fixes in parent return)

Apply in **low → medium → high** order when snapshots and gates allow. **Do not** append **Option A/B** or **ARCH-FORK-0x** under **D-044**/**D-059** without operator action.

## Notes for future tuning

- Repeated **`missing_roll_up_gates`** on honest tertiary slices suggests validators should weight **rollup index present + cited** separately from **HR ≥ min_handoff_conf** closure.
- **`missing_task_decomposition`** should distinguish **WBS present** vs **executable evidence** (checkbox + `queue_entry_id`); IRA should not recommend checking boxes without cited runs.
- Consider a **single** `Roadmap/rollup-gates-index.md` (project-local) maintained on each recal — reduces scatter across tertiary notes.
