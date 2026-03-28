---
title: Research — Phase 2.1.1 stage IO & manifest patterns (pre-deepen)
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master, roadmap]
para-type: Resource
project-id: genesis-mythos-master
linked_phase: Phase-2-1-1
research_query: "ECS manifest spawn pipeline stage graph PCG deterministic"
research_tools_used: [web_search]
agent-generated: true
research_escalations_used: 0
status: active
---

# Phase 2.1.1 — external grounding (pre-deepen)

Focus: **per-stage IO contracts**, **read-only manifest → spawn** patterns, and **graph-structured PCG** references to tighten Genesis stage graph + `manifest_hash` propagation without contradicting Phase 1 replay.

## Synthesis

Graph-based PCG (e.g. Unreal PCG) composes **filter/transform/spawn** nodes over structured point sets; production systems stress **deterministic regeneration from seeds** for QA and networked sims. ECS-facing manifest approaches (e.g. Bevy ecosystem “manifest” crates) separate **stable ids**, **shared item definitions**, and **serialization-friendly raw manifests** so runtime spawn clones from an immutable catalog—matching Genesis’s “immutable `TOut` publish” invariant.

For Genesis, map external patterns to: **StageGraph version string** + **acyclic v0** rule; **stage ledger** entries carrying `stage_version_id` and input/output **content hashes**; **manifest rows** as the spawn-facing projection of the last generation stage, consumed by `ENTITY_SPAWN` per distilled-core Phase 2.1.4.

## Sources

- [Source: Leafwing Manifest — GitHub](https://github.com/Leafwing-Studios/leafwing_manifest)
- [Source: ProcGen — deterministic regeneration](https://procgen.com/)
- [Source: Mastering Procedural Content Generation — decodesfuture](https://www.decodesfuture.com/articles/mastering-procedural-content-generation)
- [Source: Procedural Content Generation Workflows (Unreal/Unity overview)](https://www.animaticsassetstore.com/2025/11/14/inside-unreal-and-unity-procedural-content-generation-workflows-that-scale/)
- [Source: Procedural Generation System in Godot (multi-stage pipeline)](https://itch.io/blog/1322894/procedural-generation-system-in-godot)

## Raw sources (vault)

_Web snippets only this run; no Raw-Index rows._

## Research integration (inject block)

```markdown
## Research integration

### Key takeaways

- Treat **stage outputs** as publish-once artifacts with **stable content hashes**; manifests are a **downstream read-only catalog** for spawn, not a mutable scratchpad.
- **Graph PCG** patterns (filter → transform → spawn) reinforce Genesis **StageGraph** as a DAG with explicit node contracts and versioned graph metadata.
- **Deterministic regeneration** is a first-class product requirement in mature PCG stacks—aligns with Phase 1 replay harness and sorted traversal rules.
- **ECS manifest** idioms favor **id → shared item → spawn command**; Genesis `EntityManifest` rows should carry **deterministic keys** (rule id, cell coord, stream id) before generational entity ids attach at commit.
- **Multi-stage terrain/foliage** examples (Godot blog) justify **ordered stage enums** even when some stages are stubbed in v0.

### Decisions / constraints

- **Constraint:** Published `TOut` for each stage must record **`stage_version_id`** + **`output_hash`** in the ledger before any consumer reads (fail-closed on skew).
- **Constraint:** `manifest_hash` remains the chained function described in distilled-core (lattice + policy + ordering salt); external “manifest crate” patterns inform shape, not hash math.
- **Pending decisions:** Minimum stage set for v0 (seed parse vs lattice vs policy vs manifest-only smoke) and which nodes are **no-op stubs** vs **kernel-required**.

### Links

- [[Ingest/Agent-Research/phase-2-1-1-stage-io-manifest-research-2026-03-19-1930|This synthesis note]]
- [[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912|Phase 2.1 secondary roadmap]]

### Sources

- See **## Sources** above.
```
