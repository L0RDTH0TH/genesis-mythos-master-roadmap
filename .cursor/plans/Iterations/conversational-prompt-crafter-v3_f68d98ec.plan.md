---
name: conversational-prompt-crafter-v3
overview: Refine the conversational-on-rails Prompt Crafter to give locks clear precedence over profiles, implement a granular resume/profile gate, and align all surrounding systems and docs while preserving existing queue and pipeline contracts.
todos:
  - id: v3-contract-audit
    content: Re-scan prompt-crafter rules, RESUME-ROADMAP handling, Config prompt_defaults, and auto-eat-queue to ensure the lock-first, profile-second semantics can be implemented without breaking queue or pipeline contracts.
    status: pending
  - id: v3-rails-and-scratchpad
    content: Refine the rails and scratchpad model to explicitly track rail_index, explicit_choices, profile_info (profile-derived vs manual), and session_id for both CODE and ROADMAP branches.
    status: pending
  - id: v3-resume-lock-gate
    content: Specify the exact RESUME-ROADMAP resume-gate flow, including the locked-param list, profile-change diff computation, and options A–D behavior so that locks always supercede profiles unless user explicitly changes them.
    status: pending
  - id: v3-profile-save-path
    content: Design the end-of-run profile save behavior that snapshots final locked params into a read-only YAML patch for prompt_defaults.profiles, ensuring only stable knobs are included.
    status: pending
  - id: v3-param-meta-and-lock-ux
    content: Plan conversational question patterns that incorporate param_meta (descriptions, defaultWhenC, accepts_manual_text) and are aware of lock vs default vs profile-derived states.
    status: pending
  - id: v3-commander-vs-crafter
    content: Document and justify the separation between conversational crafter and Commander macros, and decide if/when macros should be aligned with named profiles later.
    status: pending
  - id: v3-docs-alignment
    content: Enumerate and later update all affected docs (Questions Reference, Structure-Detailed, User-Flow files, Config comments, plan-mode rule) to describe lock-first, conversational-on-rails behavior and known limitations.
    status: pending
  - id: v3-safeguards
    content: Consolidate all safeguards (lock precedence, profile mismatch warnings, queue/scratchpad errors) into a clear checklist to follow during implementation and testing.
    status: pending
isProject: false
---

## Conversational-On-Rails Prompt Crafter – V3 (Locks First)

### 1. Confirm existing contracts and touchpoints

- **Read-only survey (no edits yet)** across the codebase to ground changes:
  - `[plan-mode-prompt-crafter.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/plan-mode-prompt-crafter.mdc)` for current question-led invariants, scratchpad schema, and fail conditions.
  - `[User-Questions-and-Options-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)` §1 for param order, param descriptors, and final confirmation semantics.
  - `[Prompt-Crafter-Param-Table.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)` for per-branch param ownership and `accepts_manual_text` flags.
  - `[Second-Brain-Config.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Second-Brain-Config.md)` for `crafting.tmp_prompt_path`, `prompt_defaults.roadmap`, and `prompt_defaults.profiles`.
  - `[Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Second-Brain-Config.md)` and `[auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc)` for RESUME-ROADMAP param handling, profile merge semantics, and queue routing.
  - Roadmap skills/rules (e.g. `roadmap-deepen`, `roadmap-resume`, `auto-roadmap`) to verify they only consume `params` and do not depend on the old A/B/C UI.
- **Goal**: Ensure the V3 flow can change crafter behavior without breaking:
  - RESUME-ROADMAP normalization and stale-resume removal.
  - Guidance-aware runs (`prompt` vs `agent_reasoning`).
  - Commander macros that bypass the crafter.

---

### 2. Rails and session model (unchanged core, clarified)

- **Rails per branch**:
  - Maintain a deterministic `rail` sequence for each branch/mode:
    - ROADMAP: kickoff → ROADMAP MODE vs RESUME-ROADMAP → resume gate → profile rail → RESUME-ROADMAP param rail (2–18) → manual-text phase → final confirmation.
    - CODE (INGEST/ORGANIZE/DISTILL/EXPRESS/ARCHIVE/TASK): side choice → mode choice → profile rail (where defined) → branch param rail → manual-text phase → final confirmation.
- **Scratchpad fields** in `tmp-prompt.json` (conceptual; implementation later):
  - `session_id`, `mode`, `rail` (array of steps), `rail_index` (current position).
  - `asked`: list of params already surfaced.
  - `explicit_choices`: param → concrete value (user-set or locked).
  - `profile_info`: current profile name (if any) + which params were profile-derived vs manual.
  - `agent_reasoning_log`, `final_payload_draft` as in V2.
- **On-rails guarantee**:
  - Each turn either resolves a gate, advances to the next rail param, or collects manual text for a param that already had its structural inclusion decided.
  - No param in the branch’s `Param order by branch` is skipped; defaults/profile can satisfy them but they are always considered and logged.

---

### 3. Mid-session restart handling (refined from V2)

- **Detect unfinished sessions**:
  - On prompt-crafter kickoff, attempt to read `tmp-prompt.json`.
  - If structurally valid and `rail_index` < `rail.length`, treat as an unfinished session.
- **User-facing choices**:
  - Offer three simple options in conversational form:
    - Resume from where we left off (`rail[rail_index]`).
    - Start over for this branch/mode (fresh session, keeping old scratchpad only as a backup on disk).
    - Show a short summary of current locks and answered params, then choose.
- **Behavior**:
  - Resume: keep `session_id`, `explicit_choices`, `profile_info`, and continue from next rail step.
  - Start over: create a new in-memory session with new `session_id`, empty `asked`/`explicit_choices`/`profile_info`; only overwrite the scratchpad after this run completes, so old state is never silently blended.
- **Failure path**:
  - If `tmp-prompt.json` fails to parse or is missing required keys, follow existing hard-fail rule but clarify in docs that the user can delete/repair the file; do not attempt automatic repair.

---

### 4. RESUME-ROADMAP resume gate with lock-supercedes-profile (V3 core)

- **Lock semantics**:
  - Locks are authoritative: when a param is in `explicit_choices`, its value is treated as the source of truth unless the user explicitly changes it.
  - Profiles are **presets only**; they may propose values, but they never override locks without explicit user action.
- **Flow when RESUME-ROADMAP has prior locks**:
  1. **Resume gate**:
    - Present prior locked params as a concise list (e.g., grouped by type: depth, breadth, tokens) with current values.
    - Offer:
      - A: Keep previous locks and continue.
      - B: Discard previous locks and start a fresh session for this project (clears `explicit_choices` and `profile_info` for this run).
  2. **Profile rail (with locks visible)**:
    - Show previous profile (if any) and available profiles from Config.
    - Options:
      - Keep old profile.
      - Switch to another existing profile.
      - Use default (no profile).
      - Defer creation of a new profile to the end.
  3. **If user keeps old profile**:
    - Locks remain untouched; profile continues to provide defaults only for params that are not locked and not explicitly set this run.
  4. **If user chooses a different profile or default with existing locks**:
    - Compute the **diff** between new profile defaults and current locked values for profile-relevant params.
    - Present a compact diff list:
      - For each affected param: new default vs locked value.
    - Offer four actions (your refined flow):
      - **A – Adopt profile and unlock all affected params**:
        - Remove affected params from `explicit_choices` and from lock set.
        - Mark them as pending on the rail; re-ask them in order later.
      - **B – Adopt profile but keep current locked values**:
        - Keep `explicit_choices` as-is for those params and record that they are **manual overrides over profile defaults**.
        - Ensure final summary explicitly flags these as “manual override > profile”.
      - **C – Keep old profile**:
        - Abort the profile change; leave `profile_info` and `explicit_choices` unchanged.
      - **D – Manually adjust locked params**:
        - Ask the user which locked param(s) to change; support fuzzy references (e.g. “token limit”, “depth cap”) and map back to canonical param names.
        - For each selected param:
          - Ask for a new value; update `explicit_choices[param]` and `final_payload_draft.params[param]`.
        - Adopt the new profile for non-locked params, treat the manually adjusted ones as overrides.
- **Downstream safety**:
  - From auto-eat-queue and pipeline perspective, nothing changes:
    - They receive a final `params` object reflecting locked and manually overridden values.
    - `params.profile` remains purely advisory for defaults; its effects are already baked into the final concrete values or omitted.

---

### 5. Profile creation and namespaces (with lock precedence)

- **New profiles are user-made snapshots of concrete params**:
  - During profiling rail, "create new profile" only sets intention and maybe a name; it does **not** change behavior mid-run.
  - At final confirmation, if user chooses to save a new profile:
    - Build the profile’s value map from `final_payload_draft.params`, **after** lock/profile resolution:
      - Include only stable knobs (e.g. `token_cap`, `branch_factor`, `max_depth`, `context_mode`, `max_candidates`, `rationale_style`, roadmap toggles).
      - Exclude run-specific items like `source_file`, `user_guidance`, `userText`, `queue_next`, `sectionOrTaskLocator`.
    - Emit a YAML patch block for `prompt_defaults.profiles` that the user can paste into Config; do not write to Config automatically.
- **Locks → profile precedence**:
  - When generating the YAML snippet, ensure that values come from **post-lock** state:
    - Manual adjustments made in step D (lock editing) take precedence over what any profile would have suggested.
    - The saved profile therefore encodes the user’s final, locked preferences rather than any momentary default.
- **Roadmap vs CODE profiles**:
  - Keep roadmap-focused profiles as-is; document that CODE-side presets are a future extension.
  - In conversational profile lists:
    - Clearly mark roadmap-tuned profiles.
    - For CODE modes, explain that selecting these has limited or no effect today, and that concrete CODE profiles will be added later.

---

### 6. Conversational question generation with param_meta and locks

- **Question shaping from meta**:
  - Use `accepts_manual_text` to separate “select/include” decisions from “provide content” decisions:
    - First: determine **whether/how** the param is set (default, locked, profile-driven, or explicit value).
    - Later: for included manual-text params, ask open, natural-language questions (e.g. source_file path, user_guidance) on their own rail turns.
  - Use `description` and `defaultWhenC` from param descriptors to:
    - Explain what the param controls.
    - Offer “you choose” / "stick with default" conversational paths mapped to C/B semantics, respectively.
- **Lock-aware prompts**:
  - When a param is already locked (`explicit_choices`), and the user has not opted to change it via the profile diff flow, treat it as read-only for this session:
    - Either skip re-asking and merely show it in the summary, or
    - Offer a quick "do you want to change this locked value?" micro-prompt before moving on.
  - For params re-inserted on the rail after choosing profile option A (unlock affected), ask fresh questions using updated defaults, while still referencing the prior value for context (“Previously set to 80000; profile suggests 60000”).

---

### 7. Commander macros and dual paths

- **Keep macros separate and fast**:
  - Commander macros continue to construct queue entries directly with pinned params, bypassing the conversational crafter and locks/profile interplay.
  - Ensure their payloads still pass the same validation rules as crafter output.
- **Surface distinction in docs**:
  - In Prompt-Crafter and user-flow docs, explicitly call out:
    - Conversational-on-rails crafter: honors locks and profile interplay, best for nuanced runs.
    - Commander macros: quick, opinionated presets for common operations; do not consult or update tmp-prompt locks.

---

### 8. Documentation updates and known limitations

- **Core docs to update** (read-only planning now; edits later):
  - `User-Questions-and-Options-Reference` §1:
    - Reframe A/B/C as **payload semantics** rather than literal UI choices.
    - Describe the RESUME-ROADMAP lock-first resume gate and profile-change diff flow.
  - `Prompt-Crafter-Structure-Detailed`:
    - Document rails, scratchpad fields, lock precedence, and mid-session restart behavior.
  - `User-Flow-Prompt-Crafter-`*:
    - Rewrite the step-by-step user paths to show the new RESUME-ROADMAP gate (with lock list and profile diff), conversational rails, and end-of-run profile save option.
  - `Second-Brain-Config` under `prompt_defaults`:
    - Add notes about roadmap-only profiles and future CODE profiles.
  - `plan-mode-prompt-crafter.mdc`:
    - Relax strict “exact question text” constraints so they apply to **param coverage and ordering**, not literal strings, while preserving no-skip guarantees.
- **Explicitly note known limitations**:
  - CODE and ROADMAP currently share a profile namespace tuned primarily for ROADMAP.
  - Commander macros do not participate in lock/profile interplay or use tmp-prompt sessions.

---

### 9. Safeguards recap (no silent surprises)

- **Lock precedence enforced**:
  - Never let profiles overwrite `explicit_choices` without explicit user confirmation through options A–D.
  - Final summary must clearly distinguish:
    - Profile-default params.
    - Manual overrides (locked values overriding profile).
- **Profile mismatch warnings**:
  - If `params.profile` does not match a key in `prompt_defaults.profiles`, warn in the summary that the run will use defaults instead and that the profile label is for logging only.
- **Queue and scratchpad failure paths**:
  - On invalid `params` values, reject append and show fields needing correction rather than coercing.
  - On queue file write failure, present the JSON payload to the user for manual insertion; do not drop it.
  - On scratchpad corruption, fail loud with a pointer to the file and instructions to remove/repair; start fresh only after the user’s explicit action.

---

### 10. Scenario walkthroughs to validate lock-first behavior

- **Scenario 1: RESUME-ROADMAP with lock + profile change**
  - Walk through the exact interaction you sketched (lock list, profile diff, options A–D, manual adjustments) and confirm resulting `params` reflect:
    - Locks superceding profile defaults.
    - Manual changes re-locking with new values.
    - Correct params passed into auto-eat-queue and auto-roadmap.
- **Scenario 2: RESUME-ROADMAP, gate B (start over)**
  - Confirm that scratchpad state is not blended; new session ignores old locks, but old scratchpad is preserved until the new run completes.
- **Scenario 3: New profile saved after manual adjustments**
  - Verify profile YAML matches final locked params and is entirely deterministic.
- **Scenario 4: CODE flows (INGEST/ORGANIZE) with no meaningful profiles**
  - Verify that conversational rails still work and that docs clearly warn about ROADMAP-only profile presets.

