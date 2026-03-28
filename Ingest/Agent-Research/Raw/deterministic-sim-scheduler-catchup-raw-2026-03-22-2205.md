---
source_urls:
  - https://andreleite.com/posts/2025/game-loop/fixed-timestep-game-loop/
  - https://mosaik.readthedocs.io/en/develop/tutorials/sametimeloops.html
linked_phase: Phase-3-1-2
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, raw]
agent-generated: true
---

## Source: https://andreleite.com/posts/2025/game-loop/fixed-timestep-game-loop/

Excerpt (trimmed): Describes accumulator pattern, spiral of death when physics step real time exceeds dt, clamping accumulator / frame time (~250ms) to prefer slow-motion over freeze; integer nanosecond time bases for determinism; interpolation alpha = accumulator/dt for render. Cites Fix Your Timestep, Box2D determinism, Game Programming Patterns game loop.

(Full page fetched 2026-03-22 via research-agent-run Step 2; see live URL for demos and code blocks.)

## Source: https://mosaik.readthedocs.io/en/develop/tutorials/sametimeloops.html

Excerpt (trimmed): Co-simulation at different time scales; **simulator groups** with **weak** connections; a hidden second tier of time advances sub-steps inside the group; **only when the group reaches the next main step** do outside simulators receive latest outputs—they do not see all internal sub-steps. Useful analogy for “fast physics inside one `tick_epoch` commit” vs publishing only at major steps.
