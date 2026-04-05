---
title: Phase 2.4.3 - Commit decision envelope assembly and lineage attestation
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.4.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 86
created: 2026-03-31
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]"
  - "[[Phase-2-4-2-Scenario-Id-to-Decision-Reason-Code-Lineage-Parity-Roadmap-2026-03-31-0315]]"
  - "[[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]"
  - "[[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]"
  - "[[decisions-log]]"
---

## Phase 2.4.3 - Commit decision envelope assembly and lineage attestation

This tertiary defines the deterministic assembly contract for `CommitDecisionEnvelope` so every `2.4.2` scenario/reason outcome emits one canonical envelope with auditable lineage parity to `2.3.2` payload authority and `2.3.5` ordering authority.

## Scope

**In scope:**
- Canonical envelope schema segments and deterministic field population order.
- Mandatory lineage attestation fields proving scenario -> reason-code continuity from `2.4.2`.
- Deterministic normalization rules for commit, deny, and defer envelope variants.
- Trace ledger attachment requirements for validator and recal compare passes.

**Out of scope:**
- Runtime serializer implementations and binary transport details.
- Storage partitioning and retention policy internals.
- UI rendering models for operator-facing envelope explainability.

## Behavior (natural language)

Inputs are `2.4.2` scenario/reason outputs, branch result, authoritative payload lineage refs, ordering version, and parity assertions.

Assembly order:
1. Create canonical envelope skeleton with immutable identity fields (`envelope_id`, frame, branch, scenario, reason code).
2. Attach mandatory lineage refs from `2.3.2` payload authority and `2.3.5` ordering/parity authority.
3. Populate branch-specific segment (`commit`, `deny_commit`, or `defer`) using deterministic field-order rules.
4. Emit attestation block confirming warm-cache/cold-path parity and trace ledger linkage.

## Envelope assembly contract

| Segment | Required fields | Deterministic rule |
| --- | --- | --- |
| Identity | `envelope_id`, `frame_id`, `branch`, `scenario_id`, `decision_reason_code` | Field order fixed; no branch-specific reordering allowed |
| Lineage refs | `payload_authority_ref`, `ordering_authority_ref`, `parity_assertion_ref` | Missing refs force `deny_commit` normalization path |
| Branch body | `commit_payload` OR `deny_payload` OR `defer_payload` | Exactly one branch body; mutually exclusive |
| Trace | `trace_id`, `source_chain`, `attestation_digest` | Digest covers identity + lineage + branch body |

## Lineage attestation and parity rules

- `scenario_id` and `decision_reason_code` must be copied from the canonical `2.4.2` mapping output without reinterpretation.
- Envelope is invalid if any required lineage ref from `2.3.2` or `2.3.5` is absent, stale, or mismatched.
- Warm-cache and cold-path runs must produce byte-equivalent logical envelopes for the same authoritative inputs.
- Any attestation mismatch normalizes to `deny_commit` with lineage-integrity failure tagging.

## Interfaces

Upstream:
- Consumes scenario/reason lineage mapping from **2.4.2**.
- Consumes payload authority from **2.3.2** and ordering/parity authority from **2.3.5**.

Downstream:
- Provides canonical decision envelope contract for `2.4.4+` branch-finalization and execution handoff slices.
- Provides deterministic attestation rows for hostile validator compare passes.

## Acceptance criteria

- Given one canonical scenario/reason output from `2.4.2`, envelope assembly emits exactly one canonical envelope shape with one branch body.
- Given equivalent authoritative inputs, warm-cache and cold-path envelope outputs are parity-equivalent.
- Given any missing lineage authority ref, output normalizes to `deny_commit` with lineage-integrity failure tagging.
- Given branch-specific payload fields, identity + lineage segments remain invariant and ordered.

## Edge cases

- Duplicate `envelope_id` for same frame with divergent branch body: reject and classify as integrity failure.
- Scenario/reason mismatch against `2.4.2` table revision: force deny and log attestation mismatch.
- Mixed branch payload remnants after retries: normalize to single branch body and invalidate conflicting residue.

## Open questions

- Whether attestation digest should be signed at envelope mint time or only at commit boundary remains execution-deferred.
- Whether defer envelopes should include optional expiry metadata or rely solely on policy lock references remains execution-deferred.

## Pseudo-code readiness

This slice is NL-first at depth 3 but defines enough deterministic assembly and attestation rules for execution to draft schema validators and table-driven envelope builders without redefining conceptual branch authority.

## Parent

- Secondary: [[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]
- Prior tertiary authority: [[Phase-2-4-2-Scenario-Id-to-Decision-Reason-Code-Lineage-Parity-Roadmap-2026-03-31-0315]]
