---
title: Pong Game Roadmap
roadmap-level: master
phase-number: 0
project-id: Pong-Game
status: active
priority: high
progress: 0
created: 2026-03-05
tags: [roadmap, project, pong-game]
para-type: Project
links: ["[[Pong-Game-Roadmap-MOC]]"]
---

# Pong Game Roadmap

Source: [[Source-Pong-Game-Roadmap-Outline--2026-03-05-0614]]

## Phase 1 — Paddle Controls

Player paddle movement (up/down), AI opponent paddle.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Pong-Game/Roadmap/Phase-1-Paddle-Controls"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 2 — Ball Physics

Ball velocity, bounce off walls/paddles, speed ramp-up.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Pong-Game/Roadmap/Phase-2-Ball-Physics"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 3 — Collision & Scoring

Ball past paddle = score, reset ball position.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Pong-Game/Roadmap/Phase-3-Collision-Scoring"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 4 — UI & Game Loop

Score display, win/lose conditions, restart.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/Pong-Game/Roadmap/Phase-4-UI-Game-Loop"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Related

- [[Pong-Game-Roadmap-MOC]]
- [[Source-Pong-Game-Roadmap-Outline--2026-03-05-0614]]
