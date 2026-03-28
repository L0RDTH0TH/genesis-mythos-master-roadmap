---
title: Research — Deterministic application of agency slice outcomes to entity/world state (Phase 3.1.5)
research_query: "agency slice outcomes commit ordering idempotent replay CatchUpPolicy pause alignment"
linked_phase: "Phase-3-1-5"
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, simulation, determinism, agency-slices]
agent-generated: true
research_tools_used: [web_search]
research_escalations_used: 0
---

# Deterministic application of agency slice outcomes (Phase 3.1.5 support)

Synthesis for **genesis-mythos-master** roadmap deepen: after **3.1.4** (`AgencySliceSchedule_v0`, `tick_epoch`, stable tie-break, starvation credits, RNG-after-schedule), define how **slice-local outcomes** become **committed world/entity state** without wall-clock or thread schedule, aligned with **3.1.2** (`CatchUpPolicy_v0`, **D-031**), **3.1.3** (pause / `SimulationRunControl_v0`, **D-032**), and **D-027** (stack-agnostic contracts; engine examples below are **illustrative only**).

## Vault anchor (do not duplicate)

- **3.1.4** already fixes **total order** of slices within one `tick_epoch`: `(tick_epoch, slice_index, serialized tie_break_key)` and requires RNG consumption **after** schedule order. [Source: project phase note [[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]]]
- **3.1.2** bounds **how many** logical steps / substeps can run per outer frame and defines replay parity for `max_steps_per_frame`, clamp, and `on_budget_exceeded`. Partial execution within a tick is a first-class scenario. [Source: [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]]
- **3.1.3** forbids `tick_epoch` advance and tick commits while paused; catch-up must not smuggle logical work across pause boundaries unless explicitly documented. [Source: [[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]]]

## Recommended contract shape (normative sketch for 3.1.5)

### 1. Single commit stream per `tick_epoch`

Treat each agency slice as producing **ordered mutation intents** (not direct writes). A central **apply phase** (name TBD) merges intents into one stream sorted by:

1. `tick_epoch` (constant within the batch),
2. `slice_index` from `AgencySliceSchedule_v0.slices[]`,
3. `tie_break_key` for the slice (replay-serialized, per 3.1.4),
4. Optional **intra-slice sequence** `op_index` (monotonic per slice execution).

Any two operations that touch the same **state key** (entity id + component/channel/facet per your ECS/data model) **must** compare equal on this sort key space so replay and live agree on **last applied wins** or on **explicit merge**.

### 2. Overlapping mutations: ordering and conflicts

- **Default:** **stable sort then sequential apply** — after sorting as above, later operations overwrite earlier ones on the same scalar field (deterministic “last in schedule order”).
- **Non-commutative composites:** If two slices both read-modify-write the same aggregate, either:
  - **forbid** (static or dynamic conflict: fail CI / emit `SLICE_STATE_CONFLICT` in replay taxonomy), or
  - define **domain-specific merge** (e.g. max HP clamp) that is **pure function** of prior state + both intents, still evaluated **after** sort so order is irrelevant — document in vault.
- **Do not** use wall time, thread id, or pointer identity in ordering or conflict rules ([Source: parity with `WithinTickWorkOrder_v0` / `SUBSTEP_STARVATION` spirit in 3.1.2].

### 3. Idempotent apply and replay

Borrow **event-sourcing / CQRS** discipline: replay is **re-execution** of the same ordered mutation list. Idempotency guards matter when:

- The same logical mutation could be **re-delivered** (crash recovery, partial journal write, tooling bugs).

Patterns (stack-agnostic):

- **Mutation id:** Each intent carries `mutation_id` (hash of `(tick_epoch, slice_id, op_index, payload_redacted)` or monotonic row id from replay log). The apply phase maintains `applied_mutation_ids` per tick or global compact set; duplicates are **no-ops**.
- **Expected version / aggregate version:** For entity-scoped state, carry `base_version` or `preimage_hash`; if current version ≠ expected, **fail-closed** in replay verify (surfaces desync early). [Source: discussion of versioning and idempotency in event-sourced systems — [Stack Overflow: replay / ordering](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing)]

**Replay log:** Extend the **D-034** trajectory: persist not only `agency_slice_sequence` but **mutation batch** or **intent checksum** per slice so golden rows can assert identical apply input, not only slice order.

### 4. Coupling to `CatchUpPolicy_v0` (3.1.2)

When catch-up stops mid-tick (`budget_hit`, `input_coalesced`, etc.):

- The **set of slices that ran** in live must be reproduced in replay **exactly** (same truncation boundary). Overlap conflicts only arise between slices that **actually executed** in that substep ledger.
- If policy **drops substeps**, dropped slice intents must **not** appear in the commit stream for that outer frame; coalesced inputs must follow the same deterministic merge as documented for `on_budget_exceeded`.

### 5. Coupling to pause and time-scale (3.1.3)

If `SimulationRunControl_v0.paused` (draft): **no** slice execution, **no** apply phase, **no** `tick_epoch` increment — schedule is empty or latched per 3.1.4. Resume uses **`pause_resume_seq`** (or intent-equivalent) so replay aligns pause boundaries with input latch rules; no “hidden” catch-up through apply.

### 6. Parallel recording vs deterministic playback (ECS analogy)

Engines that defer structural changes often **record** commands in parallel but **play back** with an explicit **sort key** so order does not depend on job completion order. Same pattern applies conceptually: **record** slice intents may be produced in any implementation order, **playback** order is **only** the vault-defined total order. [Source: Unity ECS ECB playback ordering with sort keys — [Entity command buffer playback](https://docs.killliu.com/en/docs/unity/entities/systems-entity-command-buffer-playback/)]

### 7. Fixed timestep / multiple passes (illustrative)

When multiple fixed steps run in one display frame, **interleave** systems per step (ABAB…) rather than batching all A then all B, or determinism can depend on accumulator — aligns with “fixed step group” discipline. [Source: [Gaffer on Games — Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/) — **illustrative per D-027**]

## Desync codes (candidates for 3.1.5 taxonomy)

| Code | Detect |
|------|--------|
| `SLICE_APPLY_ORDER_DIVERGENCE` | same intents, different post-state |
| `MUTATION_REPLAY_DUPLICATE` | duplicate `mutation_id` handled differently |
| `CATCHUP_TRUNCATION_MISMATCH` | replay ran extra slice after budget_hit |
| `PAUSE_APPLY_LEAK` | commits while paused |

## Sources

- [Stack Overflow — deterministic replay in CQRS / event-sourcing](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing)
- [Entity command buffer playback (sort keys)](https://docs.killliu.com/en/docs/unity/entities/systems-entity-command-buffer-playback/)
- [Gaffer on Games — Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/) *(illustrative only; D-027)*
- [Flecs commands / defer-merge (conceptual)](https://www.flecs.dev/flecs/group__commands.html) *(illustrative only)*

## Raw sources (vault)

- None for this run (web snippets only; no Raw bundle written).
