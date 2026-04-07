---
title: Phase 2.5 (Execution) — Epoch→Presentation operator readout stub (sandbox A/B parity)
created: 2026-04-09
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2-5
  - godot
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 86
parent_slice: Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016
execution_local_index: "2.5"
conceptual_counterpart: "[[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2.5 (Execution) — Epoch→Presentation operator readout stub (A/B vs sandbox reference)

**Execution-local slice `2.5`** under [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]], sibling to [[Phase-2-4-Proc-World-Post-Commit-Epoch-Observation-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2105]], per [[../../decisions-log]] **D-Exec-1-numbering-policy**. This note defines **vault-only** contracts for **routing post-epoch signals into Presentation-facing readouts and operator escalation rows**—without claiming registry CI, compare-table closure, or **`GMM-2.4.5-*`** “done” until **scripts/CI** exist (**D-Exec-1.2-GMM-245-stub-vs-closure**).

## Scope

- **In scope:** Name **readout / escalation** surfaces that bridge **2.4** `epoch_observation` / `drift_observation` rows to **Phase 1** **1.4** `PresentationReadoutRowStub` vocabulary and **operator-visible** escalation hooks: **`operator_readout_row`**, **`escalation_severity`** stub enum, **`presentation_bridge_kind`**, and **rollup readiness** flags at stub depth only.
- **Out of scope:** Production UI bindings, **GMM-2.4.5-*** compare/rollup/retention closure, production **registry JSONL** writers — **execution-deferred** per parent spine and [[../../distilled-core]].

## Readout / escalation surface inventory (adapter layer)

| Surface | Role in spine | Godot hook (lane A) | Sandbox reference hint (lane B) |
| --- | --- | --- | --- |
| **Operator readout row** | Human-legible row derived from epoch/drift without implying validator closure | **`operator_readout_row`** kind + **`readout_summary_ref`** opaque id | Same shape; if B cannot surface operator rows, `parity_gap: true` |
| **Escalation severity** | Ordered signal for “needs attention” without HR/CI proof | Stub enum **`escalation_severity`**: `info \| warn \| block_stub`** | Same enum width; extra severities → `parity_gap` |
| **Presentation bridge kind** | Tie epoch/drift to Presentation stub family | **`presentation_bridge_kind`** + optional **`epoch_readout`** cross-ref to **2.4** | B mirrors or marks **`unsupported`** |
| **Rollup readiness flag** | Phase **2** spine bookkeeping (not closure) | **`phase2_spine_rollup_readiness: not_ready \| stub_ready`** — **no** compare-table claim | Same flag; **no** **`GMM-2.4.5-*`** satisfied |
| **Registry deferral row** | Explicit **non-closure** for **GMM-2.4.5-*** | Stub row `{ "kind": "registry_deferral_ref", "gmm_ref": "GMM-2.4.5-VALIDATOR-COMPARE-TABLE", "status": "deferred_until_scripts_ci" }` | Same shape |

## A/B parity contract (operator-visible)

1. **Same envelope schema family:** Readout rows stay inside **InstrumentationIntentEnvelope** vocabulary; lane metadata (`queue_lane: godot` \| `sandbox`) required; **`GMM-2.4.5-*`** closure remains **execution-deferred**.
2. **Divergence logging:** Godot-only readout surfaces that B cannot mirror → **`parity_gap: true`** stub rows — **not** silent drop.
3. **Non-closure row:** Do **not** claim **SCHEMA / RETENTION / VALIDATOR-COMPARE-TABLE** for **`GMM-2.4.5-*`** until **scripts/CI** exist.

## NL checklist (2.5 mint)

- [x] Enumerate **≥5** distinct **readout / escalation** loci tied to **2.4** epoch/drift and Phase **2** spine (table above).
- [x] State **A/B parity** rules: shared schema family, explicit gap flags — **no** **`GMM-2.4.5-*`** closure.
- [x] Link parent spine + **2.4** continuity and **1.4** Presentation bridge without rewriting conceptual **Phase 2** body.

## Acceptance hooks (post–IRA evidence)

- **H1:** **`operator_readout_row`** appears as a **named kind** with **`readout_summary_ref`** — stub: `{ "kind": "operator_readout_row", "readout_summary_ref": "orr_phase2_stub_05", "escalation_severity": "warn" }`.
- **H2:** **Presentation bridge** is named without implying **GMM-2.4.5-*** closure — stub `{ "kind": "presentation_bridge", "presentation_bridge_kind": "epoch_to_readout", "epoch_id": "ep_phase2_stub_04" }`.
- **H3:** **Registry deferral** remains an explicit **deferred** row — stub `{ "kind": "registry_deferral_ref", "gmm_ref": "GMM-2.4.5-SCHEMA", "status": "deferred_until_scripts_ci" }`.

## GWT-2-5-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-5-Exec-A | Readout / escalation surfaces are named and mapped to **2.4** epoch/drift + Presentation continuity | § Readout / escalation surface inventory |
| GWT-2-5-Exec-B | Sandbox lane is referenced as **comparand**, not authority over conceptual Phase 2 | § Scope + A/B parity contract |
| GWT-2-5-Exec-C | Slice is discoverable as **`2.5`** under execution-local policy | Frontmatter `execution_local_index` + parent link |

## Related

- Parent: [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]]
- Prior sibling: [[Phase-2-4-Proc-World-Post-Commit-Epoch-Observation-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2105]]
- Presentation continuity: [[Phase-1-4-PresentationEnvelope-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-1830]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- [[../../decisions-log]] (**D-Exec-1-numbering-policy**, **D-Exec-1.2-GMM-245-stub-vs-closure**)
