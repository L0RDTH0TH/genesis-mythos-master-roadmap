---
title: Phase 2.1.4 — Entity spawn manifest, density lattice & spawn policy
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1.4"
handoff_readiness: 90
links:
  - "[[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]]"
  - "[[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935]]"
  - "[[phase-2-1-1-stage-graph-and-per-stage-io-contracts-roadmap-2026-03-19-1930]]"
  - "[[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]]"
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
---

## Phase 2.1.4 — Entity spawn manifest, density lattice & spawn policy

> [!summary] TL;DR
> Specify **`ENTITY_SPAWN`**: consumes **`DensityLattice` + `SpawnPolicy`**, emits a **sorted `EntityManifest`** whose rows are stable under **normative `CellCoord` traversal** and **hierarchical RNG streams** (2.1.2). **`manifest_hash`** binds lattice hash, policy hash, and row ordering; only **terminal `ManifestEmit`** from 2.1.3 may feed **`SpawnCommit`**.

### Scope

- **Inputs:** immutable `DensityLattice` (from upstream stage), `SpawnPolicy` (per-entity-type radii, caps, layer masks, optional multi-radius bands).
- **Output:** `EntityManifest` — ordered table of spawn rows: `cell_coord`, `entity_type_id`, `pose` (position + deterministic orientation seed), `stream_id` used, `row_index` (monotonic in sort order).
- **Determinism:** Poisson / blue-noise style candidate generation is allowed only where **candidate order** is defined by **deterministic traversal** + **stream draws** (no wall-clock or thread schedule leakage).
- **Handoff gate note:** `handoff_readiness: 90` here is **slice-local**. **`advance-phase`** for Phase 2 still requires **rollup ≥ `min_handoff_conf` (93)** on the secondary closure artifact when authored — same pattern as D-013 for Phase 1.

### Normative manifest sort key

Stable sort before hash:

1. `CellCoord` lexicographic under project’s canonical space ordering (e.g. `(z, y, x)` or documented axis policy — must match 2.1.1 traversal token).
2. `entity_type_id` (integer or stable string table id).
3. `row_index` within cell (when multiple entities share a cell).

`manifest_hash := H(lattice_hash ‖ policy_hash ‖ canonical_serialized_rows*)`.

### Spawn policy layers

- **Multi-radius:** sparse vs dense entity classes use **different minimum separation radii**; grid cell size for acceleration must be derived from the **minimum radius** used in that policy pass (pattern from Poisson disk literature — see Research integration).
- **Caps:** `max_per_cell`, `max_per_type_global` enforced before sort; overflow is a **deterministic reject** with reason code (e.g. `SPAWN_CAP_EXCEEDED`).

### Preconditions (SpawnCommit)

- `SpawnCommit` MUST verify `manifest_hash` matches the **terminal** `ManifestEmit` record referenced by `published_output_ref` (2.1.3).
- No runtime entity creation from non-terminal or partial manifests.

### Tasks

- [ ] Add **`ENTITY_SPAWN` / `EntityManifest`** subsection to StageGraph IO manifest with sort key + hash tuple.
- [ ] Harness row: **two policies** (dense + sparse) same seed → identical `manifest_hash`; differ only `policy_hash` when policy bytes change.
- [ ] Cross-link **barrier** reason codes from 2.1.3 when manifest publish fails.

## Research integration

### Key takeaways

- Poisson-style placement uses **grid-accelerated** candidate search with **minimum radius** driving cell size — aligns with **SpawnPolicy** + **CellCoord** batches.
- **Multi-distribution** (dense grass, sparse trees) maps to **layered policies** over one lattice traversal if stream namespaces stay isolated (2.1.2).
- Reference engines (Unity/Godot samples) illustrate **algorithm shape** only; ledger + hash contracts remain authoritative.

### Decisions / constraints

- **Constraint:** `manifest_hash` includes **policy hash**; any tie-break or radius table change bumps policy version.
- **Constraint:** Row order is **not** “discovery order”; it is **sort key** order post-generation.
- **Pending decisions:** exact multi-cell entity footprint rules; rotation / scale streams vs pose stream.

### Links

- [[Ingest/Agent-Research/phase-2-1-4-entity-manifest-spawn-research-2026-03-19-2030|Pre-deepen synthesis note]]
- [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000|Async barrier parent]]
- [[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935|Intent / RNG]]

### Sources

- [Source: GameDev.net — Poisson disk sampling for entities](https://gamedev.net/blogs/entry/2270025-poisson-disk-sampling-for-random-entities-placement/)
- [Source: Rosetta — Sebastian Lague procedural placement](https://rosetta.to/u/sebastianlague/unity-procedural-object-placement-e01-poisson-disc-sampling)
