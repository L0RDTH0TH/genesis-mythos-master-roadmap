---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-deepen-phase3-315-gmm-20260402T224500Z
ira_call_index: 1
parent_run_id: 8f3c2a1d-eatq-20260330-gmm
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 1
validator_report_path: .technical/Validator/roadmap-handoff-auto-gmm-20260402T224500Z-followup-deepen-phase3-315.md
---

# IRA — roadmap / genesis-mythos-master (call 1)

## Context

Post–nested-validator **roadmap_handoff_auto** for queue `followup-deepen-phase3-315-gmm-20260402T224500Z` returned **`needs_work`** with **`primary_code: missing_roll_up_gates`** and **`safety_unknown_gap`**. **Effective track: conceptual** — execution rollup / registry / CI closure is **explicitly waived** in [[roadmap-state]] and [[distilled-core]]; the validator report confirms those codes are **advisory**, not hard-blockers. Residual work is **structural**: (a) **decision anchors** for scoped unknowns on **3.1.5**, (b) **single-source** distilled-core routing prose, (c) **next structural node** mint **3.2** via a normal deepen run (not execution proof rows).

## Structural discrepancies

1. **`missing_roll_up_gates`:** Triggered by **presence** of conceptual waiver text (rollup/CI/HR deferred), not by absent execution artifacts — **no incoherence**; optional audit row can cite this pass for Layer-1 compare hygiene.
2. **`safety_unknown_gap`:** [[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]] lists two **Open questions** (faction cohort lane vs shard; forge-sourced default path). They are **scoped** and **execution-deferred** in-note; validator asks for a **decisions-log / D-*** anchor so they are not “silent” across runs.
3. **Canonical routing:** [[distilled-core]] repeats **next cursor / mint 3.2** narrative in both **Phase 3 living simulation** and **Phase 2.5–2.6** sections — drift-prone duplicate; consolidate to one authoritative block.

## Proposed fixes (see structured return for machine order)

Listed in **low → high** apply order in the parent return payload.

## Notes for future tuning

- On **conceptual_v1**, treat **`missing_roll_up_gates`** as satisfied when waiver text + `gate_catalog_id: conceptual_v1` align; IRA should prefer **decision anchors + routing dedupe** over prompting execution CI work.
- After **3.1** chain complete, **second validator compare** should check **distilled-core** Phase 2.5–2.6 section for **pointer-only** routing vs Phase 3 section.
