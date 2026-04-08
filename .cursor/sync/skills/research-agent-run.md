---
name: research-agent-run
description: Runs the research sequence (vault-first → query-gen → fetch → synthesize), writes synthesized notes to Ingest/Agent-Research/, optionally writes raw scraped content to Ingest/Agent-Research/Raw/ and updates Raw-Index for vault-first deduplication, and returns paths/summaries for deepen injection. Use when RESUME-ROADMAP pre-deepen has enable_research or when queue mode RESEARCH-AGENT is dispatched.
---

# research-agent-run

## When to use

- When **auto-roadmap** runs the pre-deepen research hook (RESUME-ROADMAP action deepen with `params.enable_research` or auto-detect from phase content).
- When **auto-eat-queue** dispatches **mode: RESEARCH-AGENT** (source_file or project_id + params).

## Inputs

- **project_id** (required): From queue/params or derived from source_file path under `1-Projects/<project_id>/`.
- **linked_phase** (required): e.g. `"Phase-4-1"` or phase roadmap note path; used for frontmatter and slug.
- **queries** (array, max 3–5): Search queries; from **params.research_queries** or derived from phase/outline content. **research_queries** may be array of **strings** (unchanged) or array of **objects** `{ query, slot?, intent?, prefer? }`; normalize any string element to `{ query: element }` at start of run. Object fields: **query** (required), **slot** (optional, e.g. `"## Cancellation"`), **intent** (optional: examples | explanation | edge_cases | pseudocode | overview), **prefer** (optional: official_docs | recent | with_code | academic or array). Step 1 uses as-is or derives; Step 2 uses per-query prefer; Step 3 uses slot/intent for synthesis.
- **params.research_result_preference** (optional): Array of `official_docs` | `recent` | `with_code` | `diverse` | `academic`. Default absent = current behavior. Step 2: rank/select discovery results by these criteria; Step 3: add synthesis instruction. Per-query `prefer` overrides for that query.
- **params.candidate_urls** (optional): Array of URL strings or objects `{ url, weight?, intent?, slot? }`. When present, extract these first (Step 2), then discovery if needed; Step 3 merges curated + discovered. Default weight 1; sort by weight descending; do not drop high-weight URLs.
- **params.research_focus** (optional): `junior_handoff` | `cto_brief` | `spike_proposal` | `risk_maximal`. Default absent = current behavior. Step 3: prepend one-line audience/tone to synthesis prompt (e.g. "Target audience: junior devs who need copy-paste code").
- **params.avoid_duplicate_headings** (optional): Array of section title strings; merged with auto-derived "Do not duplicate" in Step 0; Step 3 instructed not to repeat.
- **params.research_max_escalations** (optional): `0` | `1` | `2`. Default **1** for crafted/manual entries; **pre-deepen may inject 0** unless phase/project marked research-heavy. When **0**, skip Step 1b (request sanity) and go straight from Step 1 to Step 2. When **1** or **2**, run Step 1b after Step 1; agent may revise queries/intent up to this many times (structured JSON output). **Effective cap (research_strategy tie-in):** If **params.research_strategy** is `quick` → effective max = 0 (skip Step 1b). If `critique_heavy` or `deep` → effective max = min(2, param or 1). Otherwise effective max = param (default 1). Step 1b consumes; Step 5 writes frontmatter.
- **params.research_tools** (optional): Array of tools to use; default `["web", "firecrawl"]`. Allowed values: `web`, `semantic-scholar`, `arxiv`, `crossref`, `firecrawl`, `browser`. **Normalize** when reading: treat `"freecrawl"` or `"browse"` as `"firecrawl"` (use Firecrawl MCP; if unavailable, fall back to mcp_web_fetch and record in research_tools_used); treat `"x"` as academic (use scholarly discovery when tools include semantic-scholar/arxiv/crossref); ignore unknown keys. Old payloads with `["web","x","browse"]` or `["web","freecrawl"]` continue to work.
- **params.research_max_tokens** (optional): Soft cap on synthesized output **per note** (default **15000** from Parameters); truncate if exceeded to avoid one bad query consuming context.
- **params.research_result_limit** (optional): Max results per query / total fetch calls (default 3–5, may be bumped to 5–7 in Parameters for util-driven runs).
- **params.low_util** (optional, bool): Hint from auto-roadmap that this run was triggered by a low Ctx Util % deepen; when true, derive additional gap-based queries from shallow sections of the phase note (see below).
- **params.gaps** (optional, array): When present, run in **gap-fill** mode. Each element: `id`, `heading`, `type` (missing_examples | missing_pseudocode | thin_explanation | missing_edges), `severity`, `excerpt`, `suggested_query_seed`. **~70% of generated queries** must target these gaps; remainder from phase/outline. Return structured **gap_fills** (see Outputs).
- **params.origin** (optional, string): e.g. `"roadmap-deepen"` or `"commander-gaps"`; when `roadmap-deepen`, prioritize handoff-oriented synthesis.
- **params.research_verify** (optional, bool, default false): when true, after synthesis re-query 1–2 sources to confirm key claims; if conf &lt; 68%, log #research-verify-failed and discard that fill.
- **params.max_gap_fills_per_run** (optional): Cap on number of gap fills to return (default from Parameters, e.g. 2–3). **Per-gap token sub-cap**: e.g. 2–3k tokens per fill; total still capped by **research_synth_cap_tokens**.
- **params.store_raw** (optional, default **true**): If true, write raw to Ingest/Agent-Research/Raw/ and update Raw-Index; if false, skip raw write/index; vault-first lookup in Step 2 still runs.
- **params.raw_max_chars_per_source** (optional): Cap length per block when writing raw note; truncate with one-line note if exceeded.

**Flow:** Step 0b load Raw-Index; Step 2 vault-first per URL (reuse from index or fetch); Step 5a synthesis + 5b raw note and index append; synthesis note gets ## Raw sources (vault) and raw_sources frontmatter. Synthesis notes in Ingest/Agent-Research/ are eligible for **ingest without a Decision Wrapper** when the ingest pipeline's direct-move conditions are met (ingest rule § Cursor-agent direct move). See full [SKILL](.cursor/skills/research-agent-run/SKILL.md).

## Fetch stack (external)

- **Discovery:** **web_search** (Cursor built-in); **Semantic Scholar MCP** (when `semantic-scholar` in research_tools; academic or paper-suited queries); **arXiv MCP** (when `arxiv` in research_tools); **Crossref** or academic-search aggregator (when `crossref` in research_tools). Limit total discovery calls (e.g. 3–5); respect rate limits per [Research-Stack-Rate-Limits](3-Resources/Second-Brain/Research-Stack-Rate-Limits.md).
- **Extraction:** **Firecrawl MCP (self-hosted)** when `firecrawl` in research_tools; on missing tool or error and `browser` in research_tools → **Browser MCP or browser-tools**; on missing/error → **mcp_web_fetch**. If all fail for a URL, keep snippet and note "full page unavailable". **Never throw** — if discovery returned results, always produce at least a search-only synthesis (possibly with "full page unavailable" for some URLs).
- **Academic:** When run is academic (phase/topic has **research_auto_keywords** or explicit param), prefer Semantic Scholar / arXiv / Crossref when in research_tools; else use **web_search** with `site:arxiv.org` / `site:pubmed.ncbi.nlm.nih.gov` etc. No BrowserAct.

Document in [MCP-Tools.md](3-Resources/Second-Brain/MCP-Tools.md) § Research agent and Research stack setup. See [Research-Stack-Rate-Limits](3-Resources/Second-Brain/Research-Stack-Rate-Limits.md).

## Citation format (synthesis)

- For every external source in the synthesized note use: **`[Source: Page title or short description](url)`** on its own line after a claim or block.
- Include a **"## Sources"** section at the end listing all URLs used. No tool-generated BibTeX/APA; consistency is via this inline + list format.

## Research consumption contract (fixing “research ran but wasn’t used”)

This skill is frequently invoked as a **dependency** (chain step) for another pipeline (roadmap deepen, ingest planning, express, etc.). A recurring failure mode is: research notes are created under `Ingest/Agent-Research/`, but the **caller never integrates** them into the artifact it is building.

To prevent that, this skill must return (in addition to paths/summaries) a **ready-to-inject markdown block** that callers can paste into their draft or append to the target note.

### Required return fields (in addition to paths/summaries)

- **injection_block_markdown** (string, required when synthesis exists): A single markdown block the caller can paste verbatim. It must:
  - Start with `## Research integration` (or `### Research integration` when the caller will nest it).
  - Include a short **Key takeaways** list (5–10 bullets).
  - Include a short **Decisions / constraints** list (3–7 bullets) when the sources support it; otherwise include a “Pending decisions” list.
  - Include **Links**: wiki-links (or plain paths) to the created synthesis note(s) and any used raw notes.
  - End with a **Sources** subsection or a pointer to the synthesis note’s `## Sources`.
- **key_takeaways** (array of strings, optional but recommended): Mirrors the takeaways from the injection block so callers can weave them into other structures (e.g., decision logs).
- **decision_candidates** (array of strings, optional): Candidate decisions/constraints surfaced by synthesis; callers may insert into a decisions log.

### Caller obligation (normative)

Any agent/skill/subagent that calls `research-agent-run` must do **one** of the following before it reports success:

- **Inline integrate**: Insert `injection_block_markdown` into the draft it is about to write (preferred), OR
- **Persist as pending injection**: If the caller cannot safely edit the target artifact in the same run, it must store the injection block and research paths in a durable “pending injection” slot appropriate to that pipeline (e.g., a state note frontmatter field such as `injected_research_paths` + `injected_research_summary` or an equivalent pending section), and then ensure the next run consumes and clears it.

If the caller does neither, the run should be treated as **incomplete** even if synthesis notes were created.

## Instructions

0. **Gather vault context** (before query generation):
   - Using **project_id** and **linked_phase**: call **obsidian_list_notes** on `1-Projects/<project_id>/` or `1-Projects/<project_id>/Roadmap/`; **obsidian_read_note** on (1) current phase/roadmap note for linked_phase, (2) `distilled-core.md` in project Roadmap if present, (3) PMG or key project note if easily resolvable; optionally **obsidian_global_search** with a project-scoped query (e.g. project_id or project name), cap results (e.g. 5–10).
   - Build a short "vault context" summary: what the project/phase already states, what is missing or needs confirmation. **Append "Do not duplicate:"** 3–5 key points or headings already covered in phase note / distilled-core (from first few headings or bullets; truncate to ~100 words). When **params.avoid_duplicate_headings** is present, merge those strings into this list. Use the full summary (including do-not-duplicate) in step 1 (query gen) and step 3 (synthesize).
   - **On any Obsidian MCP error** (e.g. project path missing, permission): **do not block**. Proceed with **empty vault context**; run query gen from phase content only. Optionally log one line to run context or Errors.md only if critical (e.g. "vault context skipped: path missing"). Goal: research still runs with external fetch only.

1. **Query generation**:
   - **Normalize research_queries:** For each element in params.research_queries, if string use `{ query: element }`; if object require `query`, allow slot, intent, prefer. Pass normalized list to Step 2 and Step 3.
   - If queries not provided, derive 3–5 search queries from the phase/outline content **and vault context** (e.g. current secondary or phase roadmap note via obsidian_read_note).
   - When research_queries are structured (objects with slot/intent/prefer), preserve those fields so Step 2 can use per-query prefer and Step 3 can use slot and intent for synthesis structure and style.
   - **Gap-fill mode (params.gaps present):** When **params.gaps** is present, **~70% of generated queries** must target these gaps. For each gap (up to **max_gap_queries_per_deepen**, default 3): use **suggested_query_seed** and **type** to build 1–2 targeted queries. **Templates by type**: `missing_pseudocode` → e.g. "open-source pseudo-code for [topic] [suggested_query_seed]", `missing_edges` → "best-practice [topic] edge cases", `missing_examples` → "[topic] reference implementation examples", `thin_explanation` → "expand on [heading]: [excerpt]". Cap total gap-targeted queries; remaining 30% from phase/outline for breadth. **Fixed guidance**: "Prioritize results usable for junior dev handoff: code snippets, edge cases, perf notes, open-source examples with sources."
   - When `params.low_util === true` (or equivalent flag from auto-roadmap) and **params.gaps** is absent, also derive **gap-based queries** from under-detailed sections of the phase note:
     - Scan the phase note body and identify headings or bullet blocks whose combined text under that section is **< ~50 words** — treat these as **shallow** sections.
     - Take the top 2–3 shallow candidates (by structural importance or first appearance), and for up to **2** of them generate a query of the form:  
       `"expand on [Heading or bullet]: [first sentence or bullet text]"`.
     - Cap total queries so that `base_outline_queries` (3–5) + `gap_queries` (≤2) ⇒ **at most 7 queries** for the run.

1b. **Request sanity check** (Step 1b): **When research_max_escalations is 0** (or research_strategy is "quick"), skip this step and pass the current query set from Step 1 to Step 2. **Otherwise:** Run after Step 1; may loop back to Step 1 up to **research_max_escalations** times (effective cap: research_strategy "critique_heavy" or "deep" → allow 2). **Persona:** "You are the Request Sanity Agent. Your ONLY job is to answer these three questions strictly: (1) **Alignment:** Do the current queries (and their slot/intent/prefer/tool_hint) clearly match the needs implied by the phase note, outline, linked gaps, and vault 'Do not duplicate' list? Rate 1–5. (2) **Intent mismatch:** Is there evidence the user requested one thing (e.g. 'overview') but the slot/context implies another (e.g. '## Implementation' needs pseudocode/examples)? Rate likelihood 1–5. (3) **Risk of wrong retrieval:** If we fetch now, are we likely to get irrelevant/noisy/irreproducible content (too broad/vague, wrong prefer, mismatched research_focus)? Rate 1–5. If average rating ≥4 → proceed (output: {\"proceed\": true}). If <4 → output exactly one revision: {\"proceed\": false, \"revision\": {...}}. Never invent new slots or tool_hints unless clearly justified by vault. Prefer minimal change." **Input:** Current query set (normalized), vault context summary, research_focus, slot/intent from structured research_queries. **Output:** Step 1b must emit **JSON only** (no free prose except the reason string). Schema: `{ "proceed": boolean, "revision": { "revised_research_queries": [ ... array of normalized objects or strings ... ], "reason": "string (max 100 chars)", "escalation_trigger": "intent_mismatch | alignment_low | retrieval_risk" } | null }`. **Loop:** Parse the JSON. If `proceed === true`, pass final query set to Step 2. If `proceed === false` and escalation count < effective max: set effective research_queries = revision.revised_research_queries; re-run Step 1 (query generation) with this as the new effective research_queries (normalize and preserve slot/intent); increment escalation count; **post-revision lite (optional):** run one Step 1b "lite" pass — only confirm alignment ≥4 (no full revision output); if lite says proceed, go to Step 2; if not, still go to Step 2 with the revised queries (do not consume another escalation); then run Step 1b again only if cap not reached and a full evaluation is needed. If count reached, pass current query set to Step 2. Store **escalation_count**, **escalation_reason** (revision.reason), **escalation_trigger** (revision.escalation_trigger) for Step 5 frontmatter. Optionally store **sanity_check_rating** (e.g. "4.3/5 (proceed)") when Step 1b ran and proceeded without revision, for debugging.

2. **Fetch** (Discovery): **Persona:** "You are the Discovery Agent. Your only job is to find the best sources for the queries; rank by preference and diversity; never drop high-value curated URLs." (1) **If params.candidate_urls present:** Parse as URLs (strings) or objects `{ url, weight?, intent?, slot? }`; sort by weight descending (default weight 1). Run **extraction** on these URLs first (Firecrawl → Browser MCP → mcp_web_fetch), up to research_result_limit. Do not drop high-weight candidates when merging with discovery. (2) Run **discovery** using research_tools and academic routing: if `semantic-scholar` in research_tools and (academic or paper-suited queries), call Semantic Scholar MCP; if `arxiv` in research_tools and academic/preprint, call arXiv MCP; if `crossref` in research_tools and DOI/citation need, call Crossref/aggregator; if `web` in research_tools or non-academic, use web_search. Cap total discovery calls (e.g. 3–5); respect research_result_limit and rate limits per Research-Stack-Rate-Limits. (3) When **selecting which discovery results** to send to extraction, apply **params.research_result_preference** (and per-query **prefer** from structured research_queries): rank/select by official_docs, recent, with_code, diverse, academic; prefer diversity when `diverse` in list. (4) For each chosen URL from discovery, run **extraction** chain (same as candidate_urls). (5) Respect research_result_limit and total fetch call cap. (6) Never throw; produce at least search-only synthesis when discovery or candidate_urls returned results. **Structured hand-off (in memory):** Build **raw_blocks**: array of `{ source: url or label, content: string | snippet }` from extraction output; pass to Step 3 so synthesis works from structured data before converting to markdown.

3. **Synthesize** (Synthesis): **Persona:** "You are the Synthesis Agent. Your only job is to turn evidence into clear, cited narrative; do not repeat vault content; apply slot/intent and research_focus." **Structured hand-off:** Read **raw_blocks** from Step 2; optionally build in-memory **confidence_map** (slot or section → `{ level: high|medium|low, rationale }`) before writing final markdown; Step 5 can use this for optional frontmatter (e.g. confidence_distribution in Phase 2).
   - **Do-not-duplicate:** Add instruction: "Do not repeat content that is already stated in the vault; add only new or clarifying information." Use the "Do not duplicate" list from Step 0 (vault context).
   - When **params.research_result_preference** is set: "When selecting which discovery results to use, apply: [list from param]. Prefer sources that match; if none do, use best available and note in synthesis."
   - When **research_queries** include **slot**: use slot in output structure (e.g. "## Filled: [slot]" or "Answer for: [slot]").
   - When **intent** is present (per query): tailor synthesis—e.g. prioritize code blocks for `examples`, conceptual summary for `explanation`, edge-case callouts for `edge_cases`, pseudocode for `pseudocode`, high-level for `overview`.
   - When **params.research_focus** is set: prepend one line to the synthesis prompt by value: `junior_handoff` → "Target audience: junior devs who need copy-paste code and clear edge cases."; `cto_brief` → "Target audience: CTO who cares only about risk and timeline."; `spike_proposal` → "Target: spike/proposal; scope and feasibility first."; `risk_maximal` → "Emphasize risks, failure modes, and mitigation."
   - Turn fetched content into Markdown summaries **with source URLs and inline citations** per the **Citation format** above (e.g. `[Source: Title](url)` and ## Sources at end). When **params.origin === "roadmap-deepen"** or gap-fill mode, add **fixed guidance**: "Prioritize results usable for junior dev handoff: code snippets, edge cases, perf notes, open-source examples with sources."
   - Apply **research_max_tokens** (params or Config, default 15000): soft cap on synthesized output **per note**; **truncate if exceeded**. In **gap-fill** mode, apply a **per-gap sub-cap** (e.g. 2–3k tokens per fill from Parameters); total run still capped by **research_synth_cap_tokens** (default 10000).
   - **Gap-fill output**: When **params.gaps** is present, return a structured **gap_fills** array instead of (or in addition to) a single summary. Each element: `gap_id`, `filled_markdown` (pattern: `"## Filled Gap: [heading fragment] — [short label]\n\n[explanation/code]\n\n[Source: …](url)"`), `sources` (array of URLs or labels), **fill_conf** (0–100). If **fill_conf** is below 68% for a fill, do not include it in gap_fills (or mark as discarded). When **params.research_verify** is true, re-query 1–2 sources for key claims; if mismatch or confidence below 68%, log **#research-verify-failed** and discard that fill.
   - Additionally, apply **per-run synthesis cap** (`research_synth_cap_tokens`, default **10000**): if combined synthesized content exceeds this cap, truncate and note in logs.
   - If synthesis confidence **< 68%** (no relevant hits or low relevance), treat as failure and go to step 4 (failure / empty mode).

4. **Failure / empty mode**:
   - If fetch returns **0 results**, or synthesis **confidence < 68%**, or the total synthesized content is **< ~1500 tokens** (very small / effectively empty), the skill **MUST** append one entry to [Errors.md](3-Resources/Errors.md) **before** returning. Use the **Research error entry format** in [Logs.md](3-Resources/Second-Brain/Logs.md) § Research error entry format: heading `### YYYY-MM-DD HH:MM — research-empty` or `research-failed`, metadata table (`pipeline: research-agent-run`, `linked_phase`, `project_id`, `error_type: research-empty | research-failed`), **#### Trace** (reason and, if any, queries used), **#### Summary** (root cause, impact, suggested fixes, recovery), and at least one of **#research-failed** or **#research-empty** in the body for grep/Dataview.
   - **Invariant:** If the skill returns 0 paths/summaries for any of the above reasons and does **not** write this Errors.md entry, the run is incomplete; the caller should treat as failure and log as backstop (see caller contract in auto-roadmap and roadmap-deepen).
   - Return empty paths/summaries so the caller **skips injection** and **proceeds to roadmap-deepen without research**. Do **not** block the deepen loop; a failed or empty research run may still consume a cooldown slot but must not stall roadmap progress.

5. **Write**: Call `obsidian_ensure_structure`(folder_path: `"Ingest/Agent-Research"`). Create note(s) in `Ingest/Agent-Research/` via MCP (obsidian_update_note or create). **Frontmatter**: `research_query`, `linked_phase`, `project_id`, `created` (YYYY-MM-DD), `tags: [research, agent-research]`, **`research_tools_used`** (array of tools actually used: e.g. `["semantic_scholar", "firecrawl"]`, `["web_search", "firecrawl", "firecrawl_fallback_mcp_web_fetch"]`, or `["web_search", "mcp_web_fetch"]` when Firecrawl was not used. Allowed values: `semantic_scholar`, `arxiv`, `crossref`, `web_search`, `firecrawl`, `browser_mcp` or `browser_tools`, `mcp_web_fetch`), `agent-generated: true`. **Optional (traceability):** When **research_result_preference** was used, set `research_preference_used: ["official_docs","with_code"]` (actual values applied). When **research_focus** was set, set `research_focus: "<value>"`. When **candidate_urls** was used, set `candidate_urls_used: N` (count) or log primary_sources. **Request sanity (Step 1b):** Always set **research_escalations_used: 0 | 1 | 2** (count of revisions applied). When >0 set **research_escalation_reason** (revision.reason, max 100 chars) and optionally **research_escalation_trigger** (intent_mismatch | alignment_low | retrieval_risk). When 0 but Step 1b ran, optionally set **sanity_check_rating** (e.g. "4.3/5 (proceed)") for debugging. Filename per [Naming-Conventions](3-Resources/Second-Brain/Naming-Conventions.md) (slug from research_query or linked_phase, then date-time). **Snapshot before write** per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc) when updating existing path; for new files, backup at pipeline start is sufficient.

6. **Return**: Paths of created notes and short summaries (1–2 sentences per note or combined) for the caller to inject into the deepen prompt. When run in **gap-fill** mode (**params.gaps** present), also return **gap_fills**: array of `{ gap_id, filled_markdown, sources, fill_conf }` for the caller (roadmap-deepen) to inject inline before writing the note. Respect **max_gap_fills_per_run**; only include fills with **fill_conf ≥ 68%** (or higher threshold from Parameters).

In all non-empty synthesis cases, also return:

- `injection_block_markdown`
- optionally `key_takeaways`, `decision_candidates`

## MCP tools

- **Step 0 (vault):** `obsidian_list_notes`, `obsidian_read_note`, `obsidian_global_search` — gather project-linked context.
- **Write:** `obsidian_ensure_structure`, `obsidian_update_note` / create — write synthesized note(s) with frontmatter.
- **obsidian-snapshot** skill — per-change snapshot before overwrite (not for brand-new creates at new path).
- **Fetch (discovery):** **web_search** (Cursor built-in), **Semantic Scholar MCP**, **arXiv MCP**, **Crossref** or academic-search aggregator — per research_tools and academic routing.
- **Fetch (extraction):** **Firecrawl MCP** (self-hosted), **Browser MCP or browser-tools**, **mcp_web_fetch** — in that order; fallback on missing/error.

## Reference

- [Vault-Layout § Ingest/Agent-Research](3-Resources/Second-Brain/Vault-Layout.md)
- [auto-roadmap](.cursor/rules/context/auto-roadmap.mdc) — pre-deepen research hook
- [Parameters § Queue modes](3-Resources/Second-Brain/Parameters.md) — research_max_tokens, research_tools, research_auto_keywords
- [MCP-Tools.md § Research agent](3-Resources/Second-Brain/MCP-Tools.md) — fetch stack, Research stack setup
- [Research-Stack-Rate-Limits](3-Resources/Second-Brain/Research-Stack-Rate-Limits.md) — rate limits for operator awareness
