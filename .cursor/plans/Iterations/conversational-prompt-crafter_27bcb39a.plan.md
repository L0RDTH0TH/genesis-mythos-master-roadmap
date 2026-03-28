---
name: conversational-prompt-crafter
overview: Refactor the Prompt Crafter from a rigid A/B/C question-led flow into a conversational param collector with profile-first selection, while preserving queue contracts and adding stronger guards against configuration and scratchpad failures.
todos:
  - id: survey-contracts
    content: Re-read prompt-crafter rule, User-Questions-and-Options-Reference §1, Prompt-Crafter-Param-Table, and Queue-Sources to confirm all current contracts and invariants that must be preserved.
    status: pending
  - id: design-profile-gate
    content: Design the profile-first conversational gate, including how to list existing profiles, represent ad-hoc profiles, and handle missing or mismatched profile names without silent substitution.
    status: pending
  - id: conversational-param-loop
    content: Design the conversational param collection loop that walks params in order, maps free-form answers back to A/B/C semantics internally, and updates tmp-prompt.json incrementally.
    status: pending
  - id: roadmap-code-integration
    content: Define how profile-aware conversational collection plugs into RESUME-ROADMAP and CODE modes so that auto-eat-queue and pipelines see unchanged payloads.
    status: pending
  - id: safety-and-shielding
    content: Specify explicit checks and failure paths for scratchpad corruption, config/profile issues, queue write failures, and invalid param values to avoid silent degradation.
    status: pending
  - id: docs-and-rules-update
    content: Plan updates to User-Questions-and-Options-Reference, Prompt-Crafter-Param-Table, plan-mode-prompt-crafter.mdc, and Second-Brain-Config comments to describe the conversational crafter and profile semantics.
    status: pending
  - id: integration-review
    content: Walk through representative end-to-end scenarios (INGEST, ORGANIZE, ROADMAP MODE + RESUME-ROADMAP) to verify that the new conversational flow produces valid queue entries and respects existing safety invariants.
    status: pending
isProject: false
---

## Conversational Prompt Crafter Refactor

### Goals

- **Shift interaction style**: Move from strict one-question-per-message A/B/C flow to a conversational, progressive param collector that still results in the same `mode` + `params` payload.
- **Introduce profile-first gate**: Always start with a "use existing vs create new profile" choice, surfacing profiles from `Second-Brain-Config` and handling missing/mismatched profiles safely.
- **Preserve integrations**: Keep queue format, param semantics, and downstream pipeline behavior (auto-eat-queue, roadmap, CODE pipelines) unchanged from their perspective.
- **Harden against failures**: Add explicit shielding for config/scratchpad/profile edge cases so the crafter fails loud with guidance instead of silently degrading.

### 1. Map current contracts and constraints

- **Prompt-crafter rule and questions**: Treat `[.cursor/rules/context/plan-mode-prompt-crafter.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/plan-mode-prompt-crafter.mdc)` and `[User-Questions-and-Options-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)` as the source of truth for:
  - When the "question-led" mode is triggered ("We are making a prompt" phrases).
  - The required payload shape (`mode`, `params`, optional `param_meta`, `agent_reasoning`).
  - Scratchpad expectations: `session_id`, `mode`, `asked`, `explicit_choices`, `agent_reasoning_log`, `final_payload_draft` and failure behavior when `.technical/tmp-prompt.json` is corrupt.
- **Param inventory**: Use `[Prompt-Crafter-Param-Table.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)` to:
  - Confirm which params exist per owner (CODE → INGEST/ORGANIZE/DISTILL/EXPRESS/ARCHIVE, ROADMAP MODE, RESUME-ROADMAP, task modes).
  - Ensure the conversational collector still covers every param that currently appears in `question_order`, even if it surfaces them more naturally.
- **Config and profiles**: From `[Second-Brain-Config.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Second-Brain-Config.md)` and `[Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md)`, note that:
  - `crafting.tmp_prompt_path` and `crafting.max_reasoning_sentences` are fixed.
  - `prompt_defaults.roadmap` and `prompt_defaults.profiles` are **read-only presets** that auto-eat-queue merges as `effectiveParams = deepMerge(prompt_defaults.roadmap, prompt_defaults.profiles[profile], queueParams)`.
  - When `params.profile` does **not** match a configured profile name, dispatchers must treat it as "no profile" rather than silently substituting; the conversational crafter should surface this to the user.
- **Queue consumption**: Respect that `[auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc)` and `[Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md)`:
  - Expect stable `mode` strings (INGEST MODE, ORGANIZE MODE, ROADMAP MODE, RESUME-ROADMAP, etc.).
  - Treat `params` as already merged against defaults; they do not care how the UI collected them.
  - Use `agent_reasoning` as AI-only decoration and `prompt` / `user_guidance` as human text.

### 2. Design the profile-first conversational entry

- **New entry gate** (replacing or fronting "Message 1/2" in §1):
  - First conversational turn for CODE and ROADMAP branches becomes a profile gate:
    - Present a summary of what a "profile" is (named preset that fills defaults only).
    - Offer: **A. Use existing profile**, **B. Use default behavior**, **C. Create a new ad-hoc profile for this run** – but implemented as natural-language options, not as hard-coded A/B/C the user must type.
  - When the user picks "use existing":
    - Read `prompt_defaults.profiles` from `Second-Brain-Config`.
    - List available profile names with short one-line descriptions derived from `param_meta` and Config comments.
    - Let the user pick by name or number; normalize to an exact profile key.
  - When the user picks "new profile":
    - Prompt for a profile **label** and any preferences they want to override (e.g. "more aggressive deepen", "fewer candidates").
    - Represent this as an **ephemeral, in-scratchpad profile** (not written back to Config): a small object under `final_payload_draft.profile_details` that the crafter uses to derive concrete numeric/boolean values for params before finalization.
- **Shielding for profiles**:
  - If `prompt_defaults.profiles` is empty or missing when user asks for "use existing", reply clearly (e.g. "No profiles are configured yet; using default behavior instead") and fall back to the default profile path.
  - If user names a profile that is not a key under `prompt_defaults.profiles`, do **not** silently map to another profile; instead:
    - Confirm that it is unknown.
    - Offer to either use the closest match (if any), treat it as a free-text guidance tag only, or re-ask.
  - Preserve the existing dispatcher guarantee: an unknown `params.profile` still yields a valid run (defaults + queueParams), but the crafter should warn the user before emitting such a payload.

### 3. Redesign param collection as a conversational loop

- **Internal param list**:
  - For the chosen branch and mode, derive the ordered param list from `Prompt-Crafter-Param-Table` and `User-Questions-and-Options-Reference §1 (Param order by branch)`.
  - Build an in-memory checklist of remaining params; mark those that are fully implied by the chosen profile + defaults as already satisfied but still visible for confirmation.
- **Conversational prompts instead of A/B/C**:
  - For each param in order, generate a short, natural-language question based on the existing "It does" and `defaultWhenC` text, but:
    - Offer concrete suggestions as inline choices (e.g. "Common values: strict-para, loose-para"), not as a forced A/B/C click box.
    - Allow the user to type direct values or say "use default" / "skip".
  - For `accepts_manual_text` params (e.g. `source_file`, `user_guidance`, `sectionOrTaskLocator`), keep a separate **manual text** pass:
    - Once structural params are fixed, walk the subset of params with `accepts_manual_text: true` that are included in this run, and ask open-text questions ("What is the source file?", "Any extra guidance?").
- **Mapping conversational answers back into param semantics**:
  - Define an internal mapping layer that translates free-form answers into:
    - Concrete param values (e.g. `max_candidates: 7`, `context_mode: 'strict-para'`).
    - Omitted params that should rely on Config / MCP defaults.
    - Optional `agent_reasoning` snippets when the user explicitly asks the AI to choose for them.
  - Preserve the **A/B/C semantic contract** in **payload assembly only**:
    - "User gave explicit value" → treat as A-path conceptually and record in `explicit_choices[param]`.
    - "User said 'use default' or skipped" → treat as B-path (omit key) and do not add to `explicit_choices`.
    - "User said 'you choose'" → treat as C-path; omit key but append a short reasoning snippet to `agent_reasoning_log` and `agent_reasoning`.
- **Scratchpad updates**:
  - Reuse `tmp-prompt.json` but adjust how `explicit_choices` and `asked` are populated:
    - `asked`: append the param name whenever we surface it conversationally, regardless of how the user answered.
    - `explicit_choices`: store only params where the user provided a non-default explicit value or where an ephemeral profile has concretely overridden defaults.
    - `final_payload_draft`: maintain a running JSON object with the current best `mode` and `params` view so the session can survive restarts if needed.
  - Preserve RESUME-ROADMAP resume-gate behavior that relies on `explicit_choices` to decide which params are "sacred locks"; document that conversational answers which override defaults still count as locks.

### 4. Integrate profile selection into ROADMAP and CODE modes

- **RESUME-ROADMAP**:
  - Treat the profile gate as acting on **roadmap profiles**:
    - If a profile is chosen, set `params.profile` accordingly and let auto-eat-queue's `RESUME-ROADMAP params` logic merge it via `prompt_defaults.roadmap` + profile + queueParams.
    - Expose the effective parameters (e.g. `token_cap`, `branch_factor`, `max_depth`) in the final summary, so the user sees what the profile actually does.
  - Ensure the existing `resume gate` question (lock previous explicit choices vs re-evaluate) still works:
    - If gate choice A (lock) is used, do not re-ask conversational questions for params already in `explicit_choices`.
    - Treat changing the profile during a later run as a new explicit choice that can override older profile locks.
- **CODE modes (INGEST/ORGANIZE/**etc.)**:
  - Introduce or reuse the `profile` param per branch (already present for INGEST and ORGANIZE in the param table):
    - Offer relevant CODE-side profiles (e.g. `default`, `project-priority`) when available.
    - When no explicit CODE profiles exist in Config, explain that only roadmap profiles are currently configured and that CODE runs will use their own defaults.
  - Keep auto-eat-queue’s generic param merge behavior unchanged: it will see `params.profile` and handle merging (or treat it as missing) exactly as it already does.

### 5. Preserve and adapt safety and final confirmation

- **Final confirmation unchanged for consumers**:
  - Continue to present a final summary that mirrors current Message 9:
    - Show `mode`, each non-default param, which profile is active, and any inferred defaults that matter.
  - Keep the same three-way final decision semantics:
    - "Append" → validate and write one line to `.technical/prompt-queue.jsonl` or `Task-Queue.md` per `[Queue-Sources.md]`.
    - "Cancel" → do not write; leave summary visible for copy-paste.
    - "AI double-check" → run a short self-audit over the assembled payload and either:
      - Suggest edits and wait, or
      - Confirm and then append.
- **Queue append invariants**:
  - Continue to use the existing `Read-then-append` and validation flow from the prompt-crafter rule:
    - Validate `mode` presence and membership in the known modes table.
    - Validate `params` is an object and values fit MCP/Config constraints (e.g. `rationale_style` allowed set, `max_candidates` range).
    - For RESUME-ROADMAP: perform stale-entry removal (drop previous RESUME-ROADMAPs) before appending.
- **Scratchpad and file failure shielding**:
  - If `tmp-prompt.json` cannot be read or parsed into the expected structure, fail early with a clear error message and do **not** attempt conversational recovery.
  - If `.technical/prompt-queue.jsonl` is missing or unwritable at append time, report the error (and optionally log to `Errors.md` via the existing protocol) and return the payload in text form for manual insertion instead of silently dropping it.
  - If `Second-Brain-Config` is unreadable, default to a **minimal, safe profile** mode that:
    - Asks the user for all params that would otherwise be derived from defaults.
    - Clearly states that Config-based defaults are unavailable for this run.

### 6. Update documentation and rules to reflect the new flow

- **User-Questions-and-Options-Reference**:
  - Add a subsection under §1 describing the **conversational collector** variant:
    - Clarify that the question-led A/B/C style is now an implementation detail; the core requirement is that all listed params are covered and that final payload semantics match the A/B/C table.
    - Document the profile-first gate as the new "Message 1" for both CODE and ROADMAP branches.
- **Prompt-Crafter-Param-Table**:
  - Confirm or adjust `question_order` values where the profile gate effectively moves `profile` to the front for ORGANIZE / RESUME-ROADMAP.
  - Note explicitly that profile selection can be satisfied via:
    - A concrete `params.profile` string, or
    - An ephemeral override that materializes as explicit param values without setting `profile`.
- **plan-mode-prompt-crafter.mdc**:
  - Update narrative to:
    - Allow conversational phrasing for questions while keeping the same ordering and no-skips invariant for param coverage.
    - Clarify that the "Questions source" requirement refers to param coverage and semantics, not necessarily verbatim A/B/C text.
    - Document scratchpad semantics in a way that supports conversational collection (explicit/default/AI-choice mapping) instead of literal A/B/C storage.
- **Second-Brain-Config docs**:
  - In `prompt_defaults` comments, note that profiles are consumed by the conversational crafter as presets and remain read-only; the "new profile" option is session-local unless and until a future explicit "save as profile" flow is added.

### 7. Add explicit anti-silent-failure checks

- **Profile mismatches**:
  - Before emitting a payload, run a final validation step that:
    - Compares any `params.profile` value against `prompt_defaults.profiles`.
    - If there is no match, adds a short warning to the summary (not to the queue payload) explaining that the profile will be ignored at runtime and defaults will be used.
- **Param normalization**:
  - Normalize and validate common scalar and enum params before write (e.g. clamp `max_candidates` into a safe range, normalize case for `context_mode`, ensure booleans are actual booleans).
  - On normalization failure (e.g. user answer cannot be coerced to a valid enum), surface that to the user and re-ask or revert to explicit default, instead of silently coercing.
- **Session integrity**:
  - Use `session_id` in the scratchpad to detect when a new crafting run starts while an old one is partially complete; in that case, either:
    - Offer to resume the previous session, or
    - Clear only the in-memory state, leaving the on-disk scratchpad unchanged until the user confirms.

### 8. Regression and integration checks (non-code, conceptual)

- **Existing flows still valid**:
  - Confirm that Commander macros that rely on the question-led crafter still work, since the payload contract (`mode`, `params`) and queue routing are unchanged.
  - Ensure RESUME-ROADMAP stale-removal and bootstrap logic in `auto-eat-queue` remain correct with the new profile-aware params.
- **Edge-case walkthroughs**:
  - Walk through example runs for:
    - CODE → INGEST with an existing profile and defaulted params.
    - CODE → ORGANIZE with a new ad-hoc profile.
    - ROADMAP MODE + RESUME-ROADMAP with a roadmap profile and profile mismatch.
    - RESUME-ROADMAP where Config or scratchpad is temporarily unavailable.
  - For each, confirm that:
    - The conversational experience matches your intent.
    - The resulting queue lines are valid under Queue-Sources and MCP expectations.

