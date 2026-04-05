---
title: "CDR — Phase 5.1.1 ruleset manifest admission and SeamId binding"
created: 2026-03-31
tags:
  - conceptual-decision-record
  - godot-genesis-mythos-master
  - phase-5
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-1-Ruleset-Manifest-Admission-and-Seam-Binding-Roadmap-2026-03-31-1200]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 5.1.1 ruleset manifest admission and SeamId binding

## Summary

Minted the first **Phase 5.1** tertiary (**5.1.1**) as **ruleset manifest admission** plus **SeamId binding** to **3.4.1**, so the plugin host has a deterministic NL contract for what may load before any **RuleOutcome** is emitted. **Conflict matrix** and **kernel evaluation schedule** are deferred to **5.1.2+** to avoid duplicating **5.1** secondary scope.

## PMG alignment

Advances the **rule system integration** spine: manifests are **admissible** only when seams are **catalog-bound**, preserving **one** simulation truth and **replay-stable** identity—consistent with the PMG’s deterministic / auditable world story.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Merge manifest + kernel scheduling in one tertiary | Fewer files | Oversized slice; blurs admission vs ordering | Split **5.1.1** / **5.1.2** per secondary **5.1** decomposition line |
| Allow manifest-defined **new** SeamIds | Faster iteration | Violates **3.4.1** authority | Rejected—bind to catalog only at conceptual depth |

## Validation evidence

- Pattern-only: parent [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]], upstream [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]].

## Links

- **Workflow anchor:** `2026-04-03 23:15` — `Phase-5-1-1-Ruleset-Manifest-Admission-and-Seam-Binding` — `queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z`
- **Resolver:** `gate_signature: queue-stale-guidance-reconcile-4-1-vs-5-1-1`, `effective_track: conceptual`, `gate_catalog_id: conceptual_v1`
