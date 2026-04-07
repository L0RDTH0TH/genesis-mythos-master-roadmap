---
title: Phase 2.1.1 (Execution) — SeedGraph vs Terrain stage drill
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.1"
conceptual_counterpart: "[[../../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]"
status: in-progress
progress: 15
handoff_readiness: 86
archived_from: "1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/"
archived_at: 2026-04-10
---

# Phase 2.1.1 (Execution) — SeedGraph vs Terrain stage drill

Execution-track **tertiary** under the **parallel spine** for conceptual Phase **2.1.1** — drills the **ordering and contracts** for **`S2.1-SG` (SeedGraph)** vs **`S2.1-TR` (Terrain)** before downstream biome/POI stubs, resolving the Phase **2.1** open question: **SeedGraph-first** pipeline order with explicit boundary between graph-shaped seed admission and terrain column materialization.

Aligns **[[../../../../decisions-log|decisions-log]]** **D-Exec-1-numbering-policy** (execution-local **`2.1.1`** is not a conceptual index remap) and **[[../../../../Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430|PMG]]** Phase 2 intent — staged procedural generation without claiming merge/bundle/CI closure.

## Scope

**In scope**

- Mid-technical **drill rows** for **SeedGraph** admission vs **Terrain** heightfield/column stubs (interfaces + pseudocode only).
- Explicit **non-overlap**: SeedGraph emits **typed handles**; Terrain consumes **only** those handles + intent hooks — no back-feed from terrain into seed graph shape in this stub.
- Cross-link to conceptual **[[../../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205|Phase 2.1 secondary]]** stage spine (Stages 0–5) as design authority.

**Out of scope**

- Real graph storage, meshing, asset pipelines, or registry/CI — **execution-deferred** per **[[../../../../distilled-core|distilled-core]]**.

## SeedGraph vs Terrain (resolution drill)

| Dimension | **S2.1-SG — SeedGraph** | **S2.1-TR — Terrain** |
| --- | --- | --- |
| **Role** | Admit seed-bundle identity + derive stable graph-shaped handles for downstream stages | Materialize terrain **column / heightfield stub** from admitted handles + intent hooks |
| **Inputs** | `SeedBundleRef`, `CommittedTickRef` (read-only correlation vocabulary from Phase 1 execution stubs — see **[[../../../../decisions-log|decisions-log]]** D-Exec-1) | `SeedGraphAdmitResult`, `IntentResolvedSet` |
| **Outputs** | `GraphHandle` (opaque), `namespace` binding | `TerrainColumnStub` (typed; no binary payload) |
| **Failure mode** | `tick_seed_mismatch`, `bundle_unresolved` | `upstream_graph_denied` (Terrain must not invent graph) |
| **Order** | **Always first** in the **2.1** stage ledger before Terrain | **Second** — cannot run if SeedGraph admission failed |

## NL checklist (execution 2.1.1)

- [x] Name **SeedGraph vs Terrain** boundary and ordering (table above).
- [x] Bind **D-Exec-1** execution-local numbering (this path under `Execution/` mirrors conceptual **Phase-2-1-Pipeline-Stages-Seed-to-World** folder only — not conceptual tertiary index parity).
- [x] Reference **PMG** / Phase 2 staged pipeline without claiming **GMM-2.4.5-*** closure.

## Drill rows (stub)

| Drill id | Scenario | Expected stub outcome |
| --- | --- | --- |
| **D2.1.1-H1** | Happy — bundle + tick correlate | `SeedGraphStub.Admit` → `admitted: true`, opaque `graph_handle` |
| **D2.1.1-H2** | Happy — graph handle feeds Terrain | `TerrainStub.BuildColumn(graph_handle)` → non-empty `TerrainColumnStub` |
| **D2.1.1-E1** | Edge — tick/seed mismatch | `admitted: false`, `reason: "tick_seed_mismatch"` — **Terrain not invoked** |
| **D2.1.1-E2** | Edge — Terrain invoked without graph | `TerrainStub` returns `err: "upstream_graph_denied"` |

## Test plan (stub-level AC)

Runnable acceptance mapping for **D2.1.1-*** drill ids (no real engine or CI — stub calls only).

| Test id | Drill id | Executable check (stub-level) |
| --- | --- | --- |
| **TP-D2.1.1-H1** | D2.1.1-H1 | Call `SeedGraphStub.Admit` with correlated bundle+tick → `Admitted==true`, non-zero `GraphHandle`. |
| **TP-D2.1.1-H2** | D2.1.1-H2 | Feed H1 handle into `TerrainStub.BuildColumn` → non-error `TerrainColumnStub`. |
| **TP-D2.1.1-E1** | D2.1.1-E1 | Mismatched tick → `Admitted==false`; Terrain stub **not** invoked. |
| **TP-D2.1.1-E2** | D2.1.1-E2 | Zero handle → `upstream_graph_denied` or equivalent error from `TerrainStub`. |

## Pseudocode (mid-technical)

```pseudo
type SeedGraphStub struct { Namespace string }

func (s *SeedGraphStub) Admit(bundle SeedBundleRef, tick CommittedTickRef) AdmitResult {
  if !bundle.Correlates(tick) {
    return AdmitResult{Admitted: false, Reason: "tick_seed_mismatch"}
  }
  return AdmitResult{Admitted: true, GraphHandle: opaqueHandle(bundle)}
}

func (t *TerrainStub) BuildColumn(g GraphHandle, intent IntentResolvedSet) (TerrainColumnStub, error) {
  if g.IsZero() {
    return TerrainColumnStub{}, errUpstreamGraphDenied
  }
  return TerrainColumnStub{Handle: g, IntentTags: intent.Tags()}, nil
}
```

## GWT-2-1-1-Exec-A–D

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-1-1-Exec-A | SeedGraph **before** Terrain in stub flow | § SeedGraph vs Terrain + § Drill rows |
| GWT-2-1-1-Exec-B | D-Exec-1 + PMG alignment stated | § Scope + header |
| GWT-2-1-1-Exec-C | No merge/bundle/CI closure | § Out of scope |
| GWT-2-1-1-Exec-D | Next deepen target resolvable | [[../../workflow_state-execution]] — **2.1.2** Terrain-only polish **or** secondary **2.2** intent resolver stub |

## Open questions

- Whether **2.1.2** should isolate **Terrain heightfield** only vs combined **Terrain + biome** stub — defer to next **`deepen`**.
- Phase **1** live **Execution/** paths: **DEF-EXEC-P1-LIVE-REMINT** — rollup evidence lives in **[[../../../../decisions-log|decisions-log]]** + archive snapshot paths; **not blocking** this **2.1.1** slice (parity with [[../../roadmap-state-execution#Notes]]).

## Related

- [[../../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]
- [[../../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]
- [[../../../../distilled-core]]
- [[../../roadmap-state-execution]]
- [[../../workflow_state-execution]]
