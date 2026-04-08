---
title: Git Push Workflow (Vault → Export Repo → GitHub)
created: 2026-04-02
updated: 2026-04-08
tags: [ops, git, workflow, export, roadmap]
source: Second-Brain internal ops note
---

# Git Push Workflow (Vault → Export Repo → GitHub)

This vault publishes roadmap + system contracts to GitHub using an **isolated export repo** so the working vault stays separate from Git history and branch churn.

## Branch purposes and export coverage (canonical contract)

The export repo carries **three collaboration roles** (branch names are the current convention; **`gitforge.integration_branch`** in [[Second-Brain-Config]] is the authority for the integration tip):

| Branch line | Role | What must appear in the export tree after a correct sync |
|-------------|------|----------------------------------------------------------|
| **`iteration-2-roadmap-rules`** (integration) | **Canonical system branch** — how the Second-Brain stack is **built** (agents, rules, skills, **`.cursor/sync`** mirror) and how it is **run** (queue, Python orchestrator, pipelines, config, operator docs, user flows). | **Full integration manifest** (below). This is the branch collaborators should clone to review or fork **the entire automation contract**, not a partial “core subset.” Public copies of vault-only operator notes (e.g. **Grok** custom instructions) live under **`Docs/`** here after sync — **not vault-only**. |
| **`sandbox-genesis-mythos-master`** (engine) | **Sandbox engine roadmap line** — aligns with **EAT-QUEUE lane `sandbox`**, Config **`lane_project_id: sandbox-genesis-mythos-master`**, `GMM_PROJECT_ROOT` for that project. | **Rule-sterile spine** (integration-equivalent `.cursor/`, `scripts/`, `Docs/`) **plus** only **`Roadmap/`** (including **`Roadmap/Execution/`** when execution track is active — see [Dual-Roadmap-Track](Dual-Roadmap-Track.md)) and sandbox anchor files from `1-Projects/sandbox-genesis-mythos-master/`. |
| **`godot-genesis-mythos-master`** (engine) | **Godot engine roadmap line** — aligns with **EAT-QUEUE lane `godot`**, Config **`lane_project_id: godot-genesis-mythos-master`**. | Same spine policy as sandbox; **plus** only Godot **`Roadmap/`** (including **`Roadmap/Execution/`** when execution track is active) and anchors from `1-Projects/godot-genesis-mythos-master/`. |

**Invariant:** Engine branches must **not** publish a **partial or experimental** ruleset as authoritative. Collaborators who need the **true** agents/rules/skills use the **integration** branch (or merge/rebase from it). Engine branches stay **roadmap-first**; spine files should match **`origin/<integration_branch>`** at publish time.

**Execution track (2026-04):** GMM engine projects use **`roadmap_track: execution`** in `roadmap-state.md` with forward work under **`Roadmap/Execution/`** (parallel folder spine to conceptual `Roadmap/` — see [Dual-Roadmap-Track](Dual-Roadmap-Track.md)). Published **`Roadmap/`** on an engine branch therefore includes **both** the conceptual tree (often frozen) **and** the **Execution** subtree when mirrored — do not assume “engine branch = conceptual-only.”

**GitForge:** When **`gitforge.enabled`** and export sync run, use **`gitforge.integration_branch`** vs engine branch name (and Config **`parallel_execution.tracks[]`** `lane_project_id` / `export_path`) to decide whether to run the **integration** mirror steps or the **engine-only** delta. See [[.cursor/agents/gitforge.md|agents/gitforge.md]] § **Export surfaces by branch type**.

### Integration branch — full manifest (build + run)

1. **Cursor backbone (authoritative + sync mirror)** — `rsync --delete`: `.cursor/agents/`, `.cursor/rules/`, `.cursor/skills/`, **`.cursor/sync/`** (required: mirrored `.md` copies of rules/skills for tooling and diff-friendly collaboration).
2. **Python queue system + lock helper** — `scripts/eat_queue_core/` (full package, include `tests/`, exclude `__pycache__`), `scripts/queue-gate-compute.py`, **`scripts/gitforge_lock.py`**.
3. **Official system docs** — `Docs/` ← `3-Resources/Second-Brain/Docs/` (`rsync --delete`).
4. **Complete dev backbone in `Docs/Core/`** — copy **every** `*.md` at **`3-Resources/Second-Brain/`** (vault dev root only; excludes `Validator-Reports/` and other subfolders), plus **`Roadmap Structure.md`** from the vault workspace root, plus **`3-Resources/Errors.md`**, **`Watcher-Result.md`**, **`Watcher-Signal.md`** (runtime contract surfaces).
5. **User-flow supplements** — `Docs/Second-Brain-User-Flows/` ← `3-Resources/Second-Brain/Second-Brain-User-Flows/` (`rsync --delete`).

Optional on integration: **`Roadmap/`** + `<proj>-goal.md` + MOC when you intentionally embed a **reference** engine on the integration line; otherwise integration commits may be **system-only**.

### Engine branches — minimal manifest

After refreshing spine from **`origin/<integration_branch>`** (see § Rule-sterile engine branches), sync **only**:

- **`Roadmap/`** (whole tree — includes **`Roadmap/Execution/`** when present) and **`<PROJ_ID>-goal.md`**, **`<PROJ_ID>-Roadmap-MOC.md`** from the matching **`GMM_PROJECT_ROOT`**.

Do **not** overwrite spine subtrees from a dirty engine working tree unless you have explicitly reconciled with the integration tip.

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
- **Per sync:** Checkout the branch you intend to update **before** rsync/commit so the right line moves on GitHub. For the **integration** branch, run **Step 1 — integration (full system mirror)**. For **engine** branches, refresh spine from the integration tip then run **Step 1b — engine (project delta only)**.
- **Vault:** Two engine projects → two paths under `1-Projects/` (e.g. `godot-genesis-mythos-master`, `sandbox-genesis-mythos-master`). Set `GMM_PROJECT_ROOT` to match the branch you are publishing.

## GitForge contract (v1)

When Second-Brain-Config **`gitforge.enabled`** is **true**, post–**EAT-QUEUE** git and export-repo orchestration for the success path **must** run through **GitForge** (**`Task(subagent_type: "gitforge")`**, Layer 1 **queue.mdc A.7a**) **when** **`effective_pipeline_mode`** is **`balance`** or **`quality`**. **`speed`** runs **skip** GitForge (no automatic vault git tail). Do **not** use ad-hoc **`git commit` / `git push`** from other agents for that path when GitForge applies — GitForge owns commit discipline, audit (**[[git-audit-log|git-audit-log]]**), and alignment with this workflow. With **`gitforge.enabled: false`**, operators remain responsible for manual git and export steps.

**References:** [[Subagent-Safety-Contract]], `.cursor/agents/gitforge.md`, `.cursor/rules/agents/gitforge.mdc`, [[Second-Brain-Config]] § **gitforge**.

## Parallel dual-track EAT-QUEUE (v1)

When Second-Brain-Config **`parallel_execution.enabled`** is **true**, two Cursor chats can run **`EAT-QUEUE lane sandbox`** and **`EAT-QUEUE lane godot`** with **separate** prompt queue files under **`.technical/parallel/<track>/`** (see [[Queue-Sources]] and [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x**). **Git remains one vault `.git`:** GitForge uses a **global lock** at **`.technical/.gitforge.lock`** with **`parallel_execution.gitforge.lock_timeout_seconds`** (default 30s). If the lock is held, the second chat’s GitForge run **skips** with an explicit audit entry (**`gitforge_lock_held`**) — do **not** block the rest of Layer 1.

**Branch / export:** Use per-track **`branch_prefix`** and **`export_path`** from Config **`parallel_execution.tracks[]`** when aligning Godot vs sandbox publish lines with this workflow’s **`GMM_PROJECT_ROOT`** and export checkout branch.

**Watcher:** The Obsidian plugin keeps using the **canonical** **`parallel_execution.watcher.canonical_path`** (default **`3-Resources/Watcher-Result.md`**). Optional **mirrors** **`Watcher-Result-sandbox.md`** / **`Watcher-Result-godot.md`** duplicate lines for operator clarity; concurrent canonical appends from two chats are **best-effort** in v1.

## Rule-sterile engine branches

**Integration tip** (**`iteration-2-roadmap-rules`**, or Config **`gitforge.integration_branch`**) carries the **full** mirrored spine: **`.cursor/`** (agents, rules, skills, **sync**), **`scripts/`** (queue stack + **`gitforge_lock.py`**), **`Docs/`** (including **`Docs/Core/`** full backbone and **`Docs/Second-Brain-User-Flows/`**).

When publishing an **engine** line (**`sandbox-genesis-mythos-master`** or **`godot-genesis-mythos-master`** on GitHub):

1. In **`gmm-roadmap-export`**, materialize spine from the integration tip first — e.g. `git fetch origin && git switch iteration-2-roadmap-rules && git pull` (when tracked), then run **Step 1 — integration** from a vault that matches that tip **or** merge **`origin/<integration_branch>`** into your export checkout so `.cursor/`, `scripts/`, and `Docs/` match integration.
2. **`git switch`** your **engine** branch (or create it from the integration tip per lineage above).
3. Set **`GMM_PROJECT_ROOT`** to the vault engine project path; run **Step 1b — engine** only — do **not** overwrite spine with a dirty engine working tree’s `.cursor/` unless you have explicitly reconciled with integration.

This keeps GitHub **engine** branches **roadmap+anchor-focused** while the **integration** branch remains the **complete** contract surface for how the system is built and run.

**Optional — extra worktrees** (still the same repo; just another directory bound to another branch):

```bash
cd /home/darth/Documents/gmm-roadmap-export
git worktree add ../gmm-roadmap-export-<label> <your-engine-branch>
```

## What we push (always)
- **Local vault:** `/home/darth/Documents/Second-Brain`
- **Python queue “nervous system”:** `scripts/eat_queue_core/` (mirrored to export `scripts/eat_queue_core/`), `scripts/queue-gate-compute.py`, **`scripts/gitforge_lock.py`**
- **Cursor sync mirror:** `.cursor/sync/` (paired with `.cursor/rules/` and `.cursor/skills/` per backbone-docs-sync)
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

Use **Step 1 — integration** when checked out on **`gitforge.integration_branch`**. Use **Step 1b — engine** when checked out on **`sandbox-genesis-mythos-master`** or **`godot-genesis-mythos-master`** (after spine refresh per § Rule-sterile engine branches).

The important behavior is **`rsync --delete`** on directory mirrors, so the export repo becomes a clean mirror of the chosen subtrees.

### Step 1 — integration (full system mirror; canonical collaboration branch)

**Prerequisites:** Export checkout is on **`iteration-2-roadmap-rules`** (or current **`gitforge.integration_branch`**). Run from the **root of the export clone or worktree**.

**Optional roadmap on integration:** If you also want `Roadmap/` + anchors on this branch, set **`GMM_PROJECT_ROOT`** to the reference engine path before running the optional block at the end. If you only publish system files, **skip** the final `GMM_PROJECT_ROOT` block.

```bash
cd /home/darth/Documents/gmm-roadmap-export   # or your worktree root
EXPORT_ROOT="$(pwd)"
VAULT="/home/darth/Documents/Second-Brain"
SB="${VAULT}/3-Resources/Second-Brain"

# Root README for GitHub (repo landing page — product + export layout)
cp "${SB}/Docs/GitHub-Export-Repository-README.md" "${EXPORT_ROOT}/README.md"

# Cursor backbone + sync mirror (collaboration-complete rules reference)
rsync -a --delete "${VAULT}/.cursor/agents/" ".cursor/agents/"
rsync -a --delete "${VAULT}/.cursor/rules/" ".cursor/rules/"
rsync -a --delete "${VAULT}/.cursor/skills/" ".cursor/skills/"
rsync -a --delete "${VAULT}/.cursor/sync/" ".cursor/sync/"

# Python EAT-QUEUE stack + GitForge lock helper
mkdir -p "scripts"
rsync -a --delete --exclude='__pycache__/' \
  "${VAULT}/scripts/eat_queue_core/" "scripts/eat_queue_core/"
cp "${VAULT}/scripts/queue-gate-compute.py" "scripts/queue-gate-compute.py"
cp "${VAULT}/scripts/gitforge_lock.py" "scripts/gitforge_lock.py"

# Official system documentation tree
rsync -a --delete "${SB}/Docs/" "Docs/"

# Docs/Core: ALL top-level Second-Brain dev *.md (full backbone — build + run reference)
mkdir -p "Docs/Core"
shopt -s nullglob
for f in "${SB}"/*.md; do
  cp "$f" "${EXPORT_ROOT}/Docs/Core/$(basename "$f")"
done
shopt -u nullglob
cp "${VAULT}/Roadmap Structure.md" "${EXPORT_ROOT}/Docs/Core/Roadmap Structure.md"
cp "${VAULT}/3-Resources/Errors.md" "${EXPORT_ROOT}/Docs/Core/Errors.md"
cp "${VAULT}/3-Resources/Watcher-Result.md" "${EXPORT_ROOT}/Docs/Core/Watcher-Result.md"
cp "${VAULT}/3-Resources/Watcher-Signal.md" "${EXPORT_ROOT}/Docs/Core/Watcher-Signal.md"

# User-flow supplements (prompt crafter, onboarding)
mkdir -p "Docs/Second-Brain-User-Flows"
rsync -a --delete "${SB}/Second-Brain-User-Flows/" "Docs/Second-Brain-User-Flows/"

# Optional: mirror one engine’s Roadmap + anchors onto the integration branch
if [ -n "${GMM_PROJECT_ROOT:-}" ]; then
  PROJ_ID="$(basename "$GMM_PROJECT_ROOT")"
  rsync -a --delete "${GMM_PROJECT_ROOT}/Roadmap/" "${EXPORT_ROOT}/Roadmap/"
  cp "${GMM_PROJECT_ROOT}/${PROJ_ID}-goal.md" "${EXPORT_ROOT}/${PROJ_ID}-goal.md"
  cp "${GMM_PROJECT_ROOT}/${PROJ_ID}-Roadmap-MOC.md" "${EXPORT_ROOT}/${PROJ_ID}-Roadmap-MOC.md"
fi
```

### Step 1b — engine (project delta only)

**Prerequisites:** Spine on disk already matches **`origin/<integration_branch>`** (merge, checkout, or re-run Step 1 integration from a clean vault). **`GMM_PROJECT_ROOT`** set to the engine path. Export checkout on the **engine** branch.

```bash
cd /home/darth/Documents/gmm-roadmap-export
EXPORT_ROOT="$(pwd)"
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

After **integration** sync: expect changes under **`.cursor/`** (including **`.cursor/sync/`**), **`scripts/`** (`eat_queue_core`, `queue-gate-compute.py`, **`gitforge_lock.py`**), **`Docs/`** (including **`Docs/Core/`** full backbone and **`Docs/Second-Brain-User-Flows/`**), **`README.md`**, and optionally **`Roadmap/`** + anchors.

After **engine** sync: expect changes under **`Roadmap/`** and the two anchor files (`<project-id>-goal.md`, `<project-id>-Roadmap-MOC.md`) unless you also refreshed spine.

## Step 3: Stage, commit, and push
**Integration branch** (from export checkout root):
```bash
git add README.md
git add -A .cursor scripts Docs
# When optional Roadmap embedded on integration:
if [ -n "${GMM_PROJECT_ROOT:-}" ]; then
  PROJ_ID="$(basename "$GMM_PROJECT_ROOT")"
  git add -A Roadmap
  git add "${PROJ_ID}-goal.md" "${PROJ_ID}-Roadmap-MOC.md"
fi
```

**Engine branch:**
```bash
: "${GMM_PROJECT_ROOT:?}"
PROJ_ID="$(basename "$GMM_PROJECT_ROOT")"
git add -A Roadmap
git add "${PROJ_ID}-goal.md" "${PROJ_ID}-Roadmap-MOC.md"
# If you intentionally refreshed full spine on this engine branch in the same commit:
# git add README.md .cursor scripts Docs
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
- Do **not** run `rsync --delete` on `Docs/` alone and stop: that removes `Docs/Core/*` and `Docs/Second-Brain-User-Flows/*` (those come from the Step 1 integration loop after `Docs/` rsync). Always run Step 1 **integration** in order, or restore `Docs/` from git before fixing.
- Do **not** push the main `Second-Brain` repo to GitHub as part of this workflow; the intent is “vault → mirror repo → published branch”.

