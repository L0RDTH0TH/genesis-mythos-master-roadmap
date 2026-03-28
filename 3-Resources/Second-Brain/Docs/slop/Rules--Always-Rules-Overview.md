# Always Rules Overview

**Version: 2026-03 – post-subagent migration**

One-page index of all always-applied rules in `.cursor/rules/always/` with one-line purpose and pointers to the real rule files. Use this to see how triggers, safety, and backbone sync fit together without reading every rule.

---

## Purpose

Docs/Rules/ covers **Dispatcher**, **Core-Guardrails**, and **Watcher-Result-Contract** in detail. This overview lists the **remaining always rules** so readers know what else applies every run and where to look for full behavior.

---

## Always rules (one-line purpose)

| Rule file | Purpose |
|-----------|---------|
| **00-always-core** | Persona (Thoth-AI), vault = Markdown-first Obsidian + Cursor; all new files in Ingest/; frontmatter on every new .md; first job = check Ingest/. |
| **core-guardrails** | Persona & PARA, confidence bands & refinement loops, MCP & filesystem safety (backup/snapshot before destructive), exclusions, Error Handling Protocol. See [Core-Guardrails](Core-Guardrails.md). |
| **dispatcher** | Route EAT-QUEUE / Process queue / EAT-CACHE / PROCESS TASK QUEUE to Queue rule; all other triggers (INGEST MODE, DISTILL MODE, etc.) per system-funnels. See [Dispatcher-Rule](Dispatcher-Rule.md). |
| **system-funnels** | Primary entry = question-led Prompt-Crafter ("We are making a prompt"); secondary = direct mode phrases (INGEST MODE, EAT-QUEUE, ROADMAP MODE, RESUME-ROADMAP, etc.) → context rules; routing table for manual triggers and roadmap aliases. |
| **confidence-loops** | Shared confidence bands (high ≥85%, mid 68–84%, low <68%); single non-destructive refinement loop in mid-band; decay rule; loop logging fields; Decision Wrappers for low/mid; proposal auto-escalation (approved: true + EAT-QUEUE). |
| **guidance-aware** | Load user_guidance (note frontmatter) or queue prompt when approved/source_file/#guidance-aware; pass as soft hint to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic; never override safety; guidance_conf_boost optional. |
| **watcher-result-append** | On run finish (success or failure), append one line to `3-Resources/Watcher-Result.md`: requestId, status, message, trace, completed (ISO8601). Queue/task-queue runs: one line per processed entry (id = requestId). See [Watcher-Result-Contract](Watcher-Result-Contract.md). |
| **mcp-obsidian-integration** | Folder blacklist (no 00 Inbox, 10 Zettelkasten, 99 Attachments/Templates); Ingest processing chain; ensure_backup vs create_backup; snapshot config; ensure_structure before move; dry_run before move commit; post-move frontmatter sync; MCP fallback table; roadmap state invariants; Error Handling Protocol; restore-queue mode. |
| **second-brain-standards** | PARA strictly; searchable title, frontmatter, #tags; atomic notes; attachment and note link syntax; kebab-slug-YYYY-MM-DD-HHMM filenames. |
| **backbone-docs-sync** | When backbone component (rules, skills, pipeline defs, Config, Second-Brain notes) changes → update corresponding doc in 3-Resources/Second-Brain/ and sync to .cursor/sync/. |
| **always-ingest-bootstrap** | When user says INGEST MODE / Process Ingest / run ingests → route to IngestSubagent (agents/ingest.mdc); no ingest logic in this rule. |

---

## Context rules (entry points only)

| Rule / area | Purpose |
|-------------|---------|
| **plan-mode-prompt-crafter** (context) | Question-led Q&A to build queue payload; questions from User-Questions-and-Options-Reference §1; append to queue only after user confirms. See [User-Flows/Prompt-Crafter-Flow](../User-Flows/Prompt-Crafter-Flow.md). |
| **auto-eat-queue** (context) | Step 0 wrapper semantics, dispatch table, RESUME-ROADMAP normalization; invoked by Queue rule. |
| **auto-roadmap** (context) | Roadmap flow; execution delegated to Roadmap subagent or legacy-agents/roadmap. |

Full text of always and context rules lives in `.cursor/rules/always/*.mdc` and `.cursor/rules/context/*.mdc`. This overview does not replace them; it points to where triggers, safety, and Watcher are defined.

---

## References

- [Dispatcher-Rule](Dispatcher-Rule.md) — routing to Queue rule and other triggers
- [Core-Guardrails](Core-Guardrails.md) — safety, confidence, MCP, exclusions, errors
- [Watcher-Result-Contract](Watcher-Result-Contract.md) — line format and when to append
- [Pipelines/Queue-Pipeline](../Pipelines/Queue-Pipeline.md) — what the Queue rule does
- `3-Resources/Second-Brain/Rules.md` — full Rules map in backbone
