---
description: "PromptCraftSubagent — recovery-only queue line crafter; read-mostly; no queue writes; no Task/IRA/Validator nesting. Layer 1: A.5d (prompt_craft_request) or A.5b (post_little_val, craft_source a5b_post_little_val) when Config allows."
globs: []
alwaysApply: false
---

# PromptCraftSubagent (context rule)

- **Role:** Turn **failure context** (`failure_envelope`, **`ira_repair_bundle`**, `craft_intent`, `error_correlation_id`) into **merge-aware, linted** suggested **JSONL** line(s). **Not** the question-led Prompt Crafter ([[.cursor/rules/context/plan-mode-prompt-crafter|plan-mode-prompt-crafter]]).
- **Invocation:** **Layer 0** — user says **REPAIR CRAFT** or **PROMPT CRAFT RECOVERY** → parent calls **`Task`** with **subagent_type `prompt_craft`** (if the host rejects unknown types, use **generalPurpose** and load [[.cursor/agents/prompt-craft|agents/prompt-craft.md]] as the system prompt). **Layer 1** — (1) when **`recovery_auto_craft_enabled`** is **true** and a pipeline return contains **`prompt_craft_request`** (**A.5d**); (2) when **`post_little_val_repair_use_prompt_craft`** is **true** and post–little-val hard block triggers repair append (**A.5b**), hand-off includes **`craft_source: "a5b_post_little_val"`** and **`a5b_repair_context`**; (3) when **`queue_continuation.empty_queue_bootstrap_enabled`** and **`empty_queue_bootstrap_prompt_craft`** are **true** and **A.1b** selects an eligible continuation record, hand-off includes **`craft_source: "empty_queue_bootstrap"`** and **`empty_bootstrap_context`**. See [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.1b**, **A.5b**, **A.5d**.
- **Forbidden:** Writing `.technical/prompt-queue.jsonl`, `Task-Queue.md`, `Watcher-Result.md`, Decision Wrappers; calling **`Task`** for pipelines; calling IRA or Validator; mutating user notes for “fixes.”
- **Return:** `status`, `jsonl_lines_suggested` | `jsonl_line_suggested`, `warnings`, `lint_blockers`, optional `effective_params_preview`, `recovery_metadata`. Non-empty **`lint_blockers`** ⇒ Layer 1 does **not** append.
- **Depends on:** core-guardrails, Subagent-Safety-Contract § PromptCraftSubagent, [[3-Resources/Second-Brain/Docs/Prompt-Craft-Subagent|Prompt-Craft-Subagent]].

**Agent prompt:** `.cursor/agents/prompt-craft.md`
