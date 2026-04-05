---
created: 2026-04-05
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: followup-deepen-phase6-primary-rollup-sandbox-gmm-20260406T230000Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 1
validator_report_path: .technical/Validator/roadmap-handoff-auto-sandbox-gmm-20260406T235900Z-conceptual-v1-phase6-primary-rollup.md
ira_after_first_pass: true
---

# IRA report — sandbox-genesis-mythos-master (validator-driven, call 1)

## Context

Post–deepen nested **`roadmap_handoff_auto`** (conceptual_v1) returned **`needs_work`**, **`primary_code: safety_unknown_gap`**, with **`missing_roll_up_gates`** advisory. Invocation is **`ira_after_first_pass: true`**. Authoritative state already agrees on Phase 6 primary rollup narrative vs **`workflow_state.current_subphase_index: "6"`**; the validator correctly flags **residual traceability risk**: Phase 6 primary note **`subphase-index: "1"`** vs machine cursor **`"6"`**, plus **pattern_only** CDR / deferred execution gates / host-unproven nested helpers.

## Structural discrepancies

1. **Dual routing signal:** `Phase-6-…-0430.md` frontmatter **`subphase-index: "1"`** conflicts with **`workflow_state.md`** **`current_subphase_index: "6"`** and with sibling convention (Phase 5 primary uses **`subphase-index: "5"`**).
2. **Evidence grade:** CDR **`validation_status: pattern_only`** — cannot be “fixed” to evidence without human/authored upgrade.
3. **Execution closure:** **`missing_roll_up_gates`** remains legitimately open until execution track + re-validation (advisory on conceptual_v1).
4. **Hand-off paths:** In-repo wiki links largely use full folder-relative titles; any **Layer 0/1 hand-off** that still cites a **flat** `Roadmap/Phase-6-…-0430.md` path should be normalized to the nested on-disk path (grep hand-off YAML / comms, not only vault body).

## Proposed fixes

See parent return **`suggested_fixes`** JSON (structured). Apply in order **low → medium → high**; skip any item that fails snapshot/backup/confidence gates.

## Notes for future tuning

- After **advance-phase** into a phase, consider setting primary **`subphase-index`** to **phase number** at first primary deepen, or document a single schema: **ordinal vs cursor** in Vault-Layout / Roadmap-Quality-Guide.
- Validator **`safety_unknown_gap`** on conceptual_v1 often bundles **non-fatal** items; tiered Success gate still allows roadmap Success when little val ok — IRA should still surface **low-cost** alignment edits to shrink false dual-truth.
