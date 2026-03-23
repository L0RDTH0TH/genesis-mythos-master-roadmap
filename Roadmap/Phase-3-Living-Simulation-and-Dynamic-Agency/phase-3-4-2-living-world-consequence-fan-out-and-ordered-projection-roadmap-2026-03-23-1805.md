---
title: Phase 3.4.2 — Living world consequence fan-out and ordered projection
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-23
tags: [roadmap, genesis-mythos-master, phase, living-world, fan-out, ledger, observables]
para-type: Project
subphase-index: "3.4.2"
handoff_readiness: 86
execution_handoff_readiness: 46
handoff_readiness_scope: vault-normative draft — ordered projection chain ledger→observable→tick commit; same-tick regen vs ambient scalars provisional until D-044; golden rows TBD (D-032 / D-043)
handoff_gaps:
  - "Normative same-tick interleaving for regen_apply_sequence vs dependent ambient MutationIntent_v0 rows remains dual-track until D-044 A/B is logged in decisions-log"
  - "Literal replay_row_version / registry golden rows blocked per D-032 — examples stay pseudocode-only"
  - "D-036 merge matrix extension for ambient faction reducers vs SLICE_STATE_CONFLICT is TBD"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-1-ambient-slice-taxonomy-and-schedule-binding-roadmap-2026-03-23-1620]]"
  - "[[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]"
  - "[[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]]"
  - "[[Ingest/Agent-Research/phase-3-4-2-living-world-consequence-fan-out-research-2026-03-23.md]]"
  - "[[distilled-core]]"
  - "[[decisions-log]]"
---

## Phase 3.4.2 — Living world consequence fan-out and ordered projection

> **Architect:** After **3.4.1** names *what* runs in the tick (ambient slice rows), **3.4.2** binds *how consequences become authoritative state* — one ordered apply stream per `tick_epoch`, then the **3.1.6** observable barrier, then **TickCommitRecord_v0**.

### TL;DR

- **Fan-out = projection:** Ambient slice outputs emit **`MutationIntent_v0`** rows into **`AgencySliceApplyLedger_v0`** in **schedule order** (**3.1.4** / **3.4.1**). No second broker or wall-clock ordering authority.
- **Barrier:** **`SimObservableBundleTelemetry_v0`** / **`post_apply_observable_root`** runs only after **all** ledger applies for the tick complete (**3.1.6**). **`TickCommitRecord_v0`** closes on that barrier (**3.1.1**).
- **Topology edits:** Subgraph-changing ambient paths use **`RegenRequest_v0`** + **`regen_apply_sequence`** (**3.2.3**); **`StableMergeKey_v0`** applies **after** regen lane, not instead of it (**D-044** fork still **TBD** in decisions-log).
- **Persistence:** Long-horizon NPC/environment fields that participate in hashed observables must round-trip through **`PersistenceBundle_vN`** + **`CompatibilityMatrix_v0`** preflight (**D-048**) and **`ResumeCheckpoint_v0`** tail refs (**D-047**).

## Ordered apply sketch (pseudocode)

```text
on_tick_close(tick_epoch):
  ledger = AgencySliceApplyLedger_v0.for_tick(tick_epoch)
  for intent in ledger.ordered_mutation_intents():  // total order from schedule + tie_break
    apply_mutation_intent(intent)  // idempotent mutation_id; merge policy per D-035/D-036
  bundle = build_SimObservableBundleTelemetry_v0(post_apply_state)
  assert post_apply_observable_root(bundle) aligns TickCommitRecord_v0.committed_sim_observable_hash
  publish TickCommitRecord_v0(...)
```

## Tasks

- [ ] Document **failure-closed** paths when ambient fan-out would exceed **3.1.2** catch-up budget (defer via idempotent ledger row; never reorder schedule).
- [ ] Cross-link **regen_apply_sequence** fingerprint ordering to **ambient** rows that must wait for regen completion (**provisional** narrative A vs B per **D-044**).
- [ ] Add **facet-manifest** allow-list intent for which ambient facets may appear in **`post_apply_observable_root`** before claiming **3.1.6** coupling (**D-037**).

### Task ledger (DEFERRED / BLOCKED)

| Task (above) | WAITING_ON | Notes |
| --- | --- | --- |
| Catch-up failure-closed paths | **3.1.2** policy numerics + **D-031** replay-live parity | Document deferral via idempotent ledger row only after budget bits are frozen in golden replay |
| Regen ↔ ambient ordering cross-link | **D-044** A/B (operator) | Provisional narrative allowed; normative single interleaving forbidden until logged in [[decisions-log]] |
| Facet-manifest allow-list | **D-037** + **D-032** / **D-043** | `serialization_profile_id` + registry rows TBD |

## Research integration

- **Binding chain:** `AgencySliceSchedule_v0` (ambient rows) → `MutationIntent_v0` / `AgencySliceApplyLedger_v0` (**3.1.5**) → ordered apply → `SimObservableBundleTelemetry_v0` + `post_apply_observable_root` (**3.1.6**) → `TickCommitRecord_v0` (**3.1.1**). Subgraph-changing ambient work → `RegenRequest_v0` + `regen_apply_sequence` (**3.2.3**); **not** `StableMergeKey_v0`.
- **CQRS analogy:** Read models / projections must consume a **single authoritative ordered stream** for deterministic replay — same role as the per-tick apply ledger vs broker order ([Source: SE — replay projections in order](https://softwareengineering.stackexchange.com/questions/368005/eventsource-cqrs-replaying-projections-of-an-aggregate-in-order)).
- **Commutative fan-out:** CRDT-style **commutative merge** is the external metaphor for the vault’s commutative path under `MutationIntent_v0`; it does **not** replace regen for topology edits ([Source: Wikipedia — CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)).

### Cited takeaways

1. **Single stream per tick:** All ambient consequences that affect authoritative state should appear as **ordered intents** in `AgencySliceApplyLedger_v0`, keyed by schedule order + `mutation_id` idempotency (**3.1.5**).
2. **Barrier after apply:** No `TickCommitRecord_v0` / observable hash until **all** intents for the tick are applied in vault order (**3.1.6**).
3. **Regen lane isolation:** `regen_apply_sequence` uses **RegenLaneTotalOrder_v0** (A/B **D-044**); merge buffers for player/DM use `StableMergeKey_v0` **only post-regen** (**3.2.3**).
4. **Persistence envelope:** Long-horizon NPC/environment fields → `PersistenceBundle_vN` with `last_committed_tick_epoch`, `ledger_tail_ref`, `replay_row_version`, `serialization_profile_id`; preflight via `CompatibilityMatrix_v0` (**3.3.2** / **D-048**).
5. **Deferral:** Multi-hop fan-out within one tick must respect **3.1.2** budgets and **3.4.1** deferral (carry deferred work via idempotent ledger rows, not hidden threads).

### Open questions (decisions)

- **D-044:** Which normative story for **same-tick** regen vs dependent ambient scalars — Option **A** (multi-regen ordering) vs **B** (≤1 regen/tick)? Vault must not assert a single interleaving until logged in [[decisions-log]].
- **D-032:** Replay header / `replay_row_version` freeze still blocks literal golden rows and registry authority; keep **3.4.2** examples **pseudocode-only** until coordinated bump.
- **D-036:** Ambition-specific **merge matrix** rows for ambient reducers vs `SLICE_STATE_CONFLICT` — TBD; affects faction propagation fan-out.

### Links

- Synthesis: [[Ingest/Agent-Research/phase-3-4-2-living-world-consequence-fan-out-research-2026-03-23.md]]
- Prior: [[Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600]], [[Ingest/Agent-Research/phase-3-4-living-world-operations-research-2026-03-23]]
