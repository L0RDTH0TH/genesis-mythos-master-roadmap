---
title: Phase 2.4.1 - Deterministic commit/deny/defer precedence and envelope lineage
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.4.1"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 38
handoff_readiness: 84
created: 2026-03-31
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]"
  - "[[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]"
  - "[[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]"
  - "[[decisions-log]]"
---

## Phase 2.4.1 - Deterministic commit/deny/defer precedence and envelope lineage

This tertiary defines deterministic branch selection for `commit`, `deny_commit`, and `defer` after validation closes in 2.3, with explicit envelope fields and parity lineage back to diagnostics authority.

## Scope

**In scope:**
- Normalize branch precedence so identical inputs always select the same branch outcome.
- Specify envelope fields that must be present for every branch output.
- Preserve lineage from 2.3 diagnostics payload authority into 2.4 commit-orchestration decisions.
- Enforce commit-block parity so warm-cache and cold-path frames cannot diverge in decision outcomes.

**Out of scope:**
- Storage schema details for commit ledgers.
- Runtime retry policy implementation and scheduler logic.
- UI wording and operator-facing presentation formats.

## Behavior (natural language)

Inputs are `OrderedGateFailurePayload[]`, `ValidationRollupCompanion`, operator-pick traces, and frame-level commit context. The orchestration layer evaluates deterministic precedence rules in fixed order: first unresolved mandatory failures, then defer conditions, then commit eligibility. Branch output is emitted as a typed `CommitDecisionEnvelope` that carries full lineage to the decisive 2.3 diagnostics artifacts.

## Deterministic precedence contract

`deny_commit` has highest precedence whenever any mandatory gate failure exists or required lineage evidence is missing.  
`defer` is selected when mandatory failures are absent but explicit deferral predicates hold (policy lock, unresolved external dependency, or bounded operator hold).  
`commit` is selected only when no mandatory failures exist, no defer predicates hold, and parity checks pass.

Decision ordering:
1. Validate required lineage evidence (`decision_id`, `queue_entry_id`, gate payload references).
2. Evaluate mandatory failure presence from authoritative payloads.
3. Evaluate defer predicates in deterministic key order.
4. Resolve final branch and emit `CommitDecisionEnvelope`.

## CommitDecisionEnvelope fields

Required fields:
- `decision_branch` (`commit | deny_commit | defer`)
- `decision_reason_code`
- `queue_entry_id`
- `decision_id`
- `frame_id`
- `projection_ordering_version`
- `commit_block_parity_result`
- `authoritative_payload_refs[]`
- `rollup_companion_ref`
- `operator_pick_trace_refs[]`
- `lineage_source_refs[]`
- `generated_at`

Field invariants:
- `authoritative_payload_refs[]` is non-empty for `deny_commit`.
- `commit_block_parity_result` must be present for all branches.
- `lineage_source_refs[]` must include at least one reference to `2.3.2` payload contracts and `2.3.5` ordering/parity contracts.

## Lineage to 2.3 diagnostics

Lineage requirements:
- `2.3.2` remains the authoritative contract for task decomposition and gate-specific failure payload fields.
- `2.3.5` remains the authoritative contract for deterministic payload ordering and rollup-companion non-authority.
- `2.4.1` must not redefine those authorities; it only consumes them to resolve branch outcomes.

## Commit-block parity lineage

Parity invariants:
- A frame that resolves to `deny_commit` on cold-path must resolve to `deny_commit` on warm-cache when authoritative payload inputs are equivalent.
- Missing lineage evidence is treated as parity failure and forces `deny_commit`.
- Defer and commit branches must carry parity evidence fields even when no failures are present.

## Acceptance criteria

- Given equivalent authoritative payload inputs, branch outcome selection is deterministic and stable across replays.
- Given mandatory failure payloads from 2.3, output branch is always `deny_commit` and includes payload lineage refs.
- Given no mandatory failures but active defer predicate, output branch is `defer` with explicit defer reason code and lineage refs.
- Given no failures and no defer predicates with parity pass, output branch is `commit` with complete envelope fields.

## Recal evidence pack (2.4.1 hardening)

This recal pass upgrades the slice from pattern-only confidence to concrete verification scaffolding that execution can test without redefining conceptual authority.

### Evidence matrix

| Scenario | Inputs (minimum) | Expected branch | Required envelope evidence |
| --- | --- | --- | --- |
| Mandatory gate failure present | `OrderedGateFailurePayload[]` contains one mandatory failure + valid lineage ids | `deny_commit` | non-empty `authoritative_payload_refs[]`, `decision_id`, `queue_entry_id`, `lineage_source_refs[]` |
| No mandatory failures, defer predicate true | valid payload refs + canonical defer predicate key | `defer` | `decision_reason_code` from defer key order, parity result, lineage refs |
| No failures, no defer, parity pass | valid payload refs + parity pass true | `commit` | full `CommitDecisionEnvelope`, ordering version, rollup companion ref |
| Missing lineage evidence | missing `decision_id` or empty lineage refs | `deny_commit` | explicit lineage-integrity `decision_reason_code`, parity result present |

### Comparator ordering fixture

Deterministic defer comparator key order for this slice:
1. `policy_lock`
2. `external_dependency_unresolved`
3. `bounded_operator_hold`

If more than one predicate is true, the first key in this order is the canonical `decision_reason_code`.

### Lineage closure checks

- Every branch output must cite at least one `2.3.2` payload-contract reference and one `2.3.5` ordering/parity reference.
- `ValidationRollupCompanion` remains companion-only context; it cannot override authoritative payload refs for branch selection.
- Warm-cache and cold-path parity is evaluated before final branch emission and recorded in `commit_block_parity_result`.

## Validator closure mapping (post-recal)

This block maps scenario evidence directly to deterministic `decision_reason_code` outcomes for validator traceability:

- `mandatory_failure_present` -> branch `deny_commit` -> reason code `deny_mandatory_gate_failure`.
- `lineage_integrity_missing` -> branch `deny_commit` -> reason code `deny_lineage_integrity_missing`.
- `defer_policy_lock` -> branch `defer` -> reason code `defer_policy_lock`.
- `defer_external_dependency_unresolved` -> branch `defer` -> reason code `defer_external_dependency_unresolved`.
- `defer_bounded_operator_hold` -> branch `defer` -> reason code `defer_bounded_operator_hold`.
- `eligible_with_parity_pass` -> branch `commit` -> reason code `commit_eligible_parity_pass`.

Closure status for this conceptual slice: evidence-backed precedence and lineage mapping are explicit; execution implementation remains deferred by track.

### Observed closure assertions (recal)

The following scenario outcomes are now treated as the canonical closure assertions for this slice:

| Scenario id | Observed branch assertion | Observed reason-code assertion | Closure |
| --- | --- | --- | --- |
| `S-2.4.1-MANDATORY-FAIL` | `deny_commit` | `deny_mandatory_gate_failure` | closed |
| `S-2.4.1-LINEAGE-MISSING` | `deny_commit` | `deny_lineage_integrity_missing` | closed |
| `S-2.4.1-DEFER-LOCK` | `defer` | `defer_policy_lock` | closed |
| `S-2.4.1-DEFER-EXT` | `defer` | `defer_external_dependency_unresolved` | closed |
| `S-2.4.1-DEFER-HOLD` | `defer` | `defer_bounded_operator_hold` | closed |
| `S-2.4.1-COMMIT-ELIGIBLE` | `commit` | `commit_eligible_parity_pass` | closed |

## Edge cases

- Missing `decision_id` with otherwise valid payloads: force `deny_commit` for lineage integrity failure.
- Concurrent defer predicates: deterministic key order resolves one canonical defer reason code.
- Rollup companion absent but authoritative payloads present: allow decisioning only when authoritative refs remain complete; otherwise force `deny_commit`.

## Open questions

- Defer expiration representation (`CommitDecisionEnvelope` field vs external policy pointer) is execution-deferred under [[decisions-log]] `D-2.4-defer-expiry-policy`; not a conceptual blocker.
- `operator_pick_trace_refs[]` payload shape (normalized snapshots vs stable IDs) is execution-deferred; conceptual contract only requires stable lineage references and deterministic branch reasons.

## Pseudo-code readiness

At depth 3, this slice remains NL-first but concrete enough for execution to draft comparator ordering, branch resolver stages, and envelope assembly without revisiting branch authority.

## Parent

- Secondary: [[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]
- Upstream diagnostics authority: [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]
- Upstream ordering/parity authority: [[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]
