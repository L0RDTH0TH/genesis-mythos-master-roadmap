---
title: CDR - Phase 2.2.1 tertiary (intent envelope normalization)
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]"
decision_kind: deepen
queue_entry_id: resume-deepen-a1b-bootstrap-20260330T233800Z-gmm
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record - Phase 2.2.1 tertiary (intent envelope normalization and identity binding)

## Summary

Minted Phase 2 **tertiary 2.2.1** as the first structural slice under **2.2** intent resolver + hook mapping: canonical intent envelope shape, actor/channel/frame identity binding, dedupe/idempotency policy hooks, and deterministic normalization ordering before classify/resolve stages.

## PMG alignment

Keeps collaborative world building replay-safe by making intent records explicit, comparable, and deduplicable before any hook emission — consistent with Phase 2 dry-run / commit separation and Phase 2.1 typed staged outputs.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Defer normalization to execution code | Smaller conceptual tree | Hidden coupling and replay drift | Fails determinism contract for resolver |
| Merge normalization + classify in one note | Fewer files | Harder to test identity vs semantics separately | Violates staged resolver clarity |
| Require crypto identity at conceptual depth | Strong audit story | Execution-shaped hold on conceptual track | Deferred per dual-track policy |

## Validation evidence

- Pattern-only: deterministic normalization + identity binding patterns; no `Ingest/Agent-Research/` notes bound this run.

## Links

- **Roadmap note:** [[Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]
