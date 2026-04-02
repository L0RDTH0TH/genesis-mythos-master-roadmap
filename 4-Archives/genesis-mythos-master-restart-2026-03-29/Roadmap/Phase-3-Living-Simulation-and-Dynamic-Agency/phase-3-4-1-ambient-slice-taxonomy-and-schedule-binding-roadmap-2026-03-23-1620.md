---
title: Phase 3.4.1 — Ambient slice taxonomy and schedule binding
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-23
tags: [roadmap, genesis-mythos-master, phase, living-world, ambient, slices]
para-type: Project
subphase-index: "3.4.1"
handoff_readiness: 87
execution_handoff_readiness: 48
handoff_readiness_scope: vault-normative draft — slice ID table + RNG matrix + regen/persistence predicates; registry rows + replay fields TBD (D-032 / D-044 / D-047 / D-048)
handoff_gaps:
  - "Draft `AgencySliceId_v0` labels are non-authoritative until D-032 + coordinated `replay_row_version`"
  - "Same-tick regen vs ambient scalar ordering is provisional until operator logs D-044 A/B pick in decisions-log"
  - "Golden rows for mixed ambient+agency ticks blocked per D-045 / D-032"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]]"
  - "[[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]"
  - "[[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]]"
  - "[[Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600]]"
  - "[[distilled-core]]"
  - "[[decisions-log]]"
---

## Phase 3.4.1 — Ambient slice taxonomy and schedule binding

> **Architect:** Bind **ambient** living-world producers (NPC routine, weather phase, faction propagation) to **one** `tick_epoch` schedule — extend **`AgencySliceSchedule_v0`** / **`AgencySliceId_v0`**, do not fork a wall-clock authority.

### TL;DR

- Ambient work is **additional slice rows** in the same total order as agency slices (**D-034** tie-break + starvation credits).
- **Scalar / commutative** fan-out → **`MutationIntent_v0`** via **3.1.5** merge policy; **subgraph-changing** ambient outcomes → **`RegenRequest_v0`** (**3.2.2** P1–P6) before dependent scalars (**provisional** until **D-044** pins `RegenLaneTotalOrder_v0`).
- **RNG:** Partitioned streams (`agency_core`, `ambient_npc`, `ambient_env`, …) — draws occur **after** schedule order; no cross-talk with proc/agency streams ([PCG useful features](https://www.pcg-random.org/useful-features.html)).
- **Persistence:** Long-horizon ambient fields that affect hashed observables → **`PersistenceBundle_vN`** + matrix outcome (**D-048**) + resume preflight (**D-047**).

## Contract sketch — schedule extension

```text
AgencySliceSchedule_v0 (extended):
  tick_epoch: u64
  ordered_rows: AgencySliceRow_v0[]  // stable sort: slice_index, tie_break_key

AgencySliceRow_v0:
  slice_id: AgencySliceId_v0          // agency + ambient namespaces
  actor_key: bytes | null            // nullable for global ambient phases
  fairness_class: enum { agency, ambient, system }
  estimated_cost_units: u32          // optional deferral signal (budget gate)
```

**Deferral rule:** If `estimated_cost_units` would exceed per-tick budget, emit **no** authoritative mutation this tick; carry **deferred_work_ids** in slice-local state that is itself written via an idempotent ledger row (never skip schedule slots or reorder).

## Draft slice classes (non-canonical)

| Draft `slice_id` | Role | Typical payload |
|------------------|------|-----------------|
| `AMBIENT_NPC_ROUTINE` | Deterministic NPC routine step | Commutative scalars / inventory deltas |
| `AMBIENT_WEATHER_PHASE` | Environmental phase machine | Region-scoped enums / scalars |
| `AMBIENT_FACTION_PROPAGATION` | Stance / territory reducers | Commutative merge preferred; else regen or `SLICE_STATE_CONFLICT` |

Full draft registry table + tie-break sketches: [[Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600]] §1b.

## RNG namespace matrix (sketch)

| Stream id | Consumer | Must not consume |
|-----------|----------|------------------|
| `rng_agency_core` | Player/DM agency slices | ambient_* |
| `rng_ambient_npc` | AMBIENT_NPC_ROUTINE | agency_core, proc_gen |
| `rng_ambient_env` | AMBIENT_WEATHER_PHASE | agency_core |
| `rng_ambient_faction` | AMBIENT_FACTION_PROPAGATION | agency_core |

## Regen vs ledger decision tree

```text
if change_mutates_regen_subgraph(GraphScope_v0):
    enqueue RegenRequest_v0  // 3.2.2 P1–P6
    // Provisional: complete regen_apply_sequence before topology-dependent ambient scalars
    // until D-044 A/B logged in decisions-log
else if mutations_commutative_under_MutationIntent_v0:
    append MutationIntent_v0 rows per 3.1.5 ordering
else:
    emit fail-closed reason_code (extend registry with operator)
```

## Persistence touchpoints

- Bundle any **cross-session** ambient field that feeds **post_apply_observable_root** / committed observable hash into **`PersistenceBundle_vN`** with explicit **`migration_id`** when schema shifts (**D-048** / **D-049**).
- Resume preflight: **`ResumeCheckpoint_v0`** must see consistent `tick_epoch` + ledger tail before applying ambient deltas (**D-047**).

## Research integration

### Key takeaways

- Ambient living-world work should appear as **draft `AgencySliceId_v0` rows** in the same **`AgencySliceSchedule_v0`** total order as agency slices (**D-034**), not a parallel wall-clock scheduler.
- **RNG:** Use **partitioned streams** (`agency_core` vs `ambient_*`) with draws **after** schedule order; PCG-style streams avoid cross-talk ([PCG streams](https://www.pcg-random.org/useful-features.html)).
- **Regen:** Scalar/commutative fan-out stays in **`MutationIntent_v0`**; **subgraph-changing** ambient outcomes use **`RegenRequest_v0`** (**3.2.2** P1–P6). **Provisional same-tick story:** regen-lane completes before dependent scalar ambient ledger appends — **until D-044** pin; record formally in [[decisions-log]].
- **Persistence:** Long-horizon ambient fields belong in **`PersistenceBundle_vN`** + matrix outcomes (**D-048**); resume preflight before mutating hashed observables ([Event Sourcing / snapshots](https://martinfowler.com/eaaDev/EventSourcing.html)).
- **Fixed timestep framing:** deferral uses **logical `tick_epoch`** discipline ([Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)).

### Links

- Synthesis: [[Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600]]
- Prior 3.4 secondary synthesis: [[Ingest/Agent-Research/phase-3-4-living-world-operations-research-2026-03-23]]

## Tasks

- [ ] Copy draft slice registry rows from research §1b into a dedicated `### Draft registry` subsection when operator requests literal freeze prep
- [ ] Add **one** worked example: commutative ambient scalars vs single `RegenRequest_v0` in same `tick_epoch` (pseudocode only until D-044)
- [ ] Cross-link **3.1.6** observable bundle when ambient mutations touch `post_apply_observable_root`
- [ ] Log **D-044** provisional ordering sentence in [[decisions-log]] when operator picks A/B (do not invent pick in vault)

### Task ledger (DEFERRED / BLOCKED)

| Open task (from ## Tasks) | Status | WAITING_ON / BLOCKED_ON | Closure owner |
| --- | --- | --- | --- |
| Copy draft slice registry rows into `### Draft registry` | **DEFERRED** | **D-032** (`replay_row_version` / header freeze) + **D-044** lane ordering | Operator + repo |
| One worked example: commutative scalars vs `RegenRequest_v0` | **BLOCKED** | **D-044** A/B pick in [[decisions-log]]; golden rows **D-045** / **D-032** | Operator + repo |
| Cross-link **3.1.6** observable bundle | **DEFERRED** | **D-037** serialization profile + **D-032** | Operator + repo |
| Log **D-044** ordering sentence | **WAITING_ON_OPERATOR** | Explicit A/B choice only — vault must not invent | Operator |

## Acceptance sketch

- [ ] Every ambient mutation type maps to **either** `MutationIntent_v0` **or** `RegenRequest_v0` with explicit fail-closed path
- [ ] No ambient producer bypasses **`AgencySliceSchedule_v0`** ordering
- [ ] RNG draw order documented per stream matrix (above)
- [ ] Cross-session ambient state declares **bundle version** + matrix outcome before observables commit

### Worked example (vault-only checklist — no repo / golden claims)

- [ ] **Inputs (vault):** one `tick_epoch`, two draft `AgencySliceRow_v0` lines (`AMBIENT_NPC_ROUTINE` commutative scalars + one subgraph-changing ambient row → `RegenRequest_v0`), RNG stream ids from matrix above
- [ ] **Expected vault artifacts:** pseudocode or fenced narrative under this note linking **3.1.4** schedule, **3.1.5** merge path, **3.2.2** P1–P6; pointer row in [[decisions-log]] when **D-044** A/B is logged
- [ ] **Explicit non-claim:** no `fixtures/**` rows, no CI green, no `replay_row_version` bump until **D-032** / **D-044** / operator PR path — EHR stays draft until then
- [ ] **Observability:** if example touches `post_apply_observable_root`, cite **3.1.6** and **D-037** gaps rather than implying frozen serialization
