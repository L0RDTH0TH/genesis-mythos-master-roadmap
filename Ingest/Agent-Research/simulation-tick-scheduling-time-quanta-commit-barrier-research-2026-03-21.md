---
title: Research — Simulation tick scheduling, time quanta, and commit-barrier alignment (Phase 3.1.1)
research_query: "Deterministic simulation tick scheduling vs game/replay loops; tick preimage for hashing; async commit barrier / stage ledger (Phase 2.1.3 style)"
linked_phase: Phase-3-1-1
project_id: genesis-mythos-master
created: 2026-03-21
tags: [research, agent-research]
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
research_synthesis_scope: seed
external_evidence_basis: gaffer-two-source-plus-bevy-example
validator_followup_codes: [safety_unknown_gap]
agent-generated: true
parent_context:
  queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-234
  parent_run_id: queue-eat-20260322-gmm-deepen-234
---

# Simulation tick scheduling, time quanta, and commit-barrier alignment

Synthesis for **genesis-mythos-master** / **Phase-3-1-1** (first tertiary under Phase 3.1 — simulation tick scheduler). **Evidence base:** two foundational **Gaffer On Games** articles (fixed timestep + lockstep), plus a **Bevy** documentation example that separates **fixed timestep** simulation from variable render frames—then mapped to your vault **Phase 2.1.3** / **Phase 3.1** stubs. No engine-specific API is assumed beyond these patterns.

## 1. Deterministic simulation ticks vs render / replay loops

**Separate “simulation time” from “presentation time.”** The common pattern is: advance **world state** only in **fixed** increments `dt` while **rendering** may run at arbitrary display rates. Real elapsed time accumulates in a buffer; the simulation consumes it in whole `dt` steps—this is the **accumulator pattern** (“renderer produces time; simulation consumes it in discrete dt-sized steps”).

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

**Replay alignment:** For **bit-identical** replay, the simulation path must use **the same fixed `dt` every step**, not a variable frame delta. Semi-fixed approaches (clamping variable `dt`) are often “good enough” for feel but **not** identical under floating-point rounding when remainder handling differs.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

**Lockstep / input-indexed frames:** Networking and replay tutorials stress **inputs keyed by simulation frame index**—the simulation must not advance frame `n` until the canonical input for `n` is available. Jitter from real clocks is smoothed with a **playout buffer**; the logical rule remains “one input struct per fixed tick.”

[Source: Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

**Ordering keys (conceptual):** Anything that affects outcomes at a tick should be ordered by **deterministic keys** (e.g. intent-approved ordering, stable entity ids, lattice / shard sequence)—not by thread completion time or wall clock. Phase 2.1.3 states coordinator ordering explicitly (verbatim below); apply the same idea to **simulation consumers** that merge multi-source work per tick.

> From [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000|Phase 2.1.3 roadmap]] (**Async without nondeterminism**):
>
> - **Ordering:** coordinator assigns **deterministic `shard_sequence`** from lattice traversal (e.g. `CellCoord` batches), never from scheduler timing.

## 2. Tick scheduler: fixed timestep and accumulator

Recommended mental model for Phase 3.1:

| Concern | Pattern |
|--------|---------|
| Catch-up vs spiral of death | Cap **max substeps per outer frame** or clamp accumulated real time; document slowdown vs. simulation debt. |
| Visual smoothness | **Interpolation** between previous and current **committed** simulation state using `alpha = accumulator / dt` (presentation only; **do not** feed interpolated state back into hashed / ledger inputs). |
| Determinism | Single code path integrates with **constant `dt`**; avoid mixing variable-`dt` branches in the replay-critical core. |

Modern ECS docs often document **fixed timestep** as a first-class schedule (decoupled from frame updates)—useful vocabulary even if your runtime is custom.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

[Source: Bevy — Run physics in a fixed timestep](https://bevy.org/examples/movement/physics-in-fixed-timestep/)

## 3. Time quanta boundaries for hashing “observable” state

Treat each **simulation quantum** (one fixed `dt` step after all per-tick work is **committed**) as a **hash boundary** analogous to **ManifestEmit** / barrier publish in Phase 2.1.3.

**Include in tick preimage (illustrative, engine-agnostic):**

- Logical **tick index** or **simulation time** as a rational multiple of `dt` (integer tick counter preferred over raw floats).
- **Committed** entity / component state **after** deterministic ordering passes (e.g. sorted stable keys for collections contributing to hash).
- References to **immutable** outputs already published through your **stage ledger** (e.g. manifest hash, barrier id) that this tick **reads** as inputs—not ephemeral worker buffers.
- **RNG stream state** (or stream counters) **after** the tick’s draws, if randomness is part of the sim core.

**Exclude from tick preimage (normative direction):**

- **Wall clock**, OS scheduler timestamps, thread ids, **worker_nonce**-style ephemeral ids (aligns with Phase 2.1.3: worker nonce not in hash path).
- **Partial** manifests or unconsumed scratch from async stages until the **single terminal publish** occurs.
- **Presentation-only** state (interpolation alpha, camera blend, UI-only caches).

**Failure parallel:** Just as `BARRIER_RECONCILE_DIVERGENCE` blocks publish, a **tick hash mismatch** in replay should be a **fail-closed** diagnostic: either inputs, ordering key, or preimage scope drifted.

## 4. Integration with async commit barrier / stage ledger (Phase 2.1.3 style)

Map concepts **only** at the contract level (no invented APIs):

| Phase 2.1.3 idea | Phase 3.1 simulation angle |
|------------------|----------------------------|
| **Private scratch** keyed by `barrier_id` | Async sim work (pathfinding batches, procedural sub-steps) writes to **ephemeral** stores until promoted. |
| **Single terminal publish** | A simulation tick **observes** generation outputs only after the ledger records the **terminal** emit for that barrier attempt. |
| **`shard_sequence` / stable ordering** | Per-tick **processing order** for systems, regions, or entities follows a **deterministic key** fixed for replay. |
| **`reconcile_plan_version`** | If you merge multi-shard sim contributions inside one tick, bump a **semver** when tie-break rules change—mirror harness expectations. |

**Do not duplicate:** Phase 3.1 stub already states deliverables (deterministic tick model, ordering vs ledger, quanta for hashing). This note adds external pattern names (accumulator, lockstep framing) and preimage guidance.

## 5. Pitfalls called out in sources

- **Floating-point determinism** is fragile across arch / build; checksum-based lockstep assumes **same dt, same ordering, same numeric policy**—often fixed-point or integer where feasible for hashed cores.

[Source: Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

## 6. Replay and record format (project-local sketch)

**Goal:** align **intent stream + tick counter** with **barrier visibility** so replay and live runs hash the same preimage.

- **Per fixed tick `k`**, the replay log should carry: **tick index** `k`, **canonical input bundle** (same struct as live lockstep sampling), and **references** to any **ledger-published** artifacts the tick consumed (e.g. manifest hash / barrier tail id), not raw worker scratch.
- **Cross-barrier rule:** simulation may read **generation outputs** only at **terminal publish** boundaries (mirror Phase 2.1.3 `SpawnCommit` gate language). Mid-barrier state stays **non-observable** for tick hashing.
- **Hash mismatch:** treat as **fail-closed** diagnostic (which subsystem: inputs, ordering key, preimage scope, or numeric policy)—exact taxonomy is **project-local (TBD)**.

## 7. Determinism and build policy (TBD without engine choice)

Until numeric and concurrency policies are frozen:

- **Cross-arch / SIMD / compiler flags** can break bit-identical replay even with fixed `dt`; either **document a single supported matrix** or **scope hashes to intentional subsets** (e.g. integer tick + ids only).
- **Debug vs release** float behavior is a known divergence class; harness should pin configuration for golden runs.

[Source: Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

## Sources

- [Fix Your Timestep! | Gaffer On Games](https://gafferongames.com/post/fix_your_timestep/)
- [Deterministic Lockstep | Gaffer On Games](https://gafferongames.com/post/deterministic_lockstep/)
- [Bevy — Run physics in a fixed timestep](https://bevy.org/examples/movement/physics-in-fixed-timestep/)
- Vault: [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000|Phase 2.1.3 roadmap note]], [[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346|Phase 3.1 stub]]

## Raw sources (vault)

- Prior related synthesis: [[phase-2-1-3-async-commit-barrier-research-2026-03-19-2000|phase-2-1-3-async-commit-barrier-research-2026-03-19-2000]]
