---
title: PARA Actionability Rubric v1.0
created: 2026-03-06
tags: [pkm, second-brain, para, rubric]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Second-Brain-Summary]]"]
---

# PARA Actionability Rubric v1.0 (2026-03-06)

Rank and classify strictly by **actionability priority**:

- **Projects** (highest): Time-bound goals with clear deadlines, deliverables, or clear ownership/assignment. Examples: launch a feature by a date, finish taxes, ship a report, plan a specific event.
- **Areas**: Ongoing responsibilities, habits, standards, or maintenance with **no defined end date**. Examples: health and fitness, finances, marketing, hiring, home maintenance.
- **Resources**: Evergreen reference material, how-to guides, topic collections, research, or snippets with **no implied action or deadline**. Examples: language-learning tips, CSS grid patterns, reading notes.
- **Archives** (lowest): Completed, inactive, obsolete, or historical items from any other PARA category. Examples: finished project notes, deprecated docs, past-year OKRs.

## Tie-breaker rule

When two PARA categories are plausible for a note, always favor the **more actionable** one:

- Projects > Areas > Resources > Archives

In practice:

- If there is **any clear goal, deadline, or endpoint**, treat the note as a **Project**.
- If it is about **maintaining a standard over time** (without a finish line), treat it as an **Area**.
- Only choose **Resource** when the note is **pure reference**: no tasks, no deadlines, no ongoing responsibility implied.
- Use **Archive** only when the content clearly refers to **completed** or **inactive** work.

Never default to **Resources** just because the note contains information. Prefer Projects or Areas whenever there is any hint of action, responsibility, or time-bounded work.

## Examples

Use these example patterns in tool prompts and descriptors:

1. `"Finish landing page by Friday; tasks: copy, design, dev"`  
   → **Projects** (clear deadline + concrete deliverables).

2. `"Weekly workout log, diet tracking, progress photos"`  
   → **Areas** (ongoing responsibility, no defined end).

3. `"CSS Grid layout patterns, code snippets, articles"`  
   → **Resources** (evergreen reference, no specific action attached).

4. `"2025 OKR tracking – all objectives met Dec 2025"`  
   → **Archives** (completed project/goal, no further action).

## Usage in tools and pipelines

- All PARA-related tools (e.g. `obsidian_classify_para`, `obsidian_propose_para_paths`, `propose_alternative_paths`) **must follow this rubric exactly**, including the tie-breaker rule.
- When multiple PARA types are plausible, tools and pipelines should:
  - Prefer **Projects** when there is any concrete goal or deadline.
  - Prefer **Areas** when the note describes a responsibility or standard without a clear end date.
  - Use **Resources** only when the note is clearly reference-only.
  - Use **Archives** only for completed/inactive items.
- When proposing ranked PARA paths, always **rank candidates in descending order of actionability** (Projects first, then Areas, then Resources, then Archives), then by fit within that category.

This rubric is the **single source of truth** for PARA decisions in the Second Brain automation stack. Update this note when you refine PARA criteria; MCP tool descriptors and rules should point here rather than duplicating the full text.

