---
title: Phase 3.2.3 — Replay rows, regen ledger idempotency, regen_apply_sequence vs TickCommitRecord_v0
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, replay, regen, tick-commit, event-sourcing]
source: "Vault phase notes + illustrative event-sourcing / lockstep literature (D-027: analogies only)"
linked_phase: Phase-3-2-3
project_id: genesis-mythos-master
research_query: "Deterministic replay rows for regen subgraph; idempotent regen ledger keys; regen_apply_sequence before player+DM intents in TickCommitRecord_v0; event sourcing patterns"
agent-generated: true
research_tools_used: [vault, web_search]
research_escalations_used: 0
synthesis_revision: v0.1
---

## Purpose

Consumables for **Phase 3.2.3** (next tertiary after 3.2.2): how **deterministic replay** should record **regeneration subgraph** outcomes; **idempotent** keys for a **regen ledger**; where **`regen_apply_sequence`** sits relative to **player + DM** intents before closing **`TickCommitRecord_v0`**; and how **event-sourced / command-log** idioms (illustrative only per **D-027**) inform those choices without binding engine or language.

## Vault anchors (normative draft context)

- [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]] — `RegenRequest_v0`, P1–P6, **regen-before-merge**, `regen_request_id` as idempotency key, `regen_gate_version_id` ↔ `replay_row_version`.
- [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]] — **`StableMergeKey_v0`** total order for `concat(player_intents, dm_overrides)` **after** regen completes — see **Phase boundary** below.
- [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] — `TickCommitRecord_v0` preimage family, replay log / stub row, version bumps.
- [[decisions-log]] — **D-027** (stack-agnostic; examples non-binding), **D-042** (3.2.2 adoption).

**Phase boundary (explicit):** **`StableMergeKey_v0`** applies **only** to the **post-regen** merge of **player + DM** intents. **Regen** commands are **not** sorted with that key; they occupy a **prior phase** with a **separate** total-order contract (see **Regen lane total order**). This matches [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]] regen-before-merge narrative.

**Do not duplicate:** Full `RegenRequest_v0` field table and P1–P6 text already live in [[Ingest/Agent-Research/regenrequest-v0-gated-subgraph-determinism-research-2026-03-22|regenrequest-v0 research]] and phase 3.2.2; this note extends **ordering inside the tick record** and **replay row shape** for regen.

## 1. Deterministic replay rows for regeneration subgraph outcomes

**Intent:** A replay driver must reproduce **the same committed observables** as live without relying on wall-clock or hidden caches. Regen is a **scoped, seeded** transform; its **outcome** must be representable as **replay-visible data** (not only in-memory).

**Suggested row semantics (v0 sketch):**

| Row concept | Role |
|-------------|------|
| `regen_apply_sequence` | Ordered list (or merkle-friendly digest) of **accepted** `RegenRequest_v0` applications for the tick **before** intent merge. Each element includes `regen_request_id`, `regen_gate_version_id`, outcome fingerprint (success hash or stable denial code + payload hash). |
| `regen_subgraph_outcome_row` | See **Decision rule** below — not “optional” without a criterion. |
| `replay_row_version` coupling | Any change to how these rows serialize → bump **`replay_row_version`** / **`regen_gate_version_id`** per 3.2.2 / 3.1.1. |

### When to emit `regen_subgraph_outcome_row` (golden / harness rule)

- **Emit a distinct per-request structured row** when CI or golden vectors must **diff subgraph outputs** (e.g. `subgraph_hash_out`, `denial_reason_code`, `manifest_pre_delta_ref`) **without** re-running ML, network IO, or heavyweight procedural passes.
- **Fold outcomes only into `regen_apply_sequence` elements** when tests assert **end-to-end tick observables** only and do not require per-regen structured diff — still keep **element-level** outcome fingerprints so replay can detect drift.

**Determinism rule:** The subgraph reducer must be a **pure function** of `(regen_seed, regen_scope, tick_epoch, prior committed state slice, version ids)` so **live vs replay** share one **canonical serialization** into the row.

[Source: Gaffer on Games — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — inputs and simulation ordering must align across peers for identical state; same spirit for **logged regen inputs**.

[Source: Daydreamsoft — deterministic simulation / lockstep overview](https://www.daydreamsoft.com/blog/deterministic-simulation-for-lockstep-multiplayer-engines) — fixed time steps + identical input streams → identical results; regen should appear as **explicit inputs** in that stream.

## 2. Idempotent regen ledger keys

**Problem:** At-least-once delivery, retries, and crash recovery **will** re-present the same `RegenRequest_v0`. The ledger must **dedupe** without double-applying side effects that touch **manifest preimage** or **TickCommitRecord**.

**Normative pattern (vault):** Per [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]] and [[Ingest/Agent-Research/regenrequest-v0-gated-subgraph-determinism-research-2026-03-22]] — mirror **2.2.2** ledger semantics:

- **Primary key:** `regen_request_id` (bytes32) **+** `regen_gate_version_id` (or explicit `ledger_key` tuple registered in CI).
- **First apply:** append row `applied` with outcome digest.
- **Duplicate:** second identical command → **`ledger-hit`** (no state mutation); replay must reproduce **`ledger-hit`** vs **`apply`** from the **same** logged sequence (see **Durability**).

Industry blogs discuss the same *idea* (dedupe tables, idempotent handlers); they are **not** normative for this contract — see **Further reading (non-normative)** at the end.

[Source: EventSourcingDB — event handlers and deduplication](https://docs.eventsourcingdb.io/best-practices/building-event-handlers/) — *D-027 analogy:* processed-position / handler idempotency.

## 3. `regen_apply_sequence` before player + DM intents in `TickCommitRecord_v0`

**Policy (from 3.2.1 / 3.2.2):** **Regen-before-merge** — gated regen runs **before** merging player and DM intents so overrides observe **post-regen** world.

### Regen lane total order (`RegenLaneTotalOrder_v0` — v0 policy options)

Pick **one** for 3.2.3 normative text (both are fully specified here; product chooses):

- **Option A — Multi-regen per tick:** Define tuple **`(tick_epoch_u64_be, regen_lane_sequence_u32_be, regen_request_id_lex)`** — unsigned integers **big-endian** for cross-platform stability; `regen_request_id` compared **lexicographically** as fixed 32-byte array. This order **does not** share key space with **`StableMergeKey_v0`** on player/DM intents (different phase, different tuple type).
- **Option B — At most one accepted regen per tick:** If a second `RegenRequest_v0` arrives after one has **applied** successfully in the same `tick_epoch`, either **reject** the second with a stable `reason_code` (registry TBD) or **abort the tick** as a policy decision — document which. Replay then has **zero or one** regen application per tick, simplifying ordering.

**Serialization order inside the tick (v0 proposal):**

1. **Close or carry** any **barrier / ledger tail** prerequisites (spawn/manifest lanes per 2.x family) — **regen must not skip** consumption boundaries in 2.2.2.
2. **Emit `regen_apply_sequence`** ordered per **Option A** or **Option B** above.
3. **Merge player + DM** via **`StableMergeKey_v0`** on `concat(player_intents, dm_overrides)` — **post-regen** only.
4. **Apply** through mutation ledger → observable bundle → **only then** finalize **`TickCommitRecord_v0`** fields (`committed_sim_observable_hash`, ledger tail refs, etc.) per 3.1.1 / 3.1.6.

**Why separate sequences matter:** Mixing regen and DM/player intents in **one** sort without an explicit **phase boundary** risks **ambiguous replay**. **`regen_apply_sequence`** is the replay-visible **phase separator**.

[Source: Helios command ordering example](https://helios.garagecraft.games/docs/core-concepts/command-system/) — *D-027 analogy:* staged command pipelines.

### Illustrative toy tick (non-cryptographic placeholders)

```json
{
  "tick_epoch": 42,
  "regen_apply_sequence": [
    {
      "regen_request_id": "0xaaa…",
      "regen_gate_version_id": "regen-gate-v0",
      "outcome": "applied",
      "outcome_fingerprint": "placeholder_hash_A"
    },
    {
      "regen_request_id": "0xbbb…",
      "regen_gate_version_id": "regen-gate-v0",
      "outcome": "applied",
      "outcome_fingerprint": "placeholder_hash_B"
    }
  ],
  "regen_apply_sequence_digest": "placeholder_merkle_or_concat_digest",
  "post_regen_intents_ordered": [
    "dm_override_stable_key_1",
    "player_intent_stable_key_2"
  ],
  "committed_sim_observable_hash": "placeholder_tick_commit_hash"
}
```

Ordering of the two regen rows follows **Option A** (lexicographic `regen_request_id` after fixed `tick_epoch` and lane sequence) **or** **Option B** would allow only one `applied` entry — adjust the example accordingly when the product picks.

## 4. Preimage field map (`TickCommitRecord_v0` — illustrative v0)

Field names below are **research placeholders** until frozen with [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]; tag **`#illustrative-v0`** applies.

| Digest or artifact | Typical residence in tick record / tail | Notes |
|--------------------|-------------------------------------------|--------|
| `regen_apply_sequence` (full or hashed) | `tick_record.regen_apply_sequence_digest` or equivalent | Must appear **before** intent-merge preimage if commit hash closes over both phases. |
| Post-regen merged intent stream | `tick_record.mutation_apply_digest` or ledger tail ref | Feeds mutation ledger → observables. |
| Per-request `regen_subgraph_outcome_row` | Embedded in sequence elements **or** `replay_log` side table keyed by `(tick_epoch, regen_request_id)` | Use **Decision rule** in §1 to choose. |
| Barrier / manifest tail (2.x) | `manifest_or_ledger_tail_ref` (per 3.2.1 wording family) | If preimage bytes live **only** in tail, **do not** claim they are inside the main record without a pointer row. |

**Post-regen `StableMergeKey` merge:** After regen, **world slices** used for intent resolution may change. **`StableMergeKey_v0`** components must be computed from **post-regen** canonical state (or envelopes that commit to that view). Pre-regen paths in key material → **silent replay fork** risk even when regen rows match.

## 5. Durability, crash, and replay edges

- **Durable regen ledger vs tick commit:** Regen **apply** rows may become durable **before** `TickCommitRecord_v0` is finalized. Re-drive after crash must use the same **`regen_request_id` + `regen_gate_version_id`** so a re-presented command yields **`ledger-hit`** and does **not** double-mutate manifest preimage.
- **Truncated-tail replay:** If the replay log ends mid-tick, behavior is **#open-question** for the operator (reject vs partial spec) — but **within** a committed tick, **`ledger-hit`** must reproduce the same **observable** outcome as live.
- **Partial failure between regen apply and tick commit:** If apply succeeded in the regen ledger but **tick commit** never closed, retry must be **idempotent** on regen lane (same keys → hit) and must **not** emit a second manifest fragment. Exact failure taxonomy → registry with **3.1.1** desync codes when adopted.

## 6. Event sourcing / command log patterns (D-027 illustrative)

**Analogy only — no mandated framework.**

- **Command log:** Each `RegenRequest_v0` is a **command**; outcomes are **events** in a tick-scoped stream. Replay **replays commands**, not hidden imperative steps.
- **Single writer / total order:** The **tick** is a **serialization boundary**; cross-tick ordering uses `tick_epoch` from 3.1.1.
- **Versioned handlers:** Algorithm changes → bump **`regen_gate_version_id`** (projection-version pattern).

[Source: Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) — mental model for **log-derived state**.

## Raw sources (vault)

- [[regenrequest-v0-gated-subgraph-determinism-research-2026-03-22]]
- [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]
- [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]
- [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]

## Sources

- [Gaffer on Games — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [Daydreamsoft — Deterministic simulation for lockstep multiplayer](https://www.daydreamsoft.com/blog/deterministic-simulation-for-lockstep-multiplayer-engines)
- [Helios — Command system](https://helios.garagecraft.games/docs/core-concepts/command-system/)
- [EventSourcingDB — Building event handlers](https://docs.eventsourcingdb.io/best-practices/building-event-handlers/)
- [Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)

> [!info] Further reading (non-normative)
> General CQRS/idempotency discussion (not contract authority): [Stack Overflow — duplicate commands in CQRS](https://stackoverflow.com/questions/66094642/handling-effectively-duplicate-commands-in-cqrs), [Medium — idempotency in CQRS/ES projections](https://medium.com/@arsalan.valoojerdi/idempotency-in-cqrs-es-projections-strategies-and-implementation-techniques-e21a7cd06575).
