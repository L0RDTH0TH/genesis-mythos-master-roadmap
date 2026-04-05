---
title: "CDR — Phase 5 primary checklist (rule system integration)"
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
validation_status: pattern_only
---

# Decision — Phase 5 primary NL checklist (rule system)

## Summary

Phase 5 primary establishes **NL design authority** for a **core rules engine**, **plugin ruleset registration**, **deterministic conflict resolution hooks**, and **ecosystem seams** (swap generators/events/styles) — **without** claiming execution plugin marketplace, CI, or full mod-sandbox closure (execution-deferred per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]).

## Alternatives considered

- **Monolithic rules blob:** rejected — extensibility and community remixing require explicit **plugin boundary** + **versioned ruleset manifests** (NL at primary; shapes under **5.1+**).
- **Rules in rendering layer:** rejected — rules consume **Phase 4** mode/orchestration **signals** and **sim-visible** facts from Phase 3 handoff paths; they do not own camera or checkpoint semantics.

## PMG alignment

Advances the master goal toward **toolable, deterministic, operator-legible** world-building: rules are **data-driven** where possible and **replay-stable** relative to Phase 2 commit boundaries.

## Validation evidence

Primary note [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]] — Scope / Behavior / Interfaces / Edge / Open Q / **GWT-5-A–K** scaffold; `handoff_readiness` **85**; queue **`user_guidance`** referencing **Phase 4.1** rollup was **stale** — reconciled to **Phase 5 primary** per Layer 1 **`effective_target`**.
