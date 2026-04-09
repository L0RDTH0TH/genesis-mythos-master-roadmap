---
title: Roadmap gate catalog — Sandbox lane execution overlay
created: 2026-04-12
tags: [second-brain, roadmap, gates, execution, sandbox]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]]"
  - "[[3-Resources/Second-Brain-Config|Second-Brain-Config]]"
---

# Roadmap gate catalog — Sandbox lane execution overlay

## Purpose

This note is the **lane-scoped extension** to [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]] for the **sandbox** parallel track when **`effective_track === execution`**. It does **not** replace the base **`execution_v1`** catalog; Layer 1 and RoadmapSubagent log **`gate_catalog_id: execution_sandbox_v1`** when this overlay applies so telemetry distinguishes generic execution gates from **C / C++** code-precision requirements for the **C-powered engine** lane.

**Activation (all required):**

- **`parallel_track`** **`sandbox`** (from Layer 1 **`## parallel_context`** / resolver; see [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`parallel_execution.tracks`**).
- **`effective_track`** **`execution`** (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`effective_track` resolution**).
- **`project_id`** matches the track’s **`lane_project_id`** (**`sandbox-genesis-mythos-master`** for the default sandbox row).

Godot, **default**, **shared**, and **core** lanes do **not** use this overlay unless a future Config row explicitly points here.

---

## `gate_catalog_id`

| Id | When to log |
|----|-------------|
| **`execution_sandbox_v1`** | Sandbox lane + execution track + roadmap pipeline run that is subject to **`sandbox_code_precision`** or the [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]] profile. |

---

## Gate family — `sandbox_code_precision`

**Goal:** Every **new** C / C++-shaped construct introduced under **`Roadmap/Execution/**`** (header snippets, memory / ownership patterns, ABI or compilation constraints, `static_assert` / standards references) is **evidence-backed** with **C or C++** grammar or official reference material — not Python idioms, not GDScript, not hand-waved “looks like C”.

| Requirement | Normative behavior |
|-------------|-------------------|
| **Research helper** | Before minting or expanding execution notes that introduce **new** constructs (not a trivial rename of an already-cited pattern), RoadmapSubagent **must** invoke **ResearchSubagent** via **`Task(subagent_type: "research")`** per [[.cursor/agents/roadmap|agents/roadmap.md]] nested Research contract — **not** `web_search` or **`research-agent-run`** alone as a substitute for that **`Task`**. |
| **URL whitelist (automatic §0)** | **Before** **`Task(research)`**, enforce [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] — **sandbox** lane **multi-prefix OR**: **`https://en.cppreference.com/w/`**, **`https://cplusplus.com/reference/`**, **`https://gcc.gnu.org/onlinedocs/`**, **`https://learn.microsoft.com/en-us/cpp/`**; hand-off scan **before** Research; **non-whitelisted URLs → `task_error` + `url_whitelist_violation` + honesty ledger**; **abort entire deepen**; no execution write. |
| **Verbatim grammar citation** | For each **new** construct, the execution note **must** include a short **authority** block: quoted **verbatim** passage from an **allowlisted** official reference (e.g. cppreference) **plus** stable URL. Paraphrase-only without quote **does not** satisfy this gate. |
| **Validator alignment** | **`roadmap_handoff_auto`** (and aligned types) **must** treat violations per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]] — typically **`recommended_action: block_destructive`** / **`severity: high`**. |

---

## Gate family — linkage hygiene (execution)

These reinforce [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]; they are **hard prerequisites** for claiming Success on structural writes in **`Roadmap/Execution/`** on the sandbox lane.

| Gate | Requirement |
|------|-------------|
| **`conceptual_counterpart`** | Every **new or updated** execution **phase** note (mirrored tree under **`Roadmap/Execution/`**) **must** include frontmatter **`conceptual_counterpart`** pointing at the conceptual sibling under **`Roadmap/`** (excluding **`Execution/`**). Coordination-only files **`roadmap-state-execution.md`** and **`workflow_state-execution.md`** do **not** use **`conceptual_counterpart`**; they use **`ledger_ref`** instead. |
| **`ledger_ref`** | **`roadmap-state-execution.md`** frontmatter **must** include **`ledger_ref`** (YAML array of receipt ids) updated when rollups / decision-closing runs complete, per Dual-Roadmap-Track § Execution tracking linkage. |

---

## Cross-references

- [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]] — enforceable runtime checklist (RoadmapSubagent).
- [[.cursor/rules/agents/validator.mdc|validator.mdc]] — **`roadmap_handoff_auto`**, **`effective_track`**, **`gate_catalog_id`** in hand-off.
- [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] — base tiered matrix; Sandbox code precision extends via the Sandbox-specific doc above.
