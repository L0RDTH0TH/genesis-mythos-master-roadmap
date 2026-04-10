---
description: "Mandatory post-edit: snapshot vault into private export checkout and push Curator main via curator_snapshot.sh. Pairs with execution-safety-blacklist. Does not replace GitForge public export."
globs: []
alwaysApply: true
---

# Curator mandatory backup (terminal session step)

- **Role:** Cursor/MCP agents **own** post-task git hygiene on the private **Curator** repo (`main`). After any substantive **vault file mutation** (notes, rules, queues, scripts, config, `.technical` bundles, etc.), the agent **must** run the backup tail **before** reporting **Success** or ending the session.
- **With:** [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]] — **no** raw `rm` / `find -delete`; **delete intent** → **`.trash/`** + **`scripts/move-to-trash.sh`**. See [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety Invariants]].
- **Does not replace:** [[.cursor/agents/gitforge|GitForge]] (post–**A.7** selective export to **`gmm-roadmap-export`** / public remote per [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]). **Never** ad-hoc **`git push`** from the vault to **`genesis-mythos-master-roadmap`** or **`iteration-2-roadmap-rules`** — that is **export checkout + GitForge** only. **Curator** = private full-vault backup via **`vault_backup.private_export_repo_root`**; **GitForge** = public contract mirror via **`gitforge.export_repo_root`**.

## Mandatory steps (in order)

1. **`git status --porcelain`** at the vault root (or rely on known edits from the task) to detect what the snapshot must mirror.
2. If the working tree has **no** changes: **backup step passes** (idempotent).
3. If there **are** changes: run **`./scripts/curator_snapshot.sh "<short task summary>"`** from vault root. It mirrors vault content into **`vault_backup.private_export_repo_root`**, commits there, and pushes **`curator main`**. One commit per logical task; commit message format is enforced by the script (`auto: <ISO8601> — Cursor task: …`).
4. **Failure handling:** If **`curator_snapshot`** exits non-zero, **`git push` fails**, the path is not a git work tree, or the tree is still dirty after a failed attempt → report **`task_error`**, **halt**: **do not** claim Success, **do not** continue orchestration or further file mutations.
5. **Operator bootstrap:** One-time **`git remote add curator …`**, **`git push -u curator main`** is **operator-only** — see [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]].

## Debounce

Prefer **one commit per logical task** or end-of-session, not per micro-edit — matches [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]].

## Cross-links

- [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]]
- [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety Invariants]]
- [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]]
