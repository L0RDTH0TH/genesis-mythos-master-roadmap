---
name: Unfreeze To Action Param
overview: Migrate unfreeze from standalone queue mode to `RESUME_ROADMAP` action parameter, while keeping a compatibility normalization path for any legacy lines. Update routing, validation, docs, and sync mirrors consistently.
todos:
  - id: queue-unify-action
    content: Unify queue handling so unfreeze is a RESUME_ROADMAP action; keep legacy normalization path.
    status: completed
  - id: roadmap-contracts
    content: Refactor roadmap subagent/rules docs from standalone mode to action-based unfreeze.
    status: completed
  - id: docs-params-refresh
    content: Update Queue-Sources/Parameters/Pipelines/Reference docs to action-based contract.
    status: completed
  - id: sync-and-changelog
    content: Sync changed rules/docs into .cursor/sync and add changelog migration note.
    status: completed
isProject: false
---

# Migrate Unfreeze To RESUME_ROADMAP Action

## Goal

Consolidate roadmap continuation into one funnel: `RESUME_ROADMAP` with `params.action`, using `action: unfreeze_conceptual` for conceptual unfreeze operations.

## Scope of Changes

- Replace standalone mode semantics (`ROADMAP_UNFREEZE_CONCEPTUAL`) with parameterized action semantics under `RESUME_ROADMAP`.
- Keep compatibility by normalizing any legacy `ROADMAP_UNFREEZE_CONCEPTUAL` entries to `RESUME_ROADMAP` + `params.action: unfreeze_conceptual`.
- Preserve existing safety gates (`confirm_unfreeze`, snapshots, backup, conceptual-only targeting).

## Implementation Steps

- Update queue orchestration contracts:
  - In [/.cursor/rules/agents/queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc), remove `ROADMAP_UNFREEZE_CONCEPTUAL` from canonical ordering and pipeline mode lists, and add compatibility normalization to map legacy mode -> `RESUME_ROADMAP` + `params.action: unfreeze_conceptual`.
  - Mirror those updates in [/.cursor/sync/rules/agents/queue.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/agents/queue.md).
  - In [/.cursor/rules/context/auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc), remove standalone mode from known-mode/canonical-order docs and document action-based handling; mirror to [/.cursor/sync/rules/context/auto-eat-queue.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/context/auto-eat-queue.md).
- Update roadmap subagent contracts:
  - In [/.cursor/agents/roadmap.md](/home/darth/Documents/Second-Brain/.cursor/agents/roadmap.md), move unfreeze behavior under RESUME-ROADMAP action branch (`params.action: unfreeze_conceptual`) and remove standalone mode language.
  - In [/.cursor/rules/agents/roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/roadmap.mdc), update trigger/description text to reflect action-based unfreeze.
  - Mirror in [/.cursor/sync/rules/agents/roadmap.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/agents/roadmap.md).
- Update user-facing queue and pipeline docs:
  - In [/3-Resources/Second-Brain/Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md), remove standalone mode entry and add `unfreeze_conceptual` to RESUME_ROADMAP action contract (including required `confirm_unfreeze` and optional `paths`).
  - In [/3-Resources/Second-Brain/Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md), extend RESUME action enum to include `unfreeze_conceptual`.
  - Update references in [/3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md), [/3-Resources/Second-Brain/Pipelines.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Pipelines.md), [/3-Resources/Second-Brain/Rules.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Rules.md), and [/3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md) to point to action-based unfreeze.
- Keep validator mapping coherent:
  - In [/3-Resources/Second-Brain/Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md), ensure post-pipeline validator mapping describes unfreeze as a RESUME action case (not separate mode).
  - Validate consistency with [/3-Resources/Second-Brain/Validator-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Validator-Reference.md) wording.
- Backbone sync and changelog:
  - Ensure all changed rules/skills docs are mirrored under `/.cursor/sync/**`.
  - Append migration entry in [/.cursor/sync/changelog.md](/home/darth/Documents/Second-Brain/.cursor/sync/changelog.md) describing mode->action unification.

## Validation Checklist

- Queue accepts:
  - `{"mode":"RESUME_ROADMAP","params":{"action":"unfreeze_conceptual",...}}`
- Queue still safely handles legacy lines by normalization:
  - `{"mode":"ROADMAP_UNFREEZE_CONCEPTUAL",...}` -> normalized before dispatch.
- Canonical order and known-mode lists no longer require standalone mode.
- RoadmapSubagent docs describe unfreeze only as RESUME action.
- All referenced docs and sync mirrors are internally consistent (no stale standalone-mode instructions).

