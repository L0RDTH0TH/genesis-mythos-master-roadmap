---
created: 2026-03-19
pipeline: ingest
project_id: genesis-mythos-master
queue_entry_id: ingest-research-phase-1-1-20260319-1207
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 0
  high: 0
---

## Context

IRA invoked from an INGEST_MODE phase-1 propose run after validator reported `recommended_action: needs_work` with `reason_codes: [safety_unknown_gap]`. Current run already created a decision wrapper and did not move the note, so repair scope is structural quality of rationale/path evidence, not rollback.

## Structural discrepancies

1. Destination rationale exists only at generic para-type level and does not map to a concrete existing subtree with neighbor-fit evidence.
2. Path proposal evidence is under-specified: no explicit two-alternative comparison and no recorded tie-breaker.
3. Confidence gate behavior is implied but not fully documented in the run artifact bundle as an explicit "keep in Ingest unless >=85" decision record.

## Proposed fixes

1. **Add explicit destination rationale block** (low risk)
   - action_type: `write_log_entry`
   - target_path: `3-Resources/Ingest-Log.md` (or the active ingest run log note)
   - description: Add a short rationale mapping the source note to one existing subtree under `3-Resources/` and reference at least one neighbor note/folder pattern that justifies co-location.
   - constraints: Only append; do not edit existing historic lines.

2. **Record two path alternatives with a tie-breaker** (low risk)
   - action_type: `write_log_entry`
   - target_path: `3-Resources/Ingest-Log.md` (same run section)
   - description: Document at least two candidate paths under `3-Resources/`, then select one with a deterministic tie-breaker (e.g., strongest semantic neighbor overlap + shortest stable subtree depth).
   - constraints: Keep decision as propose-only metadata; do not move file.

3. **Write explicit confidence gate outcome for this run** (low risk)
   - action_type: `rewrite_log_entry`
   - target_path: `3-Resources/Ingest-Log.md` (same run section)
   - description: Add one line stating `ingest_conf=<value>; action=keep_in_ingest; move_blocked_below_85=true` so downstream validator/little-val can verify gate compliance directly.
   - constraints: If confidence later changes in a new run, create a new log line; do not overwrite prior run verdict.

## Notes for future tuning

- `safety_unknown_gap` appears when rationale and path-selection evidence are compressed into one sentence; a small structured "destination rationale + alternatives + gate" template in phase-1 propose logs would likely reduce repeat validator failures.
