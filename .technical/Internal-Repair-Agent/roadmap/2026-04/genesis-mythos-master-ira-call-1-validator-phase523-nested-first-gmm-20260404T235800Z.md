---
created: 2026-04-04
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-deepen-phase5-523-worked-examples-replay-gmm-20260403T213500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 6
  medium: 4
  high: 1
validator_report_path: .technical/Validator/roadmap-handoff-auto-gmm-20260404T235800Z-followup-deepen-phase5-523.md
---

# IRA — genesis-mythos-master (post nested_validator_first, Phase 5.2.3)

## Context

Validator `roadmap_handoff_auto` (conceptual) reported **medium / needs_work** with **primary_code `safety_unknown_gap`** and **`missing_roll_up_gates`**. Structural cursors (workflow_state, roadmap-state, CDR queue id) were already coherent per the validator. IRA treats the report as a **weak floor** and expands evidence and rollup closure risks.

## Structural discrepancies

1. **Broken GWT evidence:** **GWT-5.2.3-C** cites **`§ Scope tension`**; no such heading exists in the 5.2.3 note (phantom anchor).
2. **Underspecified GWT evidence:** **GWT-5.2.3-H** and **GWT-5.2.3-I** use bare **`§ Behavior`**, too coarse for audit of **4.1.3** / **`operator_legibility_hook`** and Phase 2 boundary routing.
3. **Weak anchor for rollup row:** **GWT-5.2.3-K** uses **`§ Interfaces downstream`**; the note has **Downstream** bullets under **Interfaces**, not a discrete heading — easy to mis-resolve.
4. **Rollup gate not materialized in narrative artifacts:** State routes **next deepen = secondary 5.2 rollup** (NL + **GWT-5.2** vs **5.2.1–5.2.3**), but parent **5.2** / rollup checklist / DOD is not yet written as explicit Roadmap content (validator `missing_roll_up_gates`).
5. **Human confusion risk:** Filename stamp **2026-04-03-2135** vs operational mint narrative **2026-04-04** (validator advisory).

## Proposed fixes

See parent return YAML `suggested_fixes` (stable **low → medium → high**), Roadmap paths only, no `Roadmap/Execution/**`.

## Notes for future tuning

- Tighten roadmap-deepen / template lint: **GWT Evidence** must resolve to **existing** `##` / `###` heading, **numbered Behavior** item, **table row id**, or **explicit wikilink** to another phase note section.
- After tertiaries complete, emit a **rollup stub** on the parent secondary note in the same deepen pass to reduce `missing_roll_up_gates` churn.
