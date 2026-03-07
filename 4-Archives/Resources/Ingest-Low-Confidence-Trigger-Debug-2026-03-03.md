---
title: Ingest Low-Confidence Guidance Trigger — Debug Analysis
created: 2026-03-03
tags: [second-brain, ingest, decision-candidate, debug]
para-type: Resource
status: active
---

# Ingest Low-Confidence Guidance Trigger — Debug Analysis (2026-03-03)

## Expected vs observed (summary)

**Expected:** When ingest runs on low/mid-confidence notes (post_loop_conf <85%), the pipeline sets `decision_candidate: true`, `guidance_conf_boost: 15`, `decision_priority: medium`, adds `#guidance-aware`, appends [!warning] and [!tip] callouts, **creates a decision wrapper note in Ingest/Decisions/** for every decision candidate, and logs `low_conf_trigger: mid-band-failure`. User requirement: **ALL** decision files must be added to Ingest/Decisions/.

**Observed (user report):** Log claims "Decision-candidate steps applied" but "ZERO visible changes" — no frontmatter, no tag, no callouts, no Ingest/Decisions/.

**Why Ingest/Decisions/ was ignored:** The rule and pipeline text **explicitly said "Optional"** for creating the decision wrapper note in Ingest/Decisions/. Agents treated that as skippable, so the step was never executed. User intent was always that **all** decision candidates get a file in Ingest/Decisions/; the wording contradicted that. **Fix (2026-03-03):** Rule and pipeline now state that creating the decision note in Ingest/Decisions/ is **required**; ensure folder via `obsidian_ensure_structure`; create a note per decision candidate. See para-zettel-autopilot.mdc and Templates.md.

**Vault audit result:** For **batch 4 and 5** notes that are **still in Ingest/**, the on-note changes **are present**:
- `Ingest/First-Person Player Experience.md`, `Ingest/DM Free Camera.md`, `Ingest/Dm.md`, etc. have `decision_candidate: true`, `guidance_conf_boost: 15` (or 2 of 3), `decision_priority: medium`, `tags: guidance-aware`, and the two callouts (Decision needed + Suggested user_guidance).
- **Batch 2/3** notes (e.g. `Ingest/Cascade Implementation.md`) do **not** have decision-candidate frontmatter or callouts; their log lines also do not mention `decision_candidate` or `low_conf_trigger`.
- **Ingest/Decisions/** folder and decision wrapper notes were missing because the rule had marked that step as **optional**; now **required**.

---

## 1. Which part of the pipeline should have written the frontmatter/tag/callout?

**Answer:** The **agent following the rule** [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc) — specifically the section **"When no move (manual review)"** and **"Low-confidence decision candidates"**. There is **no dedicated skill**; the rule instructs the agent to:
- Set frontmatter via MCP (`obsidian_manage_frontmatter` or equivalent).
- Add tag via MCP (`obsidian_manage_tags`).
- Insert callouts into the note body via `obsidian_update_note` or `obsidian_search_replace`.

The [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) describes this as "Decision candidates (low-confidence guidance trigger)" and points to the same rule. Pipeline order does not list a separate "decision-candidate" step; it is part of the "when we do not move" branch before `log_action`.

---

## 2. Did that rule/behavior actually run?

**Evidence:**

| Source | Batch 4/5 | Batch 2/3 |
|--------|-----------|-----------|
| **Ingest-Log.md** | Log lines mention "decision_candidate + #guidance-aware + callout; low_conf_trigger: mid-band-failure". | Log lines mention only "pre_loop_conf, post_loop_conf, loop_outcome"; no `decision_candidate` or `low_conf_trigger`. |
| **Vault (notes in Ingest/)** | Notes have frontmatter keys, `tags: guidance-aware`, and [!warning] / [!tip] callouts. | Notes (e.g. Cascade Implementation) have only basic frontmatter; no decision callouts. |

**Conclusion:** For **batch 4 and 5**, the decision-candidate steps **did run** and **did write** to the notes still in Ingest/. For **batch 2 and 3**, those steps **did not run** (or the rule was not yet in place / not followed in that run).

---

## 3. If it ran but didn't write, why?

For batch 4/5 it **did** write, so this applies only to batch 2/3 or to the user's perception:

- **Batch 2/3:** The decision-candidate block may have been added to the rule **after** those runs, or the agent in those runs did not execute the "when no move" branch (e.g. different code path, or run before the rule was synced). No evidence of MCP write failure for those runs; the steps were simply not executed.
- **User saw "ZERO visible changes":** Possible causes:
  1. **Wrong location:** Log lines show the **proposed path** (e.g. `2-Areas/First-Person Player Experience.md`) as the last column. The note remains in **Ingest/** when no move is performed. If the user opened notes under 2-Areas/ or 4-Archives/, they might see no such file or a different file without the callouts.
  2. **Wrong batch:** If the user checked batch 2/3 notes (e.g. Cascade Implementation, Character Customization), those were never given the decision-candidate treatment.
  3. **Minor inconsistency:** At least one note (e.g. Dm) is missing `guidance_conf_boost: 15` in frontmatter; others have all three keys. So small gaps exist but are not "ZERO" for batch 4/5.

---

## 4. Is the trigger logic present in live rules/skills or only in the plan?

**Answer:** The trigger logic **is present in live rules**:
- [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc): "When no move (manual review)" and "Low-confidence decision candidates" with trigger (post_loop_conf < 85 or post_loop_conf ≤ pre_loop_conf), frontmatter, tag, callouts, logging.
- [Cursor-Skill-Pipelines-Reference.md](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md): Decision candidates paragraph with same behavior.
- [.cursor/sync/rules/context/para-zettel-autopilot.md](.cursor/sync/rules/context/para-zettel-autopilot.md): Synced copy with the same steps.

The [plan](.cursor/plans/ingest_low-confidence_guidance_trigger_a23c525f.plan.md) describes the design; the rule and pipeline reference contain the executable behavior.

---

## 5. Most likely root causes (ranked)

1. **User looked at the wrong notes or wrong location**  
   Batch 4/5 notes that stayed in Ingest/ have the changes. If the user inspected (a) notes under **proposed** paths (2-Areas/, 4-Archives/) instead of Ingest/, or (b) **batch 2/3** notes that never had the decision-candidate steps applied, they would see no or fewer changes.

2. **Decision-candidate steps were not applied in earlier runs (batch 2/3)**  
   The rule was either added or consistently followed only from batch 4 onward. Batch 2/3 log lines do not mention `decision_candidate` or `low_conf_trigger`, and notes like Cascade Implementation have no decision callouts. So "no visible changes" is accurate for that subset.

3. **Decision folder was marked optional (fixed)**  
   The rule and pipeline said "Optional" for creating the decision wrapper in Ingest/Decisions/, so agents skipped it. User requirement is that **all** decision files go into Ingest/Decisions/. Rule and pipeline have been updated to **required**; see para-zettel-autopilot.mdc and Cursor-Skill-Pipelines-Reference.

**Less likely:** Plan-mode simulation (batch 4/5 vault state shows real writes). MCP write failures (no Errors.md or trace for batch 4/5). Confidence gate blocking (75% is mid-band; decision steps are explicitly for "no move" branch).

---

## 6. Exact next diagnostic step

**Recommended queue prompt** (to force a real test and backfill):

1. **Add one line to** `.technical/prompt-queue.jsonl`:

```json
{"mode":"INGEST MODE","prompt":"Apply the Ingest Low-Confidence Guidance Trigger to the single note Ingest/Cascade Implementation.md only. Do not move or split. Steps: 1) Set frontmatter decision_candidate: true, guidance_conf_boost: 15, decision_priority: medium. 2) Add tag #guidance-aware. 3) Append after frontmatter the two callouts: [!warning] Decision needed (confidence 70%) with proposed path, and [!tip] Suggested user_guidance with a path-specific user_guidance YAML block. 4) Log to Ingest-Log with low_conf_trigger: mid-band-failure. Use real MCP calls (obsidian_manage_frontmatter, obsidian_manage_tags, obsidian_update_note or obsidian_search_replace). Verify by reading the note back.","source_file":"Ingest/Cascade Implementation.md","id":"debug-decision-candidate-single-20260303"}
```

2. **Run EAT-QUEUE** (or process the queue once).

3. **Verify in vault:** Open `Ingest/Cascade Implementation.md` and confirm:
   - Frontmatter contains `decision_candidate: true`, `guidance_conf_boost: 15`, `decision_priority: medium`, and `tags: guidance-aware`.
   - Body contains the [!warning] and [!tip] callouts after the frontmatter.

If this succeeds, the agent/MCP path works and the issue is limited to (a) which notes were processed in which run and (b) where the user looked. If it fails, inspect the run for MCP errors, permission, or dry_run/plan-mode behavior.

---

## References

- Rule: [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc) (§ When no move, § Low-confidence decision candidates).
- Pipeline: [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) (ingest section, Decision candidates).
- Plan: [ingest_low-confidence_guidance_trigger_a23c525f.plan.md](.cursor/plans/ingest_low-confidence_guidance_trigger_a23c525f.plan.md).
- Ingest-Run-Trace (batch 4): [Ingest-Run-Trace-2026-03-03-batch4.md](3-Resources/Ingest-Run-Trace-2026-03-03-batch4.md).
