---
title: Ingest–Roadmap Pullout Report
created: 2026-03-05
tags: [ingest, roadmap, pullout, audit]
status: complete
links: ["[[3-Resources/Second-Brain/Rules]]", "[[3-Resources/Second-Brain/Pipelines]]", "[[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference]]"]
---

# Ingest–Roadmap Pullout Report

## Purpose

Ingest should **capture and place** notes only: classify, enrich, propose path via a single Decision Wrapper type (A–G = PARA paths), and apply-mode = move/rename to the user-approved path. Roadmap **creation** (project tree, master/phase notes, MOC) is a separate responsibility and was removed from ingest apply-mode so ingest does not dilute its focus.

## Summary

- **para-zettel-autopilot.mdc**: Roadmap-seed detection subsection and roadmap-specific Decision Wrapper branch removed; single wrapper path (Ingest/Decisions/Ingest-Decisions/ only); skills line no longer references roadmap seeds or Option A.
- **auto-eat-queue.mdc**: Step 0 path-apply is apply-mode ingest only (move/rename to approved_path); Roadmap wrappers (Option A) block and re-wrap Roadmap stub removed; all references to Roadmap-Decisions removed.
- **roadmap-generate-from-outline (SKILL.md)**: Trigger updated from ingest apply-mode (Option A) to ROADMAP MODE – generate from outline (or dedicated queue mode); skill body unchanged.
- **Sync**: .cursor/sync/rules/context/para-zettel-autopilot.md and auto-eat-queue.md updated to match.
- **Docs**: Skills.md (roadmap-generate-from-outline row), Cursor-Skill-Pipelines-Reference.md (apply-mode note + Decision Wrapper path-apply), Rules.md, Queue-Sources.md, Vault-Layout.md, Pipelines.md, Rules-Structure-Detailed.md updated to remove roadmap Option A and Roadmap-Decisions; roadmap tree creation documented as ROADMAP MODE / queue.

## Removals (by file)

### para-zettel-autopilot.mdc

| What was removed | What it did | Why it was there |
|------------------|-------------|------------------|
| **Entire "Roadmap-seed detection" subsection** | After classify, before wrapper: heuristic (title/headings + ≥3 phase-like sections) set `is_roadmap: true` and `suggested_project_name` on the note. | Treated roadmap-like notes as a special case so the wrapper could offer "Option A = build roadmap tree." |
| **"Roadmap-specific branch (is_roadmap: true)"** in Decision Wrapper creation | When `is_roadmap: true`: Option A = synthetic "New project + full roadmap tree"; B–G from `propose_para_paths` with 6 candidates; set `wrapper_type: roadmap`, `suggested_project_name`; body filled with roadmap-aware A–G. | So apply-mode could call `roadmap-generate-from-outline` when user chose A. |
| **Dual wrapper paths** | Replaced two paths (Ingest-Decisions/ vs Roadmap-Decisions) with one: all wrappers to `Ingest/Decisions/Ingest-Decisions/` only; removed `obsidian_ensure_structure` for Roadmap-Decisions. | Roadmap-specific wrappers are no longer a separate type. |
| **Skills line** | The phrase "For notes detected as roadmap seeds … later apply-mode runs call roadmap-generate-from-outline when the user chooses Option A." | Remove so ingest no longer references roadmap generation. |

**After edits:** Ingest uses one wrapper type: A–G from `obsidian_propose_para_paths` with `max_candidates = "7"` for every note; no `is_roadmap`, no `wrapper_type: roadmap`, no Roadmap-Decisions path.

### auto-eat-queue.mdc

| What was removed | What it did | Why it was there |
|------------------|-------------|------------------|
| **Step 0 – "Roadmap wrappers (wrapper_type: roadmap, Option A)" block** | When `wrapper_type: roadmap` or `is_roadmap: true` and Option A chosen: call `roadmap-generate-from-outline` (create project, Roadmap/, master, phases, MOC, move seed to Source); then mark wrapper processed and archive. | To build a full roadmap tree from an ingest seed when the user picked Option A. |
| **Step 0 – Re-wrap "Roadmap wrappers (stub)" bullet** | Re-wrap for roadmap: archive to Re-Wrap/Roadmap-Decisions, create new wrapper under Roadmap-Decisions. | Mirrored ingest-decision re-wrap for the (now-removed) roadmap wrapper type. |
| **References to Roadmap-Decisions** | All mentions of `Roadmap-Decisions` in Step 0 enumeration, processed-wrapper archive, and re-wrap. | Only one wrapper type remains (Ingest-Decisions). |

**After edits:** Step 0 path-apply is only: run apply-mode INGEST (move/rename to approved_path) for every approved wrapper. No branch on `wrapper_type` or `is_roadmap`; no call to `roadmap-generate-from-outline`. Re-wrap is a single flow (ingest-decision style only); archive to Re-Wrap/Ingest-Decisions and create new wrapper under Ingest/Decisions/Ingest-Decisions/.

### roadmap-generate-from-outline (SKILL.md)

Invocation from ingest apply-mode removed. **When to use** and frontmatter description now state: trigger is **ROADMAP MODE – generate from outline** (or a dedicated queue mode) with a note path; skill body unchanged.

---

## Doc and sync updates (brief)

- **Skills.md**: roadmap-generate-from-outline row — trigger "queue / ROADMAP MODE"; description no longer references ingest Option A.
- **Cursor-Skill-Pipelines-Reference.md**: Added Decision Wrapper path-apply bullet (apply-mode only; roadmap tree via ROADMAP MODE).
- **Rules.md**: Ingest-Decisions only (removed Roadmap-Decisions from example).
- **Queue-Sources.md**: Step 0 description — single subfolder; apply-mode move/rename only; note that roadmap creation uses ROADMAP MODE.
- **Vault-Layout.md**: Ingest-Decisions and Re-Wrap — only Ingest-Decisions subfolder; removed Roadmap-Decisions from examples.
- **Pipelines.md**: Phase 2 — Ingest-Decisions only; added note that roadmap tree is ROADMAP MODE, not ingest.
- **Rules-Structure-Detailed.md**: Re-wrap branch (Ingest-Decisions only); Path-apply = apply-mode only; roadmap via ROADMAP MODE.
- **Sync copies**: para-zettel-autopilot.md and auto-eat-queue.md updated to match .mdc edits.

---

## Follow-up

**Roadmap creation** is now a separate concern from ingest. To create a full project roadmap tree from an outline note, use **ROADMAP MODE – generate from outline** (or a dedicated queue mode) with the path to the outline note; the `roadmap-generate-from-outline` skill will create project folder, Roadmap/, master and phase notes, and MOC. Ingest only captures and places notes via a single Decision Wrapper type (A–G = PARA paths) and apply-mode move/rename to the user-approved path.
