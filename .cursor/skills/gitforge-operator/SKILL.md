---
name: gitforge-operator
description: Operator and debug companion for the GitForge subagent — branch choice, export contract, lock, and skip conditions. Links to authoritative specs; does not override the subagent.
---

# gitforge-operator

## Scope (private vs public export checkouts)

This skill is **maintained in the vault**. The public integration branch updates only after **gmm-roadmap-export** Step 1 and push, while Curator updates through **gmm-curator-export**. Local [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] or [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] edits may run ahead of what is visible on **`iteration-2-roadmap-rules`** until you export.

## Authority

If anything here disagrees with [[.cursor/agents/gitforge|agents/gitforge.md]], **the subagent wins**. This file is for **orientation, manual runs, and debugging** only.

## Core references (do not duplicate tables here)

- **Export surfaces by branch type** (integration vs engine, Step 1 vs Step 1b): [[.cursor/agents/gitforge|agents/gitforge.md]] (section **Export surfaces by branch type**)
- **Hand-off block** (required fields): same file, section **Hand-off (required)**
- **Parallel lock** (`.technical/.gitforge.lock`, `gitforge_lock.py`): same file, section **Parallel execution**
- **Branch purposes** (canonical table): [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] (table at **Branch purposes and export coverage**)

## Config pointers (`gitforge` in Second-Brain-Config)

Read live values from [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] § **gitforge**. Keys operators touch most:

- **`export_repo_root`** — export checkout path (e.g. `gmm-roadmap-export`)
- **`integration_branch`** — e.g. `iteration-2-roadmap-rules`
- **`export_contract.integration_includes` / `engine_includes` / `engine_forbidden_prefixes`** — what may appear on each branch type
- **`parallel_execution.tracks[]`** — lane `lane_project_id`, `export_path`, `branch_prefix` when using sandbox/godot lanes

## `GMM_PROJECT_ROOT`

For **engine** Step 1b, set **`GMM_PROJECT_ROOT`** to the vault project root for the line you are publishing — see [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] **Step 0** and **Step 1b**. Use the workflow’s example paths or your own `1-Projects/<project_id>/` path; set **explicitly** per manual sync.

## Skip / no-op conditions (summary)

Full detail: [[.cursor/agents/gitforge|agents/gitforge.md]]. In short:

- **`queue_success: false`** → GitForge does not commit/push; audit **skip**
- **`fast` pipeline mode** → GitForge skipped for that path (per queue **A.7a** contract)
- **Lock held** → skip with **`gitforge_lock_held`** in audit (parallel chats)

## Manual export (GitForge disabled or operator-driven)

1. Complete **[[.cursor/skills/vault-git-publish-checklist/SKILL.md|vault-git-publish-checklist]]** step 1 (Curator) first.  
2. `cd` **`gitforge.export_repo_root`**; `git switch` target branch.  
3. Run **Step 1** or **Step 1b** from [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] only.  
4. `git status` clean before push where policy requires it.  
5. Append a **manual** block to [[3-Resources/Second-Brain/Docs/git-audit-log|git-audit-log]] using the **Append schema** there (level-3 heading + table; note `actions` such as `export_sync_attempted; push_attempted` and `result` summary). Align with existing **Human operators** note on that page.

## GitHub MCP

Prefer **local git** for clone/commit/push. Do not depend on GitHub MCP for publish.
