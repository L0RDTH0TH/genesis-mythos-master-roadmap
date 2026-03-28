---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-gmm-deepen-followup-post-0805-20260322T081500Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 2, high: 1 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260322T220500Z.md
parent_run_id: queue-eat-20260322T120500Z-gmm-1
---

# IRA report — roadmap — genesis-mythos-master (call 1)

## Context

Post–first-pass `roadmap_handoff_auto` on Phase **3.4.7–3.4.8** returned **medium / needs_work** with **primary_code `missing_task_decomposition`** and **`safety_unknown_gap`**. Vault hygiene for **workflow_state** vs last **`## Log`** row was read as consistent on this pass; **contaminated-report rule** applied — gaps are treated as a **weak minimum**. Residual risk: tertiary **3.4.8** still reads as **policy + two Tasks**, which a hostile implementer can interpret without bound machine parameters or fork-resolution evidence; **D-044** / **D-059** remain legitimately **unpicked** (no IRA-suggested fabrication of operator choices).

## Structural discrepancies (expanded)

1. **Task surface vs tertiary altitude:** `## Tasks` on **3.4.8** is two lines — insufficient for checkable engineering closure or second-pass validator comparison, given the note also claims an **automation decision matrix** and **high-util / recal** contract.
2. **Prose-only threshold narrative:** "80%" / "70%" appear in narrative and matrix; canonical keys live under **`prompt_defaults.roadmap`** per [[3-Resources/Second-Brain/Parameters|Parameters]] — the phase note does not **bind** readers/implementers to those keys (validator cited this gap class).
3. **`safety_unknown_gap` minimum:** Unlogged **D-044** A/B and **D-059** fork are **real** unknowns; mitigations must be **verification and blocking checks**, not invented log lines.
4. **T-P4-03:** **SCOPED_VAULT** is honest; execution path still needs an **evidence ladder** (what changes when a repo exists) as checkable leaves.

## Proposed fixes (caller applies; stable order)

See structured `suggested_fixes` in the parent return payload (low → medium → high).

## Notes for future tuning

- When minting **policy tertiaries** after a WBS slice, require **≥N** Tasks or an explicit **"meta-policy only"** demotion in Parameters with a single threshold source — catch **`missing_task_decomposition`** earlier.
- Consider a **validator reason_code** for "fork_pending_ok" vs "decomposition_missing" when hygiene is clean but operator literals are open — reduces conflation of honest unknowns with structure failures.
