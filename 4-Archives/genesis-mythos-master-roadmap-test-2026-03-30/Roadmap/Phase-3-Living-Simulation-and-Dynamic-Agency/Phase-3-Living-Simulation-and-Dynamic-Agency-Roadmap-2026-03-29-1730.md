---
title: Phase 3 — Living Simulation and Dynamic Agency
roadmap-level: primary
phase-number: 3
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

## Phase 3 — Living Simulation and Dynamic Agency

Deliver tick-based simulation (weather, NPC agendas, factions, persistence), distinguish live-session DM tweaks from deliberate re-generation for structural change, add vitality and consequence mechanics for long campaigns, and keep simulation independent of the render path for preview vs full fidelity.

- [ ] Simulation tick architecture and state persistence model.
- [ ] DM overwrite taxonomy (live vs regen-required) aligned with PMG.
- [ ] Consequence / surprise hooks without breaking player immersion contract.
- [ ] Sim-only preview channel vs full 3D session path.

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
