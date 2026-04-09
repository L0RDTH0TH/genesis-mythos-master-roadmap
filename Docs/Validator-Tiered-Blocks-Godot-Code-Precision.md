---
title: Validator tiered blocks — Godot code precision (execution lane)
created: 2026-04-11
tags: [second-brain, validator, godot, execution, gdscript]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]"
  - "[[3-Resources/Second-Brain/Validator-Reference|Validator-Reference]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
---

# Validator tiered blocks — Godot code precision (execution lane)

## Purpose

This note extends [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] for **`roadmap_handoff_auto`** (and aligned roadmap validation) when the **Godot lane execution overlay** is active — see [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]. It defines **`reason_code`** / **`primary_code`** values and the **action matrix** row for **`godot_code_precision`** failures.

**Scope:** **`parallel_track === godot`**, **`effective_track === execution`**, artifacts under **`1-Projects/godot-genesis-mythos-master/Roadmap/Execution/`**.

---

## Closed-set additions

Validators **SHOULD** emit these codes (extend [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] §2) when the facts match:

| `reason_code` | Typical use |
|---------------|-------------|
| **`godot_code_precision_violation`** | Python idioms in GDScript blocks; Godot 3-only signal/`yield` patterns; missing **`@onready`** where the snippet accesses scene-tree paths that require deferred binding per cited Godot 4 docs; **`connect`** / **`emit`** syntax wrong for Godot 4; **new** construct with no prior nested Research **`Task`** + no verbatim Godot 4.x citation block. |
| **`execution_linkage_violation`** | New execution phase note missing **`conceptual_counterpart`**; or **`roadmap-state-execution.md`** missing / stale **`ledger_ref`** when rollups claim closure. |

**`primary_code` precedence:** When **`godot_code_precision_violation`** and **`execution_linkage_violation`** both apply, prefer **`execution_linkage_violation`** if state files are inconsistent (dual-truth risk); else **`godot_code_precision_violation`**. Document effective **`primary_code`** in the report when multiple codes appear (align with Validator-Tiered-Blocks-Spec §2 ordering for base codes + append Godot codes after base hard blockers as tie-breaker).

---

## Action matrix (addendum to Validator-Tiered-Blocks-Spec §3)

| `reason_code` (primary) | Typical `severity` | Typical `recommended_action` | Nested pipeline Success? | Allowed non-blocked pivot (same project) |
|-------------------------|-------------------|------------------------------|----------------------------|------------------------------------------|
| **`godot_code_precision_violation`** | high | **`block_destructive`** | No | **`recal`**, **`handoff-audit`**; human fix with Research + citation |
| **`execution_linkage_violation`** | high | **`block_destructive`** | No | **`sync-outputs`**, **`recal`**; repair **`ledger_ref`** / **`conceptual_counterpart`** |

**Tiered Success gate:** Unchanged from base spec — **`high`** or **`recommended_action: block_destructive`** → **no Success** for automated destructive continuation on the blocked scope.

---

## Examples (non-exhaustive) mapping to **`block_destructive`**

| Finding | Maps to |
|---------|---------|
| `self` used as Python closure where GDScript requires Callable/`bind` per docs | **`godot_code_precision_violation`** |
| `signal foo` / `connect` using Godot 3 string form where Godot 4 typed / callable pattern required | **`godot_code_precision_violation`** |
| Node path access in `_ready` without **`@onready`** when the cited Godot 4 pattern requires it for the shown structure | **`godot_code_precision_violation`** |
| New GDScript block with no **`Task(research)`** in **`nested_subagent_ledger`** for this run and no verbatim quote + URL | **`godot_code_precision_violation`** |
| Execution phase note without **`conceptual_counterpart`** | **`execution_linkage_violation`** |
| Rollup row claims **`PASS`** but **`ledger_ref`** on **`roadmap-state-execution.md`** does not record the corresponding receipt id | **`execution_linkage_violation`** |

---

## Cross-references

- [[.cursor/rules/agents/validator.mdc|validator.mdc]] — report shape, **`reason_codes`**, **`primary_code`**.
- [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profile-Godot-Lane|Pipeline-Validator-Profile-Godot-Lane]] — profile overlay for this lane.
- [[.cursor/rules/agents/godot-execution-guard|godot-execution-guard]] — pre-validator agent checklist.
