---
title: System Audit Report 2026-03-12
created: 2026-03-12
tags: [audit, second-brain, documentation, glanceability]
para-type: Resource
status: active
---

# System Audit Report — Second Brain Documentation (2026-03-12)

**TL;DR** — Audit of 77+ docs in `3-Resources/Second-Brain/` and linked references: most lack TL;DR and collapsible structure; Queue-Sources and Parameters are dense prose; trigger→pipeline content is duplicated across Rules, Pipelines, Cursor-Skill-Pipelines-Reference, README; no standard section order; callouts and Mermaid exist but are sparse or diagram-after-prose. Priority: refactor Core + Queue/Params with TL;DR, tables, Mermaid-first, collapsible callouts, and README as dashboard.

---

## Summary table

| Doc | Glance | Human vs LLM | Duplication | Format | TL;DR | Tables | Mermaid | Callouts | Cross-links | UX issues | Priority |
|-----|--------|--------------|-------------|--------|-------|--------|---------|----------|-------------|-----------|----------|
| **Core** | | | | | | | | | | | |
| Rules.md | Medium | Good | Yes (triggers) | Mixed | No | Yes (2) | Yes (2, after prose) | No | OK | Long table cells; no fold | High |
| Pipelines.md | Medium | Good | Yes (triggers) | Mixed | No | Yes (3+) | No in body | No | OK | Dense Responsibility column | High |
| Cursor-Skill-Pipelines-Reference.md | Low | Good | Yes (triggers, snapshot) | Mixed | No | Yes | Yes | No | OK | Long; diagram buried | High |
| Vault-Layout.md | Good | Good | Low | Mixed | No | Yes (3) | Yes (2) | No | OK | — | High |
| Parameters.md | Low | Medium | Yes (bands) | Poor | No | Yes (1) | Yes (4) | No | OK | Walls of text; nested bullets | High |
| Logs.md | Good | Good | Low | Mixed | No | Yes (1 main) | Yes (4) | No | OK | — | High |
| Queue-Sources.md | Low | Medium | Low | Poor | No | Few | Yes (3) | No | OK | Dense paragraphs; modes in prose | High |
| Skills.md | Good | Good | Low | Mixed | No | Yes (1 large) | Yes (3) | No | OK | — | High |
| Backbone.md | Medium | Good | Low | Mixed | No | No | Yes (4) | Yes (1 danger) | OK | Long index list | High |
| README.md | Good | Good | Yes (triggers) | Mixed | No | Yes (1) | No | Yes (1 danger) | OK | Not a dashboard; no Dataview | High |
| **Queue/Params** | | | | | | | | | | | |
| Configs.md | Good | Good | Low | Mixed | Yes | Yes | No | No | OK | — | Medium |
| Queue-Alias-Table.md | Medium | Good | Yes | Mixed | No | Partial | No | No | OK | — | Medium |
| MCP-Tools.md | Medium | Good | Low | Mixed | No | Yes | Yes | No | OK | — | Medium |
| Naming-Conventions.md | Medium | Good | Low | Mixed | No | Partial | No | No | OK | — | Medium |
| Templates.md | Medium | Good | Low | Mixed | No | Partial | Yes | No | OK | — | Medium |
| Plugins.md | Medium | Good | Low | Mixed | No | Partial | Yes | No | OK | — | Medium |
| **User-Flows** (25 files) | Mixed | Good | High (High/Mid/Detailed) | Mixed | No | Varies | Yes (many) | Few | OK | Overlap; no single canonical | Medium |
| **Other** (remaining) | Mixed | Good | Low | Mixed | Few | Varies | Varies | Few | Verify | — | Low–Medium |

---

## 1. Glance-ability

- **Strong**: Rules, Pipelines, Vault-Layout, Logs, Skills use tables near the top for rule/pipeline/folder/log mapping; Configs has TL;DR and consumer table.
- **Weak**: Queue-Sources and Parameters rely on long paragraphs and nested bullets; finding a specific mode or param requires scrolling. Cursor-Skill-Pipelines-Reference is long with no one-screen cheat.
- **Missing**: No doc uses collapsible callouts (`> [!abstract]-`) to hide long blocks; no standard "Quick Reference Table" as first section after TL;DR. Diagram position: Mermaid appears after prose in Rules (Trigger → rule flow, Context rule decision flow); same in other files — diagram is not the primary explanation per section.

---

## 2. Human vs LLM readability

- **Strengths**: Clear H2/H3 in most docs; explicit refs to "canonical" (Cursor-Skill-Pipelines-Reference, Queue-Sources, Parameters); machine-parseable blocks (code, tables).
- **Gaps**: LLM parsing (e.g. § anchors, "Param order by branch") is documented in User-Questions-and-Options-Reference and plan-mode-prompt-crafter rule but not summarized in a single "How agents read this" section in Backbone or README. Dense Responsibility/Purpose table cells in Rules and Pipelines are hard for both humans and LLMs to scan.

---

## 3. Duplication

- **Trigger → pipeline / rule**: Same mapping appears in Rules (context table), Pipelines (Trigger → pipeline table), Cursor-Skill-Pipelines-Reference (Trigger → rule mapping), README (Trigger cheat sheet). Canonical skill order and snapshot triggers live in Cursor-Skill-Pipelines-Reference; Pipelines has a Snapshot triggers summary that duplicates that.
- **Confidence bands**: Stated in Parameters, core-guardrails.mdc, confidence-loops.mdc, Cursor-Skill-Pipelines-Reference, and Pipelines § Confidence and safety. One source of truth (Parameters + confidence-loops) with others referencing is acceptable but should be explicit.
- **User-Flows**: Many High/Mid/Detailed variants (Prompt-Crafter, Rules, Chat-Prompts, Skills, System-Diagram) with overlapping content; no single "canonical" flow doc per domain; Backbone points to "User-Flow-Prompt-Crafter-*" and "Prompt-Crafter-Structure-*" without naming the primary.

---

## 4. Inconsistent formatting

- **Section order**: No doc follows the target order (TL;DR → Quick Reference Table → Mermaid → Safety Invariants → Detailed Breakdown → Examples/Triggers → Troubleshooting → Cross-references). Rules has Always-applied, Context, Questions, Commander, Usage examples, Trigger→rule Mermaid, Context rule decision Mermaid, Decision Wrappers. Pipelines has Trigger→pipeline, Decision Wrappers, Sub-pipelines, Pipeline summaries, Snapshot triggers, Usage examples, etc. Each file uses a different structure.
- **Frontmatter**: Most have `para-type`, `tags`, `status`, `title`, `created`, `links`; consistent.
- **Heading levels**: H1 for title, then H2 for major sections; some docs use H3 for sub-sections. Generally consistent.

---

## 5. Missing TL;DRs, tables, or Mermaid

- **TL;DR**: Only Configs.md, sample_config_snippet.md, and 2026-02-24-building-a-second-brain-code-para-summary.md have an explicit bold TL;DR at the top. All other core docs lack it.
- **Tables**: Rules, Pipelines, Logs, Vault-Layout, Skills have tables. Queue-Sources and Parameters would benefit from mode→file and param→default tables instead of inline prose. Trigger→pipeline table exists in Pipelines but lacks the skeleton columns (Confidence Gate, Safety Step First).
- **Mermaid**: Present in Rules, Pipelines (none in body; reference only), Cursor-Skill-Pipelines-Reference, Queue-Sources, Logs, Parameters, Backbone, Skills, Vault-Layout, User-Flows. Gaps: queue Step 0 (wrapper apply) flow and RESUME-ROADMAP append/remove-stale flow could be diagrams; diagram is often after prose, not first.

---

## 6. Broken cross-links

- **Verified**: `[[4-Archives/Resources/Roadmap-Standard-Format|Roadmap-Standard-Format]]` (file exists); `[[Templates/Master-Goal]]` (exists); `[[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]]` (path valid); `[[3-Resources/Second-Brain/User-Questions-and-Options-Reference|User-Questions-and-Options-Reference]]` §1 (exists); `[[Ingest/Decisions/Wrapper-MOC]]` (exists if created). `[[3-Resources/Plugins-Usage/Commander-Plugin-Usage|Commander-Plugin-Usage]]` — path under 3-Resources; verify folder exists.
- **To verify**: All `#anchor` links (e.g. Pipelines § Snapshot triggers summary, Queue-Sources § RESUME-ROADMAP params) resolve to actual headings; Attachment-Subtype-Mapping, Clean-technical-folder, Vault-Change-Monitor.

---

## 7. Obsidian-specific UX

- **Callouts**: Only README and Backbone use `> [!danger]` for roadmap one-shot deprecation. Safety invariants (backup first, dry_run, snapshot gates) are in prose in Rules/Pipelines/MCP rule refs but not in `[!warning]` callouts. No use of `[!tip]`, `[!note]`, `[!abstract]`, or `[!question]`.
- **Collapsible**: No doc uses `> [!abstract]-` or `> [!note]-` to fold long blocks. Native `## Heading` folding works in reading view but long sections (e.g. Queue-Sources § prompt-queue.jsonl, Parameters § Context utilization) are not wrapped in foldable callouts.
- **Dataview**: Log format and fields are documented in Logs.md; README does not embed Dataview tables for recent logs or Errors. README is not a control-center dashboard.
- **Quick-command**: Trigger phrases appear in README and Pipelines but there is no single "Quick-command" section with EAT-QUEUE aliases and copy-paste phrases.

---

## Recommendations (for Phase 2)

1. Add **one-sentence bold TL;DR** at the top of every refactored doc.
2. **Table skeleton**: Use **Trigger Phrase | Pipeline | Rule(s) | Confidence Gate | Safety Step First** where applicable (Rules, Pipelines, Cursor-Skill-Pipelines-Reference, README).
3. **Mermaid first**: Under each major section, place the Mermaid diagram first, then prose.
4. **Collapsible callouts**: Wrap long blocks in `> [!abstract]-` or `> [!note]-`; use `[!warning]` for safety invariants (unfolded).
5. **Canonical section order**: TL;DR → Quick Reference Table → Mermaid → Safety Invariants → Detailed Breakdown → Examples/Triggers → Troubleshooting → Cross-references.
6. **README as dashboard**: Embedded Dataview tables (recent logs/errors), collapsible callouts linking to each major doc, Quick-command section.
7. **Reduce duplication**: Keep one canonical source per mapping (e.g. trigger→pipeline in Pipelines or Cursor-Skill-Pipelines-Reference) and have others link or summarize in one table.
