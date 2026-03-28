---
actor: validator
project_id: genesis-mythos-master
queue_entry_id: resume-recal-gmm-20260326T193000Z
parent_run_id: null
timestamp: 2026-03-26T19:30:00Z
mode: RESUME_ROADMAP
pipeline: roadmap
validation_type: roadmap_handoff_auto
report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260326T193000Z-roadmap-handoff-auto-recal-conceptual.md
severity: high
recommended_action: block_destructive
primary_code: state_hygiene_failure
reason_codes:
  - state_hygiene_failure
  - missing_roll_up_gates
  - safety_unknown_gap
  - missing_acceptance_criteria
  - missing_task_decomposition
success: partial
error_category: state-inconsistent
error_message: Hand-off queue_entry_id not anchored to authoritative workflow_state cursor structures; little_val_ok=false.
status: completed
---

# Run-Telemetry — validator (roadmap / handoff-auto)

Hostile `roadmap_handoff_auto` on `effective_track: conceptual` for `resume-recal-gmm-20260326T193000Z`. Report written to `report_path`.

Cross-ref: [[3-Resources/Telemetry-Dashboard|Telemetry-Dashboard]], [[3-Resources/Second-Brain/Parameters#Run-Telemetry|Parameters § Run-Telemetry]], [[3-Resources/Second-Brain/Vault-Layout#.technical|Vault-Layout § .technical]].
