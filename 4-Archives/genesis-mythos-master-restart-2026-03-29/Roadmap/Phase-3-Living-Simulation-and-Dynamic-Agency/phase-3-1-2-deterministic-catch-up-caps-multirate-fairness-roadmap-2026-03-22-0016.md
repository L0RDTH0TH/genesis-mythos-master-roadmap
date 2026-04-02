---
title: Phase 3.1.2 — Deterministic catch-up caps, multi-rate sub-steps, and within-tick fairness
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, simulation, tick, determinism, fairness]
para-type: Project
subphase-index: "3.1.2"
handoff_readiness: 93
handoff_readiness_scope: "catch_up_policy + substep_budget + within_tick_fairness (normative); replay driver parity + golden rows TBD"
handoff_gaps:
  - "Numeric `max_steps_per_frame`, frame-time clamp, and slow-vs-drop-vs-coalesce semantics must be pinned for `TickCommitRecord_v0` golden rows (pairs with 3.1.1 stub replay schema)"
execution_handoff_readiness: 74
links:
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
  - "[[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]]"
---

## Phase 3.1.2 — Deterministic catch-up caps, multi-rate sub-steps, and within-tick fairness

**Deliverables:** Vault-normative **catch-up policy** (`CatchUpPolicy_v0`) compatible with [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]; **sub-step budget** for accumulator loops; **within-tick work ordering** that does not depend on wall-clock or thread schedule.

**Interfaces**

- `CatchUpPolicy_v0`: `{ max_steps_per_frame: uint32, frame_dt_clamp_max_ms: uint32, on_budget_exceeded: SLOW_SIMULATION | DROP_SUBSTEPS | COALESCE_INPUTS }` — **all fields normative strings in vault**; numeric defaults wait operator/engine policy per **D-027**.
- `SubstepLedger_v0` (optional visibility): when internal sub-steps run under one `tick_epoch`, record **count** and **termination reason** (`completed`, `budget_hit`, `input_coalesced`) for audit — **not** part of `TickCommitRecord_v0` preimage until explicitly adopted.
- **Fairness / starvation:** `WithinTickWorkOrder_v0` — stable sort key `(subsystem_id, work_unit_id)` or explicit round-robin cursor; **forbidden:** `pthread_id`, wall timestamp, or nondeterministic container iteration order in replay-critical paths.
- **Multi-rate stance:** Prefer **one authoritative `tick_epoch`**; faster dynamics = **fixed integer subdivisions** of `SIM_DT_FIXED` or private integrator substeps **without** extra logical epochs. Co-simulation “major step” patterns are **illustrative only** (see research note).

### Algorithm sketch (mid-technical)

```text
function simulate_frame(world, frame_dt_real, policy: CatchUpPolicy_v0):
  dt_clamped = min(frame_dt_real, policy.frame_dt_clamp_max_ms)
  world.sim_accumulator += dt_clamped
  steps = 0
  while world.sim_accumulator >= world.SIM_DT_FIXED and steps < policy.max_steps_per_frame:
    world.sim_accumulator -= world.SIM_DT_FIXED
    world.tick_epoch += 1
    apply_inputs_for_epoch(world, world.tick_epoch)  // deterministic merge per policy.on_budget_exceeded when coalescing
    run_barrier_reconcile(world)
    if terminal_publish(world):
      emit TickCommitRecord_v0(world, world.tick_epoch)
    steps += 1
  // presentation alpha remains out-of-band (3.1.1)
  return world
```

### Desync taxonomy (v0) — extensions

| Code | Detect | Surface | Replay outcome |
|------|--------|---------|----------------|
| `CATCHUP_POLICY_DIVERGENCE` | live vs replay disagree on `max_steps` / clamp / coalesce | CI golden | Fail-closed |
| `SUBSTEP_STARVATION` | work order depends on thread schedule | Static audit | Fail-closed; remap to `WithinTickWorkOrder_v0` |
| `MULTI_CLOCK_EPOCH_SPLIT` | two competing logical epoch counters without documented mapping | Review | Hold until unified under one `tick_epoch` policy |

**Acceptance criteria**

- Catch-up path is **fully specified in prose + types** even when numeric defaults are TBD — **no silent** “best effort” steps in normative text.
- Any `on_budget_exceeded` mode documents **observable differences** (sim lags wall vs drops inputs vs merges inputs) and **replay obligation** to mirror live.
- `handoff_readiness` **93** = contract + taxonomy + interface closure; **`execution_handoff_readiness` 74** until golden harness encodes policy bits alongside 3.1.1 replay row.

## Research integration

### Key takeaways

- **Spiral of death:** If each fixed-`dt` step costs more real time than `dt`, the accumulator grows without bound—mitigate with **headroom**, **clamp incoming frame time**, and/or **`max_steps` per frame**; replay must use the **same** cap policy as live for `tick_epoch` parity.
- **Accumulator edge cases:** Guard non-positive `frameTime`; clamp huge hitches before `accumulator +=`; keep **`alpha = accumulator/dt`** strictly **presentation** (out of tick preimage per 3.1.1).
- **Single `tick_epoch`:** Prefer one authoritative logical counter; faster rates as **internal sub-steps** or **even subdivisions** of `dt`, with commits only at epoch boundaries—aligns with barrier-style publish.
- **Multi-rate analogy (illustrative):** Co-sim docs (e.g. mosaik **simulator groups**) describe hidden sub-steps with **major-step** visibility to outsiders—useful mental model only, **not** an engine prescription (**D-027**).
- **Fairness / starvation:** Use **stable sort keys** / round-robin over ids for within-tick work; avoid wall-clock or thread order as replay-critical ordering (consistent with 2.1.3 `shard_sequence` discipline).

### Decisions / constraints

- **Constraint (D-027):** No stack adoption; Gaffer, Bevy labels, mosaik, and Nystrom are **illustrative** only.
- **Constraint:** If `max_steps` truncates catch-up, document whether simulation **slows**, **drops** ticks, or **coalesces**—replay driver must match for golden rows.
- **Pending decisions:** Exact `max_steps`, frame-time clamp, and whether multi-rate is internalized under one `tick_epoch` or split clocks (prefer former for preimage simplicity).

### Links

- [[Ingest/Agent-Research/deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205|deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205]]
- [[Ingest/Agent-Research/Raw/deterministic-sim-scheduler-catchup-raw-2026-03-22-2205|Raw bundle (andreleite + mosaik)]]
- Prior: [[Ingest/Agent-Research/simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21|simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]]

## Tasks

- [ ] Pair `CatchUpPolicy_v0` bitfield / semver with `replay_row_version` in [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] when registry row exists.
- [ ] Cross-walk `WithinTickWorkOrder_v0` with Phase 2.1.2 RNG namespace rules — extend desync table if tick-scoped draws need new namespace slots.
- [ ] Add worked example: two frames with hitch + `max_steps_per_frame` truncation showing **identical** `tick_epoch` sequence in live vs replay driver stub.
