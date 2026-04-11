---
title: Phase 1.2.4 (Execution) — Determinism, seed bundles, stable identity, and replay contracts
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.4"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]"
execution_mirror_of: "Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930"
---

# Phase 1.2.4 (Execution) — Determinism, seed bundles, stable identity, and replay contracts

Execution remint for **tertiary 1.2.4** on the parallel spine. Binds conceptual **seed bundles**, **stable logical identity**, **determinism contracts** for spine stages, and **replay** semantics (dry-run vs committed) to lane-neutral registry sketches, with **Godot stable** **`RandomNumberGenerator`** / global **`randomize`** verbatim anchors as **hosting metaphors** for seeded RNG state — **not** a claim that proc-gen nodes are Godot `RandomNumberGenerator` instances. **`missing_roll_up_gates`**, golden/replay **CI**, hash-stable capture, and rollup **verdict closure** remain **execution-deferred** per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** — **not** claimed closed in-doc.

Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]] · Prior tertiary: [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-04-12-0015]] · Decisions: [[../../../decisions-log]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Hierarchical seed derivation | Conceptual 1.2.4 NL | `SeedBundle` carries world root + per-subgraph salt + per-node derived seeds from **1.2.1** kinds + **1.2.2** closure | Table: every `StageId` has derived seed row |
| Stable logical identity | Conceptual stable key | `logical_key = f(graph_path, semantic_name \| registry_id)`; **1.2.3** family tags orthogonal to scheduling order | Lint: no rename on tie-break / wave order alone |
| Determinism vs nondeterminism | Spine contract | `deterministic_spine` bit forbids clocks / unlabeled IO; nondeterministic stages tagged + excluded from default replay or input-snapshotted | Policy matrix row |
| Replay equivalence | **1.2.3** commit vs structure | Dry-run replay = same bundle + input snapshot; committed replay adds **commit-family** ordering + validation digests | Replay checklist stub |
| Godot hosting metaphor | Seeded RNG docs | **RandomNumberGenerator** `seed` / `randomize()` quotes justify *separate RNG streams* and *explicit seeding* — cites below | Verbatim citations block |

## Scope

- **In:** Lane-neutral `derive_seed`, `stable_id_for`, `replay_bundle_fingerprint` pseudocode; nondeterminism tagging table; dry-run vs committed replay rows aligned to **1.2.2** subgraph + **1.2.3** commit ordering.
- **Out:** Golden test hashes, disk serialization, network sync, CI run IDs, or claims that **`missing_roll_up_gates`** / rollup HR are satisfied.

## Lane-neutral seed bundle + identity (sketch)

```text
type SeedBundle = {
  world_root: u64,
  subgraph_salts: Map<SubgraphId, u64>,
  node_derived: Map<StageId, u64>,
  pass_id: int   # macro-pass / feedback from 1.2.2
}

function derive_seed(parent: u64, node_kind: NodeKind, local_salt: u64, pass_id: int) -> u64:
  # Conceptual: mix only declared inputs (1.2.1) + salts — not evaluation order
  return mix(parent, enum_code(node_kind), local_salt, pass_id)

function stable_id_for(logical_key: string, bundle_epoch: int) -> StableId:
  return StableId(hash_stable(logical_key), bundle_epoch)
```

**Skipped optional stages:** conceptual rule — still allocate **derived seed slot** so downstream salts do not reshuffle when a stage is skipped.

## Determinism + nondeterminism policy

| Class | Allowed inputs | Blocked without tag |
| --- | --- | --- |
| Deterministic spine | Declared deps + seed fields only | Wall clock, unlabeled HTTP |
| Nondeterministic (explicit) | Tagged in graph manifest | Included in default “strict replay” |

## Replay modes

- **Dry-run replay:** Same `SeedBundle` + frozen input snapshot of **1.2.1** outputs feeding each stage (per **1.2.2** closure).
- **Committed replay:** Adds **commit-family** ordering constraints and recorded validation digests from **1.2.3** — execution-deferred capture format.

## Godot lane (A) — verbatim anchors (stable docs)

**Explicit seeding for an RNG stream** — `RandomNumberGenerator` documents the `seed` property used to initialize state (metaphor: *per-pipeline or per-subgraph RNG stream*, not necessarily one object per stage):

> The seed used by this **RandomNumberGenerator** instance.

Source: [RandomNumberGenerator — seed — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html#class-randomnumbergenerator-property-seed)

**Re-initializing RNG from a time-based seed** — instance `randomize()` (contrast: global `randomize` below) documents a time-based seed; use as **anti-pattern callout** for proc-gen spine (prefer explicit bundle seeds, not time):

> Sets up a time-based random seed for this **RandomNumberGenerator** instance.

Source: [RandomNumberGenerator — randomize — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html#class-randomnumbergenerator-method-randomize)

**Global baseline random seed** — `@GlobalScope` `randomize()` sets the **global** seed from time; execution contract treats **explicit bundles** as authoritative over implicit global seed for reproducible graphs:

> Randomizes the **global** random number generator's seed.

Source: [@GlobalScope — randomize — Godot Engine stable](https://docs.godotengine.org/en/stable/classes/class_@globalscope.html#class-globalscope-method-randomize)

**Binding:** Lane-neutral kernel remains authoritative; Godot quotes justify **explicit seed streams** and **avoiding implicit global randomize** for reproducible tooling — **not** that each graph node owns a Godot `RandomNumberGenerator`.

## Sandbox lane (B) — comparand

| Element | B-lane stand-in |
| --- | --- |
| Seeded stream | `std::mt19937_64` per bundle fragment + explicit `seed()` |
| Identity | Stable string key → `uint64_t` id via FNV-style mix (documented) |
| Replay | Capture stdin vector + seed tuple — no global `rand()` |

## Acceptance criteria

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-1.2.4-A | Seed bundle + derive sketch documented | Sections + pseudocode | Met |
| AC-1.2.4-B | Stable identity vs scheduling order called out | `stable_id_for` + lint note | Met |
| AC-1.2.4-C | Godot verbatim citations present (`seed`, `randomize` x2) | Blockquotes + stable URLs | Met |
| AC-1.2.4-D | Rollup / CI / replay capture closure **not** claimed | Deferral callout | Met |

## Roll-up / CI / registry IDs (explicit deferral)

Open **`GMM-2.4.5-*`**, graph **`missing_roll_up_gates`**, golden replay **CI**, and rollup **verdict closure** remain **execution-deferred** until real **CI run IDs** and verdict tables land — per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**.

## Tasks

1. - [ ] Implement or document `derive_seed` / `SeedBundle` shape aligned to **1.2.1** node kinds + **1.2.2** subgraph ids.
2. - [ ] Implement or document `stable_id_for` + lint rule: no identity rename from wave/tie-break alone.
3. - [ ] Tag nondeterministic stages in graph manifest + replay exclusion / snapshot policy.
4. - [ ] Define dry-run vs committed replay rows referencing **1.2.3** commit ordering.
5. - [ ] Keep Godot RNG block strictly **metaphor + contract** (no claim that stages wrap Godot RNG objects).
6. - [ ] Maintain B-lane comparand parity for seeded STL streams.

## Test plan (stub — CI deferred)

| Check | Signal / fixture | Expected | Status |
| --- | --- | --- | --- |
| Seed derivation stability | Same bundle + graph | Same derived map | **PENDING** (execution-deferred CI) |
| Identity stability | Re-run schedule-only change | Stable ids unchanged | **PENDING** (execution-deferred CI) |
| Nondeterminism gate | Tagged stage in replay | Excluded or snapshotted | **PENDING** (execution-deferred CI) |

## Related

- Next tertiary (conceptual tree): [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]
- Execution mint **1.2.5** (parallel spine): [[Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-04-12-0215]]
- Versioning slice **1.2.5** execution deepen completed **2026-04-12**; next structural step: **Phase 1 primary** glue / safety + dry-run on [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]].
