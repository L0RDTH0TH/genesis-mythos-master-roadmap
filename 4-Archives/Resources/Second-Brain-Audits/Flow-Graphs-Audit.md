---
title: Flow Graphs Audit
created: 2026-03-10
tags: [pkm, second-brain, audit, user-flow, mermaid]
para-type: Resource
status: archived
links: ["[[3-Resources/Second-Brain/README]]", "[[Architecture-Graphs-Audit]]"]
---
# Flow Graphs Audit

Quick reference: which user-flow and structure docs have Mermaid flowcharts and what each diagram traces.

## User-Flow-* (user path through the system)

| Doc | Sections with graph | What the graphs trace |
|-----|---------------------|------------------------|
| **User-Flow-Chat-Prompts-High** | User gets ready prompt; Main gate; Safety callout | Trigger (template/Commander/type) → paste → pipeline; validation valid/invalid → paste or append → Phase1 → approve → Phase2; prompt → pipeline → proposals → approve → apply |
| **User-Flow-Chat-Prompts-Mid** | Option 1–3; Safety in every path | Template copy-paste path; Commander macro (pipeline → profile → Preview vs Craft and Queue); Queue-first path; all paths → same rules → Phase2 after approved |
| **User-Flow-Chat-Prompts-Detailed** | Safety; Template path; Commander macro; Error paths; Queue vs chat parity | Safety gate (backup, snapshot, Phase1 → Wrapper → approve → Phase2); template open→copy→paste→send; macro flow + validation; error scenarios → log/skip; chat path vs queue path → same pipeline |
| **User-Flow-Prompt-Crafter-High** | User starts crafting; Main gate; Ingest/organize outcome; Plan-mode Q&A | Trigger→pipeline→profile→assembly; params→validate→paste/queue→EAT→merge→dispatch; Phase1→Wrapper→approve→Phase2; Start→Kickoff→Mode→Optionals→ManualText→Summary→Append?→Done/NoWrite |
| **User-Flow-Prompt-Crafter-Mid** | Commander; Preview vs Craft and Queue; EAT-QUEUE; Guidance-aware; Plan-mode Q&A | Macro→pipeline/profile→out; Choice→Preview or CraftQueue→validate; Run→Merge→Validate→Dispatch; Note→guidance-aware→merge→log; CODE/ROADMAP branches→Optionals→ManualText→Summary→Append? |
| **User-Flow-Prompt-Crafter-Detailed** | Commander macro; Queue/validation; Guidance merge; Error paths; Prompt-Log; Plan-mode Q&A detailed | Macro→pipeline/profile→assembly→Preview/CraftQueue; Entry→Merge→Contract→valid/invalid; Trigger→load→merge→log; Error scenarios→abort/skip; Craft/EAT→Log→fields; Q0→CODE/ROADMAP→Q1–Q6 or Block1–4→ManualText→Summary→Validate→Route→ReadAppend |
| **User-Flow-Rules-High** | User starts a run; Main gate; Ingest Phase1 vs Phase2; EAT-QUEUE; Safety invariants | Trigger (phrase/Watcher/Commander)→rules→pipeline; confidence bands (high/mid/low)→user choice/gate; Phase1→Wrapper→user choice→EAT→Step0→apply/re-wrap; EAT→Step0→queue→dispatch→Watcher-Result; invariants (backup, dry_run, no default approved, Watcher never approves) |
| **User-Flow-Rules-Mid** | Ingest Phase1→Wrapper; Mid-band loop; Distill; Express; Archive/Organize; Roadmap; Queue; Highlight | para-zettel→Wrapper→user options→EAT→Step0; mid-band→preview→approve/feedback→re-run→gate; DISTILL/EXPRESS trigger→auto→pipeline→output; Archive/Organize→ensure→dry_run→commit; Expand→phase-direction→user choice→Step0; EAT→Step0→read→dispatch→Watcher-Result; HIGHLIGHT PERSPECTIVE→payload→EAT→distill |
| **User-Flow-Rules-Detailed** | Decision Wrapper; Confidence bands; Mid-band async; Guidance-aware; Dry_run; Queue/Step0; Watcher sync; Re-wrap; Phase-direction; Ignore proposal; Commander | Full option set (A–G, 0, R)→Step0→apply/re-wrap/re-try; high/mid/low→commit or approve gate; preview→user→re-run→feedback→gate; guidance-aware trigger→load→pipeline→safety; move→dry_run true→review→dry_run false; EAT→Step0→wrappers→queue→dispatch→Watcher-Result; user approved→Watcher sync (never sets approved); re-wrap→Step0→re-wrap branch; phase-direction→apply or re-try; ignore→no move; Commander→queue→EAT→same rules |
| **User-Flow-Diagram-*** | Diagram-first docs | Same flows as User-Flow-Rules-* but diagram-led; each section has Mermaid (High 5, Mid 8, Detailed 13) |
| **User-Flow-Skills-*** | Per-section | Ingest/skill chains; distill/express/archive/organize; queue; re-wrap; etc. (High 4, Mid 8, Detailed 15) |

## Structure / architecture (Prompt-Crafter-Structure-*)

Full architecture audit (Rules-Structure, Prompt-Crafter-Structure, System-Diagram, Skills-Structure): see **[[Architecture-Graphs-Audit]]**.

| Doc | Sections with graph | What the graphs trace |
|-----|---------------------|------------------------|
| **Prompt-Crafter-Structure-High** | End-to-end flow; Plan-mode architecture | Config/Templates→Commander→Validate→Queue→Agent→Merge→MCP; User→Agent→ParamTable+Config→Optionals→ManualText→Summary→Validate→Route→Append |
| **Prompt-Crafter-Structure-Mid** | Fallback chain; Validation; Plan-mode architecture | Queue→user_guidance→Config→MCP; Merged→contract→valid/invalid; Kickoff→CODE/ROADMAP→Optionals→ManualText→Summary→Confirm→Validate→Route→ReadAppend |
| **Prompt-Crafter-Structure-Detailed** | Plan-mode architecture (detailed); CODE funnel; ROADMAP funnel | Rule, ParamTable, QueueSources, Config→Agent→Kickoff→Mode→…→ReadAppend; CODE→mode→load→optionals→manual→out; ROADMAP→branch→MODE/RESUME→optionals→load→out |

## Verification (2026-03-10)

- **User-Flow-Rules-*** had no Mermaid; added one diagram per major section so each traces the rule(s) and user choices described in that section.
- **User-Flow-Chat-Prompts-*** had no Mermaid; added in prior pass (Safety, Template, Commander, Queue parity, Error paths).
- **User-Flow-Prompt-Crafter-*** and **Prompt-Crafter-Structure-*** already had Plan-mode and flow diagrams; confirmed they trace kickoff→mode→optionals→manual text→summary→append and architecture (rule, param table, config, validate, route).
- **User-Flow-Diagram-*** and **User-Flow-Skills-*** already diagram-heavy; no change.

All flow docs in this folder now have at least one Mermaid flowchart per substantive flow section; each diagram traces the same path or rules described in the section text.
