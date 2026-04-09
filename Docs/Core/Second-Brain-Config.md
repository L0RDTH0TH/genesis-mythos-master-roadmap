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

## profiles (familial config)

**Preferred way:** use familial keys on queue **`params`** (or nested **`params.profiles`**). **Flat keys remain fully supported** as overrides via **deepMerge** (explicit queue entry → profile expansion → this file → implicit defaults).

**Canonical reference:** [[3-Resources/Second-Brain/Docs/Core/Config-Profiles|Config-Profiles]] — `speed_mode`, `repair_strategy`, `validator_tier` and **deepMerge** order (queue entry explicit keys win over profile expansion over this file over defaults).

**Auto-applied default profile:** When a queue line omits familial keys, **config-resolve-profile** still applies the same default bundle as **`balance` + `repair_first` + `forgiving`** in memory during merge (see Config-Profiles **Resolution flow**). The **canonical default labels** (Option B) are spelled out below; flat YAML in *this* file for overlapping keys stays as **explicit overrides** — behavior is unchanged for existing runs.

**Deprecation (soft):** Prefer familial names on queue **`params`** (or the nested `params.profiles` object) instead of setting **`queue.inline_*`**, **`queue.roadmap_pass_order`**, **`validator.tiered_blocks_enabled`**, and **`pipeline_mode`** directly for every run. **All flat keys remain supported** and merge with expanded profiles per Config-Profiles; nothing is removed.

```yaml
# Mirror of Docs/Core/Config-Profiles.md — keep in sync when adding families
profiles:
  speed_mode:
    fast: {}
    balance: {}   # default familial label
    extreme: {}
  repair_strategy:
    repair_first: {}   # default
    forward_first: {}
  validator_tier:
    aggressive: {}
    forgiving: {}   # default
```

**Canonical default familial bundle (Option B)** — same three labels the resolver injects when familial keys are omitted (documentation mirror; not a second merge root):

```yaml
speed_mode: balance
repair_strategy: repair_first
validator_tier: forgiving
```

### Repair-Heavy / Hygiene-Focused Mode (vault defaults)

Preferred **familial** bundle for reliable **repair-first** + **Pass 3** inline drain (same three labels as above). **Flat** overrides below are written explicitly in **`queue:`** / **`validator`** YAML so they win via **deepMerge** over profile expansion alone (see [[3-Resources/Second-Brain/Docs/Core/Config-Profiles|Config-Profiles]] § deepMerge).

**Sandbox (2026-04-07):** followup-**deepen** dispatched while **repair-l1-hygiene** was held under **repair_first** single-slot, **`nested_validation_passed: false`**, **`suppress_clean_drain: true`**, no **`inline_repair_pending`** flip, repair row already on **PQ** but Pass 3 skipped. **This combination** ensures **`inline_repair_pending`** can trigger Pass 3 **after** **A.5b** hygiene appends **even when** a forward deepen wins the **initial** slot — **queue.mdc** **A.5.0** still requires same-run pending flags; **`inline_forward_followup_drain_enabled: true`** and higher **`max_inline_a5b_repair_generations_per_run`** give Pass 3 room to run **repair** and **forward** inline waves when those flags are set per contract.

**Flat overrides (effective with this mode):**

| Key | Value |
|-----|--------|
| `queue.inline_a5b_repair_drain_enabled` | `true` |
| `queue.inline_forward_followup_drain_enabled` | `true` |
| `queue.roadmap_pass_order` | `repair_first` |
| `queue.max_inline_a5b_repair_generations_per_run` | `8` |
| `validator.tiered_blocks_enabled` | `true` |

### queue_continuation (empty-queue bootstrap after lane drain)

When the **lane** **PQ** is **empty** after **Pass 3** / **A.7** (desired after balance work + repair churn), **Layer 1** **A.1b** (**[[.cursor/rules/agents/queue.mdc|queue.mdc]]**) may **append** the next **`RESUME_ROADMAP`** **`deepen`** from **`.technical/…/queue-continuation.jsonl`** (**QCONT**) or **unfinished-roadmap** fallback per **[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]**. **`continuation_log_enabled: true`** is still required so **A.5e** can populate **QCONT**, but missing/empty QCONT is now treated as no-record context (not an immediate bootstrap abort).

**Operator intent (balance → next balance cycle):** next bootstrapped line should be **`effective_pipeline_mode`** **balance** (familial **`speed_mode: balance`**), **`params.roadmap_track`** from **`queue_continuation.bootstrap_track`** (default **`conceptual`**), **`params.action`** from **`queue_continuation.bootstrap_action`** (default **`deepen`**) — reflected when **Layer 1** builds the candidate from **`suggested_next`** or **deterministic** **A.1b** step **10** (**not** separate **Queue-Continuation-Spec** v1 schema keys). Override **`bootstrap_track`** in this YAML (or align **[[3-Resources/Second-Brain/Docs/Core/Config-Profiles|Config-Profiles]]** defaults) when focus shifts to **execution** or another track.

```yaml
queue_continuation:
  continuation_log_enabled: true
  empty_queue_bootstrap_enabled: true
  empty_queue_bootstrap_auto_append: true
  empty_queue_bootstrap_tail_lines: 50
  empty_queue_bootstrap_max_age_minutes: 1440
  empty_queue_bootstrap_force_when_unfinished: true
  empty_queue_bootstrap_prompt_craft: false
  empty_queue_bootstrap_prompt_craft_on_no_record: false
  empty_queue_bootstrap_deterministic_when_no_record: true
  empty_queue_bootstrap_create_missing_qcont: true  # when true, A.1b may initialize missing lane QCONT before no-record fallback; when false, no init, still no-record flow
  bootstrap_track: conceptual   # params.roadmap_track on synthesized deepen lines; use execution, procedural, etc. when needed
  bootstrap_action: deepen      # params.action when synthesizing; must match RESUME_ROADMAP allowed actions
  # bootstrap_source: token workflow_state.md (default) → Layer 1 resolves the file by bootstrap_track:
  #   conceptual → Roadmap/workflow_state.md; execution → Roadmap/Execution/workflow_state-execution.md; other → try conceptual then execution path.
  #   A non-default value is read as a path relative to 1-Projects/<project_id>/ (see queue.mdc A.1b). Used for current_subphase_index in bootstrap user_guidance.
  bootstrap_source: workflow_state.md
```

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
- **python_orchestrator_enabled**: true — Layer 1 EAT-QUEUE may read **EQPLAN** (`eat_queue_run_plan.json` colocated with **PQ** — legacy `.technical/eat_queue_run_plan.json` or per-track under `.technical/parallel/<track>/`; see [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x**) produced by `python3 -m scripts.eat_queue_core.full_cycle` / plan and execute **`intents`** in order (see [[3-Resources/Second-Brain/Docs/Python-Queue-Orchestrator|Python-Queue-Orchestrator]]). Set **false** for legacy LLM-driven ordering (default when absent).
- **central_pool_fanout_enabled**: when **true**, Layer 1 **A.0.4** runs **`pool_sync`** before wrappers so **`.technical/prompt-queue.jsonl`** (pool) is merged into per-track **PQ** (see **`pool_sync_strict_central_only`**); **A.7** removes consumed ids from **pool** and **PQ** (see [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0.4**, **A.7**).
- **pool_sync_strict_central_only**: when **true**, **`scripts.eat_queue_core.pool_sync`** overwrites the track **PQ** with **only** lane-filtered central-pool lines (**legacy**; drops lane-only rows that exist only in the track file). Default **false**: **merge** central lines with lane-only rows already in the track **PQ** that match the lane and are absent from the pool (see [[3-Resources/Second-Brain/Docs/Dual-track-EAT-QUEUE-Operator|Dual-track-EAT-QUEUE-Operator]] § Lane-only preservation).
- **rationale_enforcement_enabled** (`true` \| `false`, default **`false`**): when **`true`**, Layer 1 ([[.cursor/rules/agents/queue.mdc|queue.mdc]]) **must** require **`params.option_evaluation`** on gated **`RESUME_ROADMAP`** lines (execution track — see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Parallel execution tracking). The Python harness validates shape when emitting plans.
- **allowed_lanes** (under **`queue:`** YAML): list of strings allowed for **`queue_lane`** on prompt-queue JSONL lines and for Layer 0 **`EAT-QUEUE lane <name>`**. Default in YAML below: `default`, `shared`, `sandbox`, `godot`, `core`. Unknown lane on append or filter → reject / error (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Queue lanes).
- **harness_validation_mode** (`advisory` \| `strict`, default **`advisory`**): Layer 1 **A.5i** after pipeline **Task** returns — parse **`nested_subagent_ledger`**, **`blocked_scope`** on hard-block paths; **`strict`** upgrades refusals per [[3-Resources/Second-Brain/Docs/Harness-Patterns-and-Guidelines|Harness-Patterns-and-Guidelines]] §4.
- **roadmap_pass_order** (`repair_first` \| `forward_first`): Layer 1 **A.4c** roadmap multi-dispatch; default **`repair_first`** aligns with familial **`repair_strategy: repair_first`** (overridable flat key).
- **inline_a5b_repair_drain_enabled**: default **`true`** when omitted in older configs; explicit **`true`** here — Pass 3 repair drain (see [[3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Pass-3-Operator-Guide|EAT-QUEUE Pass 3 Operator Guide]]).
- **inline_forward_followup_drain_enabled**: Pass 3 forward follow-up wave — **`true`** in **Repair-Heavy / Hygiene-Focused Mode** (see § **profiles**) so forward-class appends can set **`inline_forward_followup_pending`** and drain in Pass 3 per **A.5.0** (when gate and caps allow).
- **max_inline_a5b_repair_generations_per_run** / **max_inline_forward_followup_generations_per_run**: Pass 3 generation caps (**A.5.0**). **Repair-Heavy** sets **`max_inline_a5b_repair_generations_per_run: 8`**; forward cap remains **3** unless changed.

The following **`queue:`** block is machine-readable for `scripts/queue-gate-compute.py` and related tools (must stay aligned with the bullet above). Keys **`roadmap_pass_order`**, **`inline_*`**, and **`max_inline_*`** implement **Repair-Heavy / Hygiene-Focused Mode** defaults (§ **profiles**); they remain **explicit flat overrides** — change them here to diverge without editing queue JSONL.

queue:
  python_orchestrator_enabled: true
  central_pool_fanout_enabled: true
  pool_sync_strict_central_only: false
  rationale_enforcement_enabled: false
  harness_validation_mode: advisory
  roadmap_pass_order: repair_first
  inline_a5b_repair_drain_enabled: true
  inline_forward_followup_drain_enabled: true
  max_inline_a5b_repair_generations_per_run: 8
  max_inline_forward_followup_generations_per_run: 3
  allowed_lanes:
    - default
    - shared
    - sandbox
    - godot
    - core

## tracking (intent receipts / observability)

- **intent_receipts_enabled** (`true` \| `false`, default **`true`**): when **`true`**, `scripts.eat_queue_core` appends **`intent_snapshot`** / **`intent_actual_receipt`** rows to **`task-handoff-comms.jsonl`** beside **PQ** (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Parallel execution tracking). **Speed-mode opt-out:** set **`tracking.intent_receipts_enabled: false`** below (or omit and override in a forked Config) to skip receipt appends and reduce JSONL growth.

```yaml
tracking:
  intent_receipts_enabled: true
```

## parallel_execution (dual-track EAT-QUEUE; two Cursor chats)

- **enabled**: when **true** and Layer 0 passes **`EAT-QUEUE lane sandbox`** or **`lane godot`**, the Queue subagent uses **per-track bundles** under `.technical/parallel/<track>/` for the prompt queue, plan JSON, continuation log, audit JSONL, and optional tmp-prompt (see [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x**).
- **default_to_legacy**: when **true**, ignore bundle routing even if enabled (single `.technical/prompt-queue.jsonl`).
- **GitForge**: global **`.technical/.gitforge.lock`** with **`lock_timeout_seconds`**; **`policy: lock_last_wins`** — if lock not acquired, skip GitForge and log (see [[.cursor/agents/gitforge.md|agents/gitforge.md]]).
- **lane_project_id** (per **`tracks[]`** row): slug under **`1-Projects/`** for **A.0z** / **A.2a.1** — dual-track roadmap state must stay under **`1-Projects/<lane_project_id>/`** for that lane.
- **research_whitelist_enforced** (per **`tracks[]`** row, optional boolean, default **true** when omitted): when **true**, Layer 1 / resolver **should** emit **`research_url_intent_audit: allowlist_active`** (or equivalent parse-safe **`layer1_resolver_hints`** / **`queue_continuation`** fragment) so EAT-QUEUE runs log that [[.cursor/rules/agents/execution-research-whitelist|execution-research-whitelist]] §0 applies before **`Task(research)`** on execution-track code-precision. Operators may set **false** only for emergency debugging (not normative).
- **Watcher**: keep canonical **`watcher.canonical_path`** for the Obsidian plugin; optional **per-track mirrors** when **`watcher.enable_mirrors`** is true (see [[.cursor/rules/always/watcher-result-append.mdc|watcher-result-append]]).

Machine-readable block (keep aligned with bullets):

```yaml
parallel_execution:
  enabled: true
  default_to_legacy: false
  tracks:
    - id: sandbox
      lane: sandbox
      lane_project_id: sandbox-genesis-mythos-master
      technical_subdir: parallel/sandbox
      branch_prefix: sandbox-
      export_path: "/home/darth/Documents/gmm-roadmap-export"
      research_whitelist_enforced: true
    - id: godot
      lane: godot
      lane_project_id: godot-genesis-mythos-master
      technical_subdir: parallel/godot
      branch_prefix: godot-
      export_path: "/home/darth/Documents/gmm-roadmap-export"
      research_whitelist_enforced: true
  gitforge:
    lock_timeout_seconds: 30
    policy: lock_last_wins
  watcher:
    canonical_path: "3-Resources/Watcher-Result.md"
    enable_mirrors: true
```

## gitforge (Layer 1 post-queue git/export)

- **enabled**: true — when **true**, Queue may run **A.7a** after a successful prompt-queue **A.7** (see [[.cursor/rules/agents/queue.mdc|queue.mdc]]). Set **false** to disable the post-queue git tail.
- **Pipeline tier:** **`effective_pipeline_mode`** **`speed`** → GitForge is **not** called (fast runs skip automatic vault git). **`balance`** and **`quality`** → **one** **`Task(gitforge)`** after **A.7**, hand-off **`mode: balance`** for both; **`quality`** is traced via **`source_pipeline_mode`** (same git rules as balance — quality is stricter **pipeline** enforcement, not a separate export tier).
- **export_repo_root**: absolute path to the `gmm-roadmap-export` checkout (see [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]).
- **integration_branch**: branch name for the **canonical system mirror** — complete `.cursor/` (including **`.cursor/sync/`**), full queue **`scripts/`** (`eat_queue_core`, `queue-gate-compute.py`, **`gitforge_lock.py`**), full **`Docs/`** + **`Docs/Core/`** (all top-level `3-Resources/Second-Brain/*.md`) + **`Docs/Second-Brain-User-Flows/`** (see workflow § Branch purposes and export coverage). Default `iteration-2-roadmap-rules`.
- **Engine branches (convention):** **`sandbox-genesis-mythos-master`**, **`godot-genesis-mythos-master`** — **roadmap-only** lines: publish **`Roadmap/`** (includes **`Roadmap/Execution/`** when the project is on the **execution** roadmap track) + anchors from the matching **`lane_project_id`** / `GMM_PROJECT_ROOT`. Do **not** publish global `.cursor/`, `scripts/`, or system `Docs/` on engine branches. Pairs with **EAT-QUEUE** **`sandbox`** / **`godot`** lanes via **`parallel_execution.tracks[]`**. Align with [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] Step 1b and [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- **invoke_on_empty_queue**: false — when false, skip GitForge when there were no prompt-queue entries to process after A.1 (Step 0–only or empty file).
- **invoke_only_on_clean_success**: true — when true, skip GitForge if any prompt-queue entry this run got a failure disposition.

### GitHub branch URLs (open in Chrome)

Export remote: **`https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap.git`**. Clickable branch roots (GitHub **tree** view):

| Branch | Browse |
| --- | --- |
| `main` | [github.com/.../tree/main](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap/tree/main) |
| `iteration-2-roadmap-rules` (integration — **`gitforge.integration_branch`**) | [github.com/.../tree/iteration-2-roadmap-rules](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap/tree/iteration-2-roadmap-rules) |
| `sandbox-genesis-mythos-master` (sandbox engine line) | [github.com/.../tree/sandbox-genesis-mythos-master](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap/tree/sandbox-genesis-mythos-master) |
| `godot-genesis-mythos-master` (godot engine line) | [github.com/.../tree/godot-genesis-mythos-master](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap/tree/godot-genesis-mythos-master) |

Machine-readable block (keep aligned with bullets):

```yaml
gitforge:
  enabled: true
  export_repo_root: "/home/darth/Documents/gmm-roadmap-export"
  vault_repo_remote: "origin"
  integration_branch: "iteration-2-roadmap-rules"
  # Export contract (see Docs/git-push-workflow — § Branch purposes and export coverage):
  export_contract:
    integration_includes:
      - ".cursor/agents/"
      - ".cursor/rules/"
      - ".cursor/skills/"
      - ".cursor/sync/"
      - "scripts/eat_queue_core/"
      - "scripts/queue-gate-compute.py"
      - "scripts/gitforge_lock.py"
      - "Docs/"  # from 3-Resources/Second-Brain/Docs/
      - "Docs/Core/*.md"  # all top-level Second-Brain dev *.md + Roadmap Structure + Watcher/Errors + Run-Telemetry-Summary copies
      - "Docs/Second-Brain-User-Flows/"
    engine_includes:
      - "Roadmap/"
      - "<PROJ_ID>-goal.md"
      - "<PROJ_ID>-Roadmap-MOC.md"
    engine_forbidden_prefixes:
      - ".cursor/"
      - "scripts/"
      - "Docs/"
  invoke_on_empty_queue: false
  invoke_only_on_clean_success: true
  modes:
    fast: { tag: false, export_sync: false }
    balance: { tag: true, export_sync: false }
    extreme: { tag: true, export_sync: false, require_confirmation: false }
```

## telemetry_summary (EAT-QUEUE committed summary)

- **enabled**: when **true**, Layer 1 runs **`scripts/generate_telemetry_summary.py`** after **A.7** and **before** **A.7a** GitForge when gates pass (see [[.cursor/rules/agents/queue.mdc|queue.mdc]] **Run Telemetry Summary**). Produces a **clean first-surface** markdown file for operators and **GitHub / Grok** (mirrored with **`Docs/Core/`** in [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]]).
- **canonical_path**: vault-relative path to the **overwritten** latest summary (default below).
- **skip_on_speed_mode**: when **true** (default), **`speed`** runs skip summary generation (aligned with GitForge **A.7a** speed skip).
- **invoke_only_on_clean_success** / **invoke_on_empty_queue**: mirror **gitforge** defaults — skip when dispatch failures or empty consumption (see queue.mdc).
- **require_gitforge_enabled**: when **false** (default), summary runs even if **`gitforge.enabled`** is **false**; set **true** to tie invocation to GitForge’s master switch.
- **archive_enabled** / **archive_dir**: optional **append-only** timestamped copies (`Run-Telemetry-Summary--<ISO>.md`).
- **dry_run**: no persistent key — use script **`--dry-run`** for stdout-only.

```yaml
telemetry_summary:
  enabled: true
  canonical_path: "3-Resources/Second-Brain/Docs/Core/Run-Telemetry-Summary.md"
  skip_on_speed_mode: true
  invoke_on_empty_queue: false
  invoke_only_on_clean_success: true
  require_gitforge_enabled: false
  archive_enabled: false
  archive_dir: "3-Resources/Second-Brain/Docs/Core/Run-Telemetry-Archive"
```

## task_harden (capability probing)

- **mcp_probe_mode**: "assume_unavailable" — controls whether the roadmap subagent runs the lightweight Obsidian MCP availability capability probe at the start of each `Task(subagent_type: "roadmap")` invocation.
  - **auto**: perform the probe and set `mcp_available` from the probe outcome.
  - **assume_available**: skip the probe and set `mcp_available: true`.
  - **assume_unavailable**: skip the probe and set `mcp_available: false` (force inline-edit backend).

## pipeline_mode and validator_profiles

- **pipeline_mode**: balance  # fast | balance | extreme — default validator/safety profile for roadmap/research; **overridable flat key** (matches default **`speed_mode: balance`** expansion; see § **profiles**)
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
- **deepen_multi_artifact**: false — when false (default in **prompt_defaults.roadmap**), roadmap-deepen creates **one** structural phase-tree note per RESUME_ROADMAP deepen pass; set **true** (or use profile **deepen-aggressive**) to allow multi-mint **branch_factor** / **batch_subphases** / **max_depth** batching.
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
- **tiered_blocks_enabled** (optional; in YAML below): default **`true`** — tiered nested validator Success gate; maps to familial **`validator_tier: forgiving`**. Set **`false`** for **`validator_tier: aggressive`**-style strict behavior (overridable flat key).

```yaml
validator:
  tiered_blocks_enabled: true   # overridable; matches default **validator_tier: forgiving** (tiered nested Success gate)
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
  - deepen_multi_artifact: false
  - max_depth: (optional; derived from phase when absent: 1–2→2, 3–4→3, 5–6→4; only batches when deepen_multi_artifact true)
  - branch_factor: 1
  - inject_extra_state: (optional; when true, roadmap-deepen pulls extra context; use with token_cap)
  - token_cap: 50000
- profiles:
  - deepen-aggressive: { token_cap: 50000, deepen_multi_artifact: true, branch_factor: 4, inject_extra_state: true, max_depth: 4 }
  - (Profiles are **read-only presets**: they are consumed by auto-roadmap and the dispatcher but are never created or mutated by the Prompt-Crafter. When `params.profile` names a configured profile (e.g. "deepen-aggressive"), its object is merged **between** `prompt_defaults.roadmap` and the queue params, so it can only **pre-fill missing keys**; any explicit queue params from the crafter always win. When `params.profile` does **not** match a key under `prompt_defaults.profiles`, the dispatcher must treat the profile as missing (no preset merge) and fall back to `prompt_defaults.roadmap` + explicit params rather than failing or silently substituting another profile. Commander macros (e.g. **"Craft Deepen Aggressive"**) may still build queue entries that reference these profiles directly.)

**Profile namespaces (V4):** Conceptually, roadmap and CODE flows use separate profile buckets. **Roadmap profiles** (e.g. under `prompt_defaults.profiles` as above) are tuned for RESUME-ROADMAP / ROADMAP MODE (token_cap, branch_factor, max_depth, etc.). **CODE profiles** (e.g. for INGEST, ORGANIZE, DISTILL, EXPRESS) are TBD and may be added under a dedicated key such as `prompt_defaults.code_profiles` after roadmap deployment testing. Until then, CODE flows that present a profile gate must state clearly in chat: "Profiles are currently tuned for roadmap; CODE runs will mostly rely on per-mode defaults until CODE-specific profiles are configured." Do not offer roadmap-only profile names as if they applied to CODE runs without that warning.

**Project MOCs**: In each project MOC note, include a "Graph Focus" callout with a Dataview query that lists notes in that project, e.g. `WHERE project-id = "Test-Project"` for quick graph context.

---

**links frontmatter:** Always an array (e.g. `links: ["[[Resources Hub]]", "[[Related]]"]`). For Dataview, use `contains(links, "[[HubName]]")` or array membership.

**Tags vs frontmatter:** Tags are convenience only (e.g. #dev-task, #bug for QuickAdd and task filters). Pipelines and core filtering use frontmatter. Do not rely on tags for ingest/distill/archive logic.

Pipelines pass this note as context or read it when resolving hub names and archive thresholds. See [Cursor-Skill-Pipelines-Reference](Cursor-Skill-Pipelines-Reference.md) for pipeline order.
