---
title: Phase 2.1 (Execution) — Staged worldgen pipeline stub scope
created: 2026-04-09
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 2
subphase-index: "2.1"
conceptual_counterpart: "[[../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
status: in-progress
progress: 5
handoff_readiness: 86
---

# Phase 2.1 (Execution) — Staged worldgen pipeline stub scope

First **execution-local** secondary (**`2.1`**) under **Phase 2**, per [[../decisions-log]] **D-Exec-1-numbering-policy** — execution indices are **not** mirrored to conceptual **2.1.x** / **2.2.x** tertiary paths until PMG/MOC explicitly aligns them; conceptual Phase 2 remains the **design authority** for staged pipeline semantics ([[../distilled-core]] core decision: Phase 2 primary — staged worldgen pipeline).

## Scope

- **In scope (execution):** Define a **stub scope contract** for how execution work will **import** conceptual Phase 2’s **staged worldgen pipeline** (seed/graph → terrain → biomes → POIs → entities → sim bootstrap) as **implementation-shaped** rows — **checklists + stage boundary vocabulary only**, no claiming merge/bundle/hash closure (`GMM-2.4.5-*` and crypto replay proofs remain **execution-deferred** per [[../distilled-core]]).
- **Continuity from Phase 1 execution:** Positions **2.1** as the bridge after [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]] rollup — instrumentation spine stubs (**1.1–1.3**) precede worldgen stage stubs; no host binary.
- **Out of scope:** Mutating frozen conceptual notes under `Roadmap/**` outside `Execution/`; materializing full delta-bundle merge engines or CI — **execution-deferred**.

## NL checklist (2.1)

- [x] Name the **conceptual import** — Phase 2 primary ([[../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]) — as **wikilink only**.
- [x] List **six** **stage labels** (execution stub names) aligned to PMG / distilled-core Phase 2 primary wording: **SeedGraph** → **Terrain** → **Biomes** → **POIs** → **Entities** → **SimBootstrap** (stage ledger table below — **SimBootstrap** closes the pipeline into simulation entry vocabulary shared with conceptual **2.7.x** / Phase 1 **1.3** tick stubs).
- [x] Declare **one** acceptance line: “Operator can trace **Phase 1** instrumentation stubs → **2.1** stage ledger → conceptual Phase 2 primary headings without contradiction.”

## Stage ledger (stub rows — execution-local)

| Stage id | Intent (one line) | Upstream / downstream stub |
| --- | --- | --- |
| **S2.1-SG** | Seed + graph admission | Consumes operator seed bundle vocabulary from **1.3** `CommittedTickStub` namespace as **non-authoritative** input handle only |
| **S2.1-TR** | Terrain column / heightfield stub | Feeds **S2.1-BM**; no mesh/binary |
| **S2.1-BM** | Biome classification stub | Feeds **S2.1-POI** |
| **S2.1-POI** | POI placement stub | Feeds **S2.1-EN** |
| **S2.1-EN** | Entity spawn bundle stub | Feeds **S2.1-SB** |
| **S2.1-SB** | Sim bootstrap handoff stub | Aligns wording to conceptual **2.7** simulation-entry / first-tick contracts as **cross-links only** |

## GWT-2-1-Exec-A–D

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-1-Exec-A | Conceptual Phase 2 primary is named and linked | § NL checklist |
| GWT-2-1-Exec-B | Stage ledger is execution-local and does not claim merge/bundle closure | § Stage ledger + **Out of scope** |
| GWT-2-1-Exec-C | Continuity from Phase 1 execution spine is stated | § Scope + **S2.1-SG** row |
| GWT-2-1-Exec-D | Next execution deepen target is machine-resolvable | [[workflow_state-execution]] + [[roadmap-state-execution]] |

## Open questions

- Which **first child** under **2.1** (tertiary **2.1.1**) should mint first — **SeedGraph** drill vs **Terrain** drill — operator preference.

## Related

- [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- [[roadmap-state-execution]]
- [[workflow_state-execution]]
- [[../decisions-log]]
