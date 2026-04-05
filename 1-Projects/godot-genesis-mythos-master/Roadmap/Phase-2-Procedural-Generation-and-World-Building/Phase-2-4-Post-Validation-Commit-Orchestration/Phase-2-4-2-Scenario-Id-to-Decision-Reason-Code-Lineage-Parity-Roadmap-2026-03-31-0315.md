---
title: Phase 2.4.2 - Scenario ID to decision_reason_code lineage parity
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.4.2"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 41
handoff_readiness: 85
created: 2026-03-31
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]"
  - "[[Phase-2-4-1-Deterministic-Commit-Deny-Defer-Precedence-and-Envelope-Lineage-Roadmap-2026-03-31-0240]]"
  - "[[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]"
  - "[[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]"
  - "[[decisions-log]]"
---

## Phase 2.4.2 - Scenario ID to decision_reason_code lineage parity

This tertiary locks scenario-level closure mapping so every canonical `S-2.4.1-*` scenario resolves to one stable `decision_reason_code` lineage path, with deterministic parity across replay, warm-cache, and cold-path commits.

## Scope

**In scope:**
- Canonical mapping contract from scenario IDs to branch + `decision_reason_code`.
- Lineage parity rules tying each scenario outcome to `2.3.2` payload authority and `2.3.5` ordering/parity authority.
- Deterministic tie-break and normalization behavior when multiple scenario predicates are true.
- Traceability artifacts needed for validator/post-recal closure checks.

**Out of scope:**
- Runtime code structures, enum generation, and storage schemas.
- CI registry/rollup closure implementation details.
- Operator UI copy for scenario explainability panes.

## Behavior (natural language)

Inputs are canonical scenario IDs, authoritative payload refs, ordering version, parity result, and branch context produced by `2.4.1`. Resolver behavior is strict:
1. Normalize scenario ID and load canonical mapping table revision.
2. Verify required lineage refs (`2.3.2` payload + `2.3.5` ordering/parity) are present.
3. Resolve branch + `decision_reason_code` from deterministic table order.
4. Emit lineage parity assertion entry in the decision envelope and trace ledger.

## Canonical scenario -> reason-code mapping

| Scenario id | Branch | decision_reason_code | Required lineage refs |
| --- | --- | --- | --- |
| `S-2.4.1-MANDATORY-FAIL` | `deny_commit` | `deny_mandatory_gate_failure` | `2.3.2` mandatory payload refs + gate failure node |
| `S-2.4.1-LINEAGE-MISSING` | `deny_commit` | `deny_lineage_integrity_missing` | lineage-integrity validation record + parity check |
| `S-2.4.1-DEFER-LOCK` | `defer` | `defer_policy_lock` | policy lock predicate + deterministic comparator index |
| `S-2.4.1-DEFER-EXT` | `defer` | `defer_external_dependency_unresolved` | unresolved dependency evidence + comparator index |
| `S-2.4.1-DEFER-HOLD` | `defer` | `defer_bounded_operator_hold` | bounded hold token + comparator index |
| `S-2.4.1-COMMIT-ELIGIBLE` | `commit` | `commit_eligible_parity_pass` | parity pass record + ordering version + authority refs |

## Deterministic parity and tie-break contract

- Scenario IDs are case-sensitive canonical tokens; unknown IDs resolve to `deny_commit` with `deny_lineage_integrity_missing`.
- When multiple defer predicates are true, comparator order from `2.4.1` is authoritative: `policy_lock` -> `external_dependency_unresolved` -> `bounded_operator_hold`.
- Warm-cache and cold-path resolution must produce identical scenario -> reason-code outputs for equivalent authoritative inputs.
- Missing `2.3.2` or `2.3.5` refs invalidates parity and forces `deny_commit`.

## Interfaces

Upstream:
- Consumes precedence and envelope contract from **2.4.1**.
- Consumes payload authority from **2.3.2** and ordering/parity authority from **2.3.5**.

Downstream:
- Provides stable scenario-to-reason-code lineage assertions for `2.4.3+` commit-orchestration refinements.
- Provides deterministic evidence rows for validator compare passes and recal audits.

## Acceptance criteria

- Given any canonical `S-2.4.1-*` scenario ID, resolver emits exactly one branch + `decision_reason_code` pair from this table.
- Given equivalent authoritative inputs, warm-cache and cold-path runs produce identical mapping outputs.
- Given missing lineage refs, output is forced to `deny_commit` + `deny_lineage_integrity_missing`.
- Given concurrent defer predicates, output reason code follows comparator order from `2.4.1`.

## Edge cases

- Unknown scenario token: normalize failure path to lineage-integrity deny and log unmapped token.
- Comparator-order drift between table revisions: reject commit and require recalibration before branch resolution.
- Partial lineage refs present: treat as integrity failure; no best-effort commit/defer fallback allowed.

## Open questions

- Whether scenario mapping revision ids should be envelope fields or external policy references is execution-deferred.
- Whether cross-project scenario token namespaces should be globally reserved is execution-deferred.

## Pseudo-code readiness

This slice is NL-first at depth 3 but deterministic enough for execution to draft resolver pseudo-code and table-driven parity checks without redefining conceptual branch authority.

## Parent

- Secondary: [[Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236]]
- Prior tertiary authority: [[Phase-2-4-1-Deterministic-Commit-Deny-Defer-Precedence-and-Envelope-Lineage-Roadmap-2026-03-31-0240]]
