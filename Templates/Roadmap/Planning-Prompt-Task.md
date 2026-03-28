---
title: Planning prompt (task → Cursor-ready)
created: {{date}}
tags: [planning, roadmap, cursor]
---

# TASK-TO-PLAN-PROMPT template

Use this template when building the planning prompt for Cursor from a roadmap task. Fill placeholders at runtime (e.g. task-to-prompt skill or TASK-TO-PLAN-PROMPT handler). Merge **code_comments** from Second-Brain-Config when present.

---

You are in **planning mode** only — do not write code yet.

**Project:** {{project_name}}  
**Previous tasks completed in this session:** {{session_memory_hint}}

**Next task:**  
{{task_text}}

**Think step-by-step:**
1. How does this task fit with existing architecture / naming / error handling style?
2. Which files will need to change? (list)
3. Any new components / systems / resources required?
4. Trade-offs, risks, alternatives?
5. Clarifying questions for me before implementation?

When you later implement, **include liberal explanatory comments** in the code:
- Why this design choice was made here (especially if non-obvious)
- What assumptions this code relies on
- Known limitations or future-extension points ("TODO: later support dynamic resize")
- Links or references to relevant wrappers/decisions ("See [[Roadmap-Wrapper-Grid-Size-2026-03-07]] for approved fixed 20x20 rationale")
- Any gotchas or "don't touch this without checking X" warnings

Propose detailed plan + file change outline + **comment style guide** for this task.

---

**Placeholders:** `{{project_name}}`, `{{session_memory_hint}}` (from params.session_success_hint or Watcher-Result.md), `{{task_text}}` (from source_file + locator). Optional: `{{git_diff_hint}}` from params.git_diff_hint when building payload.
