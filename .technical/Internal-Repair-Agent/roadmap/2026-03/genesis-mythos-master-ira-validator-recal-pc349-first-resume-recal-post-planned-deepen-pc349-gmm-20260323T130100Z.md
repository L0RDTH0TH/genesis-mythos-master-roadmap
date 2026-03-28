---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-planned-deepen-pc349-gmm-20260323T130100Z
ira_call_index: 1
invocation: validator_first_pass
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T213000Z-recal-pc349-planned-first.md
status: repair_plan
risk_summary:
  low: 3
  medium: 0
  high: 0
tags: [internal-repair-agent, roadmap, genesis-mythos-master, validator-driven]
---

# IRA — genesis-mythos-master — post–nested-validator first pass (PC-349 recal)

## Context

RoadmapSubagent ran **RESUME_ROADMAP** `recal` for **genesis-mythos-master** after planned-chain deepen **`resume-deepen-post-recal-pc349-gmm-20260323T121500Z`**. Nested **`roadmap_handoff_auto`** first-pass report is **`roadmap-auto-validation-genesis-mythos-master-20260323T213000Z-recal-pc349-planned-first.md`**: **medium** / **needs_work**, **primary_code** `missing_roll_up_gates`, plus `missing_task_decomposition`, `safety_unknown_gap`. Regression guard vs compare-final **`…130000Z-post-ira-hygiene-pass2.md`** is **clean** (**dulling_detected: false**). Vault hygiene (21:22 **recal** row, **decisions-log** **D-044** / **D-059** picks **2026-03-23**) matches the validator narrative; **material** failure mode remains **rollup HR 92 < 93** and **G-P*.*-REGISTRY-CI HOLD** until **repo/CI** (or documented policy exception), not prose.

## Structural discrepancies

1. **Traceability gap:** **`workflow_state`** and **`roadmap-state`** 21:22 blocks cite the **compare-final hygiene** artifact (**`…130000Z-post-ira-hygiene-pass2.md`**) but do not yet cite **this** nested **first-pass** report (**`…213000Z-recal-pc349-planned-first.md`**), which is the actual **IRA input** and the object the second **`Task(validator)`** will compare against the first pass.
2. **Phase 3.4.9 mirror § Source line** still generically references "first pass **2026-03-23** (Layer-2 `recal`") rather than the **concrete** PC-349 planned-chain first-pass path for this cycle.
3. **No vault edit can clear** `missing_roll_up_gates` / unchecked Validator DoD mirror / `safety_unknown_gap` **honestly** without **execution evidence** or **versioned drift spec** — per validator §1d and user constraints (**no REGISTRY-CI clearance via vault-only prose**; **no fabricated operator picks**).

## Proposed fixes (for RoadmapSubagent to apply under guardrails)

Stable order; all **low** blast radius; **doc-only** citations / wording.

1. **`1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`** — On the **`2026-03-23 21:22`** **`recal`** table row **Status / Next** (and/or the matching **Notes** bullet): append explicit wikilink or backticked path to **nested first pass** `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T213000Z-recal-pc349-planned-first.md`, **alongside** the existing cite of **`.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T130000Z-post-ira-hygiene-pass2.md`** (regression / compare-final baseline). **Constraints:** do not imply that the first pass **clears** gates; label as **nested Validator first pass (IRA input)** vs **compare-final anchor**.

2. **`1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`** — In the **Nested validation** paragraph and/or **`### 2026-03-23 21:22 UTC`** callout: add the same **213000Z** first-pass path so **roadmap-state** ↔ **workflow_state** enumerate the same nested artifact set.

3. **`1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225.md`** — Under **`### Validator definition of done (mirror — not closure)`**, update the **`Source:`** line to cite **`.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T213000Z-recal-pc349-planned-first.md`** (PC-349 planned-chain **recal** cycle) while keeping all checkboxes **`[ ]`** unchanged.

## Notes for future tuning

- **Validator→IRA after first pass** on **recal** often yields **non-empty** reason codes even when vault narrative is **correct**; default IRA output should be **traceability + explicit "do not vault-clear execution gates"** unless a real doc contradiction exists.
- Consider a **template** snippet for **recal** rows: "compare-final anchor" vs "current nested first-pass path" to reduce omission on the next cycle.

## Machine return (suggested_fixes summary)

See parent structured return from Internal Repair Agent helper.
