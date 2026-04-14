---
name: vault-git-publish-checklist
description: Human operator checklist for safe vault-to-GitHub publish — Curator full backup first, then export checkout and branch-aware mirror. Companion to automation; does not replace the post_queue_gitforge harness.
---

# vault-git-publish-checklist

**One-line intent:** In chat, you can ask the agent to follow **[[.cursor/rules/context/publish-to-github.mdc|publish-to-github]]** (e.g. “update the githubs”) — it runs Curator first and routes export **without** falsely invoking GitForge outside the EAT-QUEUE **A.7a** contract.

## Scope (vault vs integration GitHub)

This checklist is **authored in the vault**. The **integration** branch on GitHub (`iteration-2-roadmap-rules`) updates only after **export Step 1** rsync and push. Until then, local edits to [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] or [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] may differ from what collaborators see on the remote.

## Authority

- **Automated post–EAT-QUEUE publish:** **`python3 -m scripts.eat_queue_core.harness post_queue_gitforge`** owns behavior after **A.7a** (branch guards, lock, engine-only rules). This skill is a **checklist + links**, not a second spec.
- **Normative procedures:** [[.cursor/agents/gitforge|agents/gitforge.md]] and [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]].

## GitHub MCP

Use **local git** in both export checkouts: **`vault_backup.private_export_repo_root`** (Curator) and **`gitforge.export_repo_root`** (public). Do **not** rely on GitHub MCP for push; prefer terminal git to avoid tool-pass flakiness.

## When to use

- Manual “ship it” after substantive vault edits  
- Teaching new operators  
- **`gitforge.enabled: false`** or manual export  
- Verifying behavior after EAT-QUEUE (you still get [[3-Resources/Second-Brain/Docs/git-audit-log|git-audit-log]] when GitForge runs)

## Mandatory sequence

### 1. Curator gate (nuke-prevention, private export lane)

**Hard gate:** Never proceed to the export checkout without a **successful** `./scripts/curator_snapshot.sh` and private export push to **`curator main`** (or your documented vault backup remote per [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]]). This is the **private full-vault safety net.**

**Never touch the export checkout for publish work** without a **fresh successful** Curator snapshot and push.

**Prereq:** `vault_backup.private_export_repo_root` points to **`/home/darth/Documents/gmm-curator-export`** and that checkout has **`curator`** (or `origin`) configured — see [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup and Recovery Strategy]].

### 2. Automation path

If you use EAT-QUEUE with **[[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]]** **`gitforge.enabled: true`** and **`gitforge.harness_enabled: true`** (default): after a clean **A.7**, Layer 1 runs **`post_queue_gitforge`**. Do not duplicate GitForge steps here; follow [[.cursor/agents/gitforge|agents/gitforge.md]].

### 3. Manual path — export checkout

1. Read **`gitforge.export_repo_root`** from Config (see **gitforge** in [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]]; example path is often `/home/darth/Documents/gmm-roadmap-export`).
2. `cd` to that directory.
3. `git switch` the target branch: **`gitforge.integration_branch`** (e.g. `iteration-2-roadmap-rules`) for the **full system mirror**, or the **engine** branch name for roadmap-only lines — see **`parallel_execution.tracks[]`** when using parallel lanes.

### 4. Mirror (Step 1 vs Step 1b)

Follow **exactly** [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]:

- **Integration:** **Step 1 — integration** (full `.cursor/`, `scripts/`, `Docs/`, etc.).
- **Engine:** **Step 1b — engine** — **Roadmap/** + anchors only.

For **engine** lines, set **`GMM_PROJECT_ROOT`** per **Step 0** in the workflow (example paths for Godot vs sandbox under `1-Projects/...`). Set it **explicitly in the shell** for each manual engine sync so rsync targets the correct project.

### 5. Safety reminders

- **Engine branches:** never publish **`gitforge.export_contract.engine_forbidden_prefixes`** (`.cursor/`, `scripts/`, `Docs/`) — see [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] § **gitforge.export_contract**.
- **Parallel EAT-QUEUE:** respect **`.technical/.gitforge.lock`** and **`scripts/gitforge_lock.py`** (see workflow **Parallel dual-track** section).

### 6. Verify

- [[3-Resources/Second-Brain/Docs/git-audit-log|git-audit-log]] (GitForge or manual row per schema there)  
- Optional: Watcher / queue mirrors per [[.cursor/rules/agents/queue.mdc|queue]]

## Companion

For GitForge-only orientation and manual-debug steps, see [[.cursor/skills/gitforge-operator/SKILL.md|gitforge-operator]].
