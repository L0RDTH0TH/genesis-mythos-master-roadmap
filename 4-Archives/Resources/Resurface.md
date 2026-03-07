---
title: Resurface
created: 2026-02-21
tags: [resurface, express, code]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[PARA-Dashboard]]"]
---

# Resurface

High-value notes for **periodic resurfacing** (Forte: bring old notes back into view so forgotten ideas spark new connections). Curate **manually** — no random Dataview; add links below as you identify key dev notes and reference material.

## Manual links (curated)

- *(Add key project or resource notes here, e.g. [[Project X]], [[Algorithm Notes]].)*
- [[PARA-Dashboard]]
- [[Dev-Task-Tracker]] — graphs, streaks, completion %
- [[Capture-Guide]]
- [[Building a Second Brain]] *(example — link to your BASB/PKM MOC if you have one)*

**Manual review weekly;** add key [[Project Note]] or resource here for quick access. Use this list when doing weekly reviews or before Express (writing, coding, teaching). For a compiled export of active projects (goal, tasks, code, bugs, deadlines), run `node Scripts/Export-Active-Projects.js` from the vault (output: `Active-Projects-Export.md`).

---

## Resurface candidates (Dataview)

Notes marked `resurface-candidate: true` (e.g. by the resurface-candidate-mark skill during archive). Run this query manually for periodic review, or when the Cursor rule **auto-resurface** is triggered (e.g. user says "resurface" or "show resurface candidates").

````markdown
```dataview
TABLE file.ctime AS "Created", file.mtime AS "Modified"
FROM ""
WHERE resurface-candidate = true
SORT file.mtime DESC
```
````

---

*Why resurface?* Progressive Summarization and CODE assume you revisit notes over time. This page is a simple, human-curated index so high-leverage notes don’t stay buried.
