---
title: Research — Deterministic pause, sim vs wall clock, time dilation, replay coupling (Phase 3.1.3)
research_query: "Deterministic pause; simulation logical time vs external wall clock; time-scale/time dilation; replay obligations with TickCommitRecord_v0 and CatchUpPolicy_v0 — stack agnostic (D-027)"
linked_phase: Phase-3-1-3
project_id: genesis-mythos-master
created: 2026-03-21
tags: [research, agent-research]
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
agent-generated: true
parent_context:
  queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-236
  parent_run_id: queue-eat-20260321-236
---

# Deterministic pause, sim clock coupling, time dilation, and replay

Synthesis for **genesis-mythos-master** targeting the **next tertiary after 3.1.2** (hand-off label **Phase-3-1-3**): deterministic **pause**, **time-scale / time-dilation**, **external vs simulation clock** coupling, and **replay obligations** alongside vault contracts **`TickCommitRecord_v0`** ([[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]) and **`CatchUpPolicy_v0`** ([[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]). **D-027:** All engine/framework names and articles below are **illustrative prior art**; the product stack remains TBD.

**Do not duplicate:** Fixed-`dt` accumulator, lockstep framing, `TickCommitRecord_v0` field sketch, float-free preimage stance, and `CatchUpPolicy_v0` enums are already normative or drafted in **3.1.1 / 3.1.2** and in [[simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21|simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]] / [[deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205|deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205]]. This note adds **pause / dilation / clock coupling** and **what must match between live and replay drivers**.

## 1. Three time bases (vocabulary)

| Base | Role | In preimage? |
|------|------|----------------|
| **Wall / host clock** | OS or display-frame timing; drives how often the outer loop runs | **No** (already excluded for tick hash in 3.1.1 direction) |
| **Real-time accumulator** | Buffers elapsed wall time between frames; feeds “how many fixed steps this frame” before caps | **No** — but **policy** that turns accumulator into tick count **must** be identical live vs replay (see **D-031** / `CatchUpPolicy_v0`) |
| **Logical simulation time** | Advances in multiples of fixed `dt` (or rational tick index); **`tick_epoch`** lives here | **Yes** — committed state + `tick_epoch` / ledger refs per `TickCommitRecord_v0` |

Decoupling render from sim is the standard “simulation consumes time in discrete `dt` steps” pattern.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

[Source: Deterministic game loops overview (O’Reilly / oboe.com)](https://oboe.com/learn/architecting-high-performance-game-simulations-zvgbii/deterministic-game-loops-2)

## 2. Deterministic pause

**Definition (contract-level):** While **paused**, the kernel performs **zero** logical fixed-timestep advances: **`tick_epoch` does not increment**, and no `TickCommitRecord_v0` is emitted for “skipped” time.

**Accumulator behavior:** If pause is implemented only by “not draining” the wall-time accumulator, ensure the implementation does not **silently coalesce** or **drop** queued inputs across the pause boundary in a way that differs between live and replay. Per-tick input sampling must be replay-stable (multiple sim ticks in one display frame require careful input fan-out).

[Source: Reliable fixed timestep & inputs](https://jakubtomsu.github.io/posts/input_in_fixed_timestep/)

**Explicit vs implicit pause:** Either (a) **implicit** — absence of advancing ticks while menu open — or (b) **explicit control** — a deterministic “pause level” or “sim run state” in the intent stream. For replay, (b) is easier to audit: the log shows *why* no ticks ran. If (a), replay must apply the **same** “no step” decisions from recorded intents only, never from wall clock.

**Networking analogy:** Lockstep tutorials treat “wait for input before advancing frame *n*” as the core rule; pause is structurally similar to “stall logical time until a condition is met,” but the condition must be **logged or derivable from logged intents**.

[Source: Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

## 3. Time scale / time dilation

**Meaning:** A scalar (or rational) **`time_scale`** maps **requested** logical progress to **actual** fixed steps per unit of *something*. Common patterns:

- **Scale outer accumulation:** Multiply effective `frame_duration` before dividing by `dt` (speed up / slow down sim relative to wall clock).
- **Scale logical `dt`:** Keep tick count per wall second but change effective `dt` (harder for golden stability unless `dt` is a rational parameter in the log).
- **Sub-step budget only:** Leave `dt` fixed but change `max_steps_per_frame` / clamp — this overlaps **`CatchUpPolicy_v0`** (already in 3.1.2).

**Replay rule:** Whatever combination you choose, **live and replay must apply the same mapping** from (recorded intents + recorded policy snapshot) → sequence of tick advances. A **`time_scale`** that exists only as a mutable global in the live build and is **not** in the replay header is a common desync source.

**Illustrative systems design:** Record/replay in virtual machines decouples **virtual time** from **host wall clock** and drives injections by a deterministic counter, not real time — same *idea* as “don’t tie replay to wall clock.”

[Source: QEMU — Execution Record/Replay (icount / virtual clock)](https://www.qemu.org/docs/master/devel/replay.html)

## 4. Coupling `TickCommitRecord_v0` (3.1.1)

Keep **wall clock** and **presentation** out of the preimage; consider **optional explicit fields** (vault-TBD, not prescriptive):

- **`sim_run_state`** or bitmask: `running | paused` at tick boundary (if pause is explicit).
- **`time_scale_q`** (rational) or versioned enum when scale changes are rare and must be hashed.
- Any change to **which inputs gate tick advancement** should be reflected in what feeds **`committed_sim_observable_hash`**, or documented as **outside** preimage with a **policy version** bump.

Align with **2.1.3**: ordering inside a tick still uses deterministic keys (e.g. `shard_sequence`), not “when the thread finished.”

## 5. Coupling `CatchUpPolicy_v0` (3.1.2 / D-031)

- **While paused:** Catch-up loops should **not** consume backlog to advance `tick_epoch` unless that behavior is **intentional** (usually false for “menu pause”). Treat pause as **`max_steps_per_frame = 0`** or a separate gate that **short-circuits** the catch-up scheduler.
- **While time-dilated:** If dilation is implemented via **more substeps per outer frame**, that must stay inside the **same** `max_steps_per_frame`, `frame_dt_clamp_max_ms`, and coalescing rules recorded for the session; otherwise replay diverges from live under load.
- **D-031 reminder:** Live and replay must implement **identical** policy semantics before execution closure; this extends naturally to **pause + scale**.

## 6. Replay obligations checklist (handoff-oriented)

1. **Fixed `dt` (or rational tick index)** identical live/replay for all committed ticks.
2. **No wall clock** in tick preimage; accumulator **policy** identical (caps, clamp, coalesce).
3. **Pause:** either explicit in intent/log or provably equivalent implicit behavior; **zero** `tick_epoch` advance while paused.
4. **`time_scale` / dilation:** serialized or fixed per session; changes versioned (`replay_row_version` alignment per 3.1.1 tasks).
5. **Per-tick inputs:** sampled/latched in a replay-stable way when multiple ticks run per display frame.

[Source: Instant replay — reproducible behavior (gamedeveloper.com)](https://www.gamedeveloper.com/design/instant-replay-building-a-game-engine-with-reproducible-behavior)

## 7. Pending vault decisions (operator)

- Is **pause** explicit in the intent stream or a derived UI flag?
- Is **time_scale** a first-class serialized parameter or a fixed compile-time constant until D-027 resolution?
- Does **`TickCommitRecord_v0`** need a visible **pause/scale** field, or is **policy + intents** enough?

## Raw sources (vault)

- [[simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]]
- [[deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205]]
- [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]
- [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]

## Sources

- https://gafferongames.com/post/fix_your_timestep/
- https://gafferongames.com/post/deterministic_lockstep/
- https://jakubtomsu.github.io/posts/input_in_fixed_timestep/
- https://www.qemu.org/docs/master/devel/replay.html
- https://oboe.com/learn/architecting-high-performance-game-simulations-zvgbii/deterministic-game-loops-2
- https://www.gamedeveloper.com/design/instant-replay-building-a-game-engine-with-reproducible-behavior
