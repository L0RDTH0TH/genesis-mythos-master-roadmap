---
title: Phase 3 — Living Simulation and Dynamic Agency
roadmap-level: primary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "3"
links:
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
---

## Phase 3 — Living Simulation and Dynamic Agency

Build a decoupled simulation loop for weather, NPC schedules, and faction-level consequences that persist over time. Introduce explicit boundaries for DM live edits versus structural regeneration to preserve both control and systemic integrity.

- [ ] Implement core simulation tick scheduler
- [ ] Add DM overwrite controls with regeneration gates
- [ ] Validate persistence and consequence propagation across sessions
- [ ] Model living-world operations (NPC schedules, cycles, faction fan-out) under tick + regen + persistence gates (**3.4**)

> [!note] Parallel track (D-029)
> Phase **3** vault decomposition may proceed while **2.3.4** **`execution_handoff_readiness`** remains below normative until merged fixtures + green **`AlignAndVerify`**. See **Roll-up gates** below and [[decisions-log]] **D-029**.

## Risk register (v0)

| Risk | Signal | Mitigation | Owner |
|------|--------|------------|-------|
| Simulation drift vs replay determinism | Divergent tick order or hidden wall-clock coupling | Bind tick boundaries to Phase 1/2 replay contracts; explicit RNG namespaces per workstream | Eng + vault |
| DM override vs replay / hash closure | Overrides bypass manifest or registry gates | Regeneration gates aligned with [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]] semantics | Eng |
| Tick load / perf masking determinism | Non-deterministic timeouts influence outcomes | Perf budgets outside hash preimage; document fence policy | Eng |
| Persistence & cross-session consistency | Session boundary loses ledger or snapshot invariants | Link to Phase 1 rollback / snapshot themes in [[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]] | Eng |
| Dependency on EMG-2 execution closure | Phase 3 assumes frozen alignment floor without repo proof | Track **Blocked until** rows in roll-up table; do not claim **F** frozen in decisions-log per **D-022** | Operator + eng |

## Roll-up gates: Phase 3 ↔ EMG-2 (2.3.3 / 2.3.4)

| Assumes (vault-normative) | Blocked until (execution truth) |
|---------------------------|----------------------------------|
| [[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]] defines registry row + `AlignAndVerify` pseudo + WA matrix | `fixtures/emg2_alignment/v0/**` merged; job green on real vectors |
| [[phase-2-3-4-emg-2-execution-closure-vcs-promotion-and-floor-freeze-roadmap-2026-03-21-2339]] sequences PR tranche + CODEOWNERS + wiki **G-EMG2-*** row | WA log rows in **2.3.3** note show PASS/FAIL with evidence |
| [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] remains CI policy parent for golden drift | Wiki **G-EMG2-*** row materialized when repo paths exist |
| **D-024** provisional **F** documented in **2.3.2** | `emg2_floor_F_status: frozen` only after calibration evidence |

## Workstreams (secondaries)

- **3.1** — [[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]
- **3.2** — [[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]
- **3.3** — [[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]]
- **3.4** — [[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
