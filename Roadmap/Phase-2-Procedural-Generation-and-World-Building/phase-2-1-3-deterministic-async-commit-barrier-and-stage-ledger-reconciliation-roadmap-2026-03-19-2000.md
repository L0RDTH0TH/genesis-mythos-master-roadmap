---
title: Phase 2.1.3 — Deterministic async commit barrier & stage-ledger reconciliation
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1.3"
handoff_readiness: 91
links:
  - "[[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935]]"
  - "[[phase-2-1-1-stage-graph-and-per-stage-io-contracts-roadmap-2026-03-19-1930]]"
  - "[[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]]"
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
---

## Phase 2.1.3 — Deterministic async commit barrier & stage-ledger reconciliation

> [!summary] TL;DR
> Define the **single commit barrier** between **ManifestEmit → SpawnCommit** (and any future async stage shards): workers may compute **out-of-band**, but **only** the **ledger-published** `EntityManifest` + `manifest_hash` may feed spawn. Specify **reconciliation**, **ordering**, and **failure** events so Phase 1 replay semantics stay closed.

### Scope

- **Barrier semantics:** what “done” means for a stage when work is **async** (thread pool, job graph, networked workers): no consumer observes partial manifests.
- **Ledger tail:** append-only **stage completion records** with `inputs_hash`, `output_hash`, `stage_graph_version`, `ordering_key` (align with Phase 1.1.9 harness ordering tuple style).
- **Reconciliation:** merging worker partials into **one** deterministic bundle **before** publish (sort keys, stable tie-breakers, forbidden nondeterministic merges).
- **SpawnCommit gate:** `SpawnCommit` accepts **only** manifests whose publish record is **terminal** for `ManifestEmit` (no `stage_failed` on that attempt).

### Commit barrier contract (normative sketch)

| Field | Meaning |
| --- | --- |
| `barrier_id` | Deterministic id = `hash(stage_name ‖ attempt ‖ inputs_hash ‖ stage_graph_version)` |
| `partial_attempts[]` | Optional worker tickets; each carries `worker_nonce` **not** in hash path |
| `reconcile_plan_version` | Semver for merge algorithm; bump on any tie-break change |
| `published_output_ref` | Handle to immutable `EntityManifest` view post-barrier |

**Invariant:** `manifest_hash` is computed **only** on the **final reconciled** manifest bytes, after stable sort of rows (per 2.1.1 traversal token + 2.1.2 stream seal).

### Async without nondeterminism

- **Private scratch:** workers write to **ephemeral** buffers keyed by `barrier_id`; promotion to ledger requires **hash match** against coordinator’s expected `partial_hash` contract.
- **Ordering:** coordinator assigns **deterministic `shard_sequence`** from lattice traversal (e.g. `CellCoord` batches), never from scheduler timing.
- **Failure:** any shard failure emits `stage_failed.event` with `SHARD_RECONCILE_TIMEOUT`, `PARTIAL_HASH_MISMATCH`, etc.; barrier does **not** publish.

### Failure surfaces

- `BARRIER_RECONCILE_DIVERGENCE` — two valid-looking partials disagree under reconcile plan.
- `BARRIER_VERSION_SKEW` — worker used stale `reconcile_plan_version`.
- `MANIFEST_PUBLISH_RACE` — illegal second publish for same `barrier_id` (fail closed; ledger rejects).

### Tasks

- [ ] Add **barrier / reconcile** subsection to StageGraph spec with semver table.
- [ ] Harness: **two-shard** manifest emit with injected delay; prove **identical** `manifest_hash` vs single-threaded golden.
- [x] Link **SpawnCommit** Preconditions to `ManifestEmit` terminal publish id — see [[phase-2-1-4-entity-spawn-manifest-density-lattice-spawn-policy-roadmap-2026-03-19-2030|Phase 2.1.4]] **Preconditions (SpawnCommit)**.

## Research integration

### Key takeaways

- **Layered / staged** PCG patterns reinforce **immutable outputs** and **explicit dependencies**—our barrier is the publish gate on those outputs.
- **DAG-shaped** parallel systems (rendering analogy) stress **explicit deps**; StageGraph provides the DAG; ledger tail provides the **serialization point**.
- Async grass/terrain examples show **async around** synchronous cores—we keep **hash closure** on the synchronous publish path.

### Decisions / constraints

- **Constraint:** No `EntityManifest` visibility to `SpawnCommit` until barrier publishes **one** terminal record.
- **Constraint:** Reconcile plan changes require **semver bump** + harness matrix row.
- **Pending decisions:** exact `shard_sequence` derivation for non-rectangular domains; networked worker trust model (future phase).

### Links

- [[Ingest/Agent-Research/phase-2-1-3-async-commit-barrier-research-2026-03-19-2000|Pre-deepen synthesis note]]
- [[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935|Intent / RNG parent]]
- [[phase-2-1-1-stage-graph-and-per-stage-io-contracts-roadmap-2026-03-19-1930|Stage graph & IO]]

### Sources

- [Source: LayerProcGen](https://github.com/runevision/LayerProcGen)
- [Source: Godot rendering DAG](https://godotengine.org/article/rendering-acyclic-graph/)
- [Source: ProcGen](https://procgen.com/)
