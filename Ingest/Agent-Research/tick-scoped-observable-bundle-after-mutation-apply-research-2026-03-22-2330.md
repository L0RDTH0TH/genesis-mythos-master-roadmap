---
title: "Research — Tick-scoped observable bundle after ordered mutation apply (Phase 3.1.6)"
research_query: "Deterministic post-apply observable bundle per tick_epoch; telemetry contract; TickCommitRecord_v0 bridge; D-027 no wall-clock/thread leakage"
linked_phase: "Phase-3-1-6"
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, simulation, determinism, replay, tick-epoch]
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
research_synthesis_normative_draft: v0
ira_repair_applied: 2026-03-22
agent-generated: true
---

# Tick-scoped observable bundle after ordered mutation apply

Synthesis for **genesis-mythos-master** **Phase 3.1.6** (next slice after **3.1.5** `AgencySliceApplyLedger_v0` / `MutationIntent_v0`): how to define a **deterministic, tick-scoped simulation observable snapshot** (telemetry contract) that (a) **commits hashes only after** the **vault-total-ordered** mutation apply stream finishes for that `tick_epoch`, (b) stays **replay-stable** with **live/replay parity**, (c) **feeds** `TickCommitRecord_v0.committed_sim_observable_hash` and **`replay_row_version`** from **3.1.1**, and (d) excludes **wall-clock and thread-schedule leakage** per **D-027** (stack-agnostic contract; engine names below are **illustrative analogies only**).

**Do not duplicate:** `TickCommitRecord_v0` field list, float-free preimage, `replay_row_version` stub row, `AgencySliceApplyLedger_v0` ordering keys, pause/catch-up coupling, and idempotent `mutation_id` are already normative or drafted in **3.1.1** / **3.1.2** / **3.1.3** / **3.1.5** vault notes. This note focuses on the **observable bundle** *between* “ledger applied” and “tick record emitted.”

---

## 1. Contract goal — one tick, one committed observable view

For each logical `tick_epoch` that **actually advances** under **3.1.2**/**3.1.3**/**3.1.4**/**3.1.5**:

1. **Produce** an ordered `AgencySliceApplyLedger_v0` (may be empty if paused or budget-truncated—must match replay).
2. **Apply** intents in **exact** vault order with **idempotent** `mutation_id` dedupe on replay.
3. **Only after** the apply phase completes for that tick, **snapshot** the **allow-listed observable sim state** into a canonical byte sequence and compute **`committed_sim_observable_hash`** (or a **Merkle root** over named facets—see §3).
4. **Emit** `TickCommitRecord_v0` whose preimage includes that hash plus **barrier / manifest / RNG counter slice** per **3.1.1** (ordering of fields in `preimage_for_tick_hash` stays versioned via `replay_row_version`).

> **Non-normative analogy (not evidentiary for CI):** Event-sourced systems often separate “decide” (commands/events) from “evolve” (state fold). Here, **ordered mutation intents** are the effect stream; **post-apply observation** should be a **deterministic encoding** of state after that stream, given identical **3.1.4–3.1.5** ordering and **CatchUpPolicy_v0** parity (**D-031**). External blog write-ups are **pedagogy only**.  
> [Source: [EventSourcingDB — Decide, Evolve, Repeat](https://docs.eventsourcingdb.io/blog/2026/03/19/decide-evolve-repeat/) — **non-normative**]

---

## 2. Ordering and replay parity (no thread leakage)

**Normative (vault contracts):** Playback applies mutations **only** in the total order defined by **3.1.4** + **3.1.5**, with identical **CatchUpPolicy_v0** truncation (**3.1.2**, **D-031**) and **pause** gating (**3.1.3**). Thread pools or parallel recorders may **stage** work, but **no** alternate order may reach `commit_intent` / observable snapshot.

> **Non-normative analogy:** Industry Q&A on global event ordering illustrates why wall timestamps and machine-local schedules are unsafe as authority; this project’s authority is the **vault-visible sort keys** on intents, not OS scheduling.  
> [Source: [Stack Overflow — deterministic replay / ordering in CQRS](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing) — **non-normative**]

**Observable bundle timing:** Hash **after** the **last** mutation in the tick’s ordered ledger is applied (or after **an explicit** no-op advance path—see §7 when the ledger is empty).

---

## 3. What goes inside `committed_sim_observable_hash` preimage (facet model)

Avoid hashing “the whole heap.” Instead:

| Facet | Examples (project-specific) | Notes |
|-------|----------------------------|--------|
| **Entity bodies** | Position, health, inventory scalars as fixed-point | Align with float-free policy (**3.1.1**) |
| **Authoritative tags / factions** | Small enums + stable IDs | Include only vault-stable IDs, not pointers |
| **RNG namespaces** | Counter snapshot per namespace | Already mirrored in `rng_counters_slice`; keep **one** authoritative representation to avoid double-count drift |
| **Sparse dirty sets** | Optional: only if merge table (**3.1.5**) guarantees commutative aggregation | Otherwise prefer **full allow-list facet** or Merkle of entity records |

**Merkle option:** For large worlds, compute **per-entity or per-chunk hashes**, sort **by stable entity/chunk id**, concatenate, hash root—gives stable **O(n log n)** ordering independent of memory layout. Replay must use the **same** facet graph and **same** sort key function.

**RNG alignment:** If `rng_counters_slice` and observable facets both reflect draws, define **which** is canonical for preimage (**3.1.1** already lists both—avoid updating counters in two places with different rules).

---

## 4. Telemetry fields (tick-scoped, replay-safe) — overview

The **normative field names and bump rules** for downstream tooling are in **§4b**. This section is a **human-readable** overview only.

---

## 4b. `SimObservableBundleTelemetry_v0` (normative draft, research)

**Purpose:** A tick-scoped, replay-safe telemetry object **emitted alongside** (or embedded by reference in) diagnostics; it **does not** replace `TickCommitRecord_v0` but must be **consistent** with `committed_sim_observable_hash`.

| Field | Required | Type (logical) | Semantics |
|-------|----------|----------------|-----------|
| `tick_epoch` | yes | uint64 | Same logical step as `TickCommitRecord_v0` |
| `observable_bundle_schema_version` | yes | semver string | Bump when **any** of: facet set, serialization, Merkle shape, empty-ledger rule, or domain separators change |
| `apply_ledger_checksum` | yes | bytes32 or opaque string | Canonical hash over ordered `MutationIntent_v0` serialization for this tick (align **3.1.5** / **D-036** golden trajectory) |
| `post_apply_observable_root` | yes | bytes32 | **Same** bytes as input to `committed_sim_observable_hash` (before outer domain tag if you use one—document in `serialization_profile_id`) |
| `facet_manifest_id` | yes | string | Registered manifest id (see §8) |
| `serialization_profile_id` | yes | string | Endianness, width, map ordering, string encoding |
| `partial_tick_ledger` | optional | bool | `true` when **3.1.2** budget truncation produced fewer slice intents than a “full” tick; must match replay |

**Bump rule:** Any change that can change **bytes** of `post_apply_observable_root` or `apply_ledger_checksum` ⇒ bump **`observable_bundle_schema_version`** and coordinate **`replay_row_version`** per **3.1.1**.

**Exclude:** wall time, frame ids, thread ids, memory addresses, debug strings without stable intern tables.

---

## 5. Bridge to `TickCommitRecord_v0` and `replay_row_version`

- Any change to **facet set**, **serialization**, **Merkle shape**, or **inclusion rules** for partial ticks ⇒ bump **`replay_row_version`** (and **`observable_bundle_schema_version`** as above).
- `preimage_for_tick_hash` should treat **`committed_sim_observable_hash`** as the **output** of the bundle contract in §3–4b, not as an ad-hoc second hash pass.
- Keep **catch-up** and **pause** behavior visible: if a tick runs **partial** slices, **ledger length and intent set** are part of what makes replay match; the observable bundle is still **post-apply** for **that** partial ledger (same in live/replay).

---

## 6. Failure modes (align with existing desync taxonomies)

| Risk | Mitigation |
|------|------------|
| Hash before apply completes | **Single commit barrier** in tick driver: no `TickCommitRecord_v0` until apply + bundle snapshot |
| Different facet order live vs replay | **Stable sort** by id; document in `serialization_profile_id` |
| Hidden dependence on allocator/layout | **Canonical encoding** only; no struct memcpy |
| RNG drift | One **authoritative** draw ledger; reconcile with **3.1.1** `rng_counters_slice` |

---

## 7. Zero-intent `tick_epoch` and empty `AgencySliceApplyLedger_v0` (normative default for this research draft)

To pin **`committed_sim_observable_hash`** when **no** intents commit in a tick:

1. **Paused (`SimulationRunControl_v0.paused`, 3.1.3):** No slice execution ⇒ **empty** ledger ⇒ **no** `tick_epoch` advance per 3.1.3; **no** `TickCommitRecord_v0` for “skipped” wall time. **No** observable bundle row for a non-advanced tick.
2. **Advanced tick with empty apply ledger** (kernel allows a logical step with zero committed mutations, e.g. explicit idle step): **Still emit** `TickCommitRecord_v0` if the kernel advanced `tick_epoch`. **`committed_sim_observable_hash`** MUST be the **canonical post-apply snapshot** of the **unchanged** observable facet set (i.e. **carry-forward** / **re-hash of prior committed observable state**, not an all-zero sentinel), so replay that applies an empty ledger reproduces the **same** bytes as live. **Do not** omit the hash field when the tick row exists.
3. **Partial tick (3.1.2 truncation):** Observable bundle reflects **only** mutations that **actually** applied in that tick; **`partial_tick_ledger: true`** when the harness exposes truncation. Replay must use the **same** truncated ledger and therefore the **same** post-apply observable root.

**Remaining product tradeoff (does not change bytes once chosen):** full-facet vs Merkle-chunk observable for scale—pick one **`serialization_profile_id`** + **`facet_manifest_id`** pair per build flavor.

---

## 8. `facet_manifest_id` registry (v0 draft, single source in this note)

**Provisional default (until repo CI owns a JSON registry):** Maintain the canonical manifest table **only** at  
`1-Projects/genesis-mythos-master/Roadmap/facet-manifest-v0.md`  
(link from phase **3.1.6** when that note exists; **decisions-log** may cite this path but must not duplicate rows).

Each manifest row: `facet_manifest_id` (string), sorted `facet_id` list, `merkle_mode` (`none` | `entity_root`), `serialization_profile_id` reference.

**Versioning:** New manifest id string on any change to facet membership or sort order; bump **`observable_bundle_schema_version`** when the **active** manifest for a run changes.

---

## Appendix A — `post_apply_observable_root` preimage (ordered fields, toy vector)

**Profile (toy):** `serialization_profile_id: "gmm.toy.v0"` — big-endian uint32/uint64, UTF-8 facet ids, domain tags as ASCII length-prefixed.

**Ordered concatenation (toy flat facet, no Merkle):**

1. Domain tag: `OBS_BUNDLE_V0`
2. `tick_epoch` — uint64
3. `facet_manifest_id` — length-prefixed UTF-8
4. For each entity row sorted by `entity_id` ascending:
   - `entity_id` — length-prefixed UTF-8
   - `x` — int32 fixed sim unit
   - `hp` — uint16

**Toy world after apply (two entities):**

| entity_id | x | hp |
|-----------|---|-----|
| `ent_a` | 10 | 100 |
| `ent_b` | 3 | 50 |

**Expected hash:** `TODO: fill after serialization_profile_id frozen in repo` — replace with **literal** `committed_sim_observable_hash` from the reference harness once **float-free** numeric encoding is pinned under **D-027**. The **structure** above is the falsifiable contract; the **hex** value is execution-gated.

---

## Raw sources (vault)

- [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015|phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]
- [[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045|phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]
- [[Ingest/Agent-Research/agency-slice-outcomes-deterministic-state-apply-research-2026-03-22-2315|agency-slice-outcomes-deterministic-state-apply-research-2026-03-22-2315]]

---

## Sources

- [Stack Overflow — How to replay in a deterministic way in CQRS / event-sourcing?](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing) *(non-normative)*
- [EventSourcingDB — Decide, Evolve, Repeat](https://docs.eventsourcingdb.io/blog/2026/03/19/decide-evolve-repeat/) *(non-normative)*
- [Gaffer on Games — Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/) *(illustrative timing separation only; D-027)*
