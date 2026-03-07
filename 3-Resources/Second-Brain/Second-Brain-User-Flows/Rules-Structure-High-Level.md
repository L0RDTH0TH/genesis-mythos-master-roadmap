---
title: Rules Structure — High-Level
created: 2026-03-05
tags: [pkm, second-brain, rules, structure, level-1]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Rules]]"]
---

# Rules Structure — High-Level

This document shows the big picture of how rules are organized: always-applied vs context-triggered, how the user’s trigger (phrase, Watcher, queue) selects which rules run, and the main safety gates (backup, snapshot, dry_run, confidence bands). It answers “when does which rule apply?” without listing every rule or trigger.

---

## Two rule layers

- **Always-applied** — Run on every agent turn. They define persona, Ingest-first behavior, MCP safety (backups, snapshots, dry_run before move), confidence bands, guidance-aware contract, when to list Ingest and run the ingest pipeline, and when to append to Watcher-Result. They also require backbone docs and `.cursor/sync` to stay updated when rules or skills change.
- **Context-triggered** — Run only when the instruction or open file matches a trigger (phrase, glob, or queue). They start pipelines: full-autonomous-ingest, queue processor, autonomous-distill, -archive, -express, -organize, plus ingest pre-steps (non-MD handling), snapshot sweep, restore, resurface, and lens/view rules (highlight perspective, distill lens, express view, mobile seed, async cascade).

---

## How the user’s trigger selects rules

1. **User says a phrase in Cursor**  
   Examples: INGEST MODE, Process Ingest, run ingests → always-ingest-bootstrap and para-zettel-autopilot (full-autonomous-ingest). DISTILL MODE, ARCHIVE MODE, EXPRESS MODE, ORGANIZE MODE → the matching auto-* context rule (autonomous-distill, -archive, -express, -organize). EAT-QUEUE, Process queue, eat cache / EAT-CACHE → auto-eat-queue (queue processor). PROCESS TASK QUEUE → auto-queue-processor.

2. **Watcher plugin**  
   Watcher writes a signal; the run is triggered by that request. The same phrases (e.g. INGEST MODE, DISTILL MODE) are used as modes; the queue processor or the bootstrap rule still applies. Watcher-Result is appended per always-applied watcher-result-append.

3. **Commander or mobile toolbar**  
   A macro or toolbar adds an entry to `.technical/prompt-queue.jsonl` or Task-Queue.md. The user (or a follow-up trigger) runs EAT-QUEUE or Process queue; auto-eat-queue reads the queue and dispatches by mode to the right pipeline.

4. **Open file / glob**  
   When the context matches `Ingest/*.md`, para-zettel-autopilot can run full-autonomous-ingest for that scope (in addition to phrase-based INGEST MODE).

---

## Main safety gates (all pipelines)

- **Backup** — Before destructive or move steps, a recent backup must exist (ensure_backup / create_backup). No destructive action until backup is in place.
- **Snapshot** — Before move, rename, split, structural distill, or large appends, a per-change snapshot is created when confidence ≥85%. Batch snapshots when batch size exceeds threshold.
- **Dry run before move** — Every `obsidian_move_note` at ≥85% is called first with `dry_run: true`; effects are reviewed; then `dry_run: false` to commit. Path must exist (ensure_structure for parent).
- **Confidence bands** — High (≥85%): snapshot then destructive step. Mid (68–84%): at most one non-destructive refinement loop; commit only if post_loop_conf ≥85%. Low (&lt;68%): proposal only; no destructive action; user adds approved and/or user_guidance and re-runs.

---

## Ingest: Phase 1 vs Phase 2 (rule split)

- **Phase 1** — Governed by para-zettel-autopilot and ingest context rules. Classify, enrich, organize proposal, split, distill, hub append, and **create/refresh Decision Wrapper**. No move/rename of the original note; the wrapper lists options A–G (and optionally 0). User checks one option and sets `approved: true`, or sets `re-wrap: true` / option 0.
- **Phase 2 (apply-mode)** — Governed by auto-eat-queue Step 0 and feedback-incorporate. When the user runs EAT-QUEUE, Step 0 runs first: for wrappers with `approved: true`, `re-wrap: true`, or `re-try: true`, it resolves path, re-wrap intent, or re-try intent. Then: apply-mode ingest (move/rename to approved path), phase-direction apply (provenance + comment guidance on roadmap; wrapper → Roadmap-Decisions/), re-wrap branch (archive wrapper, create new from Thoughts), or re-try branch (re-queue EXPAND-ROAD/TASK-TO-PLAN-PROMPT with guidance; cap re_try_max_loops). Moves and renames happen only after backup/snapshot and dry_run.

---

## Where rules live

- Always: `.cursor/rules/always/*.mdc`
- Context: `.cursor/rules/context/*.mdc`
- Synced copies: `.cursor/sync/rules/always/*.md`, `.cursor/sync/rules/context/*.md`
- Map and usage: [[Rules]], [[Cursor-Skill-Pipelines-Reference]], [[Pipelines]]
