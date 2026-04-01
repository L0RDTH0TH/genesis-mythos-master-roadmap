---
title: Phase 2.7.1 - Simulation-entry bootstrap and deterministic first-tick contract
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.7.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 80
created: 2026-04-01
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]"
  - "[[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]]"
  - "[[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]"
  - "[[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]"
  - "[[decisions-log]]"
---

## Phase 2.7.1 - Simulation-entry bootstrap and deterministic first-tick contract

This tertiary is the **first decomposition** under secondary **2.7**: it names the **SimulationEntryBootstrap** record shape (NL), how it **binds** to **2.6.3** replay anchor + cold-start minimum, to **2.5.2** timeline head for correlation, and to **2.4.5** finalization identity — and it fixes a **deterministic first-tick hook order** (input → staged world application → observation emission) for tick boundary `0 → 1` without engine APIs. Deferment anchors `GMM-2.4.5-*` remain **reference-only**.

## Scope

**In scope:**

- **Bootstrap record fields (NL)** — minimum named segments: `commit_envelope_ref` (stable id tying to **2.4.5** closure), `telemetry_timeline_head_ref` (**2.5.2** ordering), `replay_anchor_ref` + `cold_start_minimum_satisfied` boolean (**2.6.3**), `simulation_entry_id` (opaque logical id for this admission).
- **Admission gate** — rules for **block vs admit**: cold-start not satisfied → **blocked** with deterministic non-ready marker; commit invalid per **2.4** → no bootstrap (inherits deny/defer semantics).
- **First-tick ordering** — single total order of **conceptual hooks** for tick `1` (first observable sim frame after bootstrap): (1) apply validated intents / scheduler input slice, (2) apply world mutation stage outputs that are legal post-commit, (3) emit observations / telemetry segments per **2.5.1** sink binding — no reordering across equivalent replays.

**Out of scope:**

- Frame time budgets, thread pools, or GPU sync (execution-deferred).
- Compare-table / registry / CI closure (`GMM-2.4.5-*`).

## Behavior (natural language)

1. **Construct bootstrap:** After successful commit path, assembly fills `SimulationEntryBootstrap` from upstream refs; forge dialogue may **cite** bootstrap read-only per **2.6** consumer contract.
2. **Admit:** When all mandatory refs resolve and **2.6.3** cold-start predicate holds, runtime marks **admitted** and schedules **first tick** with frozen hook order below.
3. **First tick:** Hooks run in fixed order; **defer** from **2.4** still blocks observable mutation until lifted; **deny_commit** lineage prevents world application hook from asserting commit.
4. **Determinism:** Same bootstrap record + same seed lineage ⇒ same hook invocation order and same first-tick observable class (proof deferred).

## Interfaces

Upstream:

- Secondary **2.7** scope: [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]].
- Replay + cold-start: [[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]].
- Finalization floor: [[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]].
- Timeline head: [[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]].

Downstream:

- Tertiary **2.7.2** (minted): [[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]] — dry-run shadow policy, hook matrix, operator preview, multi-operator admission fields.
- Tertiary **2.7.3+** may close secondary **2.7** rollup or extend sim-loop continuation.

Outward guarantees:

- No bootstrap row implies execution completion of `GMM-2.4.5-*` artifacts.
- First-tick order is stable across replay of the same bootstrap record.

## Acceptance criteria

- Given a valid post-commit world, the bootstrap record lists all mandatory refs and evaluates **cold_start_minimum_satisfied** deterministically from **2.6.3** fields.
- Given **deny_commit** authority on the latest commit envelope, first-tick world application hook is a **no-op** with explicit logged reason (NL contract).
- Given two replays with identical bootstrap + seed lineage, first-tick hook sequence ids match.

## Edge cases

- **Rotated replay anchor:** Bootstrap must carry explicit **lineage pointer** if **2.6.3** anchor changes between commit and admission (no implicit latest).
- **Partial telemetry:** If **2.5.2** head missing but commit valid — **defer** path per **2.4**; bootstrap construction **blocked** until timeline head resolvable or defer lifted.

## Open questions

- Whether **dry-run shadow ordering** for first tick should be mandatory vs optional (may land in **2.7.2**).
- Minimum bootstrap fields when **multi-operator** forge sessions race on admission (execution binding deferred).

## Pseudo-code readiness

Depth 3 — interfaces and ordering are explicit in NL; implementation can derive checklist rows without redefining **2.4** branch vocabulary.

## Parent

- Secondary: [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from secondary **2.7** + **2.6.3** + **2.4.5** + **2.5.2** NL contracts.
