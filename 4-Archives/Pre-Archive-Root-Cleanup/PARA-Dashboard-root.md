---
type: dashboard
para-level: 3
status: active
created: 2026-02-21
tags: [dashboard, para, moc]
---

# PARA Dashboard (Level 3)

Actionability-first: **Projects → Areas → Resources → Archives**. Use this as your vault home.

---

## Ingest Review

- Review raw captures in the **Ingest/** folder; process with PARA-Zettel autopilot or manually classify into Projects/Areas/Resources/Archives.

---

## Task Overview

*Incomplete #dev-task / #bug by priority and deadline (actionability-first):*
```dataview
TASK
FROM "1-Projects"
WHERE !completed AND (contains(file.tags, "dev-task") OR contains(file.tags, "bug"))
SORT file.priority DESC, due ASC
```

---

## Active Projects

```dataview
TABLE file.name AS "Project", status, deadline, tech-stack
FROM "1-Projects"
WHERE para-type = "Project" AND status = "active"
SORT deadline ASC
```

---

## Areas Overview

```dataview
LIST
FROM "2-Areas"
WHERE para-type = "Area"
SORT file.name ASC
```

---

## Resources Hub

```dataview
LIST
FROM "3-Resources"
WHERE para-type = "Resource"
SORT file.name ASC
```

---

## Archives Summary

```dataview
TABLE file.name AS "Archived", status
FROM "4-Archives"
WHERE para-type = "Archive"
SORT file.mtime DESC
LIMIT 15
```

*Recent archives (full list in [[4-Archives]] or via hub):*
*(See Archives section above; for a numeric count, use Dataview JS or a grouped query in Obsidian.)*

---

## Dev-Focused Queries

*Projects with Python or #dev:*
```dataview
TABLE file.name, tech-stack, priority
FROM "1-Projects"
WHERE (contains(tech-stack, "Python") OR contains(tags, "dev"))
SORT priority DESC, file.name ASC
```

*All active projects with tech-stack (for dev overview):*
```dataview
TABLE file.name, tech-stack, priority, deadline
FROM "1-Projects"
WHERE para-type = "Project" AND status = "active" AND length(tech-stack) > 0
SORT deadline ASC
```

---

## Manual links (key active dev / MOCs)

*Curate manually for quick access.*

- [[Projects Hub]] — all projects
- [[Areas Hub]] — all areas
- [[Resources Hub]] — all resources
- [[Resurface]] — high-value notes for resurfacing
- [[Capture-Guide]] — quick capture + Ingest flow
- [[Periodic-Notes-Setup]] — Daily / Weekly notes (Phase 3)
*Add links to key active project/area notes here, e.g. [[Your Project]].*

---

## Dev tasks and bugs (actionability)

*Active dev-related projects (tagged #dev or #dev-task):*
```dataview
LIST
FROM "1-Projects"
WHERE status = "active" AND (contains(tags, "dev-task") OR contains(tags, "dev"))
SORT deadline ASC, file.mtime DESC
```

*Bugs and high-priority items:*
```dataview
TABLE file.name AS "Note", priority
FROM "1-Projects"
WHERE contains(tags, "bug") OR priority = "high"
SORT priority DESC, file.name ASC
```

---

## Hub Links (MOCs)

- [[Projects Hub]] — all projects
- [[Areas Hub]] — all areas
- [[Resources Hub]] — all resources

---

## Collapsible Sections (Obsidian)

Use Obsidian's native `> [!summary]- Section title` callouts to collapse sections if desired, e.g.:

> [!summary]- Click to expand: Ingest / Quick capture
> - [[Ingest]] folder: raw captures; manual review before PARA assignment.
> - Consider linking to [[PARA-Dashboard]] after classification.

---

*Why Level 3?* Dynamic PARA: notes live in numbered folders by type; Dataview surfaces by actionability. Projects first (goals/deadlines), then Areas (ongoing), then Resources (reference), then Archives (inactive).
