# Roadmap Skills Overview

**Version: 2026-03 – post-subagent migration**

Overview of skills used by the Roadmap subagent: roadmap-generate-from-outline, roadmap-deepen, roadmap-advance-phase, roadmap-resume, roadmap-audit, roadmap-revert, roadmap-phase-output-sync, hand-off-audit, expand-road-assist, research-agent-run (pre-deepen).

---

## Purpose

Single reference for which skills the Roadmap pipeline calls and when. Skill definitions live in `.cursor/skills/<skill-name>/SKILL.md`.

---

## Setup (ROADMAP MODE)

| Skill | When used |
|-------|-----------|
| **roadmap-generate-from-outline** | When roadmap-state.md does not exist; creates workflow_state.md if missing; builds initial roadmap tree from master goal / outline. |
| **normalize-master-goal** | When the seed note is a PMG; run before roadmap-generate-from-outline so the note follows the Master-Goal template (One-line, Vision, Phases, Technical Integration, TL;DR, Related). |

---

## Resume (RESUME-ROADMAP)

| Skill | When used |
|-------|-----------|
| **roadmap-deepen** | action deepen (default): one deepen step; update workflow_state; may append RESUME-ROADMAP to queue when queue_next !== false. |
| **roadmap-advance-phase** | action advance-phase: snapshot state; depth-aware gate; update roadmap-state and workflow_state. |
| **roadmap-resume** | Optional before deepen: build handoff context with distilled-core first. |
| **roadmap-audit** | action recal: drift, wrapper, ignored_wrappers → auto-revert; log exact drift score. |
| **roadmap-revert** | action revert-phase: params.phase required; archive phase to Roadmap/Branches/; reset state; re-queue EXPAND-ROAD with guidance. |
| **roadmap-phase-output-sync** | action sync-outputs: align phase-X-output.md with canonical phase roadmap. |
| **hand-off-audit** | action handoff-audit: evaluate phase for junior-dev delegatability (traceability, pseudo-code, interfaces, acceptance criteria). |
| **expand-road-assist** | action expand: sectionOrTaskLocator, userText; parse user text into sub-phases/tasks; append under target section/task. |
| **research-agent-run** | Pre-deepen when enable_research: vault-first → query gen → fetch → synthesize → write to Ingest/Agent-Research/; queue INGEST (and DISTILL if research_distill); inject into deepen. |

---

## Other

| Skill | When used |
|-------|-----------|
| **roadmap-validate** | Optional after recal: cross-check phase content against project master-goal. |
| **roadmap-checklist** | On demand: produce hierarchical checklist from roadmap note by following [[links]] recursively (e.g. ROADMAP MODE – generate checklist). |
