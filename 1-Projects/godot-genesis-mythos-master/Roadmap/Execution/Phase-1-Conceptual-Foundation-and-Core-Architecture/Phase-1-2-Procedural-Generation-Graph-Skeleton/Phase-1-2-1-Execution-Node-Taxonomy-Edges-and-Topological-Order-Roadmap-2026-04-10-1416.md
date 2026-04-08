---
title: Phase 1.2.1 — Execution node taxonomy, edges, and topological order (Godot lane)
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.1"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 85
handoff_gaps:
  - "Deferred seam closure (`GMM-2.4.5-*`, `CI-deferrals`) remains open and is tracked as owner/timebox work in 1.2."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
links:
  - "[[Phase-1-2-Execution-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-1415]]"
  - "[[../Phase-1-Execution-Foundation-and-Core-Architecture-Roadmap-2026-04-10-1315]]"
---

## Phase 1.2.1 — Execution graph-node taxonomy and ordering seam

Execution tertiary mirror for conceptual `1.2.1`. This note narrows graph node classes, edge typing, and deterministic sort invariants into a gate-verifiable execution contract with owner-path evidence.

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Node class encoding | `GraphNodeKind` enum + script-class adapter map | Enum + map in harness-only module |
| Edge typing | Typed edge records with schema key + version | Same keys with simplified payload envelope |
| Topological sort | Stable key sort (`stage_order`, `node_id`) after DAG validation | Deterministic list sort using same key tuple |
| Validation output | Structured validation report with gate IDs | Text report with same gate IDs for parity |

## Node/edge contract matrix

| Contract | Requirement | Evidence shape |
| --- | --- | --- |
| Node kind taxonomy | Every node declares one canonical `GraphNodeKind` and ownership lane | Node-kind table with owner and hook namespace |
| Edge key schema | Every edge key is typed and versioned before execution | Edge schema table with `edge_type`, `version`, `producer`, `consumer` |
| Topological determinism | Sort result is stable for same manifest + seed bundle | Determinism check row with stable digest hash |
| Dry-run parity | Dry-run and run share node ordering decisions | Validation row with identical ordering digest |

## G-1.2 roll-up gate table (execution)

| gate_id | gate_name | owner | evidence_artifact | pass_fail_criteria | current_status | blocker | due_window |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `G-1.2-Node-Taxonomy` | Node taxonomy complete and lane-owned | lane godot implementation owner | [[#Node/edge contract matrix]] | pass when every node kind has owner + hook namespace | **PASS** | none | Closed 2026-04-08 |
| `G-1.2-Edge-Typing` | Typed edge schema with version pin | architecture reviewer | [[#Node/edge contract matrix]] | pass when every edge row has type + version + producer/consumer | **PASS** | none | Closed 2026-04-08 |
| `G-1.2-Topo-Determinism` | Stable topological ordering digest | lane A/B maintainer | [[#Node/edge contract matrix]] | pass when identical manifest+seed emits identical ordering digest across lanes | **PASS** | none | Closed 2026-04-08 |
| `G-1.2-DryRun-Parity` | Dry-run ordering parity with run path | roadmap maintainer | [[#Node/edge contract matrix]] | pass when dry-run and run ordering digests match for same manifest | **PASS** | none | Closed 2026-04-08 |

## Pseudocode — deterministic sort contract

```pseudo
func topo_sort(nodes, edges):
  assert validate_dag(nodes, edges)
  ordered = stable_topo(nodes, edges, key=(stage_order, node_id))
  digest = hash(ordered.map(n => n.node_id))
  return { ordered, digest }
```

## Acceptance criteria

1. Node taxonomy table is complete with owner-path accountability.
2. Edge schema rows include typed version pins and producer/consumer ownership.
3. Topological ordering digest is stable for repeated dry-run and run inputs.
4. G-1.2 gate rows are explicit and can be propagated to 1.2 roll-up.
5. Lane comparand parity remains visible for Godot (A) vs sandbox (B).

## Next execution target

- Return to **1.2** as completed owner evidence and keep deferred seam closures tracked via explicit owner/timebox rows.
