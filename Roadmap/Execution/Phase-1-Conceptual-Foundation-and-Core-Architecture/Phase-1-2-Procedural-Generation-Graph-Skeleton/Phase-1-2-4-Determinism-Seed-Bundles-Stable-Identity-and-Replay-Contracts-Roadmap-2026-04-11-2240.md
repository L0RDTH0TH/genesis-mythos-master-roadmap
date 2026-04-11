---
title: Phase 1.2.4 (Execution) — Determinism, seed bundles, stable identity, and replay contracts
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - graph
  - determinism
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.4"
status: in-progress
handoff_readiness: 87
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Slice minted on execution spine with Intent Mapping + AC table; evidence rows Planned until repo artifacts; no verbatim C++ stdlib blocks in this pass (text sketches only — Research-backed C++ precision deferred)."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]"
---

# Phase 1.2.4 (Execution) — Determinism, seed bundles, stable identity, and replay contracts

Execution tertiary **1.2.4** on the **parallel spine** under `Phase-1-2-Procedural-Generation-Graph-Skeleton/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]. Focus: **hierarchical seed bundles**, **stable logical node identity** independent of schedule, **determinism contract** for spine stages vs explicitly tagged nondeterministic work, and **replay intent** (dry-run vs committed) — consistent with **1.2.1** taxonomy, **1.2.2** waves/subgraphs, **1.2.3** stage families, and **secondary 1.2** dry-run vs commit. **GMM-2.4.5** / **CI** graph proofs remain **explicitly deferred** unless evidenced later.

Upstream **1.2.3** execution: [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-04-11-1415]] · Upstream **1.2.2**: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-0005]] · Upstream **1.2.1**: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-0005]] · Parent secondary **1.2**: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: seed/identity/replay seams and intent mapping. **AC** rows begin **Planned** until repo artifacts attach. **`status: in-progress`**. Automation **next** structural target after this mint is **`1.2.5`** (graph versioning / interchange) — see [[../../workflow_state-execution]].

## Alignment to conceptual Phase-1-2-4

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Hierarchical seed derivation (world → subgraph → node) | `seed_bundle` composition + `derive_node_seed` text seams | AC-1.2.4.E1 |
| Stable logical IDs vs evaluation order | `logical_key` invariant + tie to **1.2.2** schedule (ordering does not rename) | AC-1.2.4.E2 |
| Deterministic spine vs tagged nondeterministic stages | `stage_determinism_tag` + explicit IO/clock prohibition for deterministic class | AC-1.2.4.E3 |
| Replay: dry-run vs committed equivalence | `replay_mode` seam + **1.2.3** commit-family ordering for committed replay | AC-1.2.4.E4 |

## Mid-technical seams (text-only)

**Depth 3:** sketches in **`text`** blocks only — same deferral as **1.2.2–1.2.3**: no committed C++ standard-library claims in this slice; a future **Research `Task` + allowlisted docs** pass may attach verbatim citations when implementation binds to `std::` facilities.

```text
compose_seed_bundle(world_root, subgraph_salt, graph):
  bundle.session_root = hash(world_root)
  bundle.subgraph_fragment = mix(bundle.session_root, subgraph_salt)
  for node in graph.nodes:
    bundle.node_seeds[node.logical_key] =
      derive_node_seed(bundle.subgraph_fragment, node.kind, node.local_salt)
  return bundle
```

```text
derive_node_seed(parent_material, node_kind, local_salt):
  // Only declared dependency outputs + declared seed fields participate (1.2.1)
  return mix(parent_material, stable_enum(node_kind), local_salt)
```

```text
replay_equivalence(mode, recorded, candidate):
  if mode == dry_run:
    return same_inputs_and_seeds(recorded, candidate)  // no commit digests required
  if mode == committed:
    return dry_run_equal AND commit_digest_match(recorded, candidate)  // uses 1.2.3 commit ordering
```

## Interfaces

| Direction | Contract |
| --- | --- |
| Upstream **1.2.1** | Only **EdgeKind**-declared deps + node kind participate in `derive_node_seed` inputs. |
| Upstream **1.2.2** | `wave_partition` order changes **schedule**, not `logical_key`; subgraph closure defines bundle visibility. |
| Upstream **1.2.3** | **Commit**-family stages may record validation digests that **committed** replay must match. |
| Downstream **1.2.5** | Versioning / interchange manifests bind deterministic outputs to exchange tooling — see conceptual Phase-1-2-5. |

## Tasks (tertiary execution breakdown)

| Task | Owner | Depends on | Target artifact |
| --- | --- | --- | --- |
| T-1.2.4-a | Roadmap agent / operator | **1.2.1** keys | `seed_bundle_schema.tsv` (E1) |
| T-1.2.4-b | Roadmap agent | T-1.2.4-a | `logical_identity_table.md` (E2) |
| T-1.2.4-c | Roadmap agent | **1.2.3** families | `determinism_tags.md` (E3) |
| T-1.2.4-d | Roadmap agent | **1.2.2** + T-1.2.4-c | `replay_modes.md` (E4) |

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.2.4.E1 | Seed bundle enumerates session → subgraph → node derivation | `seed_bundle_schema.tsv` | Planned |
| AC-1.2.4.E2 | Logical keys stable across reorderings that preserve deps | `logical_identity_table.md` | Planned |
| AC-1.2.4.E3 | Every stage classifies deterministic vs explicit nondeterministic | `determinism_tags.md` | Planned |
| AC-1.2.4.E4 | Dry-run vs committed replay rules documented | `replay_modes.md` | Planned |

## Intent Mapping

- **Design intent:** Bind **reproducibility** for the procedural graph so tooling and debugging can rely on **stable identity** and **hierarchical seeds** without smuggling hidden randomness through unspecified channels — mirroring conceptual Phase-1-2-4 authority.
- **Inspiration anchor(s):**
  - **Deterministic simulation / fixed-seed game tooling:** reproducible runs from a single seed + build graph mental model (pattern only — no engine API claims).
  - **Build systems (e.g. Bazel-style):** hermetic inputs and explicit external-tool tags as analogy for **deterministic spine** vs **explicit nondeterministic** stages (pattern only).
- **Execution implementation:** `compose_seed_bundle` / `derive_node_seed` text seams, `logical_key` invariants vs **1.2.2** ordering, `replay_equivalence` branching on dry-run vs committed (with **1.2.3** commit digests when committed).
- **Validation signal:** AC table remains **Planned** until repo paths exist — explicit deferral for **GMM-2.4.5 / CI** unchanged.

## Risks (v0)

- **Salt explosion** — mitigate with documented hierarchy and minimum fields per conceptual 1.2.4.
- **Hidden nondeterminism** — mitigate with explicit tags + prohibition list for deterministic spine stages.

## Related (execution spine)

- Prior **1.2.3**: [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-04-11-1415]]
- Next tertiary **1.2.5** (versioning / interchange): conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]

## Research integration

> [!note] External grounding
> This mint uses **text-only** algorithm sketches (no verbatim C++ / headers). A future **nested `Task(research)`** pass with **sandbox allowlisted** URLs may attach standard-library citations if implementation binds to concrete `std::` facilities — per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]].
