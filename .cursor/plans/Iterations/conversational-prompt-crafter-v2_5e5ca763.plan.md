---
name: conversational-prompt-crafter-v2
overview: Design a conversational-but-on-rails Prompt Crafter that resolves known weak spots around RESUME-ROADMAP locking, mid-session restarts, profile creation, CODE vs ROADMAP profiles, documentation drift, and param_meta-aware questioning while preserving existing queue and pipeline contracts.
todos:
  - id: v2-rails-design
    content: Define the exact rails structure per branch (CODE and ROADMAP), including where profile gate, resume gate, param rails, manual-text phase, and final confirmation sit in the sequence.
    status: pending
  - id: v2-resume-gate-profile
    content: Specify precise semantics for RESUME-ROADMAP resume gate vs profile changes, including which params are treated as sacred locks and how profile-derived params are selectively unlocked and re-asked.
    status: pending
  - id: v2-session-lifecycle
    content: Design session lifecycle behavior for tmp-prompt.json, including mid-session restart detection, resume prompts, and safe handling of corrupted scratchpad state.
    status: pending
  - id: v2-profile-creation
    content: Define how user-created profiles are captured from final_payload_draft, which params are included, and how YAML patches are output for Second-Brain-Config without direct writes.
    status: pending
  - id: v2-param-meta-ux
    content: Plan how param_meta and accepts_manual_text will influence conversational question wording and manual-text phases while keeping the flow linear and deterministic.
    status: pending
  - id: v2-commander-split
    content: Document and justify the separation between conversational crafting and Commander macro shortcuts, and ensure both paths validate against the same queue and MCP contracts.
    status: pending
  - id: v2-docs-sweep
    content: List and update all affected documentation files (User-Questions-and-Options-Reference, Prompt-Crafter-Structure-Detailed, User-Flow-Prompt-Crafter-*, README, Config comments, plan-mode rule) to describe the conversational-on-rails behavior and known limitations.
    status: pending
  - id: v2-safeguards
    content: Enumerate and formalize all added safeguards (profile mismatch warnings, queue write errors, scratchpad failures) so they surface loudly to the user instead of silently degrading behavior.
    status: pending
isProject: false
---

## Conversational-On-Rails Prompt Crafter – V2

### High-level intent

- **Experience**: Conversational, natural-language Q&A that still runs on a **strict, linear rail** derived from `Prompt-Crafter-Param-Table` and the chosen branch (CODE vs ROADMAP).
- **Invariants**: Preserve the existing queue contract (`mode`, `params`, optional `agent_reasoning`, `param_meta`), safety rules (validation, read-then-append, RESUME-ROADMAP stale removal), and scratchpad structure.
- **Corrections**: Explicitly address the seven weak areas Grok surfaced, using your clarified constraints:
  - Profile-first, but **on rails**.
  - **User-created** profiles only; no AI-designed presets.
  - Scratchpad and resume-gate semantics tightened; no silent conflicts.
  - Documentation brought in line with reality.

---

### 1. Rails model and session lifecycle

- **Single source of rails**:
  - For each branch/mode, derive the ordered param list from `[Prompt-Crafter-Param-Table.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)` and `User-Questions-and-Options-Reference §1 (Param order by branch)`.
  - Represent this as an internal `rail` array of param ids (plus special gates like kickoff, mode select, resume gate, final confirmation).
- **On-rails progression**:
  - Each conversational turn either:
    - Advances to the next param on the rail,
    - Handles the manual-text phase for a param that `accepts_manual_text: true`,
    - Or resolves a gate (kickoff, resume, final confirmation).
  - No free-form jumps: the agent must not skip or reorder params unless a profile/default already fully satisfies them, and that decision is logged in scratchpad.
- **Session lifecycle in `tmp-prompt.json`**:
  - Extend the scratchpad schema (conceptually; implementation later) to track:
    - `session_id`: opaque id per crafting run.
    - `mode`: e.g. `"CODE:INGEST"`, `"ROADMAP:RESUME-ROADMAP"`.
    - `rail`: ordered list of param names (for this session) and current index.
    - `asked`: params that have already been surfaced.
    - `explicit_choices`: map of param → concrete value chosen (or locked from prior run).
    - `agent_reasoning_log`: current behavior (C-path snippets).
    - `final_payload_draft`: in-progress `mode` + `params` view.
  - On every answered param, increment rail index, update `asked`, `explicit_choices` (for explicit overrides), and `final_payload_draft`.

---

### 2. Mid-session restart and resume behavior (Weak area #2)

- **Detect existing session**:
  - On "We are making a prompt" trigger, first read `tmp-prompt.json`.
  - If parse fails or required keys missing → fail loud per existing rule (no guessing), offer only a **fresh start recommendation** in chat (no queue writes) and ask user to repair/delete file manually.
  - If a valid, unfinished session is present (rail exists, current index < rail length):
    - Present a short, conversational choice:
      - Resume at `[next param label]`.
      - Start fresh (discard this session’s answers).
      - Inspect summary of what was already set, then decide.
- **Resume path**:
  - If user chooses resume:
    - Keep `session_id`, `explicit_choices`, and `asked`.
    - Reconstruct rail position from scratchpad and continue from the next un-asked param.
  - If user chooses start fresh:
    - Option 1 (safer, matches your suggestion):
      - Leave the old scratchpad as-is on disk, but start a new in-memory session with a new `session_id` and clean `explicit_choices` / `asked`.
      - Only overwrite scratchpad once the new run is complete or explicitly committed.
    - Document this behavior in Prompt-Crafter-Structure-Detailed so it’s clear that mid-session restarts do not silently blend sessions.

---

### 3. RESUME-ROADMAP resume gate vs profile interaction (Weak area #1)

- **Gate semantics tightened, with your lock-linking idea**:
  - When user triggers RESUME-ROADMAP:
    - Load scratchpad; if previous RESUME session exists with `explicit_choices`, surface **resume gate**:
      - A: "Lock previous explicit choices" → treat `explicit_choices` as sacred.
      - B: "Start over" → discard previous choices for this run (do not use them as sacred locks).
    - Only after gate answer do we run the profile rail.
- **Profile as a special (semi-sacred) param**:
  - On gate A (lock):
    - Treat most params in `explicit_choices` as fully locked; do not re-ask them.
    - Still **ask profile first** as the entry rail step, but with a guard:
      - If user picks **same profile** as previously stored → no conflict; continue.
      - If user picks **different profile**:
        - Show a clear warning:
          - "Changing profile will override some of your previous locked settings (e.g. token_cap, branch_factor). Do you want to re-run those rails or keep the old profile?"
        - Offer two options:
          - Keep locked profile → revert to earlier profile and continue rails without change.
          - Adopt new profile → mark affected params as **unlocked for this run**, clear them from `explicit_choices`, and place them back into the remaining rail so they will be re-asked.
  - On gate B (start over):
    - Ignore previous `explicit_choices` when deriving sacred locks (for this session).
    - Start with the profile gate, then walk the full rail, treating this as a brand-new run.
- **Implementation guardrails**:
  - Maintain a small map of which params are profile-derived vs manually set.
  - When user changes profile after choosing lock A, only clear `explicit_choices` entries that were previously profile-derived; keep true manual overrides locked unless explicitly changed.

---

### 4. Profile creation and namespaces (Weak areas #3 and #4)

- **User-created profiles only (no AI-derived presets)**:
  - During the run:
    - "Use existing profile" → pick from `prompt_defaults.profiles`.
    - "Use default" → no profile set; rely on `prompt_defaults.roadmap` or per-branch defaults.
    - "Create new profile" → treat as a **flag only** during the run (e.g. `pending_new_profile_name` and `pending_new_profile_scope` in scratchpad); do **not** try to infer param values from adjectives.
  - At final confirmation:
    - Extend the decision set (conceptually) to include:
      - Append as-is (no new profile).
      - Append and **emit a YAML patch** for a new profile under `prompt_defaults.profiles` (user-controlled save).
    - The new profile’s value map is derived deterministically from `final_payload_draft.params`:
      - Include only keys that are meaningful defaults (e.g. `token_cap`, `branch_factor`, `max_depth`, `context_mode`, `max_candidates`, `rationale_style`).
      - Exclude transient/session-specific fields (`source_file`, `user_guidance`, `queue_next`, etc.).
- **No direct writes to Config (for now)**:
  - To stay within safety guardrails, have the crafter **output a ready-to-paste YAML block** for `Second-Brain-Config.md` instead of editing it automatically.
  - Example (ROADMAP profile):

```yaml
    # Add under prompt_defaults.profiles:
    - my-profile-name: { token_cap: 50000, branch_factor: 4, max_depth: 4 }
    

```

- The plan keeps open a future path where an Obsidian MCP tool could safely apply these patches.
- **Roadmap vs CODE profile namespacing**:
  - Keep a single `prompt_defaults.profiles` table, but:
    - Add a **known limitation note** (as you suggested) in both `Second-Brain-Config.md` and `plan-mode-prompt-crafter.mdc`:
      - At present, profiles are tuned for ROADMAP; CODE-side presets are TBD.
    - Tag each profile with a `scope` field in comments or naming convention (e.g. `deepen-aggressive (roadmap)`), so it’s obvious when a profile is roadmap-only.
  - For CODE modes:
    - When listing profiles during profile gate, explicitly say that current profiles are roadmap-focused and that CODE runs will mostly rely on per-branch defaults unless/ until CODE-specific profiles are added.
    - Accept CODE profile selection for future compatibility, but treat unknown or roadmap-only profiles as **no-op** for CODE runs, with a visible note in summary.

---

### 5. Conversational question generation with param_meta awareness (Weak area #7)

- **Param-meta-driven question shaping**:
  - When building questions for each param on the rail, consult:
    - `accepts_manual_text` (from Param Table) → this param must have a dedicated manual-text turn later; do not try to fully capture it via quick choices.
    - `defaultWhenC` and `description` (from `User-Questions-and-Options-Reference` param descriptors) → use them to:
      - Phrase the question (“This controls …; default when omitted is …”).
      - Offer a natural-language "you choose" path (mapped to C semantics internally).
  - Examples:
    - `source_file` (accepts_manual_text: true):
      - Conversational question: "Which note or path should this run target? You can paste a full path, or say 'current note' to use what’s open." → never try to compress into A/B/C.
    - `max_candidates`:
      - "How many path options do you want per note? Recommended 3–10, current default 7. You can say a number, 'default', or 'you decide'."
- **Internal mapping to A/B/C semantics** (payload-only):
  - For each answer:
    - Explicit value (user types a path, number, or enum) → treat as conceptual A-path; store in `explicit_choices[param]` and `final_payload_draft.params[param]`.
    - "Default" / "skip" / blank → treat as B-path; omit from `params`, keep out of `explicit_choices`.
    - "You choose" / "AI decide" → treat as C-path; omit from `params` but add an `agent_reasoning_log` entry using `defaultWhenC` as a starting point.
  - Manual-text params get an additional turn where the raw text is stored directly under `params[param]`.

---

### 6. Commander macros and dual-path behavior (Weak area #5)

- **Keep Commander macros as a separate, fast path (for now)**:
  - Commander one-click macros (e.g. "Craft Ingest Default") continue to:
    - Construct payloads directly based on their own pinned params.
    - Append to the queue **without** running the conversational crafter.
  - Document this explicitly:
    - In `User-Flow-Prompt-Crafter-`* and `Chat-Prompts`, distinguish between:
      - **Interactive conversational crafting** (question-led, on rails).
      - **Macro-based fast crafting** (pinned profiles/params, minimal interaction).
  - Ensure both paths still validate against the same `Queue-Sources` and MCP constraints.
- **Future alignment hook**:
  - When conversational profiles stabilize, consider gradually updating Commander macros so their pinned params match known profiles exactly (e.g. macro "Craft Deepen Aggressive" simply picks the `deepen-aggressive` profile).

---

### 7. Documentation overhaul (Weak area #6)

- **Broaden docs beyond the two original files**:
  - Update at least these:
    - `[User-Questions-and-Options-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)` §1:
      - Clarify that the A/B/C table now describes **payload semantics**, not literal UI.
      - Add a subsection for "conversational-on-rails" behavior and how it maps to A/B/C internally.
    - `Prompt-Crafter-Structure-Detailed.md`:
      - Describe the new rails model, scratchpad fields, and session lifecycle (including mid-session restart behavior).
      - Document the resume gate + profile interaction rules.
    - `User-Flow-Prompt-Crafter-`* files:
      - Replace rigid Message 1–9 A/B/C step text with the new conversational sequence: profile gate, branch/mode choose, param rails, manual text phase, final confirmation.
    - `3-Resources/Second-Brain/README` (or trigger cheat sheet):
      - Add an entry for conversational crafting and explain the difference from Commander macros.
    - `Second-Brain-Config.md` under `prompt_defaults`:
      - Insert the **known limitation** note about roadmap-only profiles and CODE-side future work.
    - `plan-mode-prompt-crafter.mdc`:
      - Relax wording that currently implies questions *must* be literal A/B/C text, while preserving the "no param skipping" invariant.
      - Add notes about the conversational-on-rails implementation and how it still honors §1 param order.

---

### 8. Additional safeguards against silent failures

- **Profile mismatch warnings**:
  - Before final summary:
    - For any `params.profile`, check against `prompt_defaults.profiles`.
    - If no match, add a **visible warning in the summary only** (not in the payload):
      - "Profile 'X' is not configured; run will use defaults instead."
- **Queue write and validation**:
  - Reuse existing validation logic:
    - If `mode` is unknown or `params` fails MCP/Config validation, refuse to append and present the invalid field(s) for correction.
  - If `.technical/prompt-queue.jsonl` cannot be written:
    - Show clear error and output the final JSON payload as text for manual paste; do not silently drop work.
- **Scratchpad corruption**:
  - Keep the current hard-fail behavior when `tmp-prompt.json` is malformed, but:
    - Include a short suggestion in the user-facing error (e.g. path to the file and that they can delete/repair it), without editing the vault automatically.

---

### 9. Integration sanity passes

- **Scenario walkthroughs to validate design (no code yet)**:
  - **Scenario A: CODE → INGEST, default profile**
    - New conversational rails: profile gate (default), pipeline choice, context_mode, max_candidates, rationale_style, optional distill_lens, source_file, user_guidance, final confirmation.
    - Confirm params map back to current INGEST contract and auto-eat-queue behavior.
  - **Scenario B: ROADMAP MODE then RESUME-ROADMAP with locked choices and changed profile**
    - Walk through: previous RESUME session exists → gate A → profile gate → profile change → warning and selective unlock of profile-derived params → re-asking those rails → final payload.
  - **Scenario C: Mid-session restart**
    - Start crafting, answer a few params, stop.
    - Trigger crafter again → resume/start-fresh prompt → resume from correct rail index without losing lock semantics.
  - **Scenario D: New profile creation**
    - User chooses new profile, completes rails, then picks "append and emit profile YAML"; confirm that resulting patch is deterministic and minimal.

These design decisions together make V2 a conversational-but-structured replacement for the rigid A/B/C flow, explicitly addressing the seven weak areas and your preferences about profiles, rails, and documentation scope, while leaving actual code and MCP changes for a later implementation pass.