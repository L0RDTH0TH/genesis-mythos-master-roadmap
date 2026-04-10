---
title: Dual roadmap track (conceptual vs execution)
created: 2026-03-24
tags: [second-brain, roadmap, conceptual, execution]
links:
  - "[[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]]"
  - "[[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]]"
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

### Godot lane (execution)

When **`parallel_track`** is **`godot`**, **`effective_track`** is **`execution`**, and **`project_id`** is **`godot-genesis-mythos-master`** (see [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`parallel_execution.tracks`**), agents **must** follow [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]] (**`gate_catalog_id: execution_godot_v1`**) and [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]]. **Runtime enforcement:** [[.cursor/rules/agents/godot-execution-guard|godot-execution-guard]] (after **§0** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]]). **Mandatory order:** §0 whitelist → **`design_intent_alignment`** → precision/linkage gates. **Design intent contract:** [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Design-Intent-Alignment|Roadmap-Gate-Catalog-Design-Intent-Alignment]]. **Citation URLs (strict):** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] **godot** lane — multi-prefix **OR** (stable **`docs.godotengine.org/en/stable/`**, **`.../classes/`**, **`.../tutorials/scripting/gdscript/`**, **`godotengine.org/article/`**, **`godotengine.org/releases/`**).

### Sandbox lane (execution)

When **`parallel_track`** is **`sandbox`**, **`effective_track`** is **`execution`**, and **`project_id`** is **`sandbox-genesis-mythos-master`**, agents **must** follow [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]] (**`gate_catalog_id: execution_sandbox_v1`**) and [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]]. **Sandbox** is the **C-powered** lane — **not** GDScript. **Runtime enforcement:** [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]] (after **§0** whitelist). **Mandatory order:** §0 whitelist → **`design_intent_alignment`** → precision/linkage gates. **Design intent contract:** [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Design-Intent-Alignment|Roadmap-Gate-Catalog-Design-Intent-Alignment]]. **Citation URLs (strict):** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] **sandbox** lane — multi-prefix **OR** (cppreference **`/w/`**, cplusplus **`reference/`**, **GCC onlinedocs**, **Clang `clang.llvm.org/docs/`**, **ISO C++ Core Guidelines `isocpp.github.io/CppCoreGuidelines/`**, **MSVC `learn.microsoft.com/en-us/cpp/`**).

### Execution track — §0 whitelist + harness (all lanes)

**§0** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] runs **first** (pre-snapshot, **pre-`Task(research)` hand-off URL scan**). Violation **aborts entire deepen** **before** Research — **`task_error`**, **`url_whitelist_violation`**, **honesty ledger**; **no** destructive success. Then lane guards run. Config **`parallel_execution.tracks[].research_whitelist_enforced`** (default **true**) signals Layer 1 to log allowlist intent for EAT-QUEUE.

## Why not `.cursorignore`

Conceptual notes must stay **readable** in Cursor and Obsidian. Protection is **contractual** (frontmatter `frozen: true` + agent rules), not filesystem hiding.

**Full-vault backup:** Any session that **writes** conceptual or execution roadmap files still ends with **Curator** commit + push per [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]] (does not change conceptual vs execution semantics).

## Manual flip

Follow the checklist in [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Dual roadmap track (snapshot → set `roadmap_track: execution` → stamp frozen conceptual notes → bootstrap `Templates/Roadmap/Execution`).

## Execution path hand-off (queue / operator)

Paste into **`user_guidance`** or **`prompt`** on **`RESUME_ROADMAP`** / deepen entries when you need to reinforce layout:

```text
Deepen on execution track only.
Target root = Roadmap/Execution/
Mirror the exact conceptual phase folder hierarchy from the current roadmap-state.md.
Example mapping:
  Conceptual path → Roadmap/Execution/<same relative folders and filename>
Do NOT flatten under the Execution root.
Create any missing Phase-X/ subfolders.
After write, update all internal links, conceptual_counterpart frontmatter, and workflow_state-execution.md pointers.
Confirm new path in the hand-off log.
```

Cross-ref: [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] (RESUME_ROADMAP payloads); [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Flat Execution folder hygiene.

## Unfreeze

Use **`RESUME_ROADMAP`** with **`params.action: "unfreeze_conceptual"`** (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]) only when policy and approval allow editing frozen conceptual notes again.

## Diminishing returns

Advisory flags in `workflow_state` ## Log **Status / Next** (config: `prompt_defaults.roadmap.diminishing_returns_*`). Informational only — does not auto-switch tracks.

## Control plane v2 (progression gates)

**Conceptual** track does **not** require execution-only artifacts (e.g. depth-4 pseudo-code blocks) for **advance-phase** on phases 5–6 or for deepen **pre-create** at depth ≥4. **Execution** track keeps those gates. Deterministic rules and observability fields live in [[3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2|Control-Plane-Heuristics-v2]]; Config: `roadmap.control_plane_v2`.

## Execution tracking linkage (`ledger_ref`)

On the **execution** track, **`1-Projects/<project_id>/Roadmap/Execution/roadmap-state-execution.md`** frontmatter **must** include **`ledger_ref`** as a **YAML array of strings** (stable ids from **`intent_actual_receipt`** rows in **`task-handoff-comms.jsonl`**, e.g. receipt **`task_correlation_id`** or synthetic receipt id) for **each phase rollup** when a deepen or decision-closing run completes. This links junior-visible execution state to the nervous-system receipt trail (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Parallel execution tracking). **`workflow_state-execution.md`** may mirror the same **`ledger_ref`** for the active cursor when operators want a single scroll point.

**Hard requirement:** A RESUME_ROADMAP / roadmap pipeline run **must not** return **Success** for execution-track work that **claims** rollup closure, receipt alignment, or “execution state fully updated” while **`ledger_ref`** on **`roadmap-state-execution.md`** is **missing** or **incomplete** relative to receipts produced in that run — treat as **#review-needed** / Validator **`block_destructive`** (**`execution_linkage_violation`**) per the lane’s tiered precision doc ([[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]] for **godot**, [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]] for **sandbox**). Backfill **`ledger_ref`** in a dedicated hygiene pass when historical runs omitted it.

## Execution phase mirrors (`conceptual_counterpart`)

Every **new** execution **phase** note under **`Roadmap/Execution/`** (mirrored tree; not the two Execution-root state files) **must** include frontmatter **`conceptual_counterpart`** linking to the conceptual note at the same relative path under **`Roadmap/`** (excluding the **`Execution/`** segment). Missing link on a minted execution phase note is **`execution_linkage_violation`** for validation. See linkage hygiene in [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]] (godot) and [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]] (sandbox).

## Related

- [[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]]
- [[3-Resources/Second-Brain/Parameters|Parameters]] § Dual roadmap track
- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]] · [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]] · [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]]
- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]] · [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]] · [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]]
- [[3-Resources/Second-Brain/Docs/Dry-Run-Appendix-Godot-Execution-Gates-2026-04-11|Dry-Run-Appendix-Godot-Execution-Gates-2026-04-11]]
- `.cursor/rules/context/dual-roadmap-track.mdc` (agent enforcement)
- `.cursor/rules/agents/godot-execution-guard.mdc` (godot lane execution runtime hook)
- `.cursor/rules/agents/sandbox-execution-guard.mdc` (sandbox lane execution runtime hook)
- `.cursor/rules/agents/execution-research-whitelist.mdc` (execution Research URL allowlist; prompt-injection guard)
