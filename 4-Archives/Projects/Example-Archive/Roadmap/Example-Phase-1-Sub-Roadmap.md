---
title: Example Phase 1 — Sub-roadmap
created: 2026-03-02
tags: [roadmap, example, phase1]
project-id: Example
roadmap: true
para-type: Project
status: active
roadmap-level: subphase
phase-number: 1
priority: medium
dependencies: []
progress: 0
highlight_perspective: geosynchronous-view
links: ["[[Example-Roadmap]]"]
---

# Example Phase 1 — Sub-roadmap

Dedicated sub-roadmap for Phase 1 of the example project. Focus: establish project scaffolding (folders, README, initial configuration) so later phases can build on a clean base.

```dataview
TASK
WHERE file.path = this.file.path AND !completed
```

## Tasks

- [ ] Set up project ^phase1-setup-sub
  - [ ] Create folder structure ^phase1-folders-sub (depends on: ^phase1-setup-sub)
  - [ ] Add README ^phase1-readme-sub (depends on: ^phase1-setup-sub)
- [ ] Define scope ^phase1-scope-sub

