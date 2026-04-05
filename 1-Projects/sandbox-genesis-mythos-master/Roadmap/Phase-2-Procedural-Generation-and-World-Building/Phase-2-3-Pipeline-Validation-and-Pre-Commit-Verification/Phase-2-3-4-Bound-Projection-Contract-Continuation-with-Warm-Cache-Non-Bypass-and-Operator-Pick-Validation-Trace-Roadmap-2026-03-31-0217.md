---
title: Phase 2.3.4 - Bound projection-contract continuation with warm-cache non-bypass and operator-pick validation trace
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.4"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 86
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]"
  - "[[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]]"
  - "[[decisions-log]]"
---

## Phase 2.3.4 - Bound projection-contract continuation with warm-cache non-bypass and operator-pick validation trace

This tertiary continues the 2.3.3 branch decision by turning branch-level invariants into explicit validation-slice contracts that downstream 2.3 notes can consume without ambiguity.

## Scope

**In scope:**
- Carry forward the bound diagnostics branch (`gate-first payload + rollup companion`) as a fixed validation contract.
- Extend warm-cache non-bypass from branch intent to slice-level verification obligations.
- Define operator-pick validation trace payloads so every consuming 2.3 slice can prove which pick was applied and why.
- Keep execution-only implementation details deferred while preserving deterministic conceptual authority.

**Out of scope:**
- Runtime cache storage, TTL, eviction, or serializer implementation.
- CI wiring, benchmark thresholds, or concrete class/module layouts.

## Behavior (natural language)

For each validation frame, the slice must first evaluate mandatory gates and emit per-gate payloads whenever they fail. A rollup summary may be generated for operator readability, but it cannot replace gate payload authority. If warm-cache is used, cache hits are only accepted when all required payload fields can still be produced and the same commit-block result (`deny_commit` on mandatory failure) is preserved.

## Interfaces

Upstream:
- Consumes decomposition and payload obligations from [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]].
- Inherits branch/invariant choices from [[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]].

Downstream:
- `2.3.5+` may add projection ordering refinements and execution handoff details without changing branch authority.
- Consumers must backlink to operator-pick evidence in [[decisions-log]].

## Warm-cache non-bypass continuation

**Invariant W-2.3.4-01:**
- Warm-cache path must emit payload-equivalent mandatory-failure records.
- Warm-cache path must preserve gate failure ordering keys used by projection and rollup.
- Warm-cache path must preserve commit eligibility parity with cold-path validation.

Any cache optimization that cannot satisfy all three conditions is invalid for this slice.

## Operator-pick validation trace contract

Each consuming 2.3 slice must write a trace record containing:
- `decision_id` (for example `D-2.3-diagnostics-granularity`),
- `chosen_branch`,
- `queue_entry_id`,
- `consumer_slice_id`,
- `validation_slice_id`,
- `evidence_link` (typically [[decisions-log]]).

Minimum backlinks for this run:
- `D-2.3-diagnostics-granularity` -> [[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]], [[Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]]
- `D-2.3-warm-cache-shortcuts` -> [[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]], [[Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]]

## Edge cases

- Warm-cache hit with payload schema revision mismatch: treat as cold validation and emit full mandatory payload fields.
- Multiple mandatory failures with one cached frame: keep one payload per failing gate and one deterministic rollup summary.
- Operator-pick updated between frames: use latest logged pick for new frame while preserving previous-frame trace records.

## Open questions

- Whether operator-pick traces should be compacted by slice batch or remain per-frame is execution-deferred.
- Whether warm-cache parity checks require additional version-hash fields in trace payloads is execution-deferred.

## Pseudo-code readiness

At depth 3, this slice remains NL-first but is specific enough for execution to draft validation-trace structures and parity checks without redefining branch authority.

## Parent

- Secondary: [[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]
- Prior tertiary: [[Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]]
