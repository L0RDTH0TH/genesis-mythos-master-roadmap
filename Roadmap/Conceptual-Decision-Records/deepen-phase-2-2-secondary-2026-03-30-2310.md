---
title: CDR - Phase 2.2 secondary (intent resolver and hooks)
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-220-20260330T231000Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record - Phase 2.2 secondary (intent resolver and hook mapping)

## Summary

Minted Phase 2 **secondary 2.2** to define the intent resolver contract that translates player/DM/system intent envelopes into deterministic, typed hook payloads. The slice introduces normalization, validation, conflict resolution, and deterministic emission stages while preserving the existing Phase 2 pre-commit safety boundary.

## PMG alignment

This decision reinforces deterministic collaborative world building by making intent handling explicit and replay-safe instead of implicit in stage internals. It supports future execution implementation without forcing early engine-specific commitments.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Keep intent handling embedded in each stage | Localized logic in stage notes | Drift in semantics and inconsistent conflict policy | Weakens cross-stage determinism and replay safety |
| Lock engine-specific hook schema now | Faster coding start | Premature coupling to execution toolchain | Conflicts with conceptual track deferral policy |
| Allow unresolved conflicts to pass through | Fewer rejects in early drafts | Hidden nondeterminism and unstable replay outcomes | Violates deterministic contract for this phase |

## Validation evidence

- Pattern-only: aligned with deterministic resolver architectures and existing Phase 2 dry-run safety posture (no `Ingest/Agent-Research/` notes bound this run).

## Links

- **Roadmap note:** [[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]
