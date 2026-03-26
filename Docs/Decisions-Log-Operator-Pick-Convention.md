---
title: Decisions-Log Operator-Pick Convention
created: 2026-03-22
tags: [second-brain, roadmap, decisions-log, automation]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
---

# Decisions-log operator-pick convention

Machine-assisted flows (e.g. **decisions-preflight** skill, Layer 1 EAT-QUEUE hand-off injection) rely on **grep-stable** phrases in each project’s `Roadmap/decisions-log.md`. Human narrative may surround these lines; parsers look for the patterns below.

## Conceptual vs execution lines

- **Conceptual (design authority):** **`## Conceptual autopilot`** bullets (see [[3-Resources/Second-Brain/Parameters|Parameters]] § Conceptual autopilot) and **Conceptual authority decision** (below) record **what the design track chose** next. They are **not** operator picks for repo/CI unless they explicitly say so.
- **Execution** (repo, CI, PR): use **`Operator pick logged`** under the relevant **D-*** row when a human **operator** commits to an option.

## Required patterns

### Conceptual authority decision (dated)

Use a **sub-bullet** under the relevant **D-*** row **or** under **`## Conceptual autopilot`** for major forks:

```markdown
  - **Conceptual authority decision (YYYY-MM-DD):** <short label> — <chosen direction in natural language> (optional `queue_entry_id`; wikilinks to phase notes)
```

Regex hint: `Conceptual authority decision \((\d{4}-\d{2}-\d{2})\):`

### Operator pick logged (dated)

Use a **sub-bullet** under the relevant **D-*** row:

```markdown
  - **Operator pick logged (YYYY-MM-DD):** <short label> — **Option A** | **Option B** (optional rationale; link PR/issue)
```

Examples:

- `**Operator pick logged (2026-03-22):** RegenLaneTotalOrder_v0 — **Option A**`
- `**Operator pick logged (2026-03-22):** SimulationRunControl_v0 replay header — **Option A**` (dedicated header block vs intent-only = B)

### Phase 4.1 architect fork

Under **D-059**, log explicitly:

```markdown
  - **Operator pick logged (YYYY-MM-DD):** ARCH-FORK-01 | **ARCH-FORK-02** — optional rationale
```

Use **`ARCH-FORK-01`** (shared DM + player shell first) or **`ARCH-FORK-02`** (player-first).

### D-037 facet manifest (defer / confirm)

Either:

- `**Operator confirm (YYYY-MM-DD):** mint facet-manifest-v0.md at Roadmap/facet-manifest-v0.md`  
or  
- `**Operator defer (YYYY-MM-DD):** facet-manifest-v0.md — do not mint until …`

## Regex hints (implementations)

Implementations may use case-sensitive or normalized ASCII; prefer matching the bold labels:

- `Operator pick logged \((\d{4}-\d{2}-\d{2})\):`
- `RegenLaneTotalOrder_v0.*Option ([AB])`
- `SimulationRunControl_v0|D-032.*Option ([AB])` (or row-specific wording)
- `ARCH-FORK-(01|02)`
- `Operator (confirm|defer) \((\d{4}-\d{2}-\d{2})\):.*facet-manifest`

Track **decision ids** (e.g. **D-044**, **D-032**, **D-059**, **D-037**) by **section heading** or **bold `**D-NNN**`** on the same bullet row.

## Drift semantics

**Stale surface:** downstream text (e.g. [[roadmap-state]] HOLD bullets) still says “until D-044 A/B” when `decisions-log` contains `Operator pick logged` for that decision. Preflight skills flag **stale_surfaces**; reconciliation is a separate human or Roadmap step.

## Conceptual autopilot vs D-ids

- **Routine next-action** choices: append-only bullets under **`## Conceptual autopilot`** (timestamp, `chosen_action`, evidence).
- **Major fork** or long-lived label: add a **Conceptual authority decision** line under the appropriate **D-*** section **or** reference a new **D-*** row if the project already numbers decisions that way.

## Decision record lines (Conceptual-Decision-Records)

When **roadmap-deepen** (conceptual track) emits an atomized rationale note under **`Roadmap/Conceptual-Decision-Records/`**, append a bullet under **`## Conceptual autopilot`** using this pattern:

```markdown
- **Decision record (deepen):** [[1-Projects/<project_id>/Roadmap/Conceptual-Decision-Records/<slug>-YYYY-MM-DD-HHMM.md]] — queue_entry_id: <id> — validation: <cited|pattern_only|needs_human>
```

**Optional** general form for other **`decision_kind`** values:

```markdown
- **Decision record (<decision_kind>):** [[<path>]] — queue_entry_id: <id> — validation: <cited|pattern_only|needs_human>
```

Regex hint: `Decision record \(([^)]+)\):`

## See also

- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] — Definitions and authority
- [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] — EAT-QUEUE Step 0c / decisions preflight
- [[Templates/Roadmap/Artifacts/decisions-log|decisions-log template]]
- Skill: `.cursor/skills/decisions-preflight/SKILL.md`
