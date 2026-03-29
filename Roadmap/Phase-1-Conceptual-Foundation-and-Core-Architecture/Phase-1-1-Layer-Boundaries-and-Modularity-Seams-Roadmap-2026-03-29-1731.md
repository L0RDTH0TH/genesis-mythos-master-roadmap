---
title: Phase 1.1 — Layer boundaries and modularity seams
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-29-1730]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730]]"
handoff_readiness: 70
handoff_gaps:
  - "Draft slice; deepen to pseudo-code/interfaces on execution track"
---

## Phase 1.1 — Layer boundaries and modularity seams

Separate **world state**, **simulation**, **rendering**, and **input** with explicit dependency direction. Document **generation graph** stage boundaries and **intent resolver** injection points. Enumerate **replaceability seams** (generation stages, rule hooks, event bus) as checklist targets for deepen.

- [ ] Layer diagram + allowed dependencies (one-way arrows).
- [ ] Stage contract table (inputs/outputs/failure modes) — stub OK until deepen.
- [ ] Intent → hook mapping overview (reputation, events, env state).
