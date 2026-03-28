---
title: Distilled core — Genesis Mythos Master
created: 2026-03-08
tags: [roadmap, genesis-mythos-master, distilled]
project-id: genesis-mythos-master
core_decisions: []
status: archived
para-type: Archive
---

# Distilled core

Compressed memory for resumption. Built from phase outputs after distill.

## Hierarchy rule (enforce always)

- Master MOC links to phase MOCs.
- Each phase note is MOC for its secondary sub-phases (folders + Dataview block).
- Each secondary note is MOC for its tertiary notes (folder + Dataview).
- Tertiary notes contain only tasks/checklists/pseudo-code (no further Dataview MOC).
- Use `subphase-index: "N.M"` for secondary, `"N.M.K"` for tertiary.
- Folder pattern: `Roadmap/Phase-N-.../Phase-N-M-.../Phase-N-M-K-....md`

## Dependency graph

(To be populated after phase distill.)

```mermaid
flowchart LR
  P1[Phase 1] --> P2[Phase 2] --> P3[Phase 3] --> P4[Phase 4] --> P5[Phase 5] --> P6[Phase 6]
```
