---
title: Roadmap-Decisions Index
created: 2026-03-05
tags:
  - ingest
  - decisions
  - roadmap
---

# Pending Roadmap Decisions

```dataview
TABLE WITHOUT ID file.link AS "Decision", decision_priority, approved_option, approved_path, file.mtime AS "Modified"
FROM "Ingest/Decisions/Roadmap-Decisions"
WHERE !approved
SORT file.mtime DESC
```

## Applied Roadmap Decisions (Archive)

```dataview
TABLE WITHOUT ID file.link AS "Decision", decision_priority, approved_option, approved_path, used_at
FROM "4-Archives/Ingest-Decisions"
WHERE contains(file.name, "Decision-for-") AND wrapper_type = "roadmap"
SORT used_at DESC, file.ctime DESC
```
