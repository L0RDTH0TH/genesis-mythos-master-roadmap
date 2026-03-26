---
title: A-41110-03 - WitnessRefHash v0 registry promotion plan
created: 2026-03-26
tags: [roadmap, genesis-mythos-master, phase-4, artifact, a-41110-03]
para-type: Project
project-id: genesis-mythos-master
roadmap-track: conceptual
status: active
---

# A-41110-03 - WitnessRefHash v0 registry promotion plan

Plan from vault-defined hash preimage to registry-backed execution evidence.

| step | owner | precondition | evidence target | hold-state |
| --- | --- | --- | --- | --- |
| Freeze `H_canonical` profile text for v0 | ROLE:registry-ci | JSON preimage shape fixed in 4.1.1.10 | registry row proposal note | HOLD |
| Materialize registry row in repo/wiki | ROLE:registry-ci | policy approval (D-020 / 2.2.3) | checked-in row + review ref | HOLD |
| Add deterministic fixture path + replay tie-in | ROLE:lane-c-harness | lane-c bridge artifact exists (`@skipUntil(D-032)` still explicit) | fixture file path + queue anchor | HOLD |
| Promote to execution closure evidence | ROLE:lane-c-harness | CI evidence present | validator report updates hold semantics | HOLD |

## Acceptance rows

- [x] Owner lanes are named for each step.
- [x] Preconditions are explicit and auditable.
- [x] REGISTRY-CI remains HOLD until external proof exists.
