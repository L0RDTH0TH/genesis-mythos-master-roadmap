---
title: Phase 2.3.3 - Projection contract branch, warm-cache guardrails, and operator-pick traceability
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.3"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 38
handoff_readiness: 85
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]"
  - "[[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]"
  - "[[decisions-log]]"
---

## Phase 2.3.3 - Projection contract branch, warm-cache guardrails, and operator-pick traceability

This tertiary resolves the Phase 2.3 advisory carry-over by binding the unresolved diagnostics and warm-cache decisions to one concrete projection-contract branch while preserving conceptual-track boundaries.

## Scope

**In scope:**
- Bind `D-2.3-diagnostics-granularity` to one projection-contract branch that still preserves deferred option space.
- Add a non-bypass warm-cache invariant: shortcut paths cannot skip mandatory failure payload emission or `deny_commit`.
- Define operator-pick trace lines that backlink to the roadmap slices consuming each decision.
- Specify where the trace lines are recorded and how consuming notes reference them.

**Out of scope:**
- Runtime implementation details for cache residency, payload serializers, or commit-loop classes.
- UX copy and final operator dashboard rendering details.

## Behavior (natural language)

The validation projection contract now follows a single authority branch: **gate-first projection with rollup companion**. Each failing mandatory gate still emits a gate-level payload; rollup exists as companion summary, not replacement. Warm-cache paths are contractually equivalent to cold validation for mandatory gates, meaning they can optimize repeated computation but cannot remove payload emission requirements or alter commit-block outcomes.

## Interfaces

Upstream:
- Receives task decomposition and payload schema guarantees from [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]].
- Consumes label/chunk boundary semantics from the `2.2.5` validation envelope branch.

Downstream:
- `2.3.4+` can specialize diagnostics rendering and execution mechanics without changing branch authority.
- Decision trace lines in [[decisions-log]] are consumed as canonical backlinks from this and later 2.3 slices.

## Projection-contract branch binding

### Bound branch

`D-2.3-diagnostics-granularity` is bound to:
- **Primary contract:** per-gate payloads are mandatory and authoritative for machine workflows.
- **Companion contract:** rollup summary is mandatory whenever any mandatory gate fails.

This keeps both machine determinism and operator summarization without schema split.

### Compatibility note

If future execution chooses "rollup-first display" as UI default, it still references preserved per-gate payload ids; the schema and commit logic do not bifurcate.

## Warm-cache guardrail invariant

**Invariant W-2.3.3-01:**

For any frame evaluated via warm-cache path:
- mandatory gate failures **must** emit the same required failure payload fields as cold-path evaluation, and
- commit eligibility **must** resolve to `deny_commit` whenever any mandatory gate fails.

Warm-cache may reduce repeated computation, but it cannot bypass:
- `ValidationFailurePayload` emission contracts, or
- mandatory commit-block semantics.

## Operator-pick trace lines (decision -> consumer backlinks)

For each `D-*` decision used by validation flow, record an operator-pick trace line under the matching decision entry in [[decisions-log]] with:
- decision id,
- chosen branch text,
- queue entry id,
- consuming roadmap backlinks.

### Required consuming backlinks for this run

- `D-2.3-diagnostics-granularity` -> [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]], [[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]]
- `D-2.3-warm-cache-shortcuts` -> [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]], [[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]]

## Edge cases

- Warm-cache hit with stale label revision: must fall back to strict validation and still emit payload fields listed for `V-2.3-LABELS`.
- Multiple mandatory gate failures in one frame: per-gate payloads remain one-per-gate and rollup aggregates all failed gate refs.
- Operator-facing rollup message changes: machine keys and payload ids remain stable.

## Open questions

- Whether warm-cache policy requires additional freshness proofs beyond revision identity checks remains execution-deferred.
- Whether diagnostics default view should prioritize grouped gate families or strict gate order remains presentation-deferred.

## Pseudo-code readiness

At depth 3, pseudo-code is optional. Interface and invariant wording is concrete enough for execution to draft branch logic, cache path checks, and trace-line plumbing without changing decision authority.

## Parent

- Secondary: [[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]
- Prior tertiary: [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]
