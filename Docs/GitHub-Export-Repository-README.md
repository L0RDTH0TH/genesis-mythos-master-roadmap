<!--
  Vault path: 3-Resources/Second-Brain/Docs/GitHub-Export-Repository-README.md
  Publish: copied to genesis-mythos-master-roadmap/README.md (see git-push-workflow).
  Intentionally no YAML frontmatter so GitHub’s root README renders cleanly.
-->

# Genesis Mythos Master — roadmap export

Public Markdown export from an **Obsidian Second-Brain** vault: **[L0RDTH0TH/genesis-mythos-master-roadmap](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap)**. This repository is **not** the full vault; it is a **curated mirror** (roadmap tree, project anchors, Cursor backbone, and system docs) built from a dedicated local export checkout.

## What Genesis Mythos is for

**Genesis Mythos Master** targets an **open-source, aggressively modular first-person 3D VTT generator**: procedurally shaped living worlds from shared DM and player intent, immersive first-person play, strong DM camera and tabletop control, lore feeding systemic depth, intentional re-generation for major changes, and layers meant for community remixing.

The detailed vision and phases live in the **Project Master Goal** and **`Roadmap/`** on the branch you are viewing. Root anchor filenames follow the vault **project id** (e.g. `godot-genesis-mythos-master-goal.md`, `sandbox-genesis-mythos-master-goal.md`; older exports may use `Genesis-mythos-master-goal.md`).

## What else is in this repo

| Area | Role |
|------|------|
| **`Roadmap/`** | Phase tree, decision records, execution track under `Roadmap/Execution/` when present, coordination state |
| **`Docs/`** | Second Brain **automation** docs (Cursor subagents, queue, pipelines, safety) |
| **`Docs/Core/`** | Core reference copies (Queue-Sources, Parameters, Backbone, Watcher, Errors, …) |
| **`.cursor/`** | Agents, rules, skills mirrored from the vault |
| **`scripts/eat_queue_core/`** | Python queue orchestration helper |

**How to run** ingest, roadmap, EAT-QUEUE, and related flows: start at **[`Docs/README.md`](Docs/README.md)**.

## Branches on GitHub

- **`main`** — default line; may lag the active iteration.
- **`iteration-2-roadmap-rules`** — current integration iteration for roadmap / rules work.

**Why you might only see those two:** GitHub lists **remote** branches. Any extra line (e.g. per-engine) must be **created locally** from your chosen tip (often `iteration-2-roadmap-rules`) and published with **`git push -u origin <new-branch-name>`**. Until that push happens, the branch does not exist on GitHub.

## Clone expectations

- **Full spine (agents, rules, skills, automation docs):** Prefer cloning or checking out **`iteration-2-roadmap-rules`** (or the current integration branch named in the maintainer workflow). That line is the **canonical** mirror of **`.cursor/`** and the shared **`Docs/`** layout.
- **Engine-only branches** may emphasize **`Roadmap/`** and project anchors for a specific engine line; **`.cursor/`** on those branches should match the **integration tip** at publish time (maintainers use a **rule-sterile** export procedure — see **`Docs/git-push-workflow-2026-04-02-0446.md`** § Rule-sterile engine branches). If you need the latest queue or subagent contracts, **merge or compare against `iteration-2-roadmap-rules`** rather than assuming an engine branch is the rules source of truth.

## Operator mirror workflow

Maintainers copy from the private vault into **`gmm-roadmap-export`**, then commit and push. Step-by-step instructions live in the vault as **`git-push-workflow-2026-04-02-0446.md`** (under `3-Resources/Second-Brain/Docs/`; mirrored under **`Docs/`** in this repo when synced).
