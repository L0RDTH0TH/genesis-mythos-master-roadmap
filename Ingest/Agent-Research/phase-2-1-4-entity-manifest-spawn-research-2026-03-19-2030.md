---
title: Pre-deepen research — Phase 2.1.4 entity spawn manifest & Poisson placement
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master, roadmap]
para-type: Resource
project-id: genesis-mythos-master
linked_phase: Phase-2-1-4
research_query: "deterministic procedural entity spawn manifest Poisson disk sampling ECS placement"
research_tools_used: [web_search]
agent-generated: true
---

# Pre-deepen research — Phase 2.1.4 (entity manifest / spawn)

Vault context: Phase 2.1 chain already defines **StageGraph**, **intent/RNG isolation**, and **ManifestEmit → SpawnCommit** barrier. This pass adds external patterns for **spatial spawn selection** (Poisson / blue-noise style placement) compatible with **deterministic traversal** and **sorted manifests**.

## Synthesis

Procedural placement pipelines commonly separate **candidate generation** (e.g. Poisson disk / dart throwing with grid acceleration) from **commit**: candidates are validated, sorted, and then emitted as a stable list or manifest. [Source: GameDev.net — Poisson disk sampling for entity placement](https://gamedev.net/blogs/entry/2270025-poisson-disk-sampling-for-random-entities-placement/) describes multi-radius distributions (dense grass vs sparse trees) — maps cleanly to **SpawnPolicy** layers over a **DensityLattice**. Engine tutorials (e.g. [Sebastian Lague — procedural placement overview](https://rosetta.to/u/sebastianlague/unity-procedural-object-placement-e01-poisson-disc-sampling)) stress **grid cell size** tied to minimum radius and **local neighborhood** checks — those are deterministic when **RNG stream + traversal order** are fixed (align with 2.1.2). Reference implementations exist for Unity/Godot ([Poisson disc Unity](https://github.com/imnota4/Poisson-disc-unity), [Godot Poisson Disk Sampler](https://github.com/Decapitated/Godot-Poisson-Disk-Sampler)) as patterns only — Genesis Mythos must keep **ledger-hashable** manifests, not engine-specific APIs.

**Do not duplicate:** StageGraph IO contracts (2.1.1), hierarchical RNG namespaces (2.1.2), async barrier + reconcile (2.1.3).

## Sources

- [Source: GameDev.net — Poisson disk sampling for random entities placement](https://gamedev.net/blogs/entry/2270025-poisson-disk-sampling-for-random-entities-placement/)
- [Source: Rosetta / Sebastian Lague — Unity procedural placement (Poisson disc)](https://rosetta.to/u/sebastianlague/unity-procedural-object-placement-e01-poisson-disc-sampling)
- [Source: GitHub — imnota4/Poisson-disc-unity](https://github.com/imnota4/Poisson-disc-unity)
- [Source: GitHub — Decapitated/Godot-Poisson-Disk-Sampler](https://github.com/Decapitated/Godot-Poisson-Disk-Sampler)

## Raw sources (vault)

- _(No raw fetch note this run; web_search snippets only.)_
