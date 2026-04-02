---
title: Phase 6 — Prototype Assembly, Testing, and Iteration
roadmap-level: primary
phase-number: 6
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

## Phase 6 — Prototype Assembly, Testing, and Iteration

Assemble the Q3 2026 horizon prototype: single-player playable slice, one ruleset, full perspective split, live DM overwrites, one player intent round-trip, basic living simulation (weather + simple NPC schedules), and visible modding seams; embed provenance/traceability and close the feedback loop on immersion, agency, and modularity.

- [ ] Vertical slice integration checklist vs PMG target scope.
- [ ] Performance dry-run and validity gates before commit-to-world.
- [ ] In-game or export inspection of provenance (inputs, modules, seeds).
- [ ] Playtest feedback routing into roadmap/decisions log.

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
