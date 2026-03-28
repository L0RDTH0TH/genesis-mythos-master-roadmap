---
title: "<project-id> Roadmap"
roadmap-level: master
phase-number: 0
project-id: <project-id>
status: active
priority: high
progress: 0
created: {{date:YYYY-MM-DD}}
tags: [roadmap, <project-id>, master]
para-type: Project
links: []
---

# <project-id> — Roadmap

## Generation provenance

- Source: [[<Source-Note-Optional>]]
- Generated: {{date:YYYY-MM-DD}} {{time:HH:mm}}

## Phase 1 — <Name>

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Roadmap",
  subphase-index AS "Index",
  status AS "Status",
  progress AS "% Progress"
FROM "1-Projects/<project-id>/Roadmap/Phase-1-<Name>"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 2 — <Name>

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Roadmap",
  subphase-index AS "Index",
  status AS "Status",
  progress AS "% Progress"
FROM "1-Projects/<project-id>/Roadmap/Phase-2-<Name>"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

<!-- Repeat phase sections as needed -->

## Related

- [[<project-id>-Roadmap-MOC]]

