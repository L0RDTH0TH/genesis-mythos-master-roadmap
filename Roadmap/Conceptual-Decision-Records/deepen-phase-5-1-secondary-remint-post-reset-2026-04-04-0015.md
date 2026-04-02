---
title: CDR — Phase 5.1 secondary re-mint (post vault reset)
created: 2026-04-04
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-04-0015]]"
amends_section: "Full secondary — rule primitives, plugin host, deterministic conflict precedence"
queue_entry_id: followup-deepen-phase5-51-mint-gmm-20260403T231000Z
validation_status: pattern_only
---

## Decision

After manual removal of the pre-reset Phase **5.1** roadmap chain (secondary + tertiaries **5.1.1–5.1.3**), **re-mint secondary 5.1** as the live conceptual contract for **rule primitives**, **plugin host** admission/reject surfaces, and **deterministic conflict precedence** with **operator-visible** resolution traces aligned to **4.1.3**.

## PMG alignment

Phase **5** consumes **3.2.1** **ObservationChannel** / **authority_class**, **4.2.x** orchestration signals as **read-only triggers**, and **4.1.3** presentation envelope for explanations — without authoring Phase **2** commits or mutating **3.1.4** checkpoint authority.

## Alternatives considered

- **Reconstruct tertiaries before secondary:** rejected — secondary must exist first as slice parent; tertiaries **5.1.1+** follow in deepen order.
- **Unfreeze and edit pre-reset file paths:** rejected — files were removed; new slug **2026-04-04-0015** avoids collision with historical wikilinks.

## Evidence

- Live note: [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-04-0015]]
- Primary links updated: [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]
- Historical thematic anchor (pre-reset): [[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rule-primitives-plugin-host-conflict-2026-04-03-2310]]

## Validation

`pattern_only` — no external research synthesis this run; authority from Phase **5** primary + Phase **3–4** upstream notes + historical CDRs.
