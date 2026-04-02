---
title: "CDR — Deepen Phase 1.2.1 snapshot preimage binding"
created: 2026-03-29
tags: [roadmap, conceptual-decision-record, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-after-1-2-20260329T193500Z
master_goal: "[[Genesis-mythos-master-goal]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 1.2.1 deepen (2026-03-29)

## Summary

Minted tertiary **1.2.1** to **bind** the parent **1.2** snapshot preimage table to **commit-time validation** (required vs conditional fields, boundary ticket closure) and a **post-commit audit minimum**, with pseudo-code for `ValidatePreimageForCommit` / `AppendAudit`. Keeps bytes, stores, and CI as **execution-deferred** per dual-track policy and **D-027**.

## PMG alignment

Reinforces PMG **snapshots + dry-run before commit** and **traceability** by making preimage completeness and manifest alignment explicit at the commit gate—without locking wire formats.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Further polish **1.2** secondary only | Slightly denser parent note | Misses resolver target **1.2.1**; stalls structural tree | **1.2** NL checklist already satisfied; forward structural per Layer 1 **missing_structure → 1.2.1** |
| Jump to **1.2.2** retention slice first | Surfaces ops sooner | Skips binding contract juniors need before retention | **Binding + audit** is the natural first tertiary under safety snapshots |
| Encode Merkle / hash chain here | Stronger security story | Breaks conceptual vs execution split | Left to execution track |

## Validation evidence

- Pattern-only: consistent with [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]] preimage table and [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]] validator language.
- No external research this run (pre-deepen research skipped by util/conf policy).

## Links

- Tertiary slice: [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]]
- Parent secondary: [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]]
- Workflow anchor: `2026-03-29 19:35` — Target `Phase-1-2-1-snapshot-preimage-binding`
