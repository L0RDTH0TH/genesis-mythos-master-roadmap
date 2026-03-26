---
title: Phase 4.1.1.3 — Adapter registry promotion preflight and Lane-C fixture map
roadmap-level: task
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-24
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, task, t-p4-01]
para-type: Project
subphase-index: "4.1.1.3"
handoff_readiness: 93
handoff_readiness_scope: "Quaternary continuation for adapter registry promotion preflight; vault-normative contract only"
execution_handoff_readiness: 33
handoff_gaps:
  - "**G-P*.*-REGISTRY-CI HOLD** remains active pending 2.2.3 / D-020 execution evidence."
  - "Lane-C fixture rows remain partial until D-032 literal columns are frozen."
links:
  - "[[phase-4-1-1-2-adapter-registry-consumption-order-and-lane-c-delta-gates-roadmap-2026-03-24-0421]]"
  - "[[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]]"
  - "[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]"
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[decisions-log]]"
---

## Phase 4.1.1.3 — Adapter registry promotion preflight and Lane-C fixture map

**Parent task:** [[phase-4-1-1-2-adapter-registry-consumption-order-and-lane-c-delta-gates-roadmap-2026-03-24-0421]]

**Queue source:** `resume-deepen-post-recal-p4-1-1-1-high-util-gmm-20260324T023500Z-followup`

### TL;DR

- Add a promotion preflight checklist so adapter layout rows cannot be marked promotable without explicit gate evidence.
- Add a Lane-C fixture map that tracks which rows are still blocked by `@skipUntil(D-032)` versus ready-for-proof stubs.
- Keep roll-up honesty explicit: no REGISTRY-CI pass and no macro closure claim.

### Promotion preflight contract

```text
function PreflightPromoteAdapterLayout(layout_id, lane_c_fixture_map, gate_table):
  assert layout_id startswith "ADAPTER_ROW_LAYOUT_"
  assert gate_table["G-P4.1.1.2-LC-DELTA-01"] in ["draft", "@skipUntil(D-032)", "ready-for-proof"]
  assert lane_c_fixture_map.has_minimum_rows(3)
  assert NotClaimingRegistryCiPassWithoutEvidence()
  return "preflight-recorded"
```

### Lane-C fixture map (vault stub)

| Fixture id | Purpose | Evidence state |
| --- | --- | --- |
| F-P4.1.1.3-LC-01 | Profile reject fixture for out-of-layout projection request | `draft` |
| F-P4.1.1.3-LC-02 | Replay row version mismatch fixture for stale adapter rows | `@skipUntil(D-032)` |
| F-P4.1.1.3-LC-03 | Deterministic consume-order fixture for canonical `normative_columns` ordering | `draft` |

### Acceptance criteria

1. A promotion preflight pseudo-flow exists and binds gate checks before any promotion language.
2. Lane-C fixture map includes at least one blocked (`@skipUntil(D-032)`) and one draft row.
3. This note does not claim `REGISTRY-CI PASS` or phase rollup closure.

### Non-goals

- This note does not clear `missing_roll_up_gates`.
- This note does not mutate operator choices for D-044 or D-059.
