---
title: Phase 2 — Procedural Generation and World Building
roadmap-level: primary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-29-1730]]"
handoff_readiness: 70
handoff_gaps:
  - "Primary-only slice after restart; add secondaries on deepen"
---

## Phase 2 — Procedural Generation and World Building

Build the pipeline from seed parsing through terrain, biomes, POIs, entities, and simulation bootstrap; wire player/DM intents into systemic hooks (reputation, events, environment); support collaborative refinement of proposed scaffolds; validate that agency produces subtle, persistent ripples without hardcoded narrative content.

- [ ] Implement or specify end-to-end generation pipeline stages with override points.
- [ ] Intent loop: parse lore/backstory into hook graph and probability/state modifiers.
- [ ] Collaborative dialogue UX for scaffold accept/refine (contracts only at conceptual track).
- [ ] Session-level tests for emergence (environment/event feedback from choices).

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
