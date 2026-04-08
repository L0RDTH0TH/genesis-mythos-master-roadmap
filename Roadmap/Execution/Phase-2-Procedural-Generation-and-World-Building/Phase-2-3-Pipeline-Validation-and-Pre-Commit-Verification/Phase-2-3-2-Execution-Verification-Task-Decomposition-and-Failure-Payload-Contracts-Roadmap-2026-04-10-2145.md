---
title: Phase 2.3.2 — Execution verification task decomposition and failure payload contracts (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.2"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
priority: high
progress: 40
handoff_readiness: 85
handoff_gaps:
  - "Tertiary **2.3.4+** not yet minted; `rollup_2_primary_from_2_3` remains OPEN until **2.3.x** chain + `G-2.3-*` evidence closes."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]"
links:
  - "[[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]"
  - "[[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[../Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-5-Execution-Envelope-Validation-Labels-and-Bundle-Chunk-Ordering-Boundary-Roadmap-2026-04-10-1705]]"
  - "[[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Execution-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-10-1830]]"
---

## Phase 2.3.2 — Execution verification task decomposition and failure payload contracts

Execution tertiary mirror for conceptual **2.3.2**. This slice binds **named validation tasks** (owner / inputs / outputs / done signals) to **`V-2.3-*`** matrix rows and **deterministic failure-payload field contracts**, with lane **godot (A) vs sandbox (B)** comparand parity and explicit execution-defer rows for registry / CI / warm-cache policy decisions.

> [!note] Queue alignment
> Dispatch `followup-deepen-exec-p232-tertiary-godot-20260410T214500Z` targets **tertiary 2.3.2** under the mirrored `Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/` spine; authoritative pre-read cursor was **`2.3.2`** per [[../../workflow_state-execution]] (`current_subphase_index: "2.3.2"`).

## Scope

**In scope:** Task IDs **T-2.3.2-1…5** with execution-ready boundaries; **`ValidationFailurePayload`** + rollup semantics; tightened **AC-2.3.2-*** rows; junior-dev pseudocode stubs for orchestration + payload emission.

**Out of scope:** CI YAML, perf benchmarks, final operator UX for diagnostics granularity (`D-2.3-diagnostics-granularity` remains execution-deferred).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Task orchestration | Resource-backed orchestrator + stable catalog revisions | In-memory orchestrator; identical task ids + ordering |
| Failure payloads | Payloads include vault-relative diagnostic refs where applicable | Synthetic correlation ids; same required field keys |
| Commit block | `deny_commit` when any mandatory gate fails | Harness records rollback token; same eligibility semantics |

## Pipeline seams — 2.3.1 matrix → 2.3.2 tasks → 2.3.3+ diagnostics

| Seam | Upstream | This slice (2.3.2) | Contract |
| --- | --- | --- | --- |
| Post–**2.3.1** | `V-2.3-*` matrix + AC scaffold ([[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]]) | Tasks decompose matrix evaluation into orchestrated units | Each `V-2.3-*` row maps to ≥1 task output artifact |
| Post–**2.2.4–2.2.5** | Envelopes + labels | Tasks **T-2.3.2-1** / **T-2.3.2-3** consume bundle + label policy | Failure payloads cite gate id + policy revision |
| Pre–**2.3.3+** | Diagnostics projection | **T-2.3.2-5** emits operator projection schema placeholders | Downstream refines warm-cache + UX without breaking payload keys |

## Task decomposition (execution binding)

| Task id | Owner | Inputs | Outputs | Done signal |
| --- | --- | --- | --- | --- |
| T-2.3.2-1 VerificationBundleAssembler | Validation spine maintainer | `StagedDeltaBundle`, hook envelopes, label coverage map, bundle metadata | `PreCommitVerificationBundle` with stable schema version + revision refs | Bundle shape stable; mandatory sections present |
| T-2.3.2-2 GateExecutionOrchestrator | Gate orchestrator | Bundle + `V-2.3-ORDER` contract | Ordered gate results with deterministic ids | Replay yields identical order + status tuple |
| T-2.3.2-3 FailurePayloadEmitter | Failure taxonomy owner | Gate stream + failing context + correlation ids | `ValidationFailurePayload` per failing gate + rollup payload | Each failure includes required fields per matrix row |
| T-2.3.2-4 CommitEligibilityResolver | Commit boundary owner | Gate stream + rollup payload | `allow_commit` / `deny_commit` + justification | Mandatory failure ⇒ `deny_commit` |
| T-2.3.2-5 DiagnosticsProjectionContract | Operator diagnostics owner | Failure payloads + gate metadata | Projection schema (per-gate + rollup) | Stable machine keys; supports **D-2.3-diagnostics-granularity** A/B without schema break |

## `V-2.3` rows → failure payload expectations

| Gate row | Failure payload expectations |
| --- | --- |
| `V-2.3-ORDER` | `failed_gate_id`, `expected_stage_order`, `actual_stage_order`, `first_order_violation`, `bundle_revision_ref`, `correlation_id` |
| `V-2.3-ENVELOPE` | `failed_gate_id`, `envelope_contract_ref`, `missing_or_invalid_fields[]`, `schema_catalog_revision`, `payload_outline_ref`, `correlation_id` |
| `V-2.3-LABELS` | `failed_gate_id`, `label_policy_revision`, `missing_labels[]`, `chunk_boundary_ref`, `coverage_ratio`, `correlation_id` |
| `V-2.3-ROLLUP` | `failed_gate_id`, `failed_gate_refs[]`, `commit_blocked: true`, `rollup_reason_code`, `operator_message_key`, `correlation_id` |

## Acceptance criteria (execution)

| AC id | Criterion | Verification method (NL) | Execution deferred |
| --- | --- | --- | --- |
| AC-2.3.2-1 | Every failed mandatory gate emits a deterministic payload with required fields | Replay failing bundle twice; compare field presence | yes (harness TBD) |
| AC-2.3.2-2 | Commit blocked when any mandatory gate fails with rollup linkage | Trace failures to resolver; `deny_commit` | yes (runtime TBD) |
| AC-2.3.2-3 | Projection supports per-gate vs rollup without upstream schema change | Contract review vs **D-2.3-diagnostics-granularity** | yes (UX TBD) |
| AC-2.3.2-4 | Warm-cache cannot bypass payload emission or commit-block | Cold vs warm path review | yes (`D-2.3-warm-cache-shortcuts`) |

## Pseudocode — orchestration + payload (junior-dev)

```pseudo
func run_validation_tasks(bundle: PreCommitVerificationBundle, catalog: GateCatalog) -> CommitEligibility:
  assembled = T232_1_assemble(bundle, catalog)
  stream = T232_2_run_gates_ordered(assembled, catalog)
  if stream.has_mandatory_failure():
    payloads = T232_3_emit_failure_payloads(stream)
    rollup = T232_3_emit_rollup(payloads)
    proj = T232_5_project_diagnostics(payloads, rollup)
    return T232_4_resolve_commit(stream, rollup)  // deny_commit
  return T232_4_resolve_commit(stream, empty_failure_ref())
```

## Roll-up gates — `G-2.3.2-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.3.2-Tasks-Bound` | **PASS** | Task decomposition table | `owner_signoff_G-2.3.2-Tasks-Bound_2026-04-10` |
| `G-2.3.2-Payload-Contracts` | **PASS** | Gate → payload expectations table | `owner_signoff_G-2.3.2-Payload-Contracts_2026-04-10` |
| `G-2.3.2-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.3.2-Lane-Comparand-Parity_2026-04-10` |
| `G-2.3.2-Registry-CI` | **FAIL (explicit, non-blocking)** | Registry/CI proof deferred | `owner_defer_G-2.3.2-Registry-CI_2026-04-10` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | open (execution-deferred) | Payload contracts do not claim registry closure |
| `CI-deferrals` | open (execution-deferred) | Automation binds to AC rows in a later slice |

## Related

- Parent secondary **2.3**: [[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]
- Prior tertiary **2.3.1**: [[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]]
- Next tertiary **2.3.3**: [[Phase-2-3-3-Execution-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-04-10-2206]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]
