---
title: Phase 2.1.1 — Stage graph & per-stage IO contracts
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1.1"
handoff_readiness: 90
links:
  - "[[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]]"
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
---

## Phase 2.1.1 — Stage graph & per-stage IO contracts

> [!summary] TL;DR
> Freeze the **v0 StageGraph DAG**, **per-stage IO handles**, and **hash propagation** rules so later tertiaries (RNG ordering, failure codes, plugins) plug into a single spine. External PCG graphs and ECS manifest patterns inform **immutable published outputs** and **spawn-facing manifests** without changing Phase 1 replay semantics.

### Scope

This tertiary implements the first checkbox cluster under Phase 2.1 **Objectives**: stage graph definition + per-stage IO + deterministic ordering hooks + failure surfaces + plugin/kernel boundary **at contract level** (executable stubs remain Phase 2.2+ unless otherwise queued).

### Stage graph (v0 DAG)

- **Nodes:** minimal kernel set `{ SeedParse, LatticeSynthesis, PolicyBind, ManifestEmit, SpawnCommit }` with **optional** `{ IntentAnnotate }` stubbed behind feature flag (position TBD in 2.1.2).
- **Edges (must hold for v0):**
  - `SeedParse → LatticeSynthesis → PolicyBind → ManifestEmit → SpawnCommit`
  - `IntentAnnotate` may insert **only** at allowed attachment points decided in 2.1.2; until then, compiler rejects any edge that creates a cycle.
- **Metadata:** `StageGraph { nodes, edges, version: semver-string }` stored in `GenerationContext` ledger; **bump `version` on any edge or contract change** (replay sees graph version in harness matrix).

### Per-stage IO contracts

| Stage | Immutable inputs (handles) | Published output artifact | Required metadata on publish |
| --- | --- | --- | --- |
| SeedParse | `SeedEnvelope` bytes + `seed_hash` | `ParsedSeed` view | `stage_version_id`, `output_hash` |
| LatticeSynthesis | `ParsedSeed`, `stage_graph_version` | `DensityLattice` | `lattice_hash`, `stage_version_id` |
| PolicyBind | `DensityLattice`, `SpawnPolicySet` ref | `BoundPolicyContext` | `policy_bundle_hash`, `stage_version_id` |
| ManifestEmit | `BoundPolicyContext`, traversal order token | `EntityManifest` (sorted) | `manifest_hash` (per distilled-core 2.1.4), `stage_version_id` |
| SpawnCommit | `EntityManifest`, sim tick fence token | `SpawnLedger` events | deterministic `spawn_event_id` sequence |

**Invariant:** consumers read **only** published handles; no shared mutable scratch across stages. Async/worker stages (future) must reconcile through the **single commit barrier** described in Phase 2.1 research integration.

### Deterministic ordering hooks

- **Traversal token:** `ManifestEmit` receives an explicit **sorted key order** (e.g. `CellCoord` lexicographic) generated from lattice metadata, not from map iteration order.
- **RNG:** each stage receives **sub-stream ids** derived from `(stage_name, stage_version_id, region_id, rule_id)`; streams are **created** at stage entry and **sealed** at publish.

### Failure surfaces (replay events)

- Any publish failure emits `stage_failed.event` with `reason_code` from the Phase 1 taxonomy extension (`STAGE_INPUT_HASH_MISMATCH`, `STAGE_VERSION_SKEW`, `MANIFEST_SORT_ORDER_VIOLATION`, …) — **no silent partial publish**.
- Failed stage **does not** advance the stage ledger tail; resume paths re-enter the same stage with identical inputs or escalate to RECAL per wrapper policy.

### Plugin vs kernel

- **Kernel (non-optional in v0):** `SeedParse`, `LatticeSynthesis`, `PolicyBind`, `ManifestEmit`, `SpawnCommit`.
- **Plugin-eligible (optional modules):** post-lattice stylers, auxiliary field generators, **IntentAnnotate** when enabled—each registers **stage name + IO contract + version** at bootstrap; unknown stage names fail graph validation.

### Tasks

- [ ] Author schema stubs (IDL/psuedo-interface) for `ParsedSeed`, `DensityLattice`, `BoundPolicyContext`, `EntityManifest` publish records in the project spec folder (link targets TBD by ingest/organize).
- [ ] Add **graph validation** checklist: acyclic, topological order matches kernel expectations, semver bump on change.
- [ ] Wire **harness fixtures**: one golden path `seed → manifest_hash` with frozen vectors (ties to Phase 1.1.9 matrix style).

## Research integration

### Key takeaways

- Treat **stage outputs** as publish-once artifacts with **stable content hashes**; manifests are a **downstream read-only catalog** for spawn, not a mutable scratchpad.
- **Graph PCG** patterns (filter → transform → spawn) reinforce Genesis **StageGraph** as a DAG with explicit node contracts and versioned graph metadata.
- **Deterministic regeneration** is a first-class product requirement in mature PCG stacks—aligns with Phase 1 replay harness and sorted traversal rules.
- **ECS manifest** idioms favor **id → shared item → spawn command**; Genesis `EntityManifest` rows should carry **deterministic keys** (rule id, cell coord, stream id) before generational entity ids attach at commit.
- **Multi-stage terrain/foliage** examples justify **ordered stage enums** even when some stages are stubbed in v0.

### Decisions / constraints

- **Constraint:** Published `TOut` for each stage must record **`stage_version_id`** + **`output_hash`** in the ledger before any consumer reads (fail-closed on skew).
- **Constraint:** `manifest_hash` remains the chained function described in distilled-core (lattice + policy + ordering salt); external “manifest crate” patterns inform shape, not hash math.
- **Pending decisions:** Minimum stage set for v0 (seed parse vs lattice vs policy vs manifest-only smoke) and which nodes are **no-op stubs** vs **kernel-required**.

### Links

- [[Ingest/Agent-Research/phase-2-1-1-stage-io-manifest-research-2026-03-19-1930|Pre-deepen synthesis note]]
- [[Ingest/Agent-Research/phase-2-1-pipeline-seed-ecs-research-2026-03-19-1912|Phase 2.1 prior synthesis]]

### Sources

- [Source: Leafwing Manifest — GitHub](https://github.com/Leafwing-Studios/leafwing_manifest)
- [Source: ProcGen — deterministic regeneration](https://procgen.com/)
- [Source: Mastering Procedural Content Generation](https://www.decodesfuture.com/articles/mastering-procedural-content-generation)
- [Source: PCG Workflows That Scale (Unreal/Unity overview)](https://www.animaticsassetstore.com/2025/11/14/inside-unreal-and-unity-procedural-content-generation-workflows-that-scale/)
- [Source: Procedural Generation System in Godot](https://itch.io/blog/1322894/procedural-generation-system-in-godot)
