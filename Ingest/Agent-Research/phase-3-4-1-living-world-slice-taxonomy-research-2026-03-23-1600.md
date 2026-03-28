---
title: Phase 3.4.1 — Living world slice taxonomy (ambient sim, RNG streams, regen/persistence touchpoints)
created: 2026-03-23
tags: [research, agent-research, genesis-mythos-master]
project-id: genesis-mythos-master
linked_phase: Phase-3-4-1
agent-generated: true
research_query: "Phase 3.4.1 ambient slice taxonomy AgencySliceSchedule MutationIntent RegenRequest PersistenceBundle coupling"
research_tools_used: [web_search]
research_escalations_used: 0
research_escalation_note: "Pre-deepen run skipped Step 1b; literal registry rows and D-044 total order remain vault-TBD — see research_open_decisions."
research_escalations_used_note: "Nested IRA after validator is not research-agent-run Step 1b query escalation; ira_applied documents Validator→IRA→repair cycle."
research_open_decisions: [D-032, D-044, D-047]
research_focus: junior_handoff
parent_context:
  queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-250
  parent_run_id: queue-eat-20260322-gmm-deepen-250
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-living-world-operations-research-2026-03-23]]"
  - "[[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]]"
  - "[[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]"
  - "[[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]"
  - "[[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]]"
  - "[[decisions-log]]"
ira_applied: true
ira_call_index: 1
---

# Phase 3.4.1 — Living world slice taxonomy (research synthesis)

**Scope:** First tertiary under **Phase 3.4** — how **ambient** NPC / weather / faction work becomes **tick-scoped mutations** bound to **`AgencySliceSchedule_v0`**, **`MutationIntent_v0`**, **`RegenRequest_v0`**, and **`PersistenceBundle_vN`**, without duplicating the broader 3.4 secondary narrative in [[phase-3-4-living-world-operations-research-2026-03-23]].

**Do not duplicate (vault):** Fixed timestep + lockstep mindset + four-pattern table from that note; here we add **slice ID taxonomy**, **RNG stream matrix**, and **explicit 3.2 / 3.3 handoff predicates**.

---

## 1. Slice taxonomy (ambient as first-class schedule rows)

Treat **living-world producers** as **additional `AgencySliceId_v0` values** (or a reserved namespace `AMBIENT::*`) slotted into the **same** `tick_epoch` schedule as player/DM agency slices — **no second wall-clock scheduler** that commits authoritative state.

**Proposed slice labels (non-canonical until D-032 registry rows and coordinated `replay_row_version` bumps):**

| Slice class | Role | Typical `MutationIntent_v0` payloads |
|-------------|------|--------------------------------------|
| **AMBIENT_NPC_ROUTINE** | Deterministic NPC routine step (path segment, job queue tick) | Scalar field updates, inventory deltas commutative under 3.1.5 merge rules |
| **AMBIENT_WEATHER_PHASE** | Environmental phase machine advance | Region-scoped scalars / enums; avoid proc hooks that reorder later slices |
| **AMBIENT_FACTION_PROPAGATION** | Stance / territory / rumor fan-out reducers | Prefer **commutative** merges; non-commutative overlap → `SLICE_STATE_CONFLICT` or regen path |

**Stable ordering:** Each slice row carries the same **`tick_epoch`**, **`slice_index`**, and **`tie_break_key`** contract as **D-034** — extend the registry so ambient IDs participate in **one** total order. Starvation credits from **3.1.4** apply to ambient slices the same as agency slices when they share a fairness class.

**Tick budget rule:** If ambient work risks exceeding per-tick bounds, **defer** by emitting **no mutation** this tick and carrying **explicit deferred work ids** in slice-local state that is itself ledger-written — never by skipping schedule positions or reordering. This matches the **accumulator / fixed logical step** pattern: wall-clock variance must not change how many logical ticks execute in a replay window — see [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) for the separation of render vs simulation cadence; vault’s **`tick_epoch`** is the authoritative logical step.

---

## 1b. Draft `AgencySliceId_v0` rows (vault-TBD — not authoritative)

| slice_id (draft) | tie_break_key (sketch) | fairness_class (sketch) |
|------------------|------------------------|-------------------------|
| `AMBIENT_NPC_ROUTINE` | `hash("AMBIENT_NPC", actor_id, routine_step)` | `ambient` |
| `AMBIENT_WEATHER_PHASE` | `hash("AMBIENT_WEATHER", region_id, phase_epoch)` | `ambient` |
| `AMBIENT_FACTION_PROPAGATION` | `hash("AMBIENT_FACTION", faction_id, wave_seq)` | `ambient` |

Replace literals at **D-032** replay header freeze; until then treat as **design shorthand** only.

---

## 2. RNG namespace isolation (ambient vs agency)

**Invariant:** RNG draws occur **after** schedule order is fixed (**D-034**: RNG consumption **after** schedule order). Within that constraint, **partition streams** so ambient variety does not consume entropy from combat / proc / agency-critical streams — same discipline as deterministic lockstep: **inputs + ordering** define replay; see [Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/).

**Practical pattern (handoff-friendly):**

1. **Derive** a small set of logical stream ids, e.g. `agency_core`, `ambient_weather`, `ambient_npc_idle`, `ambient_faction_jitter`, `presentation_only` (last must not feed back into preimage).
2. For each `(tick_epoch, slice_index, stream_id)` triple, use an **independent deterministic stream** (e.g. PCG-style stream index) seeded from **replay-safe header fields** — not from wall clock.

[Source: PCG random — useful features (streams)](https://www.pcg-random.org/useful-features.html)

3. **Ban** “global RNG bump” shared across slice classes without a documented **total order** of draws; otherwise two slices can race in implementation refactors.

**Agency vs ambient:** Player/DM slices use **`agency_core`** (and linked proc hooks per **2.1.2**); ambient slices draw **only** from their ambient stream ids. Presentation layers may use `presentation_only` with **no** write-back.

*(Optional industry reading, non-normative: [Daydreamsoft — deterministic simulation](https://www.daydreamsoft.com/blog/deterministic-simulation-for-lockstep-multiplayer-engines).)*

---

## 3. Regen touchpoints vs Phase 3.2.x

Align with **`RegenRequest_v0`** (**3.2.1** / **3.2.2**) and **regen-before-merge** ordering:

- **Scalar / commutative** faction or weather fields → **ledger mutations only**; no regen.
- **Subgraph-changing** outcomes (new POI layout, regenerated territory mesh, proc chunk swap) → **`RegenRequest_v0`** with **P1–P6** preconditions satisfied **before** merging player/DM intents that assume prior topology.

### Provisional D-044 story (genesis-mythos-master — until operator pin)

**Working assumption for this vault slice:** Within a single **`tick_epoch`**, any **regen-shaped** ambient outcome **enqueues `RegenRequest_v0` and completes regen-lane apply** (per **3.2.x** ordering sketch) **before** remaining **scalar** `AMBIENT_FACTION_PROPAGATION` / weather intents that depend on finalized topology are appended to **`AgencySliceApplyLedger_v0`**. This is **provisional** — formal total order belongs in [[decisions-log]] once **D-044** selects **RegenLaneTotalOrder_v0** A vs B.

- **D-044 fork:** Until **`RegenLaneTotalOrder_v0`** A/B is pinned, do **not** assert CI goldens; keep one consistent story per project.

---

## 3b. Ambient faction × player-scoped slice — merge outcome matrix (placeholder)

|  | Commutative scalar merge | `SLICE_STATE_CONFLICT` | Escalate `RegenRequest_v0` |
|--|--------------------------|------------------------|----------------------------|
| Ambient faction × player-scoped slice | When field paths disjoint per merge table | Non-commutative overlap on shared keys | Subgraph / proc topology invalid |

Registry literals for conflict codes: **TBD** with **3.1.5** merge policy matrix (**D-036** deferrals).

---

## 4. Persistence touchpoints vs Phase 3.3.x

Cross-session **ambient** state (long-horizon faction stance, climate phase, off-screen NPC summaries) must ride **`PersistenceBundle_vN`** with **`CompatibilityMatrix_v0`** outcomes (**D-048**):

- On **save / checkpoint**, bundle pins **`replay_row_version`**, **`serialization_profile_id`**, lineage, and last committed **`tick_epoch`** (per **3.3.2** alignment).
- On **load**, run **preflight** tolerant-reader → upcast → snapshot rewrite **before** any code path mutates **hashed observables**; failed matrix path → fail-closed, not silent merge.

[Source: Event sourcing — snapshots as resume accelerators](https://martinfowler.com/eaaDev/EventSourcing.html)

[Source: Snapshots in event-sourced systems](https://www.eventsourcing.dev/first-principles/snapshots)

**Coupling to regen:** If resume encounters a bundle that implies **incomplete regen** (partial subgraph), **3.2.2** failure codes win — surface `REGEN_SUBGRAPH_PARTIAL` / registry equivalents rather than continuing apply.

---

## 5. Minimal pseudocode sketch (scheduling + RNG + regen lane)

**Non-CI / non-golden until D-044 pinned** — narrative only.

```text
for each row in AgencySliceSchedule_v0 ordered by (tick_epoch, slice_index, tie_break_key):
  if row requires_regen_first (subgraph-changing ambient outcome):
    enqueue RegenRequest_v0 with P1–P6 checks
    await regen_apply_sequence completion for this tick_epoch  // D-044 defines lane vs tick interleaving
  stream := select_rng_stream(row.slice_id)  // agency_core vs ambient_*
  with_rng_stream(stream):
    intents := produce_mutation_intents(row)   // may be empty if budget exceeded
    for intent in ordered(intents):
      append AgencySliceApplyLedger_v0 (MutationIntent_v0, mutation_id idempotent)
```

---

## 6. Open items (for tertiary roadmap note)

- Literal **`AgencySliceId_v0` registry rows** for each ambient class (blocked on **D-032** / coordinated **`replay_row_version`** bumps).
- Per-class **merge matrix** when **AMBIENT_FACTION_PROPAGATION** collides with player-scoped slices (non-commutative cases) — stub in **§3b** until **D-036** execution.
- Golden row: **one tick** with mixed ambient + agency + optional regen request — **TBD** until **D-044** resolved.

---

## 7. Actionable next tasks (junior-sized)

1. Copy **§1b** draft rows into the Phase **3.4.1** tertiary roadmap note as a checklist with **TBD** literals column.
2. Log **provisional D-044 story** (§3) into [[decisions-log]] when operator approves, or mark superseded when A/B chosen.
3. Extend **3.1.5** merge matrix with one **ambient × player** example row (**D-036**).
4. Add **one** golden-tick trace row spec (no CI) after **D-044** pin — columns: `tick_epoch`, ordered `slice_id` list, `stream_id` per slice, `mutation_id` prefixes produced.
5. Align **PersistenceBundle_vN** field list for long-horizon ambient keys with **3.3.2** envelope (**D-048**).

---

## 8. Golden-tick narrative (epoch N — non-blocking trace)

1. **Slice order:** `AGENCY_PLAYER` → `AGENCY_DM` → `AMBIENT_WEATHER_PHASE` → `AMBIENT_FACTION_PROPAGATION` → `AMBIENT_NPC_ROUTINE` *(illustrative only)*.
2. **Per slice:** select `stream_id` (`agency_core` vs `ambient_*`); run producers; emit `MutationIntent_v0` list or `RegenRequest_v0` if subgraph-changing.
3. **Regen gate:** Before any player merge that assumes topology, verify **3.2.2** P1–P6; on failure emit fail-closed `reason_code` — **no golden assert** until **D-044** + registry freeze (**D-043**).

## Raw sources (vault)

- Prior synthesis (secondary context, do not re-copy): [[phase-3-4-living-world-operations-research-2026-03-23]]

## Sources

- [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [PCG — useful features (streams)](https://www.pcg-random.org/useful-features.html)
- [Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Snapshots — Event Sourcing Guide](https://www.eventsourcing.dev/first-principles/snapshots)
- [Deterministic simulation — Daydreamsoft](https://www.daydreamsoft.com/blog/deterministic-simulation-for-lockstep-multiplayer-engines) *(optional)*
