---
title: "CDR — Phase 2.1.4 bundle identity, seam catalog stability, replay/diff"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-20260330T224500Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 2.1.4 bundle identity, seam catalog stability, replay/diff

## Summary

Minted tertiary **2.1.4** to extend **2.1.3** with **BundleIdentity**, **SeamCatalogRevision**, replay-equivalence, and deterministic bundle diff — closing the “how bundles evolve and compare” gap without duplicating merge/ordering from 2.1.3.

## PMG alignment

Supports the Phase 2 goal of a **deterministic, explainable** procedural pipeline: stable identities and catalog revisioning make regeneration and debugging tractable for a future implementation team.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
|-------------|--------|---------|------------------|
| Fold identity/revision into 2.1.3 body | One fewer file | Blurs composition vs evolution concerns | Split keeps 2.1.3 readable; 2.1.4 owns evolution contract |
| Defer identity entirely to execution | Smaller conceptual tree | Replay/regressions lack NL hooks | Project needs named contracts before code |

## Validation evidence

- **pattern_only:** Content-addressed builds, API semver, and deterministic replay testing practice; no new `Ingest/Agent-Research/` notes this run.

## Links

- Parent: [[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]
- Prior slice: [[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]
- Workflow anchor: `2026-03-30 23:05` — Target `Phase-2-1-4-Bundle-Identity-...`
