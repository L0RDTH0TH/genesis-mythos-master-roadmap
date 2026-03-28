---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: pc-a1b-gmm-recal-20260322T123100Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 4, medium: 2, high: 0 }
parent_run_id: pr-l1-eatq-20260322-a1b-recal-dispatch
validator_report_path: .technical/Validator/roadmap-auto-validation-20260322T201505Z-gmm-pc-a1b-first.md
reason_codes: [missing_roll_up_gates, safety_unknown_gap, missing_task_decomposition]
---

# IRA — roadmap — pc-a1b-gmm-recal — call 1

## Context

Post–first-pass **`roadmap_handoff_auto`** for queue **`pc-a1b-gmm-recal-20260322T123100Z`** (`ira_after_first_pass: true`). Verdict **medium** / **needs_work** with **`missing_roll_up_gates`**, **`safety_unknown_gap`**, **`missing_task_decomposition`**. Artifacts read: validator report, `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`, `workflow_state.md`, `decisions-log.md`, phase notes **3.4.8** / **3.4.9**. **No** fabricated **D-044** A/B or **D-059** **ARCH-FORK** picks per hand-off constraint.

## Structural discrepancies

1. **Temporal audit rot (`safety_unknown_gap` amplifier):** Under **`### 2026-03-22 20:15 UTC`** in **roadmap-state**, the scalar line cites **“21:05 UTC consistency block”** as the prior anchor for **unchanged** drift — **21:05 is after 20:15**, so the sentence is causally incoherent (matches validator verbatim gap).
2. **`missing_roll_up_gates`:** **D-046** / **D-050** / **D-055** already record **HR 92** vs **`min_handoff_conf` 93** and **HOLD** rows; risk is **under-emphasis** in **roadmap-state** Phase 3 summary vs compare-final expectation, not missing decisions-log rows.
3. **`safety_unknown_gap`:** **D-044** / **D-059** are correctly **open** with templates; drift scalars are already labeled qualitative in **workflow_state** Notes and **roadmap-state** drift methodology — could tighten **version token** + **non-comparability** in frontmatter or RECAL stub.
4. **`missing_task_decomposition`:** **3.4.8** ladder rows **1–2** **PASS**; **rows 3+** remain **`[ ]`** with honest deferrals. **3.4.9** has **GMM-** IDs but compare-final still wants **explicit row-by-row** WBS / acceptance binding for **each** unchecked ladder row (vault-only, no false **PASS**).

## Proposed fixes

See parent return **`suggested_fixes`** array (ordered, with **`risk_level`** / **`target_path`** / **`action_type`**).

## Notes for future tuning

- **RECAL blocks** appended **above** deepen rows should use **only timestamps ≤ heading UTC** or **snapshot paths** as “prior baseline” for “unchanged” language.
- **First-pass IRA** after clean validator runs should still emit **empty or single low-risk** doc hygiene when **`primary_code`** is **audit-trail**-adjacent.
