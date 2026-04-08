---
title: Decision Tracking Framework
created: 2026-04-08
tags: [second-brain, decisions, roadmap, governance]
source: Second-Brain governance enhancement
---

# Decision tracking framework

Canonical hybrid contract for decision tracking across roadmap projects:

- Global canonical specification lives in `3-Resources/Second-Brain/Docs/`.
- Per-project mirrors/templates live under each project roadmap area and must backlink to this spec.

## Goals

- Keep decision history append-only and auditable.
- Capture tradeoffs (`why this` vs `why not that`) for non-trivial choices.
- Preserve parse-stable labels for automation and validator checks.
- Link decisions to execution evidence and user-facing world impacts.

## Core invariants

1. **Append-only amendments**
   - Do not rewrite old rationale blocks in place.
   - Add dated amendment entries under an Amendments section when policy changes.
2. **Tradeoff table required for non-trivial decisions**
   - If the decision has meaningful alternatives, include an options table.
3. **Rationale required**
   - Must explicitly state why the selected option was chosen and why others were rejected.
4. **Linkages required**
   - Include relevant phase notes, execution state files, validator outputs, and queue IDs when applicable.
5. **World Impact field**
   - Optional globally, but required when decisions affect living-world or player-facing behavior.

## Decision template (canonical)

```markdown
# D-YYYY-MM-DD-short-name
**Decision Date**: YYYY-MM-DD
**Category**: Frontend | Backend | Simulation | React-Engine | Persistence | Platform | Process
**Status**: Active | Amended | Superseded | Archived
**World Impact**: Optional globally. Required when decision touches player-facing flow, persistence behavior, react matrix, pacing, codex/lore, or known blindspots.

## Context and Goal
Short problem statement and desired outcome.

## Options Considered
| Option | Selected? | Pros | Cons | Why accepted/rejected |
|---|---|---|---|---|
| A: ... | Yes/No | ... | ... | ... |
| B: ... | Yes/No | ... | ... | ... |
| C: ... | Yes/No | ... | ... | ... |

## Selected Approach and Rationale
Explicitly state why this option is preferred over alternatives.

## Linkages and Affected Systems
- Roadmap notes / phase slices:
- Execution references (`workflow_state-execution.md`, `roadmap-state-execution.md`):
- Validator reports:
- Queue ids / telemetry ids:
- Frontend flows affected:
- Lore / markdown hook linkage:

## Execution Notes
- Next gate or validation step:
- Known blockers/deferrals:

## Amendments (append-only)
- YYYY-MM-DD: ...
```

## Worked example (2026-04-08 UX authority)

Use `D-2026-04-08-frontend-player-ux-authority` as reference:

- Decision captures GTA-style multi-PC possession flow, DM-gated scheduling, mobile spectator non-goal, and markdown lore surface boundaries.
- World Impact should name concrete user-facing outcomes (for example: PC swap immersion continuity, scheduling authority lane clarity, cognitive-load reduction).
- Linkages should include conceptual 4.2 note, amendment note, execution stub/state references, and any validator report affecting rollout confidence.

## Required fields by decision type

- **Always required:** Decision Date, Category, Status, Context, Selected Approach and Rationale.
- **Required for non-trivial decisions:** Options Considered table.
- **Required for front-end/living-world decisions:** World Impact + at least one frontend or lore linkage.
- **Required for execution-meaningful decisions:** execution state linkages + next gate/blocker note.

## Automation compatibility

This framework augments (does not replace) grep-stable patterns in:

- `Operator pick logged (YYYY-MM-DD): ...`
- `Conceptual authority decision (YYYY-MM-DD): ...`
- `Decision record (deepen): ...`

See [Decisions-Log-Operator-Pick-Convention](3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention.md).

## Grok visibility policy

When decisions are intended to be Grok-visible, completion requires GitHub parity:

1. export
2. commit
3. push
4. verify target branch paths on GitHub

Local vault-only decision updates are draft for Grok coordination until published.
