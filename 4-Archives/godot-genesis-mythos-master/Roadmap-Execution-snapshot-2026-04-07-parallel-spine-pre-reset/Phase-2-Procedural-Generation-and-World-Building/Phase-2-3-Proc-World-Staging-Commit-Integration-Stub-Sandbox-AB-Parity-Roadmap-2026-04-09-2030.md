---
title: Phase 2.3 (Execution) — Staging → commit integration stub (sandbox A/B parity)
created: 2026-04-09
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2-3
  - godot
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 86
parent_slice: Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016
execution_local_index: "2.3"
conceptual_counterpart: "[[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2.3 (Execution) — Staging → commit integration stub (A/B vs sandbox reference)

**Execution-local slice `2.3`** under [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]], sibling to [[Phase-2-2-Proc-World-Chunk-Graph-Staging-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2025]], per [[../../decisions-log]] **D-Exec-1-numbering-policy**. This note defines **vault-only** contracts for **turning staged proc/graph outputs into committed world snapshots**—**commit barriers**, **idempotency keys**, and **deny/defer** shaped rows—without claiming registry CI, compare-table closure, or **`GMM-2.4.5-*`** “done” until **scripts/CI** exist (**D-Exec-1.2-GMM-245-stub-vs-closure**).

## Scope

- **In scope:** Name **integration** surfaces between **2.2** staging buffers and a **committed epoch** of world/chunk state: **commit_barrier_id**, **staging_fingerprint**, **world_snapshot_ref** (opaque stub), and **orchestration intents** aligned to conceptual **2.4.1** lineage vocabulary at **stub** depth only.
- **Out of scope:** Real engine transaction APIs, **GMM-2.4.5-*** compare/rollup/retention closure, production **registry JSONL** writers — **execution-deferred** per parent spine and [[../../distilled-core]].

## Commit / integration surface inventory (adapter layer)

| Surface | Role in spine | Godot hook (lane A) | Sandbox reference hint (lane B) |
| --- | --- | --- | --- |
| **Commit barrier** | Ordering boundary for staged → committed transition | Monotonic **`commit_seq`** + **`commit_barrier_id`** on envelope rows; ties to **2.2** `commit_epoch` | Same **`commit_seq`** monotonic rule; if B cannot represent barriers, `parity_gap: true` |
| **Staging fingerprint** | Detect no-op vs changed staging payload | Hash stub field **`staging_fingerprint`** (string) carried across `staging_preview` → `commit_request` kinds | Same field; optional `unsupported` when B lacks hashing |
| **World snapshot ref** | Opaque pointer post-commit graph/chunk state | **`world_snapshot_ref`** string table id (no binary payload in vault) | Symmetric string id; extra columns → `parity_gap` |
| **Deny / defer row** | Pre-commit gating without claiming full validator stack | `commit_decision: allow \| deny \| defer` + **`deny_reason_code`** stub enum | Same enum width; unknown codes → `parity_gap` |
| **Observation bridge** | Post-commit visibility before Presentation | Reuse **1.4** readout kinds where possible; add **`commit_observation`** kind optional | B mirrors or marks **`unsupported`** |

## A/B parity contract (operator-visible)

1. **Same envelope schema family:** Commit rows stay inside **InstrumentationIntentEnvelope** vocabulary; lane metadata (`queue_lane: godot` \| `sandbox`) required; **`GMM-2.4.5-*`** closure remains **execution-deferred**.
2. **Divergence logging:** Godot-only commit surfaces that B cannot mirror → **`parity_gap: true`** stub rows — **not** silent drop.
3. **Non-closure row:** Do **not** claim **SCHEMA / RETENTION / VALIDATOR-COMPARE-TABLE** for **`GMM-2.4.5-*`** until **scripts/CI** exist.

## NL checklist (2.3 mint)

- [x] Enumerate **≥5** distinct **commit / integration** loci tied to **2.2** staging and Phase **2** spine (table above).
- [x] State **A/B parity** rules: shared schema family, explicit gap flags — **no** **`GMM-2.4.5-*`** closure.
- [x] Link parent spine + **2.2** continuity without rewriting conceptual **Phase 2** body.

## Acceptance hooks (post–IRA evidence)

- **H1:** **`commit_barrier_id`** + **`commit_seq`** appear as **named fields** on commit request rows — stub: `{ "kind": "commit_request", "commit_barrier_id": "cb_0007", "commit_seq": 7, "staging_fingerprint": "fp_stub_01" }`.
- **H2:** **Deny/defer** paths are named without implying **GMM-2.4.5-*** closure — stub `{ "kind": "commit_decision", "commit_decision": "defer", "defer_reason_code": "validator_chain_deferred" }`.
- **H3:** **World snapshot** reference is **opaque string id only** at vault depth — stub `{ "kind": "commit_observation", "world_snapshot_ref": "wsnap_phase2_stub_03" }`.

## GWT-2-3-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-3-Exec-A | Commit/integration surfaces are named and mapped to **2.2** staging + instrumentation continuity | § Commit / integration surface inventory |
| GWT-2-3-Exec-B | Sandbox lane is referenced as **comparand**, not authority over conceptual Phase 2 | § Scope + A/B parity contract |
| GWT-2-3-Exec-C | Slice is discoverable as **`2.3`** under execution-local policy | Frontmatter `execution_local_index` + parent link |

## Related

- Parent: [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]]
- Prior sibling: [[Phase-2-2-Proc-World-Chunk-Graph-Staging-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2025]]
- Upstream proc stub: [[Phase-2-1-Proc-World-Execution-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2020]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- [[../../decisions-log]] (**D-Exec-1-numbering-policy**, **D-Exec-1.2-GMM-245-stub-vs-closure**)
