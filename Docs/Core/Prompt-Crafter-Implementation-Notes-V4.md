---
title: Prompt-Crafter Implementation Notes (V4 — Lock-First, Conversational-On-Rails)
created: 2026-03-12
tags: [pkm, second-brain, prompt-crafter, implementation, v4]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[Prompt-Crafter-Structure-Detailed]]", "[[User-Questions-and-Options-Reference]]", "[[Queue-Sources]]"]
---

# Prompt-Crafter Implementation Notes (V4)

Implementation contract for the **conversational-on-rails** Prompt Crafter with **lock-first, profile-aware** semantics. Use this note when implementing or testing the crafter rule, scratchpad, and queue append logic.

---

## 1. Lock-first invariants (non-negotiable)

These invariants **must** be enforced in code and in agent behavior. Violating them is a regression.

- **Lock precedence (hard invariant)**
  - When a param appears in `explicit_choices`, its value **must always win** over:
    - Any profile default (`prompt_defaults.profiles[profile]` or roadmap/code profile sections).
    - Any Config default (`prompt_defaults.roadmap` or branch defaults).
    - Any AI-chosen value (C-path reasoning).
  - Profiles are **presets only**. They may pre-fill or suggest values for **unlocked** params only. They **never** overwrite or silently mutate locked values.
  - **Never** allow profile defaults to leak into params that are present in `explicit_choices`. During payload assembly, for every key in `explicit_choices`, the final `params` object must use that value; do not substitute from profile or Config.

- **Final summary annotations**
  - The final summary **must** explicitly mark any param where a locked/manual value overrides a profile default.
  - Use a consistent label, e.g. `param: value (manual override over profile default X)` or `param: value (locked; profile default was X)`.
  - This ensures auditability: users and maintainers can see why a value differs from the active profile.

- **Testing / validation**
  - When adding tests or fixtures: assert that for any payload built from a session with `explicit_choices` populated, the emitted `params` contain exactly those values for the corresponding keys; no key in `explicit_choices` may be overwritten by profile or Config in the final payload.

---

## 2. Profile-derived map (deterministic)

The scratchpad **must** maintain a deterministic map that tracks which params are currently driven by profile defaults vs manual/lock. This prevents hallucination when computing the profile-vs-lock diff during profile change.

- **Schema**
  - Under `profile_info` (see § Scratchpad schema in Prompt-Crafter-Structure-Detailed):
    - `profile_derived`: object mapping **param name** (string) → **boolean**.
      - `true` = current value for this param came from the active profile (or Config default when no profile). Safe to unlock and re-ask when user changes profile.
      - `false` = current value came from user explicit choice (A-path) or a prior lock; treat as manual override.
  - When the user sets a param via an explicit choice (A or manual text), set `profile_derived[param] = false`.
  - When a param is filled from profile or Config default (user chose B or C, or param was never asked and default was applied), set `profile_derived[param] = true`.
  - When loading from scratchpad after resume gate "lock previous", preserve `profile_derived` from the previous session; do not reset it unless the user chooses "start fresh".

- **Use in profile-change diff**
  - When the user switches profile (or selects "default") and locks exist:
    - **Profile-relevant params**: those that appear in `prompt_defaults.roadmap` or in the new profile object (e.g. token_cap, branch_factor, max_depth, inject_extra_state).
    - **Diff list**: include only params where (1) the param is profile-relevant, and (2) the **new** profile default ≠ current value in `explicit_choices` (or current effective value). Use `profile_derived` to know which params are locked vs profile-sourced; for locked params, "current value" is `explicit_choices[param]`.
  - Do **not** infer "profile-derived" from context; always use the stored `profile_derived` map. If a param is missing from `profile_derived`, treat it as manual (`false`) for safety.

---

## 3. RESUME-ROADMAP resume gate and profile gate (options A–D)

- **Step 1 – Resume gate**
  - When RESUME-ROADMAP is selected and scratchpad contains a prior RESUME session with non-empty `explicit_choices`:
    - Show a grouped summary of locked params and their values (e.g. depth-related, breadth-related, token limits).
    - Offer:
      - **A:** Keep previous locks and resume with them.
      - **B:** Discard previous locks and start a completely fresh RESUME-ROADMAP session for this project.
  - If A: proceed with existing `explicit_choices` and `profile_info`; go to profile gate.
  - If B: clear `explicit_choices` and `profile_info` for this run; re-derive rails and start from profile gate (no lock list).

- **Step 2 – Profile gate**
  - Show current `active_profile` (if any) and available roadmap profiles from Config.
  - Options: Keep current profile | Switch to another existing profile | Use default (no profile) | Defer new profile creation to end of run.

- **Step 3 – Profile change with locks (when user switches profile or selects default and locks exist)**
  - Compute **profile-vs-lock diff** using `profile_derived` and the new profile/Config defaults (see §2). Show only params where new default ≠ current locked/effective value.
  - Offer four options **exactly**:
    - **A – Adopt profile and unlock all affected params**
      - For each param in the diff list: remove from `explicit_choices`, set `profile_derived[param] = true`, and re-insert into the remaining rail to be re-asked in order.
    - **B – Adopt profile but keep current locked values (hybrid state)**
      - Keep `explicit_choices` for all diff-list params. Set `profile_derived[param] = false` for those params (manual override over profile default). Continue rails without re-asking. Final summary **must** label them: `param: value (manual override over profile default X)`.
    - **C – Keep old profile**
      - Cancel profile switch; leave `active_profile` and all locks unchanged.
    - **D – Manually adjust locked params**
      - Ask which locked param(s) to adjust; accept fuzzy labels (e.g. "token limit", "depth") and map to canonical param names. For each selected param, ask for new value; update `explicit_choices[param]` and `final_payload_draft.params[param]`; set `profile_derived[param] = false`. Then adopt the new profile only for non-locked, profile-relevant params.

- **Downstream**
  - Auto-eat-queue and roadmap pipelines receive the final `params` object only. Locked values are already baked in; `params.profile` is a label and never retroactively overrides locked values.

---

## 4. Mid-session restart safety (no blending)

- **Detect unfinished session**
  - On "We are making a prompt" trigger, read scratchpad. If valid and `rail_index < rail.length` for the same branch/mode, treat as resumable.

- **User choice**
  - Present explicitly: (1) Resume from next rail step, (2) Start fresh for this branch/mode, (3) Show summary of locks and answered params then decide.

- **Behavior**
  - **Resume:** Reuse `session_id`, `explicit_choices`, `profile_info`, `rail`, `rail_index`. Continue from next step.
  - **Start fresh:**
    - Create **new** in-memory state: new `session_id`, empty `explicit_choices`, `profile_info`, `asked`. Do **not** merge or reuse old state.
    - Use old scratchpad only as **read-only** reference until the new run completes.
    - **Do not overwrite** `tmp-prompt.json` until the new run has **successfully finished** (or user explicitly cancels with a clear message). This avoids accidental blending of old and new sessions.
  - **Scratchpad corrupt:** If parse fails or required keys missing, abort with a clear error; instruct user to delete or repair the file manually. Do not attempt to repair or reuse partial content.

---

## 5. Runtime safeguards checklist

Use this checklist during implementation and regression testing.

- [ ] **Lock precedence:** Before writing final `params`, for every key in `explicit_choices`, assert `params[key] === explicit_choices[key]` (or equivalent); no profile/Config overwrite.
- [ ] **Final summary:** For every param that is in `explicit_choices` and whose value differs from the active profile default, include the "(manual override over profile default X)" annotation.
- [ ] **Profile mismatch:** If `params.profile` is set and does not match a key in the relevant namespace (roadmap or code profiles), add a warning in the summary that the label will be ignored at runtime.
- [ ] **Queue validation:** Before append, validate `mode` is known and `params` keys/values satisfy Config and MCP-Tools (enums, ranges). On failure, do not append; show invalid fields and offer payload for manual edit.
- [ ] **Queue write failure:** If `.technical/prompt-queue.jsonl` (or Task-Queue.md) cannot be written, present the payload to the user and explain the error; never drop it silently.
- [ ] **Scratchpad corruption:** On parse failure or missing required keys, abort crafter and report clearly; do not repair or overwrite the file automatically.
- [ ] **Mid-session start fresh:** When user chooses "start fresh", never write to scratchpad until the new run completes or is explicitly cancelled; do not blend old and new state.

---

## Cross-references

- Scratchpad schema and rails: [[Prompt-Crafter-Structure-Detailed]] § Scratchpad and rails.
- Param order and A/B/C semantics: [[User-Questions-and-Options-Reference]] §1.
- Queue contract and routing: [[Queue-Sources]].
- Rule file: `.cursor/rules/context/plan-mode-prompt-crafter.mdc`.
