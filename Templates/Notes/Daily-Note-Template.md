---
title: <% tp.date.now("YYYY-MM-DD") %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags: []
para-type: Area
status: active
links: ["[[PARA-Dashboard]]", "[[<% tp.date.now("YYYY-[W]WW") %>]]"]
---

# <% tp.date.now("YYYY-MM-DD") %>

<< [[<% tp.date.now("YYYY-MM-DD", -1) %>|Yesterday]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>|Tomorrow]] >> · Week: [[<% tp.date.now("YYYY-[W]WW") %>]]

---

## Daily TL;DR

_One–two sentences capturing the main outcome, learning, or theme for today._

-  

## Today's Code Goals

*Use checkboxes; add `#dev-task` and optional priority/deadline for aggregation.*

- [ ] *(priority: high, deadline: YYYY-MM-DD, #dev-task)*
- [ ] 
- [ ] 

## Reflections

*Code progress, bugs, learnings. Tag accomplishments with `#dev-accomplishment` for weekly aggregation.*

- 
- 

## Dev Tasks Aggregated

*Active project tasks due or relevant today (from 1-Projects):*

```dataview
TASK
FROM "1-Projects"
WHERE status = "active" AND (deadline = date(this.file.name) OR !deadline)
SORT priority DESC, due ASC
```

*Incomplete dev tasks (from 1-Projects and this daily note); high priority first:*
```dataview
TASK
FROM "1-Projects" OR this.file
WHERE !completed AND (contains(file.tags, "dev-task") OR contains(file.tags, "bug"))
SORT file.priority DESC, due ASC
```

---

[[PARA-Dashboard]] · [[Projects Hub]] · [[<% tp.date.now("YYYY-[W]WW") %>|This week]]
