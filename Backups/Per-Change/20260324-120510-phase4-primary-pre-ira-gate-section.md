---
title: Phase 4 — Perspective Split and Control Systems
roadmap-level: primary
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "4"
links:
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
---

## Phase 4 — Perspective Split and Control Systems

Deliver role-specific control schemes: locked first-person immersion for players and fast free-cam plus orthographic precision tools for DMs. Ensure seamless transitions so viewpoint changes never break decision flow.

- [ ] Implement player first-person interaction rig
- [ ] Implement DM free-cam + orthographic toggle rig
- [ ] Add camera transition interpolator and validate UX continuity

## Subphases & notes

- **4.1 (secondary — player-first spine):** [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]] — **ARCH-FORK-02** per **D-059**; first Phase 4 deepen after operator advance (**D-062** traceability).

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
