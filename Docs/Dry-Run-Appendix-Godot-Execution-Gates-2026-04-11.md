---
title: Dry-run appendix — Execution gates (Godot + Sandbox lanes)
created: 2026-04-11
tags: [second-brain, roadmap, godot, sandbox, execution, dry-run]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]"
  - "[[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]]"
---

# Dry-run appendix — Execution gates (Godot + Sandbox lanes)

**Part A — Godot (`godot-genesis-mythos-master`):** Static scan of project-root MOC, master goal, and all **`Roadmap/Execution/**/*.md`** notes for **`conceptual_counterpart`** and **`ledger_ref`** against [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] and [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]. **Part B — Sandbox (`sandbox-genesis-mythos-master`):** Same contract **when** Execution tree exists; precision stack is [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]] (**C/C++**). **Both lanes:** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] **§0** runs **before** **`Task(research)`** — **Godot (multi-prefix OR):** **`https://docs.godotengine.org/en/stable/`**, **`.../classes/`**, **`.../tutorials/scripting/gdscript/`**, **`https://godotengine.org/article/`**, **`https://godotengine.org/releases/`**; **Sandbox (multi-prefix OR):** **`https://en.cppreference.com/w/`**, **`https://cplusplus.com/reference/`**, **`https://gcc.gnu.org/onlinedocs/`**, **`https://clang.llvm.org/docs/`**, **`https://isocpp.github.io/CppCoreGuidelines/`**, **`https://learn.microsoft.com/en-us/cpp/`** — **no cross-lane URLs** for code-precision. **Method:** automated frontmatter grep + manual classification. **Last hygiene pass:** 2026-04-11 (godot ledger backfill + **2.4.1** tertiary); **2026-04-14** (GDScript tutorial path + Clang/Core Guidelines prefixes).

---

## Part A — Godot lane

## `godot-genesis-mythos-master-Roadmap-MOC.md`

| Check | Result |
|-------|--------|
| **`conceptual_counterpart`** | **N/A** — project MOC is not an execution phase mirror; contract applies to notes under **`Roadmap/Execution/`** parallel spine, not the hub MOC. |
| **`ledger_ref`** | **N/A** — not an execution state file. |

---

## `godot-genesis-mythos-master-goal.md`

| Check | Result |
|-------|--------|
| **`conceptual_counterpart`** | **N/A** — PMG / goal note; not under **`Roadmap/Execution/`**. |
| **`ledger_ref`** | **N/A** |

---

## `Roadmap/Execution/roadmap-state-execution.md`

| Check | Result |
|-------|--------|
| **`conceptual_counterpart`** | **Expected absent** — coordination file; use **`ledger_ref`** per Dual-Roadmap-Track. |
| **`ledger_ref`** | **PRESENT** — YAML array includes hygiene placeholder **`task-handoff-2026-04-11-hygiene-backfill`** and deepen receipt **`ledger-exec-deepen-phase-2-4-1-signal-callable-2026-04-11`**. Replace placeholders with real **`task_correlation_id`** values from **`.technical/parallel/godot/task-handoff-comms.jsonl`** when operator completes live EAT-QUEUE handoffs. |

---

## `Roadmap/Execution/workflow_state-execution.md`

| Check | Result |
|-------|--------|
| **`conceptual_counterpart`** | **Expected absent** — coordination log; conceptual state remains **`../workflow_state`**. |
| **`ledger_ref`** | **PRESENT** (optional mirror) — same ids as **`roadmap-state-execution`** for joinable ledger replay. |

---

## Execution phase mirrors (`Roadmap/Execution/**` excluding state files)

**Files scanned:** all **`.md`** under **`1-Projects/godot-genesis-mythos-master/Roadmap/Execution/`**.

| Metric | Count |
|--------|-------|
| Notes with **`conceptual_counterpart`** in frontmatter | **25** |
| Notes **without** **`conceptual_counterpart`** (coordination only) | **2** — **`roadmap-state-execution.md`**, **`workflow_state-execution.md`** |

**Assessment:** All mirrored phase notes include **`conceptual_counterpart`**; the two gaps are the Execution-root state files, which are **exempt** from **`conceptual_counterpart`** by design.

---

## `godot_code_precision`

**Pre-existing content:** Not evaluated line-by-line in this dry-run. After policy effective date, Validator / RoadmapSubagent must enforce Research + verbatim Godot 4.x citations for **new** constructs per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Godot-Code-Precision|Validator-Tiered-Blocks-Godot-Code-Precision]]. **2026-04-11 sample:** [[1-Projects/godot-genesis-mythos-master/Roadmap/Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-4-Post-Validation-Commit-Orchestration/Phase-2-4-1-Execution-Signal-Callable-Patterns-for-Commit-Orchestration-Hooks-Roadmap-2026-04-11-1200|Phase-2-4-1 execution signal/Callable deepen]] includes a **Grammar / Authority** block with stable doc URLs.

| §0 check | Result |
|---------|--------|
| **Pre-`Task(research)` abort (godot)** | Hand-off containing e.g. **`https://evil.com/`** or non-allowlisted path (e.g. **`https://docs.godotengine.org/en/latest/...`**) → **§0** **`url_whitelist_violation`** **before** Research — same contract as Part B sandbox row. |
| **Example — newly explicit pass (godot)** | **`https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html`** — **passes** §0 (prefix **`https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/`**); **`https://godotengine.org/article/...`** still passes via **`/article/`** prefix. |

---

## Follow-ups

1. ~~Add **`ledger_ref`** to **`roadmap-state-execution.md`**~~ — **done** (2026-04-11); optional mirror on **`workflow_state-execution.md`** — **done**.
2. Optional: add **`godot_lane_validator_overlay: true`** under the godot track row in [[3-Resources/Second-Brain-Config|Second-Brain-Config]] if machine merge of [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]] is desired (documented as optional in that note).
3. Mint optional **secondary 2.4** execution mirror when operator wants a roll-up row before **2.4.2–2.4.5** tertiaries.

---

## Part B — Sandbox lane (`sandbox-genesis-mythos-master`)

**Isolation:** Sandbox execution precision is **C/C++**-shaped per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]] — **not** GDScript; **no** reuse of Godot gate docs for sandbox validation.

## Execution state + mirrors (when `Roadmap/Execution/` exists)

| Check | Expected |
|-------|----------|
| **`roadmap-state-execution.md` `ledger_ref`** | **PRESENT** when operator has run execution rollups; backfill placeholders per Dual-Roadmap-Track if missing. |
| **`workflow_state-execution.md` `ledger_ref`** | Optional mirror — **PRESENT** when operator mirrors godot hygiene pattern. |
| **Phase mirrors `conceptual_counterpart`** | **Required** on every execution phase note under **`1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/**`** (excluding the two Execution-root state files). |

**Files scanned (when path exists):** all **`.md`** under **`1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/`**. If the directory is absent or empty, record **N/A — execution spine not minted** for this dry-run.

## `sandbox_code_precision` + whitelist

| Check | Result |
|-------|--------|
| **Automatic guard** | [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]] applies on **`parallel_track: sandbox`** + **`effective_track: execution`** + **`project_id: sandbox-genesis-mythos-master`** — **no** manual step (see [[.cursor/agents/roadmap|agents/roadmap.md]]). |
| **Research URL allowlist (strict, multi-prefix)** | [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] — **`sandbox`** lane **OR**-prefix list: cppreference **`/w/`**, cplusplus **`reference/`**, **GCC onlinedocs**, **Clang `clang.llvm.org/docs/`**, **`isocpp.github.io/CppCoreGuidelines/`**, **MSVC `learn.microsoft.com/en-us/cpp/`**. Non-whitelisted URLs → **`task_error`** + **`url_whitelist_violation`** + honesty ledger. |
| **Example — newly explicit pass (sandbox)** | **`https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html`** — **passes** §0 (prefix **`https://clang.llvm.org/docs/`**); would **fail** on **godot** lane. |
| **Pre-`Task(research)` abort** | **2026-04-12:** If hand-off contains e.g. **`https://evil.com/`** or any disallowed host, **§0** fails **before** Research launches — **entire deepen aborts**; no lane guard “success” path for structural writes. |

---

## Cross-lane summary (both lanes)

| Lane | `gate_catalog_id` | Code-precision family | Research allowlist (vetted multi-prefix **OR**) |
|------|-------------------|------------------------|--------------------------------------------------|
| **godot** | **`execution_godot_v1`** | **`godot_code_precision`** | **`docs.godotengine.org/en/stable/`**, **`.../classes/`**, **`.../tutorials/scripting/gdscript/`**, **`godotengine.org/article/`**, **`godotengine.org/releases/`** |
| **sandbox** | **`execution_sandbox_v1`** | **`sandbox_code_precision`** | **`en.cppreference.com/w/`**, **`cplusplus.com/reference/`**, **`gcc.gnu.org/onlinedocs/`**, **`clang.llvm.org/docs/`**, **`isocpp.github.io/CppCoreGuidelines/`**, **`learn.microsoft.com/en-us/cpp/`** |

**Assessment:** Backbone + rules **2026-04-14**: **§0** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] runs **first** (pre-hand-off URL scan **before** **`Task(research)`**); **multi-prefix OR** per lane (vendor-maintained paths only); Config **`research_whitelist_enforced: true`** on **`parallel_execution.tracks[]`** for Layer 1 audit hints. **Good URL** (matches any lane prefix) → Research may launch after scan. **Bad URL** (e.g. **`https://evil.com/`**, wrong lane, **`/latest/`** Godot docs) → **`task_error`** + **`url_whitelist_violation`** at §0 — **before** **`Task(research)`** when embedded in hand-off.
