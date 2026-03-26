---
title: Phase 4.1.1.2 — Adapter registry consumption order and Lane-C delta gates
roadmap-level: task
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-24
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, task, t-p4-01]
para-type: Project
subphase-index: "4.1.1.2"
handoff_readiness: 93
handoff_readiness_scope: "Quaternary follow-on for adapter registry consumption order and Lane-C delta gate stubs; vault-normative only"
execution_handoff_readiness: 32
handoff_gaps:
  - "**G-P*.*-REGISTRY-CI HOLD** unchanged pending execution evidence from 2.2.3 / D-020."
  - "Lane-C delta gate rows remain `@skipUntil(D-032)` until literal replay columns freeze."
links:
  - "[[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]]"
  - "[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]"
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[decisions-log]]"
---

## Phase 4.1.1.2 — Adapter registry consumption order and Lane-C delta gates

**Parent task:** [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]]

**Queue source:** `resume-deepen-p4-1-1-1-post-handoff-hygiene-gmm-20260324T042100Z`

### TL;DR

- Add a deterministic consumption order contract for `adapter_row_layout_id` lookups before projection.
- Extend Lane-C delta gate placeholders so downstream replay checks can be promoted without changing registry semantics.
- Keep all claims vault-honest: no REGISTRY-CI PASS and no implied rollup closure.

### Deterministic consumption order (stub)

```text
function ResolveAdapterLayoutForProjection(snapshot, layout_registry):
  id = snapshot.adapter_row_layout_id
  assert id in layout_registry
  layout = layout_registry[id]
  assert IsCanonicalOrder(layout.normative_columns)
  return layout
```

### Lane-C delta gate scaffold

| Gate id | Intent | Status |
| --- | --- | --- |
| G-P4.1.1.2-LC-DELTA-01 | Verify removed `@skipUntil(D-032)` columns have mapped delta proof row ids | `@skipUntil(D-032)` |
| G-P4.1.1.2-LC-DELTA-02 | Verify TickCommitRecord delta fields remain aligned to consumed layout id | `@skipUntil(D-032)` |
| G-P4.1.1.2-LC-DELTA-03 | Verify profile allow-list rejects out-of-layout lane projections | `draft` |

### Acceptance criteria

1. A deterministic consume-order pseudo-flow exists and references `adapter_row_layout_id` before projection.
2. Lane-C delta gate table includes explicit blocked states where literals are not yet frozen.
3. This note does not claim `REGISTRY-CI PASS` or phase rollup closure.

### Non-goals

- This note does not clear `missing_roll_up_gates`.
- This note does not supersede operator picks for D-044 or D-059.
