---
name: conceptual-decision-record
description: Creates one atomized note under Roadmap/Conceptual-Decision-Records with PMG alignment, alternatives, validation evidence; create-only MCP. Used after conceptual-track roadmap-deepen success.
---

# conceptual-decision-record

## When to use

- After a **successful** **roadmap-deepen** step when **`active_track === conceptual`** and **`roadmap.conceptual_decision_record_mode`** is not **`off`** (read from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] **`roadmap.conceptual_decision_record_mode`**, with optional override **`params.conceptual_decision_record_mode`** on the queue entry). Allowed values: **`off`** \| **`best_effort`** (default) \| **`required`**.
- Optionally from other conceptual actions (**advance-phase**, **expand**, **recal**) when the RoadmapSubagent records a design decision and needs a companion file—same shape.

## Inputs

- **project_id** (required): Project slug.
- **parent_roadmap_note** (required): Vault path or wikilink to the **primary** phase note created or targeted this run (the main artifact of the deepen).
- **decision_kind** (optional): default **`deepen`**.
- **queue_entry_id** (optional): From queue / hand-off when available.
- **master_goal** (optional): Wikilink to PMG / master goal. If absent, resolve from `1-Projects/<project_id>/Roadmap/roadmap-state.md` body line **`Source master goal:`** or from **`Roadmap/distilled-core.md`** § **Phase 0 anchors** → **Master goal** link.
- **chosen_summary** (required): 1–3 sentences describing what was chosen.
- **pmg_alignment** (required): How the choice serves the master goal.
- **alternatives** (required): At least one row or bullet list; each alternative **name**, **upside**, **downside**, **why not chosen**.
- **evidence_links** (required): Bullets with wikilinks to vault notes, **`Ingest/Agent-Research/`** synth notes, or short **pattern** citations (named practice). If no external evidence exists, set **`validation_status: pattern_only`** or **`needs_human`** in frontmatter—never fabricate citations.
- **injected_research_paths** (optional): Array of paths from pre-deepen research; add to **`related_research`** in frontmatter and **Validation evidence** body.
- **workflow_state_anchor** (optional): Short cite of last Log row (Timestamp + Target) for **Links** section.

## Mode behavior

| Mode | Behavior |
|------|----------|
| **off** | Caller skips invoking this skill. |
| **best_effort** | Create the note; on MCP/create failure, log to [[3-Resources/Errors|Errors.md]] with **`error_type: conceptual-decision-record-failed`**; **do not** fail the parent deepen. |
| **required** | Create the note; on failure, return **failure** to the caller so roadmap-deepen / RoadmapSubagent treats the run as **failed** (queue entry retained). |

## Instructions

1. **Resolve mode:** `effective_mode = params.conceptual_decision_record_mode ?? config['roadmap']['conceptual_decision_record_mode'] ?? 'best_effort'`. If **`off`**, return immediately with `{ skipped: true, reason: "mode_off" }`.
2. **`obsidian_ensure_structure`** for `folder_path`: `1-Projects/<project_id>/Roadmap/Conceptual-Decision-Records`.
3. **Filename:** `deepen-<slug-fragment>-<YYYY-MM-DD-HHMM>.md` (from target note slug or phase folder + local time per [[3-Resources/Second-Brain/Parameters|Parameters]] § Timestamp resolution).
4. **Create** the note via **`obsidian_update_note`** with **`mode: create`** (or server-supported create) at  
   `1-Projects/<project_id>/Roadmap/Conceptual-Decision-Records/<filename>.md`.  
   Populate YAML frontmatter: `title`, `created`, `tags`, `para-type: Project`, `project-id`, **`parent_roadmap_note`**, **`decision_kind`**, **`queue_entry_id`**, **`master_goal`**, **`validation_status`**, **`related_research`** (array).  
   Body: **Summary**, **PMG alignment**, **Alternatives and tradeoffs** (table), **Validation evidence**, **Links** (match scaffold in `Templates/Roadmap/Conceptual-Decision-Record.md`).
5. **Do not** read or modify frozen parent bodies for this purpose—**create only**.
6. **Return:** `{ path: "<full vault path>", created: true }` or `{ created: false, error: "..." }`.

## decisions-log append (optional; caller may delegate)

If the **caller** (e.g. **roadmap-deepen**) appends to **`decisions-log.md`**, ensure **`## Conceptual autopilot`** exists (create section after `## Decisions` if missing). Append one bullet:

```markdown
- **Decision record (deepen):** [[Conceptual-Decision-Records/<filename>]] — `queue_entry_id: <id>` — validation: <cited|pattern_only|needs_human>
```

Regex for parsers (see [[3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention|Decisions-Log-Operator-Pick-Convention]]): `Decision record \((deepen|advance-phase|expand|recal|track_flip|other)\):`

## Reference

- [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] § Conceptual-Decision-Records
- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]
- [[.cursor/rules/context/dual-roadmap-track.mdc|dual-roadmap-track]]
