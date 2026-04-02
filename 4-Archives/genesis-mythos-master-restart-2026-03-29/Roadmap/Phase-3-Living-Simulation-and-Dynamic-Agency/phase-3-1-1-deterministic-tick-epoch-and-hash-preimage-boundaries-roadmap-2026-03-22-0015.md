---
title: Phase 3.1.1 — Deterministic tick epoch and hash preimage boundaries
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, simulation, tick, determinism, replay]
para-type: Project
subphase-index: "3.1.1"
handoff_readiness: 93
handoff_readiness_scope: "tick_epoch_contract + tick_hash_preimage + barrier_alignment (normative; replay log matrix TBD per synthesis §6–7)"
handoff_gaps:
  - "Golden replay row + CI evidence — TBD until repo fixtures + D-030 build matrix closure (vault has v0 schema + stub row below)"
execution_handoff_readiness: 72
links:
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
  - "[[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]]"
---

## Phase 3.1.1 — Deterministic tick epoch and hash preimage boundaries

**Deliverables:** Canonical **simulation tick index** (`tick_epoch`) monotonic under fixed `dt`; **tick commit record** visible to replay hash; explicit **preimage allow-list** vs **excluded ephemera** (render interpolation, wall clock, partial barrier buffers).

**Interfaces**

- `TickSchedule_v0`: advances `tick_epoch` only when accumulator ≥ `SIM_DT_FIXED`; never couples to frame delta for logical state.
- `TickCommitRecord_v0`: `{ tick_epoch, barrier_publish_ref, manifest_or_ledger_tail_ref, rng_counters_slice, committed_sim_observable_hash }` — consumable by `ReplayAndVerify` when EMG / registry rows exist.
- Alignment with [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]]: **ordering keys for shard work derive from lattice traversal (`shard_sequence`), not scheduler timing** — simulation tick ordering must not introduce a second, competing sequence source.

### Pseudo-code (normative sketch)

```text
function advance_simulation_tick(world, inputs_for_tick_k, dt_fixed):
  // Accumulator pattern: frame delta does not change logical step count
  world.sim_accumulator += world.last_frame_delta
  while world.sim_accumulator >= dt_fixed:
    world.sim_accumulator -= dt_fixed
    world.tick_epoch += 1
    apply_inputs_indexed(world, inputs_for_tick_k, world.tick_epoch)
    run_barrier_reconcile(world)  // private buffers → terminal publish only
    if terminal_publish(world):
      emit TickCommitRecord_v0(world, world.tick_epoch)
  // render_alpha is OUT of preimage (presentation only)
  return world

function preimage_for_tick_hash(record: TickCommitRecord_v0) -> bytes:
  return canonicalize(
    record.tick_epoch,
    record.barrier_publish_ref,
    record.manifest_or_ledger_tail_ref,
    record.rng_counters_slice,
    record.committed_sim_observable_hash
  )
```

### Float policy (v0)

**Stance:** **No IEEE floats in the tick hash preimage.** Logical simulation uses **fixed-point or rational `dt`** plus **integer `tick_epoch`**; any floating helper in prototyping must not serialize into `TickCommitRecord_v0` or `preimage_for_tick_hash` until a future explicit decision (per **D-027**) adopts a canonical binary-float profile.

### Replay log row schema (v0)

| Field | Type | Notes |
|-------|------|-------|
| `tick_epoch` | uint64 | Monotonic logical step |
| `barrier_publish_ref` | bytes32 / ledger pointer | Terminal publish from 2.1.3 barrier |
| `manifest_or_ledger_tail_ref` | bytes32 / pointer | Spawn / manifest tail as applicable |
| `rng_counters_slice` | canonical struct | Namespaced counters, stable sort |
| `committed_sim_observable_hash` | bytes32 | Hash of allow-listed observable slice only |
| `replay_row_version` | semver string | Row format version for golden registry |

**Worked example (stub hashes):**

```json
{
  "tick_epoch": 42,
  "barrier_publish_ref": "0xSTUB_BARRIER_PUBLISH_REF",
  "manifest_or_ledger_tail_ref": "0xSTUB_LEDGER_TAIL",
  "rng_counters_slice": { "sim_core": 1001, "intent_fanout": 77 },
  "committed_sim_observable_hash": "0xSTUB_SIM_OBS_HASH",
  "replay_row_version": "0.1.0"
}
```

### Desync taxonomy (v0)

| Code | Detect | Surface | Replay outcome |
|------|--------|---------|----------------|
| `TICK_PREIMAGE_DRIFT` | `preimage_for_tick_hash` differs given same inputs | Validator / CI golden | Fail-closed; inspect float policy + field allow-list |
| `BARRIER_REF_MISMATCH` | `barrier_publish_ref` does not match terminal publish | Ledger audit | Fail-closed; reject partial barrier state |
| `RNG_NAMESPACE_COLLISION` | Tick-scoped draw overlaps intent stream namespace | Static audit + harness | Fail-closed; remap namespaces per 2.1.2 |

**Acceptance criteria**

- Given fixed `dt` and identical input stream keyed by `tick_epoch`, `TickCommitRecord_v0` sequence is stable across machines per **Float policy (v0)** (no floats in preimage; rationals/fixed-point only).
- Partial async work **never** appears in preimage until **terminal publish** (parallel to SpawnCommit gating).
- `handoff_readiness` **93** reflects **normative** contract closure; **`execution_handoff_readiness` 72** until replay log + golden row exist per synthesis TBD.

## Research integration

### Key takeaways

- Separate **simulation time** (fixed `dt`, accumulator) from **render** time; replay must not depend on variable frame deltas ([Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/)).
- **Lockstep-style** framing: one canonical **input struct per tick**; jitter belongs in transport/presentation, not in logical tick indexing ([Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)).
- **Tick preimage:** include committed observable state + stable ordering keys + ledger-published refs; exclude partial async work until **terminal publish** (parallel to Phase 2.1.3).
- Phase **2.1.3** already mandates **deterministic `shard_sequence` from lattice traversal, never from scheduler timing** — see [[Ingest/Agent-Research/simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21|simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]].
- **Bevy** docs illustrate **fixed timestep** schedules as a pattern label, without locking an engine ([Bevy — fixed timestep](https://bevy.org/examples/movement/physics-in-fixed-timestep/)).
- **Replay log sketch + determinism/build matrix** are in the synthesis note §6–7 with explicit **TBD** until policy is pinned.

### Decisions / constraints

- **Constraint:** Interpolated presentation state must not feed hashed / ledger preimage (accumulator `alpha` is render-only).
- **Constraint:** Simulation consumers of generation output should mirror **SpawnCommit-style** visibility: **terminal ledger record** only.
- **Pending decisions:** Pinned build/flavor matrix for golden replay; exact hash subset vs full-state checksum; desync taxonomy when mismatch fires.

### Links

- [[Ingest/Agent-Research/simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21|Simulation tick scheduling — synthesis (2026-03-21)]]
- [[Ingest/Agent-Research/phase-2-1-3-async-commit-barrier-research-2026-03-19-2000|Prior 2.1.3 research note]] (related context)

## Tasks

- [ ] Freeze `TickCommitRecord_v0` field list vs registry / CI row when `fixtures/emg2_alignment` path exists — **blocked** until repo per **D-026**; link row schema to [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] when path live.
- [x] Add replay log worked example row (stub) under **Replay log row schema (v0)** — `tick_epoch` + `barrier_publish_ref` populated.
- [ ] Cross-check RNG namespace boundaries with Phase 2.1.2 intent stream policy (no collision on tick-scoped draws) — see **Desync taxonomy (v0)** `RNG_NAMESPACE_COLLISION`.
