---
name: Commander Plugin Integration
overview: Document the installed Obsidian Commander plugin in the Second Brain backbone, add a dedicated usage guide aligned with Watcher and mobile-toolbar docs, and update existing references so Commander is the recommended way to place queue/task/roadmap commands in the UI.
todos: []
isProject: false
---

# Commander Plugin Integration Plan

## Summary

**Commander** (phibr0, v0.5.4) is an Obsidian community plugin that places any core or community command in the ribbon, status bar, context menus, editor title bar, and mobile toolbar. It supports device-specific visibility, macros (chained commands with delays/loops), and custom icons/labels/colors. The vault already references Commander in [Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md) and [Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) for "Process Queue" one-tap and "Roadmap Tools" grouping; this plan formalizes Commander as an integrated optional plugin with a single usage doc and backbone updates.

**Out of scope**: No Cursor rules or MCP changes—Commander is Obsidian-only. No editing of `.obsidian/plugins/cmdr/data.json` (user-configured in Obsidian Settings).

---

## 1. Add Commander to Plugins.md

**File**: [3-Resources/Second-Brain/Plugins.md](3-Resources/Second-Brain/Plugins.md)

- In **Obsidian (optional)**, add a row for Commander:
  - **Commander**: Place Watcher/queue and roadmap commands in ribbon, status bar, or mobile toolbar; optional macros for pipeline triggers; device-specific visibility. See [[3-Resources/Commander-Plugin-Usage|Commander-Plugin-Usage]].
- Optionally add Commander to the Mermaid diagram in the Obsidian subgraph (e.g. `Commander[Commander toolbar/ribbon]`) with a short label that it surfaces commands (no new data flows; diagram remains readable).

---

## 2. Create Commander-Plugin-Usage.md

**New file**: `3-Resources/Commander-Plugin-Usage.md`

Structure (aligned with [Watcher-Plugin-Usage.md](3-Resources/Watcher-Plugin-Usage.md)):

- **Frontmatter**: `title`, `created`, `tags` (e.g. `commander`, `second-brain`, `setup`, `toolbar`), `para-type: Resource`, `links` to Resources Hub and Plugins.md.
- **What Commander does**: One short paragraph (place commands everywhere; macros; mobile toolbar; declutter).
- **How it fits this vault**: Commander does not replace Watcher—Watcher provides the commands (Ingest, Distill, etc.) and queue behavior; Commander is where you **put** those commands (and others) in the UI.
- **Suggested setup**:
  - **One-tap Process Queue**: Add a toolbar/ribbon item that runs the command that triggers queue processing (e.g. "Watcher: Prompt Modal" with a preset, or a custom Shell-command/open-Cursor step if used). Reference [Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md) § One-tap Process Queue.
  - **Roadmap Tools**: Group TASK-ROADMAP, Task Complete, Add Roadmap Item, etc., under one icon or sub-menu if Commander supports it; prioritize Task Complete and Process Queue on the main bar (per Mobile-Toolbar-Task-Commands).
  - **Optional macros**: E.g. chain "Open Watcher modal" → delay → "Copy EAT-CACHE" for desktop workflows; document as optional.
  - **Device-specific**: Show "Process Queue" on mobile toolbar; optionally hide or show Roadmap Tools only on mobile/desktop as desired.
- **Contextual visibility**: Note that context-based visibility (e.g. show Roadmap Tools only when `para-type: Roadmap` or path under `1-Projects/…/Roadmap/`) is plugin/settings-dependent; [Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) already describes this; link there.
- **Links**: To [Watcher-Plugin-Usage](3-Resources/Watcher-Plugin-Usage.md), [Mobile-Toolbar-Task-Commands](3-Resources/Mobile-Toolbar-Task-Commands.md), [Plugins](3-Resources/Second-Brain/Plugins.md).

No step-by-step screenshots required; keep it concise like Watcher-Plugin-Usage.

---

## 3. Update Mobile-Toolbar-Task-Commands.md

**File**: [3-Resources/Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md)

- In **One-tap Process Queue**: Replace "via Obsidian **Commander** or **Advanced Toolbar**" with "via **Commander** (recommended; see [[3-Resources/Commander-Plugin-Usage]]) or Advanced Toolbar".
- In **Toolbar overcrowding**: Add a line that Commander is installed and that grouping/sub-menu setup is in [[3-Resources/Commander-Plugin-Usage]].

---

## 4. Backbone and sync

- **Plugins.md** is the canonical plugin list; the new Commander-Plugin-Usage note is linked from there and from Mobile-Toolbar-Task-Commands. No new Backbone README index entry is required (Plugins.md already covers plugins).
- **backbone-docs-sync**: Adding a new Resource note (Commander-Plugin-Usage) and editing Plugins.md counts as updating backbone docs; no new rule or skill is added, so `.cursor/sync/` has nothing to sync for Commander.

---

## 5. Optional cross-references

- **Vault-Layout.md**: Already says "Configure via Commander or Note Toolbar plugin settings"; optionally add a short link: "See [[3-Resources/Commander-Plugin-Usage]] for Commander setup."
- **Second-Brain-Starter-Kit**: If [Second-Brain-Starter-Kit/0-Onboarding/Mobile-Setup.md](Second-Brain-Starter-Kit/0-Onboarding/Mobile-Setup.md) or similar mentions Commander, add a link to the main vault’s Commander-Plugin-Usage (or "see main vault Commander-Plugin-Usage") so starter-kit users have one place to read.

---

## Implementation order

1. Create `3-Resources/Commander-Plugin-Usage.md` with the structure above.
2. Update `3-Resources/Second-Brain/Plugins.md` (Commander row; optional diagram tweak).
3. Update `3-Resources/Mobile-Toolbar-Task-Commands.md` (Commander links and "installed" note).
4. Optionally update `3-Resources/Second-Brain/Vault-Layout.md` and Starter-Kit Mobile-Setup with a link to Commander-Plugin-Usage.

---

## Verification

- All new/edited notes have frontmatter and tags per second-brain-standards.
- Plugins.md and Commander-Plugin-Usage are linked bidirectionally; Mobile-Toolbar-Task-Commands points to Commander-Plugin-Usage.
- No Cursor rules or MCP config changes; Commander remains a documented optional Obsidian plugin.

