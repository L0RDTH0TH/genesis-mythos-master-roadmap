---
title: Phase 2.3.5 - Projection ordering, rollup companion, and commit-block parity
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.5"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 89
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]"
  - "[[Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]]"
  - "[[decisions-log]]"
---

## Phase 2.3.5 - Projection ordering, rollup companion, and commit-block parity

This tertiary closes the 2.3 branch by fixing deterministic ordering rules for gate-first diagnostics while preserving rollup as a companion view, never a source of authority.

## Scope

**In scope:**
- Define deterministic projection ordering for gate failure payloads and companion rollup surfaces.
- Preserve operator-pick traceability from `D-2.3-diagnostics-granularity` and `D-2.3-warm-cache-shortcuts`.
- Lock commit-block parity rules so warm-cache and cold-path validation produce identical commit eligibility.
- Hand off a clear closure contract for the 2.3 tertiary chain.

**Out of scope:**
- UI rendering details for operator diagnostics.
- Storage engine details for payload retention and replay indexing.
- CI policy or benchmark enforcement for projection latency.

## Behavior (natural language)

Validation output for a frame must be ordered by deterministic gate keys before any rollup summary is produced. Each failing mandatory gate yields an authoritative payload record, and rollup is generated as a readable companion from those records. Commit eligibility is denied whenever any mandatory gate fails, regardless of warm-cache or cold-path origin, and trace links must show which operator pick shaped the projection contract.

## Interfaces

Upstream:
- Consumes failure payload decomposition from [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]].
- Consumes branch and parity invariants from [[Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]].

Downstream:
- `2.4+` may build commit orchestration and execution mirrors without redefining 2.3 ordering authority.
- Consumers use this slice as the closure contract for `2.3.x` validation projection consistency.

## Interface specification (conceptual contract)

- `PreCommitVerificationBundle` -> canonical input aggregate (staged deltas + hook payloads + validation labels).
- `OrderedGateFailurePayload[]` -> authoritative ordered output used for commit eligibility.
- `ValidationRollupCompanion` -> non-authoritative readable summary derived from `OrderedGateFailurePayload[]`.
- `CommitEligibilityVerdict` -> deterministic `allow_commit | deny_commit` tied to mandatory gate outcomes.

## Deterministic ordering contract

**Invariant O-2.3.5-01:**
- Sort authoritative failure payloads by stable gate key and deterministic stage order.
- Produce rollup companion only after authoritative ordering is finalized.
- Preserve identical ordering keys across warm-cache and cold-path outcomes.

**Invariant O-2.3.5-02:**
- Rollup may summarize or group records, but it cannot delete, merge away, or override any mandatory gate payload.

## Commit-block parity contract

**Invariant C-2.3.5-01:**
- Mandatory gate failure always yields `deny_commit`.
- Cache hit/miss does not alter commit eligibility.
- Operator-facing summary may differ in readability, never in outcome.

## Task decomposition

- `T-2.3.5-01`: Normalize gate payload records into stable ordering keys (owner: validation projection stage).
- `T-2.3.5-02`: Build rollup companion strictly from ordered payload records (owner: diagnostics aggregation stage).
- `T-2.3.5-03`: Compute commit verdict parity check (warm-cache vs cold-path) and emit trace result (owner: commit gate stage).
- `T-2.3.5-04`: Persist operator-pick backlinks and decision ids into validation slice trace envelope (owner: trace sink stage).

## Test-plan matrix (conceptual)

- `V-2.3.5-A`: Mandatory gate failure in cold-path -> ordered payload emitted + `deny_commit`.
- `V-2.3.5-B`: Same failing frame served via warm-cache -> identical ordered payload keys + `deny_commit`.
- `V-2.3.5-C`: Rollup generation failure with valid payloads -> commit decision still derived from authoritative payloads.
- `V-2.3.5-D`: Operator pick changes between frames -> new frame uses latest pick while prior trace remains immutable.

## Operator-pick trace closure

Required trace fields for each emitted projection bundle:
- `decision_id`
- `chosen_branch`
- `queue_entry_id`
- `projection_ordering_version`
- `commit_block_result`
- `evidence_link` (typically [[decisions-log]])

Backlink additions this slice:
- `D-2.3-diagnostics-granularity` -> [[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]
- `D-2.3-warm-cache-shortcuts` -> [[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]

## Edge cases

- Same gate fails multiple times in one frame: keep one payload per occurrence with deterministic sequence keys.
- Rollup generation fails but payload generation succeeds: commit decision still based on payload records; rollup can be retried.
- Cache-sourced frame lacks ordering metadata: treat as parity failure and revalidate through cold-path rules.

## Decision-ID closure for this slice

- `D-2.3-diagnostics-granularity`: closed at conceptual level for `2.3.5` as gate-first payload authority + rollup companion view.
- `D-2.3-warm-cache-shortcuts`: closed at conceptual level for `2.3.5` as strict parity contract (cache never bypasses payload and commit-block invariants).
- Execution-level implementation details remain deferred to `2.4+`.

## Pseudo-code readiness

At depth 3, this slice remains NL-first and execution-deferred for implementation details, but it is specific enough to draft ordering comparators, rollup assembly stages, and commit-block checks without revisiting branch authority.

## Parent

- Secondary: [[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]
- Prior tertiary: [[Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]]
