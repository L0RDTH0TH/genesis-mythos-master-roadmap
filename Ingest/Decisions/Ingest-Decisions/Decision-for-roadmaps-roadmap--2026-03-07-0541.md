---
approved: false
decision_candidate: true
wrapper_type: ingest-decision
clunk_severity: medium
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-roadmaps-roadmap--2026-03-07-0541.md
original_note: [[Roadmaps Roadmap.md]]
original_path: Ingest/Roadmaps Roadmap.md
decision_priority: high
created: 2026-03-07 05:41
re-wrap: false
---

> [!important] Safety invariant — Watcher never approves
> Watcher **only** syncs `approved_option` + `approved_path` when `approved: true` is **already set by the user**.
> Watcher **never** sets `approved: true` itself — that remains a manual user action (frontmatter edit or Commander macro).

> [!tip] How to approve this wrapper
> 1. Check **exactly one** option A–G
> 2. (optional) Add thoughts/guidance in the Thoughts callout
> 3. Set `approved: true` in frontmatter (or use Commander "Approve Wrapper" macro if set up)
> → Watcher will auto-sync your choice → run **EAT-QUEUE** (or wait for auto-nudge) to apply

# Decision: Where should [[Roadmaps Roadmap.md]] go?

**Classifier top candidates** (ranked by confidence):

- [ ] **A.** 1-Projects/Roadmaps-Roadmap/Roadmaps Roadmap.md — 40%  
  ⚠ Potential new folder: Roadmaps-Roadmap

- [ ] **B.** 1-Projects/New/Roadmaps Roadmap.md — 40%  
  ⚠ Potential new folder: New

- [ ] **C.** 1-Projects/Test-Project/Roadmaps Roadmap.md — 40%  
  Under 1-Projects/Test-Project

- [ ] **D.** 1-Projects/Unfiled/Roadmaps Roadmap.md — 40%  
  ⚠ Potential new folder: Unfiled

- [ ] **E.** 1-Projects/Inbox/Roadmaps Roadmap.md — 40%  
  ⚠ Potential new folder: Inbox

- [ ] **F.** 1-Projects/Misc/Roadmaps Roadmap.md — 40%  
  ⚠ Potential new folder: Misc

- [ ] **G.** 1-Projects/Ideas/Roadmaps Roadmap.md — 40%  
  ⚠ Potential new folder: Ideas

**Your action — check ONE box above AND set ONE frontmatter line:**

Quick pick (recommended):  
`approved_option: A`    ← change to the letter you checked

OR custom/override path:  
`approved_path: "exact/path/you-want.md"`

OR reject all candidates (free guidance only):  
`approved_option: 0`

OR unhappy with all options — get a fresh wrapper with your Thoughts as seed:  
`re-wrap: true` (in frontmatter; then run EAT-QUEUE — Cursor archives this wrapper and creates a new one using Thoughts as seed)

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
