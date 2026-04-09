---
title: Pipeline validator profile — Sandbox lane (execution overlay)
created: 2026-04-12
tags: [second-brain, validator, queue, roadmap, sandbox, execution]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]]"
  - "[[3-Resources/Second-Brain-Config|Second-Brain-Config]]"
  - "[[3-Resources/Second-Brain/Docs/Core/Config-Profiles|Config-Profiles]]"
---

# Pipeline validator profile — Sandbox lane (execution overlay)

## Purpose

[[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]] defines global **`pipeline_mode`** rows (**`fast`** | **`balance`** | **`extreme`**). This note defines the **additional profile snapshot** that applies when **all** of the following hold:

- **`parallel_track`** **`sandbox`**
- **`effective_track`** **`execution`**
- **`project_id`** **`sandbox-genesis-mythos-master`** (Config **`parallel_execution.tracks[]`** **`lane_project_id`** for the sandbox track)

**Merge order** (same as Config-Profiles): explicit queue **`params`** > **this overlay** (when activation matches) > **`validator_profiles[pipeline_mode]`** from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`pipeline_mode and validator_profiles`** > implicit defaults.

---

## Canonical overlay keys

These keys mirror the shape in Pipeline-Validator-Profiles § **Canonical profile keys**. When this overlay applies, **merge** these defaults **unless** the queue entry or **`effective_profile_snapshot`** already sets the same key (explicit wins).

| Key | Value | Meaning |
|-----|-------|---------|
| **`l1_post_lv_policy`** | **`always`** | After every successful roadmap-class return with **`little_val_ok`** and valid **`validator_context`**, Layer 1 runs post–little-val **`Task(validator)`** — **no** `minimal` / `conditional_nonhard_skip` shortcut for this lane + track. |
| **`nested_ira_policy`** | **`always`** | When the nested Validator→IRA cycle applies, run the **full** cycle (no **`clean_skip`** on first-pass **`log_only`**) if **`sandbox_code_precision`** or linkage gates could be under-tested. |
| **`research_synthesis_depth`** | **`full`** | Pre-deepen / scoped Research for **new C/C++ constructs** uses full synthesis depth per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]; aligns with Pipeline-Validator-Profiles § **4** escalation when safety signals exist. |
| **`design_intent_alignment_enforced`** | **`true`** | Hostile passes must require Intent Mapping + inspiration citations per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Design-Intent-Alignment|Roadmap-Gate-Catalog-Design-Intent-Alignment]] before execution writes are considered safe. |
| **`sandbox_code_precision_enforced`** | **`true`** | Hostile passes **must** evaluate **`sandbox_code_precision`** **before** treating **`Roadmap/Execution/**` writes as safe to land; see [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Sandbox-Code-Precision|Validator-Tiered-Blocks-Sandbox-Code-Precision]]. |
| **`target_nested_validator_passes`** | **`4`** | Soft budget / telemetry expectation consistent with **`extreme`** baseline; does **not** override Validator-Tiered-Blocks-Spec hard blocks. |

---

## Ordering invariant (sandbox execution)

1. **URL whitelist:** Enforce [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] for **`sandbox`** **before** accepting Research consumables for citations.
2. **Linkage:** Confirm **`conceptual_counterpart`** on target execution phase notes and **`ledger_ref`** on **`roadmap-state-execution.md`** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
3. **Design intent:** Enforce **`design_intent_alignment`** (intent mapping + inspiration citations) per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Design-Intent-Alignment|Roadmap-Gate-Catalog-Design-Intent-Alignment]] before code-precision acceptance.
4. **Research + citation:** For **new** C/C++ constructs, nested **Research** **`Task`** + verbatim allowlisted citation (see Roadmap-Gate-Catalog-Sandbox-Execution).
5. **Structural write:** Mint or update notes under **`Roadmap/Execution/`**.
6. **Nested Validator → IRA → compare:** Per Pipeline-Validator-Profiles § **5 Safety escalation** when any hard signal fires.
7. **Layer 1 post–little-val:** With **`l1_post_lv_policy: always`**, Queue runs **A.5b** hostile pass.

---

## Config hook (optional YAML)

Operators may add a **`sandbox_lane_validator_overlay: true`** flag under **`parallel_execution.tracks`** for **`id: sandbox`** in [[3-Resources/Second-Brain-Config|Second-Brain-Config]] so Layer 1 can emit **`effective_profile_snapshot`** without hand-authored hints. **Default when absent:** if **`parallel_track`** and **`lane_project_id`** match this doc’s activation tuple, treat the overlay as **active** for resolver purposes.

---

## Cross-references

- [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]] — runtime enforcement for RoadmapSubagent.
- [[.cursor/rules/agents/queue.mdc|queue.mdc]] — **A.5b**, **`effective_profile_snapshot`**, **`layer1_resolver_hints`**.
- [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] — nested helper returns, **`validator_context`**.
