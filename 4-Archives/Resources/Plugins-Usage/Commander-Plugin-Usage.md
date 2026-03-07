---
title: Commander Plugin — Usage & Setup
created: 2026-03-01
tags: [commander, second-brain, setup, toolbar]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Plugins]]"]
---

# Commander Plugin — Usage & Setup

Commander lets you place any Obsidian command (core or community) in the ribbon, status bar, context menus, editor title bar, and mobile toolbar. It supports device-specific visibility, macros (chained commands with delays or loops), and custom icons, labels, and colors. Use it to declutter the UI and put pipeline and roadmap actions where you need them.

## What Commander does

Commander does not add new commands—it **surfaces** existing ones. You choose which commands appear in the left ribbon, status bar, right-click menus, editor header, and (on mobile) the toolbar. You can restrict visibility by device (desktop vs mobile), rename commands, change icons, and create **macros** that run multiple commands in sequence (with optional delays). On mobile, Commander offers multi-row toolbar layouts and styling so you can prioritize one-tap actions.

## How it fits this vault

Commander does **not** replace Watcher. **Watcher** provides the commands (Ingest, Distill, Express, Archive, Organize, Prompt Modal, Task Complete, TASK-ROADMAP, Add Roadmap Item, etc.) and the queue behavior; **Commander** is where you **put** those commands in the UI. Enable both: Watcher for behavior, Commander for placement and grouping.

## Suggested setup

### One-tap Process Queue

Add a toolbar or ribbon item that runs the command that triggers queue processing. For example: **Watcher: Prompt Modal** (then pick a mode and Send), or a Shell-command / external script that opens Cursor with "Process queue" if you use that flow. See [[3-Resources/Mobile-Toolbar-Task-Commands#One-tap Process Queue|Mobile-Toolbar-Task-Commands § One-tap Process Queue]].

### Roadmap Tools

Group TASK-ROADMAP, Task Complete, Add Roadmap Item, Expand Road, Reorder, Duplicate, Merge, Export, and Progress under one icon or sub-menu if Commander supports it. **Prioritize Task Complete and Process Queue (EAT-QUEUE)** on the main bar; put the rest in the sub-menu to reduce clutter. See [[3-Resources/Mobile-Toolbar-Task-Commands|Mobile-Toolbar-Task-Commands]].

### Macros (depth / queue)

- **Seed and Layer**: Detect user `<mark>` (or prompt for note) + queue highlight-seed-enhance + optional preview gen. Document in mobile-seed-detect and highlight-seed-enhance skill.
- **Express View Chain**: Prompt for view (e.g. stakeholder vs dev) + trigger EXPRESS MODE + append to hub. Make **contextual** (visible only on express-eligible notes).
- **Async Approve**: Scan Mobile-Pending-Actions + set approved: true on selected note(s) + re-queue. **Device-specific**: mobile-only for quick reflections. See confidence-loops (async mid-band).
- **MOC Refresh**: Run health_check + aggregate or link latest log summaries into [Vault-Change-Monitor](3-Resources/Vault-Change-Monitor.md). Optional; document in Vault-Change-Monitor.
- **Safety Wrapper** (pre-check macro): Chain ensure_backup + health_check before destructive or pipeline macros. Run this first when using macros that trigger move/distill/archive. See Safety best practices below.

### Prompt-crafter macros (laptop-only)

**"Craft Prompt" / "Prompt Craft"** — Assemble MCP params from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] prompt_defaults and [[3-Resources/Second-Brain/Templates#Prompt-Components (laptop)|Templates/Prompt-Components]] for consistent ingest/organize. Laptop/desktop only; no mobile toolbar required.

- **Param selection UI**: Macro prompts for inputs — e.g. "Pipeline: ingest | organize? Profile: default | project-priority?" Then assemble and paste or append. Set **commander_macro** for logging (e.g. `craft_prompt_ingest`) per [[3-Resources/Second-Brain/Rules|Rules]] § Commander and Queue-Sources commander_source/commander_macro.
- **Preview Assembly** (sub-option): Paste crafted prompt to a temp note before queue append; log via **commander_macro: "craft_prompt_preview"**. Debug-friendly for param tweaks.
- **Craft and Queue**: Appends to `.technical/prompt-queue.jsonl` with **validated** params (mode, params, id, source_file, prompt). **If invalid, aborts and logs to Prompt-Log.md.** EAT-QUEUE then passes params to MCP; guidance-aware when note has user_guidance or queue has prompt.
- **Validation (optional)**: Before paste/append, lightweight check (e.g. propose_para_paths with params) and preview callout: `> [!preview] Crafted params: ... Expected paths: A–G sample.` Abort or warn if invalid; document as optional for minimal first implementation.
- **Sub-macros**: "Craft Ingest Default" vs "Craft Organize Custom" for batch or one-shot; document chainability.

**How to configure**: In Commander → Macros, chain commands (e.g. open template, fill from config, copy to clipboard or append to queue). Use a template from `Templates/Prompt-Components/` or a static snippet; if a script or Templater builds the string, document its path and usage in this note or in Queue-Sources. No JS implementation required in this doc.

### Optional macros (generic)

For desktop workflows you can chain commands, e.g. "Open Watcher modal" → delay → "EAT-CACHE (copy queue to clipboard)" so you can paste into Cursor. Configure in Commander → Macros. **Limitation**: Commander has no built-in delays/loops; consider Commando plugin for timed chains (optional; see Plugins.md).

### Device-specific

Show "Process Queue" (or the command that opens Cursor / runs queue processing) on the **mobile** toolbar. Optionally show or hide Roadmap Tools only on mobile or only on desktop. **Mobile-only**: e.g. "Async Approve", "Queue Highlight Perspective" for ingestion breaks; hide complex batch macros on mobile to reduce clutter.

## Safety best practices

- **Manual triggers only**: Macros require user tap; no auto-execution. All Commander-triggered queue entries should set **commander_source: true** and **commander_macro: name** for MOC tracking (see Queue-Sources Commander-Sourced Modes).
- **Safety Wrapper**: For destructive or pipeline macros, chain a pre-check macro (e.g. ensure_backup + health_check) so backup exists before running the main macro.
- **Dry_run**: Any macro that triggers move_note should respect dry_run then commit (handled by pipeline; no change to Commander config).
- **Errors**: When a run fails, Errors.md entry can include **commander_macro** for traceability. See Errors.md template.

## Contextual visibility

Some setups support showing commands only in certain contexts (e.g. show Roadmap Tools only when the note has `para-type: Roadmap` or path under `1-Projects/…/Roadmap/`). This is plugin/settings-dependent. See [[3-Resources/Second-Brain/Vault-Layout#Toolbar (mobile)|Vault-Layout § Toolbar]] for the contract; configure in Commander or Note Toolbar plugin settings.

## Setup steps (summary)

1. Install Commander via Community Plugins.
2. Settings → Commander: add commands (e.g. link to Watcher commands for queue processing, Prompt Modal, Task Complete, Add Roadmap Item).
3. Assign to mobile toolbar, ribbon, status bar, or title bar as desired.
4. (Optional) Create macros: Seed and Layer, Express View Chain, Async Approve, MOC Refresh, Safety Wrapper. See Macros above.
5. Set device-specific visibility (e.g. mobile-only for Async Approve, Queue Highlight Perspective).
6. Log Commander-triggered runs with commander_source: true and commander_macro in queue payload and pipeline logs; see Queue-Sources and Vault-Change-Monitor Commander Dashboard.

## See also

- [[3-Resources/Watcher-Plugin-Usage]] — Watcher commands and queue flow
- [[3-Resources/Mobile-Toolbar-Task-Commands]] — Toolbar entries and EAT-QUEUE
- [[3-Resources/Second-Brain/Plugins]] — Plugin list and roles; Commando optional for timed chains
- [[3-Resources/Vault-Change-Monitor]] — Commander Dashboard (macros used, commander_source)
- [[3-Resources/Second-Brain/Queue-Sources#Commander-Sourced Modes]] — commander_source, commander_macro format
