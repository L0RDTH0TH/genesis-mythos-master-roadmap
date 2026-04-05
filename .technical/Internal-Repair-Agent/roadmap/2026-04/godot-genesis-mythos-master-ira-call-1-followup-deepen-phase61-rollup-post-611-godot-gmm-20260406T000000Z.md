---
created: 2026-04-06
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: followup-deepen-phase61-rollup-post-611-godot-gmm-20260406T000000Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 0
  high: 0
validator_report_path: .technical/Validator/l1postlv-followup-phase6-primary-rollup-godot-gmm-20260406T190800Z.md
---

# IRA — roadmap (validator→IRA cycle)

## Context

Post–little-val **roadmap_handoff_auto** (conceptual_v1) reported **`state_hygiene_failure`** because Phase 6 primary frontmatter keeps **`status: active`** while **`phase6_primary_rollup_nl_gwt: complete`** and project **`roadmap-state.md`** assert **`status: complete`** / Phase 6 rollup closure. **`safety_unknown_gap`** flags CDR **`validation_status: pattern_only`** as under-specified for machines. **`missing_roll_up_gates`** is **advisory** on conceptual track (execution-deferred); optional copy clarifies that for validators/operators.

## Structural discrepancies

1. **Phase 6 primary** — `status: active` contradicts rollup-complete flags and **`roadmap-state`** project completion semantics.
2. **CDR** — `validation_status: pattern_only` lacks catalog binding and evidence-class disambiguation (reads as “unknown” to hostile validators).
3. **Advisory** — Execution debt remains correctly waived; a single explicit sentence prevents **`missing_roll_up_gates`** from being misread as a conceptual hard blocker.

## Proposed fixes (caller applies; snapshot/backup per roadmap rules)

See parent return **`suggested_fixes`** JSON array for machine consumption.

## Notes for future tuning

- Prefer **one** canonical meaning for roadmap phase-note **`status`** on conceptual primaries when rollup flags are `complete`: either **`complete`** or a dedicated `roadmap_note_lifecycle` key used consistently across phases 4–6 primaries.
- CDR frontmatter could standardize **`validation_gate_catalog`** + **`validation_evidence_class`** wherever **`validation_status`** is not `matrix` / `hardened`.
