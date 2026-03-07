---
title: Projects Hub
created: 2026-02-21
tags: [hub, moc, para]
para-type: Resource
status: active
links: [[PARA-Dashboard]]
---

# Projects Hub

MOC for all **Projects** (time-bound goals with endpoints). Actionability-first: projects live in `1-Projects/`.

```dataview
TABLE file.name AS "Project", status, deadline, priority
FROM "1-Projects"
WHERE para-type = "Project"
SORT status = "active" DESC, deadline ASC, file.name ASC
```

*Incomplete tasks in projects (actionability); #dev-task / #bug first by priority:*
```dataview
TASK
FROM "1-Projects"
WHERE !completed AND (contains(file.tags, "dev-task") OR contains(file.tags, "bug"))
SORT file.priority DESC, due ASC
```

*All incomplete tasks in projects (any):*
```dataview
TASK
FROM "1-Projects"
WHERE !completed
SORT file.priority DESC, due ASC
```

*Recently updated projects:*
```dataview
TABLE file.name AS "Project", file.mtime AS "Updated"
FROM "1-Projects"
WHERE para-type = "Project"
SORT file.mtime DESC
LIMIT 10
```

*Completion tracking:* Use `- [x]` for completed tasks; optional daily notes with `#dev-accomplishment` for streaks.

---

## Manual links

- [[PARA-Dashboard]]
