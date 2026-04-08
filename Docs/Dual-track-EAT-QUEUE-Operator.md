---
title: Dual-track EAT-QUEUE operator guide
created: 2026-04-05
updated: 2026-04-08
tags: [second-brain, eat-queue, parallel, operator]
para-type: Resource
status: active
---

# Dual-track EAT-QUEUE operator guide

Run **two Cursor chats** in parallel on **separate prompt-queue bundles** (sandbox vs godot) without corrupting **PQ**, **continuation**, or **git**. This note is the **operator contract**; normative mechanics live in [[.cursor/rules/agents/queue.mdc|queue.mdc]] (**A.0x**, **A.0.4**, **A.0z**, **A.2a**, **A.2a.1**, **A.6**, **A.7**, **A.7a**), [[.cursor/rules/always/dispatcher.mdc|dispatcher.mdc]], and [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] (`parallel_execution`, `queue.central_pool_fanout_enabled`).

## Must

1. **Lane in the trigger** — Each parallel chat must use an explicit lane, e.g. **`EAT-QUEUE lane sandbox`** in chat A and **`EAT-QUEUE lane godot`** in chat B. Bare **`EAT-QUEUE`** leaves **`queue_lane_filter`** unset, uses **legacy** **PQ** at `.technical/prompt-queue.jsonl`, and processes **all** lanes in one file — not dual-track.
2. **Config** — `parallel_execution.enabled: true` and `default_to_legacy: false` (see Config machine-readable block). Tracks **`sandbox`** and **`godot`** must match your **`technical_subdir`** rows. Set **`queue.central_pool_fanout_enabled: true`** to use **`.technical/prompt-queue.jsonl`** as the single append pool; Layer 1 **A.0.4** copies lane-aligned lines into each track **PQ** before dispatch. Each track row should set **`lane_project_id`** (slug under **`1-Projects/`**) so **A.2a.1** rejects roadmap lines for the wrong project.
3. **Queue lines** — Append new work to the **central pool** **`.technical/prompt-queue.jsonl`** when fanout is enabled (Prompt Crafter already targets this path). Set **`queue_lane`** on JSONL entries per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] (Queue lanes). Use **`shared`** only when the work should run with **sandbox ∪ shared** or **godot ∪ shared** (see **A.2a**). Prefer explicit **`default`** on general work when not parallel. Do not rely on hand-editing **`.technical/parallel/<track>/prompt-queue.jsonl`** when fanout is on — it is overwritten at hydrate.
4. **Layer 0 hand-off** — The parent chat must invoke **`Task(subagent_type: queue)`** with:
   - **`## queue_lane_filter`** plus the lane token (lowercase), and
   - When parallel is on and the lane matches a configured track, **`## parallel_context`** (YAML) with **`resolved_prompt_queue_path`**, **`technical_bundle_root`**, sibling paths, **`parallel_track`**, **`parallel_branch_prefix`**, **`parallel_export_path`**, and **`lane_project_id`** / **`lane_project_root`** / **`roadmap_dir`** when Config defines **`lane_project_id`** (dispatcher.mdc).
5. **Post-drain recovery expectation** — With lane trigger + config enabled, a fully drained lane can self-seed one continuation via hardened **A.1b** bootstrap when no usable continuation record exists. Bare **`EAT-QUEUE`** still bypasses per-lane bundles.

## Must-not

1. **Same `project_id` in both chats at once** — Roadmap truth lives under `1-Projects/<project_id>/Roadmap/` (`roadmap-state.md`, `workflow_state.md`, phase notes, `decisions-log.md`). Two concurrent **`RESUME_ROADMAP`** (or similar) runs on the **same** project cause races and provisional / hygiene failures. **Policy:** assign **one active project per track**, or **serialize** roadmap work for a shared project to one chat.
2. **Assuming zero git contention** — Vault has **one** `.git`. GitForge serializes via **`.technical/.gitforge.lock`**; the losing track **skips** git for that run (not a failure of the other track).

## Expect

1. **Watcher-Result** — Appends go to the **canonical** path (`parallel_execution.watcher.canonical_path`) for the Obsidian plugin. Concurrent appends may **interleave** (best-effort v1). When **`enable_mirrors`** is true, each track also mirrors to **`Watcher-Result-sandbox.md`** / **`Watcher-Result-godot.md`** for a per-chat tail.
2. **GitForge** — After **A.7**, balance/quality runs invoke GitForge once. If the lock is held, return is **`skipped`** with message like **`GitForge skipped — lock held by other track`** and an audit line — **queue consumption is not rolled back**.
3. **Deterministic lock helper** — GitForge should run **`python3 scripts/gitforge_lock.py acquire`** before git and **`release`** in a **`finally`** from the vault root (see [[.cursor/agents/gitforge.md|agents/gitforge.md]]). **`release`** clears the lock when the acquirer process has exited; if a **live foreign** process still holds the lock, exit code **1** means another track is active — do not delete manually unless you know that process is stuck.

## Step 0 (wrappers) and parallel lanes

When **`queue_lane_filter`** is **`sandbox`** or **`godot`**, Step 0 **skips** a wrapper whose frontmatter **`queue_lane`** is set to a **different** track lane (not `shared`, not the active filter). **Omitted** **`queue_lane`** on a wrapper: still processed in every chat that runs Step 0 (operator may set **`queue_lane`** on track-specific wrappers to avoid duplicate applies). See [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0**.

## Related paths (per-track bundle)

When parallel routing applies, **PQ** and siblings live under `.technical/parallel/<track>/`:

- `prompt-queue.jsonl`
- `queue-continuation.jsonl`
- `eat_queue_run_plan.json`
- `prompt-queue-audit.jsonl`
- `tmp-prompt.json`
- `eat-queue-decisions.jsonl`
- `control-plane-nightly.jsonl` (when **A.5h** runs and nightly ledger is enabled — colocated with **PQ** for parallel tracks)

**Task hand-off comms** for the lane: `{technical_bundle_root}/task-handoff-comms.jsonl` (see dispatcher.mdc).

## Engine GitHub branches and execution track (2026-04)

- **Branches `sandbox-genesis-mythos-master` / `godot-genesis-mythos-master`** on the export remote are the **published** engine lines for the same vault projects wired in **`parallel_execution.tracks[]`** (`lane_project_id`). They are **not** “lane names” in git — they are **branch + project** identifiers. After **execution-track** cleanup, both GMM projects keep **`roadmap_track: execution`** in **`roadmap-state.md`**; ongoing automation targets **`Roadmap/Execution/`** (see [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]). When you sync **`Roadmap/`** to GitHub (Step 1b), the **Execution** subtree is part of the tree — operators should not strip it.

## Further reading

- [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] — PQ resolution, lanes, append rules
- [[3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Flow|EAT-QUEUE-Flow]] — end-to-end flow
- [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] — parallel dual-track git notes
- [[3-Resources/Second-Brain/Pipelines|Pipelines]] — trigger map

## v2 backlog

Git **worktrees** or separate checkouts for same-project parallel roadmap — explicitly out of scope for v1.
