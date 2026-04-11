---
title: Phase 1.1.5 (Execution) — Cross-layer observability, test seams, and slice handoff
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - layering
  - observability
  - testing
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.5"
status: in-progress
handoff_readiness: 85
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment to conceptual 1.1.5, observability/test-seam contracts vs 1.1.1–1.1.4, and intent mapping; not evidence closure while AC rows remain Planned."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431]]"
---

# Phase 1.1.5 (Execution) — Cross-layer observability, test seams, and slice handoff

Execution tertiary **1.1.5** on the **parallel spine** under `Phase-1-1-Layering-and-Interface-Contracts/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431]]. Focus: **correlation-scoped diagnostics** across layers, **published test seams** (fake backends, clock control, golden inputs) that respect **commit authority** from [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2306]], and **slice handoff criteria** for declaring Phase **1.1** execution work coherent enough to deepen **1.2** (procedural generation graph skeleton) without reopening layer identities. **GMM-2.4.5** cross-lane harnesses and **CI / registry closure** remain **explicitly deferred** unless evidenced later.

Parent execution secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] · Prior tertiary: [[Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-04-10-2340]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, observability/test contracts, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**.

## Slice status vs execution cursor

- This note is the **1.1.5** execution spec slice (observability surfaces, test seams, 1.1.x slice handoff).
- After this mint, **`workflow_state-execution`** **`current_subphase_index`** advances to **`1.2`** (next deepen target: **Phase 1.2** secondary on the parallel spine).

## Alignment to conceptual Phase-1-1-5

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Per-layer diagnostics + single correlation id | `DiagnosticsRouter` + `correlation_id` threading at tick boundary | AC-1.1.5.E1 |
| Test doubles only at published seams | `TestHooks` registry + forbidden peer access table | AC-1.1.5.E2 |
| Slice handoff: 1.1.1–1.1.5 coherent before 1.2 | Handoff checklist + explicit “open debt” table | AC-1.1.5.E3 |

## Observability (execution)

**Rule:** Diagnostics are **layer-local emits** aggregated by tick; **no** layer calls another layer’s private internals for logging. **Correlation id** is carried on **intents** and echoed on **commit receipts** (wire format deferred).

> [!note] Notional pseudocode (dialect)
> Fenced blocks use **language-agnostic illustrative IL** (dot/member syntax is for readability when mapping to C++ engine seams). They are **not** committed C++ surface APIs.

```text
emit_layer_diagnostics(layer, tick, correlation_id):
  sink = diagnostics.resolve_sink(layer)
  sink.emit(tick, correlation_id, layer.summary_vector())  # no cross-layer peer calls
```

## Test seams (execution)

**Rule:** Tests attach only at **named hooks**: commit API ingress, intent ingress, render snapshot read, simulation clock control. **Forbidden:** tests reaching around a boundary into another layer’s private graph (mirrors conceptual NL).

| Seam | Allowed test hook | Forbidden |
| --- | --- | --- |
| World / commit | Fake `IWorldState` behind commit API | Direct mutation of ledger internals |
| Simulation | Clock-controlled stepper + deterministic RNG inject | Reading render private caches |
| Render | Golden inputs + snapshot read surface | Writing simulation intents |
| Input | Record/replay at normalized intent boundary | Bypassing validation policy |

## Slice handoff checklist (1.1.x → 1.2)

| Gate | Evidence expectation (this track) | Status |
| --- | --- | --- |
| G-1.1.H1 | Tertiaries **1.1.1–1.1.5** each have Intent Mapping + AC hooks | Planned |
| G-1.1.H2 | No silent crossing of forbidden boundaries across the stack | Planned |
| G-1.1.H3 | Explicit deferrals for GMM-2.4.5 / CI remain visible in phase notes | Met (deferral tables) |

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.1.5.E1 | Correlation id present on intent drain + commit digest rows | `correlation_trace.jsonl` | Planned |
| AC-1.1.5.E2 | Test hook registry lists only published seams; peer-access attempts fail closed | `test_seam_audit.txt` | Planned |
| AC-1.1.5.E3 | Handoff memo links 1.1.x AC statuses + open debt before 1.2 deepen | `slice_handoff_1_1.md` | Planned |

> [!tip] Roll-up posture (execution debt)
> While **E1–E3** remain **Planned**, project-scale **roll-up gates**, **registry/CI-shaped closure**, and **GMM-2.4.5** harness work stay **explicitly deferred** per this slice and [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] — not hidden behind “done” language.

## Intent mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Observability without peer coupling (conceptual 1.1.5) | Conceptual NL + 1.1.1 commit authority | `emit_layer_diagnostics` + correlation threading | AC-1.1.5.E1 |
| Deterministic test seams | Published boundaries from 1.1.1–1.1.4 | `TestHooks` + forbidden table | AC-1.1.5.E2 |
| Slice handoff | Conceptual “close 1.1.x” | Checklist + handoff memo | AC-1.1.5.E3 |

## Risks (v0)

| Risk | Mitigation | Linked AC |
| --- | --- | --- |
| Diagnostics re-entrancy / peer calls | Layer-local sinks only | AC-1.1.5.E1 |
| Tests bypassing commit API | Fail-closed registry | AC-1.1.5.E2 |
| Scope creep into telemetry backends / CI | Explicit deferrals | Deferrals |

## Explicit deferrals

- **GMM-2.4.5-*** comparator / cross-lane harness: not claimed.
- **CI** gates (coverage, stress matrices): not claimed.
- **New** verbatim C/C++ standard API citations: deferred to a future Research-backed pass with allowlisted URLs; this slice uses **pseudocode** and **reuse-only** references to sibling execution notes (same pattern as execution **1.1.4**).

## Related execution slices

- [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2306]] — commit authority + ingress seams
- [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-10-2315]] — cache/epoch observability coupling
- [[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-04-10-2325]] — lifecycle hooks for test doubles
- [[Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-04-10-2340]] — failure routing vs diagnostics

## Research integration

> [!note] External grounding
> No nested Research **`Task`** was required this run: pseudocode-only execution narrative; **§0** URL scan clean on queue hand-off; util-based research auto-enable did not trigger (**confidence** veto). **GMM-2.4.5 / CI** remain deferred per `user_guidance`.
