---
title: Phase 4.2.4 — Input Loop Seam
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.4"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-2-DM-Controls-Roadmap-2026-03-09-1903]]"
---

## Phase 4.2.4 — Input Loop Seam

DM input (flight, toggle, tools) flows into DM intent path only; isolated from player intent (Phase 4.1.5). Document boundary so player and DM input never cross. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Role-based input routing** — Input layer routes by active role: DM → DM intent path (flight, ortho toggle, fog/token tools); Player → player intent path (WASD, look, interaction raycasts). No shared intent queue between roles.
- [ ] **Boundary contract** — Document the seam: which systems consume DM input vs player input. Phase 4.1.5 (Input Loop Seam) defines player side; this note defines DM side.
- [ ] **Tool invocations** — DM-only actions (e.g. place token, paint fog, trigger event) emit as DM intents; never as player intents. Ensure UI and shortcuts respect role.

### Interface sketch

- **DMInputHandler**: Consumes input when role = DM; produces DMIntent (flight_delta, toggle_ortho, tool_action, etc.). Not visible to player input pipeline.
- **Intent paths**: Two distinct pipelines: PlayerIntent → player systems (Phase 4.1); DMIntent → DM systems (this phase). No cross-wire.
