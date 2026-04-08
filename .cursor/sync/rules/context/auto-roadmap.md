---
description: "Roadmap behavior moved to RoadmapSubagent. ROADMAP MODE and RESUME-ROADMAP are handled by agents/roadmap.mdc; this file is kept for rollback and reference."
globs: []
alwaysApply: false
---

# Auto-roadmap (context rule) — superseded by RoadmapSubagent

- **Default handler**: **ROADMAP MODE** and **RESUME-ROADMAP** (and aliases) are executed by the **RoadmapSubagent** ([agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)). The Queue subagent dispatches ROADMAP MODE and RESUME-ROADMAP entries to that rule after normalization, bootstrap, and Step 0.
- **When this file is the active handler** (e.g. after rollback): Run the full roadmap flow as previously defined; restore full content from version control or backup for rollback.
- **Reference**: Cursor-Skill-Pipelines-Reference, Queue-Sources, [agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc).

## How to activate (delegated to RoadmapSubagent)

When the queue or user triggers **ROADMAP MODE** or **RESUME-ROADMAP** and **this rule** is the active handler (e.g. after rollback), run the full behavior that is now in [agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc).
