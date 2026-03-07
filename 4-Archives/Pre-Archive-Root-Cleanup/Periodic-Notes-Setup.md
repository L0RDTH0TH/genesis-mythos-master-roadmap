---
title: Periodic Notes Setup (Daily / Weekly)
created: 2026-02-21
tags: [periodic-notes, quickadd, templater, phase3]
para-type: Resource
status: active
links: ["[[PARA-Dashboard]]", "[[Capture-Guide]]"]
---

# Periodic Notes Setup (Phase 3)

**Daily/Weekly only;** dev focus (code goals, reflections, tasks). No energy/habits tracking.

## QuickAdd configuration (suggested)

*Copy these into Obsidian → Settings → QuickAdd → Add Choice.*

### Daily note

1. **Add Choice** → **Template**.
2. **Template path:** `Templates/Daily-Note-Template.md`.
3. **Folder:** `Daily Notes/`.
4. **File name:** `2026-02-21` (so the note is named by date).
5. **Open after creation:** Yes (recommended).
6. **Hotkey (optional):** e.g. **Ctrl+D**.
7. **Choice name:** e.g. **"Daily Note"**.

*Templater must run on new file creation:* In Templater settings, enable "Trigger Templater on new file creation" or run manually (Ctrl+E) after creating the note.

### Weekly note

1. **Add Choice** → **Template**.
2. **Template path:** `Templates/Weekly-Note-Template.md`.
3. **Folder:** `Weekly Notes/`.
4. **File name:** `2026-W08` (e.g. 2026-W08).
5. **Open after creation:** Yes.
6. **Hotkey (optional):** e.g. **Ctrl+W**.
7. **Choice name:** e.g. **"Weekly Note"**.

Again, run Templater after creation if not auto-triggered.

---

## Accomplishments aggregation

- In **Daily notes**, add `#dev-accomplishment` to the **tags** frontmatter (or in body) when you log a reflection worth surfacing.
- The **Weekly note** Dataview block "Accomplishments from Dailies" lists daily notes that contain that tag.
- If nothing appears, tag at least one daily with `dev-accomplishment` or log wins manually in the weekly note.

---

## Links

- [[PARA-Dashboard]] · [[Projects Hub]] · [[Resurface]]
- [[Daily-Note-Template]] · [[Weekly-Note-Template]]
