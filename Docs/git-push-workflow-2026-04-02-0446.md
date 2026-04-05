---
title: Git Push Workflow (Vault → Export Repo → GitHub)
created: 2026-04-02
tags: [ops, git, workflow, export, roadmap]
source: Second-Brain internal ops note
---

# Git Push Workflow (Vault → Export Repo → GitHub)

This vault publishes roadmap + system contracts to GitHub using an **isolated export repo** so the working vault stays separate from Git history and branch churn.

## Isolated export = GMM roadmap **and** engine exports (one place)

- **Only** the export checkout (`gmm-roadmap-export`) is mirrored from the vault and pushed to GitHub. The vault itself is **not** the publish target.
- **Engine-specific published trees live in that same export repo** — not a second export folder, not a separate “engine-only” remote by default. Branches (and any renames) are how you separate Godot vs sandbox (or other) lines on GitHub.
- **Lineage:** Treat **`iteration-2-roadmap-rules`** as the current integration tip. When you add an engine line, **branch from that tip** (and rename locally/remotely if your workflow calls for it). Example:
  ```bash
  cd /home/darth/Documents/gmm-roadmap-export
  git fetch origin
  git switch iteration-2-roadmap-rules
  git pull  # if you use a tracked remote tip
  git switch -c <your-engine-branch>   # e.g. engine/godot — name is operator-owned
  git push -u origin <your-engine-branch>
  ```
- **Per sync:** Checkout the branch you intend to update **before** rsync/commit so the right line moves on GitHub. For the **integration** branch, Step 1 mirrors **`.cursor/`**, **`scripts/`**, **`Docs/`**, and project **`Roadmap/`** + anchors from the vault as today. For **engine** branches, use **rule-sterile** spine handling below so `.cursor/` and core spine do not drift from the integration tip.
- **Vault:** Two engine projects → two paths under `1-Projects/` (e.g. `godot-genesis-mythos-master`, `sandbox-genesis-mythos-master`). Set `GMM_PROJECT_ROOT` to match the branch you are publishing.

## GitForge contract (v1)

When Second-Brain-Config **`gitforge.enabled`** is **true**, post–**EAT-QUEUE** git and export-repo orchestration for the success path **must** run through **GitForge** (**`Task(subagent_type: "gitforge")`**, Layer 1 **queue.mdc A.7a**) **when** **`effective_pipeline_mode`** is **`balance`** or **`quality`**. **`speed`** runs **skip** GitForge (no automatic vault git tail). Do **not** use ad-hoc **`git commit` / `git push`** from other agents for that path when GitForge applies — GitForge owns commit discipline, audit (**[[git-audit-log|git-audit-log]]**), and alignment with this workflow. With **`gitforge.enabled: false`**, operators remain responsible for manual git and export steps.

**References:** [[Subagent-Safety-Contract]], `.cursor/agents/gitforge.md`, `.cursor/rules/agents/gitforge.mdc`, [[Second-Brain-Config]] § **gitforge**.

## Parallel dual-track EAT-QUEUE (v1)

When Second-Brain-Config **`parallel_execution.enabled`** is **true**, two Cursor chats can run **`EAT-QUEUE lane sandbox`** and **`EAT-QUEUE lane godot`** with **separate** prompt queue files under **`.technical/parallel/<track>/`** (see [[Queue-Sources]] and [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x**). **Git remains one vault `.git`:** GitForge uses a **global lock** at **`.technical/.gitforge.lock`** with **`parallel_execution.gitforge.lock_timeout_seconds`** (default 30s). If the lock is held, the second chat’s GitForge run **skips** with an explicit audit entry (**`gitforge_lock_held`**) — do **not** block the rest of Layer 1.

**Branch / export:** Use per-track **`branch_prefix`** and **`export_path`** from Config **`parallel_execution.tracks[]`** when aligning Godot vs sandbox publish lines with this workflow’s **`GMM_PROJECT_ROOT`** and export checkout branch.

**Watcher:** The Obsidian plugin keeps using the **canonical** **`parallel_execution.watcher.canonical_path`** (default **`3-Resources/Watcher-Result.md`**). Optional **mirrors** **`Watcher-Result-sandbox.md`** / **`Watcher-Result-godot.md`** duplicate lines for operator clarity; concurrent canonical appends from two chats are **best-effort** in v1.

## Rule-sterile engine branches

**Integration tip** (**`iteration-2-roadmap-rules`**, or Config **`gitforge.integration_branch`**) carries the **canonical** mirrored **`.cursor/`** (agents, rules, skills) and shared automation **Docs** spine.

When publishing an **engine** line (any other branch name):

1. In **`gmm-roadmap-export`**, materialize spine from the integration tip first — e.g. `git fetch origin && git switch iteration-2-roadmap-rules && git pull` (when tracked), run Step 1’s **`.cursor/`**, **`scripts/`**, and **`Docs/`** rsync/cp **from the vault** only if the vault matches that tip; otherwise copy those subtrees from a **clean** integration checkout or merge from **`origin/iteration-2-roadmap-rules`** so the export tree’s spine is not polluted by engine-only experiments.
2. **`git switch`** your **engine** branch (or create it from integration tip per lineage above).
3. Set **`GMM_PROJECT_ROOT`** to the vault engine project path; run Step 1’s **project-specific** rsync (**`Roadmap/`**, **`<PROJ_ID>-goal.md`**, **MOC**) only — do **not** overwrite spine with a dirty engine working tree’s `.cursor/` unless you have explicitly reconciled with integration.

This keeps GitHub **engine** branches **roadmap+anchor-focused** while the **integration** branch remains the contract surface for rules and agents.

**Optional — extra worktrees** (still the same repo; just another directory bound to another branch):

```bash
cd /home/darth/Documents/gmm-roadmap-export
git worktree add ../gmm-roadmap-export-<label> <your-engine-branch>
```

## What we push (always)
- **Local vault:** `/home/darth/Documents/Second-Brain`
- **Python queue “nervous system”:** `scripts/eat_queue_core/` (mirrored to export `scripts/eat_queue_core/`) plus `scripts/queue-gate-compute.py`
- **Export repo (mirror checkout):** `/home/darth/Documents/gmm-roadmap-export` — **only** publish surface for GMM roadmap + engine exports
- **GitHub remote:** `https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap.git`
- **Branches:** **`iteration-2-roadmap-rules`** = current integration iteration; engine lines = **new branches (or renames) derived from that tip** — exact names are operator-defined. **GitHub only shows branches that have been pushed** (`git push -u origin <name>`); local-only branches never appear on the remote.
- **Root `README.md`:** Source in vault `3-Resources/Second-Brain/Docs/GitHub-Export-Repository-README.md` (no YAML frontmatter — GitHub renders the file as the repo landing page). Step 1 copies it to the export repo root.

## Step 0: Checkout target branch + set vault project root

```bash
cd /home/darth/Documents/gmm-roadmap-export   # or a worktree path for that branch
git status --short
git branch --show-current
git switch <branch-you-are-publishing>   # iteration-2-roadmap-rules and/or your engine branch from that tip
```

Set **`GMM_PROJECT_ROOT`** to the vault project whose `Roadmap/` + anchors you are mirroring (must match the engine line for that branch):

```bash
export GMM_PROJECT_ROOT="/home/darth/Documents/Second-Brain/1-Projects/godot-genesis-mythos-master"
# or
# export GMM_PROJECT_ROOT="/home/darth/Documents/Second-Brain/1-Projects/sandbox-genesis-mythos-master"
```

## Step 1: Sync the vault into the export repo (mirror copy)
Run the rsync/copy mirror from the vault into the export repo. The important behavior is `--delete` on rsync, so the export repo becomes a “clean mirror” of the chosen vault subtrees.

**Prerequisites:** `GMM_PROJECT_ROOT` is set (Step 0). Run the block from the **root of the export checkout** you are updating (main clone `gmm-roadmap-export` or a `git worktree` path). Project id for anchor filenames is the folder basename (e.g. `godot-genesis-mythos-master`).

```bash
cd /home/darth/Documents/gmm-roadmap-export   # or your worktree root
EXPORT_ROOT="$(pwd)"

# Root README for GitHub (repo landing page — product + export layout)
cp "/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Docs/GitHub-Export-Repository-README.md" "${EXPORT_ROOT}/README.md"

# Mirror Cursor backbone (agents/rules/skills)
rsync -a --delete "/home/darth/Documents/Second-Brain/.cursor/agents/" ".cursor/agents/"
rsync -a --delete "/home/darth/Documents/Second-Brain/.cursor/rules/" ".cursor/rules/"
rsync -a --delete "/home/darth/Documents/Second-Brain/.cursor/skills/" ".cursor/skills/"

# Python EAT-QUEUE “nervous system” (`eat_queue_core` package + queue gate helper)
mkdir -p "scripts"
rsync -a --delete --exclude='__pycache__/' \
  "/home/darth/Documents/Second-Brain/scripts/eat_queue_core/" "scripts/eat_queue_core/"
cp "/home/darth/Documents/Second-Brain/scripts/queue-gate-compute.py" "scripts/queue-gate-compute.py"

# Mirror user-facing system docs (3-Resources → Docs/)
rsync -a --delete "/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Docs/" "Docs/"

# Ensure Docs/Core exists, then mirror the “Core/*” subset
mkdir -p "Docs/Core"

cd /home/darth/Documents/Second-Brain/3-Resources/Second-Brain
for f in Queue-Sources.md Parameters.md Rules.md Skills.md Pipelines.md Cursor-Skill-Pipelines-Reference.md User-Questions-and-Options-Reference.md Prompt-Crafter-Param-Table.md Subagent-Safety-Contract.md Vault-Layout.md Queue-Alias-Table.md Roadmap-Quality-Guide.md Roadmap-Upgrade-Plan.md Second-Brain-Config.md Backbone.md Logs.md; do
  if [ -f "$f" ]; then
    cp "$f" "${EXPORT_ROOT}/Docs/Core/$f"
  fi
done
#
# Roadmap Structure lives at the vault workspace root (not under 3-Resources/Second-Brain/).
cp "/home/darth/Documents/Second-Brain/Roadmap Structure.md" "${EXPORT_ROOT}/Docs/Core/Roadmap Structure.md"
#
# Mirror additional global system docs that roadmap runtime depends on.
# (These live outside the `3-Resources/Second-Brain/` subtree.)
cp "/home/darth/Documents/Second-Brain/3-Resources/Errors.md" "${EXPORT_ROOT}/Docs/Core/Errors.md"
cp "/home/darth/Documents/Second-Brain/3-Resources/Watcher-Result.md" "${EXPORT_ROOT}/Docs/Core/Watcher-Result.md"
cp "/home/darth/Documents/Second-Brain/3-Resources/Watcher-Signal.md" "${EXPORT_ROOT}/Docs/Core/Watcher-Signal.md"
cd "${EXPORT_ROOT}"

# Mirror roadmap + project anchors (full tree: conceptual + Execution/)
: "${GMM_PROJECT_ROOT:?Set GMM_PROJECT_ROOT to the vault 1-Projects/<engine>-genesis-mythos-master path}"
PROJ_ID="$(basename "$GMM_PROJECT_ROOT")"
rsync -a --delete "${GMM_PROJECT_ROOT}/Roadmap/" "${EXPORT_ROOT}/Roadmap/"
cp "${GMM_PROJECT_ROOT}/${PROJ_ID}-goal.md" "${EXPORT_ROOT}/${PROJ_ID}-goal.md"
cp "${GMM_PROJECT_ROOT}/${PROJ_ID}-Roadmap-MOC.md" "${EXPORT_ROOT}/${PROJ_ID}-Roadmap-MOC.md"
```

## Step 2: Check what changed
```bash
git status --short
```

You should see modifications under `.cursor/`, `scripts/` (Python `eat_queue_core`), `Docs/`, `Roadmap/`, and the two anchor files for this engine (`<project-id>-goal.md`, `<project-id>-Roadmap-MOC.md`).

## Step 3: Stage, commit, and push
Typical staging set (from the **same** export checkout root as Step 1):
```bash
: "${GMM_PROJECT_ROOT:?}"
PROJ_ID="$(basename "$GMM_PROJECT_ROOT")"
git add README.md
git add -A .cursor scripts Docs Roadmap
git add "${PROJ_ID}-goal.md" "${PROJ_ID}-Roadmap-MOC.md"
```

Commit (use a descriptive message that mentions the intent of the surgery/harden pass, not just “sync”):
```bash
git commit -m "Sync: <what changed> + <why>"
```

Push to the **same** branch you checked out in Step 0:
```bash
git push origin <branch-you-are-publishing>
```

### If `git push` complains about missing upstream
```bash
git push -u origin <branch-you-are-publishing>
```

## Step 4: Quick sanity check after push
```bash
git log -1 --oneline
```

Then verify the updated tree on GitHub for that branch, e.g. `https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap/tree/<branch-you-are-publishing>`.

## Gotchas
- **Branch vs vault project mismatch:** Syncing `Roadmap/` from `godot-genesis-mythos-master` while checked out on a sandbox line (or vice versa) writes the wrong engine into that branch. Align `git switch` with `GMM_PROJECT_ROOT` every time.
- The export repo is treated as a mirror: `rsync --delete` can remove files in `gmm-roadmap-export` if they’re removed from the vault tree.
- Python: `eat_queue_core` is synced with `--exclude='__pycache__/'`; the export repo root `.gitignore` ignores `__pycache__/` and `*.pyc` so bytecode is not committed.
- Do **not** run `rsync --delete` on `Docs/` alone and stop: that removes `Docs/Core/*` (those files come from `cp`, not from `3-Resources/Second-Brain/Docs/`). Always run Step 1 in order, or restore `Docs/` from git before fixing.
- Do **not** push the main `Second-Brain` repo to GitHub as part of this workflow; the intent is “vault → mirror repo → published branch”.

