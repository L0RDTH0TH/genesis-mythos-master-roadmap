---
title: Research silent-failure audit
created: 2026-03-11
tags: [pkm, second-brain, research, roadmap, observability, audit]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Logs]]", "[[3-Resources/Second-Brain/Queue-Sources]]", "[[.cursor/rules/context/auto-roadmap]]"]
---

# Research silent-failure audit

Short reference for who invokes research, where **linked_phase** comes from, and how to confirm research ran or failed.

## Who invokes research

| Invoker | Trigger | How |
|--------|---------|-----|
| **auto-roadmap** (pre-deepen) | RESUME-ROADMAP with `action: deepen` and research enabled | Inline: resolve linked_phase from workflow_state, then call research-agent-run before roadmap-deepen. |
| **auto-eat-queue** | Queue mode **RESEARCH-AGENT** | Resolves project_id + linked_phase from `source_file` or payload (params.phase / params.linked_phase); runs research-agent-run; 0 notes → failure + Watcher-Result + queue_failed. |
| **roadmap-deepen** (step 4.5) | Gap-fill only | When high-severity gaps and research enabled and depth ≥ 2: calls research-agent-run in **gap-fill** mode with params.gaps; must pass project_id and linked_phase. |

## Where linked_phase comes from

- **Pre-deepen (RESUME-ROADMAP):** From **workflow_state** in auto-roadmap: `current_phase` + `current_subphase_index` → stable id e.g. `Phase-1-1`, `Phase-1-1-2`. If missing or invalid, research is skipped and #research-skipped is logged.
- **RESEARCH-AGENT:** From `source_file` (phase note under `1-Projects/<id>/Roadmap/`) or payload `params.phase` / `params.linked_phase`.
- **Gap-fill (roadmap-deepen):** From the current deepen target (phase note path or stable id for the target being deepened). If either project_id or linked_phase is missing, gap-fill is skipped and #research-skipped is logged.

## Logging and observability

- **Research error entry format:** All research-related Errors.md entries use the structure in [[3-Resources/Second-Brain/Logs#Research error entry format]]. Tags: **#research-failed**, **#research-empty**, **#research-skipped**.
- **Skill (research-agent-run):** MUST append to Errors.md when returning 0 paths (empty/fail). Callers (auto-roadmap, roadmap-deepen) MUST append as backstop when the skill returns empty or throws and did not log.
- **Research-Log:** Optional one line per run at `3-Resources/Research-Log.md` (timestamp, project_id, linked_phase, outcome, note_count). See [[3-Resources/Second-Brain/Logs#Pipeline logs]].
- **Watcher-Result:** For RESUME-ROADMAP deepen, when research was enabled and invoked but produced 0 notes, the success message may include a suffix: "deepen success; research ran, 0 notes (see Errors.md or Research-Log)".

## Post-run check

After RESUME-ROADMAP runs with **enable_research: true**, check **Errors.md** for #research-failed / #research-empty / #research-skipped (and **Research-Log** if in use). If there are no such entries and no new notes in `Ingest/Agent-Research/`, either linked_phase was not resolved (research skipped) or failure was not logged; the hardening (linked_phase resolution + mandatory logging) is intended to prevent silent skips.
