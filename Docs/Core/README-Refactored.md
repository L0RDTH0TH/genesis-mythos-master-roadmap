---
title: Second Brain — Refactored Documentation Index
created: 2026-03-12
tags: [pkm, second-brain, refactored, migration]
para-type: Resource
status: active
---

**TL;DR** — This note is the entry point for the **refactored** Second Brain doc set (2026-03-12). All refactored files live in the same paths under `3-Resources/Second-Brain/` (in-place updates). Use [[3-Resources/Second-Brain/README|README]] as the **control center** (Quick-command, collapsible doc links, Dataview placeholders). Full audit: [[3-Resources/Second-Brain/System-Audit-Report-2026-03-12|System-Audit-Report-2026-03-12]].

---

## What changed (migration 2026-03-12)

- **Goal**: Human-first, glanceable format; core patterns to reduce walls of text.
- **Applied everywhere (refactored docs)**:
  - **Bold TL;DR** (1–3 sentences) at the top of every refactored file.
  - **Quick Reference Table** with skeleton where applicable: Trigger Phrase | Pipeline | Rule(s) | Confidence Gate | Safety Step First.
  - **Mermaid first** under each major section (diagram then prose).
  - **Safety Invariants** in `> [!warning]` or `> [!danger]` callouts.
  - **Collapsible callouts** (`> [!abstract]-`, `> [!note]-`) for long blocks.
  - **Canonical section order**: TL;DR → Quick Reference Table → Mermaid → Safety Invariants → Detailed Breakdown → Examples/Triggers → Troubleshooting → Cross-references.
- **README as dashboard**: Quick-command section (copy-paste triggers), collapsible callouts linking to each major doc, Dataview query placeholders for recent logs/errors.

---

## Refactored files (same paths)

| Document | Location |
|----------|----------|
| Rules | [[3-Resources/Second-Brain/Rules|Rules.md]] |
| Pipelines | [[3-Resources/Second-Brain/Pipelines|Pipelines.md]] |
| Cursor-Skill-Pipelines-Reference | [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference|Cursor-Skill-Pipelines-Reference.md]] |
| Vault-Layout | [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout.md]] |
| Parameters | [[3-Resources/Second-Brain/Parameters|Parameters.md]] |
| Logs | [[3-Resources/Second-Brain/Logs|Logs.md]] |
| Queue-Sources | [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources.md]] |
| Skills | [[3-Resources/Second-Brain/Skills|Skills.md]] |
| Backbone | [[3-Resources/Second-Brain/Backbone|Backbone.md]] |
| README (dashboard) | [[3-Resources/Second-Brain/README|README.md]] |
| System Audit Report | [[3-Resources/Second-Brain/System-Audit-Report-2026-03-12|System-Audit-Report-2026-03-12.md]] |

Canonical behavior still lives in `.cursor/rules/` and `.cursor/skills/`; these docs are the readable surface and map.

---

## Quick-command (same as README)

| Trigger | What runs |
|---------|-----------|
| **INGEST MODE** | full-autonomous-ingest on Ingest/ |
| **EAT-QUEUE** | Step 0 wrappers first, then prompt-queue.jsonl by mode |
| **DISTILL MODE** | autonomous-distill |
| **EXPRESS MODE** | autonomous-express |
| **ARCHIVE MODE** | autonomous-archive |
| **ORGANIZE MODE** | autonomous-organize |
| **ROADMAP MODE** | Setup only |
| **Resume roadmap** / **RESUME-ROADMAP** | Single continue (deepen default) |
| **We are making a prompt** | Question-led Prompt-Crafter |

---

## Cross-references

- **Audit details**: [[3-Resources/Second-Brain/System-Audit-Report-2026-03-12|System-Audit-Report-2026-03-12]]
- **Control center**: [[3-Resources/Second-Brain/README|README]]
- **Plan (no edits)**: `.cursor/plans/second-brain_audit_and_migration_8ded6860.plan.md`
