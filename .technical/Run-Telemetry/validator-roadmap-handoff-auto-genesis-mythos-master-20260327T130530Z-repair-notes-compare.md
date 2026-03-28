---
actor: validator
project_id: genesis-mythos-master
queue_entry_id: repair-l1-postlv-notes-recal-d112-vs-d122-gmm-20260327T125200Z
parent_run_id: l1-eatq-20260327-gmm-repair-notes-d112-d122
timestamp: "2026-03-27T13:05:30Z"
validation_type: roadmap_handoff_auto
effective_track: conceptual
gate_catalog_id: conceptual_v1
report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260327T130530Z-post-l1-repair-notes-compare-124800Z.md
severity: high
recommended_action: block_destructive
primary_code: contradictions_detected
success: partial
error_category: validator_tier1_coherence
error_message: "Consistency reports skimmer stale vs workflow_state YAML and roadmap-state frontmatter; see report."
---

Validator subagent run: `roadmap_handoff_auto` with `compare_to_report_path` regression guard vs `roadmap-handoff-auto-genesis-mythos-master-20260327T124800Z-post-little-val-queue-layer1.md`. Single write: report at `report_path` above.
