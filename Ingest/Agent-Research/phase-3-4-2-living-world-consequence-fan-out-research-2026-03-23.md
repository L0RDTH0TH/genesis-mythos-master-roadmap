---
title: Phase 3.4.2 — Living-world consequence fan-out (ledger, regen lane, observables, persistence)
created: 2026-03-23
tags: [research, agent-research, roadmap, genesis-mythos-master, phase-3-4-2, living-world]
project-id: genesis-mythos-master
linked_phase: Phase-3-4-2
research_query: "living-world consequence fan-out: ambient slices × MutationIntent_v0 / AgencySliceApplyLedger_v0 × TickCommitRecord_v0 × regen_apply_sequence × PersistenceBundle_vN"
research_tools_used: [web_search, vault_context]
research_escalations_used: 0
agent-generated: true
source: vault-first + external light touch
para-type: Resource
status: draft
parent_context:
  queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-251
  parent_run_id: queue-eat-20260323-resume-gmm-251
links:
  - "[[phase-3-4-1-ambient-slice-taxonomy-and-schedule-binding-roadmap-2026-03-23-1620]]"
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]"
  - "[[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]]"
  - "[[decisions-log]]"
---

# Phase 3.4.2 — Living-world consequence fan-out (research synthesis)

Target: **tertiary 3.4.2** after **3.4.1** — how **ambient / living-world** producers fan out into authoritative state **without** breaking **tick-total order**, **replay**, or **cross-session persistence**. This note **extends** [[Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600]] and [[Ingest/Agent-Research/phase-3-4-living-world-operations-research-2026-03-23]]; it does **not** re-derive the ambient slice ID table or RNG matrix.

## 1. Vault contract stack (binding graph)

| Stage | Artifact | Role for 3.4.2 fan-out |
|--------|-----------|------------------------|
| Schedule | `AgencySliceSchedule_v0` + `AgencySliceRow_v0` (**3.1.4**, extended in **3.4.1**) | Ambient slices are **rows** in the same total order as agency; fan-out **starts** here, not in a wall-clock scheduler. |
| Apply | `MutationIntent_v0` → `AgencySliceApplyLedger_v0` (**3.1.5**) | Each slice emits **ordered** intents; merge policy (last-writer / commutative / fail-closed) decides how overlapping ambient writes compose **within** the tick. |
| Observable barrier | `SimObservableBundleTelemetry_v0` + `post_apply_observable_root` (**3.1.6**) | **After** full ordered apply, hashed observables are taken; anything that should affect replay-visible state must be reflected **before** this barrier. |
| Commit | `TickCommitRecord_v0` preimage (**3.1.1**) | Carries tick-close fingerprint; must align with ledger checksum + observable root story. |
| Regen lane | `regen_apply_sequence` + `RegenLaneTotalOrder_v0` A/B (**3.2.3**, **D-044**) | **Subgraph-changing** ambient outcomes **do not** use `StableMergeKey_v0`; they close through **regen lane** before post-regen player/DM merge buffers. |
| Persistence | `PersistenceBundle_vN` + `CompatibilityMatrix_v0` (**3.3.2**, **D-048**) | Long-horizon NPC/environment fields that feed observables belong in the bundle envelope (`last_committed_tick_epoch`, `ledger_tail_ref`, `replay_row_version`, `serialization_profile_id`, etc.). |

**Consequence fan-out (normative direction):** treat “fan-out” as **either** (a) **append-only growth** of the **same-tick** `AgencySliceApplyLedger_v0` under a commutative / ordered merge policy, **or** (b) a **regen-shaped** branch that mutates topology first, then allows **dependent** scalar intents in **post-regen** buffers — with **3.4.1’s provisional** story that **regen_apply_sequence** completes before topology-dependent ambient scalars **until D-044** pins `RegenLaneTotalOrder_v0`.

## 2. Pattern: projections and global order (external)

CQRS / event-sourcing materialized views are **projections** over an **ordered** event stream: replay determinism comes from **reading the store in sequence**, not from message-broker delivery order. For multi-stream / multi-aggregate consumers, practitioners emphasize **a single authoritative ordering** (e.g. global sequence or `$all`-style subscription) so projections do not depend on discovery order.

[Source: Stack Exchange — Replaying projections in order](https://softwareengineering.stackexchange.com/questions/368005/eventsource-cqrs-replaying-projections-of-an-aggregate-in-order)

[Source: Stack Overflow — Deterministic replay in CQRS / event sourcing](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing)

**Map to vault:** `AgencySliceApplyLedger_v0` is the **tick-scoped** analogue of “events to project”; `TickCommitRecord_v0` is the **commit barrier** after projection (apply) completes (**3.1.6**). Ambient fan-out must not introduce a **second** ordering source.

## 3. Pattern: commutative merges vs rebuild (external)

CRDT-style structures guarantee convergence under **commutative** merge semantics; they are a useful **metaphor** for the vault’s “commutative under `MutationIntent_v0`” path (**D-036** matrix TBD). They **do not** replace regen when subgraph scope changes — rebuild/regen corresponds to **non-commutative** topology change, which the vault routes to **`RegenRequest_v0`** (**3.2.2**) and **`regen_apply_sequence`** (**3.2.3**).

[Source: Wikipedia — Conflict-free replicated data type](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)

## 4. Recommended 3.4.2 design checklist (draft)

1. **Classify each ambient fan-out edge:** commutative ledger append vs `SLICE_STATE_CONFLICT` vs `RegenRequest_v0` (reuse **3.4.1** decision tree; add **explicit** “dependent scalar after regen” placeholder keyed to **D-044**).
2. **Ledger row shape:** ensure ambient-produced intents carry stable `mutation_id` / `target_key` (**3.1.5**); multi-hop fan-out (A affects B affects C) stays **within** the same tick only if bounded by **3.1.2** substeps and reflected in **schedule rows** (deferral rule from **3.4.1**).
3. **Observable coupling:** any field that feeds `post_apply_observable_root` must be updated **before** the **3.1.6** barrier; document which ambient facets are allow-listed (**facet_manifest** / **D-037** gaps).
4. **TickCommitRecord coupling:** tick-close preimage must include **final** `regen_apply_sequence` digest when regen ran (**3.2.3**); ambient scalars that assume regen layout must not commit **ahead** of that sequence under the **provisional D-044** ordering note.
5. **PersistenceBundle:** for cross-session NPC/environment state, pin **`bundle_schema_version`**, **`last_committed_tick_epoch`**, **`ledger_tail_ref`**, **`replay_row_version`**, **`serialization_profile_id`** (**3.3.2**); run **CompatibilityMatrix_v0** before mutating hashed observables after resume.

## 5. Open questions (explicit ties)

- **D-044:** Until **RegenLaneTotalOrder_v0** Option **A** (multi-regen tuple order) vs **B** (≤1 regen/tick) is logged, **do not** normatively assert a single interleaving story for **same-tick** ambient scalars + regen; keep **two** illustrative narratives in vault prose labeled **provisional**.
- **D-032:** Golden / `replay_row_version` / header freeze still blocks literal registry rows; consequence fan-out examples stay **pseudocode-only** until coordinated bump.
- **D-036:** Per-component merge matrix (commutative vs last-writer) remains TBD; ambient faction propagation may need **explicit** merge rows to avoid silent convergence.

## 6. Related vault research

- [[Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600]]
- [[Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830]]
- [[Ingest/Agent-Research/agency-slice-outcomes-deterministic-state-apply-research-2026-03-22-2315]]
- [[Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330]]

## Sources

- [Stack Exchange — CQRS replay / projection order](https://softwareengineering.stackexchange.com/questions/368005/eventsource-cqrs-replaying-projections-of-an-aggregate-in-order)
- [Stack Overflow — Deterministic replay in CQRS / event sourcing](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing)
- [Wikipedia — CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)
- [Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) (cross-session snapshot narrative; already cited on **3.4** secondary)
- [Gaffer On Games — Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/) (logical tick discipline; aligns with deferral / catch-up)

## Raw sources (vault)

- No separate raw note for this run; sources above were fetched for this synthesis. Prior vault synthesis notes linked in §6.
