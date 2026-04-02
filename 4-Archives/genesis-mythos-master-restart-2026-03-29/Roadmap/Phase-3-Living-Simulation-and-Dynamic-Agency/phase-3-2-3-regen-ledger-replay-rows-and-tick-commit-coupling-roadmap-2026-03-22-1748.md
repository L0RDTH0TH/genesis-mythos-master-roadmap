---
title: Phase 3.2.3 — Regen ledger replay rows and TickCommitRecord coupling
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, regeneration, replay, tick-commit, determinism]
para-type: Project
subphase-index: "3.2.3"
handoff_readiness: 92
handoff_readiness_scope: "Normative draft: regen_apply_sequence + RegenLaneTotalOrder_v0 (A/B) + TickCommitRecord_v0 coupling + optional regen_subgraph_outcome_row rule; field names frozen vs 3.1.1 + Option A/B product pick TBD"
execution_handoff_readiness: 62
handoff_gaps:
  - "Operator must pick **RegenLaneTotalOrder_v0** Option **A** (multi-regen tuple order) vs **B** (≤1 accepted regen/tick) before CI golden rows"
  - "`TickCommitRecord_v0` slice field names must be reconciled with [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] when replay_row_version next bumps"
links:
  - "[[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]"
  - "[[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]"
  - "[[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]"
---

## Phase 3.2.3 — Regen ledger replay rows and TickCommitRecord coupling

**Deliverables:** Normative **v0 sketch** for **`regen_apply_sequence`** serialization into the tick preimage story, **`RegenLaneTotalOrder_v0`** policy fork (**A** vs **B**), explicit **ledger-hit** durability edges aligned with **3.2.2**, and coupling hooks to **`TickCommitRecord_v0`** / **`replay_row_version`** on **3.1.1** — **without** collapsing regen into **`StableMergeKey_v0`** (post-regen player+DM only).

### `regen_apply_sequence` (draft row concept)

| Element | Role |
|--------|------|
| Ordered list (or Merkle-friendly digest) | One entry per **accepted** `RegenRequest_v0` in **regen lane order** (see below), **before** `StableMergeKey_v0` merge of player+DM intents. |
| Per-element payload (min) | `regen_request_id`, `regen_gate_version_id`, outcome fingerprint (`APPLY` digest or stable `reason_code` + denial payload hash). |
| Coupling | Any serialization change → bump **`regen_gate_version_id`** and co-register **`replay_row_version`** per **D-042** / **3.2.2** P5. |

### `RegenLaneTotalOrder_v0` — policy options (pick one)

- **Option A — Multi-regen per tick:** Tuple **`(tick_epoch_u64_be, regen_lane_sequence_u32_be, regen_request_id_lex)`** — big-endian integers; `regen_request_id` compared lexicographically as fixed **32** bytes. **Does not** share ordering key-space with **`StableMergeKey_v0`**.
- **Option B — ≤1 accepted regen / tick:** After one successful apply, additional requests in the same `tick_epoch` are **rejected** with a registry **`reason_code`** or the tick **aborts** — document which. Replay then has **zero or one** regen application per tick.

> [!warning]
> **BLOCKED_ON_OPERATOR:** Normative closure for **3.2.3** text requires choosing **A** or **B**; placeholders in research synthesis remain **`#illustrative-v0`** until then.

### `regen_subgraph_outcome_row` (golden rule)

- Emit a **distinct structured row** per regen request when CI must diff **subgraph outputs** without re-running heavy work.
- Otherwise fold fingerprints **inside** `regen_apply_sequence` elements only — still require **element-level** outcome hashes for drift detection.

### Algorithm sketch (tick close)

```text
function close_tick_commit_record(world, tick_epoch):
  regen_lane := sort_regen_requests(RegenLaneTotalOrder_v0, pending_regen[tick_epoch])
  sequence := []
  for r in regen_lane:
    outcome := apply_or_ledger_hit_regen(world, r)  // mirrors 3.2.2 P6
    sequence.append(outcome_fingerprint(outcome))
  regen_apply_sequence := finalize_sequence(sequence)  // list or digest per replay_row_version
  merged := sort_by_StableMergeKey_v0(concat(player_intents, dm_overrides))  // post-regen buffers only
  return TickCommitRecord_v0.tick_close(tick_epoch, regen_apply_sequence, merged, ...)
```

**Invariant:** **`StableMergeKey_v0`** is evaluated **only** on **post-regen** player+DM intents (**3.2.1**).

### Risk register v0 (3.2.3)

| Risk | Mitigation |
|------|------------|
| Accidental merge of regen into player/DM sort keys | Explicit phase boundary in tick close pseudo-code; hostile `ReplayAndVerify` on ordering |
| Silent change to sequence serialization | P5-style gate + registry row with **D-020** PR policy |
| Truncated-tail replay after partial regen failure | Align denial taxonomy with **3.2.2** P3 / `REGEN_SUBGRAPH_PARTIAL` candidate |

## Research integration

### Vault-aligned synthesis (nested Research `Task`, 2026-03-22)

- **[[Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830]]** — `regen_apply_sequence` vs **`TickCommitRecord_v0`**, **RegenLaneTotalOrder_v0** Options A/B, ledger-hit durability, optional `regen_subgraph_outcome_row` rule; **D-027** sources non-binding.
- **Prior:** [[Ingest/Agent-Research/regenrequest-v0-gated-subgraph-determinism-research-2026-03-22]] — P1–P6 + regen ledger sketch (**3.2.2**).

**Key takeaways (for implementers)**

- Regen lane uses **its own** total order; **not** **`StableMergeKey_v0`**.
- Close **`TickCommitRecord_v0`** only after **`regen_apply_sequence`** is finalized for the tick.
- Idempotency: **`apply`** vs **`ledger-hit`** must replay identically (**3.2.2** P6).

## Tasks

- [x] Draft `regen_apply_sequence` + **A/B** fork + tick-close coupling (this note)
- [ ] **Operator — RegenLaneTotalOrder_v0:** choose **Option A** (multi-regen tuple order) vs **Option B** (≤1 accepted regen/tick); record in [[decisions-log]] under **D-044** / new row when chosen (**BLOCKED_ON_OPERATOR** until then).
- [ ] **Eng — TickCommitRecord alignment:** reconcile literal field names in tick-close pseudo-code with [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] stub row; plan **`replay_row_version`** bump with **D-043** preimage freeze (**D-044**).
- [ ] **Eng — Golden row (deferred):** minimal two-regen tick (A) or single-regen + reject (B) — **explicitly deferred** until **D-032** replay header + **RegenLaneTotalOrder_v0** A/B per **D-045**; do not imply CI readiness in vault text.
