---
title: Phase 2.4.4 - Deny-commit reason attestation and escalation boundary
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.4.4"
project-id: genesis-mythos-master
status: active
priority: high
progress: 43
handoff_readiness: 87
created: 2026-03-31
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]"
  - "[[Phase-2-4-3-Commit-Decision-Envelope-Assembly-and-Lineage-Attestation-Roadmap-2026-03-31-0325]]"
  - "[[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]"
  - "[[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]"
  - "[[decisions-log]]"
---

## Phase 2.4.4 - Deny-commit reason attestation and escalation boundary

This tertiary defines the canonical deny-commit attestation boundary so every deny path emitted by `2.4.3` has one stable reason lineage, one deterministic escalation class, and one operator-visible recovery contract.

## Scope

**In scope:**
- Deterministic deny-reason attestation fields and ordering within `CommitDecisionEnvelope`.
- One-way mapping from deny `decision_reason_code` to escalation class and recovery path.
- Guardrails that prevent mixed defer/deny semantics in the same envelope revision.
- Trace contract for hostile validation and recal compare passes.

**Out of scope:**
- UI notification rendering, inbox routing, and message templates.
- Runtime retry scheduler implementation details.
- External incident/ticket integrations.

## Behavior (natural language)

Inputs are finalized deny branch outcomes from `2.4.3`, canonical scenario/reason lineage from `2.4.2`, payload authority refs (`2.3.2`), and ordering authority refs (`2.3.5`).

Attestation flow:
1. Validate that branch is `deny_commit` and lineage refs are complete.
2. Bind one canonical deny `decision_reason_code` to one escalation class.
3. Attach deterministic recovery metadata (`next_operator_action`, `recal_required`, `retry_policy_tag`).
4. Emit immutable deny attestation block and trace row for validator/recal comparators.

## Deny reason -> escalation class contract

| decision_reason_code | Escalation class | Required recovery contract |
| --- | --- | --- |
| `deny_mandatory_gate_failure` | `hard_block` | No auto-retry; operator remediation required |
| `deny_lineage_integrity_missing` | `integrity_block` | Recal + lineage repair before any retry |
| `deny_payload_contract_mismatch` | `contract_block` | Payload/schema repair then replay |
| `deny_policy_violation` | `policy_block` | Explicit policy override or design amendment |

## Attestation and escalation invariants

- A deny envelope must contain exactly one deny reason code and exactly one escalation class.
- Escalation class is derived only from canonical reason-code mapping; no heuristic overrides.
- Missing lineage authority refs force `integrity_block` regardless of the incoming reason label.
- Warm-cache and cold-path deny outcomes must produce parity-equivalent attestation blocks for identical authorities.

## Interfaces

Upstream:
- Consumes canonical envelope assembly and lineage attestation from **2.4.3**.
- Consumes scenario/reason-code authority from **2.4.2**.

Downstream:
- Provides deterministic deny escalation boundary for `2.4.5` closure and handoff slices.
- Supplies hostile validator compare artifacts for deny-path integrity checks.

## Acceptance criteria

- Given any deny outcome from `2.4.3`, resolver emits one deterministic escalation class with one recovery contract.
- Given missing lineage refs, escalation class is always `integrity_block` and `recal_required: true`.
- Given equivalent authoritative inputs, deny attestation output is parity-stable across warm-cache and cold-path paths.
- Given mixed branch residue, deny attestation rejects the envelope instead of silently coercing defer semantics.

## Edge cases

- Multiple deny reasons present in one envelope: reject as invalid and require rebuild.
- Unknown deny reason code: normalize to `integrity_block` and log unmapped code.
- Policy override requested on integrity failure: denied until lineage repair pass succeeds.

## Open questions

- Whether escalation classes should be globally standardized across projects remains execution-deferred.
- Whether deny recovery contracts should include bounded operator SLA fields remains execution-deferred.

## Pseudo-code readiness

This slice is NL-first at depth 3 but deterministic enough for execution to implement deny-reason attestation tables, escalation dispatch guards, and parity assertions without redefining conceptual branch authority.

## Parent

- Secondary: [[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]
- Prior tertiary authority: [[Phase-2-4-3-Commit-Decision-Envelope-Assembly-and-Lineage-Attestation-Roadmap-2026-03-31-0325]]
