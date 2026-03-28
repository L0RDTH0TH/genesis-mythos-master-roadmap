---
title: <% tp.date.now("YYYY-[W]WW") %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags: []
para-type: Area
status: active
links: ["[[PARA-Dashboard]]"]
---

# Week <% tp.date.now("YYYY-[W]WW") %>

*Daily notes from the last 7 days (adjust range in query if needed):*

```dataview
LIST
FROM "Daily Notes"
WHERE date(file.name) >= date(today) - dur(7 days)
SORT file.name DESC
```

*Or link manually: [[YYYY-MM-DD]], [[YYYY-MM-DD]], …*

---

## Weekly TL;DR

_One–two sentences capturing the main outcomes, shifts, or themes from this week._

-  

## Weekly Code Goals

*Use checkboxes; tag with `#dev-task` for tracking.*

- [ ] *(#dev-task)*
- [ ] 
- [ ] 

## Weekly Reflections

- 
- 

## Aggregated Dev Tasks

*Active projects (actionability-first):*
```dataview
LIST
FROM "1-Projects"
WHERE status = "active"
SORT deadline ASC, priority DESC
```

*Incomplete dev tasks (from 1-Projects and Daily Notes); high priority first:*
```dataview
TASK
FROM "1-Projects" OR "Daily Notes"
WHERE !completed AND (contains(file.tags, "dev-task") OR contains(file.tags, "bug"))
SORT file.priority DESC, due ASC
```

## Accomplishments from Dailies

*Add `#dev-accomplishment` in Daily Notes → Reflections for entries to appear here.*

```dataview
TABLE file.name AS "Day", file.ctime AS "Created"
FROM "Daily Notes"
WHERE contains(tags, "dev-accomplishment")
SORT file.name DESC
```

*If no results:* tag accomplishments in daily reflections with `#dev-accomplishment` (in tags frontmatter or in body), or log key wins manually below.

- 
- 

---

[[PARA-Dashboard]] · [[Projects Hub]] · [[Resurface]]
