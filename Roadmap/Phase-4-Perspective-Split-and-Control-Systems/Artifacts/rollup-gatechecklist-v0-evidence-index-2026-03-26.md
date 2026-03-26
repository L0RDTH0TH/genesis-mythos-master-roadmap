---
title: A-41110-01 - RollUpGateChecklist v0 evidence index
created: 2026-03-26
tags: [roadmap, genesis-mythos-master, phase-4, artifact, a-41110-01]
para-type: Project
project-id: genesis-mythos-master
roadmap-track: conceptual
status: active
---

# A-41110-01 - RollUpGateChecklist v0 evidence index

This artifact indexes each RollUpGateChecklist row to one validator, one workflow row, and one decision anchor.

| gate_row_id | validator_ref | workflow_ref | decision_ref | acceptance_status |
| --- | --- | --- | --- | --- |
| G-P4.1-ROLLUP-GATE-01 | 3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T130500Z-roadmap-handoff-auto-conceptual-v1-post-d080.md | [[workflow_state]] (`resume-forward-map-phase-41110-gmm-20260326T180000Z`) | [[decisions-log]] D-083 | OPEN |
| G-P4.1-ROLLUP-GATE-02 | 3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T130500Z-roadmap-handoff-auto-conceptual-v1-post-d080.md | [[workflow_state]] (`layer1-next-followup-deepen-post-forward-map-recal-gmm-20260326T191900Z`) | [[decisions-log]] D-085 | OPEN |
| G-P4.1-ROLLUP-GATE-03 | 3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T191900Z-roadmap-handoff-auto-conceptual-v3-post-forward-map-recal.md | [[workflow_state]] (`layer1-next-followup-deepen-post-forward-map-recal-gmm-20260326T191900Z`) | [[decisions-log]] D-085 | HOLD |

## Acceptance rows

- [x] Each row has validator_ref + workflow_ref + decision_ref.
- [x] No row claims HR >= 93.
- [x] No row claims REGISTRY-CI PASS.
