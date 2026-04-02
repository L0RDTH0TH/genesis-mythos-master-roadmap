---
title: Second Brain Config
created: 2026-02-25
tags: [pkm, second-brain, config]
para-type: Resource
status: active
links: [[Resources Hub]]
---

# Second Brain Config

Single source of truth for pipeline and skill configuration. Skills and rules that need hub names or thresholds should read this note (e.g. via context or Templater/Dataview).

## hub_names

- projects: "Projects Hub"
- areas: "Areas Hub"
- resources: "Resources Hub"
- resurface: "Resurface"

## archive

- age_days: 90
- no_activity_days: 60

## highlight

- default_key: "3-Resources/Highlightr-Color-Key.md"
- **short_note_word_threshold**: 300 — post-process stabilizer: notes below this word count bias toward core (drift 0).
- **default_core_bias**: true — whether short notes get core bias.
- **mobile_emoji_fallback**: true — when mobile context detected, use emoji indicators instead of/in addition to CSS gradients.

## graph

- moc_strength: 3

## queue

- **queue_nudge_after_seconds** (optional): e.g. 30 — after this inactivity, Watcher or cron can append a reminder to Watcher-Signal.md to run Process Queue. Omit or 0 to disable.
- **queue_nudge_enabled**: true | false — when true, nudge is allowed when queue has pending entries.
- **auto_cleanup_after_process**: true | false — when true, run queue-cleanup skill after each EAT-QUEUE run (auto-mark failed entries, append to Errors.md). When false, cleanup only when user runs "Clear queue" or "Queue cleanup".
- **re_try_max_loops**: 3 — cap on re-try spins per thread (e.g. same section/phase_path). When exceeded, abort re-try and create cap-hit wrapper (A: Force approve, B: Prune branch, 0: Re-wrap full phase). Document in Parameters.md.

## task_harden (capability probing)

- **mcp_probe_mode**: "assume_unavailable" — controls whether the roadmap subagent runs the lightweight Obsidian MCP availability capability probe at the start of each `Task(subagent_type: "roadmap")` invocation.
  - **auto**: perform the probe and set `mcp_available` from the probe outcome.
  - **assume_available**: skip the probe and set `mcp_available: true`.
  - **assume_unavailable**: skip the probe and set `mcp_available: false` (force inline-edit backend).

## pipeline_mode and validator_profiles

- **pipeline_mode**: balance  # fast | balance | extreme — default validator/safety profile for roadmap/research
- **validator_profiles**:
  - extreme:
    - l1_post_lv_policy: always
    - nested_ira_policy: always
    - research_synthesis_depth: full
    - target_nested_validator_passes: 4
  - balance:
    - l1_post_lv_policy: conditional_nonhard_skip
    - nested_ira_policy: clean_skip
    - research_synthesis_depth: light
    - target_nested_validator_passes: 2
  - fast:
    - l1_post_lv_policy: minimal
    - nested_ira_policy: medium_or_higher
    - research_synthesis_depth: fast
    - target_nested_validator_passes: 2

## crafting (prompt-crafter)

- **tmp_prompt_path**: ".technical/tmp-prompt.json" — machine-only scratchpad for the question-led Prompt-Crafter. Used to track which params have been asked, which values were chosen explicitly (A-path/manual), and C-choice reasoning across a crafting session. Treated as implementation detail; excluded from Obsidian and not surfaced in PARA notes.
- **max_reasoning_sentences**: 3 — hard cap on sentences per C-choice reasoning snippet when writing to the scratchpad and to queue `agent_reasoning`. Keeps payloads short and machine-readable.

## snapshot

- **batch_size_for_snapshot**: 5 — when queue length (or batch size) > this value, use BATCH_SNAPSHOT_DIR for the run; when ≤ this value, use per-change snapshots per note. Fine-tunes overhead for mobile single-item vs batch.

## roadmap (optional)

> Mirror of `prompt_defaults.roadmap` for human-readable reference. Edit values in `## prompt_defaults (Config)` / `prompt_defaults.roadmap` to change behavior; keep this section in sync. For **context utilization tracking**, this block is descriptive: the **effective** on/off flag is computed per run by auto-roadmap (default-on) and can only be turned off via an explicit RESUME-ROADMAP queue param `enable_context_tracking: false`; setting `enable_context_tracking: false` here is treated as misconfiguration and ignored by the dispatcher.

- **phase_fork_heuristic**: "strict" | "off" — when "strict", expand-road-assist post-step scans expanded output for choice indicators ("or", "vs", "options:") and, if found, sets phase_forks frontmatter and auto-queues Phase Direction Wrapper creation. When "off", only explicit phase_forks frontmatter triggers wrapper creation. Document in Skills.md and expand-road-assist SKILL.
- **custom_hand_off** (optional): Path to hand-off template; roadmap-resume reads it when building the resumption prompt (default: Templates/Hand-Off-Roadmap.md).
- **distill_roadmap_lens** (optional): e.g. "accuracy-focus" — bias distill toward factual anchors over creative fluff when updating decisions-log and distilled-core in the roadmap chain.
- **phase_output_sync**: "report_only" | "auto_refresh" — when phase-X-output.md is out of sync with canonical phase roadmap, report only (#review-needed) or auto-refresh (snapshot + backup before overwrite). Used by roadmap-phase-output-sync.
- **multi_run_mobile_bias** (optional): true | false — when true, shorten hand-off prompts for phone screens (e.g. cap directive length, denser summaries).
- **aggressive_auto_apply_threshold** (optional): e.g. 82 — when a wrapper has only one high-confidence option and confidence ≥ this value, auto-apply with per-change snapshot and log "auto-approved safe fix". Default off or 85 to stay conservative.
- **max_iterations_per_phase**: 80 — default per-phase iteration cap for multi-run roadmap; `workflow_state.md` frontmatter mirrors this value and `roadmap-deepen` enforces it as a hard ceiling when set.
- **enable_context_tracking**: true — documents the intended **default-on** behavior for context utilization tracking. Auto-roadmap always treats tracking as enabled when this key is omitted or true; it can only be disabled for a specific RESUME-ROADMAP run via an explicit queue param `enable_context_tracking: false`. A value of `false` here **must not** globally disable tracking and is treated as a configuration error by validation.
- **context_util_threshold**: 80 — utilization % above which deepen is paused and **RECAL-ROAD** is queued instead of another deepen.
- **context_token_per_char**: 0.25 — chars → tokens heuristic (approx. 4 characters per token) used to estimate context usage without a tokenizer.
- **context_window_tokens**: 128000 — assumed model context window size used as the denominator when computing utilization.
- **display_timezone** (optional): IANA timezone name (e.g. `America/New_York`) used to convert queue entry `timestamp` (UTC) to local time when writing workflow_state ## Log. When invalid or missing, pipelines fall back to server time and log to Errors.md; see Parameters § Timestamp resolution.

## code_comments (optional)

- **density**: medium — high | medium | minimal (default medium to avoid over-commenting).
- **required_sections**: ["why", "provenance_link"] — mandatory in plan output; optional_sections: ["assumptions", "limitations"].
- **provenance_format**: "> See [[{wrapper_link}]] for decision context" — merged into TASK-TO-PLAN-PROMPT template by prompt-crafter/task-to-prompt handler. Document in Parameters.md.

## depths (optional)

User-tunable depth-enhancement parameters. Read by depth skills and pipeline rules; enables personalization post-rollout.

- **highlight_coverage_min**: 50 — minimum % of meaningful spans to target for highlighting (distill-highlight-color). Range typically 50–70%; skill may adapt within range from content length/complexity.
- **async_loop_max_hours**: 24 — max age (hours) for async preview/refinement context when considering loop outcomes.
- **commander_macro_limits**: 5 — cap on chained commands in a single Commander macro to avoid runaway chains.
- **async_preview_threshold** (optional, in depths or top-level): e.g. 68 or 85 — below this confidence, always emit async preview and do not commit; document in Configs.md and Parameters.md.

## confidence_bands (optional)

Override default bands when present. Pipelines and skills read these; fallback to 68–84% mid, 85% high if omitted.

- **mid**: [80, 90] — mid-band range (min, max %).
- **high_threshold**: 90 — minimum % to proceed with destructive actions after snapshot.
- **non_destructive_lower** (optional): e.g. 75 — minimum % for metadata-only or preview-only steps (no destructive write). Safety unchanged for destructive (still ≥85% + snapshot). Document pros/cons in Parameters.md.

## validator (optional)

Validation-type → model (Cursor model id) or `"auto"`. Fixed model = stable hostile pass; no Auto discount for that call. High-stakes types (e.g. roadmap handoff) use fixed model; **liberal types** may use `"auto"` so Validator can run often and cheaply.

- **roadmap_handoff**: Final validation pass on roadmap → one handoff-readiness report. High-stakes; use fixed model (Grok code). **Manual trigger only** via ROADMAP_HANDOFF_VALIDATE queue mode.
- **research_synthesis**: Hostile check over synthesized research notes (sourcing strength, consistency, overclaim). **Liberal** type; use `"auto"` so pipelines can append VALIDATE runs frequently.
- **Future types**: Add rows as needed (e.g. `ingest_classification: { model: "auto" }`). Document in Parameters which types are high-stakes (fixed model, manual-only) vs liberal (Auto, pipeline-appendable).

```yaml
validator:
  roadmap_handoff:
    model: "grok-code"   # Cursor model id for Grok code; high-stakes → fixed model
  research_synthesis:
    model: "auto"        # liberal type; Validator may run often
    enabled: true        # when true, pipelines may append VALIDATE(research_synthesis)
    min_notes: 1         # minimum synthesized notes before queuing validation
  # Global controls for standalone VALIDATE/ROADMAP_HANDOFF_VALIDATE entries only
  global_max_per_run: 20        # hard cap on VALIDATE entries processed per EAT-QUEUE run (does NOT apply to post-pipeline validator)
  global_sampling_rate: 1.0     # 0.0–1.0; probability for pipeline-appended VALIDATE entries; post-pipeline validator runs every time (no sampling)
  # Post-pipeline validator: runs once per pipeline success after little val passes; does not count toward global_max_per_run. All types below must have model set.
  distill_readability:
    model: "auto"
    enabled: false       # when true, autonomous-distill may also append VALIDATE(distill_readability); post-pipeline always runs when little val ok
    min_words: 500
  ingest_classification:
    model: "auto"
  organize_path:
    model: "auto"
  express_summary:
    model: "auto"
  archive_candidate:
    model: "auto"
  roadmap_handoff_auto:
    model: "auto"
```

## prompt_defaults (Config)

- roadmap:
  - max_iterations_per_phase: 33
  - enable_context_tracking: true
  - context_util_threshold: 80
  - context_token_per_char: 0.25
  - context_window_tokens: 128000
  - recal_util_high_threshold: 70
  - max_depth: (optional; derived from phase when absent: 1–2→2, 3–4→3, 5–6→4)
  - branch_factor: 4
  - inject_extra_state: (optional; when true, roadmap-deepen pulls extra context; use with token_cap)
  - token_cap: 50000
- profiles:
  - deepen-aggressive: { token_cap: 50000, branch_factor: 4, inject_extra_state: true, max_depth: 4 }
  - (Profiles are **read-only presets**: they are consumed by auto-roadmap and the dispatcher but are never created or mutated by the Prompt-Crafter. When `params.profile` names a configured profile (e.g. "deepen-aggressive"), its object is merged **between** `prompt_defaults.roadmap` and the queue params, so it can only **pre-fill missing keys**; any explicit queue params from the crafter always win. When `params.profile` does **not** match a key under `prompt_defaults.profiles`, the dispatcher must treat the profile as missing (no preset merge) and fall back to `prompt_defaults.roadmap` + explicit params rather than failing or silently substituting another profile. Commander macros (e.g. **"Craft Deepen Aggressive"**) may still build queue entries that reference these profiles directly.)

**Profile namespaces (V4):** Conceptually, roadmap and CODE flows use separate profile buckets. **Roadmap profiles** (e.g. under `prompt_defaults.profiles` as above) are tuned for RESUME-ROADMAP / ROADMAP MODE (token_cap, branch_factor, max_depth, etc.). **CODE profiles** (e.g. for INGEST, ORGANIZE, DISTILL, EXPRESS) are TBD and may be added under a dedicated key such as `prompt_defaults.code_profiles` after roadmap deployment testing. Until then, CODE flows that present a profile gate must state clearly in chat: "Profiles are currently tuned for roadmap; CODE runs will mostly rely on per-mode defaults until CODE-specific profiles are configured." Do not offer roadmap-only profile names as if they applied to CODE runs without that warning.

**Project MOCs**: In each project MOC note, include a "Graph Focus" callout with a Dataview query that lists notes in that project, e.g. `WHERE project-id = "Test-Project"` for quick graph context.

---

**links frontmatter:** Always an array (e.g. `links: ["[[Resources Hub]]", "[[Related]]"]`). For Dataview, use `contains(links, "[[HubName]]")` or array membership.

**Tags vs frontmatter:** Tags are convenience only (e.g. #dev-task, #bug for QuickAdd and task filters). Pipelines and core filtering use frontmatter. Do not rely on tags for ingest/distill/archive logic.

Pipelines pass this note as context or read it when resolving hub names and archive thresholds. See [Cursor-Skill-Pipelines-Reference](Cursor-Skill-Pipelines-Reference.md) for pipeline order.
