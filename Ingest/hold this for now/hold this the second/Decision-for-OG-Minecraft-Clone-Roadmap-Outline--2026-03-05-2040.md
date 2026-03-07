---
approved: false
decision_candidate: true
wrapper_type: roadmap
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-OG-Minecraft-Clone-Roadmap-Outline--2026-03-05-2040.md
original_note: [[minecraft-beta.md]]
original_path: Ingest/minecraft-beta.md
decision_priority: high
created: 2026-03-05 20:40
re-wrap: false
suggested_project_name: OG Minecraft Clone
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

**Archived previous:** [[4-Archives/Ingest-Decisions/Re-Wrap/Ingest-Decisions/Decision-for-OG-Minecraft-Clone-Roadmap-Outline--2026-03-05-0935.md]]

# Decision: Where should [[minecraft-beta.md]] go?

**Re-wrap seed:** *This is a project but I want a complete roadmap run for it not just a simple move to project.*

**Classifier top candidates** (ranked by confidence):

- [ ] **A.** 1-Projects/OG-Minecraft-Clone/Roadmap/ — New project + full roadmap tree
  Create new project and decompose into master + phase notes + MOC (full roadmap run).

- [ ] **B.** 1-Projects/OG Minecraft Clone Roadmap Outline.md — 65%
  Treat as active project; simple move.

- [ ] **C.** 4-Archives/Pre-Archive-Root-Cleanup/minecraft-beta.md — 37%
  Under 4-Archives/Pre-Archive-Root-Cleanup

- [ ] **D.** 4-Archives/Ingest-2026-03-01/minecraft-beta.md — 32%
  Under 4-Archives/Ingest-2026-03-01

- [ ] **E.** 3-Resources/Game-Design/OG Minecraft Clone Outline.md — 45%
  Treat as reference design doc if you only need it as evergreen resource.

- [ ] **F.** 2-Areas/minecraft-beta.md — 5%
  Direct under 2-Areas

- [ ] **G.** 4-Archives/Ingest-2026-03-05/minecraft-beta.md — 5%
  4-Archives/Ingest-YYYY-MM-DD

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

> This is a project but I want a complete roadmap run for it not just a simple move to project.
> 
> 

**After editing → run EAT-QUEUE** (or use Commander macro "Process Queue").

```dataview
TABLE WITHOUT ID file.link AS "Pending decision", decision_priority, approved_option, approved_path
FROM "Ingest/Decisions"
WHERE decision_candidate = true AND approved = false
  AND (file.folder = "Ingest/Decisions/Ingest-Decisions" OR file.folder = "Ingest/Decisions/Roadmap-Decisions")
SORT decision_priority DESC, file.ctime DESC
```

```dataview
TABLE WITHOUT ID file.link AS "Recent decision (pending)", decision_priority, approved_option, approved_path, used_at
FROM "Ingest/Decisions"
WHERE approved = true
  AND (file.folder = "Ingest/Decisions/Ingest-Decisions" OR file.folder = "Ingest/Decisions/Roadmap-Decisions")
SORT used_at DESC, file.ctime DESC
```

```dataview
TABLE WITHOUT ID file.link AS "Applied (archived)", decision_priority, approved_option, approved_path, used_at
FROM "4-Archives/Ingest-Decisions"
SORT used_at DESC, file.ctime DESC
```
