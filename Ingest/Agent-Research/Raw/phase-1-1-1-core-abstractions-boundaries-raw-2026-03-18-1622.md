---
created: 2026-03-18
tags: [research, agent-research, raw]
project_id: genesis-mythos-master
linked_phase: "Phase-1-1-1"
source_urls:
  - https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns
  - https://gafferongames.com/post/deterministic_lockstep
  - https://gafferongames.com/post/fix_your_timestep
  - https://gafferongames.com/post/floating_point_determinism
  - https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays
agent-generated: true
---

## Source: https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns
Key excerpt (ECS boundaries):
- Small components and composed features keep boundaries explicit.
- Qualify/disqualify work using queries/events so expensive setup happens when needed.

## Source: https://gafferongames.com/post/deterministic_lockstep
Key excerpt (determinism + checksums):
- Determinism here means bit-level identical results given the same initial condition and inputs.
- With deterministic lockstep, you can take a checksum at the end of each frame/tick to detect divergence.

## Source: https://gafferongames.com/post/fix_your_timestep
Key excerpt (fixed/semi-fixed timestep):
- Variable delta time can change simulation behavior (stability/feel issues).
- Use fixed `dt` steps (or semi-fixed clamping with an accumulator) so behavior doesn’t depend on render framerate.

## Source: https://gafferongames.com/post/floating_point_determinism
Key excerpt (FP determinism constraints):
- Floating point determinism is “yes, if…”: you must control compilation/architecture and the FP environment if you want bitwise reproducibility.

## Source: https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays
Key excerpt (replay-safe patterns):
- Make replay safe by isolating side effects; replay handlers should be idempotent.
- Use snapshots/checkpoints for restartability and apply filtering to avoid processing unrelated events.

