---
created: 2026-03-24
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-empty-bootstrap-resume-gmm-20260324T085235Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 2
  high: 1
---

## Context

IRA invoked for RESUME_ROADMAP `action: recal` after nested validator first pass reported `severity: medium`, `recommended_action: needs_work`, primary code `safety_unknown_gap`, plus `missing_roll_up_gates`. The immediate objective is a minimal reconciliation pass that preserves current gate honesty while removing run-identity ambiguity across authoritative roadmap surfaces.

## Structural discrepancies

1. Run identity drift across authority surfaces: `workflow_state.md` frontmatter points to `last_auto_iteration: resume-deepen-post-recal-d060-021700z-gmm-20260324T021800Z`, while the active queue chain is `resume-recal-post-empty-bootstrap-resume-gmm-20260324T085235Z`.
2. `roadmap-state.md` contains a non-queue-style narrative timestamp marker (`last_deepen_narrative_utc: "2026-03-24-0852"`), which is not machine-chain equivalent to queue id fields.
3. `distilled-core.md` includes mixed historical/terminal cursor statements in dense bullets; no compact canonical reconciliation block tying all three files to one explicit chain marker.
4. Rollup gate semantics are still blocked (`HR 92 < min_handoff_conf 93` and `G-P*.*-REGISTRY-CI HOLD`), but evidence references are distributed and partly prose-dense, reducing fast verifiability for handoff checks.
5. `G-P4-1-*` is explicitly FAIL/stub until evidence, but acceptance evidence pointers are not normalized into one concise, machine-checkable checklist location.

## Proposed fixes

### Low risk

1. **Add canonical reconciliation frontmatter key in roadmap-state**
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`
   - **action_type:** `adjust_frontmatter`
   - **constraints:** only append keys; do not rewrite historical narrative blocks
   - **description:** Add `canonical_queue_chain_id: "resume-recal-post-empty-bootstrap-resume-gmm-20260324T085235Z"` and `canonical_queue_chain_timestamp_utc: "2026-03-24T08:52:35Z"` in frontmatter.
   - **rationale:** Establishes a machine-readable authority marker without disturbing narrative history.

2. **Mirror canonical reconciliation key in workflow_state**
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`
   - **action_type:** `adjust_frontmatter`
   - **constraints:** preserve existing `last_auto_iteration` and existing table rows verbatim
   - **description:** Add the same `canonical_queue_chain_id` and `canonical_queue_chain_timestamp_utc` keys used in `roadmap-state.md`.
   - **rationale:** Removes ambiguity between terminal deepen cursor and active recal queue chain by making both explicit and non-competing.

3. **Add compact "Canonical cursor parity" section in distilled-core**
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md`
   - **action_type:** `write_log_entry`
   - **constraints:** append a short section near Phase 0 anchors; avoid editing historical decision bullets
   - **description:** Add a 3-line parity block that cites `canonical_queue_chain_id`, `last_auto_iteration`, and `last_deepen_narrative_utc` with a one-sentence interpretation rule.
   - **rationale:** Gives validator and operator a single quick parity checkpoint instead of parsing long bullets.

### Medium risk

4. **Normalize rollup gate evidence pointers into one reconciliation block**
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`
   - **action_type:** `rewrite_log_entry`
   - **constraints:** do not change numeric gate values (`92`, `93`) or HOLD/FAIL statuses
   - **description:** Add/update a concise "Rollup gate reconciliation" block listing: (a) three Phase 3 rollup notes, (b) current HR vs threshold, (c) explicit HOLD reason and dependency (`2.2.3` / `D-020` execution evidence), (d) validator citation path.
   - **rationale:** Addresses `missing_roll_up_gates` by making evidence aggregation auditable without changing gate outcomes.

5. **Replace stub-only wording for G-P4-1-* with evidence checklist references**
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-and-Control-Systems/phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201.md`
   - **action_type:** `recompute_phase_metadata`
   - **constraints:** keep row status as FAIL/HOLD until evidence exists; only upgrade prose clarity
   - **description:** Convert any "FAIL (stub)" narrative-only phrasing into a checklist-style evidence contract (fixture path, CI artifact id, acceptance pointer) while retaining blocked status.
   - **rationale:** Prevents implied readiness and aligns gate language with verifiable evidence requirements.

### High risk

6. **One-pass log row annotation for queue-chain reconciliation**
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`
   - **action_type:** `rewrite_log_entry`
   - **constraints:** append annotation only to the latest relevant recal row; no historical row reordering
   - **description:** Add a single annotation column/value for the active recal entry tying it to `canonical_queue_chain_id` and validator report `.technical/Validator/validator-roadmap_handoff_auto-genesis-mythos-master-20260324T091955Z.md`.
   - **rationale:** High blast radius because table schema edits can impact parsers, but it provides hard traceability for future validator passes.

## Notes for future tuning

- Repeated drift pattern: deep historical cursor prose in `distilled-core.md` is informative but expensive for validators; consider a tiny machine-auth section as standard.
- Repeated gate pattern: blocked rollup is usually correct, but references are fragmented; a standardized reconciliation block template in `roadmap-state.md` would reduce false `missing_roll_up_gates`.
