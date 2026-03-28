---
title: Triggers Quick Reference
created: 2026-03-10
tags: [second-brain, triggers, pipelines, queue]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Queue-Alias-Table]]", "[[3-Resources/Second-Brain/Pipelines]]", "[[3-Resources/Second-Brain/Mode-Success-Contracts]]"]
---

# Triggers Quick Reference

Single source of truth for **core voice commands / phrases**, which **mode** they map to, and what each mode **guarantees** on success. Aliases and additional modes are documented in [[3-Resources/Second-Brain/Queue-Alias-Table|Queue-Alias-Table]].

## Core modes (8–10 entries)

| Trigger phrase(s) (examples)                                   | Canonical mode    | Guarantees (success contract, short)                                                                                                                                                           | Common failure modes & recovery                                                                                                                |
| -------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `INGEST MODE`, “Process Ingest”, “run ingests”                 | INGEST_MODE       | For each `Ingest/*.md`, classify + enrich + (optional) split/distill, then **create/refresh a Decision Wrapper with 7 PARA candidates**; apply-mode runs only when wrapper is approved. **Exception:** Notes in `Ingest/Agent-Output/` or `Ingest/Agent-Research/` may move without wrapper when ingest_conf ≥85% and single clear target. | Wrapper missing or not updated → check `Ingest/Decisions/**` and `Ingest-Log`; look for errors in `Errors.md`                                  |
| `ORGANIZE MODE – safe batch autopilot`                        | ORGANIZE MODE     | Re-classify and, when confidence ≥85%, **move and/or rename** notes within PARA; otherwise leave note and emit organize Decision Wrappers for low/mid band outcomes.                         | Note stayed in place with no wrapper → check `Organize-Log` and `Errors.md`; run ORGANIZE MODE on that note again                              |
| `DISTILL MODE – safe batch autopilot`                         | DISTILL MODE      | Backup then apply distill layers, highlight, TL;DR, readability flag when distill_conf ≥85%; mid/low band runs either produce a (possibly shallower) distill or a distill Decision Wrapper.  | No distill change and no wrapper → inspect `Distill-Log` and `Errors.md`; re-run with guidance or via wrapper                                  |
| `EXPRESS MODE – safe batch autopilot`                         | EXPRESS MODE      | Backup + version-snapshot, then add Related, mini-outline, and CTA when express_conf ≥85%; mid/low band runs either commit a shorter outline/CTA or surface wrappers/async previews.         | No outline/CTA and no wrapper/preview → check `Express-Log` + `Errors.md`; re-run EXPRESS MODE or inspect wrappers                             |
| `ARCHIVE MODE – safe batch autopilot`                         | ARCHIVE MODE      | For archive-ready notes (archive_conf ≥85%), backup + snapshot then **move to 4-Archives/** with summary preserved and resurface mark; others get archive wrappers or remain active.         | Candidate not moved and no wrapper → check `Archive-Log` + `Errors.md`; look for snapshot/move failures                                        |
| `ROADMAP MODE`                                                | ROADMAP_MODE      | **Setup-only**: create/verify `roadmap-state.md`, `workflow_state.md`, `decisions-log.md`, `distilled-core.md`; **never** runs RESUME_ROADMAP or deepen; safe to re-run for setup checks.    | No roadmap artifacts and no error/wrapper → inspect `Roadmap-Upgrade-Plan`, `Errors.md`; treat as setup failure, not a continue run            |
| `Resume roadmap`, `RESUME-ROADMAP`                            | RESUME_ROADMAP    | **One action per run** (default `deepen`): each run must end in **advance**, **follow-up queue**, **Decision Wrapper**, or **high-severity error**; silent no-op runs are treated as bugs.  | Content changed but state/queue/wrapper/error did not → inspect `workflow_state.md`, `roadmap-state.md`, `Errors.md`; treat as roadmap bug     |
| `EAT-QUEUE`, “Process queue”, “eat cache / EAT-CACHE”         | EAT-QUEUE         | Step 0 applies approved wrappers; then reads prompt-queue, validates, dedups, orders, and **dispatches each entry**, writing a Watcher-Result line per entry and updating state/wrappers.    | Entry consumed with no Watcher-Result and no visible effect → check `Watcher-Result.md`, `Errors.md`, and logs for queue_failed                |
| `PROCESS TASK QUEUE`                                          | PROCESS TASK QUEUE| Reads `Task-Queue.md` and applies task/roadmap actions (TASK_ROADMAP, TASK_COMPLETE, ADD_ROADMAP_ITEM, EXPAND_ROAD, etc.), changing notes or emitting wrappers/errors per entry.            | Task entry disappears without note change or wrapper → check `Task-Queue.md`, `Errors.md`, and relevant logs                                   |

See [[3-Resources/Second-Brain/Mode-Success-Contracts|Mode-Success-Contracts]] for full success/failure contracts and self-audit requirements for each mode.

## Conversational crafting (V4)

| Trigger phrase(s) | What runs | Notes |
|-------------------|-----------|--------|
| "We are making a prompt", "We are making a CODE prompt", "We are making a ROADMAP prompt" | **Conversational-on-rails Prompt Crafter** (lock-first, profile-aware) | Covers every param in §1 order; resume gate (keep vs discard locks) and profile gate with options A–D when switching profile with locks; mid-session restart (resume \| start fresh); final summary annotates manual overrides. Use when you care about locks and per-run nuance. |
| Commander "Craft Prompt", "Craft Ingest Default", "Craft and Queue" | **Macro fast path** | Builds queue entry directly with pinned params; does **not** use tmp-prompt or locks. One-click presets only. |

