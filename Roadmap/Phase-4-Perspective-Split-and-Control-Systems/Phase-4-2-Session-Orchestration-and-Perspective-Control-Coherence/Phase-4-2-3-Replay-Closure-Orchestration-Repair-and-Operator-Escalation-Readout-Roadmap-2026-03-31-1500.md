---
title: Phase 4.2.3 — Replay closure, orchestration repair, and operator escalation readout
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 58
progress_semantics: slice_narrative_depth_not_percent_complete
handoff_readiness: 87
created: 2026-03-31
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]]"
  - "[[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]]"
  - "[[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 87` — tertiary **4.2.3** — **ReplayClosureBundle** (minimum field set + hash chain for cross-session audit) + **OrchestrationRepairToken** ladder after **4.2.2** `parity_violation` / frozen transitions + **operator escalation readout** (DM vs auditor lanes) bound to **TransitionOutcomeLedger** rows — **reconciled** stale queue **`user_guidance`** (secondary **4.1** rollup / cursor **4.1**) vs authoritative **`workflow_state.current_subphase_index: "4.2.3"`** pre-mint; queue **`followup-deepen-phase4-41-rollup-gmm-20260403T211500Z`**. **GWT-4.2.3-A–K** narrow **GWT-4.2-A–K**. **Tertiary chain 4.2.1–4.2.3** structurally complete; **next:** **secondary 4.2 rollup** (NL + **GWT-4.2** parity vs **4.2.1–4.2.3**). **`parent_run_id: a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d`** \| **`pipeline_task_correlation_id: b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e`**.

## Phase 4.2.3 — Replay closure, orchestration repair, and operator escalation readout

This **tertiary** closes the **4.2** stress path after **4.2.2**: replays must admit a **minimum auditable bundle** independent of forge UI, **repair** must be token-governed (no silent graph edits), and **operators** must see escalation classes that map to ledger rows — without duplicating Phase **2.3** pre-commit machinery.

## Scope

**In scope:**

- **ReplayClosureBundle (NL)** — deterministic minimum: ordered **`commit_seq`** tail + **`session_id`** + **`orchestration_hash`** chain + **`ledger_checkpoint_ref`** (pointer into **TransitionOutcomeLedger**) sufficient to re-derive **LaneProjectionParityPredicate** outcomes for a bounded window (**4.2.2**).
- **OrchestrationRepairToken** — typed tokens (**rollback_to_commit_seq** \| **invalidate_transition** \| **force_single_writer_repair**) issued only through **4.2.1** `apply_control_commit` seam after **4.2.2** **`parity_violation`** or freeze; tokens carry **reason_code** + **attested_ledger_row_id** (no body overwrite of frozen conceptual parents).
- **OperatorEscalationReadout** — role-scoped summaries (DM vs auditor) that cite **ledger row ids** + **4.1.3** presentation-time validation labels — **legibility** without a second authority lane.

**Out of scope:**

- External audit export formats, Merkle batching, or CI compare tables (**execution-deferred** per **D-2.4.5-*** style anchors).
- Forge panel layout / hotkeys.

## Behavior (natural language)

1. **Closure before handoff:** No **cross-session** consumer may claim “replay-safe” without a **ReplayClosureBundle** that validates against **4.2.2** ledger projections.
2. **Repair is never silent:** **OrchestrationRepairToken** must log to **TransitionOutcomeLedger** as a synthetic row class **`repair_event`** (append-only) before lanes may publish post-repair projections.
3. **Escalation binds to ledger:** **OperatorEscalationReadout** rows reference **`transition_id`** + **`commit_seq`**; **4.1.3** checks that operator-visible text does not contradict **`repair_event`** outcomes.

## Interfaces

**Parent:**

- [[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]] — secondary **4.2** + **GWT-4.2-A–K**.

**Upstream:**

- [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]] — ledger + parity + **4.1.3** binding.
- [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]] — hooks + `apply_control_commit`.
- [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] — presentation-time validation vs ledger.

## Edge cases

- **Partial bundle on crash:** If **ReplayClosureBundle** is incomplete, consumers enter **degraded_readout** — still single-writer via **4.2.1** (no forked perspective authority).
- **Repair storm:** Multiple **`parity_violation`** events in one tick — **OrchestrationRepairToken** serializes by **`commit_seq`** (deterministic tie-break: lower **`transition_id`** first).

## Open questions

- Cap on **`repair_event`** rows per session before mandatory **RECAL-ROAD** hygiene (**execution-deferred** policy).
- Whether **auditor** readout may omit DM-only narrative emphasis (**execution-deferred** RBAC).

## Pseudo-code readiness

**Mid-technical:** struct sketches for **ReplayClosureBundle**, **OrchestrationRepairToken**, **OperatorEscalationReadout**; deterministic ordering lemmas reference **4.2.2** digest fields.

## Tertiary slice GWT — narrowed vs **GWT-4.2-A–K**

| Narrow ID | Parent GWT | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- | --- |
| **GWT-4.2.3-A** | **GWT-4.2-A** | Session active | Cross-session replay claimed | Bundle validates | § ReplayClosureBundle |
| **GWT-4.2.3-B** | **GWT-4.2-B** | Parity break | Repair | Token + ledger row | § OrchestrationRepairToken |
| **GWT-4.2.3-C** | **GWT-4.2-C** | Deferred narrative | Repair path | Ordering in ledger | § Behavior (2) |
| **GWT-4.2.3-D** | **GWT-4.2-D** | Checkpoint | Bundle | Barrier ref present | § Scope |
| **GWT-4.2.3-E** | **GWT-4.2-E** | Preview vs committed | Readout | No contradiction | § Behavior (3) |
| **GWT-4.2.3-F** | **GWT-4.2-F** | Handoff | Export | Closure attached | § Interfaces |
| **GWT-4.2.3-G** | **GWT-4.2-G** | Advisory | Validator | Waiver explicit | [[roadmap-state]] |
| **GWT-4.2.3-H** | **GWT-4.2-H** | Coherence | Escalation | Maps to ledger | § OperatorEscalationReadout |
| **GWT-4.2.3-I** | **GWT-4.2-I** | Operator legibility | DM/auditor | Scoped | § Scope |
| **GWT-4.2.3-J** | **GWT-4.2-J** | Stress path | Repair storm | Serialized | § Edge cases |
| **GWT-4.2.3-K** | **GWT-4.2-K** | **4.2** chain | Rollup next | Evidence in **4.2.1–4.2.3** | this note |

## Research integration

- None for this slice (vault-first pattern).
