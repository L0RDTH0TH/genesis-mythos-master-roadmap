---
approved: true
decision_candidate: true
proposal_path: Ingest/Decisions/cascade-branches-2026-03-03-2305.md
original_note: 
original_path: Ingest/Cascade Branches.md
decision_priority: high
created: "2026-03-03 23:05"
used_at: "2026-03-03T23:06:15Z"
processed: true
---
# Decision: Where should [[Cascade Branches]] go?

**Classifier top candidates** (ranked by confidence):

- [x] **A.** 4-Archives/Genesis/Cascade Branches.md — 70%  [completion:: 2026-03-03]
  Under 4-Archives/Genesis; treat as archived Cascade implementation spec.

- [ ] **B.** 4-Archives/Ingest-2026-03-01/Cascade Branches.md — 70%  
  Under 4-Archives/Ingest-2026-03-01; generic ingest archive.

- [ ] **C.** 4-Archives/Pre-Archive-Root-Cleanup/Cascade Branches.md — 70%  
  Under 4-Archives/Pre-Archive-Root-Cleanup.

- [ ] **D.** 3-Resources/Game-Dev/Godot/Cascade Branches.md — 65%  
  Use if you treat this as **active** implementation reference (evergreen Resource).

- [ ] **E.** 2-Areas/Genesis-Mythos/UI/Cascade Branches.md — 60%  
  Use if this is ongoing area work for Cascade wedge/branch UI.

**Your action — check ONE box above AND set ONE frontmatter line:**

Quick pick (recommended):  
`approved_option: A`

OR custom/override path:  
`approved_path: "exact/path/you-want.md"`

OR reject all candidates (free guidance only):  
`approved_option: 0`

**Thoughts / corrections / why this location?**  
(This becomes `user_guidance` — be as specific or corrective as you like)

> This is a depricated spec for the cascade branch UI
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
