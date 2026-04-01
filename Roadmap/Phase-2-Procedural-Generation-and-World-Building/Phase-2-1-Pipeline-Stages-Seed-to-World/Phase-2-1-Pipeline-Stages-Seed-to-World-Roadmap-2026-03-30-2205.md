---
title: Phase 2.1 — Pipeline stages from seed to world
roadmap-level: secondary
phase-number: 2
subphase-index: "1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 35
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

## Phase 2.1 — Pipeline stages from seed to world

This secondary slice defines the **stage pipeline** that turns a deterministic **seed bundle** (plus DM/player intent hooks) into **staged world deltas**. The output of this slice is intentionally *pre-commit*: it produces typed deltas, overlays, or overlays-ready structures while deferring authoritative world mutation until the agreed commit boundary.

## Conceptual waiver & safety invariants

- Conceptual track waiver (rollup / CI / HR): This project’s **design authority** on the **conceptual** track does **not** claim execution rollup, registry/CI closure, or HR-style proof rows; those are **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- Safety invariants (Phase 1 contract): use **seed snapshots + dry-run validation hooks** as the NL contract for safe boundaries; execution tooling, CI, and registry closure are explicitly out of scope for this conceptual slice.

## Scope

**In scope:**
- Stage list and **stage-to-stage ordering** for seed-to-world generation.
- Typed **inputs** (seed bundle, prior stage outputs, intent hooks) and **outputs** (staged deltas, validation artifacts, commit-ready overlays).
- Named **intent injection points** so downstream simulation/play can query hooks without re-parsing narrative.
- Determinism rules at the *pipeline spine* level (what must be stable across replay).

**Out of scope:**
- Concrete engine integrations (exact API calls, file formats, asset IDs, plugin manifests).
- Execution-track CI, performance budgets, and registry closure.
- Player-facing narrative text and lore storylines (kept as data/injection inputs, not hardcoded text).

## Behavior (natural language)

Actors: **systems** (pipeline runner, stage evaluators, validation gates), **DM** (regeneration requests + intent overrides), **players** (intent sources like lore preferences).  
Inputs: a **seed bundle identity**, DM/player intent hooks, and prior-stage outputs (typed).  
Outputs: **staged deltas** (what would change) plus validation artifacts (what to trust) and finally an agreed commit boundary token.

Ordering (canonical spine):
- Stage 0: seed expansion (create stable derived seeds / bundle sub-identities; no external calls).
- Stage 1: intent resolve (map DM/player intent into hook values for downstream stages).
- Stage 2: stage pipeline evaluation (seed->terrain->biomes->POIs->entities).
- Stage 3: simulation bootstrap packaging (prepare sim bootstrap inputs from generated entities/overlays).
- Stage 4: dry-run validation gate (reject before commit on invalid stage outputs).
- Stage 5: commit boundary (authoritative world mutation happens only after dry-run clears).

Regeneration semantics:
- Regeneration re-runs the pipeline stages using the same bundle identity for unchanged subcomponents, and different deterministic seeds only where the user intent or regeneration request requires it.
- Conflicting intents resolve via explicit hook priority rules; default behavior defers the *merge policy* to execution track.

## Interfaces

Upstream:
- Phase 2 primary defines the staged world-build story and intent hook vocabulary: generation never bypasses world-state commit APIs when mutating authoritative state.

Downstream:
- Tertiary notes under this secondary refine stage families (e.g. how terrain data is represented at conceptual level, how entity placement boundaries are validated) without re-defining the stage ordering.

Adjacent slices:
- Phase 2 primary provides the overarching “forge” narrative and the collaboration loop contract; this slice names stage boundaries and typed outputs so later work can attach interfaces without rework.

Outward guarantees:
- This slice guarantees deterministic stage ordering and stable hook naming at the **natural language interface** level.
- It guarantees *no partial commit* on pipeline-stage failure: failed validation yields empty staged outputs or blocked commit, never “half-mutated” world state.

## Edge cases

- Partial stage failure: when a stage produces invalid outputs, downstream stages receive empty typed outputs (no commit), and the user intent override remains isolated for replay.
- Nondeterminism leakage: any external APIs or clocks must be isolated to explicitly labeled stages; the default conceptual policy is “no hidden nondeterminism in the core spine.”
- Conflicting intents / merge policy: hook collisions are resolved by priority rules; the exact merge policy for execution remains execution-deferred.
- Hot reload / mid-campaign regeneration: regeneration requests must re-validate the dry-run gate before commit.

## Open questions

- Whether the minimum viable generation for vertical slice is strictly linear (single pass) or uses explicit **subgraph runs** for regeneration prefixes (deferred to tertiary / execution).
- Exact hook naming convention (topic-like vs path-like) for stable intent resolution across DM/player overrides (deferred to execution registry, but named at NL level here).

## Pseudo-code readiness

At this depth, readers can sketch **an ordered stage list** and **typed input/output contracts** without writing pseudo-code. Algorithm-shaped pseudo-code for individual stage bodies belongs in tertiary notes under this secondary (e.g. `1.1+` slice notes), not in the stage pipeline spine itself.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from staged world-build pipelines and deterministic generation practice.

## Risk register v0

| Risk | Mitigation (conceptual; execution may add CI/tooling) |
|------|--------------------------------------------------------|
| Stage ordering drift | Declare the canonical stage list; validate stage order changes as a breaking interface |
| Nondeterminism leaks into spine | Isolate any external entropy to labeled stages only |
| Intent hook collisions | Use stable hook naming + explicit priority rules; execution merge policy deferred |
| Partial commit after failure | Dry-run gate is a hard precondition for commit boundary |
| Scope creep into simulation | Routing rule: simulation logic stays in later phases after generation commits |

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

