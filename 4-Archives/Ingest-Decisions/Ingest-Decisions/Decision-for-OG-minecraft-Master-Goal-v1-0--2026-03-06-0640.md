---
approved: true
decision_candidate: true
wrapper_type: ingest-decision
clunk_severity: medium
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-OG-minecraft-Master-Goal-v1-0--2026-03-06-0640.md
original_note: 
original_path: Ingest/OG-minecraft-Master Goal v1.0.md
decision_priority: high
created: "2026-03-06 06:40"
re-wrap: false
approved_option: A
approved_path: 1-Projects/OG-minecraft/minecraft-beta-clone-master-goal-2026-03-06-0640.md
used_at: "2026-03-06T06:45:00Z"
processed: true
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

# Decision: Where should [[OG-minecraft-Master Goal v1.0]] go?

**Classifier top candidates** (ranked by confidence):

- [x] **A.** 1-Projects/OG-minecraft/minecraft-beta-clone-master-goal-2026-03-06-0640.md — 85%  [completion:: 2026-03-06]
  New project folder for this Master Goal (recommended).

- [ ] **B.** 1-Projects/Test-Project/OG-minecraft-Master Goal v1.0.md — 27%  
  Under 1-Projects/Test-Project

- [ ] **C.** 1-Projects/Pong-Game/OG-minecraft-Master Goal v1.0.md — 19%  
  Under 1-Projects/Pong-Game

- [ ] **D.** 1-Projects/Retro Snake Game/OG-minecraft-Master Goal v1.0.md — 16%  
  Under 1-Projects/Retro Snake Game

- [ ] **E.** 1-Projects/Genesis-Mythos/OG-minecraft-Master Goal v1.0.md — 12%  
  Under 1-Projects/Genesis-Mythos

- [ ] **F.** 1-Projects/Example/OG-minecraft-Master Goal v1.0.md — 7%  
  Under 1-Projects/Example

- [ ] **G.** 3-Resources/OG-minecraft/Minecraft-Beta-Clone-Master-Goal-2026-03-06.md — 5%  
  As Resource (evergreen reference) if not treated as project.

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
