---
title: Phase 2.3.1 - Validation test plan and acceptance criteria scaffold
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 28
handoff_readiness: 82
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]"
  - "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

## Phase 2.3.1 - Validation test plan and acceptance criteria scaffold

First tertiary under **2.3**: explicit **test-plan** rows and **acceptance-criteria** scaffolding so execution can attach automated tests later without changing the conceptual contract.

## Scope

**In scope:**
- A **test matrix** naming validation gates, inputs, and expected outcomes at NL.
- **Acceptance criteria** rows with IDs tied to **2.3** gate taxonomy.
- Explicit **execution-deferred** markers for CI, perf, and crypto.

**Out of scope:**
- Test code, fixtures, or CI YAML.

## Behavior (natural language)

Each validation gate in **2.3** maps to one or more **test-plan rows**. Each row describes **given** bundle shape, **when** the gate runs, **then** expected pass/fail signal. **Acceptance criteria** rows are stable IDs used by operators to gate releases; automation binds in execution.

## Interfaces

Upstream:
- **2.3** secondary (gate taxonomy + pre-commit bundle).

Downward:
- Future tertiaries **2.3.2+** may split failure taxonomy, operator diagnostics, or warm-cache policy; **2.3.2** should treat **D-2.3-diagnostics-granularity** and **D-2.3-warm-cache-shortcuts** (see [[decisions-log]]) as policy anchors when decomposing tasks.

## Edge cases

- **Flaky** external signals (network, time) — not part of conceptual validation; **execution-deferred**.

## Open questions

- Whether AC IDs should embed **phase** prefix (`GMM-AC-2.3.1-*`) or stay globally unique per project.

## Pseudo-code readiness

Not required at depth 3; **interfaces + tables** are the deliverable.

## Test plan (scaffold)

| Gate id (conceptual) | Inputs (bundle elements) | Expected outcome | Notes |
| --- | --- | --- | --- |
| V-2.3-ORDER | Staged deltas + apply order from **2.1.3** | Pass iff ordering matches spine | |
| V-2.3-ENVELOPE | Hook payloads + **2.2.4** envelope | Pass iff emission envelope valid | |
| V-2.3-LABELS | Validation labels + chunk boundaries **2.2.5** | Pass iff label coverage matches chunk policy | |
| V-2.3-ROLLUP | All prior gates | Pass iff **no partial commit** on any failure | |

## Acceptance criteria (scaffold)

| AC id | Criterion | Verification method (NL) | Execution deferred |
| --- | --- | --- | --- |
| AC-2.3.1-1 | No commit when **V-2.3-ROLLUP** fails | Observe dry-run blocks commit | yes (automated test TBD) |
| AC-2.3.1-2 | Deterministic outcome for same bundle + catalog revision | Repeat dry-run; compare outcomes | yes (replay harness TBD) |
| AC-2.3.1-3 | Diagnostics reference failing **gate id** | Inspect failure payload shape | yes (UX TBD) |

## Parent

- Secondary: [[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]
