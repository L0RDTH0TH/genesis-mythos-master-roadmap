---
title: Phase 2.7.2 - First-tick dry-run shadow, hook matrix, and operator bootstrap preview
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.7.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 48
handoff_readiness: 82
created: 2026-04-01
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]"
  - "[[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]]"
  - "[[Phase-2-6-2-Operator-Session-Escalation-Surfaces-and-Forge-Continuity-Roadmap-2026-03-30-1200]]"
  - "[[decisions-log]]"
---

## Phase 2.7.2 - First-tick dry-run shadow, hook matrix, and operator bootstrap preview

This tertiary **refines** [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]]: it names a **first-tick dry-run shadow** pass (optional vs mandatory policy), a **hook matrix** that labels sub-stages within the three top-level hooks (input / world / observation), and **operator-visible bootstrap preview** surfaces that stay read-only until admission. It also specifies **minimum multi-operator admission fields** when forge sessions race on the same `simulation_entry_id`. `GMM-2.4.5-*` remain **reference-only**.

## Scope

**In scope:**

- **Dry-run shadow** — a deterministic **pre-observable** rehearsal of the **2.7.1** hook order that emits **shadow hook ids** and **no world commits**; policy flag: `first_tick_dry_run_mode` ∈ { `mandatory`, `optional_operator`, `off` } with default **`optional_operator`** so tooling can force **`mandatory`** without changing **2.7.1** admission rules.
- **Hook matrix** — rows: `hook_lane` (input | world_apply | observation), `sub_hook_id`, `depends_on`, `replay_stable` (bool), `forbidden_when_deny_commit` (bool); matrix must be a **refinement** of **2.7.1** total order (no reordering of the three lanes).
- **Operator bootstrap preview** — read-only projection of **SimulationEntryBootstrap** fields + resolved refs (**2.6.3**, **2.5.2**, **2.4.5**) suitable for forge dialogue citation per **2.6.1**; **no** mutation path from preview to runtime admit.
- **Multi-operator minimum** — when multiple forge sessions target admission: `admission_ticket_id`, `session_actor_id`, `tie_break_order` (deterministic compare on opaque ids), and `conflict_outcome` ∈ { `first_wins`, `defer_all`, `operator_pick` } (execution binding deferred; NL contract only).

**Out of scope:**

- Shadow pass performance budgets, GPU sync, or parallel shadow lanes (execution-deferred).
- Compare-table / registry / CI closure (`GMM-2.4.5-*`).

## Behavior (natural language)

1. **Shadow:** Before tick `1` observable hooks, runtime may run **shadow** sub-hooks in matrix order; **deny_commit** still forces **world_apply** sub-hooks to **no-op** with logged reason (inherits **2.7.1**).
2. **Preview:** Operators see **bootstrap preview** only after commit-valid path; preview never substitutes **admit** authority.
3. **Multi-op race:** Two sessions with same bootstrap identity → **tie_break_order** selects deterministic winner for **admission_ticket_id** issuance; **`operator_pick`** surfaces as forge escalation per **2.6.2** lanes.

## Interfaces

Upstream:

- **2.7.1** hook order + bootstrap fields: [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]].
- Operator / forge lanes: [[Phase-2-6-2-Operator-Session-Escalation-Surfaces-and-Forge-Continuity-Roadmap-2026-03-30-1200]].

Downstream:

- Tertiary **2.7.3+** may close secondary **2.7** rollup or open **2.8**-class topics (sim loop continuation) per Phase 2 MOC.

Outward guarantees:

- Shadow ids are **replay-stable** when bootstrap + seed lineage match (**2.7.1** determinism contract).
- Preview surfaces are **strictly read-only** relative to admit.

## Acceptance criteria

- Given **2.7.1** hook order, the matrix lists every **sub_hook_id** with a unique total order within each lane compatible with **2.7.1**.
- Given `first_tick_dry_run_mode: mandatory`, shadow completes before any observable tick-1 hook; given `off`, no shadow row is required in trace.
- Given two sessions with colliding `simulation_entry_id`, `tie_break_order` yields a single **admission_ticket_id** winner or a named **defer_all** / **operator_pick** outcome in NL.

## Edge cases

- **Shadow + defer:** If **2.4** defer is active, shadow may run but **observation** lane must not assert committed world (NL **no-op** semantics).
- **Preview stale ref:** If replay anchor rotates after preview, **admit** must re-resolve refs — preview shows **stale** marker (inherits **2.7** stale-bootstrap edge case).

## Open questions

- Whether **mandatory** dry-run should be the default for **multi-operator** sessions only (execution policy).
- Whether **hook matrix** should version with `HookSchemaCatalog` revision (**2.2.x**) — cross-link deferred.

## Pseudo-code readiness

Depth 3 — matrix + policy flags are NL-explicit; engine binding deferred.

## Parent

- Secondary: [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.7.1**, **2.6.2**, and secondary **2.7** open questions.
