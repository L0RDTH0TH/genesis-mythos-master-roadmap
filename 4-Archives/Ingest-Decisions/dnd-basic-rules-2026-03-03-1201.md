---
approved: true
decision_candidate: true
proposal_path: Ingest/Decisions/dnd-basic-rules-2026-03-03-1201.md
original_note:
  - - Ingest/dnd basic rules.md
original_path: Ingest/dnd basic rules.md
decision_priority: high
created: 2026-03-03 12:01
used_at: "2026-03-03T22:12:00Z"
processed: true
---

# Decision: Where should [[Ingest/dnd basic rules.md]] go?

**Classifier top candidates** (ranked by confidence):

- [ ] **A.** 3-Resources/TTRPGs/DnD-5e/Rulebooks/dnd basic rules.md — 92%  
  Core D&D 5e Basic Rules reference; actively used at table for rules lookups.

- [ ] **B.** 3-Resources/TTRPGs/DnD-5e/Core-Rules/dnd basic rules.md — 88%  
  Same as A but organized under a Core-Rules folder if you want multiple rulebook variants together.

- [x] **C.** 3-Resources/TTRPGs/Rulebooks/dnd basic rules.md — 80%  [completion:: 2026-03-03]
  Treat this as a general TTRPG rulebook reference without locking into a specific campaign or world.

- [ ] **D.** 3-Resources/Reference-Docs/dnd basic rules.md — 72%  
  For a minimal, catch-all reference-docs shelf shared with non-TTRPG material.

- [ ] **E.** 4-Archives/TTRPGs/DnD-5e/dnd basic rules.md — 55%  
  Only if you expect to rarely consult this in active play but still want it preserved.

**Your action — check ONE box above AND set ONE frontmatter line:**

Quick pick (recommended):  
`approved_option: A`

OR custom/override path:  
`approved_path: "exact/path/you-want.md"`

OR reject all candidates (free guidance only):  
`approved_option: 0`

**Thoughts / corrections / why this location?**  
(This becomes `user_guidance` — be as specific or corrective as you like)

> Minimal organization there are references to these rules in some of the Genesis-Mythos linked docs.
> But there are also references in those same docs about using them for the prototype and using a different system later.
> Thus a general location is superior due to the implicit reference to additional future rule files  
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
TABLE WITHOUT ID file.link AS "Recent decision", decision_priority, approved_option, approved_path, used_at
FROM "Ingest/Decisions"
WHERE approved = true
SORT used_at DESC, file.ctime DESC
```
