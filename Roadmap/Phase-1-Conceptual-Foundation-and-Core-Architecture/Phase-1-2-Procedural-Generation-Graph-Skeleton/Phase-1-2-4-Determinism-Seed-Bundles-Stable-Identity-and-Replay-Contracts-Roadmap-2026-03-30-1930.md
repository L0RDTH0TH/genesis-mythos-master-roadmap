---
title: Phase 1.2.4 — Determinism, seed bundles, stable identity, and replay contracts
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.4"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 78
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]"
  - "[[Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]"
  - "[[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
  - "[[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.2.4 — Determinism, seed bundles, stable identity, and replay contracts

This tertiary slice pins **reproducibility** for the procedural graph: how **seed bundles** flow from session/world down to **node-level derived seeds**, how **stable node identity** stays addressable across saves and tooling, and what **replay** means for debugging (dry-run vs committed runs) — without choosing serialization formats (**execution-deferred**).

## Scope

**In scope:** Hierarchical **seed derivation** (world → subgraph → node); **stable logical IDs** for nodes independent of evaluation order; **determinism contract** for spine stages (same inputs + seeds ⇒ same typed outputs modulo explicitly labeled nondeterministic stages); **replay intent** (what to log for a minimal repro). **Out of scope:** PRNG algorithms, fixed-point math, disk formats, network sync. **Execution-deferred:** golden tests, hash-stable serialization, CI nondeterminism lint.

## Behavior (natural language)

- A **seed bundle** carries at least: **session/world root**, optional **per-subgraph salt** (from **1.2.2** subgraph selection), and **per-node derived seeds** computed from parent outputs + local salt + node kind (from **1.2.1**).
- **Stable identity:** Each node has a **logical key** (phase graph path + semantic name or registry id) used in docs and **1.2.3** family tags; **evaluation order** does not rename nodes—tie-break rules from **1.2.2** only affect scheduling, not identity.
- **Determinism:** For stages marked **deterministic spine**, implementations must not read clocks or unlabeled external IO; **nondeterministic** stages (e.g. optional cloud fetch) must be **explicitly tagged** and excluded from default replay or must snapshot inputs (**execution-deferred** capture).
- **Replay:** **Dry-run** replays use the same seed bundle + graph snapshot of inputs; **committed** runs additionally require **commit-family** ordering from **1.2.3** to match recorded validation outcomes.

## Interfaces

- **Upstream (1.2.1):** Node kinds and edge types constrain which inputs participate in seed derivation (only declared dependency outputs + declared seed fields).
- **Upstream (1.2.2):** Subgraph closure defines which nodes receive bundle fragments; parallel wave order does not change derived seeds—only **dataflow** does.
- **Upstream (1.2.3):** **Commit** vs **structure** families affect what “replay equivalence” means (commit stages may record validation digests).
- **Downstream ([[Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]] / Phase 2):** **Versioning**, **interchange manifests**, and **pre-run validation** bind determinism to tool exchange; **registry IDs**, hashing, and capture formats for CI remain **Phase 2 / execution-deferred**.

## Edge cases

- **Floating-point outputs:** Conceptual contract: either **avoid** fp in cross-node contracts or declare **tolerance buckets** per output type (**execution-deferred** numerics).
- **Optional stages:** Skipped nodes still have **derived seeds** for identity stability even if execution is skipped (so reruns do not reshuffle downstream salts).
- **Feedback / macro-pass (1.2):** Second-pass stages get **new** derived seeds from updated parent outputs—document **pass id** in bundle (**execution-deferred** detail).

## Open questions

- Minimum **replay artifact** for vertical slice (seed bundle only vs bundle + selected stage outputs) — **PMG** when Phase 2 scopes MVP.
- Whether **DM overrides** participate in seed derivation or attach as **post-seed modifiers** (affects auditability).

## Pseudo-code readiness

Readers can sketch **seed derivation chains** (`derive(parent_seed, node_kind, local_salt)`) and **identity tables** (logical key → stable id). No engine code.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from deterministic simulation, seeded noise, and reproducible build graphs.
