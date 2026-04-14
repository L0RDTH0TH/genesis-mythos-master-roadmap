---
description: "Operator intent — safe Curator backup then public export guidance. Does not invoke GitForge outside the Queue A.7a contract."
globs: []
alwaysApply: false
---

# Publish to GitHub (orchestrator — Curator first)

When the user clearly wants to **back up the vault to Curator** and/or **publish to the public export repo**, match **intent** (case-insensitive), not casual use of single words like “publish” in unrelated tasks.

## Trigger phrases (examples — extend as needed)

- update the githubs / update githubs  
- ship to github / ship changes to github  
- publish vault / publish to github  
- run publish sequence  
- curator + export  
- git publish  
- push everything (when clearly meaning vault + export, not a single file)
- back up dir now

## Hard invariant — do not invent GitForge from chat

**GitForge** (**`python3 -m scripts.eat_queue_core.harness post_queue_gitforge`**, default) runs **only** after **EAT-QUEUE** completes **A.7** successfully, with a JSON hand-off, per [[.cursor/agents/gitforge|agents/gitforge.md]] and [[.cursor/rules/agents/queue|queue.mdc]] **A.7a**. Legacy **`Task(gitforge)`** only when **`gitforge.harness_enabled`** is **false**.

A **standalone chat** (“update the githubs” **without** a queue run in this session) **must not** claim to invoke GitForge as if it were a generic button. There is **no** valid hand-off without the queue processor.

## Behavior (strict order)

### Two publish behaviors (must stay explicit)

- **Private GitHub behavior:** run Curator snapshot flow (`vault_backup.private_export_repo_root` -> Curator `main`).
- **Public GitHub behavior:** run public export flow (`gitforge.export_repo_root` -> `genesis-mythos-master-roadmap` branch lane).
- Never collapse these into a single checkout or rename one lane to represent both.

### Manual bypass phrase (special case)

If the user says **`Back up dir now`** (or obvious casing/spacing variants), treat it as a **manual bypass**:

- **Do not invoke GitForge** (no **`post_queue_gitforge`** harness / no `Task(gitforge)` in this path).
- Run **`./scripts/backup_all_githubs.sh "<summary>"`** from vault root.
- This path is intended to push **all branches/tags** for both export remotes after Curator snapshot succeeds.
- On any push failure: stop and report failure; do not claim success.

### 1. Curator hard gate (always first)

Run **`./scripts/curator_snapshot.sh`** from vault root to mirror vault content into the private export checkout and push Curator with a short summary derived from context (or the user’s words).

- **Success:** push to **`curator main`** (or script fallback to `origin`) must succeed.  
- **Failure:** if there is **no git repo**, **no remote**, or **push fails** — **stop**. Point to [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]] and [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]]; do not proceed to export steps until Curator is healthy.

### 2. Public export — two legitimate paths

**A. Automated GitForge (queue-driven)**  

- Explain: **GitForge** runs **after** a successful **A.7** when [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] **`gitforge.enabled`** is true and **`effective_pipeline_mode`** is **`balance`** or **`quality`** (not **`speed`**).  
- If the user has **not** just run EAT-QUEUE: tell them to **run EAT-QUEUE** (or the relevant parallel lane) so Layer 1 can reach **A.7a** and invoke GitForge with a proper hand-off. Do **not** call **`Task(gitforge)`** from this chat without that contract.

**B. Manual export (operator)**  

- Follow [[.cursor/skills/vault-git-publish-checklist/SKILL.md|vault-git-publish-checklist]] and [[.cursor/skills/gitforge-operator/SKILL.md|gitforge-operator]]: **`cd` `gitforge.export_repo_root`**, correct branch, **Step 1** vs **Step 1b** per [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]; set **`GMM_PROJECT_ROOT`** for engine lines as documented.  
- Use **local git** only; do **not** rely on GitHub MCP for push.

### 3. Post-action

- If appropriate, remind: append or verify [[3-Resources/Second-Brain/Docs/git-audit-log|git-audit-log]] for manual runs (schema on that page).  
- Summarize: **Curator** state + what was done or deferred for **export**.

## Authority

- **Normative specs:** [[.cursor/agents/gitforge|agents/gitforge.md]], [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]], [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] § **gitforge**.  
- This rule **orchestrates and disambiguates** only; it does not replace them.
