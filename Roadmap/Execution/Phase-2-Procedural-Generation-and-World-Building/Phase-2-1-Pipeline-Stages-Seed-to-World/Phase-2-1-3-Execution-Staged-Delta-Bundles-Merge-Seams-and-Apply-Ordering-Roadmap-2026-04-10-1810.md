---
title: Phase 2.1.3 — Execution staged delta bundles, merge seams, and apply ordering (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.3"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 87
handoff_gaps:
  - "Tertiaries 2.1.4–2.1.5 not minted; `phase2_gate_replay_traceability` remains open at primary until chain advances."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]"
links:
  - "[[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-1-1-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2215]]"
  - "[[Phase-2-1-2-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2230]]"
---

## Phase 2.1.3 — Execution pipeline stage seams (seed → world)

Execution tertiary mirror for conceptual **2.1.3**. This slice makes **stage-to-stage seams** (S0→S5) and **StagedDeltaBundle** merge/apply ordering **gate-verifiable**: explicit `G-2.1.3-*` rows, junior-dev stub pseudocode at each seam, and lane **godot (A)** vs **sandbox (B)** comparand parity. **`GMM-2.4.5-*`** registry closure and **CI** proof rows remain **execution-deferred** with owner/timebox callouts (see [[../../workflow_state-execution#Deferred safety seam closure map]]) — not blocking this slice.

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Bundle materialization | `StagedDeltaBundle` resource assembled from stage outputs | In-memory bundle object; identical field names |
| Merge seam registry | `MergeSeamCatalog` loaded from project settings | Harness catalog with same seam IDs |
| Ordering digest | `apply_ops_ordered` + `ordering_key` hashed for replay | Same digest schema |
| Trace IDs | `trace_id` per seam fan-in for tooling | Harness-local IDs |

## Stage seam matrix (seed → world spine)

| Seam ID | From → To | Typed handoff | Failure surface | Notes |
| --- | --- | --- | --- | --- |
| `seam_S0_S1` | S0 → S1 | `ExpandedSeedIdentity` → `IntentEnvelope` | `seed_shape_invalid` | Junior stub: `handoff_seed_to_intent(expanded)` |
| `seam_S1_S2` | S1 → S2 | `ResolvedHookBatch` → pipeline eval inputs | `hook_collision` | Stub binds hooks to eval scope |
| `seam_S2_S3` | S2 → S3 | `StagedWorldDelta` → `SimBootstrapPackage` | `bootstrap_shape_invalid` | Merge seams fan-in multi-fragment deltas |
| `seam_S3_S4` | S3 → S4 | Package → `DryRunVerdict` | `dry_run_reject` | Bundle-level validation (extends 2.1.1/2.1.2) |
| `seam_S4_S5` | S4 → S5 | Labels + `CommitAllowed` → commit | `commit_reject` | No commit without S4 materialization (2.1.2) |

## `G-2.1.3-*` gate rows (execution)

| Gate ID | Check | Evidence in this note | Verdict | Owner token |
| --- | --- | --- | --- | --- |
| `G-2.1.3-Merge-Seam-Explicit` | Every fan-in declares a **MergeSeamId** + rule family (no silent LWW) | [[#Merge seam catalog (stub)]] | **PASS** | `owner_signoff_G-2.1.3-Merge-Seam-Explicit_2026-04-10` |
| `G-2.1.3-Apply-Order-Total` | Default ordering follows stage spine 0→5; disjoint ops may partial-order | [[#Pseudocode — bundle assembly]] | **PASS** | `owner_signoff_G-2.1.3-Apply-Order-Total_2026-04-10` |
| `G-2.1.3-Labels-Preserved-Across-Seams` | `ValidationDecisionLabels` survive merge (bundle-level + per-seam optional) | [[#Lane comparand]] + [[#Edge-case rows]] | **PASS** | `owner_signoff_G-2.1.3-Labels-Preserved-Across-Seams_2026-04-10` |
| `G-2.1.3-Registry-CI-Deferred` | `GMM-2.4.5-*` / CI closure not claimed here | [[#Deferred registry / CI (owner + timebox)]] | **FAIL (explicit, non-blocking)** | `owner_defer_G-2.1.3-Registry-CI-Deferred_2026-04-10` |

## Merge seam catalog (stub)

| MergeSeamId | Rule family | Domains | Resolution record required on conflict |
| --- | --- | --- | --- |
| `terrain+biome@regionA` | additive_composition | terrain, biome | yes |
| `poi+entity@layerL` | disjoint_or_explicit_override | POI, entity | yes |
| `sim_bootstrap+staged_delta` | spine_order_then_merge | sim, world | yes |

## Pseudocode — bundle assembly (junior-dev stub)

```pseudo
func assemble_bundle(fragments[], seams: MergeSeamCatalog, labels_from_212: ValidationDecisionLabels):
  bundle = StagedDeltaBundle.new(bundleIdentity = hash(fragments, seams))
  for seam in seams.ordered_fanins():
    merged = seam.merge(fragments.filter(seam.domain_tags))
    assert merged.has_resolution_record_if_overlap()
    bundle.apply_ops.extend(merged.ops_with_ordering_keys())
  bundle.validation_labels = labels_from_212.propagate_through_seams(seams)
  return bundle

func seam_S3_S4(bootstrap: SimBootstrapPackage, intents):
  # seam before dry-run: package shape must match Stage 3 outputs
  assert bootstrap.staged_delta.seams_referenced ⊆ catalog.ids
  return pipeline.dry_run(bootstrap.manifest, intents)
```

## Edge-case rows

| Case | Expected | Gate |
| --- | --- | --- |
| Overlapping fragments without resolution | Stage 4 deny; bundle not commit-eligible | `G-2.1.3-Merge-Seam-Explicit` |
| Empty bundle | Trivial S4 pass; labels may state no-op | aligns with conceptual **2.1.3** |
| Label loss at a seam | Validation fails closed | `G-2.1.3-Labels-Preserved-Across-Seams` |

## Deferred registry / CI (owner + timebox)

| Item | Owner role | Timebox | Evidence path (planned) |
| --- | --- | --- | --- |
| `GMM-2.4.5-*` | registry/tech lead | **2026-04-22** review checkpoint | See [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416]] + [[../../workflow_state-execution#Deferred safety seam closure map]] |
| `CI-deferrals` | build/CI owner | **2026-04-29** review checkpoint | See [[Phase-1-2-Execution-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-1415]] |

## Test matrix (executable sketch)

| Case ID | Fixture | Expected | Pass ties to |
| --- | --- | --- | --- |
| TM-2.1.3-01 | Two overlapping fragments, explicit resolution | Bundle validates; S4 PASS | `G-2.1.3-Merge-Seam-Explicit` |
| TM-2.1.3-02 | Overlap, no resolution | S4 deny; no S5 token | seam + 2.1.2 label rules |
| TM-2.1.3-03 | Labels stripped at seam (injected bug) | Digest mismatch / deny | `G-2.1.3-Labels-Preserved-Across-Seams` |

## Acceptance criteria

1. Mirrored path matches conceptual subtree (parallel spine; no Execution-root heap).
2. `G-2.1.3-*` rows are explicit PASS or explicit non-blocking FAIL for deferrals.
3. Stage seams S0→S5 are named with junior stubs and ordering discipline.
4. Lane A/B comparand remains machine-traceable.

## Related

- Prior tertiaries **2.1.1**, **2.1.2**: [[Phase-2-1-1-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2215]], [[Phase-2-1-2-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2230]]
- Parent secondary: [[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]
- Execution primary: [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
