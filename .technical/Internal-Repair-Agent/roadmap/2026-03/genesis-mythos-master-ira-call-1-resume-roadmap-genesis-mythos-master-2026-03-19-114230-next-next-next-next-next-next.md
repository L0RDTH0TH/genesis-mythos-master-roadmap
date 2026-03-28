---
created: 2026-03-19
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-19-114230-next-next-next-next-next-next
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 0
  high: 0
---

## Context

RESUME_ROADMAP `action=deepen` was flagged by validator report `genesis-mythos-master-20260319T122926Z.md` with `recommended_action: needs_work` and reason codes `missing_message_flow_example`, `missing_command_event_schemas`, and `safety_unknown_gap`. This IRA call proposes one-cycle, additive-only repairs against the phase `1.1.7` roadmap note and `decisions-log.md`.

## Structural discrepancies

1. The phase `1.1.7` note defines reason codes and a gate function but lacks branch-complete command-to-event flow examples.
2. The phase `1.1.7` note lacks strict command/event schema contracts (required/optional/nullability/bounds/versioning semantics).
3. `decisions-log.md` still contains template handoff placeholders and no explicit closure mapping for current validator gaps.

## Proposed fixes

### Fix 1 (maps to `missing_message_flow_example`)
- **action_type:** append_section
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230.md`
- **risk_level:** low
- **constraints:** append after existing "Deterministic recovery pseudocode"; do not alter existing state machine or reason-code enum.

```diff
*** Begin Patch
*** Update File: 1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230.md
@@
+## Deterministic command->event message flows (reason-code complete)
+
+```yaml
+flow_examples:
+  - name: quorum_lost_freeze
+    input_command:
+      name: EvaluateWriteGate
+      activation_epoch: 77
+      cluster_epoch: 77
+      quorum_proof_hash: null
+      state_hash: "abc123"
+    emitted_event:
+      name: WriteGateDenied
+      reason_code: QUORUM_PROOF_MISSING
+      allow_write: false
+      allow_read: true
+      terminal_state: DEGRADED_READ_ONLY
+```
*** End Patch
```

### Fix 2 (maps to `missing_command_event_schemas`)
- **action_type:** append_section
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230.md`
- **risk_level:** low
- **constraints:** append as a new contract section; keep field names aligned with existing `write_fence.policy`.

```diff
*** Begin Patch
*** Update File: 1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230.md
@@
+## Command and event schema contracts (v1)
+
+```yaml
+commands:
+  EvaluateWriteGate:
+    required:
+      command_id: {type: string, non_empty: true}
+      command_version: {type: integer, min: 1}
+      node_id: {type: string, non_empty: true}
+      activation_epoch: {type: integer, min: 0}
+      cluster_epoch: {type: integer, min: 0}
+      state_hash: {type: string, non_empty: true}
+    optional:
+      quorum_proof_hash: {type: string, nullable: true}
+
+events:
+  WriteGateDenied:
+    required:
+      event_id: {type: string, non_empty: true}
+      event_version: {type: integer, min: 1}
+      command_id: {type: string, non_empty: true}
+      reason_code:
+        type: enum
+        values: [QUORUM_LOST, EPOCH_MISMATCH, HASH_DIVERGENCE, QUORUM_PROOF_MISSING, WRITE_FENCE_ACTIVE, RECOVERY_NOT_PREPARED, REACTIVATION_BLOCKED]
+      allow_write: {type: boolean}
+      allow_read: {type: boolean}
+```
*** End Patch
```

### Fix 3 (maps to `safety_unknown_gap`)
- **action_type:** append_section
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md`
- **risk_level:** low
- **constraints:** append only under `## Handoff notes`; keep prior entries unchanged.

```diff
*** Begin Patch
*** Update File: 1-Projects/genesis-mythos-master/Roadmap/decisions-log.md
@@
 ## Handoff notes
 
 - Add `#handoff-review` and `#handoff-needed` bullets here when hand-off-audit flags issues.
 - Message-flow reference: [[command-event-schema-v0]].
 - Decomposition reference: [[phase-1-decomposition-sheet-v0]].
+- [H-2026-03-19-1.1.7] #handoff-review Closed validator gaps for phase 1.1.7:
+  - `missing_message_flow_example` -> add deterministic branch-complete command->event examples in phase 1.1.7 note.
+  - `missing_command_event_schemas` -> add explicit command/event schema contract section with required/optional/nullability/bounds/versioning.
+  - `safety_unknown_gap` -> replace placeholder-only handoff state with this closure mapping and artifact pointers.
*** End Patch
```

### Fix 4 (supporting closure traceability for the same reason-code set)
- **action_type:** append_checklist
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230.md`
- **risk_level:** low
- **constraints:** append under `## Verification and test matrix`; additive only.

```diff
*** Begin Patch
*** Update File: 1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230.md
@@
 - [ ] Validate write re-enable only after quorum proof and matching state hash.
+- [ ] Validate schema contract rejects unknown `reason_code` and missing `event_version`.
+- [ ] Validate each canonical denial branch emits exactly one deterministic `WriteGateDenied` event with stable `command_id` linkage.
*** End Patch
```

## Notes for future tuning

- Repeated validator hits indicate phase notes need a standard "message-flow + schema-contract" section template at tertiary depth.
- decisions-log handoff notes should not rely on placeholders once a validator report exists for the same timestamped cycle.
