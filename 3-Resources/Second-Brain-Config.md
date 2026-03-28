---
title: Second Brain Config
created: 2026-03-02
tags: [pkm, second-brain, config]
para-type: Resource
status: active
---

hub_names:
  projects: "Genesis Mythos Hub"
  resources: "Genesis Resources Hub"
  areas: "Genesis Areas Hub"

highlight:
  default_key: "3-Resources/Highlightr-Color-Key.md"  # create this stub next if missing
  # Post-process stabilizer (distill): short-note core bias and emoji fallback
  short_note_word_threshold: 300
  default_core_bias: true       # whether short notes bias toward core (drift 0)
  mobile_emoji_fallback: true   # force emojis when mobile context detected; else CSS gradients

archive:
  age_days: 180
  no_activity_days: 60          # used with #stale/#review-later for confidence-floor boost (post-process stabilizer)

depths:
  async_preview_threshold: 75
  batch_size_for_snapshot: 8

# Nested Validator → IRA (Layer-2 pipelines). When true (default), every first nested ValidatorSubagent pass is followed by exactly one IRA call, apply suggested_fixes (may be empty), then (for pipelines that use little val) little val once, then a second Validator pass with compare_to_report_path. Set false for legacy: skip IRA and second validator when the first pass is clean log_only with no actionable gaps.
nested_validator:
  ira_after_first_pass: true

# Validator tiered blocks (roadmap_handoff_auto / aligned). When true (default), final nested pass may return Success if verdict is needs_work (medium) without high/block_destructive; pipelines still block on high or block_destructive. When false, treat any historical strict behavior per Subagent-Safety-Contract only.
validator:
  tiered_blocks_enabled: true
  max_incoherence_retries: 1
  # ROADMAP_HANDOFF_VALIDATE — fixed model for high-stakes pass (queue passes Task model from here)
  roadmap_handoff:
    model: inherit
  # VALIDATE recovery_outcome — did PromptCraft + follow-up runs clear the original failure?
  recovery_outcome:
    model: auto

# PromptCraft recovery (Layer 1 optional hook). Defaults off — no silent craft→append loops.
recovery_auto_craft_enabled: false
recovery_auto_append: false
max_prompt_craft_per_correlation_per_run: 1
recovery_pre_append_lint_enabled: true
# When true, A.5b post–little-val hard-block repair JSONL is produced by Task(prompt_craft) first (merge-aware craft). When false or on PromptCraft failure / empty lines / lint_blockers / Task error, Layer 1 appends the minimal deterministic repair line (legacy A.5b template). Repair is still appended when tiering applies unless incoherence budget is exhausted — fallback guarantees a line.
post_little_val_repair_use_prompt_craft: false

# Queue continuation: structured follow-up metadata + optional durable log + empty-queue bootstrap (see Docs/Queue-Continuation-Spec).
queue_continuation:
  continuation_log_enabled: true
  empty_queue_bootstrap_enabled: true
  empty_queue_bootstrap_max_age_minutes: 1440
  # If strict continuation_eligible filters yield no candidate, allow one forced bootstrap when roadmap-state is unfinished.
  empty_queue_bootstrap_force_when_unfinished: true
  # Optional wider lookback for forced fallback branch (falls back to empty_queue_bootstrap_max_age_minutes when omitted).
  empty_queue_bootstrap_force_max_age_minutes: 10080
  # If no continuation record is eligible after fallback, call PromptCraft anyway with unresolved roadmap hints.
  empty_queue_bootstrap_prompt_craft_on_no_record: true
  # If PromptCraft cannot return a line in no-record path, synthesize one deterministic RESUME_ROADMAP deepen line.
  empty_queue_bootstrap_deterministic_when_no_record: true
  empty_queue_bootstrap_tail_lines: 50
  empty_queue_bootstrap_prompt_craft: true
  empty_queue_bootstrap_auto_append: true

# Task hand-off comms: verbatim Cursor Task prompt/return pairs in .technical/task-handoff-comms.jsonl (Layer 0, Layer 1, Layer 2 nested helpers). See Docs/Task-Handoff-Comms-Spec.
task_handoff_comms:
  enabled: true
  max_body_bytes: 524288

# Layer 1 nested attestation (validator_context + nested_subagent_ledger + ledger semantic check). When strict flags are false, queue.mdc keeps legacy skip-post-LV-and-consume if validator_context is missing; enable strict gates to refuse consumption and log continuation rows (nested_attestation_failure). When strict_nested_return_gates is true, queue.mdc A.5 (b0)(iii) also refuses consumption if nested_subagent_ledger shows hollow attestation (invoked_ok / invoked_empty_ok with task_tool_invoked false on mandated helper steps). See Parameters.md § Queue nested attestation, Queue-Sources § Nested attestation, queue.mdc A.5 / A.5e.
queue:
  # Append-only movement trace for prompt-queue (consumed lines + appends). See Docs/Queue-Audit-Log-Spec.md.
  audit_log_enabled: true
  audit_log_path: .technical/prompt-queue-audit.jsonl
  # full = store entire queue entry object on audit rows; metadata_only = mode/id/project_id/source_file/params keys only.
  audit_log_payload_mode: full
  # Roadmap pass order: repair_first = legacy one roadmap dispatch per project per EAT-QUEUE (after repair-first sub-sort). forward_first = initial pass: up to max_blocking_repair_preflight blocking repairs + max_forward forward-class; cleanup pass: up to max_repair repair-class lines. See queue.mdc A.4c.
  roadmap_pass_order: forward_first # repair_first | forward_first
  max_forward_roadmap_dispatches_per_project_per_run: 1
  max_repair_roadmap_dispatches_per_project_per_run: 3
  max_blocking_repair_preflight_per_project_per_run: 1
  # Re-read roadmap-state / workflow_state between roadmap Task dispatches when true.
  roadmap_refresh_between_roadmap_dispatches: true
  # Stall skip: when queue_agent_may_skip_if_stall on a line and (stall_skip_confirmed OR hard_block_return_count >= threshold in-run), skip Task. See queue.mdc A.5.0.
  stall_skip_enabled: true
  stall_skip_min_hard_block_returns_per_run: 2
  strict_nested_return_gates: false
  strict_nested_ledger_all_pipelines: false
  # State-driven anti-spin resolver for RESUME_ROADMAP dispatch.
  # Conceptual-first tuning (optional): set `roadmap_next_need_enabled: false` to disable automatic resolver `effective_target` hints (manual queue targets only). See Docs/Dual-Roadmap-Track, queue.mdc § Conceptual effective_target guard.
  roadmap_next_need_enabled: true
  # Prefer conceptual track when decomposition is sparse and no explicit track lock exists.
  roadmap_next_need_prefer_track_when_sparse: true
  # Minimum structural delta (0-100) to keep repeating same action class; below this, pivot class.
  roadmap_next_need_min_structural_delta: 8
  # Spin detection from structural delta/action repetition.
  spin_detection_enabled: true
  spin_detection_streak_threshold: 2
  spin_detection_require_same_need_class: true
  # Gate-block detection: repeated contract gate failures should pivot track, not loop same-track action class.
  gate_block_detection_enabled: true
  gate_block_streak_threshold: 2
  prefer_track_shift_on_gate_block: true
  gate_block_same_track_cooldown_runs: 1
  # Durable gate streak file (see Docs/Queue-Gate-State-Spec.md). Layer 1 / queue-gate-compute.py read this before resolver + A.5c.
  gate_state_path: .technical/queue-gate-state.json
  # When true, Layer 1 must run scripts/queue-gate-compute.py for report (pre-hand-off), validate-line (before A.5c append), record-outcome (after A.5e).
  deterministic_gate_script_enabled: false
  deterministic_gate_script_path: scripts/queue-gate-compute.py
  # gate_key = project_id|effective_track|gate_signature when true (see Docs/Queue-Gate-State-Spec.md)
  gate_key_includes_track: true
  # When gate_block + explicit track lock, skip automatic A.5b repair append (operator / wrapper path)
  gate_block_skip_repair_when_track_locked: true
  # On conceptual track, these primary_codes alone do not trigger Layer 1 post–little-val repair append (see Docs/Roadmap-Gate-Catalog-By-Track.md)
  conceptual_skip_auto_repair_primary_codes:
    - missing_roll_up_gates
    - safety_unknown_gap
  # When true, Layer 1 preserves subphase-exit params on append (see queue.mdc A.5c.0); primary rewrite policy is Layer 2
  conceptual_subphase_exit_l1_guard_enabled: true
  # Same-subphase anti-churn: when Layer 1 detects repeated follow-ups targeting the same conceptual subphase at/above this streak, it must pivot to next-node continuation unless a hard blocker is active.
  conceptual_same_subphase_streak_threshold: 2
  # Conceptual forward-lube: bias resolver/synth follow-ups to structural deepen unless hard conceptual blockers exist.
  conceptual_forward_prefer_deepen: true
  # Repeated conceptual medium-gap escalation (structural only when true — see queue.mdc A.5b.5; never rollup/CI on conceptual).
  conceptual_force_build_on_repeated_gap: false
  # Consecutive same-spine medium-gap hits before A.5b.5 escalation activates (default 4 when re-enabled).
  medium_gap_escalation_threshold: 4
  # Require scaffold evidence when conceptual run reports structural block/no-advance (queue strict path).
  require_conceptual_scaffold_on_block: true
  # Resolver alignment policy from task-handoff-comms and pipeline return (warn-only in v1).
  resolver_alignment_warn_only: true
  # When true (default), after RESUME_ROADMAP Success with queue_next !== false, if Layer 2 omits a valid queue_followups.next_entry, Layer 1 A.5c.1 appends one synthesized RESUME_ROADMAP line and logs queue_next_contract_violation_recovered. Set false to refuse silent recovery (operator must fix Layer 2 return). Conceptual-heavy runs may set false to reduce queue self-churn; pair with explicit `queue_next: false` on terminal entries.
  synthesize_followup_when_queue_next_true: true
  # Hard guard: after RESUME_ROADMAP success + queue_next !== false, re-check queue and append one synthesized follow-up if none remains for the same project.
  assert_followup_presence_after_resume_success: true
  # EAT-QUEUE BREAK-SPIN: Layer 0 passes ## operator_break_spin YAML; Layer 1 merges into layer1_resolver_hints (see queue.mdc). Alternate deepen first; recal fallback when no alternates if enabled.
  break_spin_prefer_alternate_deepen: true
  break_spin_recal_fallback_when_no_alternate: true
  # Layer 0 only — after Task(queue) returns; parse ## layer0_queue_signals in Queue return. Never put loud copy in Watcher-Result.
  layer0_escalation_enabled: false
  layer0_no_gain_voice_lines:
    - "Autonomous roadmap iteration stops here until you set explicit gates. No further queue churn until you own the next move."
  layer0_no_gain_voice_vault_path: null  # optional vault note path; when set, prepend lines from that note instead of or in addition to layer0_no_gain_voice_lines (dispatcher policy)
  # Decisions preflight (read-only): compare decisions-log operator picks vs rollup surfaces; inject YAML into roadmap Task hand-off. See Docs/Decisions-Log-Operator-Pick-Convention.md and .cursor/skills/decisions-preflight/SKILL.md.
  decisions_preflight:
    enabled: false
    on_drift: inject_handoff # inject_handoff | inject_only | off — inject_only treated same as inject_handoff in v1; off skips skill and merge
    apply_to_modes:
      - ROADMAP_MODE
      - RESUME_ROADMAP
    tracked_decision_ids:
      - D-044
      - D-032
      - D-037
      - D-059
    stale_scan_paths:
      - roadmap-state.md
      - distilled-core.md
    watcher_result_on_stale: true

# Prompt-crafter defaults (laptop-only). Consumed by prompt-crafter and rules (e.g. para-zettel-autopilot) for MCP pass-through; queue payload overrides take precedence. Non-destructive defaults only—params influence proposals but require approved: true for any move/rename per Pipelines § Phase 2. No auto-approval injection.
prompt_defaults:
  ingest:
    context_mode: strict-para  # For ingest/wrapper; fallback to organize for re-org
    max_candidates: 7          # Wrapper must pad to exactly 7 per Pipelines.md
    rationale_style: concise   # Per MCP-Tools.md optional
    auto_apply_agent_generated_without_wrapper: true  # Keep wrapper approval semantics unchanged; this toggles only the Phase 1 direct-move policy branch for eligible agent-generated notes (including Ingest/Agent-Research)
    validator_block_agent_generated_without_wrapper: false  # When false, ingest validator is advisory-only for the auto-apply agent-generated direct-move branch; normal/wrapper paths still block on high-severity validator verdicts
  organize:
    context_mode: organize
    max_candidates: 5
  roadmap:   # RESUME-ROADMAP; merged with queue params when mode is RESUME-ROADMAP
    action: deepen             # default; deepen | recal | revert-phase | sync-outputs | handoff-audit | resume-from-last-safe | expand
    max_iterations_per_phase: 80   # optional hard ceiling when set; deprecated as sole blocker — use iteration_guidance_ranges for guidance
    max_iterations_total: null # optional cap across all phases
    iteration_guidance_ranges:     # per-depth expected iteration ranges (guidance only; no automatic block)
      depth_1: [10, 15]       # high-level phase container
      depth_2: [8, 12]        # secondary
      depth_3: [5, 10]        # tertiary
      depth_4_plus: [3, 6]    # quaternary and deeper (pseudo-code territory)
    context_util_threshold: 80     # % of context window above which to trigger RECAL-ROAD instead of another deepen when tracking is enabled
    context_token_per_char: 0.25  # chars → tokens heuristic for context estimates (approx. 4 chars per token; configurable)
    context_window_tokens: 128000 # assumed model context window size used for utilization estimates
    enable_context_tracking: false # when true, compute/log context utilization for deepen runs and apply the RECAL-ROAD gate
    granularity: null           # optional: secondary-tertiary | tertiary-mid-technical | full-pseudo-code; overridden per-phase in deepen
    focus: null                 # optional, e.g. handoff-readiness
    handoff_gate: false
    min_handoff_conf: 85
    # Advisory only — roadmap-deepen may append to workflow_state Status / Next; no auto-freeze or phase advance
    diminishing_returns_advisory_enabled: true
    diminishing_returns_window_runs: 5
    diminishing_returns_confidence_epsilon: 3
    diminishing_returns_same_target_streak: 3
    # Execution subtree folder name under Roadmap/ (mirrors Roadmap Structure)
    execution_subfolder: Execution
  profiles:  # Named overrides; selectable via Commander macro; fallback to pipeline default
    project-priority:
      context_mode: project-strict
      max_candidates: 5

# Roadmap (multi-run default; one-shot deprecated). Read by auto-roadmap, roadmap-generate-from-outline, roadmap-audit, RECAL-ROAD handler.
roadmap:
  default_mode: multi-run
  one_shot_deprecated: true
  conf_phase_complete_threshold: 85
  drift_score_threshold: 0.08    # drift above this forces wrapper; log exact score in recal report
  auto_apply_safe_threshold: 82  # single-option wrappers ≥82% may auto-apply with snapshot + log
  ignored_wrappers_auto_revert: 3  # after this many ignored recal wrappers, auto-revert to last safe phase
  # Hand-off readiness (parallel gate): junior-dev delegatability before phase completion
  handoff_gate_enabled: false           # set true to enforce junior-dev readiness before phase completion
  handoff_readiness_high_threshold: 85
  handoff_readiness_mid_min: 70
  handoff_readiness_mid_max: 84
  min_handoff_conf: 85
  # Conceptual track: minimum phase handoff_readiness for "design team ready" terminal stop (execution-only gaps advisory)
  conceptual_design_handoff_min_readiness: 75
  # Slice-level exit (distinct from conceptual_target_reached): when true, RoadmapSubagent may rewrite deepen follow-ups to advance to the next structural node — see Parameters § Conceptual subphase exit (default on for conceptual forward motion; set false to allow polish-only churn on the same subphase)
  conceptual_subphase_exit_enabled: true
  # When true, conceptual subphase exit may override high-util recal tails and force next-node deepen when no hard conceptual blocker is active.
  conceptual_subphase_exit_override_high_util_recal: true
  # Minimum handoff_readiness on the current slice note to treat subphase slice as complete (slice-level; not whole-project)
  conceptual_subphase_min_readiness: 75
  # Optional: max deepen log rows targeting the same subphase before forcing slice-exit rewrite when enabled (omit or 0 = do not use this cap)
  conceptual_max_deepen_per_subphase: 0
  # Optional: handoff_gaps entries whose text starts with one of these prefixes do not block slice exit
  conceptual_nonblocking_gap_prefixes: []
  # Conceptual forward-lube: max consecutive conceptual non-advance runs before forcing deepen + scaffold fallback mode.
  conceptual_non_advance_force_threshold: 2
  # When true, conceptual blocked-write runs must emit conversion-ready scaffold artifact (in-note or Conceptual-Amendments note).
  conceptual_force_scaffold_on_block: true
  handoff_thresholds_by_tech:           # optional; falls back to default if no tech-specific match
    default: { high: 85, mid_min: 70 }  # used when no tech-specific match
    1-2:    { high: 80, mid_min: 60 }  # early conceptual → lower bar
    3-4:    { high: 85, mid_min: 68 }  # mid → standard rigor
    5+:     { high: 88, mid_min: 72 }   # late phases demand more executability
  handoff_gaps_drift_penalty: 0.3      # optional; add to drift_score when handoff_gaps.length > 2 (capped 0.0–1.0)
  # Optional: handoff_bonus_heuristics (e.g. mermaid_flow: 12, criteria_per_task: 10, swap_example: 8)
  # Optional: handoff_heuristics_weights (e.g. missing_pseudo_code: -20, unresolved_fork: -15, no_criteria: -10, trace_gap: -25)
  # Optional: tech_level_reqs (e.g. 1: 'trace only', 4: 'pseudo-code', 5: 'stubs + tests') — progressive rigor by phase tech_level
  # Optional VALIDATE type roadmap_mirror_integrity: advisory check execution↔conceptual links (Validator-Reference)
  # Conceptual-Decision-Records: off = skip; best_effort = create note, log Errors on failure, do not fail deepen; required = fail deepen if record not created
  conceptual_decision_record_mode: required

# Technical progression (roadmap / Cursor agent). When true, queue payloads can carry tech_level (from phase number); late phases get pseudo-code depth. See Cursor-Agent-Ingest-Workflow and Parameters § Confidence bands.
roadmap_tech_progression: true   # Core philosophy: late phases must reach pseudo-code hand-off granularity
tech_levels:
  level_1: high-concept   # Phases 1–2: user impacts only, no jargon
  level_2: mid-tech       # Phases 3–4: architecture patterns, tradeoffs
  level_3: pseudo-code    # Phases 5+: pseudo-code, edges, data shapes
