---
title: Architecture Graphs Audit
created: 2026-03-10
tags: [pkm, second-brain, audit, architecture, structure, mermaid]
para-type: Resource
status: archived
links: ["[[3-Resources/Second-Brain/README]]", "[[Flow-Graphs-Audit]]"]
---
# Architecture Graphs Audit

Same criteria as [[Flow-Graphs-Audit]]: every architecture/structure section that describes a system or data flow has a Mermaid diagram that **traces** that architecture (components, layers, or flow). This audit covers **Rules-Structure-***, **Prompt-Crafter-Structure-***, **System-Diagram-***, and **Skills-Structure-***.

---

## Rules-Structure-* (rules layout and trigger → pipeline)

| Doc | Sections with graph | What the graphs trace |
|-----|---------------------|------------------------|
| **Rules-Structure-High-Level** | Two rule layers; How trigger selects rules; Main safety gates; Ingest Phase 1 vs Phase 2; Where rules live | Always vs context layers + trigger; Phrase/Watcher/Commander/Glob → rules → pipeline; Backup/snapshot/dry_run/confidence gates (mcp + confidence-loops); Phase1 → Wrapper → user → EAT → Step0 → apply; always/context dirs → sync dirs → map docs |
| **Rules-Structure-Mid-Level** | Trigger → rule → pipeline; Decision Wrapper and re-wrap; Confidence and safety | Triggers (INGEST, EAT-QUEUE, DISTILL*, TASK QUEUE) → context rules → pipelines; Wrapper → Step0 → approved → feedback-incorporate → path-apply / re-wrap / re-try; confidence-loops bands + mcp gates + Error Protocol |
| **Rules-Structure-Detailed** | Step 0 and re-wrap / re-try / phase-direction | Step0 → filter (approved/re-wrap/re-try) → feedback → Re-wrap branch, Re-try branch, Path-apply |

**Verification:** Rules-Structure had **no** Mermaid before this audit. Diagrams added so each major section (layers, trigger selection, safety gates, Phase 1/2, trigger→pipeline, Decision Wrapper/Step0, confidence/safety, Step0 detail) has a diagram tracing that architecture.

---

## Prompt-Crafter-Structure-* (prompt-crafter components and flows)

| Doc | Sections with graph | What the graphs trace |
|-----|---------------------|------------------------|
| **Prompt-Crafter-Structure-High-Level** | End-to-end flow; Plan-mode architecture (high-level) | Config/Templates → Commander → Validate → Queue → Agent → Merge → MCP; User → Agent → ParamTable+Config → Optionals → ManualText → Summary → Validate → Route → Append |
| **Prompt-Crafter-Structure-Mid-Level** | Fallback chain; Validation (pre-dispatch); Plan-mode architecture (mid-level) | Queue → user_guidance → Config → MCP (merge order); Merged params → contract → valid/invalid; Kickoff → CODE/ROADMAP → Optionals → ManualText → Summary → Confirm → Validate → Route → ReadAppend |
| **Prompt-Crafter-Structure-Detailed** | Plan-mode architecture (detailed); CODE funnel design; ROADMAP funnel design | Rule, ParamTable, QueueSources, Config → Agent → Kickoff → Mode → Optionals → ResolveC → ManualText → Summary → Validate → Route → ReadAppend; CODE → mode → load defaults → optionals → manual → out; ROADMAP → branch → MODE (setup) or RESUME → optionals → load → out |

**Verification:** Plan-mode architecture was already present at all three levels. **Added:** Fallback chain (param precedence), Validation flow (pre-dispatch), CODE funnel (architecture steps), ROADMAP funnel (branch + optionals + output). Table-only sections (prompt_defaults, Template components, Param table, Config, Template files, Queue payload, Validation rules table, Prompt-Log structure) are reference; no diagram required for pure tables.

---

## System-Diagram-* (system-wide architecture)

| Doc | Sections with graph | What the graphs trace |
|-----|---------------------|------------------------|
| **System-Diagram-High-Level** | Major components; Capture to PARA flow; Triggers to pipelines; Safety gates; Logs and observability | Components (Ingest, Rules, Skills, MCP, Queue, Backbone); Capture → Ingest → classify → PARA; Triggers → rules → pipelines; Backup/snapshot/dry_run/confidence; Logs → MOC / observability |
| **System-Diagram-Mid-Level** | Trigger→rule→pipeline mapping; Rule types; Skills by pipeline; MCP tool groups; Queue branches; Ingest skill chain; Confidence band decisions; Vault folder tree | Same as section titles; pipeline→skills mapping; prompt-queue vs Task-Queue; ensure_structure → dry_run → commit; high/mid/low → commit or wrapper; PARA + exclusions |
| **System-Diagram-Detailed** | System flow; Safety flow; Full ingest flowchart; Ingest confidence loop; Distill/Archive/Express/Organize; **Snapshot triggers**; MCP tool groups; Log destinations; Log→MOC; Config sources; Queue processor; Highlighter flow; Testing layers; Move fallback | Backbone flow; safety gates; two-phase ingest + Wrapper; confidence state; pipeline overview; pipelines → per-change vs batch snapshot; MCP groups (Core, Move, Classify, etc.); log dests; log→MOC; Config consumers; queue flow; highlight flow; test layers; ensure_structure → dry_run → review → commit |

**Verification:** System-Diagram-* are diagram-led; almost every section already had a diagram. **Added:** Snapshot triggers (per pipeline) — diagram tracing pipelines → per-change vs batch trigger. **Naming conventions** section is reference text only (no flow); left without diagram per same criteria as Flow-Graphs-Audit (reference tables/text don’t require a graph).

---

## Skills-Structure-* (skill chains and MCP sequences)

| Doc | Sections with graph | What the graphs trace |
|-----|---------------------|------------------------|
| **Skills-Structure-High-Level** | Overall stack; High-level MCP flow; Confidence and safety gates; Pipeline → log destinations; Safety invariant flow | Rules → skills → MCP; backup → classify → organize → content → move; confidence bands → snapshot/destructive; pipeline → log dest; mcp-obsidian-integration invariant flow |
| **Skills-Structure-Mid-Level** | Ingest/Distill/Archive/Express/Organize skill chains; Key MCP sequence (move path); Confidence loop structure; Per-change vs batch snapshot; Log append points | Skill slots per pipeline; ensure_structure → dry_run → commit; loop_* fields and refinement; batch_size threshold → per-change vs batch; log after each note |
| **Skills-Structure-Detailed** | Ingest full sequence; Ingest snapshot triggers; Distill/Archive/Express/Organize full sequences; MCP move pattern; Mid-band fallback; Confidence band logic; Snapshot triggers table; Queue dispatch→pipeline→skills; Highlight flow; ensure_structure; Error handling path; Backup gate | Phase 1 skill+MCP order; when to snapshot in ingest; full skill sequences; exact move order/params; move failure → fallbacks; band logic; pipeline→snapshot; queue→pipeline→skills; highlight in distill/ingest; ensure_structure param; error path; ensure_backup vs create_backup |

**Verification:** Skills-Structure-* were already diagram-heavy; each section that describes an architecture or sequence has a matching Mermaid diagram. No gaps found.

---

## Summary

- **Rules-Structure-***: Had no graphs; added diagrams for two layers, trigger selection, safety gates, Phase 1/2, trigger→pipeline, Decision Wrapper/Step0, confidence/safety, Step0 detail.
- **Prompt-Crafter-Structure-***: Had Plan-mode architecture at all levels; added fallback chain, validation flow, CODE funnel, ROADMAP funnel.
- **System-Diagram-***: Already had graphs per section; added Snapshot triggers diagram; Naming conventions remains text-only (reference).
- **Skills-Structure-***: Already had graphs per section; no changes.

All architecture docs now have at least one Mermaid diagram per substantive **architecture** section (component layout, data flow, or trigger→pipeline); table-only or reference-only sections are not required to have a graph.
