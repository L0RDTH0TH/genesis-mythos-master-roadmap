---
title: Example Roadmap
created: 2026-02-28
tags: [roadmap, example]
project-id: Example
roadmap: true
para-type: Project
status: active
roadmap-level: phase
phase-number: 1
priority: medium
dependencies: []
progress: 0
highlight_perspective: geosynchronous-view
links: ["[[Resources Hub]]"]
---

# Example Roadmap

Sample structure for [[3-Resources/Roadmap-Standard-Format]]. Use block-IDs (`^id`) and `depends on: ^id` for reliable Task Complete validation.

## Phase 1

This phase sets up the basic project structure and scaffolding so later work has a clean foundation. The goal is to create the folders, README, and initial configuration before adding features.

```dataview
TASK
WHERE file.path = this.file.path AND !completed
```

- See also: [[Example-Phase-1-Sub-Roadmap]] for a dedicated sub-roadmap version of this phase.

- [ ] Set up project ^phase1-setup
  - [ ] Create folder structure ^phase1-folders (depends on: ^phase1-setup)
  - [ ] Add README ^phase1-readme (depends on: ^phase1-setup)
- [ ] Define scope ^phase1-scope

## Phase 2

High-level work for implementing the core features (API, tests, and review) of the example project.

- [ ] Implement core ^phase2-core
  - [ ] API layer ^phase2-api (depends on: ^phase2-core)
  - [ ] Tests ^phase2-tests (depends on: ^phase2-core)
- [ ] Review and ship ^phase2-ship

## Phase 3

Follow-up iteration on feedback once the initial phases are complete.

- [ ] Iterate from feedback ^phase3-iterate

> [!feedback]
> Add notes here; re-queue via EAT-QUEUE for refinement.
