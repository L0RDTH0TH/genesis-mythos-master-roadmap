---
title: Phase 1.2.5 — Graph versioning, interchange manifests, and pre-run validation
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.5"
project-id: genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 77
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]"
  - "[[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.2.5 — Graph versioning, interchange manifests, and pre-run validation

This tertiary slice closes the **1.2** procedural-graph tertiary chain (five slices, mirroring **1.1**) by defining how **graph definitions evolve**, how **fragments are exchanged** between tools or sessions, and what **static validation** runs **before** execution — bridging **determinism/replay (1.2.4)** and Phase 2 **registry/serialization** work without picking file formats here.

## Scope

**In scope:** **Compatibility/version** labels for graph shapes (major/minor semantics at NL level); **interchange manifest** (what travels with a graph fragment: node kinds, edge kinds, hook names, seed-bundle references per **1.2.4**); **pre-run validation hooks** (acyclicity, declared-input satisfaction, hook resolution, family/tag consistency with **1.2.3**) as **design-time or dry-run** obligations. **Out of scope:** Concrete file extensions, hashing, CI gates, plugin ABI. **Execution-deferred:** schema diff tools, migration scripts, registry-backed closure proofs.

## Behavior (natural language)

- **Versioning:** Each published graph definition carries a **schema generation** (breaking vs additive) so tools can **refuse** or **adapt** mixes of old/new stage descriptions; optional **compatibility matrix** (which node kinds interoperate across generations) stays **documentation-first** until execution registry exists.
- **Interchange manifest:** Bundles **minimal** metadata to reconstruct evaluation intent: subgraph closure from **1.2.2**, **seed bundle** shape from **1.2.4**, **stage family** tags from **1.2.3**, and **injection hook** identifiers from **1.2** secondary — enough for another tool to **validate** without executing.
- **Pre-run validation:** Before any **committed** run, a **static pass** checks: DAG (no undeclared cycles), **topological feasibility**, **type-shaped edges** per **1.2.1**, **hook targets** resolve to declared nodes, and **nondeterministic** stages are **labeled** per **1.2.4**. Failures surface as **blocking diagnostics**, not silent skips.

## Interfaces

- **Upstream (1.2.4):** Seed bundles and replay intent inform what the manifest must **preserve** for equivalence classes.
- **Upstream (1.2.3):** Family and pipeline-role tags feed **compatibility** and **validation** rules (e.g. commit stages requiring prior structure outputs).
- **Upstream (1.2.1–1.2.2):** Node/edge taxonomy and execution/subgraph semantics define **validation predicates**.
- **Downstream (Phase 2):** Serialization, golden manifests, and CI **bind** these NL contracts to artifacts.

## Edge cases

- **Partial manifests:** Importing a subgraph without world context — validation may pass **structurally** yet fail **semantic** hook resolution; contract: **explicit “context required”** diagnostics (**execution-deferred** UX).
- **Version skew:** Mixed-generation nodes in one graph — either **disallowed** by default or **requires** explicit adapter stages (**execution-deferred**).
- **Dry-run vs static validation:** **Dry-run** may exercise **more** than static checks (per **1.2** secondary); static pass is **cheaper** and **required** first.

## Open questions

- Whether **manifest** is **always** separate from **world snapshot** or **merged** in some toolchains — **PMG** when vertical slice is chosen.
- Minimum **version granularity** (per whole graph vs per node kind) — **execution-deferred** registry decision.

## Pseudo-code readiness

Readers can sketch **`validate_graph(gdef) -> Diagnostic[]`** and **`Manifest.from(graph, seed_bundle_ref)`** as **signatures only**; no engine code.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from schema evolution, package manifests, and static analysis hooks in build graphs and data pipelines.
