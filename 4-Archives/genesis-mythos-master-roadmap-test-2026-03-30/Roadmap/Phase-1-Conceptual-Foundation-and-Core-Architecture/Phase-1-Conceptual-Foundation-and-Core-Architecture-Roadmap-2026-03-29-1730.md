---
title: Phase 1 — Conceptual Foundation and Core Architecture
roadmap-level: primary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-29-1730]]"
handoff_readiness: 84
handoff_gaps:
  - "Cursor **1.2** (snapshots/dry-run secondary) deepened 2026-03-29; next: optional **1.2.x** tertiaries or reconcile Phase 1 primary checklist vs MOC; execution-deferred per D-027"
---

## Phase 1 — Conceptual Foundation and Core Architecture

Define key abstractions separating world state, simulation, rendering, and input; outline the procedural generation graph and intent population pipeline with clear interfaces for seeds, overrides, and lore; identify modularity seams (generation stages, rule hooks, event bus); prototype safety invariants such as seed snapshots and dry-run validation so later phases inherit a disciplined iteration loop.

### Scope

This phase covers the **conceptual** architecture for how the product separates concerns (state, simulation, presentation, input), how procedural generation and intent flow through staged contracts, and where modules can be swapped without picking an engine or language (**D-027**). It does **not** select a runtime stack, define shipping CI jobs, or specify renderer APIs—those belong to execution track and later phases.

### Behavior

**Actors:** designers/authors (seeds, overrides, lore packs), the generation pipeline (stages consuming seeds and emitting world artifacts), the simulation loop (advancing authoritative state), presentation adapters (read-only views of state), and input routing (commands → validated intents). **Ordering:** seed + manifest load → generation graph stages (deterministic where required) → commitable snapshot of generated state → simulation ticks that consume the same state model → render/read models derived from state (no feedback that mutates sim without an intent path). **Outputs:** versioned generation manifests, replayable state checkpoints, and explicit hooks for intent resolution (reputation, events, environment) documented as contracts in words.

### Interfaces

**Inward:** Phase 1 expects from [[Genesis-mythos-master-goal]] a stable product vision and non-goals; from [[distilled-core]] the stack-agnostic decision corpus. **Outward:** Phase 1 guarantees documented stage boundaries for generation, a clear intent→hook surface, and modularity seams (generation stages, rule hooks, event bus) so Phase 2+ can attach algorithms without rewriting this skeleton. **Peer secondaries** **1.1** (layer seams) and **1.2** (snapshots / dry-run) sit directly under this primary folder; each is `roadmap-level: secondary` with `subphase-index` `1.1` and `1.2`.

### Edge cases

Ambiguous or conflicting seeds/overrides must be detected at generation commit time (dry-run or validation stage) rather than silently corrupting state. Partial generation failure should leave no half-committed authoritative state (all-or-nothing or explicit rollback contract). **TBD on execution track:** exact error taxonomy and user-facing diagnostics.

### Open questions

- Granularity of “intent” vs raw input events for multi-modal clients (deferred until perspective/control phases).
- Whether lore packs are validated in-band with generation or as a pre-flight plugin chain (**TBD**; default: pre-flight contract).

### Pseudo-code readiness

A reader can sketch modules such as `LoadSeed()`, `RunGenerationStage(n, in_manifest, out_artifacts)`, `ValidateCommit(snapshot)`, and `SimulationTick(state, intents)` without guessing the core ordering or authority boundaries. Detailed signatures and engine bindings are explicitly out of scope here (**execution track**).

- [x] Document layer boundaries and dependency direction (sim vs render vs input). — **Covered in secondary [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]]**
- [x] Specify generation graph stage contracts and intent resolver touchpoints. — **Same secondary + tertiaries 1.1.1 / 1.1.2**
- [x] List replaceability seams with minimal interface sketches (no engine lock-in). — **[[Phase-1-1-1-Replaceability-Seams-and-Hook-Surface-Roadmap-2026-03-29-1905]]**
- [x] Define snapshot + dry-run validation flow for generation commits. — **[[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]]**

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
