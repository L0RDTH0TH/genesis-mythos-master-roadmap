---
title: Phase 1.1 (Execution) — Layering and Interface Contracts
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - layering
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
---

# Phase 1.1 (Execution) — Layering and Interface Contracts

Execution secondary **1.1** on the parallel spine. Tightens **interface boundaries** between scheduler, ledger, dispatch, and presentation seams relative to the Phase 1 execution primary; expands **pseudocode seams** for handoff points; adds **AC evidence rows** with explicit artifact hooks. **GMM-2.4.5** lineage/compare harnesses and **CI closure** automation remain **explicitly deferred** unless/until evidenced in a later execution slice.

Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]] · Primary execution container: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Boundary matrix (execution-tightened)

| Boundary | Upstream contract | Downstream contract | Forbidden crossing |
| --- | --- | --- | --- |
| Scheduler ↔ Ledger | Checkpoint identity + monotonic tick | Atomic read/write pairs keyed by `(session_id, tick)` | Partial publish of ledger state mid-tick without commit token |
| Dispatch ↔ Scheduler | Ordered intent batch per tick with idempotency key | Single merge pass into scheduler step | Scheduler reading presentation packets |
| Ledger ↔ Dispatch | Event envelope schema version + causal predecessor id | Replayable trace rows | Direct world mutation from dispatch without ledger receipt |
| Presentation ↔ Dispatch | Projection packet per tick with schema id | Consumer ack or drop policy | Presentation feeding intents without input normalization |

## Pseudocode seams (expanded)

Seams mark **where** authoritative data changes ownership; they are not a full engine implementation (depth-2 execution slice).

```text
seam tick_boundary(scheduler, ledger, dispatch, presentation, tick):
  pre = ledger.checkpoint_token(tick - 1)
  intents = dispatch.drain_ordered_intents(tick, pre)
  stepped = scheduler.step(ledger.view(pre), intents, tick)
  commit = ledger.prepare_commit(stepped, tick)   # ownership: ledger
  dispatch.publish_after_commit(commit.projection_envelope, tick)
  presentation.emit_visible_packets(commit.projection_envelope, tick)
  ledger.finalize(commit)                         # single committer; no render write-back
  return ledger.digest(tick)
```

```text
seam intent_ingress(input_normalized, dispatch, tick):
  envelope = input_normalized.to_intent_envelope(tick)
  dispatch.accept(envelope)  # idempotent insert; may reject with reason code
```

## Acceptance criteria — evidence rows

Evidence is **planned** here; artifacts are named so a future run can attach concrete paths without reopening conceptual scope.

| ID | Criterion | Evidence artifact (planned hook) | Status |
| --- | --- | --- | --- |
| AC-1.1.E1 | Ledger commit token prevents replay of the same tick without invalidation | `ledger_commit_trace.jsonl` row: `{tick, token, digest}` | Planned |
| AC-1.1.E2 | Dispatch ordering has zero inversion vs scheduler merge order | `dispatch_order_audit.log` with predecessor chain | Planned |
| AC-1.1.E3 | Presentation packets validate against declared schema id per tick | `packet_schema_validation.tsv` (tick, schema_id, ok) | Planned |
| AC-1.1.E4 | Seed bundle replay yields identical final digest (sandbox lane) | `replay_digest_compare.txt` (two runs, one hash line each) | Planned |

> Deferral: **GMM-2.4.5** comparator tables, registry/CI closure, and cross-lane stress harnesses are **out of scope** for this slice unless evidence is explicitly attached later — aligns with conceptual execution-deferral waiver.

## Lane comparand (sandbox vs godot)

| Concern | Sandbox B (this slice) | Godot A (reference) | Shared contract |
| --- | --- | --- | --- |
| Tick ownership | C++ scheduler + explicit commit boundary | `_physics_process` frame vs idle separation | One authoritative tick clock per session |
| Intent ingress | Normalized envelope + idempotency | InputMap / action → `InputEvent` path | Single intent pipeline into simulation |
| Projection | Renderer-agnostic packet schema | Scene tree / viewport consumption | Sim-visible data crosses only via packet seam |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Four-layer stack with one-way data flow | Conceptual 1.1 NL behavior + Phase 1 primary seams | Boundary matrix + pseudocode seams encode commit order and forbidden crossings | AC-1.1.E1–E4 evidence hooks can be wired without changing conceptual text |
| Deterministic replay readiness | PMG invariants + primary `IStateLedgerStore` | Ledger token + digest at each tick boundary | AC-1.1.E4 digest compare; GMM-2.4.5 harness deferred |
| Presentation isolation | Conceptual render read-only rule | `presentation.emit_visible_packets` only after commit | AC-1.1.E3 schema validation |

## Risks (v0)

| Risk | Mitigation (this slice) | Linked AC |
| --- | --- | --- |
| Seam ordering drift between scheduler, ledger, and dispatch | Boundary matrix + `tick_boundary` pseudocode enforce single committer | AC-1.1.E2 |
| Idempotency key collisions on intent ingress | `intent_ingress` seam + dispatch accept path; ordered drain | AC-1.1.E2 |
| Projection/schema drift vs lane comparand | Evidence hook `packet_schema_validation.tsv`; comparand table | AC-1.1.E3 |
| Premature presentation read before commit | `tick_boundary` ordering; forbidden-crossing row | AC-1.1.E1 |
| Residual GMM-2.4.5 / CI scope creep | Explicit deferrals; no closure claimed without artifacts | Deferrals block |

## Handoff readiness basis

- Boundary matrix and pseudocode seams document **forbidden crossings** and **commit order** aligned to conceptual 1.1 NL stack.
- AC evidence rows name **plannable hooks** (`ledger_commit_trace`, `dispatch_order_audit`, etc.) without claiming GMM-2.4.5 or CI artifacts.
- Intent Mapping ties design intent → execution mechanism → validation signal for each seam family.
- Lane comparand preserves **sandbox vs godot** contract without mixing GDScript into C++ precision blocks.

## Explicit deferrals

- **GMM-2.4.5-*** comparator / lineage closure: not claimed here; execution-track slice must add evidence headers if introduced later.
- **CI** automation (coverage thresholds, stress matrices, report gates): deferred; this slice only names evidence hooks.
- **Cross-lane** long-run replay matrix: deferred to execution Phase 2+ or dedicated lane queue.

## Code precision (reuse-only)

No new C/C++ API surfaces were introduced in this slice beyond **reference-only** patterns already cited on the Phase 1 execution primary ([[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] **Code precision authority**). Additional verbatim citations will be added when tertiary **1.1.x** notes introduce new constructs.

## Next structural intent

Deepen execution tertiary **1.1.1** on the mirrored spine (layer boundary + commit pipeline), unless a RECAL gate supersedes.
