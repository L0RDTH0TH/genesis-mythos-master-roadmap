---
approved: false
decision_candidate: true
wrapper_type: phase-direction
clunk_severity: medium
phase_path: {{phase_path}}
original_path: {{original_path}}
proposal_path: {{proposal_path}}
created: {{date}} {{time}}
re-wrap: false
re-try: false
# technical_by_option: { "A": "...", "B": "...", ... } — optional; store technical resolution per letter for provenance (creators must populate when creating wrapper)
---

> [!important] Safety invariant — Watcher never approves
> Watcher **only** syncs `approved_option` + `approved_path` when `approved: true` is **already set by the user**.
> Watcher **never** sets `approved: true` itself — that remains a manual user action (frontmatter edit or Commander macro).

> [!tip] How to approve this wrapper
> 1. Check **exactly one** option A–G (or R for re-try with guidance)
> 2. (optional) Add thoughts/guidance in the Thoughts callout
> 3. Set `approved: true` in frontmatter (or use Commander "Approve Wrapper" macro if set up)
> → Run **EAT-QUEUE** to apply (or re-queue with guidance if R)

# Phase direction: {{direction_question}}

**Phase:** {{phase_path}}

**Options** (conceptual end states — what the situation is after each choice; technical resolution is stored for provenance only):

- [ ] **A.** {{option_a}}

- [ ] **B.** {{option_b}}

- [ ] **C.** {{option_c}}

- [ ] **D.** {{option_d}}

- [ ] **E.** {{option_e}}

- [ ] **F.** {{option_f}}

- [ ] **G.** {{option_g}}

- [ ] **R.** Re-try with guidance — re-queue EXPAND-ROAD / TASK-TO-PLAN-PROMPT with my Thoughts (capped by re_try_max_loops).

**Your action — check ONE box above AND set frontmatter:**

`approved_option: A` (or B–G, or R for re-try)

OR custom: `approved_path: "exact/path/you-want.md"`  
OR reject / re-wrap: `approved_option: 0` or `re-wrap: true`

**Wrapper state** *(do not edit manually)*
<!-- CHECK_WRAPPERS: insert Wrapper state block above this line -->

**Thoughts / how will it be used?** (feeds user_guidance for re-try or downstream)
> 
> 
> 

> [!example]- Technical resolution (for reference)
> Optional: A: … ; B: … ; C: … ; D: … ; E: … ; F: … ; G: … (stored in frontmatter `technical_by_option` for provenance; creators populate when creating wrapper)

**After editing → run EAT-QUEUE.**
