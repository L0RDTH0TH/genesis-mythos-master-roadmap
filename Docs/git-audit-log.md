---
title: Git audit log (GitForge)
created: 2026-04-04
tags: [ops, git, gitforge, audit]
para-type: Resource
status: active
source: Second-Brain automation
links:
  - "[[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]]"
  - "[[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]"
---

# Git audit log

Append-only operator and **GitForge** trail for vault / export git actions. **GitForge** (when enabled and **`effective_pipeline_mode`** is **`balance`** or **`quality`**) appends one structured block per invocation after **EAT-QUEUE** **A.7** per [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.7a**. **`speed`** runs do not invoke GitForge (no audit line from GitForge for that path).

## Append schema (one block per run)

Use a level-3 heading per event for scanability:

```markdown
### YYYY-MM-DD HH:MM UTC — gitforge | completed | skipped | failed

| Field | Value |
|-------|--------|
| mode | fast \| balance \| extreme |
| branch_context | git branch name or unknown |
| queue_success | true \| false |
| actions | audit_logged; commit_attempted; push_attempted; export_sync_attempted (subset) |
| vault_root | path |
| eat_queue_run_id | id or — |
| result | short summary |
| error_excerpt | sanitized one line if failed |
```

**Human operators** may add similar `###` rows for manual commits/pushes when GitForge is disabled.

## Related

- Agent contract: `.cursor/agents/gitforge.md`
- Config: [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] § **gitforge**

### 2026-04-04 23:59 UTC — gitforge | pending_clarifier

| Field | Value |
|-------|--------|
| mode | balance |
| branch_context | iteration-2-roadmap-rules |
| queue_success | true |
| actions | audit_logged |
| vault_root | /home/darth/Documents/Second-Brain |
| export_repo_root | /home/darth/Documents/gmm-roadmap-export |
| eat_queue_run_id | eatq-20260404T235959Z-l1-default-audit |
| result | `clarifier_input` absent per balance contract — no commit, no push, no tag. `export_sync` skipped (Config `balance.export_sync: false`). Note: working tree has extensive local changes; `iteration-2-roadmap-rules` has no git upstream. |
| error_excerpt | — |
