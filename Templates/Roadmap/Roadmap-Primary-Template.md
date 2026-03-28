title: "Primary N — <Name>"
roadmap-level: primary
phase-number: N
project-id: <project-id>
status: active
priority: high
progress: 0
created: {{date:YYYY-MM-DD}}
tags: [roadmap, <project-id>, phase]
para-type: Project
links:
  - "[[<project-id>-Roadmap-YYYY-MM-DD-HHMM]]"
---

## Primary N — <Name>

<Short narrative of the phase intent.>

### Seed tasks

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Subphases & notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Roadmap",
  subphase-index AS "Index",
  status AS "Status",
  progress AS "% Progress"
FROM "1-Projects/<project-id>/Roadmap/Phase-N-<Name>"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

