---
title: Phase 2.3.2 - Verification task decomposition and failure payload contracts
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 35
handoff_readiness: 84
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]"
  - "[[Phase-2-3-1-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-03-30-2140]]"
  - "[[decisions-log]]"
---

## Phase 2.3.2 - Verification task decomposition and failure payload contracts

This tertiary turns the 2.3 validation slice into explicit execution-ready work units while staying conceptual-track safe: no CI wiring, no code, but concrete owner/input/output/done contracts and deterministic failure-payload expectations.

## Scope

**In scope:**
- Decompose Phase 2.3 validation flow into named tasks with ownership boundaries.
- Bind each task to deterministic inputs and outputs from 2.1 / 2.2 artifacts.
- Map `V-2.3-*` rows to explicit failure-payload contracts.
- Tighten acceptance-criteria scaffold rows from placeholder form to actionable NL.

**Out of scope:**
- Runtime implementation classes, benchmark thresholds, or CI scripts.
- Final policy picks for warm-cache optimization and diagnostics UX (tracked decisions remain execution-deferred).

## Behavior (natural language)

Validation proceeds as a staged task chain where each task emits a typed contract artifact consumed by the next task. A failure at any task emits a deterministic payload envelope and blocks commit rollup. Tasks are written so execution can implement directly without re-litigating intent.

## Interfaces

Upstream:
- `StagedDeltaBundle` composition and ordering semantics from `2.1.3`.
- Envelope and pre-commit handoff contracts from `2.2.4`.
- Label/chunk boundary semantics from `2.2.5`.

Downstream:
- `2.3.3+` can refine diagnostics rendering, warm-cache policy, and deferred execution details using these task contracts as authority.

## Task decomposition (explicit)

| Task id | Owner | Inputs | Outputs | Done signal |
| --- | --- | --- | --- | --- |
| T-2.3.2-1 VerificationBundleAssembler | Validation spine maintainer | `StagedDeltaBundle`, hook envelopes, label coverage map, bundle metadata | `PreCommitVerificationBundle` with stable schema version and source revision refs | Bundle serialization shape is stable and references all required upstream revisions; no missing mandatory sections |
| T-2.3.2-2 GateExecutionOrchestrator | Validation gate orchestrator | Verification bundle + gate ordering contract (`V-2.3-ORDER`) | Ordered gate result stream with deterministic gate ids and statuses | Re-running same bundle yields same gate order and same gate status tuple set |
| T-2.3.2-3 FailurePayloadEmitter | Failure taxonomy owner | Gate result stream + failing gate context + correlation ids | `ValidationFailurePayload` envelope per failing gate and one rollup payload | Every failing gate emits a payload with required fields; rollup payload exists when any mandatory gate fails |
| T-2.3.2-4 CommitEligibilityResolver | Commit loop boundary owner | Gate result stream + failure rollup payload | Commit eligibility verdict (`allow_commit`/`deny_commit`) + justification reference | Any mandatory gate failure sets `deny_commit`; success path emits `allow_commit` with empty failure reference list |
| T-2.3.2-5 DiagnosticsProjectionContract | Operator diagnostics owner | Failure payload(s), gate metadata, correlation refs | Operator-facing diagnostics projection schema (per-gate + rollup placeholders) | Projection contains stable pointers to gate ids and supports both `D-2.3-diagnostics-granularity` options without schema break |

## V-2.3 gate rows -> failure payload expectations

| Gate row | Failure payload expectations |
| --- | --- |
| `V-2.3-ORDER` | Must include `failed_gate_id`, `expected_stage_order`, `actual_stage_order`, `first_order_violation`, `bundle_revision_ref`, `correlation_id` |
| `V-2.3-ENVELOPE` | Must include `failed_gate_id`, `envelope_contract_ref`, `missing_or_invalid_fields[]`, `schema_catalog_revision`, `payload_outline_ref`, `correlation_id` |
| `V-2.3-LABELS` | Must include `failed_gate_id`, `label_policy_revision`, `missing_labels[]`, `chunk_boundary_ref`, `coverage_ratio`, `correlation_id` |
| `V-2.3-ROLLUP` | Must include `failed_gate_id`, `failed_gate_refs[]`, `commit_blocked: true`, `rollup_reason_code`, `operator_message_key`, `correlation_id` |

## Tightened acceptance criteria (replaces scaffold looseness)

| AC id | Criterion (tightened) | Verification method (NL) | Execution deferred |
| --- | --- | --- | --- |
| AC-2.3.2-1 | Every failed mandatory gate emits a deterministic failure payload with the gate-specific required fields listed above | Replay the same failing bundle twice; compare field presence and semantic equality per payload type | yes (automation harness TBD) |
| AC-2.3.2-2 | Commit eligibility is blocked whenever any mandatory gate fails and references rollup payload id | Trace `V-2.3-*` failures to resolver output; confirm `deny_commit` and payload linkage | yes (runtime enforcement wiring TBD) |
| AC-2.3.2-3 | Diagnostics projection supports both per-gate and rollup summary views without changing upstream payload schema | Validate projection contract against both decision branches: `D-2.3-diagnostics-granularity` unresolved options A/B | yes (UX contract binding TBD) |
| AC-2.3.2-4 | Warm-cache shortcut path cannot bypass mandatory failure payload emission or commit-block semantics | Compare warm-cache vs cold-path conceptual flow; mandatory payload fields and `deny_commit` behavior remain identical | yes (perf strategy binding TBD; `D-2.3-warm-cache-shortcuts`) |

## Edge cases

- Mixed pass/fail bundles across chunk boundaries must still produce one rollup payload with full failed gate refs.
- Unknown label revisions in a warm-cache frame must degrade to strict validation path and emit `V-2.3-LABELS` payload when coverage contracts break.
- Diagnostics projection must preserve machine-stable keys even when human message text changes.

## Open questions

- `D-2.3-diagnostics-granularity`: final operator default between per-gate and rollup-first display remains execution-deferred.
- `D-2.3-warm-cache-shortcuts`: policy may optimize repeated frames but cannot violate payload and commit-block invariants above.

## Pseudo-code readiness

At depth 3, pseudo-code is optional; interfaces and task contracts are sufficiently concrete for execution to draft implementation without redefining responsibilities or payload fields.

## Parent

- Secondary: [[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]]
- Prior tertiary: [[Phase-2-3-1-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-03-30-2140]]
