---
title: "CDR — Deepen Phase 1.2.2 dry-run waiver and bypass policy"
created: 2026-03-29
tags: [roadmap, conceptual-decision-record, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-2-Dry-Run-Waiver-and-Bypass-Policy-Roadmap-2026-03-29-1940]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-after-1-2-1-20260329T193500Z
master_goal: "[[Genesis-mythos-master-goal]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 1.2.2 deepen (2026-03-29)

## Summary

Minted tertiary **1.2.2** to specify a **waiver ladder** (standard / expedited / emergency), **audit coupling** for `dry_run_skipped`, **conflict rules** when **1.2.1** tickets require dry-run, and **cooldown intent**—without RBAC or storage schemas (**D-027**, execution-deferred).

## PMG alignment

Supports PMG **dry-run before commit** by making skips **explicit, attributable, and gated** so iteration speed does not erase traceability.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Ban all dry-run skips | Maximum safety | Blocks legitimate hotfix / inner-loop speed | Parent **1.2** already allows skip path in diagram; policy must exist |
| Merge waiver text into **1.2.1** only | Fewer files | Blurs binding vs policy concerns | **1.2.1** is commit preimage; **1.2.2** is policy layer |
| Encode RBAC here | Clearer enforcement story | Violates conceptual vs execution split | Roles stay labels until execution track |

## Validation evidence

- Pattern-only: extends [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]] mermaid and [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]] audit / ticket language.
- Pre-deepen research skipped (util under 30 and confidence veto per prior row policy).

## Links

- Tertiary slice: [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-2-Dry-Run-Waiver-and-Bypass-Policy-Roadmap-2026-03-29-1940]]
- Parent secondary: [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]]
- Prior tertiary: [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]]
- Workflow anchor: `2026-03-29 19:40` — Target `Phase-1-2-2-dry-run-waiver-bypass`
