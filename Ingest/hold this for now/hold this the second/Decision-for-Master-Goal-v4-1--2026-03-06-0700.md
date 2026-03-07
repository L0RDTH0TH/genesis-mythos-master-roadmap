---
approved: false
decision_candidate: true
wrapper_type: ingest-decision
clunk_severity: medium
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-Master-Goal-v4-1--2026-03-06-0700.md
original_note: [[Master Goal v4.1]]
original_path: Ingest/Master Goal v4.1.md
decision_priority: high
created: 2026-03-06 07:00
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

# Decision: Where should [[Master Goal v4.1]] go?

**Classifier top candidates** (ranked by confidence):

- [ ] **A.** 1-Projects/Second-Brain-System/Master-Goal-v4-1--2026-03-06-0700.md — 85%  
  New dedicated Second-Brain-System project folder with timestamped filename.

- [ ] **B.** 1-Projects/Test-Project/Master Goal v4.1.md — 27%  
  Under 1-Projects/Test-Project.

- [ ] **C.** 1-Projects/Genesis-Mythos/Master Goal v4.1.md — 12%  
  Under 1-Projects/Genesis-Mythos.

- [ ] **D.** 1-Projects/OG-minecraft/Master Goal v4.1.md — 9%  
  Under 1-Projects/OG-minecraft (shared Master Goal across systems).

- [ ] **E.** 1-Projects/Pong-Game/Master Goal v4.1.md — 9%  
  Under 1-Projects/Pong-Game.

- [ ] **F.** 1-Projects/Retro Snake Game/Master Goal v4.1.md — 9%  
  Under 1-Projects/Retro Snake Game.

- [ ] **G.** 3-Resources/Second-Brain-System/Master-Goal-v4-1--2026-03-06.md — 5%  
  As Resource reference instead of active Project.

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
