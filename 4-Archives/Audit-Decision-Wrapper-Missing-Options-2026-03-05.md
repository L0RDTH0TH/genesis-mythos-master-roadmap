---
title: Audit — Decision Wrapper missing options (fewer than 7)
created: 2026-03-05
tags: [audit, ingest, decision-wrapper, para]
para-type: Resource
status: done
---

# Audit: Why are wrappers created with missing options (fewer than 7)?

## Requirement

Every Decision Wrapper must present **exactly 7 options (A–G)** upon creation so the user always has a consistent, comparable set of choices. Template: `Templates/Decision-Wrapper.md` (A–G).

## Root cause

1. **MCP returns a variable number of candidates**  
   `propose_para_paths` (and its server wrapper) is called with `max_candidates: "7"` and `context_mode: "wrapper"`, but the **server returns only as many candidates as it discovers** (e.g. from existing folders, scoring, or internal limits). So the API often returns 1, 3, or 5 candidates—not 7—depending on vault structure and scoring.

2. **Rule allowed leaving slots unfilled**  
   In `.cursor/rules/context/para-zettel-autopilot.mdc`, the fill step said: *"map candidates[0]→A … candidates[6]→G; **leave unfilled if fewer than 7**"*. So the agent correctly followed the rule by writing "— —" for empty slots, producing wrappers with only 1–5 options filled.

3. **No padding step**  
   There was no requirement to **pad** the candidate list to 7 when the API returned fewer. So wrappers were created with missing B–G (or similar) whenever the proposal engine returned fewer than 7 paths.

## Fix (agent-side padding)

- **Rule change**: When creating or refreshing a Decision Wrapper, the agent must **always fill all 7 slots (A–G)**. If `candidates.length < 7`, **pad to 7** using deterministic fallback options (see para-zettel-autopilot.mdc § Decision Wrapper creation).
- **Fallback options** (used only for empty slots, in order, without duplicating already-listed paths):
  1. Direct under the **classified** PARA root: `{1-Projects|2-Areas|3-Resources|4-Archives}/<basename>.md`.
  2. Direct under the **other** PARA roots (one per slot), e.g. `2-Areas/<basename>.md`, `3-Resources/<basename>.md`, `4-Archives/<basename>.md`, `1-Projects/<basename>.md` (cycle as needed).
  3. Standard fallback folders: `3-Resources/Unfiled/<basename>.md`, `4-Archives/Ingest-YYYY-MM-DD/<basename>.md` (use current date for YYYY-MM-DD).
- Use a low display confidence for padded options (e.g. 5% or "—") and `reason_short` such as "Direct under [root]" or "Alternative: [PARA type]" so the user can tell they are fallbacks.
- **MCP/server**: Optionally, the proposal engine could be updated to always return 7 candidates in wrapper mode (e.g. by padding with low-score options). Until then, padding on the agent side is required.

## References

- [[.cursor/rules/context/para-zettel-autopilot.mdc]] — Decision Wrapper creation (updated to require 7 options + padding).
- [[3-Resources/Second-Brain/Pipelines]] — Phase 1 wrapper with A–G.
- [[3-Resources/Second-Brain/MCP-Tools]] — propose_para_paths returns variable-length `candidates`.
