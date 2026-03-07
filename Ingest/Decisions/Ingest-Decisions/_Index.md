---
title: Ingest-Decisions Index
created: 2026-03-05
tags:
  - ingest
  - decisions
---

# Pending Ingest Decisions

```dataview
TABLE WITHOUT ID file.link AS "Decision", decision_priority, approved_option, approved_path, file.mtime AS "Modified"
FROM "Ingest/Decisions/Ingest-Decisions"
WHERE !approved
SORT file.mtime DESC
```

## Applied Ingest Decisions (Archive)

```dataview
TABLE WITHOUT ID file.link AS "Decision", decision_priority, approved_option, approved_path, used_at
FROM "4-Archives/Ingest-Decisions"
WHERE contains(file.name, "Decision-for-")
SORT used_at DESC, file.ctime DESC
```
