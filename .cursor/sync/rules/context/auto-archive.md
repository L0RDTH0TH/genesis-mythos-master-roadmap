---
description: "Archive behavior moved to ArchiveSubagent. ARCHIVE MODE handled by agents/archive.mdc; kept for rollback."
globs: []
alwaysApply: false
---

# Auto-archive (context rule) — superseded by ArchiveSubagent

- **Default handler**: ARCHIVE MODE, archive this note, send to Archives, move completed to 4-Archives → **ArchiveSubagent** (agents/archive.mdc). Rollback: restore full content from version control. Reference: agents/archive.mdc, Cursor-Skill-Pipelines-Reference.
