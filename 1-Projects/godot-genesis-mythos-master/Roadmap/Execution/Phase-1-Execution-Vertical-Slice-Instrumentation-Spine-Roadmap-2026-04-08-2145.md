---
title: Phase 1 (Execution) — Vertical-Slice Instrumentation Spine
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 86
---

# Phase 1 (Execution) — Vertical-slice instrumentation spine

Execution-track **Phase 1** establishes the **first concrete binding** between conceptual **Phase 6** vertical-slice artifacts ([[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]], secondary [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]], tertiaries **6.1.1–6.1.3**) and **operator-visible instrumentation** paths that can be iterated without mutating frozen conceptual notes.

## Scope

- **In scope (execution):** stub **instrumentation spine** contracts (ObservationChannel → PresentationEnvelope handoff, bounded tick windows, manifest field registry rows) as **implementation-shaped** checklists — not claiming registry/CI closure (`GMM-2.4.5-*` remains execution-deferred per [[decisions-log]]).
- **Out of scope:** rewriting conceptual Phase 6 notes; any change under `Roadmap/**` excluding `Execution/` that would violate freeze policy.

## NL checklist (Phase 1 entry)

- [x] Name the **three** execution binding surfaces imported from conceptual **6.1.x** (manifest/admission, tick/sim-visible matrix, observation/readout) with vault links:
  - **Manifest / registry / instrumentation envelope:** [[../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]
  - **Bounded tick / sim-visible matrix:** [[../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]
  - **ObservationChannel → presentation readout:** [[../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]
- [x] Declare **one** minimal **vertical-slice happy path** (seed → first tick → one ObservationChannel sample → PresentationEnvelope stub) as prose-only: operator supplies **seed bundle** → engine runs **first committed tick** (per **2.7.3** trace vocabulary, conceptual) → **ObservationChannel** emits one labeled sample row → **PresentationEnvelope** stub renders operator-visible readout (no host binary; execution-deferred).
- [x] List **execution-deferred** items explicitly (compare tables, CI retention proofs) with pointer to [[../distilled-core]] deferral language (e.g. **`GMM-2.4.5-*`**, registry/CI closure — **execution track** per [[decisions-log]] **Track:** line).

## GWT-1-Exec-A–C (execution spine — initial)

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-1-Exec-A | Conceptual **6.1.x** binding surfaces are named and linked for execution import | § NL checklist (checked) + § Handoff from conceptual Phase 6 |
| GWT-1-Exec-B | No authoritative gate is framed as blocking **conceptual** completion | § Out of scope + [[../roadmap-state]] `roadmap_track: execution` |
| GWT-1-Exec-C | Next execution deepen target is machine-resolvable from [[workflow_state-execution]] | Parent state files + ## Log |

## Handoff from conceptual Phase 6

- Primary rollup closure: CDR [[Conceptual-Decision-Records/deepen-phase-6-primary-rollup-nl-gwt-active-tree-2026-04-07-2105]].
- Secondary **6.1** rollup (active tree): CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]].

## Open questions

- **Resolved (policy):** execution-local numbering vs conceptual **6.1.x** mirrors — see [[../decisions-log]] **D-Exec-1-numbering-policy (2026-04-08)**.

## Execution progress semantics

- **Child slices:** for each execution note listed under § **Execution child slices** (at last vault sync: **`1.1`–`1.4`**), frontmatter **`progress`** is **slice-local** (0–100) for that execution note only.
- **This Phase 1 spine (parent):** **`progress`** = **max** of **`progress`** on linked **Execution child slices** listed under § **Execution child slices** at last vault sync (recompute after a child slice deepens or materially changes).
- **Rationale:** avoids reading the parent bar as “behind” a child when the parent is a rollup container — see [[../decisions-log]] **D-Exec-1-parent-progress-rollup**.

## Execution child slices (1.x)

- **1.1 — Godot engine binding surfaces vs sandbox A/B parity:** [[Phase-1-1-Godot-Engine-Binding-Surfaces-Sandbox-AB-Parity-Roadmap-2026-04-08-2300]] (mint **2026-04-08 23:00Z**, queue `followup-deepen-execution-phase1-godot-gmm-20260408T230000Z`).
- **1.2 — Registry / telemetry stub slice (A/B parity):** [[Phase-1-2-Registry-Telemetry-Stubs-Sandbox-AB-Parity-Roadmap-2026-04-09-0000]] (mint **2026-04-09 00:00Z**, queue `followup-deepen-exec-phase1-2-registry-stubs-godot-gmm-20260409T000000Z`) — artifact path table, **`GMM-2.4.5-*`** deferral rows, links **1.1** ↔ **1.2**.
- **1.3 — Instrumentation harness / ObservationChannel stub (A/B parity):** [[Phase-1-3-Instrumentation-Harness-ObservationChannel-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-0100]] (mint **2026-04-09 01:00Z**, queue `followup-deepen-exec-phase1-3-instrumentation-harness-stub-godot-gmm-20260409T010000Z`) — harness wiring **1.1** surfaces → **1.3** stub → **1.2** sinks; **no** **`GMM-2.4.5-*`** closure.
- **1.4 — PresentationEnvelope stub (A/B parity):** [[Phase-1-4-PresentationEnvelope-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-1830]] (mint **2026-04-09 18:30Z**, queue `followup-deepen-exec-phase1-3-instrumentation-harness-stub-godot-gmm-20260409T010000Z` — **forward deepen** after **1.3** satisfied) — **1.3** sample → **1.4** readout stub; sandbox role-parity vs [[1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/Phase-1-2-PresentationEnvelope-Stub-Roadmap-2026-04-06-1200]].

## Related

- [[roadmap-state-execution]]
- [[workflow_state-execution]]
- [[../roadmap-state]]
