---
title: Areas Hub
created: 2026-02-21
tags: [hub, moc, para]
para-type: Resource
status: active
links: [[PARA-Dashboard]]
---

# Areas Hub

MOC for all **Areas** (ongoing responsibilities and standards). Notes live in `2-Areas/`.

```dataview
LIST
FROM "2-Areas"
WHERE para-type = "Area"
SORT file.name ASC
```

*Recently updated areas:*
```dataview
TABLE file.name AS "Area", file.mtime AS "Updated"
FROM "2-Areas"
WHERE para-type = "Area"
SORT file.mtime DESC
LIMIT 10
```

---

## Manual links

- [[PARA-Dashboard]]
