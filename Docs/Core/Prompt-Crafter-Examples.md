---
title: Prompt-Crafter Plan-Mode Examples
created: 2026-03-10
tags: [pkm, second-brain, prompt-crafter, plan-mode, examples]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Prompt-Crafter-Structure-Detailed]]", "[[Prompt-Crafter-Param-Table]]", "[[Chat-Prompts]]"]
---

# Prompt-Crafter Plan-Mode Examples

Transcript-style examples for Plan-mode crafting with two kickoffs (CODE, ROADMAP), A/B/C options with "It does …", and the manual text phase. **Option semantics (per User-Questions-and-Options-Reference §1):** **A** = explicit value (include param with chosen value); **B** = default (omit key → Config/MCP default); **C** = AI reasoning (omit key + append short reasoning to user_guidance). Use these to validate agent behavior and fixture expectations.

**Format:** Each question is shown with options on **separate lines** and no second question or "Next I'll ask" in the same message; this format helps Cursor show the question box.

---

## Example 1: CODE → INGEST MODE (with user_guidance, C for project)

**User:** We are making a CODE prompt.

**Agent:** Which kind?

**A.** CODE (pipelines: ingest, organize, distill, express, archive, task modes)

**B.** ROADMAP (setup or resume roadmap)

**User:** A.

**Agent:** Which pipeline or task mode? INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, or task modes (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, …).

**User:** INGEST MODE.

**Agent:** Include source_file / target note? **It does:** path to the note to process (e.g. Ingest/My-Note.md).

**A.** I'll specify

**B.** use default / infer

**C.** let AI decide

**User:** A.

**Agent:** Include context_mode? **It does:** controls how strict PARA classification is (e.g. strict-para for ingest).

**A.** strict-para (explicit)

**B.** default (omit key)

**C.** AI reasoning (omit + suggest)

**User:** B.

**Agent:** Include user_guidance? **It does:** free-text hint for classification and path (e.g. "Prefer subfolder under 1-Projects for time-bound content").

**A.** yes (I'll provide text)

**B.** no / skip

**C.** AI reasoning (suggest starter guidance)

**User:** A.

**Agent:** What is the user_guidance? [text input]

**User:** Prefer subfolders under 1-Projects for time-bound content; explain rankings.

**Agent:** [Summary] Params: source_file (to be filled), context_mode: default (omitted), user_guidance: "Prefer subfolders under 1-Projects for time-bound content; explain rankings." Final: **A.** yes — append to queue | **B.** no — cancel | **C.** AI double-check (see User-Questions-and-Options-Reference §1 Message 9).

**User:** A.

**Agent:** [Emits JSONL] `{"mode":"INGEST MODE","source_file":"Ingest/My-Note.md","id":"req-1","params":{"user_guidance":"Prefer subfolders under 1-Projects for time-bound content; explain rankings."}}`

---

## Example 2: ROADMAP → RESUME-ROADMAP deepen (research + one C)

**User:** We are making a ROADMAP prompt.

**Agent:** Setup or continue?

**A.** ROADMAP MODE (setup only)

**B.** RESUME-ROADMAP (continue: deepen, recal, revert-phase, …)

**User:** B.

**Agent:** Which action? **It does:** deepen = one more deepen step; recal = audit and optionally revert; Other = revert-phase, sync-outputs, handoff-audit, expand, advance-phase, etc. (if C, ask again with A/B/C).

**A.** deepen

**B.** recal

**C.** Other

**User:** A.

**Agent:** Include project_id? **It does:** target project folder (e.g. 1-Projects/my-project).

**A.** I'll specify

**B.** use current / infer

**C.** let AI decide

**User:** C.

**Agent:** Include phase? **It does:** which roadmap phase to deepen (e.g. 1, 2, or current).

**A.** I'll specify

**B.** use current

**C.** let AI decide

**User:** B.

**Agent:** Include sectionOrTaskLocator? **It does:** target section or task within the phase (manual text).

**A.** yes (I'll specify)

**B.** default (omit key)

**C.** AI reasoning (omit + suggest)

**User:** B.

**Agent:** Include enable_context_tracking? **It does:** write context util and token metrics to workflow_state.

**A.** yes (explicit on)

**B.** default (omit key)

**C.** AI reasoning (omit + suggest)

**User:** A.

**Agent:** Include enable_research? **It does:** run external research before deepen and inject results; can fill gaps when util is low.

**A.** yes (explicit on)

**B.** default (omit key)

**C.** AI reasoning (omit + suggest)

**User:** A.

**Agent:** Include research_queries? **It does:** explicit search queries for research-agent-run.

**A.** yes (I'll provide)

**B.** default (omit key)

**C.** AI reasoning (omit + suggest)

**User:** A.

**Agent:** Include profile (e.g. deepen-aggressive)? **It does:** applies token_cap, branch_factor, inject_extra_state for high-util runs.

**A.** yes (e.g. deepen-aggressive)

**B.** default (omit key)

**C.** AI reasoning (omit + suggest)

**User:** C.

**Agent:** What is the research_queries? (comma or newline separated)

**User:** procedural generation best practices, narrative consistency in branching

**Agent:** [Summary] action: deepen, enable_research: true, profile: deepen-aggressive (AI decided), research_queries: ["procedural generation best practices", "narrative consistency in branching"]. Final: **A.** yes — append | **B.** no — cancel | **C.** AI double-check (§1 Message 9).

**User:** Y.

**Agent:** [Emits JSONL] `{"mode":"RESUME-ROADMAP","source_file":"1-Projects/my-project/Roadmap/workflow_state.md","id":"req-2","params":{"action":"deepen","enable_research":true,"profile":"deepen-aggressive","research_queries":["procedural generation best practices","narrative consistency in branching"]}}`

---

## C resolution rules

- **When to resolve C:** After all A/B/C questions are answered; agent runs a single pass over every param where user chose C.
- **Inputs:** Config defaults (prompt_defaults, prompt_defaults.roadmap), current file path, roadmap state (workflow_state, roadmap-state) when available, and already-selected params.
- **Output:** Set the param to a concrete value (or omit if optional and no clear inference). Document in Prompt-Log or merge_trace when C was used (e.g. `profile: deepen-aggressive (C resolved from context)`).

---

## Fixtures and validation

For given A/B/C answers (and manual text when applicable), the resolved payload should match the shape expected by Queue-Sources and Parameters. Tests can assert:

- Required fields present (mode, id; source_file or project_id where required).
- Params validate against MCP-Tools and allowed enums (e.g. rationale_style, context_mode, action).
- C-resolved params are within allowed values (e.g. profile one of known profiles).
- accepts_manual_text params that were included have a non-empty value after manual text phase.

See [[3-Resources/Second-Brain/Testing#Fixtures|Testing § Fixtures]] (prompt-crafter subdir) and [[3-Resources/Second-Brain/Prompt-Crafter-Param-Table|Prompt-Crafter-Param-Table]].
