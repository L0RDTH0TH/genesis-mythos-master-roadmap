---
title: Phase 3.1.4 — Deterministic agency tick slices, starvation guards, and tie-break policy
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, simulation, tick, determinism, agency, fairness]
para-type: Project
subphase-index: "3.1.4"
handoff_readiness: 92
handoff_readiness_scope: "AgencySliceSchedule_v0 + stable tie-break + starvation budget within one tick_epoch (normative draft); HR 92 until slice order appears in replay log / golden row"
handoff_gaps:
  - "`AgencySliceId_v0` registry and collision policy vs spawn/manifest IDs still **TBD** until operator names slice ownership model"
  - "Golden row asserting **identical** slice order across live/replay drivers waits **D-032** header + **3.1.1** `replay_row_version` bump"
execution_handoff_readiness: 71
links:
  - "[[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]]"
  - "[[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935]]"
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
---

## Phase 3.1.4 — Deterministic agency tick slices, starvation guards, and tie-break policy

**Deliverables:** Vault-normative **`AgencySliceSchedule_v0`** for **one** `tick_epoch`: ordered **slices** (per-agent or per-cohort work units) that consume **bounded** substeps under **`CatchUpPolicy_v0`** (**D-031**), with **replay-stable** tie-break when priorities collide and **anti-starvation** budgets so low-priority agencies still advance when the schedule is not empty.

> [!warning] Authoritative handoff rule
> **Do not** treat **`handoff_readiness: 92`** as execution green. Use **`execution_handoff_readiness`** and **Tasks** until replay artifacts list slice IDs in deterministic order per tick.

**Interfaces**

- `AgencySliceId_v0`: stable string or uint identifier assigned at **registration** time (spawn/manifest epoch or explicit registry); **must** sort with a **total order** key `(tick_epoch, slice_index, tie_break_key)` where `tie_break_key` is **replay-serialized** (not OS thread id, not pointer).
- `AgencySliceSchedule_v0` (draft record): `{ tick_epoch, slices: AgencySliceId_v0[], max_slices_per_tick: uint32, starvation_credit: map<AgencySliceId_v0, uint32> }` — counts are illustrative; real caps align with **3.1.2** `max_steps_per_frame` / sub-step budget.
- **Pause / control coupling:** When **`SimulationRunControl_v0.paused`** (**3.1.3** / **D-032**), **do not** advance `tick_epoch`; slice schedule for the paused boundary is **empty** or **explicitly latched** — same rule as pause invariant on logical steps.
- **RNG coupling:** Per-slice draws use **namespaced** streams per **2.1.2**; schedule order **precedes** RNG consumption order so replay can reproduce draws without implicit parallelism.

### Algorithm sketch (mid-technical)

```text
function build_agency_slice_schedule(world, tick_epoch, policy, control):
  if control.paused:
    return empty_schedule  // no slice work this logical instant; see 3.1.3
  candidates = eligible_agencies(world, tick_epoch)  // deterministic filter
  ordered = stable_sort(candidates, primary=priority_band, secondary=AgencySliceId_v0)
  budget = policy.max_substeps_budget_for_tick(tick_epoch)  // 3.1.2 parity
  schedule = take_with_starvation(ordered, budget, credits=world.starvation_credit)
  return AgencySliceSchedule_v0(tick_epoch, schedule, ...)
```

### Desync taxonomy (v0) — agency scheduling

| Code | Detect | Surface | Replay outcome |
|------|--------|---------|----------------|
| `SLICE_ORDER_DIVERGENCE` | live vs replay slice sequence differs at same `tick_epoch` | CI golden | Fail-closed |
| `STARVATION_CREDIT_DRIFT` | credit map not serialized / reset semantics differ | Harness | Fail-closed |
| `RNG_SLICE_CROSS_TALK` | slice A consumes stream reserved for slice B | Audit | Fail-closed |

**Acceptance criteria**

- Within a single `tick_epoch`, **every** agency slice that runs has a **position** in a **total** order that is **fully determined** by vault-visible state + intents + policies (**D-027** examples are non-normative).
- Tie-break does **not** depend on wall time, thread schedule, or hardware floating behavior.
- **Cross-links:** **3.1.1** (commit preimage may reference slice order hash), **3.1.2** (sub-step budget), **3.1.3** (pause/control), **2.1.2** (RNG namespaces).

## Research integration

No nested Research `Task` this run (`params.enable_research` absent; util-based auto-enable not triggered). Prior art citations in **2.1.2** / **3.1.2** notes apply as internal vault context only.

## Tasks

- [ ] Register **`AgencySliceId_v0`** assignment policy (spawn-time vs explicit registry) and **extend / promote** existing **[[decisions-log#D-034|D-034]]** (draft → frozen checklist: collision + rename rules + wiki links) — **do not mint a new decision id**; **D-034** already anchors this tertiary in [[decisions-log]].
- [ ] Add worked example: **three** agencies with colliding priority bands showing **stable** tie-break + **one** starvation credit recovery across ticks.
- [ ] Extend replay log v0 schema stub (**3.1.1**) with optional `agency_slice_sequence` column **after** operator picks **D-032** A/B header shape.
