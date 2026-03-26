---
title: PromptCraft subagent (recovery)
created: 2026-03-21
tags: [second-brain, subagents, queue, prompt-craft]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Subagent-Safety-Contract]]"
  - "[[3-Resources/Second-Brain/Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Validator-Reference]]"
  - "[[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference]]"
---

# PromptCraft subagent (machine recovery crafting)

## What it is

**PromptCraftSubagent** is a **read-mostly** helper that turns **failure context** (especially post–IRA / post–nested-Validator hard blocks) into **merge-aware, linted** suggested **JSONL queue line(s)**. It does **not** replace the **question-led Prompt Crafter** ([[.cursor/rules/context/plan-mode-prompt-crafter|plan-mode-prompt-crafter]] § User-Questions §1).

## What it is not

- Not a **pipeline** (no ingest/roadmap/distill execution).
- Not allowed to **write** `.technical/prompt-queue.jsonl`, `Watcher-Result.md`, or Decision Wrappers.
- **IRA** and **nested Validator** must **not** call PromptCraft; only **Layer 0** (manual) or **Layer 1** (EAT-QUEUE, when Config allows) invokes **`Task(prompt_craft)`**.

## Layers

Canonical labels: [[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference|Subagent-Layers-Reference]].

| Layer | Who | PromptCraft role |
|-------|-----|-------------------|
| **L0** | Cursor chat | User says **REPAIR CRAFT** / **PROMPT CRAFT RECOVERY** → `Task(prompt_craft)` with hand-off; operator pastes or saves suggested lines. |
| **L1** | Queue/Dispatcher | **A.5d:** If `recovery_auto_craft_enabled`, parse pipeline return for `prompt_craft_request` → `Task(prompt_craft)` → optional append when `recovery_auto_append` + empty `lint_blockers`. **A.5b:** If `post_little_val_repair_use_prompt_craft`, after post–little-val **hard block** on roadmap repair-eligible entries → `Task(prompt_craft)` with **`craft_source: a5b_post_little_val`** + **`a5b_repair_context`** → normalize + append, or **A.5b.3** minimal fallback on failure/lint. |
| **L2** | Pipelines | Emit **`prompt_craft_request`** + **`ira_repair_bundle`** YAML trailer on **`failure`** / **`#review-needed`** when IRA ran and nested validator still hard-blocks. |

## Return contract

PromptCraft **must** end its return with a structured tail (see [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] § PromptCraftSubagent):

- `status`: **Success** | **failure**
- `jsonl_lines_suggested` (or single `jsonl_line_suggested`)
- `warnings[]`, `lint_blockers[]` (non-empty **blocks** Layer 1 append)
- optional `effective_params_preview`, `recovery_metadata`

## Merge rules

When proposing **`RESUME_ROADMAP`** (or other modes with rich `params`), merge like the roadmap dispatcher: **queue / hand-off params override** Config **`prompt_defaults.roadmap`** and **`prompt_defaults.profiles[profile]`** for any key present; use `deepMerge` semantics (nested objects merge, last writer wins on scalars). Document overrides in `recovery_metadata.rationale_short`.

## A.5b post–little-val repair craft

When **`craft_source`** is **`a5b_post_little_val`**, PromptCraft receives **`a5b_repair_context`** from the Queue (repair policy action, validator report path, codes, project_id, excerpt of the triggering queue entry). It emits **one** suggested **`RESUME_ROADMAP`** line with merge-aware **`params`** and richer **`user_guidance`** than the **A.5b.3** minimal template. Layer 1 still sets **`queue_priority`**, **`validator_repair_followup`**, fresh **`id`**, and **`incoherence_retries_remaining`** when applicable. On PromptCraft failure, empty suggestions, or non-empty **`lint_blockers`**, Layer 1 uses **A.5b.3** only. Agent behavior: `.cursor/agents/prompt-craft.md` § **A.5b**.

## A.1b empty-queue continuation bootstrap

When **`craft_source`** is **`empty_queue_bootstrap`**, PromptCraft receives **`empty_bootstrap_context`** (selected **`continuation_record`** from `.technical/queue-continuation.jsonl`, **`bootstrap_key`** for **`idempotency_key`**, optional tail excerpt). It emits **one** suggested line (typically **`RESUME_ROADMAP`** **`deepen`**) honoring **`suggested_next`** when valid, with merge-aware **`params`** and traceable **`user_guidance`**. Layer 1 never runs PromptCraft for bootstrap when **`empty_queue_bootstrap_prompt_craft`** is **false** (deterministic line from **`suggested_next`** / **`project_id`** instead). Agent behavior: `.cursor/agents/prompt-craft.md` § **A.1b**.

## Pre-append lint (Layer 1)

Separate from **recovery_outcome** Validator: shallow checks (valid JSON, `mode` known per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]], required fields for mode). Gated by **`recovery_pre_append_lint_enabled`** in [[3-Resources/Second-Brain-Config|Second-Brain-Config]].

## Recovery outcome Validator

After suggested lines are **appended and executed**, optional **`VALIDATE`** / **`validation_type: recovery_outcome`** — hostile pass: **did the original failure clear?** See [[3-Resources/Second-Brain/Validator-Reference|Validator-Reference]] § **recovery_outcome**; model: `validator.recovery_outcome.model`.

## Implementation files

- Agent prompt: `.cursor/agents/prompt-craft.md`
- Context rule: `.cursor/rules/agents/prompt-craft.mdc`
- Queue hooks: `.cursor/rules/agents/queue.mdc` **A.1b** (empty-queue bootstrap), **A.5b** (post–little-val repair), **A.5d** (pipeline failure craft), **A.5e** (continuation log)
