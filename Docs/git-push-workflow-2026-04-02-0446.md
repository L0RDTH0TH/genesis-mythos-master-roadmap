---
title: Git Push Workflow (Vault → Export Repo → GitHub)
created: 2026-04-02
tags: [ops, git, workflow, export, roadmap]
source: Second-Brain internal ops note
---

# Git Push Workflow (Vault → Export Repo → GitHub)

This vault publishes roadmap + system contracts to GitHub using an **isolated export repo** so the working vault stays separate from Git history and branch churn.

## What we push (always)
- **Local vault:** `/home/darth/Documents/Second-Brain`
- **Python queue “nervous system”:** `scripts/eat_queue_core/` (mirrored to export `scripts/eat_queue_core/`) plus `scripts/queue-gate-compute.py`
- **Export repo (mirror checkout):** `/home/darth/Documents/gmm-roadmap-export`
- **GitHub remote + branch:**
  - Remote repo: `https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap.git`
  - Branch: `iteration-2-roadmap-rules`

## Step 0: Make sure you’re on the right repo/branch
From the export repo directory:
```bash
cd /home/darth/Documents/gmm-roadmap-export
git status --short
git branch --show-current
```

If you’re not on `iteration-2-roadmap-rules`, switch to it (create tracking branch if needed):
```bash
git switch iteration-2-roadmap-rules
```

## Step 1: Sync the vault into the export repo (mirror copy)
Run the rsync/copy mirror from the vault into the export repo. The important behavior is `--delete` on rsync, so the export repo becomes a “clean mirror” of the chosen vault subtrees.

```bash
cd /home/darth/Documents/gmm-roadmap-export

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
    cp "$f" "/home/darth/Documents/gmm-roadmap-export/Docs/Core/$f"
  fi
done
#
# Roadmap Structure lives at the vault workspace root (not under 3-Resources/Second-Brain/).
cp "/home/darth/Documents/Second-Brain/Roadmap Structure.md" "/home/darth/Documents/gmm-roadmap-export/Docs/Core/Roadmap Structure.md"
#
# Mirror additional global system docs that roadmap runtime depends on.
# (These live outside the `3-Resources/Second-Brain/` subtree.)
cp "/home/darth/Documents/Second-Brain/3-Resources/Errors.md" "/home/darth/Documents/gmm-roadmap-export/Docs/Core/Errors.md"
cp "/home/darth/Documents/Second-Brain/3-Resources/Watcher-Result.md" "/home/darth/Documents/gmm-roadmap-export/Docs/Core/Watcher-Result.md"
cp "/home/darth/Documents/Second-Brain/3-Resources/Watcher-Signal.md" "/home/darth/Documents/gmm-roadmap-export/Docs/Core/Watcher-Signal.md"
cd /home/darth/Documents/gmm-roadmap-export

# Mirror roadmap + project anchors
# Phase 5-1 subfolder (WIP): do NOT publish — exclude from rsync, then remove any stale copy.
P5_1_REL='Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence'
rsync -a --delete \
  --exclude="${P5_1_REL}/" \
  "/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/" \
  "/home/darth/Documents/gmm-roadmap-export/Roadmap/"
rm -rf "/home/darth/Documents/gmm-roadmap-export/Roadmap/${P5_1_REL}"

cp "/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Genesis-mythos-master-goal.md" "/home/darth/Documents/gmm-roadmap-export/Genesis-mythos-master-goal.md"
cp "/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/genesis-mythos-master-Roadmap-MOC.md" "/home/darth/Documents/gmm-roadmap-export/genesis-mythos-master-Roadmap-MOC.md"
```

## Step 2: Check what changed
```bash
git status --short
```

You should see modifications under `.cursor/`, `scripts/` (Python `eat_queue_core`), `Docs/`, `Roadmap/`, and/or the two GMM anchor files.

## Step 3: Stage, commit, and push
Typical staging set:
```bash
git add -A .cursor scripts Docs Roadmap Genesis-mythos-master-goal.md genesis-mythos-master-Roadmap-MOC.md
```

Commit (use a descriptive message that mentions the intent of the surgery/harden pass, not just “sync”):
```bash
git commit -m "Sync: <what changed> + <why>"
```

Push to the configured branch:
```bash
git push origin iteration-2-roadmap-rules
```

### If `git push` complains about missing upstream
This usually means the branch tracking wasn’t set up in the export repo:
```bash
git push -u origin iteration-2-roadmap-rules
```

## Step 4: Quick sanity check after push
```bash
git log -1 --oneline
```

Then verify the updated tree on GitHub if needed:
- [iteration-2-roadmap-rules tree](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap/tree/iteration-2-roadmap-rules)

## Gotchas
- The export repo is treated as a mirror: `rsync --delete` can remove files in `gmm-roadmap-export` if they’re removed from the vault tree.
- Python: `eat_queue_core` is synced with `--exclude='__pycache__/'`; the export repo root `.gitignore` ignores `__pycache__/` and `*.pyc` so bytecode is not committed.
- **Phase 5-1 directory** (`…/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence/`) is **intentionally omitted** from the export (work in progress). Always use the `rsync --exclude` + `rm -rf` of that path under `gmm-roadmap-export/Roadmap/` so GitHub never receives that subtree until you remove this policy.
- Do **not** push the main `Second-Brain` repo to GitHub as part of this workflow; the intent is “vault → mirror repo → published branch”.

