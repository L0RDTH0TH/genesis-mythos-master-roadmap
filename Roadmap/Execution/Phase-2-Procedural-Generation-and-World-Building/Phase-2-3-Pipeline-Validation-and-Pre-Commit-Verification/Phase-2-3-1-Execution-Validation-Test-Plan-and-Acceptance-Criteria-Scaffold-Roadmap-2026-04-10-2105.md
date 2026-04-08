---
title: Phase 2.3.1 — Execution validation test plan and acceptance criteria scaffold (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.1"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
priority: high
progress: 35
handoff_readiness: 84
handoff_gaps:
  - "Tertiary **2.3.3+** not yet minted; `G-2.3-*` secondary roll-up still OPEN until chain + owner tokens."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-1-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-03-30-2140]]"
links:
  - "[[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[../Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-5-Execution-Envelope-Validation-Labels-and-Bundle-Chunk-Ordering-Boundary-Roadmap-2026-04-10-1705]]"
  - "[[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Execution-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-10-1830]]"
---

## Phase 2.3.1 — Execution validation test plan and acceptance criteria scaffold

Execution tertiary mirror for conceptual **2.3.1**. This slice materializes the **test matrix** + **acceptance criteria IDs** for `PreCommitVerificationBundle` validation against the **2.3** gate taxonomy, with explicit dry-run vs execute parity hooks and lane **godot (A) vs sandbox (B)** comparand rows.

> [!note] Stale queue target reconciled
> Queue `followup-deepen-exec-p23-secondary-godot-20260410T180500Z` + user_guidance referenced **secondary 2.3** mint / cursor **`2.3`**. **Authoritative cursor at dispatch** was **`2.3.1`** (secondary **2.3** already minted **Iter 25** in [[../../workflow_state-execution]]). This run mints **tertiary 2.3.1** (forward reconcile — **not** a duplicate secondary).

## Scope

**In scope:** NL **test-plan rows** mapping each mandatory gate to bundle inputs + expected pass/fail; **AC-* IDs** tied to `G-2.3-*` rollup semantics; explicit execution-deferred markers for CI/automation binding.

**Out of scope:** test code, CI YAML, cryptographic proofs (`GMM-2.4.5-*` remain defer rows).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Test harness | Resource-backed `ValidationOrchestrator` + stable `GateCatalog` revision | In-memory harness with identical ordering keys |
| Matrix rows | Same `V-2.3-*` IDs; diagnostics include resource paths | Synthetic fixtures; diff-only diagnostics |
| AC verification | Manual operator signoff tokens on AC rows | Harness records expected AC token when automation lands |

## Pipeline seams — 2.3 secondary → 2.3.1 test scaffold

| Seam | Upstream | This slice (2.3.1) | Contract |
| --- | --- | --- | --- |
| Post–**2.3** | Gate taxonomy + bundle assembly ([[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]) | Matrix maps gates → bundle elements | Every `G-2.3-*` mandatory row has ≥1 `V-2.3-*` matrix row |
| Post–**2.2.5** | Validation labels + chunk boundaries | Matrix includes label/chunk coverage rows | Fails closed when label coverage violates chunk policy |
| Post–**2.1.5** | Replay ledger + restore cursor | Matrix binds digest inputs for deterministic replay | Same bundle + catalog revision → same verdict |

## Test matrix (execution scaffold)

| Gate / check ID | Bundle elements consumed | Expected outcome | Evidence owner |
| --- | --- | --- | --- |
| `V-2.3-ORDER` | Staged deltas + spine order keys (**2.1.3** seams) | Pass iff ordering matches canonical spine | Ordering digest row |
| `V-2.3-ENVELOPE` | Hook payloads + **2.2.4** envelope | Pass iff `PreCommitVerificationBundle` envelope valid | Envelope shape table |
| `V-2.3-LABELS` | Validation labels + chunk boundaries (**2.2.5**) | Pass iff label coverage satisfies chunk policy | Label coverage checklist |
| `V-2.3-ROLLUP` | All prior `V-2.3-*` results | Pass iff **no commit** when any mandatory check fails | Roll-up verdict row |

## Acceptance criteria (stable IDs)

| AC id | Criterion | Verification method (NL) | Execution deferred |
| --- | --- | --- | --- |
| AC-2.3.1-1 | No commit when `V-2.3-ROLLUP` fails | Dry-run blocks commit; diagnostics cite failing gate | yes (automation TBD) |
| AC-2.3.1-2 | Deterministic verdict for same bundle + catalog revision | Repeat dry-run; compare verdict + diagnostics | yes (replay harness TBD) |
| AC-2.3.1-3 | Failure payload references **gate id** (not opaque codes) | Inspect failure payload shape | yes (UX TBD) |

## Pseudocode — matrix evaluation stub (junior-dev)

```pseudo
func eval_validation_matrix(bundle: PreCommitVerificationBundle, matrix: ValidationMatrix, catalog: GateCatalog) -> MatrixVerdict:
  rows = []
  for row in matrix.rows_ordered_like_spine(catalog):
    r = row.eval(bundle)
    rows.append(r)
    if row.mandatory and not r.ok:
      return MatrixVerdict(commit_eligible=false, failed_row=row.id, rows=rows)
  return MatrixVerdict(commit_eligible=true, rows=rows)
```

## Roll-up gates — `G-2.3.1-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.3.1-Matrix-Complete` | **PASS** | Test matrix table + seam binds | `owner_signoff_G-2.3.1-Matrix-Complete_2026-04-10` |
| `G-2.3.1-AC-IDs` | **PASS** | Acceptance criteria table | `owner_signoff_G-2.3.1-AC-IDs_2026-04-10` |
| `G-2.3.1-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.3.1-Lane-Comparand-Parity_2026-04-10` |
| `G-2.3.1-Registry-CI` | **FAIL (explicit, non-blocking)** | Registry/CI proof deferred | `owner_defer_G-2.3.1-Registry-CI_2026-04-10` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | open (execution-deferred) | Matrix does not claim registry closure |
| `CI-deferrals` | open (execution-deferred) | Automation binds to AC rows later |

## Related

- Next tertiary **2.3.2**: [[Phase-2-3-2-Execution-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-04-10-2145]]
- Parent secondary **2.3**: [[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-1-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-03-30-2140]]
