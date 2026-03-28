---
title: Phase 3.1.4 — Faction and Relationship State
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.4"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-3-1-Tick-Based-Simulation-Layer-Roadmap-2026-03-09-1405]]"
---

## Phase 3.1.4 — Faction and Relationship State

Specify faction and relationship state: reputation graphs, tension, and events triggered by thresholds. Mid-technical: interfaces and algorithm sketches; runs in tick Phase 3 (after NPCs).

### Tasks

- [ ] **Reputation graphs**
  - [ ] Per-entity or per-faction reputation: directed or undirected edges (A → B: score, or faction ↔ faction). Scores numeric or tiered; updated only in tick Phase 3.
  - [ ] Intent hooks: player/DM intents can seed or modify reputation edges (e.g. "player faction X has +20 with faction Y"); resolver applies deltas at defined points (session start, quest complete).
  - [ ] Read-only API for systems that need "relationship between A and B": `get_reputation(entity_a, entity_b)` or `get_faction_standing(faction_id, target_id)`.
- [ ] **Tension and thresholds**
  - [ ] Tension as derived or stored scalar per pair or per faction: conflict level, trade openness, etc. Thresholds define bands (e.g. 0–30 hostile, 31–60 wary, 61–100 friendly).
  - [ ] Threshold-triggered events: when reputation or tension crosses a threshold (e.g. drops below 30), emit event or set flag for event bus / script hooks. No hardcoded narrative — only "event type + payload" for downstream consumers.
- [ ] **Events triggered by thresholds**
  - [ ] Declarative list per faction or global: (condition, event_id, payload). Condition = e.g. "reputation(A,B) < 30" or "tension(faction) > 0.8". On tick Phase 3, evaluate conditions; if newly true, enqueue event. Idempotent per tick (once per threshold cross).
  - [ ] Event bus contract: events are typed and carry minimal payload (entity ids, faction ids, old/new values); simulation and DM overwrites can subscribe.
- [ ] **Integration with tick phases**
  - [ ] Faction and relationship updates run in tick Phase 3 (after environment and NPCs). Same tick boundary as Phase 3.1.1; consume prior phase state as read-only.

### Interface sketch

- **ReputationGraph** (read-only view):
  - `get_reputation(from_id, to_id): float | tier`
  - `get_tension(faction_id or pair): float`
- **ThresholdRegistry**: list of (condition, event_id, payload); evaluated once per tick Phase 3.
- **FactionState**: written only by tick Phase 3; exposes no direct write API from game logic.

### Invariants

- Faction and relationship state advance only in tick Phase 3; no writes from game logic outside the tick driver.
- Same tick index ⇒ same reputation/tension and same threshold-evaluated events for deterministic replay (given same intent and seed).
