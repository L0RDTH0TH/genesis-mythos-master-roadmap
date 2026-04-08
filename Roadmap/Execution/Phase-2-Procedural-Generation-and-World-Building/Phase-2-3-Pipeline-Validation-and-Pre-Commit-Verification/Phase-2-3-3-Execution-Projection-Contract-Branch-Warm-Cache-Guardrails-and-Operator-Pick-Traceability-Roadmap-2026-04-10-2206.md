---
title: Phase 2.3.3 — Execution projection contract branch, warm-cache guardrails, operator-pick traceability (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.3"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
priority: high
progress: 42
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
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-3-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-03-31-0216]]"
links:
  - "[[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]"
  - "[[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]]"
  - "[[Phase-2-3-2-Execution-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-04-10-2145]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[../Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-5-Execution-Envelope-Validation-Labels-and-Bundle-Chunk-Ordering-Boundary-Roadmap-2026-04-10-1705]]"
---

## Phase 2.3.3 — Execution projection contract branch, warm-cache guardrails, operator-pick traceability

Execution tertiary mirror for conceptual **2.3.3**. This slice binds **`D-2.3-diagnostics-granularity`** to the **gate-first projection + rollup companion** branch, materializes **warm-cache non-bypass** (`W-2.3.3-01`) against **2.3.2** task outputs, and defines **operator-pick trace** backlinks consumable by **2.3.4+** without schema bifurcation. Lane **godot (A) vs sandbox (B)** comparand parity is explicit; registry/CI remain execution-deferred.

> [!note] Queue alignment — stale target reconciled
> Queue `user_guidance` cited **first tertiary 2.3.1** / test-plan scaffold vs authoritative **`current_subphase_index: "2.3.3"`** in [[../../workflow_state-execution]]. **stale_queue_target_reconciled: true** — this run mints **2.3.3** (not duplicate **2.3.1** / **2.3.2**). Cursor advances to **`2.3.4`**.

## Scope

**In scope:** Projection-contract branch tables; warm-cache guardrail vs **T-2.3.2-5** projection contract; operator-pick trace line schema (decision id → consumer wikilinks); `G-2.3.3-*` PASS rows where evidence is NL-complete.

**Out of scope:** Cache residency/TTL implementation, serializer classes, CI wiring, final diagnostics UX (`GMM-2.4.5-*`, `CI-deferrals` explicit non-blocking FAIL).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Projection branch | Gate-first payloads + rollup companion; stable machine keys | Identical branch; synthetic fixtures |
| Warm-cache | Resource-backed memoization with revision-fallback to cold path | In-memory memoization; same non-bypass invariant |
| Operator-pick trace | Vault-relative backlinks in [[../../../decisions-log]] rows | Same trace schema; synthetic queue ids |

## Pipeline seams — 2.3.2 tasks → 2.3.3 branch → 2.3.4+

| Seam | Upstream | This slice (2.3.3) | Downstream |
| --- | --- | --- | --- |
| Post–**2.3.2** | Task + payload tables ([[Phase-2-3-2-Execution-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-04-10-2145]]) | Binds branch + `W-2.3.3-01` to emitted payloads | **2.3.4** specializes validation-trace payloads |
| Post–**2.3.1** | `V-2.3-*` matrix | Branch preserves per-gate authority vs rollup companion | Matrix rows unchanged — branch is display/UX policy, not gate taxonomy |
| Post–**2.2.5** | Labels + chunk boundaries | Warm-cache cannot skip label revision checks | Same as cold path for mandatory failures |

## Bound projection-contract branch (execution)

| Contract | Authority | Machine invariant |
| --- | --- | --- |
| **Gate-first** | Per-gate `ValidationFailurePayload` ids are authoritative for commit block | Mandatory failure ⇒ per-gate payload emitted before rollup |
| **Rollup companion** | Rollup summarizes failed mandatory gates; never replaces per-gate payload | Rollup refs ⊆ failed gate id set |
| **UI default** | “Rollup-first display” allowed only as presentation; commit logic uses per-gate ids | No schema split |

## Warm-cache guardrail — **W-2.3.3-01** (execution binding)

For any evaluation path labeled warm-cache:

1. Mandatory gate failures emit the **same required fields** as cold-path evaluation for that gate id + bundle revision.
2. Commit eligibility resolves to **`deny_commit`** whenever any mandatory gate fails — warm-cache may not short-circuit payload emission or flip commit outcome.
3. Stale label revision ⇒ **fallback to cold strict validation** for `V-2.3-LABELS` (per conceptual edge case).

## Operator-pick trace lines (schema)

Each applied `D-*` decision records under [[../../../decisions-log]]:

- `decision_id`, `chosen_branch`, `queue_entry_id`, `consuming_artifacts[]` (wikilinks).

**This slice consumes:**

- `D-2.3-diagnostics-granularity` → branch rows in this note.
- `D-2.3-warm-cache-shortcuts` (if present) → non-bypass table; defer if not in decisions-log yet (`#review-needed` advisory only).

## Acceptance criteria (execution)

> [!note] HR vs harness-deferred ACs
> **`handoff_readiness: 85`** here applies to **NL + table/schema completeness** for this slice (projection branch + warm-cache invariant + trace schema). **Executable falsification** rows remain **`execution deferred: yes`** until **2.3.4+** introduces harness-bound references — consistent with **`last_conf` 81** on [[../../workflow_state-execution]] **Iter 28** (per-run confidence), which measures the deepen pass, not a runtime proof.

| AC id | Criterion | Verification method (NL) | Execution deferred |
| --- | --- | --- | --- |
| AC-2.3.3-1 | Branch binding is unique and referenced by warm-cache rows | Trace table ↔ conceptual **2.3.3** | yes (harness) |
| AC-2.3.3-2 | Non-bypass invariant is falsifiable (warm vs cold payload field parity) | Pair replay with injected failures | yes |
| AC-2.3.3-3 | Operator-pick trace schema is stable for **2.3.4** consumption | Contract review vs **2.3.4** conceptual | yes |

## Pseudocode — warm-cache evaluation wrapper (junior-dev)

```pseudo
func eval_with_warm_cache(bundle: PreCommitVerificationBundle, cache: ValidationMemo) -> CommitEligibility:
  key = stable_cache_key(bundle)
  if cache.has(key) and cache.revision_matches(bundle.label_revision):
    cold_equiv = materialize_failure_payloads_if_mandatory_failed(cache.payload_refs)
    if cold_equiv.incomplete():
      return cold_strict_eval(bundle)  // fallback — still emit full payloads
    return resolve_commit(cold_equiv)
  return cold_strict_eval(bundle)
```

## Roll-up gates — `G-2.3.3-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.3.3-Branch-Bound` | **PASS** | Bound branch table | `owner_signoff_G-2.3.3-Branch-Bound_2026-04-10` |
| `G-2.3.3-Warm-Cache-NonBypass` | **PASS** | W-2.3.3-01 + pseudocode | `owner_signoff_G-2.3.3-Warm-Cache-NonBypass_2026-04-10` |
| `G-2.3.3-Operator-Trace-Schema` | **PASS** | Operator-pick trace section | `owner_signoff_G-2.3.3-Operator-Trace-Schema_2026-04-10` |
| `G-2.3.3-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.3.3-Lane-Comparand-Parity_2026-04-10` |
| `G-2.3.3-Registry-CI` | **FAIL (explicit, non-blocking)** | Registry/CI proof deferred | `owner_defer_G-2.3.3-Registry-CI_2026-04-10` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | open (execution-deferred) | Branch binding does not claim registry closure |
| `CI-deferrals` | open (execution-deferred) | Warm-cache proofs in CI harness later |

## Related

- Parent secondary **2.3**: [[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]
- Prior tertiaries: [[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]], [[Phase-2-3-2-Execution-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-04-10-2145]]
- Next tertiary **2.3.4** (conceptual): [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]]
