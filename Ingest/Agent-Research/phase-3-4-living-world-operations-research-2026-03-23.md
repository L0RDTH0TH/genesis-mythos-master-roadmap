---
title: Phase 3.4 living world operations — research synthesis (schedules, cycles, faction fan-out)
created: 2026-03-23
tags: [agent-research, roadmap, genesis-mythos-master]
project-id: genesis-mythos-master
para-type: Resource
status: draft
source: vault-first + external light touch
linked_phase: Phase-3-4
parent_context:
  queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-followup-suggested-249
  parent_run_id: pr-qeat-20260323-genesis-249
links:
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]"
  - "[[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]]"
  - "[[phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200]]"
  - "[[decisions-log]]"
---

# Phase 3.4 — Living world operations (research synthesis)

Narrow research pass for the **next planned secondary under Phase 3**: **living world operations** (NPC schedules, environmental / weather cycles, faction-level consequence fan-out), constrained to stay compatible with **deterministic tick / replay (3.1)**, **DM / regen gates (3.2)**, and **cross-session persistence / resume / migration (3.3)**.

## 1. Vault anchors (genesis-mythos-master Phase 3)

### 3.1 — Tick, scheduling, apply ledger, observables

- **Secondary:** [[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]] — `TickSchedule_v0` / `TickCommitRecord_v0`, barrier coupling to [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]], catch-up / pause / time-scale (**D-031**–**D-033**), **AgencySliceSchedule_v0** with stable tie-break + starvation + **RNG after schedule order** (**D-034**), **MutationIntent_v0** + **AgencySliceApplyLedger_v0** (**D-035** / **D-036**), post-apply observable bundle vs commit hash (**D-037**), rollup **D-038** on [[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]].

**Implication for 3.4:** Any “background sim” (schedules, weather, faction propagation) must **emit mutations only through the same tick-scoped, totally ordered paths** already normative on 3.1.x — no hidden wall-clock or parallel threads that reorder agency slices or RNG draws.

### 3.2 — DM overrides, regen, replay lane

- **Secondary:** [[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]] — `DmOverrideIntent_v0`, `RegenRequest_v0`, **regen-before-merge** vs player+DM intents (**D-041** / **D-042**), **`regen_apply_sequence`** + **RegenLaneTotalOrder_v0** fork and **TickCommitRecord_v0** coupling (**D-044** / **D-045**).

**Implication for 3.4:** Living-world systems that **reshape subgraphs** (e.g. faction territory regen) stay **gated regen**, not ad-hoc mutation; fan-out that touches procedural slices must respect **fail-closed** preconditions and replay row ordering once operator picks **RegenLaneTotalOrder_v0** A vs B.

### 3.3 — Persistence, resume, migration rollup

- **Secondary:** [[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]] — `ResumeCheckpoint_v0` (**D-047**), bundles + matrix (**D-048**), migrate harness (**D-049**).

- **Rollup / advance gate:** [[phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200]] — **D-050**: **G-P3.3-*** inventory (**3 PASS** persistence core + **2 HOLD** cross-cuts); rollup **HR 92** vs **min_handoff_conf 93** blocks strict **advance-phase** from 3.3 until a **HOLD** clears or policy documents an exception.

**Implication for 3.4:** Cross-session **faction / NPC / weather state** must be **versioned persistence bundles** with the same checkpoint + migration story as 3.3.x; “sim-only” caches cannot become the sole source of truth without a **replayable event projection** into hashed observables.

## 2. External patterns (light touch)

| Pattern | Use for Phase 3.4 | URL |
|--------|-------------------|-----|
| **Fixed timestep + accumulator** | Decouple **render / UI cadence** from **logical tick** so catch-up and multi-step frames stay identical in live vs replay (aligns with **CatchUpPolicy_v0** / pause coupling). | [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) (Gaffer On Games) |
| **Deterministic lockstep mindset** | Treat **inputs + ordering** as the replay contract; any schedule or faction update must be **a function of committed tick state**, not of discovery order or I/O timing. | [Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) (Gaffer On Games) |
| **Independent RNG streams** | Per-system or per-entity **stream indices** (e.g. PCG-style streams) so weather, NPC idle variety, and faction **jitter** do not steal entropy from combat / proc hooks — matches “RNG after schedule order” from **D-034**. | [PCG useful features — streams](https://www.pcg-random.org/useful-features.html) |
| **Event sourcing + snapshots** | Persist **append-only domain events** for fan-out; **materialized “living world” views** are projections; **snapshots** (checkpoints) shorten resume — parallels **ResumeCheckpoint_v0** and migrate harness narrative. | [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) (Martin Fowler) |

## 3. Recommended architecture sketch for 3.4 (normative direction, not vault law)

1. **Two-tier state:** (a) **Authoritative sim state** committed per `tick_epoch` into existing ledger + `TickCommitRecord_v0` preimage; (b) **Player-visible / presentation** layer derived from (a) and allowed to lag (interpolation), never fed back into (a) without an intent.
2. **Schedules & cycles as first-class tick consumers:** NPC routines and weather phase machines run as **additional agency slices** or **sub-schedulers** with explicit **stable IDs** and **tie_break_key** semantics — extend **AgencySliceSchedule_v0** rather than inventing a second ordering universe.
3. **Faction fan-out:** Model **cross-NPC / cross-region effects** as **commutative where possible** (merge tables) or as **ordered event reducers** per tick; non-commutative overlaps continue to surface **`SLICE_STATE_CONFLICT`** or regen-gated subgraphs per **3.1.5** / **3.2.x**.
4. **Persistence boundary:** Only **checkpointed + bundle-versioned** projections cross session lines; optional **async “world think”** jobs may exist offline but may not alter replay unless their outputs are **re-materialized as deterministic intents** on next session load.

## 4. Open questions (for phase note / operator)

- Should **ambient living world** (distant NPCs) use **coarser tick quanta** under **3.1.2** fairness caps, or a **separate slice class** with shared `tick_epoch`?
- Does faction propagation ever **imply regen** (new POI / layout), forcing **RegenRequest_v0** on every material change, or can most fan-out stay in **mutation ledger** scalars?

## Related prior research

- [[simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]]
- [[deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205]]
- [[agency-slice-outcomes-deterministic-state-apply-research-2026-03-22-2315]]
- [[phase-3-3-1-sim-persistence-cross-session-research-2026-03-22-1830]]
