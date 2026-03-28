---
name: Roadmap todo coordination gap
overview: Align the Layer 2 Task prompt and the todo-orchestrator skill with the canonical Todo orchestration already defined in `roadmap.mdc`, and fix `sync/rules/agents/roadmap.md` so it mirrors the `.mdc` (not the Task agent file), per sync README.
todos:
  - id: agents-roadmap-todo-section
    content: Replace vague TodoWrite paragraph in .cursor/agents/roadmap.md with full Todo orchestration block matching roadmap.mdc
    status: completed
  - id: skill-todo-orchestrator-roadmap
    content: "Update todo-orchestrator SKILL.md: ROADMAP_MODE phases, rename snapshot phase to snapshot-and-log, cross-link roadmap.mdc"
    status: completed
  - id: sync-backbone
    content: Regenerate .cursor/sync/skills/todo-orchestrator.md; replace sync/rules/agents/roadmap.md with roadmap.mdc export; changelog entry
    status: completed
isProject: false
---

# Close roadmap todo coordination gap

## Problem (current state)

- **Canonical spec already exists:** `[.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)` § **Todo orchestration (todo-orchestrator)** (lines 36–55) defines `run_id`s (`roadmap-setup` / `roadmap-resume`) and phase ids for **ROADMAP_MODE** (`resolve-project`, `bootstrap-state`, `generate-from-outline`) and **RESUME_ROADMAP** (`load-state`, `determine-action`, `apply-action`, `snapshot-and-log`, `queue-followup-if-needed`), plus the same completion/cancel invariants as other pipelines.
- **Gap 1 — Task context:** `[.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)` still uses a **vague** one-line **TodoWrite** example (`read-params`, `branch-by-action`, …) that **does not match** the rule file or `[.cursor/skills/todo-orchestrator/SKILL.md](.cursor/skills/todo-orchestrator/SKILL.md)`. The Queue `Task` hand-off loads this agent file; models may never see `.mdc` content, so coordination with Layer 1’s “todo-orchestrator block” stays weak.
- **Gap 2 — skill drift:** `todo-orchestrator` lists only **RESUME** phases and uses phase id `**snapshot-and-update-state`** while `roadmap.mdc` uses `**snapshot-and-log`**. It does **not** document **ROADMAP_MODE** setup phases at all.
- **Gap 3 — sync hygiene:** Per `[.cursor/sync/README.md](.cursor/sync/README.md)`, `[.cursor/sync/rules/agents/roadmap.md](.cursor/sync/rules/agents/roadmap.md)` should mirror `**.cursor/rules/agents/roadmap.mdc`**. Today it incorrectly duplicates `**.cursor/agents/roadmap.md`** (YAML frontmatter + Task prompt), unlike e.g. `[.cursor/sync/rules/agents/queue.md](.cursor/sync/rules/agents/queue.md)` which correctly mirrors `queue.mdc`.

**Explicitly out of scope (architecture):** Parent/child **verification** of todo state (structured return field, parsing) — no change unless you later want a new contract.

## Implementation steps

### 1. Harden the Task agent prompt

In `[.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)`, **replace** the single **TodoWrite** paragraph (currently ~line 16) with a `**## Todo orchestration (todo-orchestrator)`** section that is **verbatim or near-verbatim** the same bullets as `roadmap.mdc` § Todo orchestration: run_ids, both mode phase lists, `TodoWrite` transition rules, and “must not return Success with pending/in_progress”.

- Place it **after** the opening safety/pre-deepen paragraphs and **before** the first `---` / `## RESUME action` so it is visible early in the prompt.
- Keep a one-line pointer: **canonical duplicate** lives in [[.cursor/rules/agents/roadmap.mdc|roadmap.mdc]] § Todo orchestration (for humans/tools that diff rules vs agents).

### 2. Align `todo-orchestrator` with `roadmap.mdc`

In `[.cursor/skills/todo-orchestrator/SKILL.md](.cursor/skills/todo-orchestrator/SKILL.md)`, under **Recommended phase sets → RoadmapSubagent**:

- Add a **ROADMAP_MODE (setup)** subsection with the three phases from `roadmap.mdc` (`resolve-project`, `bootstrap-state`, `generate-from-outline`) and short descriptions matching the rule text.
- In the **RESUME_ROADMAP** list, rename `**snapshot-and-update-state`** → `**snapshot-and-log`** and align the gloss with `roadmap.mdc` (state snapshots, workflow/roadmap updates, associated logging).
- Add a single cross-link sentence: normative detail for roadmap also in `roadmap.mdc` § Todo orchestration.

### 3. Backbone sync

- Regenerate `[.cursor/sync/skills/todo-orchestrator.md](.cursor/sync/skills/todo-orchestrator.md)` from the updated `SKILL.md` (same content policy as other skills).
- **Replace** `[.cursor/sync/rules/agents/roadmap.md](.cursor/sync/rules/agents/roadmap.md)` with a faithful markdown export of `[.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)` (same pattern as `queue.md`: frontmatter + body; `.mdc` → `.md` conversion only).
- Append a line to `[.cursor/sync/changelog.md](.cursor/sync/changelog.md)`: roadmap agent todo alignment + skill sync + sync folder fix for `rules/agents/roadmap.md`.

### 4. Optional (low priority)

- **Legacy rule:** `[.cursor/rules/legacy-agents/roadmap.mdc](.cursor/rules/legacy-agents/roadmap.mdc)` — add a short “see `agents/roadmap.mdc` § Todo orchestration” note only if you still rely on legacy for rollback; README says legacy is not copied to sync.
- **Vault docs:** One sentence in [3-Resources/Second-Brain/Docs/Subagent-Layers-Reference.md](3-Resources/Second-Brain/Docs/Subagent-Layers-Reference.md) tying Layer 2 roadmap todos to `roadmap.mdc` — only if you want user-facing docs updated; not required to close the structural gap.

## Verification

- Diff: `agents/roadmap.md` phase ids **match** `roadmap.mdc` and `todo-orchestrator`.
- `sync/rules/agents/roadmap.md` starts with `description:` / `globs:` / `alwaysApply` from `.mdc`, **not** `name: roadmap` / `model: inherit` from the Task file.
- No change to Queue dispatch architecture; `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)` already requires a todo-orchestrator block referencing RoadmapSubagent phases.

