---
title: RegenRequest_v0 — gated regeneration subgraph, ManifestEmit boundary, and hash-chain bumps
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, regen, determinism, intent-plan]
source: "Vault: phase-3-2-1, phase-2-2-2, phase-3-1-1, decisions-log D-027/D-041; conceptual patterns (no engine binding)"
linked_phase: Phase-3-2-2
project_id: genesis-mythos-master
research_query: "RegenRequest_v0 preconditions, regen_scope allow-list, ManifestEmit / IntentPlan consumption, idempotency, CRDT/event-sourcing analogies (D-027)"
agent-generated: true
research_tools_used: [vault]
---

## Purpose

Draft **consumables** for roadmap deepen on **`RegenRequest_v0`**: explicit seed, **`regen_scope`** allow-list, precondition vs denial table, interaction with **Phase 2.2.2** (`ManifestEmit` / `IntentPlan` consumption), **idempotency** and **hash-chain bumps** (`regen_gate_version_id` ↔ `replay_row_version`), plus **stack-agnostic** comparison to CRDT / event-sourcing replay patterns in games (**D-027**: examples are analogies, not product stack).

## Normative anchors (vault)

- [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]] — split **`DmOverrideIntent_v0`** vs **`RegenRequest_v0`**; regen must not emit **`ManifestEmit`** without passing [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]; **`regen_gate_version_id`** aligns with **`replay_row_version`** on [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]].
- [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]] — pinned boundary: consumption at **manifest-emission**; `ReplayAndVerify` ledger key includes **`deterministic_gate_version_id`**; double-apply → **`ledger-hit`**.
- [[decisions-log]] — **D-041** adopts 3.2.1 draft; **D-027** stack-agnostic contract.

## Proposed `RegenRequest_v0` fields (v0 sketch)

| Field | Role |
|--------|------|
| `domain_tag` | Literal `REGEN_REQUEST_V0` (registry row TBD with 2.2.1) |
| `regen_request_id` | Bytes32 idempotency key (dedup in regen ledger, parallel role to intent `intent_id` / mutation ids) |
| `tick_epoch` | Bind regen to the tick under which it is requested (same family as 3.1.1) |
| `regen_seed` | **Explicit** deterministic seed material (hash of operator-approved inputs, subgraph version, prior manifest refs — **no** wall-clock); feeds gated subgraph RNG / procedural inputs only inside allow-listed scope |
| `regen_scope` | **Allow-list** of stage / facet / entity-set ids the subgraph may read or rewrite (closed enum or bounded bitset per policy) |
| `regen_gate_version_id` | Bumps when outputs would change **any** byte in **IntentPlan → manifest** preimage chain or **TickCommitRecord** preimage family; must co-register with **`replay_row_version`** / **`deterministic_gate_version_id`** when regen affects those rows |
| `upstream_manifest_ref` / `barrier_ref` | Optional pointers proving regen runs **after** terminal barrier / ledger tail (align 2.1.3 / SpawnCommit story) |
| `expected_precondition_fingerprint` | Optional hash of world slice required **before** regen; mismatch → single denial |

## Precondition table (allowed vs denied)

| # | Precondition | If true | If false — `reason_code` (draft) |
|---|----------------|---------|----------------------------------|
| P1 | `regen_scope` ⊆ policy allow-list | proceed gated subgraph | `REGEN_SCOPE_OVERFLOW` |
| P2 | `regen_seed` present and canonical | deterministic regen | `REGEN_PRECONDITIONS_FAILED` (generic) or dedicated `REGEN_SEED_INVALID` when registry frozen |
| P3 | No partial manifest: regen either completes subgraph **or** emits **one** denial | safe replay | `REGEN_SUBGRAPH_PARTIAL` (new row candidate) |
| P4 | Regen does not skip **IntentPlan validation + hash wiring** before any `ManifestEmit` | 2.2.2 satisfied | `OVERRIDE_MANIFEST_BYPASS` |
| P5 | Any change to hash preimages ⇒ **`regen_gate_version_id`** bumped and reflected in golden registry / CI | no silent drift | `REGEN_HASH_CHAIN_DRIFT` |
| P6 | Idempotent replay: same `regen_request_id` + same inputs ⇒ same outcome; second apply ledger-hit | aligns with 2.2.2 ledger | `REGEN_IDEMPOTENCY_VIOLATION` (optional new row) |

**Ordering note (from 3.2.1 sketch):** run **gated regen** for all `regen_requests` **before** merging player + DM intents for tick apply, so overrides see post-regen world; failures return **one** denial and do not emit manifest fragments.

## Interaction with ManifestEmit / IntentPlan (2.2.2)

- **Consumption boundary:** Any structural output that would feed **`manifest_hash`** / spawn ordering must go through the same **canonicalize → validate → `intent_hash` / chain** path (or a **documented parallel domain** that still lands in `ReplayAndVerify`). Regen is **not** a side door: either (a) regen outputs are expressed as **replay-logged commands** consumed at the same boundary, or (b) regen only mutates **pre-IntentPlan** internal buffers that are **re-derived** into a fresh validated `IntentPlan` before `ManifestEmit`.
- **`deterministic_gate_version_id`:** When regen algorithms change, bump **gate** id in lockstep with **`regen_gate_version_id`** and registry rows per **D-020**.

## Idempotency and hash-chain bumps

- **Ledger pattern:** Mirror 2.2.2: `ledger_key := (stage_graph_version, boundary_id, regen_request_id, regen_gate_version_id)`; first apply `applied`, second `ledger-hit`; assert no extra mutations.
- **Tick record coupling:** If regen affects **`TickCommitRecord_v0`** fields (`manifest_or_ledger_tail_ref`, `committed_sim_observable_hash`, etc.), **`replay_row_version`** (3.1.1) must bump or the row is invalid → **`REGEN_HASH_CHAIN_DRIFT`** / **`TICK_PREIMAGE_DRIFT`** family.

## CRDT / event-sourcing replay (high level, D-027)

**Analogy only — no implied engine or library choice.**

- **Event sourcing:** Regen is a **scoped reducer** over a **prefix** of the log: allowed if the reducer is **pure** w.r.t. the allow-listed projection and **replays identically** from `(regen_seed, regen_scope, version ids)`. Denials are **events** with stable codes (same spirit as 2.2.1 denials).
- **CRDT-style merge:** If multiple lanes could regenerate overlapping data, the **allow-list** + **total order** (cf. `StableMergeKey_v0` for DM/player) prevent ambiguous merge; regen does not introduce implicit **last-write-wins** without a recorded version bump.
- **Game/sim patterns:** Deterministic lockstep / replay systems treat **simulation** as a pure function of **inputs + seed + prior committed state**; regen fits that mold when **`regen_seed`** and **`regen_scope`** fix the **input tuple** and **mutable surface**.

## Raw sources (vault)

- [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]
- [[phase-3-2-1-dm-override-vs-regeneration-gates-synthesis-2026-03-22]]
- [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]
- [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]
- [[decisions-log]]

## Sources

- Vault phase notes and decisions above; external URLs not required for this vault-first pass.
