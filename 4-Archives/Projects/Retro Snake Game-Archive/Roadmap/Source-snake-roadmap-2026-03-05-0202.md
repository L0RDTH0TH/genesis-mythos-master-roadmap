---
title: Retro Snake Game Roadmap
created: 2026-03-05 02:02
tags:
  - ingest
  - raw-capture
  - no-template
para-type: Ingest
status: ingest
is_roadmap: true
suggested_project_name: Retro Snake Game
decision_candidate: true
proposal_path: Ingest/Decisions/Decision-for-snake-roadmap--2026-03-05-0216.md
decision_priority: high
---

# Snake Game – High-Level Systems

## 1. Game Grid
Fixed grid (e.g. 20×20 cells), wrap-around walls or solid walls option.

## 2. Snake
Body as linked segments, head moves in 4 directions, grows when eating.

## 3. Food / Apple
Random spawn on empty cell, disappear when eaten, new one spawns.

## 4. Collision Detection
Snake head hits body = game over; head hits wall (if no wrap) = game over.

## 5. Scoring & UI
Score = length - 1, display current score, high score, game over screen.

## 6. Controls & Game Loop
Arrow keys / WASD, constant tick rate, pause/restart.

# No template selected

Paste your raw capture here. You can refactor or re-template this later.

