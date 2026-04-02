---
title: Roadmap System Run Documentation Index
created: 2026-04-02
tags: [second-brain, roadmap, docs, index]
---

# Roadmap System Run Documentation Index

This index is the explicit “vault → export repo” mapping for documentation that describes how the **roadmap system runs** (ROADMAP_MODE setup, RESUME_ROADMAP single-action continuation, dual-track conceptual/execution behavior, and the queue/dispatcher wiring).

It is intentionally explicit about file locations so the exported GitHub mirror stays complete.

## Mapping conventions (used below)

- Vault `.cursor/agents/`, `.cursor/rules/`, `.cursor/skills/` are mirrored to the export repo at the same path.
- Vault `3-Resources/Second-Brain/Docs/**` are mirrored to export repo at `Docs/**`.
- Vault core docs in `3-Resources/Second-Brain/*.md` are copied into export repo `Docs/Core/`.
- Vault core watcher/error docs in `3-Resources/*` are copied into `Docs/Core/` by the push workflow.

## Index: Roadmap-runtime docs (vault path → export path)

### User-facing roadmap run references (mirrored from `3-Resources/Second-Brain/Docs/`)

| Vault path | Export path | What it covers |
|---|---|---|
| `3-Resources/Second-Brain/Docs/Roadmapping-System.md` | `Docs/Roadmapping-System.md` | High-level operational reference: setup vs resume, state authority, dual-track behavior, lifecycle steps. |
| `3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md` | `Docs/Dual-Roadmap-Track.md` | Conceptual vs execution track definitions and gating semantics (effective_track). |
| `3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track.md` | `Docs/Roadmap-Gate-Catalog-By-Track.md` | Catalog of gate families per track and how validators/queue treat them. |
| `3-Resources/Second-Brain/Docs/Pipelines/Roadmap-Pipeline.md` | `Docs/Pipelines/Roadmap-Pipeline.md` | The multi-run roadmap pipeline steps and return behavior (what each action branch does). |
| `3-Resources/Second-Brain/Docs/User-Flows/Roadmap-Resume-Flow.md` | `Docs/User-Flows/Roadmap-Resume-Flow.md` | RESUME-ROADMAP execution flow: enqueue → queue dispatch → roadmap subagent → one action per run. |
| `3-Resources/Second-Brain/Docs/Skills/Roadmap-Skills-Overview.md` | `Docs/Skills/Roadmap-Skills-Overview.md` | Skill roster for the roadmap subagent (generate, deepen, advance-phase, audit, revert, sync outputs, etc.). |
| `3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2.md` | `Docs/Control-Plane-Heuristics-v2.md` | Control-plane heuristics used by dual-track and roadmap decision gates. |
| `3-Resources/Second-Brain/Docs/Contract-Index.md` | `Docs/Contract-Index.md` | Single-page contract index (safety, ledger spec, roadmap overview pointer). |
| `3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446.md` | `Docs/git-push-workflow-2026-04-02-0446.md` | Push/mirror workflow used for the GitHub export repo. |

### Safety & validation contracts (mirrored from `3-Resources/Second-Brain/Docs/`)

| Vault path | Export path | What it covers |
|---|---|---|
| `3-Resources/Second-Brain/Subagent-Safety-Contract.md` | `Docs/Core/Subagent-Safety-Contract.md` | Subagent helper/probing honesty rules and mandatory helper contracts. |
| `3-Resources/Second-Brain/Docs/Safety-Invariants.md` | `Docs/Safety-Invariants.md` | Global safety invariants: backups/snapshots, confidence bands, nested helper constraints. |
| `3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md` | `Docs/Nested-Subagent-Ledger-Spec.md` | `nested_subagent_ledger` schema + attestation rules. |
| `3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles.md` | `Docs/Pipeline-Validator-Profiles.md` | Validator behavior by pipeline mode/profile (tiered block treatment). |
| `3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md` | `Docs/Validator-Tiered-Blocks-Spec.md` | Mapping from validator severity and recommended_action to “hard block” vs “advisory”. |
| `3-Resources/Second-Brain/Docs/Queue-Continuation-Spec.md` | `Docs/Queue-Continuation-Spec.md` | Schema for queue continuation blocks used by roadmap follow-ups. |
| `3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec.md` | `Docs/Task-Handoff-Comms-Spec.md` | JSONL shape for `handoff_out` / `return_in` around nested Task calls. |

### Queue wiring & roadmap mode parameterization (mirrored from `3-Resources/Second-Brain/*.md` into `Docs/Core/`)

| Vault path | Export path | What it covers |
|---|---|---|
| `3-Resources/Second-Brain/Queue-Sources.md` | `Docs/Core/Queue-Sources.md` | Mode routing logic and RESUME_ROADMAP parameter semantics (including action aliases). |
| `3-Resources/Second-Brain/Queue-Alias-Table.md` | `Docs/Core/Queue-Alias-Table.md` | Explicit alias table: e.g. RECAL-ROAD, REVERT-PHASE, SYNC-PHASE-OUTPUTS normalization. |
| `3-Resources/Second-Brain/Parameters.md` | `Docs/Core/Parameters.md` | Confidence thresholds, gate/tier tuning, and shared parameter defaults. |
| `3-Resources/Second-Brain/Second-Brain-Config.md` | `Docs/Core/Second-Brain-Config.md` | Operational defaults (prompt defaults, roadmap config knobs, optional gating flags). |
| `3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md` | `Docs/Core/Cursor-Skill-Pipelines-Reference.md` | Pipeline mode → dispatch behavior reference. |
| `3-Resources/Second-Brain/Pipelines.md` | `Docs/Core/Pipelines.md` | Pipeline overview and trigger mapping for roadmap modes. |
| `3-Resources/Second-Brain/User-Questions-and-Options-Reference.md` | `Docs/Core/User-Questions-and-Options-Reference.md` | Question-led prompt crafter options mapping used in wrapper creation. |
| `3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md` | `Docs/Core/Prompt-Crafter-Param-Table.md` | Param order/semantics for prompt-crafter payload creation. |

### Roadmap state model & structural references (mirrored into `Docs/Core/` by push workflow)

| Vault path | Export path | What it covers |
|---|---|---|
| `3-Resources/Second-Brain/Vault-Layout.md` | `Docs/Core/Vault-Layout.md` | Roadmap state artifacts, dual-track folder patterns, and protected boundaries. |
| `Roadmap Structure.md` | `Docs/Core/Roadmap Structure.md` | Roadmap index/phase/subphase structure contract used by roadmap-deepen and advance-phase. |
| `3-Resources/Second-Brain/Roadmap-Quality-Guide.md` | `Docs/Core/Roadmap-Quality-Guide.md` | Target reached criteria and roadmap automation target selection. |
| `3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md` | `Docs/Core/Roadmap-Upgrade-Plan.md` | Upgrade/reset plan for roadmap system evolution (how to migrate safely). |

### Watcher / error observability docs (mirrored into `Docs/Core/` by push workflow)

| Vault path | Export path | What it covers |
|---|---|---|
| `3-Resources/Watcher-Result.md` | `Docs/Core/Watcher-Result.md` | Stable Watcher-Result line format parsed by the Obsidian Watcher plugin. |
| `3-Resources/Watcher-Signal.md` | `Docs/Core/Watcher-Signal.md` | Watcher trigger signal schema including requestId correlation. |
| `3-Resources/Errors.md` | `Docs/Core/Errors.md` | Standard error entry format for pipeline failures and recovery wrappers. |

## Index: roadmap runtime implementation contracts (mirrored under `.cursor/` in export)

| Vault path | Export path | What it covers |
|---|---|---|
| `.cursor/agents/roadmap.md` | `.cursor/agents/roadmap.md` | RoadmapSubagent operational contract (how it reads state, runs actions, enforces gates). |
| `.cursor/rules/agents/roadmap.mdc` | `.cursor/rules/agents/roadmap.mdc` | Context rule describing roadmap pipeline executor behavior and safety gates. |
| `.cursor/rules/context/auto-roadmap.mdc` | `.cursor/rules/context/auto-roadmap.mdc` | Auto-roadmap routing logic deciding when roadmap modes should run. |
| `.cursor/rules/context/dual-roadmap-track.mdc` | `.cursor/rules/context/dual-roadmap-track.mdc` | Dual track enforcement + frozen conceptual note non-destructive constraints. |
| `.cursor/rules/always/dispatcher.mdc` | `.cursor/rules/always/dispatcher.mdc` | Dispatcher routing for EAT-QUEUE / queue modes that ultimately invoke roadmap runs. |
| `.cursor/agents/queue.md` | `.cursor/agents/queue.md` | Queue processor that dispatches ROADMAP_MODE / RESUME_ROADMAP (and wraps/normalizes actions). |
| `.cursor/rules/agents/queue.mdc` | `.cursor/rules/agents/queue.mdc` | Queue agent context rule with dispatch + rewrite behavior. |
| `.cursor/skills/roadmap-generate-from-outline/SKILL.md` | `.cursor/skills/roadmap-generate-from-outline/SKILL.md` | Phase 0 + initial roadmap tree generation skill. |
| `.cursor/skills/roadmap-deepen/SKILL.md` | `.cursor/skills/roadmap-deepen/SKILL.md` | Single deepen step skill: workflow_state update + RESUME follow-ups (queue_next). |
| `.cursor/skills/roadmap-advance-phase/SKILL.md` | `.cursor/skills/roadmap-advance-phase/SKILL.md` | Advance-phase skill with depth-aware gates. |
| `.cursor/skills/roadmap-audit/SKILL.md` | `.cursor/skills/roadmap-audit/SKILL.md` | RECAL repair/audit logic and wrapper-creation thresholds. |
| `.cursor/skills/roadmap-resume/SKILL.md` | `.cursor/skills/roadmap-resume/SKILL.md` | Resume context building for deepen handoff. |
| `.cursor/skills/roadmap-revert/SKILL.md` | `.cursor/skills/roadmap-revert/SKILL.md` | Escape hatch for phase regret; archives phase and re-queues from corrected target. |
| `.cursor/skills/roadmap-phase-output-sync/SKILL.md` | `.cursor/skills/roadmap-phase-output-sync/SKILL.md` | Phase output alignment with canonical phase note. |
| `.cursor/skills/hand-off-audit/SKILL.md` | `.cursor/skills/hand-off-audit/SKILL.md` | Handoff-audit (junior-dev delegatability) gate for handoff-audit actions. |
| `.cursor/skills/expand-road-assist/SKILL.md` | `.cursor/skills/expand-road-assist/SKILL.md` | Expansion parser/append under a selected roadmap section/task. |

## Sanity check

After running the export mirror described in `Docs/git-push-workflow-2026-04-02-0446.md`, verify that every `Export path` in this index exists in `/home/darth/Documents/gmm-roadmap-export/`.

