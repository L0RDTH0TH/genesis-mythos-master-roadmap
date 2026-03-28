---
title: Pre-deepen research — Phase 2.1.6 multi-cell footprint & hash closure
research_query: "ECS spatial grid multi-cell entity footprint deterministic manifest rows"
linked_phase: Phase-2-1-6
project_id: genesis-mythos-master
created: 2026-03-19
tags: [research, agent-research]
research_tools_used: [web_search]
agent-generated: true
---

# Phase 2.1.6 — multi-cell footprints, spatial indexing, deterministic row expansion

Vault context: Phase 2.1.4 freezes sorted **EntityManifest** rows and **manifest_hash**; Phase 2.1.5 binds **SpawnCommit** to terminal **ManifestEmit** with **spawn_row_stable_id** from manifest-stable fields only. This note informs **how multi-cell entities** map into that row model without breaking determinism — **ledger rules in project roadmap notes remain authoritative**.

## Synthesis

- **Multi-cell occupancy in grids:** Common practice is to register an entity in **every spatial partition cell** it overlaps (or maintain a secondary spatial structure). Tie-in: manifest expansion to **one row per occupied lattice cell** preserves a total order under the existing **CellCoord lex sort** from 2.1.4.
- **Spatial hashing + ECS:** Open spatial-hash implementations for ECS emphasize **range queries** and **multi-cell membership** for entities that span partition boundaries; deterministic **replay** still requires a **canonical enumeration order** independent of insertion order — aligns with **manifest sort key** discipline rather than runtime map iteration order.
- **Stable identity across rows:** For a single logical spawn spanning *N* cells, group rows with **`logical_spawn_group_id`** (manifest-stable, derived from seed + anchor + type + footprint spec hash) so **SpawnCommit** idempotency can ledger-hit **per row** while still treating the group as one user-visible spawn in harness assertions.

## Raw sources (vault)

- (none — web_search only this run)

## Terminology mapping (external patterns → Phase 2.1.6 contract)

| External concept | Phase 2.1.6 field / rule | Role |
| --- | --- | --- |
| Multi-cell spatial registration | one `ENTITY_SPAWN` row per occupied `CellCoord` | Keeps `manifest_hash` stable under sort-key rules |
| Canonical ordering | sort already defined in D-017 | Row expansion must occur **before** hash + sort |
| Grouped spawn | `logical_spawn_group_id` | Harness can aggregate fingerprints across rows |

## Sources

- [GitHub — Sylmerria/Spatial-Hashing (Unity ECS/DOTS spatial hashing)](https://github.com/Sylmerria/Spatial-Hashing)
- [Leetless — Spatial Hashing vs ECS](https://leetless.de/posts/spatial-hashing-vs-ecs/)
- [Stack Overflow — represent grid map data in Unity ECS](https://stackoverflow.com/questions/51905153/unity-how-to-represent-grid-map-data-in-ecs)
- [GameDev.net — spatial partitioning grid multi-cell entities](https://gamedev.net/forums/topic/711411-spatial-partitioning-grid-am-i-doing-it-right/)
- [GitHub — supahero1/hshg hierarchical spatial hash](https://github.com/supahero1/hshg)
