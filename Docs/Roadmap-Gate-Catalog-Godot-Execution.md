---
title: Roadmap gate catalog — Godot lane execution overlay
created: 2026-04-11
tags: [second-brain, roadmap, gates, execution, godot]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]]"
  - "[[3-Resources/Second-Brain-Config|Second-Brain-Config]]"
---

# Roadmap gate catalog — Godot lane execution overlay

## Purpose

This note is the **lane-scoped extension** to [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]] for the **godot** parallel track when **`effective_track === execution`**. It does **not** replace the base **`execution_v1`** catalog; Layer 1 and RoadmapSubagent log **`gate_catalog_id: execution_godot_v1`** when this overlay applies so telemetry distinguishes generic execution gates from **Godot 4.x** code-precision requirements.

**Activation (all required):**

- **`parallel_track`** **`godot`** (from Layer 1 **`## parallel_context`** / resolver; see [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`parallel_execution.tracks`**).
- **`effective_track`** **`execution`** (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`effective_track` resolution**).
- **`project_id`** matches the track’s **`lane_project_id`** (**`godot-genesis-mythos-master`** for the default godot row).

Sandbox, **default**, **shared**, and **core** lanes do **not** use this overlay unless a future Config row explicitly points here.

---

## `gate_catalog_id`

| Id | When to log |
|----|-------------|
| **`execution_godot_v1`** | Godot lane + execution track + roadmap pipeline run that is subject to **`godot_code_precision`** or the [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]] profile. |

---

## Gate family — `godot_code_precision`

**Goal:** Every **new** GDScript-shaped construct introduced under **`Roadmap/Execution/**`** (pseudo-code blocks, API sketches, signal/connect examples, `@onready` / `await` usage) is **evidence-backed** with **Godot 4.x** grammar or official docs — not Python idioms, not Godot 3-only syntax, not hand-waved “looks like GDScript”.

| Requirement | Normative behavior |
|-------------|-------------------|
| **Research helper** | Before minting or expanding execution notes that introduce **new** constructs (not a trivial rename of an already-cited pattern), RoadmapSubagent **must** invoke **ResearchSubagent** via **`Task(subagent_type: "research")`** per [[.cursor/agents/roadmap|agents/roadmap.md]] nested Research contract — **not** `web_search` or **`research-agent-run`** alone as a substitute for that **`Task`**. |
| **Verbatim grammar citation** | For each **new** construct, the execution note **must** include a short **authority** block: quoted **verbatim** passage from official material **plus** stable URL whose prefix matches **one** of the **godot** lane rows in [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] § **Allowlists** — **`https://docs.godotengine.org/en/stable/`**, **`.../stable/classes/`**, **`.../stable/tutorials/scripting/gdscript/`**, **`https://godotengine.org/article/`**, **`https://godotengine.org/releases/`** (multi-prefix **OR**; playable **GDScript** precision; no blanket hosts). Paraphrase-only without quote **does not** satisfy this gate. |
| **Validator alignment** | **`roadmap_handoff_auto`** (and aligned types) **must** treat violations per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]] — typically **`recommended_action: block_destructive`** / **`severity: high`**. |

---

## Gate family — linkage hygiene (execution)

These reinforce [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]; they are **hard prerequisites** for claiming Success on structural writes in **`Roadmap/Execution/`** on the godot lane.

| Gate | Requirement |
|------|-------------|
| **`conceptual_counterpart`** | Every **new or updated** execution **phase** note (mirrored tree under **`Roadmap/Execution/`**) **must** include frontmatter **`conceptual_counterpart`** pointing at the conceptual sibling under **`Roadmap/`** (excluding **`Execution/`**). Coordination-only files **`roadmap-state-execution.md`** and **`workflow_state-execution.md`** do **not** use **`conceptual_counterpart`**; they use **`ledger_ref`** instead. |
| **`ledger_ref`** | **`roadmap-state-execution.md`** frontmatter **must** include **`ledger_ref`** (YAML array of receipt ids) updated when rollups / decision-closing runs complete, per Dual-Roadmap-Track § Execution tracking linkage. |

---

## Cross-references

- [[.cursor/rules/agents/godot-execution-guard|godot-execution-guard]] — enforceable runtime checklist (RoadmapSubagent).
- [[.cursor/rules/agents/validator.mdc|validator.mdc]] — **`roadmap_handoff_auto`**, **`effective_track`**, **`gate_catalog_id`** in hand-off.
- [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] — base tiered matrix; Godot code precision extends via the Godot-specific doc above.
