---
description: Frozen conceptual roadmap notes — no destructive MCP; execution subtree writes; RESUME_ROADMAP unfreeze action exception.
alwaysApply: true
globs: []
---

# Dual roadmap track (frozen conceptual + execution subtree)

When a note has **both** `frozen: true` and `roadmap_track: conceptual` in frontmatter (or path is under `1-Projects/*/Roadmap/` **excluding** `Roadmap/Execution/` and the project’s `roadmap-state.md` has `roadmap_track: execution` — treat unstamped legacy notes under conceptual tree as frozen only after human has set freeze stamps per Vault-Layout checklist):

## Destructive MCP (blocked)

Do **not** perform on frozen conceptual roadmap notes:

- `obsidian_update_note` that overwrites body (except narrow append-only audit if a future spec explicitly allows it — default **no**)
- `obsidian_move_note`, `obsidian_rename_note`, `obsidian_delete_note`
- `obsidian_split_atomic`, structural `obsidian_distill_note`, `obsidian_append_to_hub` into frozen notes

**Reads** (`obsidian_read_note`, search, list) are always allowed. Do **not** use `.cursorignore` to hide `Roadmap/` — keep files readable.

## Execution track

When **`roadmap_track: execution`** on `…/Roadmap/roadmap-state.md`, deepen/recal **writes** go under `…/Roadmap/Execution/` per **roadmap-deepen** and **RoadmapSubagent**. Use `workflow_state-execution.md` and `roadmap-state-execution.md` for execution iteration state.

## Conceptual-Amendments (post-freeze companion notes)

When conceptual phase notes are **frozen**, **do not** overwrite their bodies for new design direction. **Create** atomized notes under `1-Projects/<project_id>/Roadmap/Conceptual-Amendments/` (ensure folder via MCP), **one note per section-level change**, with frontmatter **`parent_roadmap_note`** and **`amends_section`** per [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Conceptual-Amendments. This is **non-destructive** (new file); allowed even when parent notes are frozen.

## Conceptual-Decision-Records (rationale per decision)

On the **conceptual** track, **create** atomized notes under `1-Projects/<project_id>/Roadmap/Conceptual-Decision-Records/` (ensure folder via MCP), **one note per meaningful decision** (e.g. successful **deepen**), per [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Conceptual-Decision-Records. **Non-destructive** (new file only); allowed even when parent phase notes are **frozen**.

## Exception

**`RESUME_ROADMAP` with `params.action: unfreeze_conceptual`** (with explicit user approval / wrapper per Queue-Sources) may authorize edits to previously frozen conceptual notes. Until then, route fixes through **execution mirrors** or **advisory** outputs (Errors.md, Decision Wrappers, validator reports).

## Pipelines

**DISTILL, EXPRESS, ORGANIZE, ARCHIVE, INGEST** (destructive branches): before mutating a note, if path matches `**/Roadmap/**` and not `**/Roadmap/Execution/**`, read frontmatter; if `frozen: true` and `roadmap_track: conceptual`, **skip** destructive steps for that note and log `#review-needed` or advisory.

## Cross-links

- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]
- [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Dual roadmap track
- [[3-Resources/Second-Brain/Parameters|Parameters]] § Dual roadmap track
