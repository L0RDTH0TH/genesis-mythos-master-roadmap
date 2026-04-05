---
title: Phase 2 — Procedural Generation and World Building
roadmap-level: primary
phase-number: 2
subphase-index: "0"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 85
phase2_primary_checklist: complete
phase2_primary_rollup_post_27: complete
handoff_readiness: 86
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[sandbox-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
---

## Phase 2 — Procedural Generation and World Building

Deliver the collaborative forge: pipeline stages from seed through terrain, biomes, POIs, entities, and bootstrap, with intent loops that turn player/DM inputs into systemic hooks without shipping hardcoded narratives.

## Conceptual waiver & safety invariants

- Conceptual track waiver (rollup / CI / HR): This project’s **design authority** on the **conceptual** track does **not** claim execution rollup, registry/CI closure, or HR-style proof rows; those are **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- Safety invariants (Phase 1 contract): use **seed snapshots + dry-run validation hooks** as the NL contract for safe boundaries; execution tooling, CI, and registry closure are explicitly out of scope for this conceptual phase.

- [x] Core implementation task — End-to-end generation pipeline with deterministic stages → [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]
- [x] Core implementation task — Intent resolver feeding reputation/event/environment hooks
- [x] Glue / integration task — Collaborative dialogue loop (scaffold propose → refine → commit)

### Progress semantics (frontmatter)

`progress` is **0–100** for this note’s conceptual slice depth: **0** = stub only; **~20** = primary NL checklist complete enough to mint secondaries; **~50+** = secondaries drafted; **100** = phase-ready for execution handoff (still execution CI deferred).

## Scope

**In scope:** the Phase 2 conceptual “forge” contract for staged world generation: a seed-to-world pipeline spine, intent-to-hook mapping via an intent resolver, and a collaborative dialogue loop that scaffolds, refines, and commits generation deltas safely.

**Out of scope:** concrete engine APIs, asset pipeline IDs, execution-track proof obligations (tests/CI/perf budgets/registry closure), and any final narrative “hardcoded lore” decisions (kept as data/injection inputs).

## Behavior (natural language)

Actors: **systems** (pipeline runner + validation gates), **DM** (regeneration requests + intent overrides), **players** (inputs that become intent hooks).  
Inputs: seed bundle identity, prior staged outputs, DM/player intent hooks, and deterministic regeneration directives.  
Outputs: staged deltas and commit-ready overlays produced only after the dry-run validation gate clears.

Ordering: **seed expansion → intent resolve → stage pipeline evaluation → simulation bootstrap packaging → dry-run validation → commit boundary**.

## Interfaces

Upstream (Phase 1 conceptual): Phase 2 consumes the generation-graph skeleton and safety invariants, and uses those hook/vocabulary contracts when assembling stage ordering.  
Downstream: secondaries/tertiaries under this phase (starting with **2.1**) refine stage bodies and representation details; they never change the Phase 2 pipeline spine without explicitly revising the interface contract.

Outward guarantees:
- Deterministic stage ordering and stable hook naming at the NL contract level.
- No partial commit on failure: invalid stage outputs produce empty staged deltas or blocked commit.

## Edge cases

- Partial stage failure: downstream stages receive empty typed outputs; commit is blocked.
- Conflicting intents / merge policy: collisions resolve via explicit hook priority rules; the execution-track merge implementation is deferred.
- Regeneration mid-campaign: regeneration requests re-run the dry-run validation gate before any commit boundary is crossed.

## Open questions

- Hook naming convention across DM/player intent domains (topic-like vs path-like) before execution registry closure.
- Minimum viable vertical-slice granularity for stage families (linear vs explicit subgraph runs; execution deferred).

## Pseudo-code readiness

At this primary conceptual depth, pseudo-code is not required. Readers should be able to outline the stage spine and typed interfaces without writing algorithms; pseudo-code for specific stage bodies belongs in secondaries/tertiaries.

## Phase 2 primary rollup (post-2.7 simulation chain)

> **Architect:** Same queue pass resolved **stale** user text (“mint 2.7.3”) against **authoritative** vault state — **2.7.1–2.7.3** already minted (`resume-deepen-gmm-273-followup-20260401T120100Z`). This section records **primary-level** rollup after the **2.7** simulation-entry / first-tick chain so Phase 2 can meet the **advance-phase** gate without implying execution CI/registry closure (`GMM-2.4.5-*` remain reference-only).

**Spine closed in NL (conceptual):** secondaries **2.1–2.7** are each chain-complete at their declared tertiary depth; **2.7** closes the **simulation-entry bootstrap → dry-run shadow / hook matrix → shadow-to-live parity + FirstCommittedTickTrace** story and binds upstream **2.6.3** replay/cold-start into admission.

**Roll-up invariants (design authority):**

- **Ordering:** seed expansion → intent resolve → staged pipeline → simulation bootstrap packaging → dry-run validation → commit boundary → (where applicable) post-commit audit/telemetry/consumer surfaces → simulation entry / first committed tick — consistent with Phase 2 primary **Behavior** and secondaries **2.1–2.7**.
- **Execution-deferred:** registry/CI/compare-table/HR-style proofs stay **out of scope** for conceptual completion; see primary **Conceptual waiver** above.
- **Next structural operator choice:** **`advance-phase`** to Phase **3** when gates pass, **or** optional **2.8** mint only if PMG expands Phase 2 scope (not assumed here).

`handoff_readiness` on this primary note raised to **86** after rollup narrative alignment with **2.7.3** closure (`handoff_readiness` **84** on tertiary slice).

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
