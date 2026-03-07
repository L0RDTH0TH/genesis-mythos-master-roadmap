---
title: Resources Hub
created: 2026-02-21
tags: [hub, moc, para]
para-type: Resource
status: active
links: [[PARA-Dashboard]]
---

# Resources Hub

MOC for all **Resources** (reference topics, research, hobbies). Notes live in `3-Resources/`.

```dataview
LIST
FROM "3-Resources"
WHERE para-type = "Resource"
SORT file.name ASC
```

*Recently updated resources:*
```dataview
TABLE file.name AS "Resource", file.mtime AS "Updated"
FROM "3-Resources"
WHERE para-type = "Resource"
SORT file.mtime DESC
LIMIT 10
```

---

## Manual links

- [[PARA-Dashboard]]
- [[Ingest/Decisions/Wrapper-MOC]] — Pending decisions and plan evolution (overlord dashboard)
