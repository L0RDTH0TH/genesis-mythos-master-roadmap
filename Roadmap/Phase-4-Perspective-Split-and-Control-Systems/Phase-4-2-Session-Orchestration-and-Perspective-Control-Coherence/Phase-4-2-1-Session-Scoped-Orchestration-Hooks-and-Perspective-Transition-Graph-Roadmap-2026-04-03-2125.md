---
title: Phase 4.2.1 — Session-scoped orchestration hooks and perspective transition graph
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.1"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 50
handoff_readiness: 85
created: 2026-04-03
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **4.2.1** — **session-scoped orchestration hooks** bind **perspective transition requests** to a single **SessionOrchestration** path (no direct control mutation); **perspective transition graph** instantiates Phase **4 primary** mode graph as **legal edge** set + **replay-stable transition ids**; **defer-merge binding** forces transitions to respect **3.1.2** work-queue / deferral ledger ordering and **3.1.4** checkpoint barriers. **GWT-4.2.1-A–K** narrow **GWT-4.2-A–K** to this slice only. **Next structural cursor:** **4.2.2** (continue **4.2** chain). **Queue reconcile:** consumed stale queue line `followup-deepen-phase4-41-rollup-gmm-20260403T211500Z` as **authorized deepen** while vault cursor was already **4.2.1** (see [[workflow_state]] ## Log).

## Phase 4.2.1 — Session-scoped orchestration hooks and perspective transition graph

This **tertiary** decomposes **secondary 4.2** into NL contracts for **how** perspective control changes enter the system: only via **session-scoped orchestration hooks** that wrap a **PerspectiveTransitionGraph** (nodes = perspective modes from the Phase **4 primary** graph; edges = legal transitions with deterministic **transition_id** for replay). Hooks coordinate with **3.1.2** tick scheduling (deferral / merge) and **3.1.4** durability so control state never forks a second authority lane.

## Scope

**In scope:**

- **SessionOrchestrationEnvelope (NL)** — fields: `session_id`, `active_perspective_mode`, `pending_transition_request` (optional), `blocked_by_deferral` (bool), `checkpoint_barrier_class` (none | pre_tick | post_checkpoint) — all **control-affecting** inputs pass through this envelope before lane adapters (**4.1**) see updates.
- **PerspectiveTransitionGraph** — for each requested edge, record **source_mode**, **target_mode**, **transition_id** (stable hash inputs), **serialization_order** vs **3.1.2** `WorkItem` ids (conceptual reference only).
- **Hook triple** — `request_transition` (validate graph edge + deferral compatibility) → `schedule_merge_slot` (3.1.2) → `apply_control_commit` (after merge outcome; single writer).

**Out of scope:**

- UI animation curves, camera rig parameters, or input rebinding (**execution-deferred**).
- Closing execution-only **D-3.4-*** bundle rows (**execution-deferred**; see [[decisions-log]]).

## Behavior (natural language)

1. **Single ingress:** Any perspective or control-mode change arrives as a **SessionOrchestrationEnvelope**; narrative/rendering lanes (**4.1**) receive **projected** state only after `apply_control_commit`.
2. **Graph-first:** Illegal transitions (missing edge) are rejected at `request_transition` with a deterministic reason code — no partial application to either lane.
3. **Deferral dominance:** If **3.1.2** marks deferral for control-adjacent work, `request_transition` may return **blocked_by_deferral** until the deferral ledger clears — **no** lane-specific bypass.

## Interfaces

**Parent:**

- [[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]] — secondary **4.2** + **GWT-4.2-A–K**.

**Upstream:**

- [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — deferral ledger + merge matrix.
- [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — checkpoint barriers vs control commits.

**Phase 4 primary:**

- [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]] — mode graph + interpolator (nodes for transition graph).

## Edge cases

- **Transition requested mid-handoff:** Session handoff token from **4.2** secondary defers `apply_control_commit` until handoff completes — both lanes see **consistent** “handoff_active” presentation state.
- **Checkpoint barrier during transition:** If **3.1.4** requires a durability fence, `apply_control_commit` is ordered **after** checkpoint acknowledgment (ordering id ties to **3.1.2** merge outcome).

## Open questions

- Minimum **transition_id** alphabet size for cross-session replay audits (**execution-deferred** test matrix).
- Whether **forge-sourced** preview defaults (**D-3.1.5-***) may short-circuit **request_transition** — default **no** at conceptual layer (remains execution policy).

## Pseudo-code readiness

**Mid-technical:** structured field lists for **SessionOrchestrationEnvelope** + edge validation; executable pseudo-code deferred until **4.2.2+** if escalated.

## Tertiary slice GWT — narrowed vs **GWT-4.2-A–K**

| Narrow ID | Parent GWT | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- | --- |
| **GWT-4.2.1-A** | **GWT-4.2-A** | Active perspective mode | Transition requested | Request enters orchestration path via envelope | § Behavior (1) |
| **GWT-4.2.1-B** | **GWT-4.2-B** | **4.1** lane adapters | Control commit | Single committed control state | § SessionOrchestrationEnvelope |
| **GWT-4.2.1-C** | **GWT-4.2-C** | Deferred work pending | Transition | Ordering deterministic vs deferral | § Behavior (3) |
| **GWT-4.2.1-D** | **GWT-4.2-D** | Checkpoint class | Commit | Barrier respected | § Edge cases |
| **GWT-4.2.1-E** | **GWT-4.2-E** | Preview vs committed | Operator compares | No authority inversion | § Behavior (1) + **4.1** |
| **GWT-4.2.1-F** | **GWT-4.2-F** | Session handoff | Control input | Handoff policy + replay lineage | § Edge cases |
| **GWT-4.2.1-G** | **GWT-4.2-G** | Advisory execution gaps | Validator | Conceptual waiver explicit | [[roadmap-state]] |
| **GWT-4.2.1-H** | **GWT-4.2-H** | Coherence conflict | Reconciliation | Single graph truth | § PerspectiveTransitionGraph |
| **GWT-4.2.1-I** | **GWT-4.2-I** | Operator legibility | Transition shown | **4.1.3** presentation envelope honored | § Scope |
| **GWT-4.2.1-J** | **GWT-4.2-J** | Stress path | Cadence drop | Disclosure without reinterpretation | § Behavior (2) |
| **GWT-4.2.1-K** | **GWT-4.2-K** | **4.2** tertiaries | Next deepen | Evidence narrows in **4.2.2+** | this note |

## Research integration

- None for this slice (vault-first pattern).
