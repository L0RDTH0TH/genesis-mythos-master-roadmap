---
title: Phase 4 — Collision Detection
roadmap-level: phase
phase-number: 4
project-id: Retro Snake Game
status: active
priority: high
progress: 0
created: 2026-03-05
tags: [roadmap, retro-snake-game, phase]
para-type: Project
links:
  - "[[retro-snake-game-roadmap-2026-03-05-0202]]"
---

## Phase 4 — Collision Detection

Snake head hits body = game over; head hits wall (if no wrap) = game over. This phase centralizes collision checks so game state transitions are deterministic and easy to reason about.

- [ ] Implement self-collision detection for snake head vs body
- [ ] Implement wall collision behavior for non-wrap mode
- [ ] Trigger game-over state and events on collision

