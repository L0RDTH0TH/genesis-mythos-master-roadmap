---
title: Decisions Log — genesis-mythos-master
created: 2026-03-29
tags: [roadmap, decisions, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
status: active
---

# Decisions log — genesis-mythos-master

## Decisions

- Phase 0: initialized 2026-03-29 — `workflow_state`, `roadmap-state`, `decisions-log`, `distilled-core`, master + six phase roadmaps + MOC created from [[Genesis-mythos-master-goal]] (PMG unchanged in project root per operator constraint). Queue: `roadmap-setup-gmm-restart-20260329T160000Z`.
- **D-027 (2026-03-21; migrated 2026-03-29):** **Stack-agnostic contract; engine and primary language TBD:** Roadmap artifacts define **cross-runtime contracts** (determinism, replay, authoritative state, generation/manifest boundaries, CI goldens)—**not** a chosen game engine, renderer, or implementation language. Citations and links to Unity, Godot, Bevy, Unreal, Rust, pytest, etc. in phase or research notes are **illustrative prior art or tooling analogies** unless a **later explicit decision** adopts a stack. **Do not infer the product’s engine or language from examples or sources.** **Authoritative prior row:** [[4-Archives/genesis-mythos-master-restart-2026-03-29/Roadmap/decisions-log|archived decisions-log (pre-restart)]] (same wording). **PMG pointer** at [[Genesis-mythos-master-goal]] Technical Integration remains valid for this live log row.

**Operator picks:** For grep-stable machine preflight ([[3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention|Decisions-Log-Operator-Pick-Convention]]), log dated sub-bullets under each **D-*** row, e.g. `**Operator pick logged (YYYY-MM-DD):** … — **Option A** | **Option B**`.

## Conceptual autopilot

- **Autopilot (deepen):** Refined Phase 1 **primary** container with full NL handoff checklist (Scope through Pseudo-code readiness), advanced cursor **1 → 1.1**, aligned with queue `user_guidance` (fresh tree / begin Phase 1 conceptual foundation). `queue_entry_id: resume-deepen-gmm-begin-buildout-20260329T180000Z`, `effective_track: conceptual`, `need_class: missing_structure` (Layer 1 hints).
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-primary-nl-checklist-2026-03-29-1800]] — `queue_entry_id: resume-deepen-gmm-begin-buildout-20260329T180000Z` — validation: pattern_only
- **Autopilot (deepen):** Phase **1.1** — layer/gen-graph **Mermaid** diagrams, **stage contract** stub table, **intent→hook** map; nested **Research** consumables inlined under Research integration; **D-027** preserved. `queue_entry_id: resume-deepen-gmm-phase11-followup-20260329T183600Z`, `effective_track: conceptual`, `need_class: missing_structure`.
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-1-layer-diagrams-2026-03-29-1836]] — `queue_entry_id: resume-deepen-gmm-phase11-followup-20260329T183600Z` — validation: pattern_only
- **Autopilot (deepen):** Minted **1.1.1** tertiary [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-1-Replaceability-Seams-and-Hook-Surface-Roadmap-2026-03-29-1905]] under **Phase-1-1-Layer-Boundaries-and-Modularity-Seams/**; **S-L / S-G / S-H** seam catalog; cleared Phase 1.1 prior `#review-needed` structural waiver (no shallow-tree-only decision). **D-027** preserved. `queue_entry_id: resume-deepen-gmm-phase11-next-tertiary-or-waiver-20260329T190500Z`, `effective_track: conceptual`, `need_class: missing_structure`.
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-1-1-tertiary-seams-2026-03-29-1905]] — `queue_entry_id: resume-deepen-gmm-phase11-next-tertiary-or-waiver-20260329T190500Z` — validation: pattern_only
- **Autopilot (deepen):** Minted **1.1.2** tertiary [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-2-Event-Bus-Topology-and-Mod-Load-Order-Roadmap-2026-03-29-1915]] — partitioned event domains, bridge rules, mod-load **bands** (core → world → player → extension), conceptual sequencing for replay; builds on **1.1.1** **S-H/S-G**. **D-027** preserved. `queue_entry_id: resume-deepen-gmm-after-1-1-1-20260329T190500Z`, `effective_track: conceptual`, `need_class: missing_structure` (Layer 1).
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-1-2-event-bus-2026-03-29-1915]] — `queue_entry_id: resume-deepen-gmm-after-1-1-1-20260329T190500Z` — validation: pattern_only
- **Autopilot (deepen):** Advanced from **1.1.2** to peer secondary **1.2** per Layer 1 `missing_structure` / MOC; deepened [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]] — snapshot preimage table, dry-run↔commit gate diagram, provenance rule, checklist closure; **D-027** preserved; pre-deepen research **skipped** (low util path + confidence veto). `queue_entry_id: resume-deepen-gmm-after-1-1-2-20260329T193000Z`, `effective_track: conceptual`.
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-2-safety-snapshots-dryrun-2026-03-29-1930]] — `queue_entry_id: resume-deepen-gmm-after-1-1-2-20260329T193000Z` — validation: pattern_only
- **Autopilot (deepen):** Minted **1.2.1** [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]] — preimage→commit binding, boundary ticket closure, audit row minimum; **1.2** secondary gained Dataview **Tertiary notes** MOC + wikilink; **D-027** preserved; pre-deepen research **skipped** (util<30 + conf veto). `queue_entry_id: resume-deepen-gmm-after-1-2-20260329T193500Z`, `effective_track: conceptual`, Layer 1 `need_class: missing_structure`, `effective_target: 1.2.1`.
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-2-1-preimage-binding-2026-03-29-1935]] — `queue_entry_id: resume-deepen-gmm-after-1-2-20260329T193500Z` — validation: pattern_only
- **Autopilot (deepen):** Minted **1.2.2** [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-2-Dry-Run-Waiver-and-Bypass-Policy-Roadmap-2026-03-29-1940]] — dry-run **waiver ladder**, ticket/dry-run **conflict rule**, audit field shape for `dry_run_skipped`, cooldown **intent**; **1.2** secondary MOC + links updated; **D-027** preserved; pre-deepen research **skipped** (util&lt;30 + conf veto); Pass3 **inline_forward** `dispatch_ordinal=3`. `queue_entry_id: resume-deepen-gmm-after-1-2-1-20260329T193500Z`, `effective_track: conceptual`, Layer1 `need_class: missing_structure`.
- **Decision record (deepen):** [[Conceptual-Decision-Records/deepen-phase1-2-2-waiver-bypass-2026-03-29-1940]] — `queue_entry_id: resume-deepen-gmm-after-1-2-1-20260329T193500Z` — validation: pattern_only

## Handoff notes

- Add `#handoff-review` and `#handoff-needed` bullets here when hand-off-audit flags issues.
