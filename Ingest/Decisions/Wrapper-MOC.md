---
title: Wrapper MOC (Decisions dashboard)
created: 2026-03-07
tags: [moc, decisions, wrappers]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Logs]]"]
---

# Wrapper MOC — Pending decisions and plan evolution

Single "overlord" view for all Decision Wrappers: pending by folder and applied (plan evolution). See [[3-Resources/Second-Brain/Logs#Vault-Change-Monitor blocks (Plan Evolution, Pending Re-Tries)|Logs § Vault-Change-Monitor blocks]].

## Pending wrappers (by subfolder)

```dataview
TABLE WITHOUT ID file.link AS "Pending", decision_priority, clunk_severity, wrapper_type, approved_option, approved_path
FROM "Ingest/Decisions"
WHERE decision_candidate = true AND approved = false
  AND (file.folder = "Ingest/Decisions/Ingest-Decisions" OR file.folder = "Ingest/Decisions/Roadmap-Decisions" OR file.folder = "Ingest/Decisions/Refinements" OR file.folder = "Ingest/Decisions/Low-Confidence" OR file.folder = "Ingest/Decisions/Errors")
SORT clunk_severity DESC, decision_priority DESC, file.ctime DESC
```

## Pending re-tries

```dataview
LIST
FROM "Ingest/Decisions"
WHERE re-try = true AND (processed != true OR !processed)
SORT file.mtime DESC
```

## Plan evolution (applied roadmap/phase-direction wrappers)

```dataview
TABLE file.link AS "Wrapper", used_at, approved_option
FROM "4-Archives/Ingest-Decisions/Roadmap-Decisions"
WHERE processed = true
SORT used_at DESC
LIMIT 20
```

For per-project view, add `GROUP BY project-id` in Dataview when frontmatter includes project-id.
