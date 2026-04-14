---
title: Backup and Recovery Strategy
created: 2026-04-09
updated: 2026-04-12
tags: [ops, backup, git, syncthing, curator, recovery, trash]
para-type: Resource
status: active
---

# Backup and Recovery Strategy

**TL;DR** — **Curator** (`main`) = private full-vault git history published from a dedicated private export checkout (`/home/darth/Documents/gmm-curator-export`); **Cursor/MCP agents** end file-modifying sessions with **`./scripts/curator_snapshot.sh`** (mirror vault -> private export commit + push to **`curator main`**) per [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]]. **Obsidian Git** (optional) = operator convenience debounced commits — **not** the agent backup spine. **Syncthing** = fast sync (use **`.stignore`** for **`.git/`**); **OS snapshots** = point-in-time safety; **`gmm-roadmap-export`** = **selective public** mirror via **GitForge** only. **No raw shell deletes** — use **move-to-trash** (`.trash/` + manifest). Restore order: **Curator** → **Obsidian trash / File Recovery** → **OS snapshot**.

---

## Recovery layers (stack)

| Layer | Role | Recoverable? |
|-------|------|----------------|
| **1. Curator (private git, branch `main`)** | Full vault tree; default undo for catastrophic edits. | **Yes** — clone / `git reset --hard` / revert |
| **2. Obsidian Git** (optional operator tool) | Debounced auto commit + push if you enable the plugin; not required for agent backup. | **Yes** — when pushed to Curator |
| **3. Syncthing** | Live replication across devices. | **Partial** — not authoritative vs git |
| **4. Obsidian trash + File Recovery** | In-app deleted notes; core **File Recovery** plugin (short interval, longer retention). | **Partial** — note-level |
| **5. OS-level** | Windows File History, VSS; macOS Time Machine; etc. | **Yes** — whole-folder / volume |
| **6. `gmm-curator-export`** | Private export checkout that pushes full-vault mirrors to **Curator `main`**. | **Yes** — private full-vault backup lane |
| **7. `gmm-roadmap-export`** | Publish to **`genesis-mythos-master-roadmap`** per [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]. | **Selective** — not a private full-vault backup |

**Naming discipline:** Curator default branch **`main`**. Do **not** name Curator’s branch **`iteration-2-roadmap-rules`** unless intentional — that name is the **public integration** branch on **`genesis-mythos-master-roadmap`**.

---

## Restore playbook (order matters)

1. **Git / Curator:** `git fetch` + `git reset --hard` to known-good **`main`** (or specific SHA) on the machine that holds the vault clone. Resolve or stash **uncommitted** work first.
2. **Obsidian:** **Settings → File Recovery** (core plugin); recover from **Obsidian trash** (if notes were deleted through the app with **Move to Obsidian trash**).
3. **OS snapshot:** Restore folder or file from File History / Shadow Copy / Time Machine when git and Obsidian are insufficient.

If **git is missing** from disk: restore from zip / Syncthing / OS backup, then **`git init`**, add remote **`curator`**, fetch, reconcile.

**Syncthing vs git conflict:** Prefer **Curator** as authority; merge Syncthing deltas deliberately.

---

## Move-to-trash policy (agents and shell)

- **No raw deletes:** Do **not** run **`rm`**, **`rm -rf`**, **`find ... -delete`**, or shell **`unlink`** on vault paths. See [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety Invariants]] and [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]].
- **Rewrite:** Move targets to **`.trash/<YYYYMMDD-HHMMSS>/…`** and append **`.trash/TRASH-MANIFEST.log`**. Use **`./scripts/move-to-trash.sh`** from vault root when shell is required.
- **Permanent emptying of `.trash/`** is **operator-only** with explicit confirmation — not an agent step.

---

## Obsidian settings (operator — mandatory in docs)

- **Files & Links → Deleted files:** **Move to Obsidian trash** (not permanent delete).
- Enable core **File Recovery** plugin; set a **short** recovery interval and adequate **retention** for your risk tolerance.

---

## Operator setup: Curator remote and first push (human)

Run in the **private export checkout** (adjust path). Prefer remote name **`curator`** for clarity vs other remotes:

```bash
cd /home/darth/Documents/gmm-curator-export
git status   # if not a repo: git init
git remote add curator git@github.com:L0RDTH0TH/Curator.git
# or: git remote add curator https://github.com/L0RDTH0TH/Curator.git
git branch -M main
git add -A
git commit -m "chore: bootstrap full vault backup to Curator (post-recovery) - $(date -Iseconds)"
git push -u curator main
```

If you already use **`origin`** for Curator, **`git push -u origin main`** is equivalent; **`./scripts/curator_snapshot.sh`** prefers remote **`curator`**, then falls back to **`origin`**.

1. **Cursor/MCP:** after substantive edits, agents run **`./scripts/curator_snapshot.sh`** automatically (see [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]]); the script mirrors vault content into **`/home/darth/Documents/gmm-curator-export`** then pushes Curator. Operator only does **one-time** remote add + bootstrap push above.
2. **Obsidian Git (optional):** if you use the plugin, point at the same remote; debounced sync; pull on startup.
3. **`.stignore`:** Consider **`.git/`** (and **`.obsidian/workspace*`)** if Syncthing must not sync git objects — see [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]].
4. **Manual:** **`./scripts/curator_snapshot.sh "message"`** anytime — same commit + push to **`curator`** or **`origin`**.

---

## GitHub Actions on Curator (expectations)

Scheduled workflows only see commits **already on GitHub**. Use for **staleness alerts**, not for recovering **unpushed** local work. See prior section in this doc (health-check only).

---

## Relationship to GitForge and export

- **GitForge** pushes **selective public export** via **`gmm-roadmap-export`** to **`genesis-mythos-master-roadmap`** / **`iteration-2-roadmap-rules`** — **not** Curator. Do not confuse remotes or ad-hoc push from the vault to the public integration branch.
- **Curator** = private **full-vault** backup on **`main`** via **`/home/darth/Documents/gmm-curator-export`**; **operator** performs **initial** `git remote` + first **`git push`** only.
- **Agents** own ongoing **post-task** **`git commit` + `git push`** to **Curator** via **`curator_snapshot.sh`**; that is parallel in intent to GitForge’s post–EAT-QUEUE export discipline, applied to the **entire vault**.
- **Operator publish order** (Curator snapshot **before** export checkout / public push): follow [[.cursor/skills/vault-git-publish-checklist/SKILL.md|vault-git-publish-checklist]]; use [[.cursor/skills/gitforge-operator/SKILL.md|gitforge-operator]] for GitForge orientation and manual-debug steps.

---

## Safe post-task snapshot (validation example)

**Clean tree (nothing to send):**

```bash
git status --porcelain   # empty
./scripts/curator_snapshot.sh "no-op check"
# prints: curator_snapshot: nothing to commit — exit 0
```

**After vault edits:**

```bash
git status --porcelain   # lists changed paths
./scripts/curator_snapshot.sh "short task label"
# commits with: auto: <ISO8601> — Cursor task: short task label
# git push -u curator main  (or origin if curator missing)
```

**Failure:** if **`git push`** fails or the script exits non-zero → agents report **`task_error`** and **do not** claim Success (see [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]]).

---

## In-vault mirrors (Obsidian-visible, backup-only)

**`.technical/`** is often excluded from Obsidian; **JSONL** queues and root **`.cursorignore`** are still mirrored to **Curator** on disk but easy to miss after a bad session. Small **duplicate** copies for recovery visibility (not authoritative) live under [[3-Resources/Second-Brain/Backup-Mirrors-Curator/README|Backup-Mirrors-Curator]]. Refresh those files when canonical paths change, then run **`./scripts/curator_snapshot.sh`**.

---

## Cross-links

- [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety Invariants]] — move-to-trash; MCP gates
- [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]] — blacklist `rm` / `find -delete`
- [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]] — mandatory post-edit Curator commit+push
- `scripts/move-to-trash.sh` — shell move-to-trash helper
- `scripts/curator_snapshot.sh` — agent-mandatory commit + push (operators may run manually too)
- [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] — `vault_backup`
- [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] — `.stignore`, Syncthing
- [[3-Resources/Second-Brain/Backup-Mirrors-Curator/README|Backup-Mirrors-Curator]] — in-vault duplicates of `.technical` queues + `.cursorignore`
