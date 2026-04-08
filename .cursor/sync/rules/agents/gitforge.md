---
description: "GitForge subagent — Layer 1 post-queue git/export specialist; invoked only after prompt-queue A.7 on clean success when gitforge.enabled. Not a queue-entry pipeline."
globs: []
alwaysApply: false
---

# GitForge (context rule)

- **Subagent**: **GitForge** — single-purpose git and export-repo orchestration after a **successful** **EAT-QUEUE** prompt-queue run (**Part A** through **A.7**). Invoked only by the **Queue/Dispatcher** subagent per [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.7a**.
- **Vault index**: **Layer 1 post-run specialist** (not RESUME_ROADMAP-style Layer 2).
- **Reference**: [[.cursor/agents/gitforge.md|agents/gitforge.md]]; [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]; [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] § **gitforge**; [[3-Resources/Second-Brain/Docs/git-audit-log|git-audit-log]].

## Depends on (shared always rules)

GitForge runs in contexts that must still respect **core-guardrails** (no shell mv/cp/rm on vault PARA content except this contract’s git CLI); errors → **[[3-Resources/Errors|Errors.md]]** when appropriate.

## Subagent nesting

- GitForge **must not** call **`Task`**, **must not** read/write the prompt queue (**PQ** — see [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x**), **must not** own queue consumption or **Watcher-Result** lines for **`requestId`** queue entries.
- GitForge **may** create/remove **`{vault_root}/.technical/.gitforge.lock`** per [[.cursor/agents/gitforge.md|agents/gitforge.md]] **Parallel execution (v1)** when **`parallel_execution.enabled`** is true (serialize cross-track git), preferably via **`python3 scripts/gitforge_lock.py acquire|release`** from **`vault_root`**; **must** skip with audit + explicit message if lock cannot be acquired within **`parallel_execution.gitforge.lock_timeout_seconds`**.
- GitForge **may** run **git** and documented **export** shell steps on paths allowed by [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|git-push-workflow]].
- **Export by branch type:** **`gitforge.integration_branch`** gets the **full system mirror** (`.cursor/` including **`.cursor/sync/`**, queue **`scripts/`** + **`gitforge_lock.py`**, full **`Docs/`** + **`Docs/Core/`** backbone + **`Docs/Second-Brain-User-Flows/`**). **Engine** branches (`sandbox-` / `godot-` lines) get **spine from `origin/<integration_branch>`** + **Step 1b** (`Roadmap/` + anchors only). See [[.cursor/agents/gitforge.md|agents/gitforge.md]] § **Export surfaces by branch type** and [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] **`gitforge.export_contract`**.

## How to activate

- **Only** from Layer 1 **Queue** after **A.7a** conditions hold (**[[.cursor/rules/agents/queue.mdc|queue.mdc]]**), and **not** when **`effective_pipeline_mode`** is **`speed`** (GitForge skipped for fast pipeline runs).
- **Never** from Layer 0 chat directly, never from Layer 2 pipelines.

## GitHub parity invariant (Grok visibility)

- **Operational rule:** Grok is treated as **GitHub-only** unless explicitly provided local artifacts. Therefore, Git operations must treat **published GitHub branch state** as the collaboration surface Grok can verify.
- When roadmap/content changes are intended for Grok-reviewed branches, GitForge (or manual operator flow when GitForge is skipped) must ensure those changes are **committed and pushed** to the relevant remote branch(es), not left as local-only vault updates.
- For dual-track runs, keep **all active branches** current (integration + affected engine lane branches) according to the export contract so Grok does not observe stale or contradictory branch state.
- A run is not considered "Grok-visible complete" until post-push verification confirms the intended file paths are present on GitHub for each targeted branch.
