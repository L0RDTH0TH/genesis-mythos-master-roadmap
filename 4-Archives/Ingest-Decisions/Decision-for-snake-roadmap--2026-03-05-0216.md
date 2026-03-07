---
approved: true
decision_candidate: true
proposal_path: Ingest/Decisions/Decision-for-snake-roadmap--2026-03-05-0216.md
original_note:
  - - snake-roadmap.md
original_path: Ingest/snake-roadmap.md
decision_priority: high
approved_option: A
used_at: 2026-03-05 02:20
processed: true
wrapper_type: roadmap
suggested_project_name: Retro Snake Game
created: 2026-03-05 02:16
---

# Decision: Where should [[snake-roadmap.md]] go?

**Classifier top candidates** (ranked by confidence):

- [x] **A.** 1-Projects/Retro Snake Game/Roadmap/ — 90%  [completion:: 2026-03-05]
  New project + full roadmap tree (master + phase notes + MOC) generated from this roadmap seed.

- [ ] **B.** 1-Projects/Retro Snake Game/Retro Snake Game Roadmap.md — 75%  
  Single roadmap note at the project root, no separate phase notes yet.

- [ ] **C.** 1-Projects/Game Prototypes/Retro Snake Game Roadmap.md — 60%  
  Under a generic game prototypes project container.

- [ ] **D.** 2-Areas/Game Design/Roadmaps/Retro Snake Game Roadmap.md — 20%  
  Ongoing area for multiple game design roadmaps.

- [ ] **E.** 3-Resources/Game Design/Roadmaps/Retro Snake Game Roadmap.md — 20%  
  Reference roadmap under Resources.

- [ ] **F.** 3-Resources/Unfiled/Retro Snake Game Roadmap.md — 5%  
  Catch-all resource location for later organization.

- [ ] **G.** 4-Archives/Ingest-2026-03-05/Retro Snake Game Roadmap.md — 5%  
  Archive this capture for historical reference.

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
