---
title: Raw — Phase 2.2 intent parser hooks determinism integration sources
created: 2026-03-20
tags: [research, agent-research, raw, genesis-mythos-master]
source_urls:
  - https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html
  - https://www.gamedeveloper.com/programming/developing-your-own-replay-system
  - https://json-schema.org/draft/2020-12
  - https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html
  - https://en.wikipedia.org/wiki/Parsing_expression_grammar
linked_phase: Phase-2-2
project_id: genesis-mythos-master
agent-generated: true
---

## Source: https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html

Given the same hardware and Isaac Sim (and consequently PhysX) version, the simulation produces identical results for scenes with rigid bodies and articulations; however results can vary across different hardware configurations due to floating point precision and rounding errors. Isaac Lab provides a deterministic simulation by using the same random seed for the simulation environment and the physics engine; at construction time, `configure_seed()` sets the random seed globally across CPU/GPU libraries (e.g. PyTorch, NumPy). The docs also warn that GPU work scheduling and runtime changes to simulation parameters can alter the order of operations and introduce minor floating-point differences; do such changes at setup time before stepping begins.

## Source: https://www.gamedeveloper.com/programming/developing-your-own-replay-system

The “deterministic replay” approach is to record only the essential inputs (e.g. controller inputs and initial conditions) and rely on deterministic code behavior to reproduce the same simulation over time, instead of snapshotting full object state every frame. The article frames determinism as requiring a clear boundary: you must either make the relevant parts deterministic or explicitly keep nondeterministic subsystems (sound/visual effects, etc.) from affecting deterministic game objects. It also emphasizes restoring the RNG seed in the replay and using different RNG behavior for deterministic vs nondeterministic parts so non-determinism can’t leak into the deterministic border.

## Source: https://json-schema.org/draft/2020-12

JSON Schema defines declarative validation rules for structured JSON data, and Draft 2020-12 is a comprehensive update that supports evolving contracts while remaining explicit about schema vocabulary/version changes. The spec describes how the draft includes features such as vocabulary separation (e.g. `format` as assertion vs annotation) and dynamic references/anchors, and it provides guidance for draft-level compatibility so validators can enforce stable contracts across versions.

## Source: https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html

Hypothesis saves failing test cases to an ExampleDatabase (by default under a local `.hypothesis` directory) so that once a failure is found, the next test run replays that failing input deterministically. The docs describe the database-based replay mechanism and also note ways to reproduce failures using mechanisms like `@example` or `@reproduce_failure` (including sharing the database across machines/devs for CI replay).

## Source: https://en.wikipedia.org/wiki/Parsing_expression_grammar

A parsing expression grammar (PEG) is a recognition-based formal grammar where the choice operator is ordered: if the first alternative succeeds, subsequent alternatives are ignored. This ordered-choice semantics makes PEG parsing deterministic/unambiguous in a way that differs from CFG choice ambiguity; grammar ordering therefore controls which parse tree is selected (or whether parsing fails) and gives practical levers for defining predictable parse outputs for DSLs (like an intent language).

