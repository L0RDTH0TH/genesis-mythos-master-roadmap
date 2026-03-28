---
title: Research — Phase 2.1 pipeline seed ECS (pre-deepen)
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master, roadmap]
para-type: Resource
project-id: genesis-mythos-master
linked_phase: Phase-2-1
research_query: "procedural world generation pipeline deterministic seed ECS entity spawn"
research_tools_used: [web_search]
agent-generated: true
research_escalations_used: 0
status: active
---

# Phase 2.1 — external grounding (pre-deepen)

Vault-first context: Phase 2 primary emphasizes seed-to-entities pipeline, intent hooks, and repeatable generation. Phase 1 closed deterministic replay, snapshots, and command/event contracts.

## Synthesis

Deterministic procedural pipelines typically fix a **seed** and a **stable stage graph** so each stage consumes immutable outputs from the prior stage (e.g. density fields → placement policies → spawn manifests). ECS-oriented runtimes treat **spawn** as authoritative component attachment under deterministic ordering; worker/main-thread splits are common for heavy generation while keeping **simulation tick** and **spawn commit** on deterministic boundaries.

Industry and reference material consistently recommends: (1) isolate generation in ordered stages with versioned inputs/outputs, (2) keep RNG streams **hierarchically split** per stage/subsystem to avoid cross-stage leakage, (3) treat entity spawn as a **transactional** step with idempotent keys when replay or resume is required—aligned with Genesis Phase 1 snapshot and replay contracts.

## Sources

- [Source: System Architecture | redblobgames/mapgen4 | DeepWiki](https://deepwiki.com/redblobgames/mapgen4/2-system-architecture)
- [Source: World Generation | Spawn Documentation](https://www.spawntools.ai/docs/core-concepts/world-generation)
- [Source: Venture — deterministic seed-based procedural generation (pkg.go.dev)](https://pkg.go.dev/github.com/opd-ai/venture)
- [Source: kimgoetzke/procedural-generation-2 (deterministic 2D world)](https://github.com/kimgoetzke/procedural-generation-2)
- [Source: Anatomy of the World — bevy_ecs_ldtk](https://trouv.github.io/bevy_ecs_ldtk/v0.10.0/explanation/anatomy-of-the-world.html)

## Raw sources (vault)

_No raw fetch note this run — web_search snippets only; eligible for future Raw-Index when URLs are fetched._

## Research integration (inject block)

```markdown
## Research integration

### Key takeaways

- Fix a **directed stage graph** (seed → lattice/policy → manifests → spawn) with immutable stage outputs and explicit stage version ids.
- Use **hierarchical RNG streams** keyed by stage + region + rule id so reordering within a stage does not poison downstream determinism.
- Prefer **main/worker split** only for CPU-heavy synthesis; commit spawn + authoritative components on the deterministic simulation thread (or behind an explicit fence lifted per Phase 1.1.8 semantics).
- Model **ECS spawn** as ordered commands with stable entity identity policy (generational ids + manifest rows) to align with replay harness expectations.
- Chunked/world-partition strategies should carry **deterministic traversal order** (e.g. sorted cell coords) when emitting manifests—matches distilled-core ENTITY_SPAWN / CellCoord themes.

### Decisions / constraints

- **Constraint:** Any async generation must reconcile through a **single commit barrier** that emits deterministic `manifest_hash` inputs (see distilled-core Phase 2.1.4 sketch).
- **Constraint:** Stage failures remain **replay events** with stable reason codes (Phase 1 D-004).
- **Pending decisions:** Exact stage enum for Genesis (terrain vs lore vs entity vs simulation bootstrap) and which stages are optional plugins vs core kernel.

### Links

- [[Ingest/Agent-Research/phase-2-1-pipeline-seed-ecs-research-2026-03-19-1912|This synthesis note]]
- [[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912|Phase 2.1 secondary roadmap]]

### Sources

- See **## Sources** above.
```
