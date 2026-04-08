---
title: Decision Template (Sandbox)
created: 2026-04-08
tags: [decision-template, roadmap, sandbox]
source: "[[3-Resources/Second-Brain/Docs/Decision-Tracking-Framework]]"
---

# Decision template (sandbox)

Use this template for new `D-*` entries in the sandbox roadmap decisions log.

## Required blocks

- Decision id and date
- Context and goal
- Options considered (A/B/C for non-trivial decisions)
- Why selected / why rejected
- Linkages (phase, execution state, validator, queue id as applicable)
- World Impact (required for front-end/living-world decisions)

## Skeleton

```markdown
- **D-YYYY-MM-DD-short-name:** one-line summary.
  - **World Impact:** ...
  - **Options considered:** Option A ... | Option B ... | Option C ...
  - **Why selected:** ...
  - **Why rejected:** ...
  - **Linkages:** [[phase-note]], [[Execution/workflow_state-execution]], `queue-id`, `.technical/Validator/...`
  - **Amendment (YYYY-MM-DD):** ... (append-only)
```
