---
title: "Phase N.M — <Secondary Name>"
roadmap-level: secondary
phase-number: N
project-id: <project-id>
status: active
priority: high
progress: 0
created: {{date:YYYY-MM-DD}}
tags: [roadmap, <project-id>, phase, secondary]
para-type: Project
links:
  - "[[Phase-N-<Name>-Roadmap-YYYY-MM-DD-HHMM]]"
subphase-index: "N.M"
---

## Phase N.M — <Secondary Name>

<Short description of this secondary subphase and its role in the phase.>

### Responsibilities

- [ ] Responsibility 1
- [ ] Responsibility 2
- [ ] Responsibility 3

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Roadmap",
  subphase-index AS "Index",
  status AS "Status",
  progress AS "% Progress"
FROM "1-Projects/<project-id>/Roadmap/Phase-N-<Name>/Phase-N-M-<Secondary-Name>"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

