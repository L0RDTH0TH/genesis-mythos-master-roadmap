---
title: Phase 2.1 — Stage pipeline skeleton (seed → entity contracts)
roadmap-level: secondary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1"
handoff_readiness: 88
links:
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
---

## Phase 2.1 — Stage pipeline skeleton (seed → entity contracts)

Establish the **first executable slice** of Phase 2: a ordered **generation stage pipeline** from parsed seed metadata through **spawn-ready manifests**, without yet requiring full gameplay simulation. This secondary aligns the Phase 2 primary checklist item *“Implement stage pipeline skeleton (seed to entities)”* with Phase 1 determinism, replay, and snapshot invariants.

### Objectives

- [ ] Define the **stage graph** (nodes, edges, allowed branch points) from `SeedEnvelope` → `DensityLattice` / policy inputs → `EntityManifest` draft.
- [ ] Specify **per-stage IO contracts**: immutable input handles, output artifacts, and `stage_version_id` + `manifest_hash` propagation rules (forward reference to Phase 2.1.4 distilled-core bullet).
- [ ] Wire **deterministic ordering** for manifest emission (sorted traversal keys; RNG stream allocation per stage/rule).
- [ ] Declare **failure surfaces** as deterministic replay events (reason codes, no silent partial commits).
- [ ] Identify **plugin insertion points** vs kernel stages (which stages are optional modules registered at bootstrap).

### Contract sketch (v0)

```text
interface IGenerationStage<TIn, TOut> {
  name: StageName;
  run(ctx: GenerationContext, input: TIn) -> StageResult<TOut>;
}
Invariant: TOut is immutable once published; ctx carries seed_hash, ordered stage ledger, and stream-scoped RNG handles.
```

```text
type StageGraph = { nodes: StageName[]; edges: [StageName, StageName][]; version: string };
Invariant: graph is acyclic for v0; cycles require explicit RECAL + wrapper approval.
```

### Open questions (for tertiary breakdown)

- Where does **intent parser** hook first—pre-lattice, post-lattice, or post-manifest (affects Phase 2 primary “Integrate intent parser”)?
- Do we require **multi-threaded generation** in v0 or a single-threaded skeleton with worker hooks stubbed?

## Research integration

### Key takeaways

- Fix a **directed stage graph** (seed → lattice/policy → manifests → spawn) with immutable stage outputs and explicit stage version ids.
- Use **hierarchical RNG streams** keyed by stage + region + rule id so reordering within a stage does not poison downstream determinism.
- Prefer **main/worker split** only for CPU-heavy synthesis; commit spawn + authoritative components on the deterministic simulation thread (or behind an explicit fence lifted per Phase 1.1.8 semantics).
- Model **ECS spawn** as ordered commands with stable entity identity policy (generational ids + manifest rows) to align with replay harness expectations.
- Chunked/world-partition strategies should carry **deterministic traversal order** (e.g. sorted cell coords) when emitting manifests.

### Decisions / constraints

- **Constraint:** Any async generation must reconcile through a **single commit barrier** that emits deterministic `manifest_hash` inputs (see distilled-core Phase 2.1.4 sketch).
- **Constraint:** Stage failures remain **replay events** with stable reason codes (Phase 1 D-004).
- **Pending decisions:** Exact stage enum for Genesis (terrain vs lore vs entity vs simulation bootstrap) and which stages are optional plugins vs core kernel.

### Links

- [[Ingest/Agent-Research/phase-2-1-pipeline-seed-ecs-research-2026-03-19-1912|Pre-deepen synthesis note]]

### Sources

- [Source: System Architecture | redblobgames/mapgen4 | DeepWiki](https://deepwiki.com/redblobgames/mapgen4/2-system-architecture)
- [Source: World Generation | Spawn Documentation](https://www.spawntools.ai/docs/core-concepts/world-generation)
- [Source: Venture — deterministic seed-based procedural generation](https://pkg.go.dev/github.com/opd-ai/venture)
- [Source: kimgoetzke/procedural-generation-2](https://github.com/kimgoetzke/procedural-generation-2)
- [Source: Anatomy of the World — bevy_ecs_ldtk](https://trouv.github.io/bevy_ecs_ldtk/v0.10.0/explanation/anatomy-of-the-world.html)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
