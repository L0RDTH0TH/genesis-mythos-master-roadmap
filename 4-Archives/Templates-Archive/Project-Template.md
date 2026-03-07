---
archived_from: Templates/Project-Template.md
archived_date: 2026-03-06
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags: []
para-type: Project
status: active
links: ["[[Projects Hub]]"]
tech-stack: []
priority: medium
deadline: YYYY-MM-DD
---

# <% tp.file.title %>

## TL;DR

_Short 1–3 sentence summary of what this project is about and why it matters._

-  

## Goal / Endpoint

*What does done look like? (Time-bound; Forte: Project = specific endpoint.)*

## Tasks

*Use native checkboxes; tag dev tasks with `#dev-task`, bugs with `#bug`. Sort by priority (high/medium/low).*

- [ ] Dev Task *(priority: high, #dev-task)*
- [ ] Fix bug *(#bug)*
- [ ]
- [ ]

## Code Snippets

```lang
// paste or describe
```

## Bugs / Issues

- 

## Related Notes

- [[ ]]
- [[ ]]

## Dataview Queries

*Incomplete tasks in this project:*
```dataview
TASK
FROM this.file
WHERE !completed
SORT due ASC
```

*Incomplete dev tasks across all projects (for copy into hub/dashboard):*
```dataview
TASK
FROM "1-Projects"
WHERE !completed AND (contains(file.tags, "dev-task") OR contains(file.tags, "bug"))
SORT file.priority DESC, due ASC
```

---

## Why Project?

*This note is classified as a **Project** per PARA: it has a clear goal/endpoint and is time-bound. Actionability-first: projects get priority over areas/resources.*
