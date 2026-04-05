---
title: Phase 1 — Conceptual Foundation and Core Architecture
roadmap-level: primary
phase-number: 1
subphase-index: "0"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 72
phase1_primary_checklist: complete
handoff_readiness: 82
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[sandbox-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
---

## Phase 1 — Conceptual Foundation and Core Architecture

Establish the high-level blueprint and modular skeleton so world state, simulation, rendering, and input stay decoupled while preserving the master goal’s emphasis on immersion, collaboration, and extensibility. This phase sets interfaces for seeds, overrides, and lore injections and names the modularity seams that later work will deepen.

- [x] Core implementation task — Layering diagram + interface contracts (world state vs sim vs render vs input) → [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]
- [x] Core implementation task — Procedural generation graph skeleton (stages + intent injection points) → [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- [x] Glue / integration task — Safety invariants + dry-run validation hooks *(NL design authority in section below; tooling/CI closure **execution-deferred**)*

## Glue / integration — Safety invariants and dry-run validation hooks

This section **checklist-completes** the primary row **in place** (no **1.2.6** tertiary unless PMG expands scope). It binds **1.1** layering seams and **1.2** graph semantics into cross-cutting safety **before** any committed world replacement.

### Safety invariants (snapshot posture)

- **When snapshots apply:** (1) Before any **destructive** world replacement (full regen, major graph swap), capture a **world snapshot** sufficient to restore prior playable state (conceptual: opaque snapshot handle — concrete format **execution-deferred**). (2) On **DM major-change** intent (per PMG), snapshot before applying graph deltas that alter committed topology. (3) Optional **rolling checkpoints** between pipeline stages for coarse rollback — policy choice, not mandated at conceptual depth.
- **What must be preserved:** Seed bundle identity + graph definition version + manifest hash (see **1.2.5**) so replay and audit traces align; **1.2.4** replay contracts define whether restore is byte-identical or semantic-equivalent.
- **Failure semantics:** If snapshot cannot be taken, **abort** the destructive path before commit; surface **stage-level** failure (no partial world commit).

### Dry-run validation hooks

- **Dry-run path:** A **validation-only** execution produces an **interchange manifest** (or delta manifest) describing intended mutations **without** committing world state. **Pre-run static validation** (**1.2.5**) is the same class of gate: **reject before run** when the graph definition is invalid.
- **Hooks:** (1) **Graph-level** — topological order + stage boundary checks before execution. (2) **World-level** — schema/registry checks for outputs that would attach to world state. (3) **Policy-level** — DM/player intent merge (see **Open questions**) remains **TBD** where not explicit; dry-run does **not** silently choose merge policy.
- **Determinism alignment:** Dry-run and live execution share **deterministic semantics** (same seed, same bundle identity per **1.2.4**); divergence is a **bug class** for execution track.

### Integration with Phase 1 slices

- **Layering (1.1):** Commit pipeline + error boundaries (**1.1.1**, **1.1.4**) ensure a **single** commit boundary at the agreed seam — no layer sneaks partial commits mid-generation.
- **Graph (1.2):** Manifests and versioning (**1.2.5**) attach to dry-run; **1.2.2** subgraph semantics define **what** runs in a dry-run slice.

**Execution-deferred:** CI wiring, binary artifact hashes, performance budgets, automated rollback drills — **out of scope** for conceptual completion; resolved on **execution track** per dual-track contract.

## Scope

**In scope for this primary slice:** The conceptual contract for Phase 1 as a whole—what “foundation layer” means for the VTT generator: naming the four major layers (world state, simulation, rendering, input), the procedural generation graph as an ordered pipeline with explicit intent injection points, and the modularity seams (generation stages, rule hooks, event bus) that allow swapping implementations without rewriting the spine.

**Explicitly out of scope here:** Concrete engine APIs, file formats, network protocols, plugin ABI versioning, and execution-track proof obligations (tests, CI hooks, performance budgets). Those belong to execution-track notes and later phases. This note is **design authority** for alignment, not implementation closure.

## Behavior (natural language)

Actors: **systems** (simulation tick, render frame, input dispatch), **DM** (overrides, regeneration requests), **players** (lore intents, actions). Inputs: seeds, DM/player intents, prior world snapshots. Outputs: deterministic or staged world mutations, renderable state, logged events. Ordering: **input → simulation → world state commit → render read**; generation runs **offline or on-demand** as a pipeline before live play, with hooks for mid-campaign regeneration that respect the master goal’s “major changes require intentional re-generation.”

## Interfaces

- **Adjacent slices:** Phase 2 consumes the generation graph skeleton and intent injection points; Phase 4 consumes camera/control abstractions; Phase 5 consumes rule-hook seams. Inward, Phase 1 depends on Phase 0 anchors (PMG, state files) only.
- **Outward guarantees:** (1) Documented layer boundaries so no layer imports another’s concrete types. (2) Named extension surfaces: event bus topics, rule hook registry, generation stage list. (3) Safety hooks: snapshot + dry-run before destructive world replacement.

## Edge cases

- **Partial generation failure:** Pipeline must surface stage-level failure without corrupting committed world state; dry-run path validates before commit.
- **Conflicting intents / merge policy:** See **[[#Execution-track deferred decisions (stable IDs)]]** — **GMM-EXEC-TBD-001**.
- **Hot reload:** Optional module swap at runtime; if unsupported at launch, defer with explicit “restart required” contract.

## Open questions

- **Graph topology vs cycles:** See **[[#Execution-track deferred decisions (stable IDs)]]** — **GMM-EXEC-TBD-002**. (Default assumption until decided: DAG with explicit feedback edges.)

## Execution-track deferred decisions (stable IDs)

| ID | Topic | Default / pointer |
| --- | --- | --- |
| **GMM-EXEC-TBD-001** | DM vs player lore merge (last-writer vs explicit merge) on the same entity | Execution-track plugin spec; no silent policy in dry-run (**Glue** section). |
| **GMM-EXEC-TBD-002** | Strict DAG vs controlled cycles for iterative refinement | Default: DAG + explicit feedback edges; formal choice deferred. |

## Pseudo-code readiness

At this conceptual depth, readers can sketch **without** full implementation: pseudo-code is **not** required in this primary note; the **intent** is that later secondary/tertiary notes under Phase 1 will add interface sketches and algorithm-shaped bullets. **Execution-deferred:** HR/rollup registry closure artifacts are **out of scope** for conceptual completion of this slice.

### Progress semantics (frontmatter `progress`)

`progress` is **0–100** for this note’s **conceptual slice depth** (not execution CI %): **0** = stub only; **~10** = primary NL checklist + rollup alignment started; **50+** = secondaries substantially drafted; **100** = Phase 1 primary + agreed secondaries ready for execution handoff (still not execution CI closure). **`phase1_primary_checklist`** in frontmatter is **`complete`** when all three primary rows (1.1, 1.2, glue) are checklist-done; **`progress: 72`** = mid–late conceptual drafting (secondaries + glue NL done; execution proof still deferred). Glue NL finalized **2026-03-30** (`resume-gmm-deepen-glue-primary-20260330T201500Z`).

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
