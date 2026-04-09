---
title: Roadmap gate catalog by track (conceptual vs execution)
created: 2026-03-26
tags: [second-brain, roadmap, gates, conceptual, execution]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]"
---

# Roadmap gate catalog by track

## Purpose

**Conceptual** and **execution** roadmaps answer different questions. Validators, Layer 1 repair policy, and anti-spin **`gate_block_signal`** must not treat **execution-only** debt as a hard failure on a **conceptual** track. This note lists gate families per track. Canonical resolution: [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`effective_track` resolution**.

**`gate_catalog_id`:** Use string **`conceptual_v1`** or **`execution_v1`** in continuation telemetry when logging which catalog applied. For **godot lane + execution** (**`parallel_track: godot`**, **`lane_project_id: godot-genesis-mythos-master`**), also log **`execution_godot_v1`** per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]].

---

## Conceptual track (`effective_track === conceptual`)

**Goal:** Coherent map, stable **design** decisions in natural language, no fatal contradictions, outline safe to resume and **ready for handoff** per [[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]]. **Design authority** for *what* to build lives on conceptual + `decisions-log` conceptual sections — see [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] Definitions.

| Gate family | Examples | Validator / queue treatment |
|-------------|----------|------------------------------|
| **Coherence** | `contradictions_detected`, `incoherence`, `state_hygiene_failure` (stale cursor vs workflow_state, narrative contradicts frontmatter) | **Hard block** allowed per Validator-Tiered-Blocks-Spec; Layer 1 may append **recal** / **handoff-audit** repair lines. |
| **Decision hygiene** | Open critical decisions, missing decisions-log anchors for claimed picks | **`needs_work`** / **`medium`**; optional wrapper. |
| **Execution-deferred** | `missing_roll_up_gates`, `safety_unknown_gap`, REGISTRY-CI / HR≥93 / rollup PASS / junior handoff bundle / registry row completion | **Informational only** on conceptual: report as **`needs_work`** or **`log_only`** with **`severity: medium`** or **`low`** — **do not** use these as sole drivers for **`block_destructive`** or **`high`**. Conceptual track **never** hard-fails completion solely on these. Layer 1 **must not** auto-append **A.5b** **`recal`** / **`handoff-audit`** repair lines when the post–little-val **effective primary** is only in **`queue.conceptual_execution_only_advisory_codes`** ([[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`queue.conceptual_execution_only_advisory_codes`**) and no true block code fired. |

### Verbose logging (conceptual)

Execution-deferred and advisory signals **must** be logged verbosely for traceability: **continuation** telemetry (see [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]), **`workflow_state`** ## Log **Status / Next** (advisory text), nested **`roadmap_handoff_auto`** report paths under **`.technical/Validator/`**, and optional **Watcher-Result** / **Errors.md** lines when a consumer needs visibility. Logging **does not** imply a hard gate on conceptual.

**Human framing (not new gates):** Layer 1 **Watcher-Result** lines for post–little-val **`roadmap_handoff_auto`** use the **`execution-deferred (advisory); out of scope for conceptual completion —`** prefix when **`primary_code`** is only in **`queue.conceptual_execution_only_advisory_codes`** ([[3-Resources/Second-Brain-Config|Second-Brain-Config]] § `queue`). Validator **`roadmap_handoff_auto`** reports include a **banner** after the title (see [[.cursor/rules/agents/validator.mdc|validator.mdc]]) so rollup/registry/CI rows are visibly **advisory** on conceptual. See [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Conceptual track: Watcher-Result prefix and Config.

---

## Execution track (`effective_track === execution`)

**Goal:** Delegatable work, registry/CI-shaped evidence where applicable, handoff bundles, roll-up closure.

| Gate family | Examples | Treatment |
|-------------|----------|-----------|
| **Roll-up / registry** | `missing_roll_up_gates`, REGISTRY-CI HOLD, HR &lt; min_handoff_conf | **`needs_work`** minimum; may escalate per Validator-Tiered-Blocks-Spec when execution claims “done”. |
| **Handoff** | Junior handoff bundle, acceptance criteria, WBS | Standard **`roadmap_handoff_auto`** / **hand-off-audit** behavior. |
| **Coherence** | Same as conceptual | **Hard block** when true block codes apply. |

### Godot lane overlay (`parallel_track === godot`, execution)

Additional gate families (**`godot_code_precision`**, linkage hygiene) apply only when **`effective_track === execution`** and the resolver has **`parallel_track: godot`** for **`godot-genesis-mythos-master`**. Full table: [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]. Validator profile overlay: [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]]. **Research URL allowlist:** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] (**godot** → **`https://docs.godotengine.org/en/stable/`** only; **§0** pre-`Task(research)` scan).

### Sandbox lane overlay (`parallel_track === sandbox`, execution)

Additional gate families (**`sandbox_code_precision`**, linkage hygiene) apply only when **`effective_track === execution`** and the resolver has **`parallel_track: sandbox`** for **`sandbox-genesis-mythos-master`**. Full table: [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]. Validator profile overlay: [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]]. **Sandbox** targets **C / C++** precision — **not** GDScript; **zero overlap** with the Godot lane docs. **Research URL allowlist:** [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] (**sandbox** → **`https://en.cppreference.com/w/`** and **`https://cplusplus.com/reference/`** only; **§0** pre-`Task(research)` scan).

---

## Cross-references

- [[.cursor/rules/agents/validator.mdc|validator.mdc]] — **`roadmap_handoff_auto`** branch with **`effective_track`**.
- [[.cursor/rules/agents/queue.mdc|queue.mdc]] — **A.5b** conceptual skip, **`layer1_resolver_hints`**, **`record-outcome`** **`blocked_track`**.
- [[scripts/queue-gate-compute.py|queue-gate-compute.py]] — **`gate_key`** includes track when **`queue.gate_key_includes_track`** is true.
ed_track`**.
- [[scripts/queue-gate-compute.py|queue-gate-compute.py]] — **`gate_key`** includes track when **`queue.gate_key_includes_track`** is true.
