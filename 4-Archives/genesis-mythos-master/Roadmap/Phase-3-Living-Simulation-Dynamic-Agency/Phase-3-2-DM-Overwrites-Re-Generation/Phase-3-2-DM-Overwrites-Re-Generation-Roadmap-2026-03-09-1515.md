---
title: Phase 3.2 — DM Overwrites and Re-Generation Boundary
roadmap-level: secondary
phase-number: 3
subphase-index: "3.2"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-3-Living-Simulation-Dynamic-Agency-Roadmap-2026-03-08-2358]]"
---

## Phase 3.2 — DM Overwrites and Re-Generation Boundary

Define how DM overwrites work in-session (live tweaks) vs when major structural changes demand deliberate re-generation. Respect cost and intent: move tokens, shift weather, trigger events, whisper to NPCs for dynamic flair; terrain reshaping, biome relocation, or other structural changes require explicit re-generation of regions or the full world.

- [ ] Define live in-session overwrites: which simulation state (tokens, weather, events, NPC whispers) is writable by DM without re-generation; contracts and APIs.
- [ ] Define re-generation triggers: what counts as "major structural change"; when to queue or run region/full-world re-generation; how overwrites interact with persistence and replay.
- [ ] Specify overwrite application order and persistence: overwrites as patch layer vs baked into next commit; rollback and replay implications (see Phase 3.1.5).

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-Dynamic-Agency/Phase-3-2-DM-Overwrites-Re-Generation"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
