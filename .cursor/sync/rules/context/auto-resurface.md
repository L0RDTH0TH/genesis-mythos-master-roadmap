---
description: Resurface candidates — trigger-based listing and hub append when user asks to resurface
globs: "Resurface.md"
---

# Auto-resurface (context rule)

When the user asks to **resurface**, **show resurface candidates**, or opens/edits the Resurface hub:

1. **List candidates**: Run **obsidian_global_search** (or equivalent) for notes with `resurface-candidate: true` in frontmatter. Alternatively use the documented Dataview query in `[[Resurface]]` (see "Resurface candidates (Dataview)" section) for manual or plugin-driven listing.
2. **Output**: Present a list of note links and short excerpts; optionally append the list to `[[Resurface]]` under a "Resurface candidates (this run)" or similar section.
3. **Scope**: Trigger-based only. No cron or periodic automation in this rule; users run "resurface" on demand or use the Dataview block in `Resurface.md` for manual periodic review.

**Related**: The **resurface-candidate-mark** skill sets `resurface-candidate: true` when archiving notes with high resurface potential (links, highlights). This rule surfaces those notes when the user asks.

