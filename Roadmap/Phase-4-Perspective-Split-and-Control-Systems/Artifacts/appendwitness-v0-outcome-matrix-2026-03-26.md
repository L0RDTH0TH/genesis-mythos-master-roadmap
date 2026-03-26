---
title: A-41110-02 - AppendWitness v0 outcome matrix
created: 2026-03-26
tags: [roadmap, genesis-mythos-master, phase-4, artifact, a-41110-02]
para-type: Project
project-id: genesis-mythos-master
roadmap-track: conceptual
status: active
---

# A-41110-02 - AppendWitness v0 outcome matrix

Conversion-ready matrix for AppendWitness outcomes. This is structural only and does not imply closure.

| outcome | closure_table_effect | rollback_hook | acceptance_status |
| --- | --- | --- | --- |
| WITNESS_BOUND_OK | write `witness_ref`, keep row OPEN/HOLD semantics | none | OPEN |
| PATH_FAIL | no closure promotion | apply 4.1.1.9 rollback section 1 downgrade | OPEN |
| TABLE_KEY_MISSING | no closure promotion | apply missing key variant in 4.1.1.9 rollback section 1 | OPEN |
| APPEND_DUPLICATE_IDEMPOTENT | no-op | none | OPEN |

## Acceptance rows

- [x] All four outcomes from `AppendWitnessOutcome_v0` are represented.
- [x] Rollback coupling is explicit for path/key failures.
- [x] No row claims CI closure or rollup PASS.
