---
title: Phase 3.1 — Simulation tick scheduler and time quanta
roadmap-level: secondary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, simulation, tick, determinism]
para-type: Project
subphase-index: "3.1"
handoff_readiness: 88
handoff_gaps:
  - "First tertiary [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] closes normative tick preimage; roll-up to ≥93 pending 3.1.2+ or secondary bundle"
  - "Secondary `handoff_readiness` **88** vs **≥93** target in **### Tertiary roll-up (≥93 closure)** — numeric gap **5** until listed tertiaries (through **3.1.6+**) satisfy that table; do not infer secondary closure from narrative alone."
links:
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
  - "[[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]]"
  - "[[phase-2-3-4-emg-2-execution-closure-vcs-promotion-and-floor-freeze-roadmap-2026-03-21-2339]]"
---

## Phase 3.1 — Simulation tick scheduler and time quanta (stub)

**Deliverables (draft):** Deterministic tick model; ordering guarantees vs Phase 2 stage ledger / commit barrier; explicit time-quanta boundaries for hashing observable simulation state.

**Interfaces:** Replay and registry contracts from Phase 2.1.3 / 2.2.x; EMG-2 alignment only after execution closure per **2.3.4** roll-up gates on primary.

### Interface table (v0)

| Contract | Producer | Consumer | Stable ID / version | Wiki anchor |
|----------|----------|----------|---------------------|-------------|
| `TickSchedule_v0` / `TickCommitRecord_v0` | Simulation kernel | Replay / `ReplayAndVerify` | `tick_schedule_contract_id` (TBD) | [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] |
| Async barrier terminal publish | Stage coordinator (2.1.3) | Tick commit preimage | `reconcile_plan_version` | [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]] |
| Golden / registry row | CI policy parent | EMG + sim replay | `deterministic_gate_version_id` | [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] |
| EMG-2 alignment floor | EMG-2 notes | Sim observable hash | `emg2_gate_version_id` | [[phase-2-3-4-emg-2-execution-closure-vcs-promotion-and-floor-freeze-roadmap-2026-03-21-2339]] |

### Risk register (v0)

| Risk | Blast radius | Owner | Mitigation | Evidence link |
|------|--------------|-------|------------|---------------|
| Tick ordering competes with ledger `shard_sequence` | Replay divergence | Eng | Preimage uses barrier publish ref only; **no** wall-clock / worker timing in ordering key | [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]] |
| EMG-2 execution still open while Phase 3 sim proceeds | Misread “frozen F” | Operator + eng | Roll-up gates on primary; D-029 parallel track; no numeric F in decisions-log per D-022 | [[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]] |
| Replay / CI coupling undefined | False green or blocked merge | Eng | Vault v0 schema + stub row in 3.1.1; real golden waits repo | [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] |
| Float / serialization in preimage | Cross-platform desync | Eng | **Float policy (v0)** pinned in 3.1.1; rationals or canonical profile | [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015#Float policy (v0)]] |
| Research synthesis §6–7 TBD | Stalled execution narrative | Roadmap | **D-030** defers matrix until policy; normative HR still valid | [[decisions-log]] **D-030** |

### Tertiary roll-up (≥93 closure)

| Tertiary | Normative HR | Execution HR | Blocking? | Parallel under D-029? | Notes |
|----------|--------------|--------------|-----------|------------------------|-------|
| 3.1.1 | 93 | 72 | No (vault normative) | Yes | Replay log golden TBD |
| 3.1.2 | 93 | 74 | No (vault normative) | Yes | Catch-up policy + fairness — [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]] |
| 3.1.3 | 91 | 72 | No (vault normative draft) | Yes | Pause + time-scale + replay header coupling — [[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]] (**D-032** / **D-033**) |
| 3.1.4 | 92 | 71 | No (vault normative draft) | Yes | Agency slices + tie-break + starvation — [[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]] (**D-034**) |
| 3.1.5 | 91 | 70 | No (vault normative draft) | Yes | Mutation ledger + replay-stable apply — [[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]] (**D-035** / **D-036**) |
| 3.1.6 | 92 | 69 | No (vault normative draft) | Yes | Observable bundle after apply + `TickCommitRecord_v0` bridge — [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]] (**D-037**) |
| 3.1.7 (rollup) | 93 | 68 | No (rollup authority) | Yes | **G-P3.1-*** **6/6 PASS** + advance gate — [[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]] (**D-038**) |

**Acceptance sketch:** Given fixed seed + intent stream, tick schedule produces stable ordering key for downstream emergence metrics (ties to EMG path when frozen).

### Tertiary spine

- **3.1.1** — [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] — tick epoch, accumulator, `TickCommitRecord_v0`, preimage boundaries vs 2.1.3 barrier.
- **3.1.2** — [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]] — `CatchUpPolicy_v0`, sub-step budget, within-tick fairness, multi-rate stance under one `tick_epoch`.
- **3.1.3** — [[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]] — `SimulationRunControl_v0` (draft), pause + dilation invariants, replay header coupling vs D-031/D-027.
- **3.1.4** — [[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]] — `AgencySliceSchedule_v0`, stable tie-break, starvation credits, RNG order vs **2.1.2** — **D-034**.
- **3.1.5** — [[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]] — `MutationIntent_v0`, `AgencySliceApplyLedger_v0`, idempotent apply — **D-035** / **D-036**.
- **3.1.6** — [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]] — `SimObservableBundleTelemetry_v0`, post-apply observable barrier — **D-037**.
- **3.1.7** — [[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]] — **G-P3.1-*** secondary closure rollup + advance readiness — **D-038**.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, handoff_readiness AS "Handoff"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "tertiary" AND contains(subphase-index, "3.1")
SORT subphase-index ASC
```
