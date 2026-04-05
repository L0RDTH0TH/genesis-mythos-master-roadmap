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
| **`Docs/`** | Second Brain **automation** docs (Cursor subagents, queue, pipelines, safety, operator flows) |
| **`Docs/Core/`** | **Full** dev backbone: **all** top-level `3-Resources/Second-Brain/*.md` from the vault (parameters, queue sources, rules index, MCP, templates, prompt-crafter refs, …) plus `Roadmap Structure`, Watcher, Errors copies — **how the system is built and run** |
| **`Docs/Second-Brain-User-Flows/`** | Supplemental user-flow notes (e.g. prompt crafter) mirrored from the vault |
| **`.cursor/`** | Agents, rules, skills **and** **`.cursor/sync/`** (`.md` mirrors of rules/skills for diff-friendly collaboration) |
| **`scripts/eat_queue_core/`** | Python queue orchestration package (plan, lanes, pool sync, tests) |
| **`scripts/gitforge_lock.py`** | Cross-track GitForge lock helper |
| **`scripts/queue-gate-compute.py`** | Queue gate helper |

**How to run** ingest, roadmap, EAT-QUEUE, and related flows: start at **[`Docs/README.md`](Docs/README.md)**.

## Branches on GitHub

- **`main`** — default line; may lag the active iteration.
- **`iteration-2-roadmap-rules`** — **canonical integration branch**: full **`.cursor/`** (including **`.cursor/sync/`**), full queue **`scripts/`**, complete **`Docs/`** + **`Docs/Core/`** backbone + user-flow supplements. Use this branch to **collaborate on the automation system itself**.
- **`sandbox-genesis-mythos-master`** / **`godot-genesis-mythos-master`** — **engine roadmap lines** (sandbox vs Godot); spine should match integration; content emphasis is **`Roadmap/`** + project anchors.

**Why you might only see some branches:** GitHub lists **remote** branches. Any extra line must be **created locally** from your chosen tip (often `iteration-2-roadmap-rules`) and published with **`git push -u origin <new-branch-name>`**.

## Clone expectations

- **Complete system reference (build + run):** Clone or check out **`iteration-2-roadmap-rules`**. This is the **authoritative** mirror for agents, rules, skills, **sync**, Python queue tooling, and **full** documentation backbone — not a trimmed “core only” subset.
- **Engine-only branches** emphasize **`Roadmap/`** and anchors for one engine line; **`.cursor/`** and **`Docs/`** on those branches should match **`origin/iteration-2-roadmap-rules`** at publish time (**rule-sterile** procedure in **`Docs/git-push-workflow-2026-04-02-0446.md`**). For queue contracts or subagent behavior, **always** use the **integration** branch as source of truth.

## Operator mirror workflow

Maintainers copy from the private vault into **`gmm-roadmap-export`**, then commit and push. Step-by-step instructions live in the vault as **`git-push-workflow-2026-04-02-0446.md`** (under `3-Resources/Second-Brain/Docs/`; mirrored under **`Docs/`** in this repo when synced).
