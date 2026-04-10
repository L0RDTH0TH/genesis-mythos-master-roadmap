---
description: "Sandbox lane execution guard — pre-write checks for Roadmap/Execution (conceptual_counterpart, ledger_ref, sandbox_code_precision: Research Task + C/C++ verbatim citations from whitelist-only URLs). Activates when parallel_track sandbox + execution track + sandbox-genesis-mythos-master."
globs: []
alwaysApply: false
---

# Sandbox execution guard (RoadmapSubagent runtime hook)

- **Role:** Tighten **structural writes** under **`1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/**`** when the hand-off carries **`parallel_track: sandbox`** (or Layer 0 **`EAT-QUEUE lane sandbox`** → **`## parallel_context`**) **and** **`effective_track: execution`** (from **`layer1_resolver_hints`**, queue **`params.roadmap_track`**, or **`roadmap-state.md`** per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]).
- **Does not replace:** [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]], nested Validator / IRA / little val, or [[.cursor/rules/agents/roadmap.mdc|roadmap.mdc]] — this rule **adds** lane-specific gates **before** claiming Success on deepen / bootstrap / expand that **mutate** execution tree notes or execution state files.

## Depends on (shared always rules)

This rule **depends on** and does not duplicate: [[.cursor/rules/always/core-guardrails.mdc|core-guardrails]], [[.cursor/rules/context/dual-roadmap-track.mdc|dual-roadmap-track]], [[.cursor/rules/always/mcp-obsidian-integration.mdc|mcp-obsidian-integration]].

## Depends on (execution Research gate — §0 harness)

[[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] — **mandatory §0** at harness **before** this lane guard runs: pre-snapshot, **pre-`Task(research)` hand-off URL scan**, abort entire deepen on violation **before** Research. This guard **§0** re-validates Research **return** URLs before merge.

## Normative docs (iteration-2)

- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]] — **`gate_catalog_id: execution_sandbox_v1`**, **`sandbox_code_precision`**.
- [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]] — profile overlay keys.
- [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]] — **`reason_code`** / **`block_destructive`** mapping.

---

## Pre-write checklist (mandatory order)

Run **before** snapshot-backed destructive edits to **`Roadmap/Execution/**`** phase notes or execution state bodies (including new file mint under the parallel spine):

### 0. Research URL whitelist (hardened — **must** match harness §0)

- **Prerequisite:** Harness **§0** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] **already passed** pre-hand-off scan.
- For **any** nested **`Task(subagent_type: "research")`** for **new** C/C++ constructs: citation / fetch URLs **must** match **one** of the **sandbox** lane prefix rows in [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] § **Allowlists** (cppreference **`/w/`**, cplusplus **`reference/`**, **GCC onlinedocs**, **Clang `clang.llvm.org/docs/`**, **ISO C++ Core Guidelines `isocpp.github.io/CppCoreGuidelines/`**, **MSVC `learn.microsoft.com/en-us/cpp/`** — **OR**-prefix list only). Reject bare site roots, **godot**-lane URLs, `http://`.
- If Research returns **any** non-allowlisted URL → **`task_error`**, **`url_whitelist_violation`**, **honesty ledger** — **abort entire deepen**; **no** destructive write may succeed on the blocked scope.

### 1. `design_intent_alignment`

- Every execution item must carry explicit design-intent traceability: **`conceptual_counterpart`** wikilink to conceptual authority, concrete inspiration source citation(s), and a short **Intent Mapping** block that explains how this execution item implements the chosen design decision.
- Intent Mapping must include: design intent target, inspiration anchor(s), execution mechanism, and validation signal. Missing or hand-wavy intent mapping is a hard gate failure.
- On violation: return **#review-needed** / failure with **`primary_code: design_intent_alignment_violation`**, **`recommended_action: block_destructive`**; do not claim structural Success.

### 2. `conceptual_counterpart`

- For **every** execution **phase mirror** note created or materially edited: ensure frontmatter **`conceptual_counterpart`** is a valid wikilink to the **conceptual** sibling under **`Roadmap/`** (same relative path **without** **`Execution/`** in the conceptual target).
- **Exempt:** **`roadmap-state-execution.md`** and **`workflow_state-execution.md`** — they do **not** carry **`conceptual_counterpart`**; they carry **`ledger_ref`** instead (see [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] § Execution tracking linkage).

### 3. `ledger_ref`

- When a run **closes a rollup**, **updates execution canonical state**, or appends receipt-correlated closure: ensure **`roadmap-state-execution.md`** frontmatter will include **`ledger_ref`** as a YAML array of stable ids from **`task-handoff-comms.jsonl`** / **`intent_actual_receipt`** (e.g. **`task_correlation_id`**) per Dual-Roadmap-Track.
- If **`ledger_ref`** cannot be updated honestly this run, **do not** claim Success for execution structural completion that depends on that receipt trail; return **#review-needed** with **`primary_code: execution_linkage_violation`** per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]].

### 4. `sandbox_code_precision` (Research + verbatim C/C++ citation)

- For **each new** C/C++-shaped construct (headers, **`static_assert`**, ownership / lifetime, **`restrict`**, ABI or compilation flags in narrative): **must** invoke **ResearchSubagent** via **`Task(subagent_type: "research")`** before relying on that construct in committed narrative — per [[.cursor/agents/roadmap|agents/roadmap.md]] nested Research contract (**not** `web_search` / skill-only substitution).
- The execution note **must** contain a **verbatim** quoted passage from an **allowlisted** official reference **plus** stable URL (see [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] § **`sandbox`** allowlist).
- If any of: GDScript or Python idioms in C blocks, obvious UB, wrong lane docs, or missing citation for a **new** construct → **do not** write; return **#review-needed** / failure with Validator-facing **`sandbox_code_precision_violation`** ( **`recommended_action: block_destructive`** ).

---

## `validator_context` / telemetry

Echo **`gate_catalog_id: execution_sandbox_v1`**, **`effective_track: execution`**, **`parallel_track: sandbox`** in **`validator_context`** and **`queue_continuation`** so Layer 1 and Run-Telemetry stay aligned with [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]].

---

## Cross-references

- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] — parallel spine, **`ledger_ref`**, **`conceptual_counterpart`**, lane isolation (**sandbox** vs **godot**).
- [[.cursor/agents/roadmap|agents/roadmap.md]] — lane-scoped **`roadmap_dir`**, nested **`Task`** helpers.

## Terminal vault hygiene (after Success-eligible writes)

If this run **wrote or rewrote vault files** under this guard’s scope, **`./scripts/curator_snapshot.sh`** is the **mandatory last step** — see [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]]. On script or push failure → **`task_error`**, **no** Success.
