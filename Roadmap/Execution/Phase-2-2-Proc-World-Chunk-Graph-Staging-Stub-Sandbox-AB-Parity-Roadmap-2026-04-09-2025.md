---
title: Phase 2.2 (Execution) — Chunk / graph staging stub (sandbox A/B parity)
created: 2026-04-09
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2-2
  - godot
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 86
parent_slice: Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016
execution_local_index: "2.2"
conceptual_counterpart: "[[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2.2 (Execution) — Chunk / graph staging stub (A/B vs sandbox reference)

**Execution-local slice `2.2`** under [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]], sibling to [[Phase-2-1-Proc-World-Execution-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2020]], per [[../decisions-log]] **D-Exec-1-numbering-policy**. This note defines **vault-only** staging contracts for **proc graph outputs → chunk / region graphs → observable world deltas** on **lane A (Godot)** with explicit **lane B (sandbox)** comparand rows. **No** registry CI, compare-table closure, or **`GMM-2.4.5-*`** “done” claims until **scripts/CI** exist (**D-Exec-1.2-GMM-245-stub-vs-closure**).

## Scope

- **In scope:** Name **staging** surfaces that sit **between** **2.1** proc/world inventory and downstream presentation/readout — **chunk keys**, **region graph handles**, **staging buffers** for deterministic replay, and **cross-chunk seam** identifiers that can ride the same envelope families as **1.3**/**1.4**.
- **Out of scope:** Shipping streaming loaders, **GMM-2.4.5-*** compare/rollup/retention closure, production **registry JSONL** writers — **execution-deferred** per parent spine and [[../distilled-core]].

## Chunk / staging surface inventory (adapter layer)

| Surface | Role in spine | Godot hook (lane A) | Sandbox reference hint (lane B) |
| --- | --- | --- | --- |
| **Chunk identity key** | Stable id for proc/world correlation across ticks | `Vector3i` / region id + **chunk_coord** tuple; emitted on envelope rows as `chunk_key` | Same tuple schema; if B lacks 3D grid, document **2D projection** + `parity_gap` |
| **Region graph handle** | Named subgraph for proc experiments | `Resource` id or `RID`-like string stub in envelope (`region_graph_id`) | Symmetric **region_graph_id** string table; extra fields flagged `parity_gap` when B has no RID |
| **Staging buffer contract** | Where partial proc outputs land before world commit | In-memory **staging dict** with **schema_version** + **commit_epoch** counter | Same **commit_epoch** monotonic rule; B may use pure map stub |
| **Cross-chunk seam** | Boundary rules for adjacent chunk deltas | Explicit **seam_id** + neighbor **chunk_key** pair in delta rows | Same seam row shape; missing neighbor → `parity_gap: true` |
| **Observation / readout bridge** | Staging rows visible before Presentation | Reuse **2.1** `proc_graph_emit` / `world_delta_emit` kinds; add **`staging_preview`** kind optional | B emits **`staging_preview`** or marks **`unsupported`** + gap |

## A/B parity contract (operator-visible)

1. **Same envelope schema family:** Staging rows stay inside **InstrumentationIntentEnvelope** vocabulary; lane metadata (`queue_lane: godot` \| `sandbox`) required; **`GMM-2.4.5-*`** closure remains **execution-deferred**.
2. **Divergence logging:** Godot-only **RID** / **SubViewport** behaviors that B cannot mirror → **`parity_gap: true`** stub rows — **not** silent drop.
3. **Non-closure row:** Do **not** claim **SCHEMA / RETENTION / VALIDATOR-COMPARE-TABLE** for **`GMM-2.4.5-*`** until **scripts/CI** exist.

## NL checklist (2.2 mint)

- [x] Enumerate **≥5** distinct **staging / chunk** loci tied to **Phase 2** spine (table above).
- [x] State **A/B parity** rules: shared schema family, explicit gap flags — **no** **`GMM-2.4.5-*`** closure.
- [x] Link parent spine + **2.1** continuity without rewriting conceptual **Phase 2** body.

## Acceptance hooks (post–IRA evidence)

- **H1:** **Chunk_key** + **region_graph_id** appear as **named fields** on staging rows before **2.x** expansion continues — evidence stub: `{ "kind": "staging_preview", "chunk_key": [0,1,-2], "region_graph_id": "rg_proc_01", "commit_epoch": 17 }`.
- **H2:** **Seam** rows include **neighbor chunk_key** pair or declare `parity_gap` when B cannot represent seams — stub `{ "kind": "seam", "parity_gap": true, "feature": "seam_neighbor_missing" }` when applicable.
- **H3:** **Staging** kinds are enumerated and aligned to **1.4** readout kinds where applicable — initial names: `staging_preview`, `seam`, `region_graph_emit`.

## GWT-2-2-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-2-Exec-A | Chunk/staging surfaces are named and mapped to **2.1** + instrumentation continuity | § Chunk / staging surface inventory |
| GWT-2-2-Exec-B | Sandbox lane is referenced as **comparand**, not authority over conceptual Phase 2 | § Scope + A/B parity contract |
| GWT-2-2-Exec-C | Slice is discoverable as **`2.2`** under execution-local policy | Frontmatter `execution_local_index` + parent link |

## Related

- Parent: [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]]
- Next sibling: [[Phase-2-3-Proc-World-Staging-Commit-Integration-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2030]]
- Prior sibling: [[Phase-2-1-Proc-World-Execution-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-2020]]
- Prior instrumentation chain: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- [[../decisions-log]] (**D-Exec-1-numbering-policy**, **D-Exec-1.2-GMM-245-stub-vs-closure**)
