---
name: conversational-prompt-crafter-v4
overview: Finalize a lock-first, conversational-on-rails Prompt Crafter design where locks always win over profiles, profile-derived params are tracked deterministically, mid-session restarts are safe, CODE vs ROADMAP profiles are clearly separated, and final summaries remain fully auditable, all while preserving existing queue and pipeline contracts.
todos:
  - id: v4-lock-invariants
    content: "Encode the lock-first invariants explicitly in the implementation notes and tests: never allow profiles or defaults to override explicit_choices, and always annotate manual overrides in summaries."
    status: completed
  - id: v4-profile-derived-map
    content: Design and document a deterministic profile_derived map (param → bool) that tracks which params are currently driven by profile defaults vs manual/lock, for use in the profile-change diff and unlock logic.
    status: completed
  - id: v4-resume-gate-flow
    content: Fully specify the RESUME-ROADMAP resume gate + profile gate interaction with options A–D, including how to compute and present the diff list and how each option mutates explicit_choices, profile_info, and the rail.
    status: completed
  - id: v4-session-safety
    content: Reinforce mid-session restart safety by ensuring the new-run-vs-resume choice is explicit and that scratchpad writes never blend old and new sessions until commit.
    status: completed
  - id: v4-profile-namespaces
    content: Clarify conceptual separation between roadmap and CODE profiles in Config and gating logic, and ensure CODE profile limitations are surfaced clearly in chat and docs.
    status: completed
  - id: v4-param-meta-lock-ux
    content: Refine conversational prompts using param_meta and lock state so that manual-text params, locked params, and AI-choice paths are all clearly explained and auditable.
    status: completed
  - id: v4-docs-and-macros
    content: Plan doc edits to reflect V4 behavior (lock-first, profile-aware, rails model) and clearly distinguish conversational crafter from Commander macro fast-paths.
    status: completed
  - id: v4-safeguard-checklist
    content: Create a checklist of runtime safeguards (profile mismatch warnings, queue append validation, scratchpad corruption handling) to guide later implementation and regression testing.
    status: completed
isProject: false
---

## Conversational-On-Rails Prompt Crafter – V4 (Lock-First, Profile-Aware)

### 1. Non-negotiable invariants (strengthened)

- **Lock precedence (hard invariant)**
  - When a param appears in `explicit_choices`, its value **must always win** over:
    - Any profile default (`prompt_defaults.profiles[profile]`).
    - Any Config default (`prompt_defaults.roadmap` or branch defaults).
    - Any AI-chosen value (C-path reasoning).
  - Profiles are presets **only**. They may pre-fill or suggest values for **unlocked** params, but they never overwrite or silently mutate locked values.
  - Final summary must explicitly mark any param where a locked/manual value overrides a profile default (e.g. "`branch_factor: 5 (manual override over profile default 4)`").
- **No blending of sessions (mid-session safety)**
  - A new crafting run **must never** merge state from a previous unfinished session implicitly.
  - Old scratchpad content (`tmp-prompt.json`) is treated as one of:
    - A resumable session (user explicitly chooses to resume), or
    - A historical artifact (user explicitly chooses to start fresh, in which case new state is kept in memory until commit).
  - The crafter **must not** overwrite or partially reuse old `explicit_choices` / `profile_info` / `rail` unless the user has picked "resume" at the restart prompt.

---

### 2. Deterministic rails and scratchpad model

- **Rails per branch (unchanged core)**
  - For each branch/mode, derive a fixed `rail` sequence from `Prompt-Crafter-Param-Table` and `User-Questions-and-Options-Reference §1`:
    - ROADMAP: kickoff → ROADMAP MODE vs RESUME-ROADMAP → (if RESUME) resume gate → profile gate → RESUME-ROADMAP params 2–18 → manual-text phase → final confirmation.
    - CODE (INGEST/ORGANIZE/DISTILL/EXPRESS/ARCHIVE/TASK): side → mode → profile gate (where applicable) → branch params (by `question_order`) → manual-text phase → final confirmation.
- **Scratchpad fields (explicitly tracked)**
  - `session_id`: unique id per run.
  - `mode`: e.g. `"CODE:INGEST"`, `"ROADMAP:RESUME-ROADMAP"`.
  - `rail`: ordered list of logical steps.
  - `rail_index`: index of next step to ask.
  - `asked`: array of param ids already surfaced in this session.
  - `explicit_choices`: param → concrete value (user-specified or previously locked).
  - `profile_info`:
    - `active_profile`: current profile name (or `null`).
    - `profile_derived`: map `param` → boolean (true if current value came from profile, false if from manual/lock/default).
  - `agent_reasoning_log`: list of `{ param, text }` for AI-choice paths.
  - `final_payload_draft`: in-progress `mode` + `params` object.

---

### 3. Mid-session restart semantics (re-hardened)

- **Detect unfinished session**
  - On "We are making a prompt" trigger:
    - Attempt to parse `tmp-prompt.json`.
    - If valid and `rail_index < rail.length` for the same branch/mode, treat as resumable.
- **User choice (explicit)**
  - Present three options:
    - Resume from `[rail[rail_index]]` (continue this exact session).
    - Start fresh for this branch/mode (ignore old state for this run).
    - Show a compact summary of locks and answered params, then decide.
- **Behavior**
  - **Resume**:
    - Reuse `session_id`, `explicit_choices`, `profile_info`, `rail`, and `rail_index`.
    - Continue rails from the next step.
  - **Start fresh**:
    - Create new in-memory state with new `session_id`, empty `explicit_choices`, `profile_info`, and `asked`.
    - Use old scratchpad only as read-only reference if needed (no writes) until the new run completes.
    - Only overwrite `tmp-prompt.json` once the new run has successfully finished (or been explicitly cancelled with a clear message).
  - **Scratchpad failure**:
    - If parse fails or required keys are missing, fail loud:
      - Explain that the scratchpad is corrupt and must be deleted or repaired manually.
      - Do not attempt to repair or reuse partial content.

---

### 4. Lock-first RESUME-ROADMAP + profile gate (with full A–D options)

- **Step 1 – Resume gate**
  - When RESUME-ROADMAP with prior locks is detected:
    - Show a grouped summary of locked params and their values (e.g. depth-related, breadth-related, token limits).
    - Offer:
      - A: Keep previous locks and attempt to resume with them.
      - B: Discard previous locks and start a completely fresh RESUME-ROADMAP session for this project.
  - A → proceed with existing `explicit_choices` and `profile_info`.
  - B → clear `explicit_choices` and `profile_info` for this run, then re-derive rails and start from profile gate.
- **Step 2 – Profile gate**
  - For RESUME-ROADMAP after gate A:
    - Show current `active_profile` (if any) and available roadmap profiles from Config.
    - Options:
      - Keep current profile.
      - Switch to another existing profile.
      - Use default (no profile).
      - Flag that a new profile may be saved at the end (no immediate behavioral change).
- **Step 3 – Profile change with locks**
  - If user keeps current profile:
    - No further action; keep `profile_info` and `explicit_choices` as-is.
  - If user picks a different profile or "default" while locks exist:
    - Compute **profile-vs-lock diff**:
      - Use `profile_derived` map and `prompt_defaults.roadmap` + new profile object to determine:
        - Which params are *profile-relevant* (present in defaults for roadmap).
        - For each such param, the new profile default vs current locked value (if locked).
    - Show an explicit diff list:
      - Only include params where new profile default ≠ locked value.
    - Offer four options (must be implemented exactly):
      - **A – Adopt profile and unlock all affected params**
        - For each param in the diff list:
          - Remove from `explicit_choices`.
          - Mark `profile_derived[param] = true`.
        - Insert these params back into the remaining rail to be re-asked in order.
      - **B – Adopt profile but keep current locked values (hybrid state)**
        - Keep `explicit_choices` for all diff-list params.
        - Set `profile_derived[param] = false` for diff-list params and record that they are manual overrides over profile default.
        - Continue rails without re-asking these params.
        - Final summary must label them explicitly: `param: value (manual override over profile default X)`.
      - **C – Keep old profile**
        - Cancel profile switch; leave `active_profile` and all locks unchanged.
      - **D – Manually adjust locked params**
        - Ask: "Which locked param(s) do you want to adjust?"; accept fuzzy labels and map to canonical param names.
        - For each selected param:
          - Ask for a new value; update `explicit_choices[param]` and `final_payload_draft.params[param]`.
          - Set `profile_derived[param] = false` (now clearly manual).
        - Adopt the new profile **only for non-locked, profile-relevant params** (those not in `explicit_choices`).
- **Downstream impact**
  - Auto-eat-queue and roadmap pipelines see only the final `params` object:
    - Locked values are already baked in.
    - `params.profile` acts purely as a label and hint for defaults; it never retroactively overrides locked values.

---

### 5. CODE vs ROADMAP profiles (separated and transparent)

- **Profiles storage split (conceptual)**
  - Treat roadmap and CODE profiles as separate conceptual buckets even if still stored under one `prompt_defaults` section:
    - `prompt_defaults.roadmap_profiles`: tuned for RESUME-ROADMAP / ROADMAP MODE.
    - `prompt_defaults.code_profiles`: future section for CODE side (INGEST/ORGANIZE/etc.).
  - In the current Config, note that only roadmap profiles are defined; CODE profiles are TBD.
- **Gate behavior per side**
  - **ROADMAP flows**:
    - When listing profiles, show roadmap-focused ones only.
    - Make it clear they affect RESUME-ROADMAP params like `token_cap`, `branch_factor`, `max_depth`, etc.
  - **CODE flows (INGEST/ORGANIZE/DISTILL/EXPRESS/ARCHIVE/TASK)**:
    - If no `code_profiles` exist yet:
      - Say explicitly in chat: "Profiles are currently tuned for roadmap; CODE runs will mostly rely on per-mode defaults until CODE-specific profiles are configured."
      - Either:
        - Do not offer profile selection at all for CODE until `code_profiles` exist, **or**
        - Offer them only as labels for future use, clearly stating they have limited/no effect today.
    - When CODE-side profiles are eventually added, use a separate gate that lists only `code_profiles`.

---

### 6. Conversational questions with param_meta + lock awareness

- **Param-meta usage**
  - For each param on the rail, use its descriptor from `User-Questions-and-Options-Reference`:
    - `description` → short explanation of what the param controls.
    - `defaultWhenC` → natural-language explanation of what the system will do if user says "you choose".
    - `accepts_manual_text` → ensures a dedicated manual-text turn to capture content after structural inclusion is resolved.
- **Lock-aware phrasing**
  - When a param is locked and not scheduled for re-ask via the profile diff flow:
    - Optionally show: "`param` is currently locked at `value`. Do you want to change it? (yes/no)".
    - "No" → keep lock and skip to next rail step.
    - "Yes" → treat like option D for that single param (ask for new value and update `explicit_choices`).
  - For params reinserted after option A (unlock affected):
    - Reference both previous locked value and new profile default for better context.

---

### 7. Mid- and end-of-run UX and auditability

- **CODE profile transparency in-chat**
  - Whenever the profile gate appears in a CODE flow, the agent must verbally reflect the roadmap-CODE limitation so users aren’t surprised by roadmap-only entries.
- **Final summary enhancements**
  - For every run, summary must:
    - Show `mode` and effective profile (if any).
    - Enumerate all params that differ from Config + profile defaults.
    - For each such param, specify why it’s set that way:
      - `default` (derived from Config or MCP default, not shown unless relevant).
      - `profile` (explicitly from active profile, not locked or manually changed).
      - `manual override` (locked value overriding profile default, with both numbers).
      - `AI choice` (omitted from params, but reasoning text placed in `agent_reasoning`).
- **Final confirmation**
  - Keep three main choices:
    - Append to queue.
    - Cancel / edit manually.
    - Ask the AI to double-check.
  - Optionally layer in an additional choice to "Save these settings as a new profile (YAML patch)" before or after append, using final locked params.

---

### 8. Commander macros vs conversational crafter

- **Separate but consistent paths**
  - Commander macros continue to:
    - Build queue entries directly with pinned params.
    - Bypass tmp-prompt, locks, and profile interplay entirely.
  - They must still satisfy:
    - Queue validation rules from `Queue-Sources`.
    - MCP param validation from `MCP-Tools`.
- **Docs clarifying the split**
  - In Prompt-Crafter docs and user flows, call out that:
    - Conversational crafter is the correct path when users care about locks, profiles, and per-run nuance.
    - Commander macros are intentionally minimal and do not consult or update RESUME-ROADMAP locks.

---

### 9. Safeguards and failure paths (no regressions)

- **Profile mismatch warnings**
  - If `params.profile` doesn’t match a configured profile key in the relevant namespace (roadmap or code), warn in the summary that this label will be ignored at runtime.
- **Queue write and param validation**
  - When assembling the final payload, always validate:
    - `mode` is known.
    - `params` keys and values satisfy constraints (enums, ranges) from Config and MCP-Tools.
  - On failure, do not append:
    - Show the invalid fields and suggest corrections.
    - Provide the near-final JSON for manual editing if desired.
  - If `.technical/prompt-queue.jsonl` can’t be written, never drop the payload silently; present it to the user and explain what went wrong.
- **Scratchpad corruption**
  - Maintain existing strict behavior (abort crafter, instruct user to repair/Delete the file), with clear messaging and no silent resets.

---

### 10. Integration sanity scenarios

- **Scenario A – RESUME-ROADMAP with prior locks, profile change, and manual tweaks**
  - Walk through the full A–D flow (keep locks, profile change, diff list, options A–D, manual param selection, re-asking unlocked params) and verify that:
    - Locked values always supercede profile defaults.
    - Manual edits from option D are reflected as new, locked values.
    - Final `params` match the user’s explicit choices and the lock-first invariant.
- **Scenario B – RESUME-ROADMAP start-fresh**
  - Confirm old scratchpad is never blended; new session uses fresh rails and only overwrites `tmp-prompt.json` on completion.
- **Scenario C – CODE INGEST with profile gate**
  - Exercise the profile gate in a CODE run and verify that:
    - The agent explicitly calls out roadmap-only profiles.
    - The resulting payload clearly shows that CODE behavior defaults are used.
- **Scenario D – New roadmap profile from final locked settings**
  - Verify that the emitted YAML patch for a new profile:
    - Includes only stable tuning params.
    - Reflects final locked values (after any profile interactions).
    - Can be safely pasted into Config without affecting unrelated systems.

