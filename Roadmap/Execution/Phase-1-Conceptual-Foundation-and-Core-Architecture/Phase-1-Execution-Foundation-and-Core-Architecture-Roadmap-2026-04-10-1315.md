---
title: Phase 1 — Execution foundation and core architecture (Godot lane)
roadmap-level: primary
phase-number: 1
subphase-index: "0"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps:
  - "Deferred seams `GMM-2.4.5-*` and `CI-deferrals` remain execution-open with explicit owner/timebox."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
conceptual_counterpart: "[[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
links:
  - "[[../../godot-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
---

## Phase 1 — Execution foundation (parallel spine)

> **Scope:** This note is the **execution-track** counterpart to the conceptual Phase 1 primary. It translates design authority into **repo-shaped contracts** for the **Godot** implementation lane while keeping **GMM-2.4.5-*** registry rows and **CI / HR closure** explicitly **deferred** (see deferral table). **Sandbox** (lane B) may differ only where the comparand table calls out an alternate stub.

## TL;DR

- **One spine:** world state ↔ simulation ↔ render ↔ input, with a **single commit boundary** and a **generation graph** staged before live play.
- **This execution slice:** folder + module boundaries, **interface IDs**, and **acceptance criteria** sufficient for a junior dev to implement **Phase 1.1** execution mirrors without picking storage or network stacks.
- **Deferred:** rollup registry closure, CI wiring, performance proofs — tracked as execution-deferred, not blocking this note.

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| **Host runtime** | Godot 4.x project; C# or GDScript modules per PMG | Ephemeral stub / non-Godot harness for API experiments |
| **Commit boundary** | `WorldState` facade + explicit `CommitResult` enum surfaced to autoload/singleton boundary | In-memory facades only; no export packaging |
| **Graph execution** | Scene-tree-friendly stage list; signals for stage boundaries | Callable list; stdout logging |
| **Observability** | Hook names stable for later **mar.*** join tests (execution-deferred) | printf-style trace IDs |

## Interfaces (execution-shaped)

| ID | Responsibility | Consumers | Notes |
| --- | --- | --- | --- |
| **IF-EXEC-1.0** | `IWorldRead` / `IWorldCommit` — read during staging; single committer | Simulation, render | Version token increments on successful commit |
| **IF-EXEC-1.1** | `IGraphStage` — `DryRun()` vs `Run()`; emits manifest handle | Pipeline orchestration | Aligns to conceptual **1.2.5** interchange manifests |
| **IF-EXEC-1.2** | `IIntentIngress` — shape validation vs semantic validation split | Input, DM tools | Authorization bits carried on intent object |

## Pseudocode — orchestration skeleton (Godot-flavored)

```pseudo
# Autoload boundary (lane A) — names illustrative, not binding filenames
class WorldGateway:
    func stage_delta(sim: Simulation, intents: Array) -> CommitResult:
        var staged = sim.build_delta(intents, self.read_view())
        if not self.validate_hard(staged):
            return CommitResult.rejected("hard_invariant")
        return self.commit(staged)

    func dry_run_graph(graph: GraphDef) -> ManifestHandle:
        return graph_compiler.validate_only(graph)
```

## Acceptance criteria

1. **AC-1:** All four layers named in the conceptual primary are represented as **namespaces or folders** in the execution tree proposal (no cross-layer concrete type imports).
2. **AC-2:** `CommitResult` / `ManifestHandle` appear in **public** interface docs for this phase (stub implementations allowed).
3. **AC-3:** Dry-run path returns a **reject-before-run** outcome for invalid graphs without mutating world state.
4. **AC-4:** Lane comparand table (above) copied or linked from **every** Phase 1 execution secondary mint until lane B is retired.

## GMM-2.4.5-* and CI — explicit deferrals

| Artifact class | Status | Where it closes |
| --- | --- | --- |
| **GMM-2.4.5-*** registry rows | **Deferred** — reference-only here | Execution tertiaries / Phase 5+ seams; not gate for Phase 1 execution scaffolding |
| **CI / HR / rollup proof** | **Deferred** | Execution track + plugin spec; **no** workflow blocker for **1.x** mirrors |

## Next structural execution targets

1. **1.1** — [[Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Execution-Layering-and-Interface-Contracts-Roadmap-2026-04-10-1316]] (closed roll-up): layering contracts translated to module boundaries and commit seam stubs.
2. **1.2** — [[Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Execution-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-1415]] (minted): graph skeleton and dry-run seam contracts now explicit.
3. **1.2.1** — Next tertiary target under the mirrored `Phase-1-2-Procedural-Generation-Graph-Skeleton/` spine.

## Phase-1 primary gate propagation map (from 1.1 roll-up)

| Primary gate anchor | Upstream source | Current state | Evidence / note |
| --- | --- | --- | --- |
| `rollup_1_primary_from_1_1` | `rollup_1_1_from_1_1_1` on [[Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Execution-Layering-and-Interface-Contracts-Roadmap-2026-04-10-1316]] | closed | Final pass/fail closure evidence linked from secondary and tertiary artifacts; owner signoff token `owner_signoff_rollup_1_primary_from_1_1_2026-04-10`. |
| `phase1_gate_commit_boundary` | `G-1.1-Commit-Seam` | pass-propagated | Commit seam evidence linked from `1.1.1` pseudocode and interface stub sections. |
| `phase1_gate_boundary_isolation` | `G-1.1-Boundary-Isolation` | pass-propagated | Forbidden-call checklist owner signoff captured in `1.1` secondary note. |
| `phase1_gate_lane_parity` | `G-1.1-Comparand-Parity` | pass-propagated | Godot (A) vs sandbox (B) comparand parity remains explicit and linked. |

## Phase-1 primary gate propagation map (from 1.2 roll-up)

| Primary gate anchor | Upstream source | Current state | Evidence / note |
| --- | --- | --- | --- |
| `rollup_1_primary_from_1_2` | `G-1.2-*` closure rows on [[Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Execution-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-1415]] | closed | 1.2 roll-up now closed with explicit PASS verdicts and owner signoffs; parity notes retained for lane A/B and mirrored in [[../workflow_state-execution#Execution gate tracker]]. |
| `phase1_gate_graph_taxonomy` | `G-1.2-Node-Taxonomy` | pass-propagated | Node-family taxonomy and ownership are now lifted to primary gate scope. |
| `phase1_gate_graph_edges` | `G-1.2-Edge-Typing` | pass-propagated | Edge typing/version rows are parity-visible and linked to 1.2.1 evidence. |
| `phase1_gate_topology_determinism` | `G-1.2-Topo-Determinism` | pass-propagated | Stable key-order digest constraints are anchored at primary scope. |
| `phase1_gate_dryrun_parity` | `G-1.2-DryRun-Parity` | pass-propagated | Dry-run vs run parity semantics are explicit across Godot and sandbox comparands. |

## Handoff-readiness rationale (execution threshold)

| Component | Evidence | Score contribution |
| --- | --- | --- |
| Gate closure completeness | `rollup_1_1_from_1_1_1` closed on 1.1 secondary + `rollup_1_primary_from_1_1` closed in this note with owner tokens | 30 / 30 |
| Interface + boundary traceability | IF-EXEC interfaces, pseudocode seam, and forbidden-call matrix links are explicit and cross-referenced | 24 / 25 |
| Lane parity visibility | Godot (A) vs sandbox (B) comparand rows are present and propagated from secondary/tertiary | 16 / 20 |
| Residual risk treatment | Deferred seams (`GMM-2.4.5-*`, CI/HR) remain explicitly non-blocking and tracked by state surfaces | 16 / 25 |

Execution handoff-readiness score: **89 / 100** (>=85 threshold met for this phase slice).

## Related

- Conceptual primary (design authority): [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]
- Distilled core (shared): [[../../distilled-core]]
- Decisions log: [[../../decisions-log]]
