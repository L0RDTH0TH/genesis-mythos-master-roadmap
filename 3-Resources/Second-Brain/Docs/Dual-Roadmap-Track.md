---
title: Dual roadmap track (conceptual vs execution)
created: 2026-03-24
tags: [second-brain, roadmap, conceptual, execution]
links:
  - "[[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]]"
---

# Dual roadmap track (conceptual vs execution)

Official user-facing summary. Authoritative paths and tables: [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Roadmap state artifacts and Dual roadmap track; folder patterns: [[Roadmap Structure|Roadmap Structure]].

## Definitions (canonical)

- **Conceptual complete:** The system is explained in plain natural language end-to-end; the map is coherent and stable enough to resume; work is **ready to start pseudo-code** at the appropriate leaves. Does **not** require registry/CI/rollup PASS.
- **Ready for handoff to execution:** Every **primary, secondary, tertiary, quaternary,** and deeper phase/subphase note in scope has **behavior fully described in natural language**, per [[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]].
- **Design authority:** The **conceptual** map plus **`decisions-log.md`** sections **`## Conceptual autopilot`** (and, where used, **Conceptual authority decision** lines per [[3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention|Decisions-Log-Operator-Pick-Convention]]) are the **source of truth for what to build**. **Execution** implements, instruments, and proves; rollup HR, REGISTRY-CI, and similar gates apply on the **execution** track.
- **Forward-first conceptual policy:** On `effective_track: conceptual`, structural roadmap progress is preferred by default (deepen-first), and execution-debt gates remain advisory unless true hard conceptual blockers exist (`incoherence`, `contradictions_detected`, `state_hygiene_failure`, `safety_critical_ambiguity`).
- **Post-freeze amendments:** After the conceptual tree is **frozen** (flip checklist), **do not** overwrite frozen phase bodies for new direction. Add **atomized companion notes** under `Roadmap/Conceptual-Amendments/` (see [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Conceptual-Amendments), **one note per section-level change**, linked from the parent.
- **Conceptual decision records:** For **reasoning, alternatives, PMG alignment, and validation evidence** on conceptual-track pipeline decisions (primarily **deepen**), use **atomized notes** under `Roadmap/Conceptual-Decision-Records/` (see [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Conceptual-Decision-Records). One note per meaningful decision; distinct from section-level **amendments**.
- **Scaffold fallback contract:** If a conceptual structural write is blocked (especially on frozen notes), the run must still produce a conversion-ready scaffold artifact (sections, tasks, acceptance criteria, artifact names) in the active phase note or as a new `Conceptual-Amendments` companion note.

## What it is

- **Conceptual roadmap:** Default. Lives under `1-Projects/<project_id>/Roadmap/` (phase tree, `workflow_state.md`, `roadmap-state.md`). **Design authority** for structure and behavior-in-words; soft / verbose logging; no execution-shaped **completion** gates.
- **Execution roadmap:** **Parallel** track. After a **manual** switch (or **`RESUME_ROADMAP`** with **`params.action: bootstrap-execution-track`** when preconditions are met), new deepen/recal work targets **`Roadmap/Execution/`** with separate **`workflow_state-execution.md`** and **`roadmap-state-execution.md`**, linked to conceptual notes via **`conceptual_counterpart`**. **Hard** gates (rollup, registry, CI-shaped evidence) apply here.

## `effective_track` (single resolution)

All layers use the same precedence — see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`effective_track` resolution**:

1. If the queue entry **sets** **`params.roadmap_track`**, that value is the active track for the run (**track lock** for that entry).
2. Else use **`roadmap_track`** from **`roadmap-state.md`** frontmatter (default **`conceptual`** if absent).

**Gate catalogs** differ by track — see [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]].

## Why not `.cursorignore`

Conceptual notes must stay **readable** in Cursor and Obsidian. Protection is **contractual** (frontmatter `frozen: true` + agent rules), not filesystem hiding.

## Manual flip

Follow the checklist in [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Dual roadmap track (snapshot → set `roadmap_track: execution` → stamp frozen conceptual notes → bootstrap `Templates/Roadmap/Execution`).

## Unfreeze

Use **`RESUME_ROADMAP`** with **`params.action: "unfreeze_conceptual"`** (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]) only when policy and approval allow editing frozen conceptual notes again.

## Diminishing returns

Advisory flags in `workflow_state` ## Log **Status / Next** (config: `prompt_defaults.roadmap.diminishing_returns_*`). Informational only — does not auto-switch tracks.

## Control plane v2 (progression gates)

**Conceptual** track does **not** require execution-only artifacts (e.g. depth-4 pseudo-code blocks) for **advance-phase** on phases 5–6 or for deepen **pre-create** at depth ≥4. **Execution** track keeps those gates. Deterministic rules and observability fields live in [[3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2|Control-Plane-Heuristics-v2]]; Config: `roadmap.control_plane_v2`.

## Related

- [[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]]
- [[3-Resources/Second-Brain/Parameters|Parameters]] § Dual roadmap track
- `.cursor/rules/context/dual-roadmap-track.mdc` (agent enforcement)
