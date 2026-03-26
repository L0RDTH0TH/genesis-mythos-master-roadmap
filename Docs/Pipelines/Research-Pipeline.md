# Research Pipeline

**Version: 2026-03 – post-subagent migration**

Describes the RESEARCH-AGENT (and RESEARCH-GAPS) pipeline: queue-only, resolve project_id + linked_phase, research-agent-run, queue INGEST/DISTILL for new notes, Errors backstop when 0 notes.

---

## Purpose

Single reference for when and how the Research subagent runs: triggers, required params (project_id, linked_phase), skill flow, downstream queue entries, and failure handling.

---

## Triggers

- **Queue mode RESEARCH-AGENT** — dispatched by the Queue rule when an entry has `mode: "RESEARCH-AGENT"`.
- **Queue mode RESEARCH-GAPS** — alias: same as RESEARCH-AGENT with `params.gaps` set (from gap detection on current phase note).

Pre-deepen research (RESUME-ROADMAP with enable_research) is **not** run by this subagent; the **Roadmap** subagent calls **research-agent-run** directly for that path.

---

## Flow

1. **Resolve project_id and linked_phase**  
   From `source_file` (e.g. phase note under `1-Projects/<project_id>/Roadmap/`) or payload `project_id` + `params.phase` / `params.linked_phase`. **Require both.** If either missing: skip entry; append Watcher-Result failure "RESEARCH-AGENT: project_id or linked_phase missing"; do not run research-agent-run; do not add to processed_success_ids.

2. **Run research-agent-run**  
   With project_id, linked_phase, params (research_queries, research_max_tokens, gaps, etc.). Skill: vault-first → query gen → fetch → synthesize → write to `Ingest/Agent-Research/`.

3. **Queue INGEST (and optionally DISTILL) for new notes**  
   For each new note path returned by research-agent-run, the parent/Queue includes an INGEST MODE entry (source_file: path). If `params.research_distill === true`, also include DISTILL MODE per note. Pipeline-appended entries are preserved when the Queue rule re-reads and writes the queue file at Step 8.

4. **Caller backstop (0 notes)**  
   If research-agent-run returned 0 new note paths: if the skill did not add an Errors.md entry, append one per Research error entry format (Logs.md): #research-empty or #research-failed. Treat as failure: Watcher-Result failure; do not add to processed_success_ids.

5. **Watcher-Result**  
   Append one line per processed RESEARCH-AGENT entry to `3-Resources/Watcher-Result.md` (success or failure).

---

## Query context and result selection

The research-agent-run skill accepts **structured query context** and **result-selection** params so users can steer what is researched and how results are chosen.

- **research_queries**: May be an array of strings (unchanged) or array of objects `{ query, slot?, intent?, prefer? }`. **slot** = heading/section where the answer will be used; **intent** = examples | explanation | edge_cases | pseudocode | overview; **prefer** = per-query result preference (official_docs, recent, with_code, academic). Used in Step 1 (query gen), Step 2 (per-query prefer), Step 3 (slot/intent for synthesis structure).
- **research_result_preference**: Optional array of `official_docs` | `recent` | `with_code` | `diverse` | `academic`. Step 2 ranks/selects discovery results by these criteria; Step 3 adds synthesis instruction. Default absent = current behavior.
- **candidate_urls**: Optional array of URLs (strings or objects with `url`, `weight?`, `intent?`, `slot?`). Extracted first in Step 2; then discovery if needed. High-weight URLs are not dropped when merging with discovery.
- **research_focus**: Optional `junior_handoff` | `cto_brief` | `spike_proposal` | `risk_maximal`. Steers synthesis audience/tone in Step 3 (one-line prepend to synthesis prompt).
- **research_max_escalations**: Optional `0` | `1` | `2`. Default **1** for crafted/manual entries; **pre-deepen may inject 0** (fast path) unless phase/project marked research-heavy. **Step 1b (request sanity):** After Step 1 (query gen), the agent evaluates alignment, intent mismatch, and retrieval risk (rate 1–5 each); average ≥4 → proceed to Step 2; <4 → output one revision (structured JSON), re-run Step 1, repeat up to research_max_escalations. When **research_strategy** exists: `quick` → skip Step 1b; `critique_heavy` or `deep` → allow 2. See [research-agent-run SKILL](../../../../.cursor/skills/research-agent-run/SKILL.md) Step 1b.

Queue processor must pass **full params** in the RESEARCH_AGENT hand-off (no stripping). See [Queue-Sources](../../Queue-Sources.md) § RESEARCH_AGENT payload and [research-agent-run SKILL](../../../../.cursor/skills/research-agent-run/SKILL.md) Inputs.

---

## Return

One-paragraph summary; any queue entries to append (INGEST, optionally DISTILL); Success / failure. Watcher-Result with requestId.

---

## References

- [Queue-Sources](../../Queue-Sources.md) — RESEARCH-AGENT payload, research params
- [Logs](../../Logs.md) — Research error entry format
- `.cursor/agents/research.md`, `.cursor/skills/research-agent-run/SKILL.md`
