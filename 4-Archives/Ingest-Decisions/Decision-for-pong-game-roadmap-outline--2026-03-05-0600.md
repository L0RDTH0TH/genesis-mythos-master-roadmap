---
approved: true
decision_candidate: true
proposal_path: Ingest/Decisions/Decision-for-pong-game-roadmap-outline--2026-03-05-0600.md
original_note: 
original_path: Ingest/Pong Game Roadmap Outline.md
decision_priority: high
created: "2026-03-05 06:00"
wrapper_type: roadmap
suggested_project_name: Pong-Game
used_at: "2026-03-05T06:15:00Z"
processed: true
---
# Decision: Where should [[Pong Game Roadmap Outline]] go?

**Classifier top candidates** (ranked by confidence):

- [x] **A.** New project + full roadmap tree — 90%  [completion:: 2026-03-05]
  Create new project (Pong-Game) and decompose this outline into master roadmap, phase notes, and MOC at `1-Projects/Pong-Game/Roadmap/`.

- [ ] **B.** 1-Projects/Test-Project/Pong Game Roadmap Outline.md — 40%  
  Under 1-Projects/Test-Project

- [ ] **C.** 1-Projects/Genesis-Mythos/Pong Game Roadmap Outline.md — 40%  
  Under 1-Projects/Genesis-Mythos

- [ ] **D.** 1-Projects/Example/Pong Game Roadmap Outline.md — 40%  
  Under 1-Projects/Example

- [ ] **E.** 1-Projects/Pong-Game/Pong Game Roadmap Outline.md — 5%  
  Direct under project root

- [ ] **F.** 3-Resources/Unfiled/Pong Game Roadmap Outline.md — 5%  
  Direct under 3-Resources/Unfiled

- [ ] **G.** 4-Archives/Ingest-2026-03-05/Pong Game Roadmap Outline.md — 5%  
  Archive under Ingest-2026-03-05

**Your action — check ONE box above AND set ONE frontmatter line:**

Quick pick (recommended):  
`approved_option: A`    ← change to the letter you checked (A = new Pong-Game project + full roadmap tree)

OR custom/override path:  
`approved_path: "exact/path/you-want.md"`

OR reject all candidates (free guidance only):  
`approved_option: 0`

**Wrapper state** *(do not edit manually; set by EAT-QUEUE when wrapper is orphaned or not archived)*
<!-- CHECK_WRAPPERS: insert Wrapper state block above this line -->

**Thoughts / corrections / why this location?**  
(This becomes `user_guidance` — be as specific or corrective as you like)

> Its basic but set up in a clear phase/step like list.
> The source file has Roadmap in the name.
> Pong is a historic game.
> There are no references to pong projects already.
> The file content references "High-Level Systems" which is *exactly* what road maps are for.

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
