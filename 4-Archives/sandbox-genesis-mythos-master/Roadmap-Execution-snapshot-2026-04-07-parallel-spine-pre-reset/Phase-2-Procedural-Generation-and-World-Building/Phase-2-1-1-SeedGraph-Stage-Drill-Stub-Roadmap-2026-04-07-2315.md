---
title: Phase 2.1.1 (Execution) — SeedGraph stage drill stub
created: 2026-04-07
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
conceptual_counterpart: "[[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
status: in-progress
progress: 10
handoff_readiness: 86
---

# Phase 2.1.1 (Execution) — SeedGraph stage drill stub

First **tertiary** under execution secondary **2.1** — drills **`S2.1-SG`** (Seed + graph admission) from [[Phase-2-1-Staged-Worldgen-Pipeline-Stub-Scope-Roadmap-2026-04-09-2306]] before **`S2.1-TR`** (Terrain), per **Phase 2.1** open-question resolution: **SeedGraph first** (pipeline order). Aligns **D-Exec-1-numbering-policy** (execution-local **`2.1.1`** ≠ conceptual **`2.1.x`** procedural indices) and PMG / [[../../distilled-core]] Phase 2 primary — staged worldgen pipeline vocabulary without claiming merge/bundle closure.

## Scope

- **In scope:** Stub **drill rows** + **mid-technical pseudocode** for how **`CommittedTickStub`** / seed-bundle handles from [[Phase-1-3-FirstCommittedTick-Stub-Binding-Roadmap-2026-04-09-2210]] surface as **non-authoritative** inputs to a **SeedGraphStub** envelope (namespaced IDs only).
- **Out of scope:** Real graph storage, hashing, delta bundles, or CI — **execution-deferred** per [[../../distilled-core]].

## NL checklist (2.1.1)

- [x] Name parent secondary **2.1** and link [[Phase-2-1-Staged-Worldgen-Pipeline-Stub-Scope-Roadmap-2026-04-09-2306]].
- [x] Bind **`S2.1-SG`** row to **at least one** upstream Phase 1 stub field (`tick_commit_id` / seed bundle vocabulary) as **read-only** input.
- [x] Declare **drill** Happy/Edge cases without claiming authoritative simulation state.

## Drill rows (stub)

| Drill id | Scenario | Expected stub outcome |
| --- | --- | --- |
| **D2.1.1-H1** | Happy — minimal seed bundle + tick id | `SeedGraphStub.admit()` returns `admitted: true` with opaque `graph_handle` |
| **D2.1.1-E1** | Edge — missing tick correlation | `admitted: false`, `reason: "tick_seed_mismatch"` |

## Pseudocode (mid-technical)

```pseudo
type SeedGraphStub struct {
  namespace string // execution-local; not a conceptual index remap
}

func (s *SeedGraphStub) Admit(bundle SeedBundleRef, tick CommittedTickRef) AdmitResult {
  if bundle.Correlates(tick) != true {
    return AdmitResult{Admitted: false, Reason: "tick_seed_mismatch"}
  }
  return AdmitResult{Admitted: true, GraphHandle: opaqueHandle(bundle)}
}
```

## GWT-2-1-1-Exec-A–D

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-1-1-Exec-A | Parent **2.1** linked; **`S2.1-SG`** drill exists | § Scope + § Drill rows |
| GWT-2-1-1-Exec-B | Phase 1 **1.3** correlation vocabulary referenced | § Scope + pseudocode `CommittedTickRef` |
| GWT-2-1-1-Exec-C | No merge/bundle/hash closure claimed | § Out of scope |
| GWT-2-1-1-Exec-D | Next deepen target is machine-resolvable | [[workflow_state-execution]] — Terrain drill **2.1.2** (pending) or secondary **2.2** |

## Open questions

- Whether **tertiary 2.1.2** should be **Terrain** drill only vs combined **Terrain+heightfield** stub — defer to next **`deepen`**.

## Related

- [[Phase-2-1-Staged-Worldgen-Pipeline-Stub-Scope-Roadmap-2026-04-09-2306]]
- [[Phase-1-3-FirstCommittedTick-Stub-Binding-Roadmap-2026-04-09-2210]]
- [[roadmap-state-execution]]
- [[workflow_state-execution]]
- [[../../decisions-log]]
