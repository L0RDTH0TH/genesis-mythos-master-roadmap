---
name: Phase 1 stabilizers add to plan
overview: "Add two Phase 1 post-process stabilizers to the existing targeted heuristics plan: (1) name-enhance tie-breaker forking the ingest pattern, and (2) split/atomicity proposal heuristic in the ingest chain. Both are low-risk, proposal-first, and gated by existing confidence and safety."
todos: []
isProject: false
---

# Phase 1 Additions to Post-Process Stabilizers Plan

Add **two new sections** to [.cursor/plans/targeted_heuristics_for_consistency_a2535b19.plan.md](.cursor/plans/targeted_heuristics_for_consistency_a2535b19.plan.md) as Phase 1 items, and update the plan’s overview, “Where stabilizers live”, rollout, and diagram accordingly.

---

## 1. Name-enhance tie-breaker (new section in plan)

**Placement in plan:** Insert as new **§1b** (or renumber as §5 and §6; existing §2–4 become §3–5). Alternatively add as subsections under a new “Phase 1 additions” block after §4 (Queue dispatch) and before §5 (Rollout).

**Content to add:**

- **Where:** After name-enhance produces multiple candidate filenames (or when re-ranking suggested names); same skill family as ingest (subfolder-organize → name-enhance). Used in **organize** and **NAME-REVIEW** queue; ingest already uses suggested_name from name-enhance without applying rename.
- **Technique (tie-break order):**
  1. Prefer candidate that **matches [Naming-Conventions](3-Resources/Second-Brain/Naming-Conventions.md)** format: `kebab-slug-YYYY-MM-DD-HHMM` (slug first, date-time at end).
  2. If tied: **shorter slug length** (fewer chars).
  3. If still tied: **alphabetically first** slug.
- **Frontmatter:** When heuristic re-ranks or picks a name: set `heuristic_adjusted: true`, `heuristic_reason: "name-enhance tie-breaker per Naming-Conventions"` on the note (or in the name-enhance output structure used by the pipeline).
- **Logging:** Log to **Organize-Log** or **Name-Review-Log** (per [Logs](3-Resources/Second-Brain/Logs.md)) with a line that includes e.g. `heuristic: name-enhance tie-breaker applied`, old_stem, suggested_name, confidence.
- **Ownership:** [name-enhance](.cursor/skills/name-enhance/SKILL.md) skill — add a post-process block that applies the tie-break when multiple valid names exist; same pattern as ingest path re-rank (deterministic, no new skill file).
- **Safety:** Renames (or propose-only in ingest) already gated by existing confidence + dry_run + snapshot per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc); name-enhance already documents apply only at ≥85% (organize/name-review). Zero new risk.
- **Tests / measurement:** NAME-REVIEW queue runs; add a row to [Regression-Stability-Log](3-Resources/Second-Brain/Regression-Stability-Log.md) for filename flip-rate or consistency metric if desired.

**Rationale (for plan wording):** Directly extends the ingest/organize stabilizer; high user-visible variance (flaky filenames); low effort (copy ingest tie-breaker, swap PARA rubric for Naming-Conventions rules).

---

## 2. Split / atomicity proposal heuristic (new section in plan)

**Placement in plan:** Insert as new section (e.g. **§1c** or §6) after name-enhance and before §2 (Distill), so both ingest-chain items are grouped.

**Content to add:**

- **Where:** In full-autonomous-ingest chain, **before** `obsidian_split_atomic` is called (or as a thin pre-step that proposes split points). Current flow: classify_para → … → subfolder-organize → (confidence gate) → **split_atomic** → split-link-preserve → distill_note → … ([Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md), [Pipelines](3-Resources/Second-Brain/Pipelines.md)).
- **Technique (deterministic proposal rules):**
  - **Prefer splits at H2/H3 headings** (e.g. `##` , `###` ).
  - If **multiple same-level headings** qualify: take **first occurrence** (document order).
  - **Tie-break:** **shorter heading text first** (more atomic intent).
  - If **no clear headings:** propose **single split at ~400–600 word boundary** (configurable in [Second-Brain-Config](3-Resources/Second-Brain-Config.md) or [Parameters](3-Resources/Second-Brain/Parameters.md), e.g. `split_fallback_word_boundary_min: 400`, `split_fallback_word_boundary_max: 600`).
- **Behaviour:** Heuristic is **100% proposal-only** when confidence < 85%: output proposed split points and add **#review-needed** callout; **do not** call `obsidian_split_atomic`. When confidence ≥ 85%, pipeline may use the proposed points to inform the MCP call (or leave MCP to decide); existing snapshot-before-split and confidence gates unchanged.
- **Ownership:** Either (a) logic inside [para-zettel-autopilot](.cursor/rules/context/para-zettel-autopilot.mdc) that runs before `obsidian_split_atomic`, or (b) a **tiny post-split processor / pre-split proposal** helper invoked by the ingest rule (no new skill file if the logic lives in the rule; otherwise one minimal skill e.g. “split-proposal” that returns proposed split points). Prefer (a) to avoid new skill files per plan §5 “Where stabilizers live”.
- **Safety:** Never auto-apply split below 85%; always proposal + #review-needed when below threshold. Pairs with existing snapshot-before-split and confidence bands.
- **Tests:** Ingest fixture with multi-heading note; assert proposed split points follow H2/H3 → first occurrence → shorter heading; fixture with no headings asserts fallback word-boundary proposal.

**Rationale (for plan wording):** Lives in same ingest chain; bad split points → manual cleanup; proposal-only below high conf; better splits → cleaner content → more confident classify_para and stabler wrappers.

---

## 3. Plan file edits (summary)


| Location                                 | Change                                                                                                                                                                                                         |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontmatter `overview`**               | Extend to mention “name-enhance tie-breaker and split/atomicity proposal heuristic” as Phase 1 additions.                                                                                                      |
| **After §4 (Queue dispatch)**            | Insert two new sections: **§5. Name-enhance tie-breaker** and **§6. Split / atomicity proposal heuristic** (then renumber current §5 Rollout → §7, §6 Research-backed → §8, §7 Doc and sync → §9).             |
| **§5 → §7 Rollout and extensibility**    | In “Start small” or “Where stabilizers live”, add name-enhance and split-proposal to the list; in Extensibility, optionally shorten the “fork the same pattern for name-enhance” sentence and point to new §5. |
| **Where stabilizers live (bullet list)** | Add: **Name-enhance:** [name-enhance](.cursor/skills/name-enhance/SKILL.md). **Split proposal:** para-zettel-autopilot (or thin helper before obsidian_split_atomic).                                          |
| **§7 → §9 Doc and sync updates**         | Add Pipelines/Skills/Logs/Parameters updates for name-enhance (Organize-Log, Name-Review-Log, heuristic_adjusted/heuristic_reason) and split (config keys, #review-needed, proposal-only).                     |
| **Summary diagram**                      | Optionally add two nodes: name-enhance tie-breaker (after name-enhance / organize path), and split-proposal (before split_atomic in Ingest).                                                                   |


---

## 4. Config and doc touch points (for plan only — no edits in this phase)

- **Second-Brain-Config or Parameters:** Document optional keys for split fallback: `split_fallback_word_boundary_min`, `split_fallback_word_boundary_max` (e.g. 400, 600).
- **Naming-Conventions:** Already the source of truth for kebab-slug-YYYY-MM-DD-HHMM; plan will reference it for name-enhance tie-break order.
- **Logs:** Organize-Log and Name-Review-Log already exist; plan will state to log name-enhance heuristic there; no new log file.

---

## 5. Out of scope for this plan

- Implementation of the two heuristics (this plan only adds them to the existing targeted heuristics plan).
- Changes to MCP server or `obsidian_split_atomic` contract (split heuristic only proposes; MCP call unchanged when conf ≥ 85%).
- New skill files unless the implementer chooses a tiny “split-proposal” skill; plan prefers logic in ingest rule.

