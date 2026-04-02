---
title: Phase 3.1.3 — Deterministic pause, time-scale, and simulation–wall clock coupling
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, simulation, tick, determinism, pause, replay]
para-type: Project
subphase-index: "3.1.3"
handoff_readiness: 91
handoff_readiness_scope: "pause_semantics + time_scale_serialization + replay_header coupling (normative draft); HR 91 = contract text + taxonomy — not execution green until Tasks + A/B freeze; golden row fields TBD"
handoff_gaps:
  - "`sim_speed` / `pause_resume_generation` encoding in replay header vs intent-only stream unresolved until operator selects schema (**BLOCKED_ON_OPERATOR** — see **D-032**)"
  - "Tertiary **Tasks** checklist remains open until encoding freeze + worked example land — do not treat prior HR headline as rollup-complete"
execution_handoff_readiness: 72
links:
  - "[[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
  - "[[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935]]"
---

## Phase 3.1.3 — Deterministic pause, time-scale, and simulation–wall clock coupling

**Deliverables:** Vault-normative **pause** semantics (zero logical `tick_epoch` advance while paused), **time-scale / dilation** policy that is **replay-serialized or session-fixed**, and explicit **coupling rules** between wall-driven frames, `CatchUpPolicy_v0` (**D-031**), and `TickCommitRecord_v0` (**3.1.1**).

> [!warning] Authoritative handoff rule
> **Do not** treat frontmatter **`handoff_readiness`** as execution green for implementers. Use **`execution_handoff_readiness`** and the **Tasks** checklist until `SimulationRunControl_v0` encoding is frozen in replay artifacts per **D-032** / operator **A/B** choice.

**Interfaces**

- `SimulationRunControl_v0` (draft): `{ paused: bool, time_scale_q16: uint16 /* rational fixed-point 1.0 = 65536 or TBD */, pause_resume_seq: uint64 }` — **vault placeholder** until operator pins **A/B** (dedicated replay header vs intent-stream commands) per **D-032**; must not be silently omitted from replay driver when it affects tick count.
- **Pause invariant:** While `paused == true`, **no** fixed-`dt` logical step executes; **no** `tick_epoch` increment; **no** `TickCommitRecord_v0` for “skipped” wall time.
- **Dilation invariant:** If time-scale changes mid-session, either (a) **record** each change in replay header / ledger with monotonic `pause_resume_seq`, or (b) **forbid** mid-session changes (operator policy). Live and replay **must** apply the **same** mapping from control state + intents → tick sequence.
- **`CatchUpPolicy_v0` interaction:** While paused, **do not** drain wall-time backlog into extra logical ticks unless explicitly documented as a **non-pause** mode (e.g. “headless catch-up”); coalescing across pause boundaries must match **3.1.2** `on_budget_exceeded` semantics.

### Algorithm sketch (mid-technical)

> [!note] Illustration only (integer-friendly)
> This sketch is **non-normative** for preimage bytes. Any `time_scale` application must stay consistent with **3.1.1** float-free preimage policy for committed records — use **fixed-point integer math** (e.g. `effective_wall_q16 = mul_q16(wall_dt_ms, control.time_scale_q16)`) in real specs; do not introduce silent `float` in replay-critical paths.

```text
function outer_frame(world, wall_dt_ms, control: SimulationRunControl_v0, policy: CatchUpPolicy_v0):
  if control.paused:
    latch_inputs_for_pause_boundary(world, control.pause_resume_seq)
    return world  // no accumulator drain, no tick_epoch advance
  effective_wall_ms = mul_q16(wall_dt_ms, control.time_scale_q16)  // integer fixed-point; must match replay driver table
  return simulate_frame(world, effective_wall_ms, policy)  // delegates to 3.1.2 sketch
```

### Desync taxonomy (v0) — extensions

| Code | Detect | Surface | Replay outcome |
|------|--------|---------|----------------|
| `PAUSE_STATE_DIVERGENCE` | live paused / replay unpaused at same `pause_resume_seq` | CI golden | Fail-closed |
| `TIME_SCALE_NOT_SERIALIZED` | mutable global speed absent from replay header | Audit | Fail-closed; add header field or ban mutation |
| `INPUT_LATCH_FRAME_MISMATCH` | per-frame vs per-tick input fan-out differs live vs replay | Harness | Fail-closed; document latch rule |

**Acceptance criteria**

- Pause + dilation behavior is **fully specified** in prose + types even when numeric `time_scale` encoding is TBD — **no** hidden globals.
- Cross-links to **3.1.1** (preimage excludes presentation/wall) and **3.1.2** (catch-up parity) are explicit.
- `handoff_readiness` **91** = normative draft + taxonomy + interface sketch (open Tasks + **BLOCKED_ON_OPERATOR** for A/B); **`execution_handoff_readiness` 72** until replay header / golden row encodes control state.

## Research integration

### Key takeaways

- Treat **wall clock**, **presentation**, and **logical sim time** separately: only logical fixed-`dt` steps advance `tick_epoch` and belong in `TickCommitRecord_v0` preimage direction (wall stays out, per 3.1.1).
- **Pause** = **zero** logical fixed steps (no `tick_epoch` advance, no commit records for “skipped” time); pair with **replay-stable input latching** when multiple ticks run in one display frame (per-tick vs per-frame input is a common desync source).
- **Time scale / dilation** must be **serialized or fixed** per session so live and replay apply the **same** mapping from intents + policy → tick sequence; do not rely on a mutable global speed that is absent from the replay header.
- **`CatchUpPolicy_v0` (D-031):** While paused, catch-up must **not** drain backlog into extra `tick_epoch` advances unless that is an explicit, logged policy; dilation implemented via extra substeps must still respect the **same** `max_steps_per_frame`, clamp, and coalescing semantics as recorded.
- **Optional contract hooks (vault-TBD):** explicit `sim_run_state` / `time_scale` in policy or commit metadata vs deriving pause/scale only from intents — operator choice; either way live/replay drivers must match.

### Decisions / constraints

- **D-027:** External articles (Fix Your Timestep, lockstep, QEMU replay, oboe loops, etc.) are **illustrative** only.
- Align pause/dilation semantics with **3.1.1** preimage exclusions and **3.1.2** replay parity obligations; bump **`replay_row_version`** when pause/scale serialization changes.

### Links

- [[Ingest/Agent-Research/deterministic-pause-sim-clock-time-dilation-replay-research-2026-03-21|deterministic-pause-sim-clock-time-dilation-replay-research-2026-03-21]]
- Prior: [[Ingest/Agent-Research/simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21|simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21]], [[Ingest/Agent-Research/deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205|deterministic-sim-scheduler-catchup-multirate-fairness-research-2026-03-22-2205]]

## Tasks

- [ ] Choose **A/B** encoding for `SimulationRunControl_v0`: dedicated replay header block vs intent-stream commands; document in **decisions-log** as **D-032** adoption row when frozen.
- [ ] Cross-walk **input latch** rules with Phase **2.1.2** intent/RNG namespaces — extend desync table if tick-scoped draws need new namespace slots.
- [ ] Add worked example: pause during hitch + resume with **identical** `tick_epoch` sequence in live vs replay stub (pairs with 3.1.2 worked example).
