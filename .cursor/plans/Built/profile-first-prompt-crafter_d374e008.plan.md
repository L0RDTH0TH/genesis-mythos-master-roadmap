---
name: profile-first-prompt-crafter
overview: Refactor the question-led Prompt-Crafter so roadmap profiles are chosen up front, while preserving existing tuned params, config defaults, and pipeline safety.
todos:
  - id: profile-flow-analysis
    content: Double-check current RESUME-ROADMAP question ordering and profile param wiring in the crafter implementation and dispatcher.
    status: completed
  - id: profile-meta-flow-design
    content: Design the internal profile meta-flow (none|existing|new|ai) that runs immediately after RESUME-ROADMAP action selection without violating User-Questions-and-Options-Reference §1.
    status: completed
  - id: params-precedence-guard
    content: Audit and, if needed, adjust the roadmap dispatcher merge order so queue params always override prompt_defaults.roadmap and profiles.
    status: completed
  - id: profile-validation-guard
    content: Add validation and graceful fallback behavior when a requested profile name is missing or removed from Second-Brain-Config.
    status: completed
  - id: docs-sync-profile-first
    content: Update Prompt-Crafter docs and Second-Brain-Config comments to describe profile-first behavior, precedence, and safety invariants.
    status: completed
isProject: false
---

### Goal

Refactor the question-led Prompt-Crafter so that, for ROADMAP (especially RESUME-ROADMAP), **profile selection happens before individual param tuning**, without breaking existing payload semantics, config fallback chains, or downstream roadmap pipelines.

### 1. Clarify invariants and current behavior

- **Question ordering invariant**: Preserve the core contract from `User-Questions-and-Options-Reference` §1 and `plan-mode-prompt-crafter.mdc`:
  - Still ask **every required question** for the active branch.
  - Maintain A/B/C semantics (A = explicit, B = omit → default, C = omit + reasoning into `user_guidance`).
- **Params precedence chain**: Keep the documented precedence from `Queue-Sources` and `Parameters`:
  - **queue entry params** → note `user_guidance`/queue `prompt` → `prompt_defaults.roadmap` / `prompt_defaults.profiles` → MCP tool defaults.
  - This guarantees **tuned params survive**: explicit queue params must always override any profile or config default.
- **Profile semantics (today)**:
  - `prompt_defaults.roadmap` holds base roadmap defaults (e.g. `max_iterations_per_phase`, `enable_context_tracking`, `context_util_threshold`, `token_cap`, `branch_factor`, etc.).
  - `prompt_defaults.profiles` (e.g. `deepen-aggressive`) defines named overrides merged when `params.profile` matches.
  - Prompt-crafter currently treats `profile` as just another late param (`question_order` 16 for RESUME-ROADMAP); it **assumes profiles already exist** in Config and **does not create or edit** them.

### 2. New high-level flow with profile-first

- **Move profile choice up in the logical flow while staying compatible with §1**:
  - After side selection (**CODE vs ROADMAP**) and mode/action narrowing (ROADMAP MODE vs RESUME-ROADMAP and "Which action?"), introduce an early **profile choice phase** for RESUME-ROADMAP, conceptually before most depth/branching questions.
  - Keep `Prompt-Crafter-Param-Table` as the **source of truth** for `question_order`, but allow a **two-pass implementation**:
    - Pass 1: Ask an early **profile meta-question** (does the user want a profile at all, and if so existing vs new vs AI suggested), without writing `params` yet.
    - Pass 2: When the engine reaches the literal `profile` param at position 16, it **reuses the earlier decision** to populate `params.profile` (or omit it) instead of asking again.
- **Early profile meta-question (conceptual position right after action)**:
  - Wording (high level, not yet wired as §1 text): explain that a profile is a named preset that can bundle `branch_factor`, `max_depth`, `token_cap`, `inject_extra_state`, etc.
  - Choices (mapping back onto A/B/C semantics):
    - **A** → "Use profile" (sub-flow determines existing vs new).
    - **B** → "No profile" (base `prompt_defaults.roadmap` + per-param tuning only; no `params.profile` key).
    - **C** → "AI reasoning" (suggest best starting profile or no-profile based on project/phase, then pick a concrete A or B and record a short explanation into `user_guidance`).
  - This phase sets **internal state** (e.g. `profile_mode: none|existing|new|ai`) but does **not yet set or modify Config**.

### 3. Sub-flow for A (use a profile) without breaking configs

- **Existing profile path**:
  - Enumerate available profile names from `Second-Brain-Config` `prompt_defaults.profiles`.
  - If there is **at least one** profile:
    - Ask a single-select question: which profile? (A/B/C semantics can be mapped to concrete choices + AI suggestion).
    - Store the chosen name in a temporary field (e.g. `selected_profile_name`).
  - If **no profiles** exist in config:
    - Treat "existing" as **unavailable**; fall back to either **B (no profile)** or offer AI reasoning that defaults to "no profile" and explains why.
    - This shields from the "silent no-op profile" problem where `params.profile` refers to a non-existent preset.
- **New profile path (concept)**:
  - For this hardening pass, treat **new profile creation as non-persistent** to avoid unexpected Config writes:
    - If user picks "new profile" and specifies a name, treat that **only as a label for the current run** (`params.profile: "my-label"`) and **do not auto-write** a new `prompt_defaults.profiles.my-label` entry.
    - All tuned params chosen later still live in `params` and therefore remain authoritative for the run; the profile name is merely an advisory tag for future inspection.
  - Optionally, after summary, you can **propose** that the user manually copy the tuned param bundle into `Second-Brain-Config` under that profile name (with a small preview snippet), but no automatic write.
  - This keeps profile creation out of the critical path and avoids backup/snapshot complexity for Config edits.

### 4. Preserving tuned params vs profile defaults

- **Hard guarantee**: tuned param values coming from earlier/resolved questions must not be overwritten by any profile or config merge.
  - Implementation rule: when constructing `params` before queue write:
    - Start from **an empty object**.
    - Insert keys directly from A-choices (explicit user answers) and C-resolutions.
    - Only then, when the dispatcher/pipeline consumes the payload, allow `prompt_defaults.roadmap` and `prompt_defaults.profiles[selected_profile]` to **fill in only missing keys**, never override.
- **Shielding against unintended overrides**:
  - Document and, if needed, enforce in `Queue-Sources` / roadmap dispatcher that merge order is:
    - `effectiveParams = deepMerge(prompt_defaults.roadmap, prompt_defaults.profiles[profileName]?, queueParams)`
  - That is: `queueParams` (what the crafter built) are merged **last**; they win over both base defaults and profile presets.
  - This ensures that even if the user picks a profile **after** tuning some params, their explicit tuned values remain in effect.

### 5. Handling B and C paths safely

- **B (default — no profile)**:
  - Do **not** set `params.profile`.
  - Ask all RESUME-ROADMAP params per the existing `question_order` list, exactly as today.
  - Pipelines then combine explicit params with `prompt_defaults.roadmap` as usual.
- **C (AI reasoning)**:
  - Use project + roadmap-state context to decide between:
    - "No profile" (most conservative; rely on base `prompt_defaults.roadmap`), or
    - An **existing named profile** (e.g. `deepen-aggressive`) when there is a clear, documented use case.
  - Emit **1–3 sentences** of reasoning and append them to `params.user_guidance` or payload `prompt`.
  - Convert the AI decision into a **concrete A/B result**:
    - If it picks a profile, behave exactly like the "existing profile" path above.
    - If it picks no profile, behave like B.
  - Never produce a profile name that isn’t present in Config; if AI wants a new category, it should recommend **tuned one-off params** plus a note in `user_guidance`, not a phantom profile.

### 6. Question ordering and compatibility

- **No breakage for existing §1 ordering**:
  - Keep the **canonical `question_order` table** in `Prompt-Crafter-Param-Table` unchanged for RESUME-ROADMAP (action, project_id, phase, …, branch_factor, profile, userText, queue_next).
  - Internally, implement **profile meta-flow as a thin wrapper** that:
    - Runs immediately after action selection.
    - Caches a decision (`profile_mode`, `selected_profile_name?`).
    - When the engine reaches the actual `profile` param at order 16, it **does not ask** a redundant question; instead it directly sets or omits `params.profile` based on the cached decision.
  - This preserves the invariant that every param in the table has a well-defined question and answer, but avoids user-facing repetition.

### 7. Failure modes and shields

- **Non-existent profile name**:
  - Guardrail: before accepting any profile name (from user or AI), validate it against `prompt_defaults.profiles`.
  - If not found:
    - Clear `selected_profile_name`.
    - Fall back to B semantics (no profile) and record a short explanation in `user_guidance` (e.g. "Requested profile 'X' not found in config; falling back to base defaults + explicit params.").
- **Config changes out of band**:
  - If Config is edited and a profile is removed/renamed between crafting and EAT-QUEUE:
    - Dispatcher must treat missing `prompt_defaults.profiles[profileName]` the same way: **ignore the profile**, do **not** fail the run, and lean entirely on explicit params + `prompt_defaults.roadmap`.
    - Log a soft warning in roadmap logs for observability; do not break the pipeline.
- **Future profile persistence**:
  - If later you want profile-creation to be automated, gate it behind:
    - A dedicated queue mode or explicit command (e.g. "SAVE PROFILE"),
    - Snapshot + backup rules for `Second-Brain-Config`, and
    - A separate skill or rule responsible for safe Config edits.
  - For this pass, **do not write** to Config from the crafter itself.

### 8. Observability and docs

- **Logs / meta**:
  - When `params.profile` is present, roadmap logs (e.g. workflow_state / phase logs) should include a small note like `profile: deepen-aggressive (source: Prompt-Crafter)`.
  - When AI reasoning (C) is used to choose or skip a profile, merge its explanation into `user_guidance` for guidance-aware runs.
- **Docs updates**:
  - Update `Prompt-Crafter-Structure-Detailed` and `User-Questions-and-Options-Reference` to:
    - Clarify that for RESUME-ROADMAP, profile is logically chosen immediately after action, but still mapped to the `profile` param.
    - Explain the three modes: **no profile**, **existing profile**, **AI-chosen profile**, with explicit statements that explicit params always override profiles.
  - Update `Second-Brain-Config` comments around `prompt_defaults.roadmap` and `prompt_defaults.profiles` to highlight the merge order and the "no Config writes from crafter" invariant.

### 9. Safety summary

- **Never** let a profile silently override explicit tuned params; queue params remain authoritative.
- **Never** create or mutate profiles in Config from inside the crafter; treat profiles as read-only presets.
- **Always** validate any profile name (user or AI) against `prompt_defaults.profiles`; on mismatch, gracefully fall back to base defaults and tuned params, with a trace in `user_guidance`/logs.
- Ensure that if anything about profile logic fails, the worst case is: **a safe, explicit, profile-less RESUME-ROADMAP payload** built purely from the already-tuned params and `prompt_defaults.roadmap`.

