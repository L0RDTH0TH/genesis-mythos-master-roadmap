---
title: "CDR — Phase 4.1.3 consumer-surface framing and presentation-time validation"
created: 2026-04-03
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-413-gmm-20260331T001700Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 4.1.3 consumer-surface framing and presentation-time validation

## Summary

Minted tertiary **4.1.3** under secondary **4.1**, defining **presentation envelope** fields (SeamId, ObservationChannel, authority, freshness/drift, emphasis, optional reconciliation tag), **presentation-time validation** as read-only legibility checks (explicitly **not** Phase **2.3** PreCommit gates), and **operator legibility** for compare-lanes, with **GWT-4.1.3-A–K** narrowing **GWT-4.1.2-***. **Tertiary chain 4.1.1–4.1.3** is structurally complete; next structural work is **secondary 4.1 rollup** (NL + GWT parity).

## PMG alignment

Preserves **one sim truth** at the consumer boundary: validation adjusts **withhold/degrade/disclose** for **presentation** only; does not import **2.3** commit authority or re-derive **3.1.4** checkpoints.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **A — Reuse PreCommit labels for UI** | Familiar vocabulary | Collapses presentation vs commit authority | Forbidden merge with **2.3** |
| **B — Single global envelope for both lanes** | Minimal duplication | Hides lane-specific emphasis | Conflicts with **4.1** dual-lane charter |
| **C — Defer all validation to execution** | Smaller conceptual surface | Weak operator legibility at handoff | **4.1.3** locks envelope + predicates now |

## Validation evidence

- Pattern-only: continuity from [[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]], [[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]], [[Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140]] (boundary: no gate reuse); no external research synth.

## Links

- Workflow anchor: **2026-04-03 21:10** deepen — Target **Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation** — `queue_entry_id: followup-deepen-phase4-413-gmm-20260331T001700Z`
