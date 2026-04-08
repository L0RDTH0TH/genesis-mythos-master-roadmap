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

## Where the “real” docs live (vault vs GitHub)

- **Operators:** Authoritative Markdown is edited in the **private vault** under `3-Resources/Second-Brain/` (dev backbone) and `3-Resources/Second-Brain/Docs/` (user-facing system docs). Those trees are **rsync’d** into this export repo on push (see **`Docs/git-push-workflow-2026-04-02-0446.md`**).
- **Everyone else (collaborators, web UI tools, Grok with repo access):** Treat **`iteration-2-roadmap-rules`** on GitHub as the **public automation source of truth** — especially **`Docs/`**, **`Docs/Core/`**, **`.cursor/`**, **`scripts/`**. You do **not** need the vault clone to read contracts; clone or browse this branch.
- **Grok Chat custom instructions** (paste-friendly, documentation-first): **[`Docs/Grok-Second-Brain-Custom-Instructions.md`](Docs/Grok-Second-Brain-Custom-Instructions.md)** on the integration branch — same file as in the vault, mirrored here so **GitHub always carries the full operator + Grok contract**, not vault-only drafts.

## What else is in this repo

| Area | Role |
|------|------|
| **`Roadmap/`** | Phase tree, decision records, **`Roadmap/Execution/`** when the project uses the **execution** roadmap track (implementation / hard gates — see **`Docs/Dual-Roadmap-Track.md`**), coordination state in `roadmap-state.md` / `workflow_state.md` |
| **`Docs/`** | Second Brain **automation** docs (Cursor subagents, queue, pipelines, safety, operator flows, **Grok** instructions, dual-track operator guide) — **this folder is the public copy** of vault `3-Resources/Second-Brain/Docs/` after sync |
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
- **`sandbox-genesis-mythos-master`** / **`godot-genesis-mythos-master`** — **engine roadmap lines** aligned with **EAT-QUEUE lanes** (`sandbox` / `godot`) and vault projects `sandbox-genesis-mythos-master` / `godot-genesis-mythos-master`. Spine (`.cursor/`, `scripts/`, `Docs/`) should match **`origin/iteration-2-roadmap-rules`** at publish time; **delta** is **`Roadmap/`** (including **`Roadmap/Execution/`** for active **execution-track** work) + project anchors. **Current state (2026-04):** both engine projects use **`roadmap_track: execution`** in `roadmap-state.md` — forward **`RESUME_ROADMAP`** work runs against **`Roadmap/Execution/`** and execution state files; the conceptual tree under `Roadmap/` remains design authority where frozen.

**Why you might only see some branches:** GitHub lists **remote** branches. Any extra line must be **created locally** from your chosen tip (often `iteration-2-roadmap-rules`) and published with **`git push -u origin <new-branch-name>`**.

**Related on `iteration-2-roadmap-rules`:** [Dual-track EAT-QUEUE operator](Docs/Dual-track-EAT-QUEUE-Operator.md) · [Git push workflow](Docs/git-push-workflow-2026-04-02-0446.md) · [Dual roadmap track (conceptual vs execution)](Docs/Dual-Roadmap-Track.md)

## Clone expectations

- **Complete system reference (build + run):** Clone or check out **`iteration-2-roadmap-rules`**. This is the **authoritative** mirror for agents, rules, skills, **sync**, Python queue tooling, and **full** documentation backbone — not a trimmed “core only” subset.
- **Engine-only branches** emphasize **`Roadmap/`** and anchors for one engine line; **`.cursor/`** and **`Docs/`** on those branches should match **`origin/iteration-2-roadmap-rules`** at publish time (**rule-sterile** procedure in **`Docs/git-push-workflow-2026-04-02-0446.md`**). For queue contracts or subagent behavior, **always** use the **integration** branch as source of truth.

## Operator mirror workflow

Maintainers copy from the private vault into **`gmm-roadmap-export`**, then commit and push. Step-by-step instructions: **[`Docs/git-push-workflow-2026-04-02-0446.md`](Docs/git-push-workflow-2026-04-02-0446.md)** (vault path `3-Resources/Second-Brain/Docs/…` — same content appears here after integration sync).
