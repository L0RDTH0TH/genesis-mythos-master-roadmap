---
title: Phase 4.1.4 - Control read-model and golden-row selection contract
roadmap-level: tertiary
phase-number: 4
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 6
created: 2026-03-27
tags: [roadmap, genesis-mythos-master, phase-4, perspective, controls, t-p4-05]
para-type: Project
subphase-index: "4.1.4"
handoff_readiness: 79
handoff_readiness_scope: "Conceptual control read-model to golden-row selection contract with explicit execution-deferred replay literals"
execution_handoff_readiness: 41
handoff_gaps:
  - "**D-032 / D-043:** replay_row_version and literal golden columns remain unresolved."
  - "**Rollup closure:** REGISTRY-CI HOLD and rollup HR 92 < 93 remain execution-deferred."
links:
  - "[[phase-4-1-3-control-contracts-and-presentation-golden-placeholder-roadmap-2026-03-26-2100]]"
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[decisions-log]]"
---

## Phase 4.1.4 - Control read-model and golden-row selection contract (tertiary)

This node advances from 4.1.3 into a narrower contract: how control read models select presentation golden rows without claiming replay closure.

### Objectives

- Define a deterministic selection contract from `ControlReadModel_v0` into `GoldenPresentationRow_v0`.
- Keep all replay literals and CI closure claims explicitly execution-deferred.
- Preserve `@skipUntil(D-032)` for lane-C verification paths.

### Contract sketch

| Step | Input | Output | Constraint |
| --- | --- | --- | --- |
| Select candidate rows | `ControlReadModel_v0`, `tick_key` | `CandidateGoldenRows_v0` | No mutation path to sim/apply ledger |
| Filter by tick/version | `CandidateGoldenRows_v0`, `tick_epoch` | `SelectedGoldenRows_v0` | Drop stale rows; no carry-forward across tick mismatch |
| Emit presentation envelope | `SelectedGoldenRows_v0` | `PresentationGoldenEnvelope_v0` | Mark all unresolved literals as OPEN_STUB |

### Acceptance checklist (conceptual)

- [x] Read-only selection path is explicit (no write-back path).
- [x] Tick/version filtering behavior is described in natural language.
- [x] Execution-deferred boundaries are explicit (`D-032`, `D-043`, REGISTRY-CI hold).
- [ ] Lane-C replay-and-verify wiring remains intentionally deferred.

### Forward-only deepen note (2026-03-27)

- Trigger: `resume-roadmap-forward-only-gmm-20260327T010000Z`
- Reason: subphase slice-exit on 4.1.3 passed; moved to next structural node to avoid same-slice polish churn.
- Guardrails: no REGISTRY-CI PASS claim, no HR>=93 closure inflation, advisory execution debt remains open.
