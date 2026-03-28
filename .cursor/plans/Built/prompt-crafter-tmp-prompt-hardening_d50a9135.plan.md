---
name: prompt-crafter-tmp-prompt-hardening
overview: Migrate the question-led prompt crafter and roadmap resume flows to use a tmp-prompt.json scratchpad, strict separation of user_guidance vs agent_reasoning, and smart RESUME-ROADMAP behavior that preserves manual choices while re-evaluating defaults, with strong shielding against failure modes.
todos:
  - id: tmp-prompt-config-spec
    content: Specify tmp-prompt.json schema, config keys (crafting.tmp_prompt_path, max_reasoning_sentences), and invariants without changing any files yet.
    status: completed
  - id: crafter-scratchpad-integration-design
    content: Design how plan-mode-prompt-crafter will read/init tmp-prompt, track asked/explicit choices, and skip already-locked params while keeping single-write-to-queue invariant conceptually intact.
    status: completed
  - id: guidance-separation-spec
    content: Define the new user_guidance vs agent_reasoning contract, including C-choice behavior changes and guidance-aware merge semantics, ensuring backward compatibility with existing queue entries.
    status: completed
  - id: smart-resume-roadmap-spec
    content: Define smart RESUME-ROADMAP behavior that locks manual A-choices, re-checks B/C/default params on resume (including auto-chained queue_next entries), and integrates the new resume gate question.
    status: completed
  - id: docs-and-sync-updates-plan
    content: Plan the documentation and sync updates across User-Questions-and-Options-Reference, Prompt-Crafter-Structure docs, Queue-Sources, Parameters, and the synced prompt-crafter rule file.
    status: completed
  - id: failure-modes-and-rollout
    content: Enumerate key failure modes (tmp-prompt corruption, missing state, legacy entries) and define safe fallbacks and dry-run validation scenarios for migration.
    status: completed
isProject: false
---

## Behavior Migration v1 — Hardened & Shielded

### 1. Map current behavior and invariants

- **Review prompt-crafter contract** in `[.cursor/rules/context/plan-mode-prompt-crafter.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/plan-mode-prompt-crafter.mdc)` and its synced copy to identify all places that:
  - Read question text / param order from `[User-Questions-and-Options-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)`.
  - Build `mode` + `params` payloads and currently merge C-choice reasoning into `user_guidance`.
  - Contain special handling for ROADMAP MODE + RESUME-ROADMAP (including remove-stale logic and single-entry funnel).
- **Confirm queue payload shape** in `[Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md)` and RESUME-ROADMAP parameter semantics / defaults in `[Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md)` to understand where crafted params are consumed and how guidance-aware runs currently treat `prompt` vs `user_guidance`.
- **Locate RESUME-ROADMAP dispatch and normalization** in `[auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc)` and the guidance-aware merge behavior in `[guidance-aware.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/always/guidance-aware.mdc)` so the new agent_reasoning field and smart-resume gate hook into the right stages without breaking existing safety gates.

### 2. Introduce tmp-prompt.json scratchpad (Phase 0–1)

- **Config & filesystem wiring (read-only in this plan)**
  - Extend the documented config structure in `[Configs.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Configs.md)` and `[Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md)` with a `crafting` block that includes:
    - `tmp_prompt_path: ".technical/tmp-prompt.json"` (single source of truth for the prompt-crafter scratch file path).
    - `max_reasoning_sentences` (default 3) to cap per-C-choice reasoning length.
  - In the plan, note that `.technical/tmp-prompt.json` must remain visible to Cursor (like `prompt-queue.jsonl`) but excluded from Obsidian indexing; actual `.cursorignore` / Obsidian exclusion edits happen later in implementation.
- **Define scratchpad JSON schema and invariants**
  - Specify the structure used by the crafter for **every question-led session**:

```json
    {
      "session_id": "req-123",
      "mode": "RESUME-ROADMAP",
      "asked": ["mode", "project_id", "phase", "context_mode", ...],
      "explicit_choices": {
        "project_id": "MyProject",
        "branch_factor": 6,
        "enable_research": true
      },
      "agent_reasoning_log": [
        {"param": "branch_factor", "text": "1–3 sentences"}
      ],
      "final_payload_draft": {"params": { /* last-crafted values for B/C/defaulted params */ }}
    }
    

```

- Document invariants:
  - **Only one active scratchpad per crafting session**; `session_id` can be the queue `id` or a synthetic token per run.
  - `explicit_choices` holds **only A-path manual picks** (sacred choices) keyed by param name, never overwritten by future resumes unless the user explicitly changes them in a later session.
  - `final_payload_draft` contains **the last non-manual state** (B/C/default values) so RESUME-ROADMAP and other modes can reuse or re-check them.
  - `agent_reasoning_log` is append-only per C-choice, capped by `max_reasoning_sentences` per entry.
- **Integrate scratchpad lifecycle into prompt-crafter rule (shielded)**
  - In `plan-mode-prompt-crafter.mdc`, specify a **non-destructive read-or-init step** at the start of any crafting run:
    - If `tmp_prompt_path` exists and parses, load into memory; otherwise treat as empty and initialize an in-memory structure (writes are still governed by existing “single allowed write” invariant — queue append — so tmp-prompt updates must be conceptually described here but implemented via safe, incremental writes later).
    - On load failure (invalid JSON), the hardened behavior is to **abort crafting** with a clear error message and **not touch** the corrupt file; error handling can be delegated to a separate repair flow so the crafter never proceeds from ambiguous state.
  - Before asking each question, the crafter must:
    - Check `explicit_choices` for that param; if a value exists, **skip the question entirely** and treat the stored value as the user’s answer (this respects “manual choices are sacred”).
    - Append the param name into `asked` (even when skipped) so the session log stays complete.
  - On **A-choice** for any param:
    - Record the choice into `explicit_choices[param]`.
    - Update `final_payload_draft` to match but ensure future resumes always source that param from `explicit_choices` first.
  - On **B or C choice**:
    - Update `final_payload_draft` for that param (or leave omitted if the semantics are “default when absent”).
    - For C, append a capped reasoning object into `agent_reasoning_log` but **never add this text to `user_guidance`** (to preserve clean guidance separation later).
  - At final confirmation (Message 9 equivalent), the crafter uses `explicit_choices + final_payload_draft` to assemble the queue payload, then marks in the design:
    - tmp-prompt may be **deleted, archived, or left for resume** depending on whether this is a one-shot crafting or the first element in an auto-chain; the hardened behavior is to **prefer keeping it** for RESUME-ROADMAP continuity and explicitly clear it only when a new crafting session intentionally resets state.

### 3. Separate user_guidance vs agent_reasoning (Phase 2)

- **Extend payload contract in Queue-Sources & Parameters (spec-level)**
  - In `[Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md)`, add `agent_reasoning` as an optional, advisory field alongside existing keys:

```json
    {
      "mode": "RESUME-ROADMAP",
      "source_file": "...",
      "user_guidance": "Human-typed text only",
      "agent_reasoning": "Concatenated 1–3 sentence snippets from each C choice"
    }
    

```

- Clarify that:
  - `**user_guidance` remains pure human input** (frontmatter or manual text phase).
  - `**agent_reasoning`** is derived solely from C choices and is safe to ignore for behavior (similar to `param_meta`), but may be used to **augment context** in guidance-aware runs and for logging/observability.
- In `[Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md)`, update the `user_guidance` section to emphasize this separation and add a new subsection for `agent_reasoning` describing its provenance, length cap, and role.
- **Adjust prompt-crafter C-choice behavior (shield backward compatibility)**
  - In `plan-mode-prompt-crafter.mdc` and `[User-Questions-and-Options-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §1 C choice behavior`, change the rule from “append to user_guidance” to:
    - Append C reasoning **only** to `agent_reasoning` (and to the in-memory `agent_reasoning_log` / scratchpad).
    - Keep `user_guidance` reserved for free-text answers from the manual text phase or existing frontmatter.
  - Ensure the plan explicitly states that older entries where C-reasoning was merged into `prompt`/`user_guidance` remain valid; guidance-aware runs should treat `prompt` as a legacy blend but **new crafted entries** must follow the clean separation.
- **Update guidance-aware merge semantics (no behavior change, only richer context)**
  - In `guidance-aware.mdc` and `auto-eat-queue.mdc` documentation, describe a new merge order for guidance text:
    - Prefer `user_guidance` frontmatter when present.
    - Else use queue `prompt` / legacy merged guidance.
    - When `agent_reasoning` is present on the queue entry, it can be appended as a clearly-marked secondary block in the guidance context (e.g. “AI reasoning from prior C choices: …”) but must **not** modify confidence bands or bypass safety gates.
  - Logging requirements: when guidance-aware runs see `agent_reasoning`, include a short flag in logs (e.g. `agent_reasoning_used: true`) but keep all safety invariants unchanged.

### 4. Smart RESUME-ROADMAP with preserved manual choices (Phase 3)

- **Define how RESUME-ROADMAP reads historical intent**
  - Document, in `Queue-Sources.md` and `Prompt-Crafter-Structure-Detailed.md`, how RESUME-ROADMAP resume runs should locate prior state:
    - Prefer `tmp-prompt.json` if it exists and the `session_id` / `mode` match the project/roadmap being resumed.
    - Otherwise, derive a “previous baseline” from the most recent RESUME-ROADMAP queue entry for that project (read-only inspection of `params`), inferring which keys were likely manual (e.g. those that diverge from Config defaults or were explicitly answered in the last crafting session once tmp-prompt is in use).
  - Clearly state that **only values in `explicit_choices`** are treated as sacred and locked; others should be treated as candidates for re-evaluation.
- **Add the resume gate question to the ROADMAP flow**
  - In `User-Questions-and-Options-Reference.md` ROADMAP section, introduce a **new first question** when entering RESUME-ROADMAP:
    - “Resume with your previous explicit choices locked in?” with A/B/C:
      - A. Yes — keep all my manual settings exactly as last time.
      - B. Default — re-evaluate everything.
      - C. AI reasoning — scan recent vault changes and suggest adjustments (1–3 sentences).
  - In `plan-mode-prompt-crafter.mdc`, describe how this gate interacts with tmp-prompt:
    - On **A**: all keys in `explicit_choices` are carried forward as hard locks; questions for those params are skipped; only B/C/default params are re-asked.
    - On **B**: treat **both explicit_choices and final_payload_draft as hints only**; the crafter is allowed to re-ask all questions, but for sacredness the plan should note that A-type locks from earlier sessions are not auto-cleared unless the user makes a new explicit choice this run.
    - On **C**: allow the crafter to scan for **recent vault or roadmap-state changes** (conceptually via workflow_state and roadmap-state) and propose param tweaks in `agent_reasoning`; sacred explicit choices remain unless the user explicitly overrides them in the new session.
- **Ensure auto-chained queue_next respects locks**
  - In `Queue-Sources.md` and `auto-eat-queue.mdc` documentation, note that when the roadmap pipeline auto-appends follow-up RESUME-ROADMAP entries based on `queue_next: true`:
    - Manual choices (those that were A in the original crafting and thus in `explicit_choices`) must be copied exactly into the auto-appended params.
    - Any params that were defaults or C-mode at craft time can be auto-carried but should be considered re-checkable when the user later starts a new crafted RESUME-ROADMAP session (i.e. they land in `final_payload_draft`, not `explicit_choices`).
  - Clarify that the **remove-stale behavior** (dropping older RESUME-ROADMAP entries when a new crafted one is appended) remains unchanged, but the smart-resume gate uses tmp-prompt + last crafted entry to restore intent.

### 5. Hardening and failure-mode shielding

- **tmp-prompt.json corruption and concurrency**
  - In the plan, enumerate defensive behaviors for tmp-prompt:
    - **Corrupt JSON** → treat as hard failure: crafter aborts, reports a clear error, and does not attempt to partially repair or synthesize state.
    - **Missing or empty** → treat as fresh session; no sacred manual choices inferred until the user answers A again.
    - **Multiple concurrent crafting sessions** (e.g. user starts a second prompt while tmp-prompt still reflects the first): define that each crafting run should either:
      - Overwrite `session_id` and treat the current run as authoritative, or
      - Use a per-session scratch file name (e.g. `tmp-prompt-<session_id>.json`) in a future iteration, while this v1 keeps a single file and assumes one active crafting session at a time.
- **Backward compatibility and partial deployment**
  - Guarantee that existing queue lines **without** `agent_reasoning` or scratchpad data remain valid:
    - Guidance-aware continues to use `prompt` / `user_guidance` as today.
    - RESUME-ROADMAP continues to function, with smart-resume behavior activating only when tmp-prompt is present.
  - Document that until all pieces are wired, the crafter must **not** change payload shape (e.g. still emit `mode`, `params`, `prompt`, optional `param_meta`), and `agent_reasoning` should be introduced as a purely additional field.
- **Safety around manual overrides**
  - Emphasize that sacred manual choices must **never be silently downgraded**:
    - Any attempt to change an `explicit_choices` value must come from a new A-choice in a later session.
    - Auto-chained entries and recal flows must read but not rewrite `explicit_choices`.
  - For smart-resume C-option “scan recent vault changes,” specify that the output is **recommendations in agent_reasoning only**; it may propose that the user re-run the crafter or adjust certain params, but must not auto-patch `explicit_choices` or queue params without a new crafting confirmation.

### 6. Documentation & sync (Phase 4)

- **Update question and flow references**
  - In `User-Questions-and-Options-Reference.md`, add:
    - The new RESUME-ROADMAP resume gate question and its A/B/C semantics, in the ROADMAP question sequence.
    - Clarifications in the **C choice behavior** table that C now writes to `agent_reasoning` instead of `user_guidance`.
    - A short subsection documenting the role of `tmp-prompt.json` as the prompt-crafter state source of truth.
  - In `[Prompt-Crafter-Structure-Detailed.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)` and `[Prompt-Crafter-Structure-Mid-Level.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Mid-Level.md)`, describe:
    - Where tmp-prompt fits in the architecture diagrams (add nodes for `tmp-prompt.json` read/write around the Agent node).
    - How `agent_reasoning` parallels `param_meta` as advisory-only data.
- **Extend queue and guidance docs**
  - In `Queue-Sources.md`, extend the queue entry spec and fallback/merge narrative to include `agent_reasoning` and clarify how it interacts with guidance-aware runs and Prompt-Log.
  - In `Parameters.md`, ensure the `prompt_defaults` / crafted-params sections reference the new crafting block and that `user_guidance` vs `agent_reasoning` semantics are clearly separated.
- **Sync rule copy**
  - Ensure that once `plan-mode-prompt-crafter.mdc` is updated, its synced copy at `[.cursor/sync/rules/context/plan-mode-prompt-crafter.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/context/plan-mode-prompt-crafter.md)` is kept in lockstep, per backbone-docs-sync, including any references to tmp-prompt, sacred manual choices, guidance separation, and smart RESUME-ROADMAP behavior.

### 7. Rollout strategy and validation (non-destructive tests)

- **Dry-run reasoning tests (no writes)**
  - Define a set of hypothetical crafting transcripts for RESUME-ROADMAP (with a mix of A/B/C answers) and describe expected scratchpad state (`explicit_choices`, `final_payload_draft`, `agent_reasoning_log`) and resulting queue payloads across:
    - First craft.
    - Auto-chained follow-up via `queue_next: true`.
    - Manual resume with the new gate using A, B, and C.
  - Cross-check that in all cases:
    - Manual A-choices propagate unchanged.
    - Defaults and C-based values can be re-evaluated on resume.
    - `user_guidance` remains human-only, while `agent_reasoning` holds all AI explanations.
- **Failure-path walkthroughs**
  - Include in the plan explicit traces for:
    - tmp-prompt missing.
    - tmp-prompt corrupt.
    - Queue entries lacking `agent_reasoning` (legacy).
    - RESUME-ROADMAP invoked without prior ROADMAP MODE but with existing state.
  - For each, declare the intended safe fallback (e.g. abort vs proceed with legacy behavior) so implementation can be checked against these expectations.

