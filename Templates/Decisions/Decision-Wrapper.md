---
approved: false
decision_candidate: true
wrapper_type: ingest-decision                        # ingest-decision | roadmap-decision | phase-direction | mid-band-refinement | low-confidence | error | force-wrapper
clunk_severity: medium                                # low | medium | high (inferred from band + error type at creation)
proposal_path: {{proposal_path}}                     # full path where this wrapper itself lives
original_note: [[{{original_filename}}]]
original_path: {{original_path}}                      # full path of the note being decided
decision_priority: high                               # high / medium / low
created: {{date}} {{time}}
re-wrap: false                                    # manual only — set true when unhappy with A–G options; run EAT-QUEUE → Cursor archives this wrapper and creates a new one with Thoughts as seed
re-try: false                                     # manual only — set true (or check option R) to re-queue EXPAND-ROAD or TASK-TO-PLAN-PROMPT with guidance; Step 0 appends queue entry and archives wrapper (capped by re_try_max_loops)
---

> [!important] Safety invariant — Watcher never approves
> Watcher **only** syncs `approved_option` + `approved_path` when `approved: true` is **already set by the user**.
> Watcher **never** sets `approved: true` itself — that remains a manual user action (frontmatter edit or Commander macro).
> This prevents accidental auto-approval loops even if Watcher logic evolves later.

> [!tip] How to approve this wrapper
> 1. Check **exactly one** option A–G
> 2. (optional) Add thoughts/guidance in the Thoughts callout
> 3. Set `approved: true` in frontmatter (or use Commander "Approve Wrapper" macro if set up)
> → Watcher will auto-sync your choice → run **EAT-QUEUE** (or wait for auto-nudge) to apply

# Decision: Where should [[{{original_filename}}]] go?

**Classifier top candidates** (ranked by confidence):

- [ ] **A.** {{candidate_a_path}} — {{candidate_a_conf}}%  
  {{candidate_a_reason}}

- [ ] **B.** {{candidate_b_path}} — {{candidate_b_conf}}%  
  {{candidate_b_reason}}

- [ ] **C.** {{candidate_c_path}} — {{candidate_c_conf}}%  
  {{candidate_c_reason}}

- [ ] **D.** {{candidate_d_path}} — {{candidate_d_conf}}%  
  {{candidate_d_reason}}

- [ ] **E.** {{candidate_e_path}} — {{candidate_e_conf}}%  
  {{candidate_e_reason}}

- [ ] **F.** {{candidate_f_path}} — {{candidate_f_conf}}%  
  {{candidate_f_reason}}

- [ ] **G.** {{candidate_g_path}} — {{candidate_g_conf}}%  
  {{candidate_g_reason}}

**Your action — check ONE box above AND set ONE frontmatter line:**

Quick pick (recommended):  
`approved_option: A`    ← change to the letter you checked

OR custom/override path:  
`approved_path: "exact/path/you-want.md"`

OR reject all candidates (free guidance only):  
`approved_option: 0`

OR unhappy with all options — get a fresh wrapper with your Thoughts as seed:  
`re-wrap: true` (in frontmatter; then run EAT-QUEUE — Cursor archives this wrapper and creates a new one using Thoughts as seed)

OR re-try with guidance (re-queue EXPAND-ROAD or TASK-TO-PLAN-PROMPT with your Thoughts):  
Check **R** above or set `re-try: true` in frontmatter; run EAT-QUEUE — Cursor appends a queue entry with your guidance and archives this wrapper (capped by re_try_max_loops; on cap hit a cap-hit wrapper is created).

**Wrapper state** *(do not edit manually; set by EAT-QUEUE when wrapper is orphaned or not archived)*
<!-- CHECK_WRAPPERS: insert Wrapper state block above this line -->

**Thoughts / corrections / why this location?**  
(This becomes `user_guidance` — be as specific or corrective as you like)

> 
> 
> 

**After editing → run EAT-QUEUE** (or use Commander macro "Process Queue").

```dataview
TABLE WITHOUT ID file.link AS "Pending decision", decision_priority, clunk_severity, wrapper_type, approved_option, approved_path
FROM "Ingest/Decisions"
WHERE decision_candidate = true AND approved = false
  AND (file.folder = "Ingest/Decisions/Ingest-Decisions" OR file.folder = "Ingest/Decisions/Roadmap-Decisions" OR file.folder = "Ingest/Decisions/Refinements" OR file.folder = "Ingest/Decisions/Low-Confidence" OR file.folder = "Ingest/Decisions/Errors")
SORT clunk_severity DESC, decision_priority DESC, file.ctime DESC
```

```dataview
TABLE WITHOUT ID file.link AS "Recent decision (pending)", decision_priority, clunk_severity, wrapper_type, approved_option, approved_path, used_at
FROM "Ingest/Decisions"
WHERE approved = true
  AND (file.folder = "Ingest/Decisions/Ingest-Decisions" OR file.folder = "Ingest/Decisions/Roadmap-Decisions" OR file.folder = "Ingest/Decisions/Refinements" OR file.folder = "Ingest/Decisions/Low-Confidence" OR file.folder = "Ingest/Decisions/Errors")
SORT used_at DESC, file.ctime DESC
```

```dataview
TABLE WITHOUT ID file.link AS "Applied (archived)", decision_priority, approved_option, approved_path, used_at
FROM "4-Archives/Ingest-Decisions"
SORT used_at DESC, file.ctime DESC
```