---
title: Phase 4.1.4 — Sensory and Feedback
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.4"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-1-Player-Perspective-Roadmap-2026-03-09-1854]]"
---

## Phase 4.1.4 — Sensory and Feedback

Visual/audio feedback for interactions and proximity (ambient, cues). Optional: simple feedback channel so simulation or narrative can push "sense" events to the player view. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Interaction feedback** — On successful interact: short visual/audio cue (e.g. sound, particle, UI flash). On hover (raycast hit): highlight and prompt (Phase 4.1.3). Consistent with project style.
- [ ] **Proximity / ambient** — Optional: ambient cues when near POIs or entities (e.g. sound radius, subtle VFX). Define radius and priority so multiple sources blend or one wins.
- [ ] **Sense event channel** — Optional: simulation or narrative can push events (e.g. "sense_danger", "sense_lore") to the player view. Consumer displays a brief cue (icon, text, sound). Contract: event type + optional payload; no mandatory implementation for MVP.

### Interface sketch

- **FeedbackBus** (optional): `emit_sense(event_type: string, payload?: object)`. Player view subscribes and maps event_type to visual/audio. No guarantee of delivery order; fire-and-forget.
- **InteractionFeedback**: `on_interact_success(entity_id, action)`, `on_hover_enter(entity_id)`, `on_hover_exit()`. Used by interaction system to trigger cues.
