---
title: Second Brain Plugins
created: 2026-02-28
tags: [pkm, second-brain, plugins, obsidian, cursor]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

**TL;DR** — Required: Dataview (dashboards), Highlightr (colors; data-highlight-source), Local REST API (MCP), Watcher (signal/result/queue). Optional: Commander (triggers, macros). Agent does not modify Dataview blocks; must not move/delete Watcher paths.

---

# Second Brain Plugins

## Obsidian (required)

| Plugin | Role | Responsibilities |
|--------|------|------------------|
| **Dataview** | Queries, dashboards, log aggregation | Queries and dashboards (e.g. Vault-Change-Monitor); agent does not modify Dataview query blocks in notes |
| **Highlightr** | Highlight colors; master key in [[3-Resources/Highlightr-Color-Key|Highlightr-Color-Key]]; project highlight_key in skills. Agent uses `data-highlight-source="agent"`. CSS: `data-drift-level` (0=core → 3=fade). See [[3-Resources/Second-Brain/Color-Coded-Highlighting|Color-Coded-Highlighting]]. | Renders highlight colors; agent sets data-highlight-source and class from master key or highlight_key; skills apply colors, plugin renders |
| **Obsidian Local REST API** | MCP server talks to vault (read, update, move, etc.); API key in MCP env | MCP uses for all vault read/update/move; API key in ~/.cursor/mcp.json env; required for pipelines |
| **Watcher** | Watcher-Signal.md → Cursor; Watcher-Result.md; queue; fixed paths | Writes signal; reads result; agent must not move/delete Watcher paths or watcher-protected notes |

## Obsidian (optional)

| Plugin | Role | Responsibilities |
|--------|------|------------------|
| **Commander** | Place Watcher/queue and roadmap commands in ribbon, status bar, or mobile toolbar; macros for pipeline triggers; commander_source/commander_macro logging. **Multi-run roadmap macros:** Resume Roadmap, RECAL-ROAD, Sync phase outputs, Reopen Phase (REVERT-PHASE), **Approve All Roadmap Wrappers** (or Approve All Pending Wrappers in Project) for bulk-approve of roadmap Decision Wrappers; **Queue Research: Phase** (RESEARCH-AGENT); **Queue Research: Gaps** (RESEARCH-GAPS — scan current phase note for gaps, append RESEARCH-AGENT with gaps array; run from roadmap phase note). When roadmap-deepen detects high-severity gaps, it appends a banner to the phase note and an entry to Mobile-Pending-Actions so mobile/laptop user can approve or run "Queue Research: Gaps". With **auto_apply_safe_threshold: 82** (Second-Brain-Config roadmap block), single-option wrappers ≥82% may auto-apply with snapshot + log. See [[3-Resources/Commander-Plugin-Usage|Commander-Plugin-Usage]] (or [[4-Archives/Resources/Plugins-Usage/Commander-Plugin-Usage]] if moved to Archives). | Surfaces triggers in UI; agent logs commander_source and commander_macro when run was Commander-triggered |
| **Commando** (optional) | Enhances Commander macros; optional for timed chains. | Add to Plugins only if needed. |
| **Templater**, **Tasks**, **QuickAdd**, **Excalidraw** | Optional; templates and task management. | Optional; not required for Second-Brain pipelines. |

## Usage example

After a pipeline run, open **Vault-Change-Monitor** (Dataview dashboard) to see last N log entries from Ingest-Log, Distill-Log, etc. Check **Watcher-Result.md** for the requestId and status (success/failure) and completed timestamp to confirm the run finished and inspect any trace on failure.

## Cursor

- **Rules**: `.cursor/rules/always/` and `.cursor/rules/context/`
- **Skills**: `.cursor/skills/<name>/SKILL.md`
- **MCP**: `~/.cursor/mcp.json` — server `obsidian-para-zettel-autopilot`

## Watcher contract

- Pipelines must **not** move or delete: `Ingest/watched-file.md`, `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`, or any note with frontmatter `watcher-protected: true`.
- See [[3-Resources/Watcher-Plugin-Usage|Watcher-Plugin-Usage]] and [[.cursor/rules/always/watcher-result-append|watcher-result-append]].

## Component and data flow

```mermaid
flowchart LR
  subgraph obsidian [Obsidian]
    Dataview[Dataview]
    Highlightr[Highlightr]
    REST[Local REST API]
    Watcher[Watcher]
    Commander[Commander toolbar/ribbon]
  end
  subgraph cursor [Cursor]
    Rules[Rules]
    Skills[Skills]
    MCP[MCP client]
  end
  Watcher -->|Watcher-Signal| MCP
  MCP -->|Watcher-Result| Watcher
  MCP <-->|REST API| REST
  Rules --> MCP
  Skills --> MCP
  subgraph protected [Watcher-protected paths]
    P1[watched-file.md]
    P2[Watcher-Signal.md]
    P3[Watcher-Result.md]
  end
```
