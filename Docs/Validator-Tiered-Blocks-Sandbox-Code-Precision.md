---
title: Validator tiered blocks — Sandbox code precision (execution lane)
created: 2026-04-12
tags: [second-brain, validator, sandbox, execution, c, cpp]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]"
  - "[[3-Resources/Second-Brain/Validator-Reference|Validator-Reference]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
---

# Validator tiered blocks — Sandbox code precision (execution lane)

## Purpose

This note extends [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] for **`roadmap_handoff_auto`** (and aligned roadmap validation) when the **Sandbox lane execution overlay** is active — see [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]. It defines **`reason_code`** / **`primary_code`** values and the **action matrix** row for **`sandbox_code_precision`** failures.

**Scope:** **`parallel_track === sandbox`**, **`effective_track === execution`**, artifacts under **`1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/`**. **Sandbox** is the **C-powered engine** lane; precision rules target **C / C++** syntax, headers, memory safety, and compilation — **not** GDScript (see [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] lane isolation).

---

## Closed-set additions

Validators **SHOULD** emit these codes (extend [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] §2) when the facts match:

| `reason_code` | Typical use |
|---------------|-------------|
| **`sandbox_code_precision_violation`** | Undefined behavior patterns in fenced C/C++ blocks; missing include / header-guard discipline where the note claims compile-ready structure; invalid pointer lifetime or alignment claims; **new** construct with no prior nested Research **`Task`** + no verbatim allowlisted citation block; **non-whitelisted URL** in authority section ([[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] violation). |
| **`execution_linkage_violation`** | New execution phase note missing **`conceptual_counterpart`**; or **`roadmap-state-execution.md`** missing / stale **`ledger_ref`** when rollups claim closure. |

**`primary_code` precedence:** When **`sandbox_code_precision_violation`** and **`execution_linkage_violation`** both apply, prefer **`execution_linkage_violation`** if state files are inconsistent (dual-truth risk); else **`sandbox_code_precision_violation`**. Document effective **`primary_code`** in the report when multiple codes appear (align with Validator-Tiered-Blocks-Spec §2 ordering for base codes + append Sandbox codes after base hard blockers as tie-breaker).

---

## Action matrix (addendum to Validator-Tiered-Blocks-Spec §3)

| `reason_code` (primary) | Typical `severity` | Typical `recommended_action` | Nested pipeline Success? | Allowed non-blocked pivot (same project) |
|-------------------------|-------------------|------------------------------|----------------------------|------------------------------------------|
| **`sandbox_code_precision_violation`** | high | **`block_destructive`** | No | **`recal`**, **`handoff-audit`**; human fix with Research + allowlisted citation |
| **`execution_linkage_violation`** | high | **`block_destructive`** | No | **`sync-outputs`**, **`recal`**; repair **`ledger_ref`** / **`conceptual_counterpart`** |

**Tiered Success gate:** Unchanged from base spec — **`high`** or **`recommended_action: block_destructive`** → **no Success** for automated destructive continuation on the blocked scope.

---

## Examples (non-exhaustive) mapping to **`block_destructive`**

| Finding | Maps to |
|---------|---------|
| Use-after-free or double-free pattern presented as valid without citation | **`sandbox_code_precision_violation`** |
| `void*` arithmetic or strict-aliasing violation presented as portable | **`sandbox_code_precision_violation`** |
| Header / interface block without include guards or `#pragma once` where the note claims drop-in compile | **`sandbox_code_precision_violation`** |
| New C/C++ block with no **`Task(research)`** in **`nested_subagent_ledger`** for this run and no verbatim quote + allowlisted URL | **`sandbox_code_precision_violation`** |
| Citation URL points at **`docs.godotengine.org`** on sandbox lane | **`sandbox_code_precision_violation`** (wrong lane authority) |
| Execution phase note without **`conceptual_counterpart`** | **`execution_linkage_violation`** |
| Rollup row claims **`PASS`** but **`ledger_ref`** on **`roadmap-state-execution.md`** does not record the corresponding receipt id | **`execution_linkage_violation`** |

---

## Cross-references

- [[.cursor/rules/agents/validator.mdc|validator.mdc]] — report shape, **`reason_codes`**, **`primary_code`**.
- [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Sandbox-Lane|Pipeline-Validator-Profile-Sandbox-Lane]] — profile overlay for this lane.
- [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]] — pre-validator agent checklist.
