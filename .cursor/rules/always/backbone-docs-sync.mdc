---
description: When backbone or rules/skills are modified, update Second-Brain docs and .cursor/sync
alwaysApply: true
---

# Backbone docs sync

When the user or the agent modifies any **backbone** component, update the corresponding documentation and (for rules/skills) the sync folder.

## Trigger

Backbone components: files under `.cursor/rules/` (always or context), `.cursor/skills/`, pipeline definitions or trigger mapping (e.g. Cursor-Skill-Pipelines-Reference or context rules), MCP server config or tool behavior (`~/.cursor/mcp.json` or project `mcps/`), `3-Resources/Second-Brain-Config.md`, or any note in `3-Resources/Second-Brain/`.

## Documentation location (official system docs)

- **All official system documentation** belongs in **`3-Resources/Second-Brain/Docs/`** (pipelines, subagents, user flows, operations, reference). When creating or placing new system docs, use that path; keep backbone index files (e.g. Rules.md, Skills.md) in `3-Resources/Second-Brain/` as the map, with detailed content under `Docs/` as appropriate.
- **`3-Resources/Second-Brain`** (the folder) is **dev docs** (configuration, indices, backbone reference).
- **`3-Resources/Second-Brain/Docs`** is the **user-facing documentation**.

## (A) Update Second-Brain documentation

Map the changed artifact to the right doc(s) in `3-Resources/Second-Brain/` (and under `Docs/` when adding or updating system documentation):

- Rules → Rules.md (tables and diagrams)
- Skills → Skills.md
- Pipelines / trigger mapping → Pipelines.md
- Plugins → Plugins.md
- MCP tools/config → MCP-Tools.md, Configs.md
- Parameters (confidence, queue modes, log format) → Parameters.md
- Log destinations or error format → Logs.md
- Vault layout or exclusions → Vault-Layout.md
- Queue sources or modes → Queue-Sources.md
- Templates or formatting standards → Templates.md
- High-level flow or safety → Backbone.md

Refresh **Mermaid diagrams** in those docs so they stay accurate.

## (B) Sync rules and skills to .cursor/sync/

When a file under `.cursor/rules/always/`, `.cursor/rules/context/`, or `.cursor/skills/<name>/` is created, renamed, or its content is changed, **update the corresponding file under `.cursor/sync/`** and optionally append an entry to **`.cursor/sync/changelog.md`** (rule/skill name, version, one-line change).

- `.cursor/rules/always/<name>.mdc` ↔ `.cursor/sync/rules/always/<name>.md`
- `.cursor/rules/context/<name>.mdc` ↔ `.cursor/sync/rules/context/<name>.md`
- `.cursor/skills/<name>/SKILL.md` ↔ `.cursor/sync/skills/<name>.md`

Copy or convert content as needed (e.g. .mdc → .md); preserve meaning. If a rule or skill is removed, remove the corresponding sync file. Ensure `.cursor/sync/` stays in sync with `.cursor/rules/` and `.cursor/skills/` whenever those are modified.

## Intent

Keep `3-Resources/Second-Brain/` as the single source of truth for backbone documentation; keep `.cursor/sync/` as the synced copy of rules and skills for reference or tooling. Whenever behavior or structure changes, update both the docs (and diagrams) and the sync folder in the same pass or as an immediate follow-up.

See [[3-Resources/Second-Brain/README|Second-Brain README]].
