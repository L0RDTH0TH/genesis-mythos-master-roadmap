---
title: Capture Guide
created: 2026-02-21
tags: [code, capture, ingest, quickadd]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[PARA-Dashboard]]"]
---

# Capture Guide (CODE — Capture)

Quick capture for the Second Brain: **Capture** → sync → **Organize** (Cursor/Agent) → Distill → Express.

## On phone (Obsidian Mobile)

1. Open Obsidian (sync vault).
2. **Create New Note** → press and hold the **"Ingest"** folder.
3. **Ingest** creates a file with the input template.
4. Paste or type your raw idea; save.
5. Sync to desktop (Syncthing, Obsidian Sync, or your method).

## On desktop

- Same flow: QuickAdd → template **Ingest-Template.md** → folder **Ingest/**.
- Or create a note manually in `Ingest/` and paste content; use frontmatter `status: raw` and `para-type: Ingest`.

## After capture

- **Do not** auto-move or auto-classify. Raw notes stay in **Ingest/** until processed.
- Process via **Cursor Agent**: open the ingest note (or select it) and prompt with something like: *"Sort this raw ingest note for software dev productivity: classify PARA, add frontmatter and hub links, add Why [para-type]?, Next Actions, and progressive summarization if applicable."*
- After Agent run: review output, then **manually** move (e.g. `mv Ingest/Note.md "3-Resources/2026-02-21-title.md"`) once you confirm.

## QuickAdd setup (suggested)

*No plugin config is edited here — use this as reference in Obsidian.*

1. Open **QuickAdd** settings (Obsidian Settings → QuickAdd).
2. **Add Choice** → **Template**.
3. **Template path**: `Templates/Ingest-Template.md`.
4. **File name**: e.g. `Capture-2026-02-21-0531` or leave "Use template file name" if you prefer.
5. **Folder**: `Ingest/`.
6. **Open file after creation**: optional (e.g. Yes for quick paste).
7. Assign a **Hotkey** (e.g. Ctrl+Shift+I for "Ingest Idea").
8. Name the choice e.g. **"Ingest Idea"** so on mobile you can tap it to create a new raw capture in Ingest.

---

**Links:** [[Resources Hub]] · [[PARA-Dashboard]] · [[Ingest-Template]]
