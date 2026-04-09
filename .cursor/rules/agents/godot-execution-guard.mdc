---
description: "Godot lane execution guard — pre-write checks for Roadmap/Execution (conceptual_counterpart, ledger_ref, godot_code_precision: Research Task + Godot 4.x verbatim citations). Activates when parallel_track godot + execution track + godot-genesis-mythos-master."
globs: []
alwaysApply: false
---

# Godot execution guard (RoadmapSubagent runtime hook)

- **Role:** Tighten **structural writes** under **`1-Projects/godot-genesis-mythos-master/Roadmap/Execution/**`** when the hand-off carries **`parallel_track: godot`** (or Layer 0 **`EAT-QUEUE lane godot`** → **`## parallel_context`**) **and** **`effective_track: execution`** (from **`layer1_resolver_hints`**, queue **`params.roadmap_track`**, or **`roadmap-state.md`** per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]).
- **Does not replace:** [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]], nested Validator / IRA / little val, or [[.cursor/rules/agents/roadmap.mdc|roadmap.mdc]] — this rule **adds** lane-specific gates **before** claiming Success on deepen / bootstrap / expand that **mutate** execution tree notes or execution state files.

## Depends on (shared always rules)

This rule **depends on** and does not duplicate: [[.cursor/rules/always/core-guardrails.mdc|core-guardrails]], [[.cursor/rules/context/dual-roadmap-track.mdc|dual-roadmap-track]], [[.cursor/rules/always/mcp-obsidian-integration.mdc|mcp-obsidian-integration]].

## Depends on (execution Research gate — §0 harness)

[[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] — **mandatory §0** at harness **before** this lane guard runs: pre-snapshot, **pre-`Task(research)` hand-off URL scan**, abort entire deepen on violation **before** Research. This guard **§0** re-validates Research **return** URLs before merge (**belt-and-suspenders**).

## Normative docs (iteration-2)

- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]] — **`gate_catalog_id: execution_godot_v1`**, **`godot_code_precision`**.
- [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]] — profile overlay keys.
- [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]] — **`reason_code`** / **`block_destructive`** mapping.

---

## Pre-write checklist (mandatory order)

Run **before** snapshot-backed destructive edits to **`Roadmap/Execution/**`** phase notes or execution state bodies (including new file mint under the parallel spine):

### 0. Research URL whitelist (hardened — **must** match harness §0)

- **Prerequisite:** Harness **§0** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] **already passed** pre-hand-off scan; do **not** skip.
- For **any** nested **`Task(subagent_type: "research")`** whose consumables will justify **new** GDScript constructs: citation / fetch URLs **must** match **one** of the **godot** lane prefix rows in [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] § **Allowlists** (stable **`docs.godotengine.org/en/stable/`** tree, **`godotengine.org/article/`**, **`godotengine.org/releases/`** — **OR**-prefix list only). Reject **`/en/4.x/`**, **`/latest/`**, non-HTTPS, **sandbox**-lane URLs, `http://`.
- If Research returns **any** non-allowlisted URL → **`task_error`**, **`nested_subagent_ledger`** **`url_whitelist_violation`**, **honesty ledger** entry — **abort entire deepen** for execution success; **no** destructive write may succeed on the blocked scope.

### 1. `conceptual_counterpart`

- For **every** execution **phase mirror** note created or materially edited: ensure frontmatter **`conceptual_counterpart`** is a valid wikilink to the **conceptual** sibling under **`Roadmap/`** (same relative path **without** **`Execution/`** in the conceptual target).
- **Exempt:** **`roadmap-state-execution.md`** and **`workflow_state-execution.md`** — they do **not** carry **`conceptual_counterpart`**; they carry **`ledger_ref`** instead (see [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] § Execution tracking linkage).

### 2. `ledger_ref`

- When a run **closes a rollup**, **updates execution canonical state**, or appends receipt-correlated closure: ensure **`roadmap-state-execution.md`** frontmatter will include **`ledger_ref`** as a YAML array of stable ids from **`task-handoff-comms.jsonl`** / **`intent_actual_receipt`** (e.g. **`task_correlation_id`**) per Dual-Roadmap-Track.
- If **`ledger_ref`** cannot be updated honestly this run, **do not** claim Success for execution structural completion that depends on that receipt trail; return **#review-needed** with **`primary_code: execution_linkage_violation`** per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]].

### 3. `godot_code_precision` (Research + verbatim Godot 4.x citation)

- For **each new** GDScript-shaped construct (signals, **`@onready`**, **`await`**, typed callables, **`class_name`**, **`.gd` API** usage in fenced blocks): **must** invoke **ResearchSubagent** via **`Task(subagent_type: "research")`** before relying on that construct in committed narrative — per [[.cursor/agents/roadmap|agents/roadmap.md]] nested Research contract (**not** `web_search` / skill-only substitution).
- The execution note **must** contain a **verbatim** quoted passage from **Godot** official **stable** documentation or other **godot**-lane allowlisted first-party pages **plus** stable URL whose prefix matches [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] § **`godot` lane** (multi-prefix **OR**).
- If any of: Python idioms, Godot 3 syntax, wrong signal wiring, or missing citation for a **new** construct → **do not** write; return **#review-needed** / failure with Validator-facing **`godot_code_precision_violation`** ( **`recommended_action: block_destructive`** ).

---

## `validator_context` / telemetry

Echo **`gate_catalog_id: execution_godot_v1`**, **`effective_track: execution`**, **`parallel_track: godot`** in **`validator_context`** and **`queue_continuation`** so Layer 1 and Run-Telemetry stay aligned with [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]].

---

## Cross-references

- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] — parallel spine, **`ledger_ref`**, **`conceptual_counterpart`**.
- [[.cursor/agents/roadmap|agents/roadmap.md]] — lane-scoped **`roadmap_dir`**, nested **`Task`** helpers.
