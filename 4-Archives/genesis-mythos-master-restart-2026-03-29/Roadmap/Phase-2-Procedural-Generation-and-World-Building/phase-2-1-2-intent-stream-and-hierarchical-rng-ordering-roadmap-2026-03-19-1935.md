---
title: Phase 2.1.2 — Intent stream & hierarchical RNG ordering
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1.2"
handoff_readiness: 91
links:
  - "[[phase-2-1-1-stage-graph-and-per-stage-io-contracts-roadmap-2026-03-19-1930]]"
  - "[[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]]"
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
---

## Phase 2.1.2 — Intent stream & hierarchical RNG ordering

> [!summary] TL;DR
> Place **`IntentAnnotate`** in the v0 DAG with **cycle-safe attachment points**, define **intent bytes → validated intent view** contracts, and lock **hierarchical RNG stream allocation** so optional stages and skipped work cannot desynchronize mandatory publishes. Aligns Phase 2.1.1 traversal tokens with **per-stage stream namespaces** and Phase 1 replay semantics.

### Scope

- Resolve **where** `IntentAnnotate` may attach relative to `{ SeedParse, LatticeSynthesis, PolicyBind, ManifestEmit, SpawnCommit }` without breaking acyclicity or hash closure.
- Specify **intent stream IDs** vs **lattice/policy/manifest streams** (no cross-pollution when intent feature flag is off).
- Define **ordering invariants**: topological commit order, stream **creation** at stage entry, **seal** at publish, and ledger fields needed for harness parity.

### DAG attachment options (v0 decision space)

| Option | Insertion edge | Risk | When to prefer |
| --- | --- | --- | --- |
| A | `SeedParse → IntentAnnotate → LatticeSynthesis` | Intent influences lattice draws early | Narrative-first worlds |
| B | `PolicyBind → IntentAnnotate → ManifestEmit` | Late intent; manifest sort must include intent hash | Gameplay-first spawn tables |
| C | **Disabled** (flag off) | No extra edges | Smoke / kernel-only v0 |

**Default for v0 kernel path:** **Option C** unless PMG explicitly enables intent; compiler still validates graph with intent **removed** as unreachable when flag off.

When flag **on**, **start with Option A** only if golden vectors prove lattice hash stability; else prefer **Option B** to keep lattice synthesis deterministic on seed-only replays.

### Intent IO contract (sketch)

| Artifact | Producer | Consumer | Ledger fields |
| --- | --- | --- | --- |
| `IntentEnvelope` (bytes) | upstream tool / CLI | `IntentAnnotate` | `intent_hash`, `intent_schema_version` |
| `AnnotatedIntent` (view) | `IntentAnnotate` | `PolicyBind` or `ManifestEmit` (per option) | `annotated_intent_hash`, `intent_stream_id` |

**Invariant:** `IntentAnnotate` **must not** mutate `ParsedSeed` or `DensityLattice` in place; it publishes a **new handle** like other stages.

### Hierarchical RNG ordering

- **Namespace:** `rng_namespace := hash(stage_name ‖ stage_version_id ‖ region_id ‖ rule_id)` as in 2.1.1; add **`intent_segment`** token when intent enabled so intent draws are isolated.
- **Skip safety:** If a stage is optional and skipped, **do not instantiate** its streams; downstream stages **must not** branch RNG on “was skipped” unless the skip is itself a **ledger-published decision** (`stage_skipped.event` with reason).
- **Splittable / PCG-style streams:** External practice uses **distinct stream IDs** from one seed to avoid correlation; document compatibility with splittable generators for future C++ runtime ([Source: PCG streams](https://www.pcg-random.org/useful-features.html)).

### Failure surfaces

- `INTENT_SCHEMA_MISMATCH`, `INTENT_HASH_CHAIN_BREAK`, `INTENT_STREAM_COLLISION` — deterministic replay events; fail-closed on publish.
- Intent disabled + graph contains intent node → **compile error** (graph validator).

### Tasks

- [ ] Patch **StageGraph v0** diagram in spec with chosen option + semver bump.
- [ ] Add harness case: **intent off** vs **intent on** with identical `manifest_hash` on mandatory path when Option B holds.
- [ ] Document **stream seal** fields in publish record appendix (align with Phase 1 event taxonomy).

## Research integration

### Key takeaways

- **Independent streams per stage** prevent desynchronization when optional stages are skipped; align with Genesis sub-stream id policy.
- **Splittable / multi-stream PRNG** patterns support hierarchical pipelines without ad-hoc reseeding at each stage.
- **Intent** should publish **immutable handles** like other stages; no in-place mutation of lattice/seed views.

### Decisions / constraints

- **Constraint:** Optional stage skip must not change RNG draws in unrelated streams (testable via stream isolation matrix).
- **Constraint:** Graph remains a **DAG**; any intent attachment must pass cycle detection + semver bump.
- **Pending decisions:** Option A vs B for enabled intent; minimum schema for `IntentEnvelope` v0.

### Links

- [[Ingest/Agent-Research/phase-2-1-2-intent-rng-ordering-research-2026-03-19-1935|Pre-deepen synthesis note]]
- [[phase-2-1-1-stage-graph-and-per-stage-io-contracts-roadmap-2026-03-19-1930|Stage graph & IO parent]]

### Sources

- [Source: PCG — multiple streams](https://www.pcg-random.org/useful-features.html)
- [Source: Splittable PRNGs (Chalmers)](https://research.chalmers.se/publication/183348)
- [Source: SplitMix / splittable generators (OOPSLA)](https://gee.cs.oswego.edu/dl/papers/oopsla14.pdf)
