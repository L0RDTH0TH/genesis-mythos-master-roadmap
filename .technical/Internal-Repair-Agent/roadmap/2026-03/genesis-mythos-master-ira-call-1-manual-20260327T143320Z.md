---
created: 2026-03-27
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: manual-ira-20260327T143320Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 0
---

## Context

IRA invoked for `RESUME_ROADMAP` with action `handoff-audit`, based on validator report `genesis-mythos-master-20260327T143320Z-post-handoff-audit-parity-repair.md` (`primary_code: state_hygiene_failure`, `reason_codes: state_hygiene_failure, contradictions_detected`). Scope constrained to state hygiene and contradiction removal only, while preserving conceptual advisory language and avoiding closure inflation.

## Structural discrepancies

1. `workflow_state.md` declares log authority semantics that require the first physical machine-advancing `deepen` row to agree with frontmatter, but the first physical row is a non-advancing `handoff-audit` row.
2. The same file contains frontmatter `last_auto_iteration: followup-deepen-post-recal-d104-continuation-gmm-20260327T181000Z` while top-row precedence currently points to a different non-advancing row, creating a skimmer-level authority contradiction.
3. Frontmatter `workflow_log_authority: last_table_row` is ambiguous with the callout’s stronger machine-cursor contract and can re-trigger interpretation drift even after row reorder.

## Proposed fixes

1. **[medium] Reorder top three rows in `workflow_state.md` log table to restore authority precedence**
   - **Target:** `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`
   - **Concrete edit instruction:** In the `## Log` table, move the row whose queue id is `followup-deepen-post-recal-d104-continuation-gmm-20260327T181000Z` to be the first data row directly under the separator row. Place non-advancing rows (`followup-recal-post-d104-continuation-gmm-20260327T181200Z` and `repair-l1-postlv-state-hygiene-post-d106-gmm-20260327T070425Z`) immediately below it.
   - **Constraint:** Keep every row body byte-identical (including advisory OPEN/HOLD language and "no machine cursor advance" clauses); change order only.

2. **[low] Normalize `workflow_log_authority` label to match actual contract semantics**
   - **Target:** `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` frontmatter
   - **Concrete edit instruction:** Replace `workflow_log_authority: last_table_row` with a semantics-aligned label such as `workflow_log_authority: frontmatter_cursor_plus_first_deepen_row`.
   - **Constraint:** Do not alter `current_subphase_index`, `last_auto_iteration`, or any confidence/advisory values.

3. **[low] Add one explicit anti-contradiction sentence to the existing log-authority callout**
   - **Target:** `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` (the `> [!important] Log authority (machine cursor)` block)
   - **Concrete edit instruction:** Append one sentence clarifying that non-advancing rows may appear above by timestamp but must not occupy first-row precedence over the latest machine-advancing `deepen` row.
   - **Constraint:** Keep wording conceptual/advisory and non-closure; do not edit rollup/REGISTRY-CI gate statuses.

## Notes for future tuning

- Repeated state-hygiene drift appears to come from prepend behavior mixing repair/audit and machine-advancing rows without a deterministic insertion rule.
- A stable insertion rule (`latest machine-advancing deepen row always top`) would likely reduce recurring `state_hygiene_failure` citations.
