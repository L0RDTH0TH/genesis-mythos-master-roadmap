---
title: Phase 1.2 — Execution procedural-generation graph skeleton (Godot lane)
roadmap-level: secondary
phase-number: 1
subphase-index: "1.2"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps:
  - "Deferred seams `GMM-2.4.5-*` and `CI-deferrals` remain execution-open with explicit owner/timebox below."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
links:
  - "[[../Phase-1-Execution-Foundation-and-Core-Architecture-Roadmap-2026-04-10-1315]]"
  - "[[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Execution-Layering-and-Interface-Contracts-Roadmap-2026-04-10-1316]]"
---

## Phase 1.2 — Execution graph skeleton (parallel spine)

Execution mirror for conceptual `1.2` under the required execution parallel spine. This slice keeps lane A/B comparand parity explicit while turning graph-stage structure into implementation-shaped contracts with deterministic ordering and pre-run validation semantics.

## Scope

**In scope:** stage families, typed edges, deterministic topological ordering, intent-injection seams, dry-run verification, and owner-path evidence rows that can be implemented by a junior dev without choosing final serialization formats.

**Out of scope:** final stage internals, CI closure, performance/HR proofs, and closure of deferred `GMM-2.4.5-*` registry rows.

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Stage registry host | `GraphStageRegistry` scriptable resource + deterministic index ordering | In-memory list with fixed order constants |
| Pre-run validation | `DryRunGraph(manifest)` checks DAG, inputs, and hook signatures before commit | Harness validates shape + edge keys only |
| Intent injection | Named hook map (`before_stage`, `after_stage`) bound to typed envelopes | Hook names preserved, payloads simplified |
| Replay identity | Seed bundle + stage digest carried with run manifest ID | Seed + hash string in log output |

## Stage/edge contract matrix

| Stage family | Inputs | Outputs | Determinism guard | Failure mode |
| --- | --- | --- | --- | --- |
| Seed expansion | Campaign seed bundle, world profile | Expanded seed graph | Stable stage digest from manifest order | `seed_bundle_invalid` |
| Topology materialization | Seed graph + terrain policy | Typed node/edge set | Topological sort must be stable by key | `graph_cycle_detected` |
| Biome/layout assignment | Node graph + biome catalogs | Tagged region overlays | Catalog key parity across lanes | `catalog_mismatch` |
| Entity spawn planning | Region overlays + spawn templates | Spawn staging delta | Deterministic spawn ordering keys | `spawn_plan_invalid` |
| Narrative glue stubs | Spawn plan + lore tags | Hook metadata for runtime systems | Manifest revision + hook namespace lock | `hook_namespace_collision` |

## Pseudocode — dry-run then commit gate

```pseudo
func run_generation(manifest, intents):
  dry = graph_runner.dry_run(manifest, intents)
  if not dry.ok:
    return reject(dry.reason)

  staged = graph_runner.execute(manifest, intents)
  if not staged.ok:
    return reject(staged.reason)

  return world_commit_gateway.commit(staged.delta, HardValidate)
```

## Acceptance criteria

1. **AC-1:** Stage registry rows are explicit and preserve deterministic order keys for all stage families in this slice.
2. **AC-2:** Dry-run path catches at least `graph_cycle_detected` and `hook_namespace_collision` before any world-state commit.
3. **AC-3:** Intent injection seams are named and parity-mapped for Godot (A) and sandbox (B).
4. **AC-4:** Replay identity fields (seed + manifest/stage digest) are documented in this note and linked to owner artifacts.
5. **AC-5:** Deferred closure artifacts (`GMM-2.4.5-*`, CI/HR) remain explicit and non-blocking for this execution secondary mint.

## Risk register v0 (Phase 1.2)

| risk_id | description | impact | likelihood | mitigation | trigger_signal | owner | review_cadence | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-1.2-topology-drift` | Topological order diverges between dry-run and execution path | high | medium | Enforce digest parity checks in `G-1.2-Topo-Determinism` and `G-1.2-DryRun-Parity` | Digest mismatch for identical manifest/seed | lane A/B maintainer | per deepen | open |
| `R-1.2-edge-schema-leak` | Edge contracts lack typed versions, causing ambiguous consumers | high | medium | Gate merge on explicit edge schema rows (`edge_type`, `version`, producer/consumer) | Missing schema keys in tertiary matrix | architecture reviewer | per deepen | open |
| `R-1.2-hook-collision` | Intent injection hook names collide across stage families | medium | medium | Namespace validation in dry-run + hook registry review | Duplicate hook namespace in validation report | lane godot implementation owner | per deepen | open |
| `R-1.2-deferred-seam-ambiguity` | Deferred seam rows remain placeholder-only and uncloseable | medium | low | Bind closure map to concrete 1.2.1 artifacts + gate IDs | Deferred seam row without artifact link | roadmap maintainer | per recal or deepen | open |

## Deferred seams (explicit)

- `GMM-2.4.5-*`: still open and tracked in execution state surfaces; this note only carries owner-path mapping placeholders.
- CI/HR/registry closure: execution-deferred and non-blocking for 1.2 structural mint.

## 1.2 roll-up closure (from 1.2.1 evidence)

| gate_id | evidence_source | verdict | parity_note | owner_signoff | closed_at |
| --- | --- | --- | --- | --- | --- |
| `G-1.2-Node-Taxonomy` | [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416#G-1.2 roll-up gate table (execution)]] | **PASS** | Godot (A) and sandbox (B) expose the same gate ID and schema row labels | `owner_signoff_g_1_2_node_taxonomy_2026-04-08` | 2026-04-08 |
| `G-1.2-Edge-Typing` | [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416#G-1.2 roll-up gate table (execution)]] | **PASS** | Lane B keeps simplified payloads but preserves typed key/version columns | `owner_signoff_g_1_2_edge_typing_2026-04-08` | 2026-04-08 |
| `G-1.2-Topo-Determinism` | [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416#G-1.2 roll-up gate table (execution)]] | **PASS** | Digest procedure and key tuple are parity-aligned across A/B | `owner_signoff_g_1_2_topo_determinism_2026-04-08` | 2026-04-08 |
| `G-1.2-DryRun-Parity` | [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416#G-1.2 roll-up gate table (execution)]] | **PASS** | Dry-run vs run gate naming remains isomorphic in both lanes | `owner_signoff_g_1_2_dryrun_parity_2026-04-08` | 2026-04-08 |

## Deferred seam owner/timebox map (explicit)

| seam_id | owner | owner_path | timebox | state | closure_requires |
| --- | --- | --- | --- | --- | --- |
| `GMM-2.4.5-*` | lane godot implementation owner | [[Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416]] | by 2026-04-22 | open | Promote owner artifact evidence into execution seam map and run recal parity check |
| `CI-deferrals` | roadmap maintainer + CI owner | [[../Phase-1-Execution-Foundation-and-Core-Architecture-Roadmap-2026-04-10-1315]] | by 2026-04-29 | open | CI proof rows for topo determinism + dry-run parity propagated from 1.2 closure |

## Next structural execution target

- Reconcile **phase 1 primary** gate map with this closed 1.2 roll-up, then route to next execution mint under the mirrored spine.

## Related

- Conceptual counterpart: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- Execution primary: [[../Phase-1-Execution-Foundation-and-Core-Architecture-Roadmap-2026-04-10-1315]]
- Execution secondary 1.1: [[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Execution-Layering-and-Interface-Contracts-Roadmap-2026-04-10-1316]]
