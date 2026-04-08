---
title: Phase 2.1.4 — Execution bundle identity, seam catalog stability, and replay/diff contracts (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.4"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 88
handoff_gaps:
  - "Tertiary **2.1.5** not minted; `phase2_gate_replay_traceability` closure pending end of chain."
execution_stub_binding: advisory_vault_anchors_only
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]"
links:
  - "[[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-1-3-Execution-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-10-1810]]"
---

## Phase 2.1.4 — Execution bundle identity, seam catalog stability, replay/diff

Execution tertiary mirror for conceptual **2.1.4**. This slice binds **BundleIdentity** + **SeamCatalogRevision** + **replay-equivalence** + **deterministic bundle diff** to gate-verifiable rows (`G-2.1.4-*`), composing upstream **2.1.3** bundle/merge seams without re-litigating Stage 4 ordering. Lane **godot (A)** vs **sandbox (B)** comparand parity preserved. **`GMM-2.4.5-*`** / **CI** remain **execution-deferred** (explicit non-blocking FAIL) per [[../../workflow_state-execution#Deferred safety seam closure map]].

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Bundle identity materialization | `BundleIdentity` resource with stable logical fields + engine digest hook | In-memory identity tuple; same field names |
| Catalog revision | `SeamCatalogRevision` string from project settings + graph stamp | Harness revision token |
| Replay equivalence | `replay_equivalent(a,b)` uses catalog rev + seam records + apply op ids | Same predicate |
| Diff surface | `BundleDiffSummary` exported to tooling / tests | Identical schema |

> [!note] Gate semantics (execution track)
> **`PASS`** on **`G-2.1.4-*`** here means **documentation completeness + explicit deferrals** for junior-dev stubs and lane comparands — **not** shipped engine code or CI proofs. Registry/CI remain **execution-deferred** per [[../../workflow_state-execution#Deferred safety seam closure map]].

## `G-2.1.4-*` gate rows (execution)

| Gate ID | Check | Evidence in this note | Verdict | Owner token |
| --- | --- | --- | --- | --- |
| `G-2.1.4-Identity-Total` | **BundleIdentity** fields populated; no silent drift vs **2.1.3** ordering digest | [[#Bundle identity composition (stub)]] | **PASS** | `owner_signoff_G-2.1.4-Identity-Total_2026-04-08` |
| `G-2.1.4-Catalog-Rev-Monotonic` | **SeamCatalogRevision** monotonic; rollback forbidden without forward migration id | [[#Seam catalog revision rules]] | **PASS** | `owner_signoff_G-2.1.4-Catalog-Rev-Monotonic_2026-04-08` |
| `G-2.1.4-Replay-Equivalence` | Replay-equivalence relation matches NL contract; mismatched rev → not equivalent | [[#Replay / diff pseudocode]] | **PASS** | `owner_signoff_G-2.1.4-Replay-Equivalence_2026-04-08` |
| `G-2.1.4-Diff-Structural` | `diff_bundle` reports seam/op/label changes under same catalog rev | [[#Edge-case rows]] | **PASS** | `owner_signoff_G-2.1.4-Diff-Structural_2026-04-08` |
| `G-2.1.4-Registry-CI-Deferred` | No claim of registry/CI closure | [[#Deferred registry / CI]] | **FAIL (explicit, non-blocking)** | `owner_defer_G-2.1.4-Registry-CI-Deferred_2026-04-08` |

## Bundle identity composition (stub)

| Field | Role | Notes |
| --- | --- | --- |
| `seedBundleRef` | Upstream seed identity | Ties to Phase 2 spine seed bundle |
| `seamCatalogRevision` | Opaque monotonic token | Bumps on seam add/remove |
| `applyFingerprint` | Canonical apply op fingerprint | Aligns with **2.1.3** ordering |
| `participatingSeams[]` | Seam ids touched this bundle | Drives partial regen story |

## Seam catalog revision rules

- **Add seam:** bump revision; old bundles rejected at Stage 4 unless migration path recorded.
- **Remove seam:** forward revision + migration note (NL); no silent deletes.
- **Rollback:** forbidden as monotonic decrease — only new forward revision restoring definitions.

## Advisory artifact binding (execution-deferral, vault anchors)

| Concept | Vault anchor | Binding class |
| --- | --- | --- |
| `BundleIdentity` | This note [[#Bundle identity composition (stub)]] + conceptual counterpart [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]] (NL § Behavior) | `advisory_narrative` |
| `SeamCatalogRevision` | [[#Seam catalog revision rules]] + parent secondary [[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]] | `advisory_narrative` |
| Engine resource paths | *Deferred* — use `pending_engine_anchor_post_215` after tertiary **2.1.5** mint | `pending_engine_anchor_post_215` |

## Replay / diff pseudocode (junior-dev stub)

```pseudo
func bundle_identity(seed_id, catalog_rev, apply_ops_ordered, seam_records):
  return stable_logical_key(seed_id, catalog_rev, canonicalize(apply_ops_ordered), canonicalize(seam_records))

func replay_equivalent(a, b):
  if a.seamCatalogRevision != b.seamCatalogRevision: return false
  return structural_match(a.applyOpsOrdered, b.applyOpsOrdered, a.seamRecords, b.seamRecords)

func diff_bundle(a, b):
  if a.seamCatalogRevision != b.seamCatalogRevision:
    return BundleDiffSummary(catalog_mismatch=true)
  return structural_diff(a.applyOpsOrdered, b.applyOpsOrdered, a.seamRecords, b.seamRecords, a.validationLabels, b.validationLabels)
```

## Edge-case rows

| Case | Expected | Gate |
| --- | --- | --- |
| Same ops, different catalog revision | Not replay-equivalent until migration | `G-2.1.4-Replay-Equivalence` |
| Catalog rollback attempt | Hard fail at validation / tooling | `G-2.1.4-Catalog-Rev-Monotonic` |
| Label drift without op change | Diff surfaces `labelChanges[]` | `G-2.1.4-Diff-Structural` |

## Deferred registry / CI

| Item | Owner role | Timebox | Evidence path (planned) |
| --- | --- | --- | --- |
| `GMM-2.4.5-*` | registry/tech lead | **2026-04-22** | [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416]] |
| `CI-deferrals` | build/CI owner | **2026-04-29** | [[Phase-1-2-Execution-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-1415]] |

## Test matrix (executable sketch)

| Case ID | Fixture | Expected | Pass ties to |
| --- | --- | --- | --- |
| TM-2.1.4-01 | Two bundles, same inputs, same catalog rev | Identities replay-equivalent | `G-2.1.4-Replay-Equivalence` |
| TM-2.1.4-02 | Catalog rev bump, no migration | Stage 4 catalog mismatch | `G-2.1.4-Catalog-Rev-Monotonic` |
| TM-2.1.4-03 | Label-only drift | Diff non-empty; replay may still pass if labels excluded by policy | `G-2.1.4-Diff-Structural` |

## Acceptance criteria

1. Mirrored path matches conceptual subtree (parallel spine).
2. `G-2.1.4-*` rows are explicit PASS or explicit non-blocking FAIL for deferrals.
3. Bundle identity + catalog revision + replay/diff contracts are named and traceable to **2.1.3**.
4. Lane A/B comparand remains machine-traceable.

## Related

- Prior tertiary **2.1.3**: [[Phase-2-1-3-Execution-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-10-1810]]
- Parent secondary: [[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]
- Phase 2 primary: [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
