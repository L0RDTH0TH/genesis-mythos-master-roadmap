---
title: Research — Deterministic sim scheduler catch-up, multi-rate vs tick_epoch, fairness (Phase 3.1.2 prep)
research_query: "Deterministic simulation scheduler catch-up; spiral of death / max substeps; accumulator + fixed dt edge cases; multi-rate systems vs single logical tick_epoch; fairness / starvation — stack agnostic (D-027)"
linked_phase: Phase-3-1-2
research_anchor_phase: Phase-3-1-1
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, simulation, tick, determinism]
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
research_escalations_used: 0
---

# Deterministic simulation scheduler: catch-up, multi-rate, fairness

**Scope:** Extends (does not replace) [[simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21|simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]] and Phase **3.1.1** tick-epoch preimage work. **D-027:** patterns are **illustrative**; no engine adoption or API lock-in.

## 1. Catch-up, spiral of death, max substeps per frame

**Problem:** With an accumulator, real time deposits into a bucket; the sim withdraws fixed `dt` chunks. If each withdrawal costs **more** real time than `dt`, the bucket grows forever → more steps per frame → worse lag → **spiral of death** (terminology and mechanics from foundational game-loop writing).

**Mitigations (orthogonal, often combined):**

1. **Headroom:** Design so average sim cost ≪ `dt` so temporary spikes drain via extra substeps.
2. **Clamp incoming frame time** before `accumulator +=` (classic example: cap at ~250 ms) so a pause/hitch does not enqueue unbounded debt in one frame.
3. **Hard cap on substeps per outer frame** (`max_steps`): deterministic **given the same inputs and cap**, but **wall-clock time diverges** from pure fixed-`dt` replay when you truncate—document whether truncated ticks are **dropped**, **coalesced** into one heavier step (usually harms determinism vs fixed-`dt` path), or **deferred** across frames with an explicit policy.

For **replay / hash preimage** alignment with Phase 3.1.1: if live play uses `max_steps`, the **replay driver must apply the same cap and ordering** so `tick_epoch` advances the same count per input stream; otherwise golden rows drift.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

[Source: Taming Time in Game Engines](https://andreleite.com/posts/2025/game-loop/fixed-timestep-game-loop/)

## 2. Accumulator + fixed `dt` edge cases

| Edge case | Risk | Stack-agnostic guidance |
|-----------|------|-------------------------|
| **Negative / zero `frameTime`** | Clock skew, breakpoint | Guard: ignore non-positive deltas or clamp to 0. |
| **Huge first frame** | Massive accumulator | Clamp `frameTime` before add (see §1). |
| **Remainder / alpha** | Visual-only path | `alpha = accumulator / dt` for interpolation is **presentation**; keep out of `TickCommitRecord_v0` preimage (already directionally stated in 3.1.1). |
| **Floating time base** | Drift, jitter at long run | Prefer integer ticks / fixed-point or rational `dt` for **logical** time; aligns with 3.1.1 float policy for preimage. |
| **Input sampling vs multiple substeps** | Same input applied to several ticks in one frame | Acceptable for many single-player loops; for lockstep/replay, **timestamp inputs per tick** or buffer like lockstep articles describe. |

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

[Source: Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

[Source: Taming Time in Game Engines](https://andreleite.com/posts/2025/game-loop/fixed-timestep-game-loop/)

## 3. Multi-rate systems vs single logical `tick_epoch`

**Two coherent strategies:**

**A. Single authoritative `tick_epoch` (recommended for your preimage story)**  
All observable mutations that affect hashed state roll up to **one** monotonic tick counter. Faster subsystems (e.g. physics 120 Hz vs sim 60 Hz) run as **internal sub-steps** *inside* the same tick commit boundary, or run on **even subdivisions** (`dt_physics = dt_tick / k`) so the outer `tick_epoch` still indexes the only published commits. As an **illustrative analogy only** (not normative for your kernel): multi-rate co-simulation docs describe **simulator groups** where fast partners take hidden sub-steps and **outside** observers see outputs only at **major** time advances—parallel to “publish at `tick_epoch` commit,” not a prescription to adopt mosaik or any framework.

[Source: How to simulate at different time scales (mosaik)](https://mosaik.readthedocs.io/en/develop/tutorials/sametimeloops.html)

**B. Multiple logical clocks**  
Separate counters per domain; requires **explicit cross-rate handshake** in preimage (which clock advanced, join points). Easier to break replay unless carefully versioned.

**Decimation / slow consumers:** If some layers run every N ticks, define deterministic **phase** within the epoch (e.g. “slow system runs when `tick_epoch % N == 0` with stable tie-break”) so ordering does not depend on wall time.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

[Source: mosaik — same-time loops / multi-rate](https://mosaik.readthedocs.io/en/develop/tutorials/sametimeloops.html)

## 4. Fairness / starvation (scheduler *between* work units at a tick)

At a fixed tick, you often have **multiple systems / shards / intent streams**. Risks:

- **Starvation:** One queue never runs if others always consume the per-tick budget (especially with `max_steps` or CPU limits).
- **Priority inversion:** High-priority cosmetic vs low-priority physics—if “physics” is replay-critical, ordering must be **declared**, not accidental.

**Deterministic mitigations:**

- **Static round-robin** over a sorted stable id list (matches `shard_sequence` / lattice ideas from 2.1.3).
- **Token / credit** fairness: each category gets a per-tick cap; unused credits do not roll across ticks if that would change cross-machine timing—**or** roll with explicit integer rules in preimage.
- **Separate concerns:** OS thread scheduling is not your ordering key; **commit barriers** publish only after deterministic merge (Phase 2.1.3 alignment).

Illustrative pattern name: fixed-order **game loop** phases (input → sim → render) as in general loop literature—adapt to your kernel, not a specific engine.

[Source: Game Loop pattern](https://gameprogrammingpatterns.com/game-loop.html)

## 5. Integration hooks for Phase 3.1.2 (tertiary draft targets)

- Specify **max substeps**, **frameTime clamp**, and **truncation policy** next to `TickSchedule_v0` when you move from sketch to normative text.
- If multi-rate exists, add a **single sentence** in the contract: either “sub-steps are internal to `tick_epoch` k” or “secondary clock IDs x,y with join rule J at epoch k.”
- Fairness: add a **deterministic ordering** bullet for “within-tick work,” citing the same stable-key principle as barrier/lattice traversal (no wall-clock ordering).

## Do not duplicate

Vault synthesis **2026-03-21** already covers accumulator basics, lockstep framing, preimage include/exclude lists, and Bevy as a **label** only. This note deepens **catch-up policy**, **multi-rate contract choice**, and **within-tick fairness**.

## Sources

- [Fix Your Timestep! | Gaffer On Games](https://gafferongames.com/post/fix_your_timestep/)
- [Deterministic Lockstep | Gaffer On Games](https://gafferongames.com/post/deterministic_lockstep/)
- [Taming Time in Game Engines | André Leite](https://andreleite.com/posts/2025/game-loop/fixed-timestep-game-loop/)
- [Same-time loops / multi-rate — mosaik docs](https://mosaik.readthedocs.io/en/develop/tutorials/sametimeloops.html)
- [Game Loop — Game Programming Patterns](https://gameprogrammingpatterns.com/game-loop.html)
- Vault: [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]], [[simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]]

## Raw sources (vault)

- [[Ingest/Agent-Research/Raw/deterministic-sim-scheduler-catchup-raw-2026-03-22-2205|deterministic-sim-scheduler-catchup-raw-2026-03-22-2205]] (new fetch)
- Prior indexed: `https://gafferongames.com/post/fix_your_timestep` → existing raw bundle (vault-first; excerpt reused conceptually)
