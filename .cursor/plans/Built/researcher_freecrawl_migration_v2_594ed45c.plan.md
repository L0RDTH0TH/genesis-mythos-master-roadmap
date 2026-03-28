---
name: Researcher FreeCrawl migration v2
overview: "V2 of the researcher migration to vault-first, skill-based FreeCrawl: same skill/MCP/Parameters/docs changes as v1, plus explicit compensation for each affected area (auto-eat-queue, auto-roadmap, roadmap-deepen, params, Vault-Layout, Logs, Mode-Success-Contracts) and shielding against FreeCrawl unavailability, vault Step 0 failure, RESEARCH-AGENT resolution failure, skill exceptions, and params backward compatibility."
todos: []
isProject: false
---

# Migrate researcher to skill-based FreeCrawl (v2)

## Goal

Same as v1: **vault-first** (Obsidian project context) then **external fetch** via **web_search + FreeCrawl MCP**, with fallbacks, academic compensation, and citation/observability. **V2 adds:** how each affected area compensates so the **goal stays identical**, and **where to shield** against failures.

---

## Prerequisites — FreeCrawl MCP setup

Complete this **before** implementing the skill and rule changes so the researcher can use FreeCrawl from the first run.

1. **Ensure uv/uvx is available**
  FreeCrawl MCP is run via `uvx`. If needed: install uv (e.g. `curl -LsSf https://astral.sh/uv/install.sh | sh` or use existing Python/uv). Confirm with `uvx --version`.
2. **Install and verify FreeCrawl MCP**
  Run `uvx freecrawl-mcp` in a terminal to confirm the server starts (stdio). Check [PyPI freecrawl-mcp](https://pypi.org/project/freecrawl-mcp/) for the exact package name and any env vars or options.
3. **Add FreeCrawl to Cursor MCP config**
  - Open **Cursor Settings → Features → MCP** (or edit `~/.cursor/mcp.json`).  
  - Add a new MCP server with the **command** that runs FreeCrawl (e.g. `uvx freecrawl-mcp`). Use the exact command from FreeCrawl docs (e.g. `uvx freecrawl-mcp` or `python -m freecrawl_mcp`).  
  - Save; restart Cursor or refresh MCP if required.
4. **Document the setup in the vault (optional)**
  In [3-Resources/Second-Brain/MCP-Tools.md](3-Resources/Second-Brain/MCP-Tools.md) (or a short note under 3-Resources), add one line with the exact command and any env vars (e.g. `FreeCrawl MCP: uvx freecrawl-mcp`) so the setup is reproducible. The main Research stack paragraph in MCP-Tools.md will already state that FreeCrawl is required; this step is for the install command.

**If FreeCrawl is not set up:** The skill and rules still run: research uses **web_search + mcp_web_fetch** fallback only (see Part C.1). No install is strictly required for the migration to be valid, but without FreeCrawl the researcher cannot scrape full pages and may produce thinner results.

---

## Part A — Core migration (unchanged from v1)

- **Skill:** [.cursor/skills/research-agent-run/SKILL.md](.cursor/skills/research-agent-run/SKILL.md) — Step 0 vault-first (list_notes, read_note, global_search); fetch = web_search + FreeCrawl MCP, fallback mcp_web_fetch; academic via web_search site:...; citation format; research_tools_used values; params.research_tools default `["web","freecrawl"]`; renumber steps; MCP list.
- **MCP-Tools.md:** Replace Research agent paragraph with new stack + vault-first + FreeCrawl requirement.
- **Parameters.md:** research_tools default and description.
- **Queue-Sources.md, Skills.md, Vault-Layout, sync, changelog:** As in v1.

---

## Part B — Compensation by affected area

Each area must achieve the **same goal** (research runs when enabled; results inject into deepen or queue INGEST; failures are visible and do not block roadmap).

### B.1 auto-eat-queue (RESEARCH-AGENT dispatch)

- **Current behavior:** Resolve project_id and linked_phase from source_file or payload; run research-agent-run; for each new note append INGEST (and optionally DISTILL); append Watcher-Result.
- **Compensation:**  
  - **Before** calling research-agent-run: require that **both** project_id and linked_phase are resolved (from source_file path under `1-Projects/<project_id>/Roadmap/` or from payload `params.project_id` + `params.phase` / `params.linked_phase`). If either is missing after resolution, **skip** this entry; append Watcher-Result: `status: failure | message: "RESEARCH-AGENT: project_id or linked_phase missing"`; do **not** run the skill; do **not** add to processed_success_ids (so Step 8 will write this entry back with `queue_failed: true`).  
  - **After** research-agent-run returns: if it returns **0 new note paths** (empty run), treat as **failure** for this entry: append Watcher-Result with `status: failure` and message e.g. "RESEARCH-AGENT: 0 notes (empty or failed research)"; do not add to processed_success_ids. This avoids **silent no-op** (Mode-Success-Contracts: recovery path = log + surface).  
  - **Identical goal:** RESEARCH-AGENT still writes to Ingest/Agent-Research/ and queues INGEST when successful; when it cannot (missing params or empty result), we fail visibly and mark queue_failed.

**File:** [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) — add explicit pre-dispatch check for RESEARCH-AGENT (project_id + linked_phase required) and post-run rule (0 notes → failure + Watcher-Result). Sync to [.cursor/sync/rules/context/auto-eat-queue.md](.cursor/sync/rules/context/auto-eat-queue.md).

### B.2 auto-roadmap (pre-deepen research)

- **Current behavior:** When research enabled, call research-agent-run inline; on 0 results / conf <68% / <1500 tokens, skip injection and proceed to deepen; log #research-failed or #research-empty.
- **Compensation:**  
  - If research-agent-run **throws** or **times out** (e.g. FreeCrawl unavailable and agent does not catch): **catch** at caller, treat as **empty**: log to Errors.md with #research-failed, reason e.g. "exception" or "tool unavailable"; return empty paths/summaries; **proceed to roadmap-deepen without research**. Do not let the exception bubble and block the deepen step.  
  - Document this in the pre-deepen steps: "If research-agent-run raises an exception, log to Errors.md (#research-failed, pipeline research-agent-run, reason), return empty paths/summaries, proceed to roadmap-deepen."
- **Identical goal:** Deepen always runs; research is best-effort; failures are logged and visible.

**File:** [.cursor/rules/context/auto-roadmap.mdc](.cursor/rules/context/auto-roadmap.mdc) — add one bullet under failure/empty mode: "If research-agent-run throws or times out, catch, log #research-failed with reason, return empty paths, proceed to deepen." Sync to [.cursor/sync/rules/context/auto-roadmap.md](.cursor/sync/rules/context/auto-roadmap.md).

### B.3 roadmap-deepen (gap-fill research)

- **Current behavior:** When high-severity gaps and research enabled, call research-agent-run with params.gaps; inject gap_fills with fill_conf ≥68% into draft; if no gap_fills, proceed without injection.
- **Compensation:** No contract change. If FreeCrawl is down, research-agent-run may return **partial** gap_fills (some URLs scraped via mcp_web_fetch only) or **empty** gap_fills. Roadmap-deepen already: inject only fills with fill_conf ≥68%; if gap_fills is empty or missing, proceed without injection. Document in roadmap-deepen skill (or keep as-is): "When research-agent-run returns empty or partial gap_fills, inject whatever is returned; do not fail the deepen step."
- **Identical goal:** Gap-fill remains best-effort; deepen never blocks on research.

**File:** [.cursor/skills/roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md) — optional one-line note in step 4.5: "If research-agent-run returns empty or partial gap_fills, inject only available fills (fill_conf ≥68%); proceed to step 5 regardless."

### B.4 params and research_tools (backward compatibility)

- **Current:** Queue entries and Config may have `params.research_tools: ["web","x","browse"]`.
- **Compensation:** In research-agent-run skill, **normalize** params.research_tools when reading: treat `"browse"` as `"freecrawl"`; treat `"x"` as "use academic path via web_search (site:...)" and do not require a separate tool. So old payloads continue to work; only the implementation (FreeCrawl, mcp_web_fetch) changes.
- **Identical goal:** Same param names; behavior maps to new stack.

**File:** [.cursor/skills/research-agent-run/SKILL.md](.cursor/skills/research-agent-run/SKILL.md) — in Inputs or Fetch section: "Normalize params.research_tools: 'browse' → freecrawl, 'x' → academic via web_search; ignore unknown keys."

### B.5 Vault-Layout and Logs (research_tools_used values)

- **Current:** Vault-Layout and Logs say research_tools_used e.g. `["web","browse"]`.
- **Compensation:** Update to accept **new** values: `["web_search","freecrawl"]`, `["web_search","freecrawl_fallback_web_fetch"]`, `["web_search"]`. Optionally note that `["web","browse"]` is legacy (skill writes new values).
- **Identical goal:** Observability and Dataview still work; no breaking change for existing notes (old values remain valid).

**Files:** [3-Resources/Second-Brain/Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) (Ingest/Agent-Research row), [3-Resources/Second-Brain/Logs.md](3-Resources/Second-Brain/Logs.md) (Research notes cell) — add sentence: "research_tools_used may be e.g. web_search, freecrawl, freecrawl_fallback_web_fetch; legacy values web, browse remain valid."

### B.6 Mode-Success-Contracts (RESEARCH-AGENT)

- **Current:** Success = notes written + INGEST queued or clear error; silent failure = no notes, no error; recovery = log Errors.md.
- **Compensation:** State explicitly: when research run returns **0 notes** (empty or failed), the **queue processor** must **not** treat as success — append Watcher-Result failure and set queue_failed so the entry is retried or visible. "Clear error" includes logging #research-failed/#research-empty and surfacing via Watcher-Result.
- **Identical goal:** No silent no-op; recovery path remains log + optional Decision Wrapper.

**File:** [3-Resources/Second-Brain/Mode-Success-Contracts.md](3-Resources/Second-Brain/Mode-Success-Contracts.md) — under RESEARCH-AGENT: add bullet "When 0 notes are written, append Watcher-Result failure and mark entry queue_failed; do not count as success."

---

## Part C — Shielding against failures

### C.1 FreeCrawl unavailable

- **Risk:** FreeCrawl MCP not configured or scrape fails for every URL.
- **Shield:** In research-agent-run skill: (1) Try FreeCrawl for each URL; (2) on missing tool or error, use mcp_web_fetch for that URL; (3) if both fail, keep search snippet + note "full page unavailable" in synthesis; (4) **never throw** — if web_search returned results, always produce at least a search-only synthesis (possibly with "full page unavailable" for some URLs). So 0 notes only when web_search also fails or synthesis conf <68% / <1500 tokens (existing failure mode).

### C.2 Vault Step 0 failure

- **Risk:** obsidian_read_note or list_notes fails (e.g. project path missing, permission).
- **Shield:** In research-agent-run Step 0: on any Obsidian MCP error for vault context, **do not block**: proceed with **empty vault context**, run query gen from phase content only (existing path). Optionally log one line to run context or Errors.md only if critical (e.g. "vault context skipped: path missing"). Goal: research still runs with external fetch only.

### C.3 RESEARCH-AGENT entry missing project_id or linked_phase

- **Risk:** User or Commander adds RESEARCH-AGENT with only source_file (e.g. non-roadmap path) or no params.
- **Shield:** In auto-eat-queue, **before** dispatch for RESEARCH-AGENT: require both project_id and linked_phase resolvable (from source_file path or payload). If not, skip entry, append Watcher-Result failure "RESEARCH-AGENT: project_id or linked_phase missing", do not run skill, entry gets queue_failed at Step 8. (Already in B.1.)

### C.4 research-agent-run exception

- **Risk:** Skill throws (e.g. unhandled tool error, timeout).
- **Shield:** auto-roadmap and auto-eat-queue: document that if the skill throws, caller **catches**, logs to Errors.md (#research-failed, reason "exception" or "timeout"), returns empty paths (or for queue: append Watcher-Result failure, do not add to processed_success_ids). Proceed to deepen without research (or mark entry queue_failed). (Already in B.1 and B.2.)

### C.5 Params backward compatibility

- **Risk:** Old queue entries with research_tools: ["web","x","browse"] break or behave unexpectedly.
- **Shield:** Skill normalizes: "browse" → freecrawl, "x" → academic via web_search; ignore unknown tool names. (Already in B.4.)

---

## Part D — Files to touch (summary)


| File                                                                                                     | Change                                                                                                     |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [.cursor/skills/research-agent-run/SKILL.md](.cursor/skills/research-agent-run/SKILL.md)                 | v1 skill changes + Step 0 vault-failure non-blocking + params normalization (browse→freecrawl, x→academic) |
| [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc)                     | RESEARCH-AGENT: pre-dispatch project_id+linked_phase check; 0 notes → failure + Watcher-Result             |
| [.cursor/rules/context/auto-roadmap.mdc](.cursor/rules/context/auto-roadmap.mdc)                         | Pre-deepen: catch research-agent-run exception, log, return empty, proceed to deepen                       |
| [.cursor/skills/roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md)                         | Optional: note that empty/partial gap_fills → inject what exists, proceed                                  |
| [3-Resources/Second-Brain/MCP-Tools.md](3-Resources/Second-Brain/MCP-Tools.md)                           | v1 Research stack + FreeCrawl requirement                                                                  |
| [3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md)                         | v1 research_tools                                                                                          |
| [3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)                   | v1 research_tools mention                                                                                  |
| [3-Resources/Second-Brain/Skills.md](3-Resources/Second-Brain/Skills.md)                                 | v1 research-agent-run row                                                                                  |
| [3-Resources/Second-Brain/Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md)                     | research_tools_used values (new + legacy)                                                                  |
| [3-Resources/Second-Brain/Logs.md](3-Resources/Second-Brain/Logs.md)                                     | research_tools_used values                                                                                 |
| [3-Resources/Second-Brain/Mode-Success-Contracts.md](3-Resources/Second-Brain/Mode-Success-Contracts.md) | RESEARCH-AGENT: 0 notes → failure + queue_failed                                                           |
| .cursor/sync/*                                                                                           | Sync skill and both rules; changelog entry                                                                 |


---

## Verification (manual)

- Run RESEARCH-AGENT with valid project_id + linked_phase: vault Step 0 runs, web_search + FreeCrawl (or fallback) run, notes written, research_tools_used set, Watcher-Result success.
- Run RESEARCH-AGENT with missing project_id or linked_phase: entry skipped, Watcher-Result failure, entry written back with queue_failed: true.
- Run RESEARCH-AGENT with FreeCrawl disabled: fallback used, notes still written (or 0 if web_search fails); if 0 notes, Watcher-Result failure.
- RESUME-ROADMAP with enable_research: if research-agent-run throws, auto-roadmap catches, logs, proceeds to deepen without research.

