---
name: User Questions and Options Reference
overview: Create a single reference document under 3-Resources/Second-Brain that lists every user-facing question and its options in the order they are presented, then save it to Second Brain resources.
todos: []
isProject: false
---

# User Questions and Options Reference Document

## Goal

Produce one canonical document in **3-Resources/Second-Brain** that lists all questions and options shown to users, in presentation order. No code or rule changes—only adding this reference and optionally linking it from existing docs (e.g. README or Backbone).

---

## Source of truth (already in vault)

- **Plan-mode Prompt Crafter (order and params):** [Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md) — `question_order` per kickoff/sub-mode.
- **Plan-mode flow and A/B/C pattern:** [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) — kickoff, branch, optionals, manual text, append confirm.
- **Decision Wrapper options:** [User-Flow-Rules-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Rules-Detailed.md), [Templates/Decision-Wrapper.md](Templates/Decision-Wrapper.md) — A–G, 0, R, re-wrap.
- **Roadmap-next-step and cap-hit:** [Parameters.md](3-Resources/Second-Brain/Parameters.md), [Cursor-Skill-Pipelines-Reference.md](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) — roadmap-next-step A–G/0 mapping; cap-hit A/B/0.
- **Commander Craft Prompt:** [User-Flow-Prompt-Crafter-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Detailed.md) — pipeline/profile and Preview vs Craft and Queue.

---

## Document to create

**Path:** `3-Resources/Second-Brain/User-Questions-and-Options-Reference.md`

**Structure:**

1. **Frontmatter and intro**
  Title, created, tags (`pkm`, `second-brain`, `user-flow`, `reference`), `para-type: Resource`, links to Prompt-Crafter-Param-Table, User-Flow-Rules-Detailed, Prompt-Crafter-Structure-Detailed. One short paragraph: this doc lists every user-facing question and options in presentation order.
2. **Plan-mode Prompt Crafter (Cursor Plan mode)**
  - **When:** User says “We are making a prompt” (or CODE/ROADMAP).  
  - **Order of questions:**
    - **Q0 (only if kickoff unclear):** “Which kind?”  
      - **Options:** A. CODE | B. ROADMAP
    - **Then by branch:**
      - **CODE:** Ask pipeline/mode (e.g. INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, or task modes per Queue-Alias-Table). Then param questions **in question_order** from [Prompt-Crafter-Param-Table](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md) for the chosen sub-mode. For **ROADMAP:** Ask “ROADMAP MODE vs RESUME-ROADMAP”; for RESUME-ROADMAP optionally “Which action?” (deepen, recal, revert-phase, sync-outputs, handoff-audit, etc.) then param questions in question_order.
    - **Per-param question (one per message):** Each optional param is asked with “It does …” and **options:** A. yes / include (or first concrete option) | B. no / exclude (or second) | C. let AI decide.  
    - **Manual text phase:** For each param with `accepts_manual_text: true` that was included, ask “What is the [param name]?” (free text).  
    - **Final:** “Append to queue?”  
      - **Options:** Y | n
       **Param order by branch (cite Param Table):**
  - **ROADMAP MODE:** 1. project_id, 2. source_file / seed note path (manual text).
  - **RESUME-ROADMAP:** 1. action, 2. project_id, 3. phase, 4. sectionOrTaskLocator (manual), 5. enable_context_tracking, 6. enable_research, 7. research_queries (manual), 8. async_research, 9. research_distill, 10. handoff_gate, 11. min_handoff_conf, 12. inject_extra_state, 13. token_cap, 14. max_depth, 15. branch_factor, 16. profile, 17. userText (manual), 18. queue_next.
  - **CODE → INGEST:** 1. source_file (manual), 2. context_mode, 3. max_candidates, 4. profile, 5. user_guidance/prompt (manual), 6. rationale_style.
  - **CODE → ORGANIZE:** 1. source_file (manual), 2. context_mode, 3. max_candidates, 4. profile, 5. user_guidance/prompt (manual).
  - **CODE → DISTILL:** 1. source_file (manual), 2. distill_lens (manual), 3. depth/layers.
  - **CODE → EXPRESS:** 1. source_file (manual), 2. express_view (manual).
  - **CODE → ARCHIVE:** 1. source_file (manual).
  - **CODE → Task modes:** 1. source_file (manual), 2. task_id (manual, TASK-COMPLETE), 3. prompt (manual), 4. sectionOrTaskLocator (manual), 5. userText (manual).
3. **Decision Wrappers (ingest, phase-direction, refinements, low-confidence, error)**
  - **Options (in order):**  
    - **A, B, C, D, E, F, G** — ranked PARA paths (or conceptual end-states for phase-direction); content varies per wrapper.  
    - **0** — Reject all.  
    - **R** — Re-try with guidance (roadmap/phase-direction wrappers only); runs re-try branch (re-queue with guidance; capped by re_try_max_loops).  
    - **re-wrap: true** (frontmatter) — Unhappy with options; archive wrapper and create new one with Thoughts as seed.
  - **User action:** Check one of A–G (or 0 or R) and set `approved: true`; then EAT-QUEUE applies path or re-wrap/re-try.
4. **Cap-hit wrapper (re-try cap exceeded)**
  - **Options:** A. Force approve | B. Prune branch | 0. Re-wrap full phase.
5. **Roadmap-next-step wrapper**
  - **Options (letter → action):** A = deepen, B = recal, C = advance-phase, D = raise cap and continue, E = revert-phase, F = sync-outputs then deepen, 0 = re-wrap.  
  - (Wrapper body includes “Why uncertain” rationale callout.)
6. **Commander “Craft Prompt” macro**
  - **Question 1:** Pipeline — **Options:** ingest | organize.  
  - **Question 2:** Profile — **Options:** default | project-priority.  
  - **Then:** **Options:** Preview Assembly (no queue append) | Craft and Queue (validate and append one line to prompt-queue.jsonl).
7. **Cross-references**
  - Link to Prompt-Crafter-Param-Table, Prompt-Crafter-Structure-Detailed, User-Flow-Rules-Detailed, User-Flow-Prompt-Crafter-Detailed, Parameters (roadmap-next-step, cap-hit), Cursor-Skill-Pipelines-Reference (apply-from-wrapper table), Queue-Alias-Table, Decision-Wrapper template.

---

## Optional follow-up

- Add a one-line mention and link to this doc in [3-Resources/Second-Brain/README](3-Resources/Second-Brain/README.md) or [Backbone](3-Resources/Second-Brain/Backbone.md) under “User flows” or “References” so it’s discoverable.
- If backbone-docs-sync applies to new Second-Brain docs, add an entry to `.cursor/sync/changelog.md` for the new reference (optional).

---

## Out of scope

- No changes to rules, skills, or Param Table.
- No new templates; Decision Wrapper stays as-is.
- No implementation of new questions or options—documentation only.

