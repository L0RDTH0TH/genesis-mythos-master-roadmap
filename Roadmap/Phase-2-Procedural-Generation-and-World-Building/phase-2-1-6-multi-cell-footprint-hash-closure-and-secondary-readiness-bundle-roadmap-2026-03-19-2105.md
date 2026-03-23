---
title: Phase 2.1.6 — Multi-cell footprint hash closure & Phase 2.1 secondary readiness bundle
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1.6"
handoff_readiness: 90
links:
  - "[[phase-2-1-5-spawn-commit-idempotent-entity-apply-replay-harness-roadmap-2026-03-19-2035]]"
  - "[[phase-2-1-4-entity-spawn-manifest-density-lattice-spawn-policy-roadmap-2026-03-19-2030]]"
  - "[[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]]"
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
---

## Phase 2.1.6 — Multi-cell footprint hash closure & secondary readiness bundle

> [!summary] TL;DR
> **Normative:** multi-cell entities expand to **one `ENTITY_SPAWN` manifest row per occupied `CellCoord`** before **sort + `manifest_hash`** (D-017). Rows that belong to one player-visible spawn share a manifest-stable **`logical_spawn_group_id`**. **`spawn_row_stable_id`** (2.1.5) remains per-row; **`SpawnCommit`** idempotency replays row-by-row in manifest order. This slice also defines the **Phase 2.1 secondary readiness bundle** (`G-P2.1-*`) that must pass before authoring a rollup closure note for **advance-phase** under `handoff_gate: true` / `min_handoff_conf: 93`.

### Scope

- **Inputs:** `EntityManifest` draft rows from 2.1.4 + footprint spec from `SpawnPolicy` (radius, shape mask, anchor cell).
- **Outputs:** Frozen rules for **footprint expansion → rows**, **`logical_spawn_group_id`** derivation, and **harness aggregation** expectations (group fingerprint vs per-row ledger hits).
- **Non-goals:** Changing D-016 barrier semantics or D-017 sort key; optional **anchor + bitmap** compression is explicitly **deferred** (documented as future optimization only).

### Normative footprint expansion (pre-hash)

1. Compute **occupied cells** = deterministic function `(anchor_cell, footprint_spec, lattice_hash)` — no runtime entity ids.
2. Emit **one manifest row per cell** with the same **`entity_type_id`**, **`stream_id`**, and shared **`logical_spawn_group_id`**.
3. **`row_index`** is **per-cell** within the group after stable sort of cells (lex `CellCoord`).
4. Run **global manifest sort** (D-017) then compute **`manifest_hash`**.

### `logical_spawn_group_id` (manifest-stable)

```
logical_spawn_group_id := H(stream_id ‖ manifest_policy_hash ‖ anchor_cell ‖ entity_type_id ‖ footprint_spec_hash ‖ spawn_batch_id)
```

- **Must not** include volatile runtime fields.
- **SpawnCommit** may aggregate **`applied_row_count`** for all rows sharing this id in one batch, but **ledger still records per-row** `spawn_row_stable_id` for replay granularity.

### Secondary readiness bundle (`G-P2.1-*`)

| Gate ID | Criterion | Primary evidence note |
| --- | --- | --- |
| G-P2.1-GRAPH | Stage graph + IO contracts bounded | [[phase-2-1-1-stage-graph-and-per-stage-io-contracts-roadmap-2026-03-19-1930]] |
| G-P2.1-INTENT | Intent stream + hierarchical RNG isolation | [[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935]] |
| G-P2.1-BARRIER | Terminal ManifestEmit + barrier reconciliation | [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]] |
| G-P2.1-MANIFEST | Sorted manifest + `manifest_hash` | [[phase-2-1-4-entity-spawn-manifest-density-lattice-spawn-policy-roadmap-2026-03-19-2030]] |
| G-P2.1-SPAWN | SpawnCommit idempotency + replay harness | [[phase-2-1-5-spawn-commit-idempotent-entity-apply-replay-harness-roadmap-2026-03-19-2035]] |
| G-P2.1-FOOTPRINT | Multi-cell expansion + group id + pre-hash ordering | **this note** |

**Rollup rule:** Phase 2.1 secondary closure artifact (future slice) must cite pass/fail for each row with **evidence link**; **`handoff_readiness ≥ 93`** on that rollup is required for **advance-phase** to Phase 2.2+ under current params — individual tertiaries may remain **90–92** slice-local.

### Tasks

- [ ] Implement footprint expansion in manifest builder; unit test: same seed → same row multiset → same `manifest_hash`.
- [ ] Extend harness: **group golden vector** = map `logical_spawn_group_id` → expected **set** of `spawn_row_stable_id` + **entity_fingerprint** rollup.
- [ ] Document deferred optimization: **single anchor row + external footprint blob** — **not v1** (would require new hash lane + semver bump).

## Research integration

### Key takeaways

- Multi-cell entities in grid/ECS contexts typically register **multiple spatial cells**; manifest-side equivalent is **multiple sorted rows** before hashing.
- Deterministic replay requires **canonical order** (already **CellCoord** sort) — footprint expansion must be **pure** w.r.t. that order.
- **Logical grouping** for UX/harness can be manifest-stable **`logical_spawn_group_id`** without changing per-row idempotency keys.

### Decisions / constraints

- **Adopted (D-019):** one row per occupied cell pre-sort; shared `logical_spawn_group_id` for harness aggregation.
- **Constraint:** footprint expansion runs **before** `manifest_hash`; no post-hash row injection.
- **Pending:** optional compact encoding (anchor + bitmap) reserved for **v2** with new `manifest_layout_semver`.

### Links

- [[Ingest/Agent-Research/phase-2-1-6-footprint-hash-closure-research-2026-03-19-2105|Pre-deepen synthesis note]]
- [[phase-2-1-5-spawn-commit-idempotent-entity-apply-replay-harness-roadmap-2026-03-19-2035|SpawnCommit parent]]
- [[phase-2-1-4-entity-spawn-manifest-density-lattice-spawn-policy-roadmap-2026-03-19-2030|Manifest parent]]

### Sources

- [Source: Spatial-Hashing ECS/DOTS (GitHub)](https://github.com/Sylmerria/Spatial-Hashing)
- [Source: Spatial Hashing vs ECS — Leetless](https://leetless.de/posts/spatial-hashing-vs-ecs/)
- [Source: Stack Overflow — grid map data in Unity ECS](https://stackoverflow.com/questions/51905153/unity-how-to-represent-grid-map-data-in-ecs)
