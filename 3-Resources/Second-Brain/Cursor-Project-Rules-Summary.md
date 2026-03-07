---
title: Cursor Project Rules Summary
created: 2026-02-23
tags: [pkm, cursor, rules, second-brain]
para-type: Resource
status: active
links: [[Resources Hub]]
---

# Cursor Project Rules Summary

Summary of the Cursor workspace rules used in this Second Brain vault. Source: `.cursor/rules/` (`.mdc` in `always/` and `context/`; synced to `.cursor/sync/rules/`). **Note filenames**: `kebab-slug-YYYY-MM-DD-HHMM.md` per [[3-Resources/Second-Brain/Naming-Conventions|Naming-Conventions]] (slug first, date and time at end).

---

## Always-applied rules (8)

| Rule file | Purpose |
|-----------|---------|
| `00-always-core.mdc` | Persona (Thoth-AI); all new files in Ingest/; frontmatter on every new .md; backup-first; no shell mv/delete |
| `second-brain-standards.mdc` | PARA; atomic notes; attachments `![[5-Attachments/...]]`; searchable title, frontmatter, #tags |
| `mcp-obsidian-integration.mdc` | Backups, snapshots, dry_run before move; Error Handling Protocol; ensure_structure; fallback table |
| `confidence-loops.mdc` | Mid-band **68–84%**, high ≥85%, low <68%; single refinement loop; loop_* in logs |
| `guidance-aware.mdc` | user_guidance / queue prompt as soft hints; guidance_conf_boost; never override safety |
| `always-ingest-bootstrap.mdc` | INGEST MODE / Process Ingest → full-autonomous-ingest (Phase 1 propose + wrapper; Phase 2 apply via EAT-QUEUE) |
| `watcher-result-append.mdc` | Watcher-Result.md: requestId, status, message, trace, completed per request |
| `backbone-docs-sync.mdc` | When rules/skills change → update Second-Brain docs and `.cursor/sync/` |

---

## Context rules (19)

| Rule file | Trigger / glob | Pipeline or flow |
|-----------|----------------|-------------------|
| `para-zettel-autopilot.mdc` | Ingest/*.md | full-autonomous-ingest |
| `ingest-processing.mdc` | Non-MD in Ingest, embedded normalization | Pre-step before ingest on Ingest/*.md |
| `auto-eat-queue.mdc` | EAT-QUEUE, Process queue, EAT-CACHE | Queue processor → dispatch by mode |
| `auto-queue-processor.mdc` | PROCESS TASK QUEUE | Task-Queue.md modes |
| `auto-distill.mdc` | DISTILL MODE, distill note | autonomous-distill |
| `auto-archive.mdc` | ARCHIVE MODE, archive | autonomous-archive |
| `auto-express.mdc` | EXPRESS MODE, express note | autonomous-express |
| `auto-organize.mdc` | ORGANIZE MODE, re-organize | autonomous-organize |
| `non-markdown-handling.mdc` | Non-.md in Ingest | Companion .md; #needs-manual-move |
| `auto-distill-perspective.mdc` | DISTILL LENS: [angle] | autonomous-distill with distill_lens |
| `auto-express-view.mdc` | EXPRESS VIEW: [angle] | autonomous-express with express_view |
| `auto-highlight-perspective.mdc` | HIGHLIGHT PERSPECTIVE: [lens] | Highlight pass with perspective |
| `mobile-seed-detect.mdc` | SEEDED-ENHANCE | highlight-seed-enhance |
| `snapshot-sweep.mdc` | Snapshot cleanup / retention | Per-change and batch retention |
| `auto-restore.mdc` | Restore from snapshot/backup | User-triggered restore |
| `auto-resurface.mdc` | Resurface, show resurface candidates | Resurface flow |
| `auto-async-cascade.mdc` | EAT-QUEUE when queue >3 entries | Propose batch run |
| `auto-garden-review.mdc` | GARDEN REVIEW, run garden review, orphans and distill candidates, garden health, vault orphans, distill candidates sweep; queue **GARDEN-REVIEW** | Garden review flow: obsidian_garden_review → report → feed to distill/organize batches |
| `auto-curate-cluster.mdc` | CURATE CLUSTER #tag, suggest gaps and merges, cluster curate #tag, theme gaps #tag, merge suggestions; queue **CURATE-CLUSTER** | Curate cluster flow: obsidian_curate_cluster → analyze report; optional split/MOC/merge |

---

## Quick reference

| Trigger / topic | Key rule(s) | Confidence | Destructive actions |
|-----------------|-------------|------------|----------------------|
| Process Ingest | always-ingest-bootstrap, para-zettel-autopilot | ≥85% act | Propose only Phase 1; apply Phase 2 via approved wrapper; backup first |
| Classify PARA | para-zettel-autopilot, confidence-loops | Mid 68–84%, High ≥85% | Propose only below 85%; snapshot + move/rename at ≥85% |
| Distill / Archive / Organize / Express | auto-distill, auto-archive, auto-organize, auto-express | 68–84% loop; ≥85% proceed | Per-change snapshot then dry_run → commit |
| MCP vault ops | mcp-obsidian-integration | — | create_backup first; ensure_structure before move |
| Uncertain / low conf | Decision Wrappers (Ingest/Decisions/) | <68% or mid-band failure | No move/edit; wrapper for user choice |

---

*Generated from `.cursor/rules` and [[3-Resources/Second-Brain/Rules|Rules]]. Filename format: kebab-slug-YYYY-MM-DD-HHMM.md. When rules change, update this summary and Rules.md.*
