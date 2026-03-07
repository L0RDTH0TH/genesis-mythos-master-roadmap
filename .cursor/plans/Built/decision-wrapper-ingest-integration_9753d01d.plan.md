---
name: decision-wrapper-ingest-integration
overview: Integrate a decision-wrapper flow into the ingest pipeline so low/mid-confidence notes generate explicit decision wrappers and feed back into guidance-aware EAT-QUEUE runs.
todos: []
isProject: false
---

### Goals

- **Replace** the current low-confidence ingest behavior with your new **Decision Wrapper** flow.
- **Wire wrappers** into guidance-aware + feedback-incorporate so EAT-QUEUE can apply user decisions.
- **Keep safety invariants** (backup, snapshot, dry-run) and update docs/sync for backbone consistency.

### Implementation Plan

- **Update ingest rule (`.cursor/rules/context/para-zettel-autopilot.mdc`)**
  - Replace the existing **“When no move (manual review)” + “Low-confidence decision candidates”** section with your new **Decision Wrapper** logic.
  - In the **confidence bands** section, change the mid/low-band outcome so that instead of just logging `#review-needed` and stopping, the pipeline:
    - Detects `ingest_conf < 85` **or** multiple strong classify candidates.
    - Calls `classify_para` with `mode: "top_candidates", max_candidates: 5`.
    - Creates a wrapper note at `Ingest/Decisions/Decision-for-{{original_slug}}--{{YYYY-MM-DD-HHMM}}.md` using your provided template (including `proposal_path`, ranked candidates, and “Your action” instructions).
    - Updates the original note’s frontmatter with `decision_candidate: true`, `proposal_path`, and `decision_priority` (high for <72, medium otherwise).
    - Logs the `#decision-wrapper-created` flag and wrapper path to `Ingest-Log.md`.
    - Explicitly **stops processing** the note (no split/distill/move) once the wrapper is created.
- **Define Decision Wrapper template (optional Template note)**
  - Add a new template file at `3-Resources/Templates/Decision-Wrapper.md` (or your preferred Templates path) containing exactly the wrapper layout you pasted (frontmatter + ranked candidates section + actions instructions).
  - Document in the ingest rule that wrappers may be rendered from this template so the behavior stays discoverable.
- **Extend `feedback-incorporate` skill for wrappers**
  - In `.cursor/skills/feedback-incorporate/SKILL.md`, add a short section describing wrapper handling:
    - When a queue entry’s `source_file` is a wrapper under `Ingest/Decisions/`, read its frontmatter.
    - If `approved: true`, or `approved_option` / `approved_path` is set, emit an object on the skill’s output (or in context) with:
      - `target_path` (resolved from `approved_option` → candidate path or `approved_path` string).
      - `guidance_text` derived from wrapper “Thoughts / corrections” block.
      - A recommended `guidance_conf_boost` (e.g. 18) to be applied on the next ingest run for that original note.
    - Ensure this remains **read-only** (no updates to notes; the queue processor / ingest pipeline will do the writes and moves).
  - Clarify how the skill maps wrapper → original note (using the `original_note` link and/or `proposal_path`).
- **Wire wrapper decisions into ingest/EAT-QUEUE flow**
  - Update the ingest/eat-queue driver logic (where it already calls `feedback-incorporate`) so that when it sees wrapper-derived output:
    - It loads `user_guidance` (from wrapper thoughts) into the **original note** context per `guidance-aware.mdc`.
    - It applies `guidance_conf_boost` (e.g. 18) and a **hard target path** into `subfolder-organize` / move decision for the original note.
    - It re-runs ingest on the original note, now in guidance-aware mode, with the usual backup + snapshot + dry-run chain unchanged.
    - Optionally mark the wrapper `approved: true` or move/archive it after successful ingestion, per your preference.
- **Backbone docs + sync updates**
  - In `3-Resources/Second-Brain/Pipelines.md` (or the relevant ingest section), briefly document the new decision-wrapper behavior and how wrappers feed into guidance-aware ingest.
  - If you keep a dedicated note for templates, add a short entry describing `Decision-Wrapper` and its location.
  - Mirror changes in `.cursor/sync/` for:
    - `rules/always|context/para-zettel-autopilot`.
    - `skills/feedback-incorporate`.
  - Ensure any ingest diagrams (Mermaid flows) show the **low/mid-confidence → Decision Wrapper → EAT-QUEUE (guidance-aware)** loop.

### Todos

- **update-ingest-rule-wrapper**: Replace the low/mid-confidence branch in `para-zettel-autopilot.mdc` with the Decision Wrapper flow and exact template you specified.
- **add-decision-wrapper-template**: Create a `Decision-Wrapper` template note under Templates with the same wrapper structure.
- **extend-feedback-incorporate-wrappers**: Update `feedback-incorporate` skill spec to interpret `approved_option` / `approved_path` from wrapper notes and emit target path + guidance data.
- **wire-queue-to-ingest-wrapper-loop**: Adjust EAT-QUEUE / ingest driver code so wrapper approvals re-run ingest on the original note with guidance-aware + `guidance_conf_boost` and a hard target path.
- **sync-docs-and-rules**: Update Second-Brain docs and `.cursor/sync/` copies to reflect the new decision-wrapper-based ingest behavior.

