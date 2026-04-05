---
title: Phase 2.7.3 - Shadow-to-live parity, admission ticket redemption, and first committed tick trace
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.7.3"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 52
handoff_readiness: 84
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]"
  - "[[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]]"
  - "[[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]]"
  - "[[decisions-log]]"
---

## Phase 2.7.3 - Shadow-to-live parity, admission ticket redemption, and first committed tick trace

This tertiary **closes the handoff from [[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]]** into **observable first committed tick**: it defines **admission ticket redemption** (binding a winning `admission_ticket_id` from **2.7.2** to a **FirstCommittedTickTrace**), **shadow-to-live parity** (every `shadow_hook_id` from the dry-run matrix must either map 1:1 to an observable tick-1 hook id or be explicitly recorded as **shadow-only no-op** with reason), and **operator acknowledgement** when `first_tick_dry_run_mode: mandatory` transitions to live observation. `GMM-2.4.5-*` remain **reference-only**.

## Scope

**In scope:**

- **Admission ticket redemption** — deterministic record that consumes **2.7.2** `admission_ticket_id` + `SimulationEntryBootstrap` identity and emits a **FirstCommittedTickTrace** header: `bootstrap_fingerprint`, `shadow_run_id` (nullable when `off`), `live_run_id`, `redeemed_at_sequence` (monotonic NL ordinal).
- **Shadow-to-live parity matrix** — extends **2.7.2** hook matrix with columns: `shadow_hook_id`, `live_hook_id | shadow_only_noop`, `parity_class` ∈ { `exact`, `semantic_equivalent`, `deferred_execution` }, and `deny_commit_inherited` (bool) flowing from **2.7.1**/**2.4** semantics.
- **First committed tick trace** — ordered list of observable hook emissions after redemption; must respect **2.7.1** total order across lanes; **no** silent reorder relative to shadow unless `parity_class: deferred_execution` is documented with rollback obligation.
- **Operator bootstrap preview handoff** — preview surfaces from **2.7.2** are **invalidated** on redemption if bootstrap fingerprint drifts; re-preview is read-only and does not substitute redemption.

**Out of scope:**

- Wall-clock latency SLOs, GPU fences, or network tick scheduling (execution-deferred).
- Compare-table / registry / CI closure (`GMM-2.4.5-*`).

## Behavior (natural language)

1. **Redeem:** Runtime (conceptual) **redeems** a valid `admission_ticket_id` only when **2.7.1** admission gates pass and **2.7.2** multi-op tie-break is resolved; failed redemption leaves simulation **unstarted** with a named failure class (inherits **2.4** deny/defer vocabulary).
2. **Parity:** For each shadow row, either a matching live hook fires in order or a **shadow_only_noop** row explains why observable tick-1 omits it (e.g. `deny_commit` frozen world_apply).
3. **Trace:** The **FirstCommittedTickTrace** is append-only for tick 1; later ticks are out of scope for this slice.

## Interfaces

Upstream:

- **2.7.2** dry-run + matrix + preview + multi-op: [[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]].
- **2.7.1** hook order + bootstrap: [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]].

Downstream:

- Phase 2 **primary** rollup / **advance-phase** to Phase 3 when Phase 2 NL checklist and gates agree — **2.7** tertiary chain **2.7.1–2.7.3** structurally complete at conceptual depth.

Outward guarantees:

- Redemption + trace are **replay-stable** with **2.6.3** replay anchor + seed lineage.
- No **live** hook runs without redemption when `first_tick_dry_run_mode: mandatory` — shadow completion remains a prerequisite in NL.

## Acceptance criteria

- Given a redeemed ticket, **FirstCommittedTickTrace** lists every observable hook id in **2.7.1** order or documents **shadow_only_noop** with cause.
- Given two conflicting sessions, only one **admission_ticket_id** redeems per **simulation_entry_id** per **2.7.2** tie-break rules.
- Given bootstrap drift between preview and redemption, preview shows **stale** and **admit** requires fresh resolution — no silent live start.

## Edge cases

- **Redeem after defer:** If **2.4** defer is active at redemption boundary, trace may be empty with **defer_hold** state — no fake “committed” hooks.
- **Mandatory shadow + operator abort:** Operator may abort before live; trace is **not** emitted; shadow ids remain audit-only.

## Open questions

- Whether **FirstCommittedTickTrace** should embed full **2.5.2** timeline head hashes or only correlation keys (execution binding deferred).

## Pseudo-code readiness

Depth 3 — redemption + parity + trace are NL tables and invariants; engine APIs deferred.

## Parent

- Secondary: [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.7.2**, **2.7.1**, and secondary **2.7**.
