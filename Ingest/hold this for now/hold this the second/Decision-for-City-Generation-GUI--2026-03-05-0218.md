---
approved: false
decision_candidate: true
wrapper_type: ingest-decision
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-City-Generation-GUI--2026-03-05-0218.md
original_note: [[City Generation GUI.md]]
original_path: Ingest/City Generation GUI.md
decision_priority: high
created: 2026-03-05 02:18
re-wrap: false
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

# Decision: Where should [[City Generation GUI]] go?

**Classifier top candidates** (ranked by confidence):

- [ ] **A.** 3-Resources/City Generation GUI.md — 40%  
  Direct under PARA root

- [ ] **B.** 1-Projects/City Generation GUI.md — 5%  
  Direct under 1-Projects

- [ ] **C.** 2-Areas/City Generation GUI.md — 5%  
  Direct under 2-Areas

- [ ] **D.** 4-Archives/City Generation GUI.md — 5%  
  Direct under 4-Archives

- [ ] **E.** 3-Resources/Unfiled/City Generation GUI.md — 5%  
  3-Resources/Unfiled

- [ ] **F.** 4-Archives/Ingest-2026-03-05/City Generation GUI.md — 5%  
  4-Archives/Ingest-YYYY-MM-DD

- [ ] **G.** 2-Areas/Unfiled/City Generation GUI.md — 5%  
  Alternative fallback

**Your action — check ONE box above AND set ONE frontmatter line:**

Quick pick (recommended):  
`approved_option: A`    ← change to the letter you checked

OR custom/override path:  
`approved_path: "exact/path/you-want.md"`

OR reject all candidates (free guidance only):  
`approved_option: 0`

**Wrapper state** *(do not edit manually; set by EAT-QUEUE when wrapper is orphaned or not archived)*
<!-- CHECK_WRAPPERS: insert Wrapper state block above this line -->

**Thoughts / corrections / why this location?**  
(This becomes `user_guidance` — be as specific or corrective as you like)

> 
> 
> 

**After editing → run EAT-QUEUE** (or use Commander macro "Process Queue").

```dataview
TABLE WITHOUT ID file.link AS "Pending decision", decision_priority, approved_option, approved_path
FROM "Ingest/Decisions"
WHERE decision_candidate = true AND approved = false
SORT decision_priority DESC, file.ctime DESC
```

```dataview
TABLE WITHOUT ID file.link AS "Recent decision (pending)", decision_priority, approved_option, approved_path, used_at
FROM "Ingest/Decisions"
WHERE approved = true
SORT used_at DESC, file.ctime DESC
```

```dataview
TABLE WITHOUT ID file.link AS "Applied (archived)", decision_priority, approved_option, approved_path, used_at
FROM "4-Archives/Ingest-Decisions"
SORT used_at DESC, file.ctime DESC
```
