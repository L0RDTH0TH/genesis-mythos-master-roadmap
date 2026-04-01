---
title: "CDR — Phase 5.1 secondary (rule primitives, plugin host, conflict precedence)"
created: 2026-04-03
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]]"
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
validation_status: pattern_only
---

# Decision — Phase 5.1 secondary (rules kernel surface)

## Summary

Phase 5.1 establishes **NL design authority** for **rule primitives** (**RuleOutcome**-shaped records, evaluation schedule relative to tick/session), **plugin host** (manifest admission, version pin, deterministic load failure classes), and **deterministic conflict precedence** with **operator-visible** explanation paths routed through **4.1.3** legibility—**without** bypassing Phase **2** commit / deny / defer semantics or **3.1.4** checkpoint authority.

## Alternatives considered

- **Rules embedded in UI layer:** rejected — rules consume **sim-visible** + **4.2** orchestration signals as **triggers**, not as persistence writers.
- **Ad-hoc conflict resolution:** rejected — requires **precedence class** + single winner + visible diff at NL.

## PMG alignment

Advances the master goal toward **toolable, deterministic, operator-legible** world-building: rules are **data-driven** where possible and **replay-stable** relative to Phase **2** lineage and Phase **3** observation authority.

## Validation evidence

Secondary note [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]] — **GWT-5.1-A–K** narrowed vs primary **GWT-5-A–K**; queue **`user_guidance`** referencing **Phase 4.1** rollup was **stale** — reconciled to **mint secondary 5.1** per Layer 1 **`effective_target`** + **`gate_signature: structural-phase-5-secondary-5.1`**.
