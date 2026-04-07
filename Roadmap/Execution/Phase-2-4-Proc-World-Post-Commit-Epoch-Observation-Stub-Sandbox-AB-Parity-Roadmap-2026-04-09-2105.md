---
title: Phase 2.4 (Execution) — Post-commit epoch observation & reconciliation stub (sandbox A/B parity)
created: 2026-04-09
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2-4
  - godot
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 86
parent_slice: Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016
execution_local_index: "2.4"
conceptual_counterpart: "[[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2.4 (Execution) — Post-commit epoch observation & reconciliation stub (A/B vs sandbox reference)

**Execution-local slice `2.4`** under [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]], sibling to [[Phase-2-3-Proc-World-Staging-Commit-Integration-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2030]], per [[../decisions-log]] **D-Exec-1-numbering-policy**. This note defines **vault-only** contracts for **what is observable after a committed epoch**—**epoch_id**, **reconciliation tick**, **drift observation rows**, and **Presentation-facing readout hooks**—without claiming registry CI, compare-table closure, or **`GMM-2.4.5-*`** “done” until **scripts/CI** exist (**D-Exec-1.2-GMM-245-stub-vs-closure**).

## Scope

- **In scope:** Name **post-commit** surfaces that bridge **2.3** `world_snapshot_ref` / committed state to **downstream readout**: monotonic **`epoch_id`** (string stub), **`reconciliation_seq`** (int stub), **drift_observation** envelope kind (lane A/B comparable), and **PresentationReadoutRowStub** continuity from **Phase 1** **1.4** (opaque string ids only).
- **Out of scope:** Real engine persistence, **GMM-2.4.5-*** compare/rollup/retention closure, production **registry JSONL** writers — **execution-deferred** per parent spine and [[../distilled-core]].

## Post-commit / epoch surface inventory (adapter layer)

| Surface | Role in spine | Godot hook (lane A) | Sandbox reference hint (lane B) |
| --- | --- | --- | --- |
| **Epoch id** | Stable label for a committed world slice post-**2.3** | **`epoch_id`** string on `epoch_observation` rows; ties to **2.3** `world_snapshot_ref` | Same id width; if B cannot represent epochs, `parity_gap: true` |
| **Reconciliation seq** | Ordering for drift/reconcile ticks without implying validator stack closure | Monotonic **`reconciliation_seq`** on `reconcile_tick` kinds | Same monotonic rule; optional `unsupported` |
| **Drift observation** | Detect post-commit mismatch signals at stub depth | **`drift_observation`** kind + **`drift_code`** stub enum | Symmetric enum; extra codes → `parity_gap` |
| **Presentation bridge** | Route epoch readout toward **1.4** | Reuse **`PresentationReadoutRowStub`** vocabulary; add **`epoch_readout`** kind optional | B mirrors or marks **`unsupported`** |
| **Registry deferral row** | Explicit **non-closure** for **GMM-2.4.5-*** | Stub row `{ "kind": "registry_deferral_ref", "gmm_ref": "GMM-2.4.5-SCHEMA", "status": "deferred_until_scripts_ci" }` | Same shape |

## A/B parity contract (operator-visible)

1. **Same envelope schema family:** Epoch/drift rows stay inside **InstrumentationIntentEnvelope** vocabulary; lane metadata (`queue_lane: godot` \| `sandbox`) required; **`GMM-2.4.5-*`** closure remains **execution-deferred**.
2. **Divergence logging:** Godot-only epoch surfaces that B cannot mirror → **`parity_gap: true`** stub rows — **not** silent drop.
3. **Non-closure row:** Do **not** claim **SCHEMA / RETENTION / VALIDATOR-COMPARE-TABLE** for **`GMM-2.4.5-*`** until **scripts/CI** exist.

## NL checklist (2.4 mint)

- [x] Enumerate **≥5** distinct **post-commit / epoch** loci tied to **2.3** commits and Phase **2** spine (table above).
- [x] State **A/B parity** rules: shared schema family, explicit gap flags — **no** **`GMM-2.4.5-*`** closure.
- [x] Link parent spine + **2.3** continuity and **1.4** Presentation bridge without rewriting conceptual **Phase 2** body.

## Acceptance hooks (post–IRA evidence)

- **H1:** **`epoch_id`** + **`reconciliation_seq`** appear as **named fields** on epoch observation rows — stub: `{ "kind": "epoch_observation", "epoch_id": "ep_phase2_stub_04", "reconciliation_seq": 4 }`.
- **H2:** **Drift** paths are named without implying **GMM-2.4.5-*** closure — stub `{ "kind": "drift_observation", "drift_code": "staging_mismatch_stub" }`.
- **H3:** **Registry deferral** remains an explicit **deferred** row — stub `{ "kind": "registry_deferral_ref", "gmm_ref": "GMM-2.4.5-SCHEMA", "status": "deferred_until_scripts_ci" }`.

## GWT-2-4-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-4-Exec-A | Post-commit / epoch surfaces are named and mapped to **2.3** commits + instrumentation continuity | § Post-commit / epoch surface inventory |
| GWT-2-4-Exec-B | Sandbox lane is referenced as **comparand**, not authority over conceptual Phase 2 | § Scope + A/B parity contract |
| GWT-2-4-Exec-C | Slice is discoverable as **`2.4`** under execution-local policy | Frontmatter `execution_local_index` + parent link |

## Related

- Parent: [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]]
- Prior sibling: [[Phase-2-3-Proc-World-Staging-Commit-Integration-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2030]]
- Upstream proc stub: [[Phase-2-1-Proc-World-Execution-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2020]]
- Presentation continuity: [[Phase-1-4-PresentationEnvelope-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-1830]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- [[../decisions-log]] (**D-Exec-1-numbering-policy**, **D-Exec-1.2-GMM-245-stub-vs-closure**)
