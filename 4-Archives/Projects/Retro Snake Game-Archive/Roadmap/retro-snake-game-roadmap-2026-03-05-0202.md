---
title: Retro Snake Game Roadmap
roadmap-level: master
phase-number: 0
project-id: Retro Snake Game
status: active
priority: high
progress: 0
created: 2026-03-05
tags: [roadmap, project, retro-snake-game]
para-type: Project
links:
  - "[[retro-snake-game-roadmap-moc]]"
roadmap_generation_status: complete
---

# Retro Snake Game Roadmap

> [!info] Generation provenance  
> Generated from `[[Source-snake-roadmap-2026-03-05-0202]]` on `2026-03-05T02:20:00Z`  
> Wrapper: `[[Decision-for-snake-roadmap--2026-03-05-0216]]` (`wrapper_type: roadmap`, option A)  
> Guidance: No additional guidance provided.  
> Intent confidence: high.

Source: [[Source-snake-roadmap-2026-03-05-0202]]

## Phase 1 — Game Grid

Design and tune the fixed grid that the snake moves on. Decide on the cell size and overall dimensions (e.g. 20×20) and whether the game uses wrap-around edges or solid walls that cause game over on collision.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Retro Snake Game/Roadmap/Phase-1-Game-Grid"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 2 — Snake

Define the snake representation and movement rules. Implement the body as linked segments, ensure the head moves in four directions on the grid, and update growth behavior when the snake eats food.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Retro Snake Game/Roadmap/Phase-2-Snake"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 3 — Food / Apple

Implement spawning and lifecycle for food items. Randomly spawn apples on empty grid cells, ensure they disappear when eaten, and immediately respawn a new apple without blocking the snake.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Retro Snake Game/Roadmap/Phase-3-Food-Apple"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 4 — Collision Detection

Handle all failure conditions for the snake. Detect when the head collides with its own body segments and when it hits walls in non-wrap mode, triggering game over and passing the right information to the UI.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Retro Snake Game/Roadmap/Phase-4-Collision-Detection"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 5 — Scoring & UI

Design the scoring model and on-screen feedback. Track score as `length - 1`, add a persistent high-score, and implement basic UI screens for in-game HUD, pause, and game-over states.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Retro Snake Game/Roadmap/Phase-5-Scoring-UI"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 6 — Controls & Game Loop

Implement the main game loop and input handling. Wire up arrow keys / WASD to direction changes, run the game at a constant tick rate, and support pausing and restarting the game cleanly.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Retro Snake Game/Roadmap/Phase-6-Controls-Game-Loop"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Related

- [[retro-snake-game-roadmap-moc]]
- [[Source-snake-roadmap-2026-03-05-0202]]

