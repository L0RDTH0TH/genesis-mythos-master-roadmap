---
title: User Questions and Options Reference
created: 2026-03-10
tags: [pkm, second-brain, user-flow, reference]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Prompt-Crafter-Param-Table]]", "[[Prompt-Crafter-Structure-Detailed]]", "[[User-Flow-Rules-Detailed]]"]
---

# User Questions and Options Reference

This document lists every user-facing question and its options **in the order they are presented**. Use it to implement macros, debug flows, or trace what users see at each decision point. Source of truth for param order: [[3-Resources/Second-Brain/Prompt-Crafter-Param-Table|Prompt-Crafter-Param-Table]]; for flows: [[3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed|Prompt-Crafter-Structure-Detailed]] and [[3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Rules-Detailed|User-Flow-Rules-Detailed]].

---

## 1. Question-led Prompt Crafter (Chat/Agent)

**When:** User says "We are making a prompt" (or "We are making a CODE prompt" / "We are making a ROADMAP prompt"). **Use Chat or Agent mode. Do not use Cursor Plan mode for this flow (Plan mode creates a plan file instead of asking questions).**

**ROADMAP mirror:** The ROADMAP side uses identical A/B/C semantics and explanatory style; ask params in existing param order with wording patterned on the CODE flow (what it does, default, recommended ranges where applicable).

**Question-led contract:** The agent must ask **every** question in this section for the current branch, **in order**. No skips. Skipping any question fails the run. The only question that may be omitted is **Q0** when the user has already said CODE or ROADMAP; all other questions must be asked. **"Optional"** refers to whether the user includes the param (A/B/C); every param in "Param order by branch" must still be **asked**.

Questions are asked **one per message** so Cursor can show the question box with clickable A/B/C. Each optional param is asked with a short "It does …" explanation.

### How to format each question (Chat/Agent)

One question per message. Use **real line breaks** (not literal `\n`). Do not wrap in a code block. Put each option on its own line: first line = question (and optional "**It does:** …"); then a blank line; then "**A.** …", "**B.** …", "**C.** …" on separate lines. This format helps Cursor show the question box with click-to-answer; Cursor has a known bug where `\n` can render literally, so avoid escaping newlines.

**Example (Q0 — each option on its own line):**

Which kind?

**A.** CODE (pipelines: ingest, organize, distill, express, archive, task modes)

**B.** ROADMAP (setup or resume roadmap)

### Order of questions

**Q0 — Only if kickoff unclear** (user said only "We are making a prompt" without CODE or ROADMAP)

**Which kind?**

- **A.** CODE (pipelines: ingest, organize, distill, express, archive, task modes)
- **B.** ROADMAP (setup or resume roadmap)

**Then by branch (exactly three options per question — A, B, C only; never D, E, F, or G):**

- **CODE:** One question with **exactly three options**: **A.** INGEST_MODE | **B.** ORGANIZE_MODE | **C.** Other (DISTILL_MODE, EXPRESS_MODE, ARCHIVE_MODE, or task modes — if user picks C, ask a follow-up with exactly A/B/C). Then param questions in **question_order** from [[3-Resources/Second-Brain/Prompt-Crafter-Param-Table|Prompt-Crafter-Param-Table]] for the chosen sub-mode.
- **ROADMAP:** First question: **A.** ROADMAP_MODE (setup) | **B.** RESUME_ROADMAP. **If B (RESUME_ROADMAP), V4 order:** (1) **Resume gate** (when scratchpad has prior RESUME session with non-empty `explicit_choices`): show locked params, offer A keep locks / B discard. (2) **Profile gate:** show active_profile and list roadmap profiles; keep / switch / default / defer. (3) **"Which action?"** with **exactly three options**: **A.** deepen | **B.** recal | **C.** Other (revert-phase, sync-outputs, handoff-audit, expand, advance-phase, bootstrap-execution-track, etc. — if C, ask again with A/B/C). (4) Then ask **every** param in "Param order by branch" for RESUME_ROADMAP (param 1 = action already set by "Which action?"; ask params 2–23: project_id, phase, sectionOrTaskLocator, research_result_preference, research_focus, candidate_urls, research_max_escalations, …, **roadmap_track**). Do not skip any param question. Do **not** ask "Which action?" before the resume and profile gates.

**ROADMAP_MODE (setup) → session ends after append (V4):** When the branch is **ROADMAP_MODE (setup)**, after the user confirms "Append to queue?" (Y), the agent (1) appends the setup payload to `.technical/prompt-queue.jsonl`, (2) commits the scratchpad (session complete), (3) outputs: *"Queued successfully to prompt-queue.jsonl. Run **EAT-QUEUE** whenever you're ready to process it. Crafting session complete. If you need another one, just say 'We are making a prompt' again."* (4) **Ends the session** — no follow-up questions. To craft a RESUME_ROADMAP entry, the user starts a new crafting run and chooses RESUME_ROADMAP.

**Quick sequence (param names only)** — ask in this order per branch; use "Param order by branch" below for full list and (manual) markers.

- **CODE → INGEST:** pipeline (set by Message 2), context_mode, max_candidates, rationale_style, distill_lens (optional conditional; manual if included), source_file (manual), user_guidance (manual). Param order by branch for CODE→INGEST now matches the Message 1–9 sequence above; distill_lens is optional conditional.
- **CODE → ORGANIZE:** source_file (manual), context_mode, max_candidates, profile, user_guidance (manual).
- **CODE → DISTILL:** source_file (manual), distill_lens (manual), depth / layers.
- **CODE → EXPRESS:** source_file (manual), express_view (manual).
- **CODE → ARCHIVE:** source_file (manual).
- **CODE → Task modes:** source_file (manual), task_id (manual), prompt (manual), sectionOrTaskLocator (manual), userText (manual).
- **ROADMAP_MODE (setup):** project_id, source_file (manual).
- **RESUME_ROADMAP:** action *(set by Which action?)*, project_id, phase, sectionOrTaskLocator (manual), enable_context_tracking, enable_research, research_queries (manual), **research_result_preference**, **research_focus**, **candidate_urls** (manual or "none"), **research_max_escalations**, async_research *(deprecated/no-op)*, research_distill, handoff_gate, min_handoff_conf, inject_extra_state, token_cap, max_depth, branch_factor, profile, userText (manual), queue_next, **roadmap_track**. **V4 rail order:** resume gate → profile gate → "Which action?" → params 2–23 (do not ask "Which action?" before the two gates).

**Option semantics (A/B/C):**

- **A** = explicit key = chosen value (user picks concrete option)
- **B** = omit key → Config / MCP default
- **C** = omit key + append short reasoning to payload (see C choice behavior below)

**Quick mapping table:**

| User choice | Queue payload effect | agent_reasoning append? |
|-------------|----------------------|-------------------------|
| **A** | explicit key = chosen value | no |
| **B** | key omitted → Config / MCP default | no |
| **C** | key omitted → default | yes (short reasoning, AI-only) |

**Boolean params:** For booleans (e.g. enable_research, enable_context_tracking): **A** = add param with chosen value (true or false); **B** and **C** = omit key — do not set explicit false on B or C. Downstream treats absent = default (e.g. usually enabled per Parameters/Queue-Sources). To explicitly disable (e.g. turn off research or context tracking), the user must choose **A** and pick the "off" option where offered, or edit the queue payload manually.

**Lock-first (V4):** When a param is in the scratchpad’s `explicit_choices`, its value **always wins** over profile or Config defaults. Profiles are presets only; they never overwrite locked values. The final payload must use `explicit_choices[param]` for every key present there. See [[3-Resources/Second-Brain/Prompt-Crafter-Implementation-Notes-V4|Prompt-Crafter-Implementation-Notes-V4]] §1.

### Conversational-on-rails and param_meta (V4)

- **Coverage and order:** The agent must cover **every** param in "Param order by branch" for the current branch, in that order. Phrasing may be conversational (on-rails) as long as each param is surfaced in sequence and semantics (explicit / default / AI-choice) are preserved.
- **Param descriptors:** When building questions, use the **Param descriptors** tables in this doc (§1): **description** → short explanation of what the param controls; **defaultWhenC** → what the system will do if the user says "you choose"; **accepts_manual_text** → if true, after structural inclusion is decided, ask a dedicated open-text turn ("What is the [param name]?" or equivalent). Do not compress manual-text params into a single choice; give them their own turn for content.
- **Lock-aware phrasing:** When a param is already locked (in `explicit_choices` and not scheduled for re-ask via profile-change flow), optionally show: "`param` is currently locked at `value`. Do you want to change it? (yes/no)." If no, keep lock and advance; if yes, ask for new value and update `explicit_choices` and `profile_derived[param] = false`. For params reinserted after "adopt profile and unlock affected," reference both the previous locked value and the new profile default when asking.
- **Final summary annotations:** For every run, the summary must label params that differ from Config/profile defaults: **profile** = from active profile; **manual override** = locked value overriding profile default (show both, e.g. "branch_factor: 5 (manual override over profile default 4)"); **AI choice** = omitted from params, reasoning in `agent_reasoning`. This keeps auditability clear.

### C choice behavior

When the user picks **C** (AI reasoning):

- Limit reasoning to **1–3 sentences max** (rule may allow up to 3–5; keep it short for payload).
- **Append that reasoning to the payload’s `agent_reasoning` field (and to the crafter scratchpad `agent_reasoning_log`) — never to `user_guidance`.** `user_guidance` is reserved for human-typed text only (manual text phase or existing frontmatter). Do not leave C reasoning in chat only; it must be written into the queue payload so EAT-QUEUE and guidance-aware flows can merge it into pipeline context as *AI reasoning*, separate from human guidance.

**Manual text phase** (after all param optionals): For each param with `accepts_manual_text: true` that was included, ask:

| Question | Input |
|----------|--------|
| What is the [param name]? | Free text |

**Final:**

> **Final confirmation question updated 2026-03-12 — see Message 9.**

**Message 9 – Final confirmation:** After presenting the payload summary, ask:

- **A.** yes — append to queue
- **B.** no — cancel / edit
- **C.** AI reasoning — double-check if anything looks off

On **A**: craft queue line, append to `prompt-queue.jsonl` (or Task-Queue.md per routing), reply "Queued. Run EAT-QUEUE when ready." On **B**: do not write; payload remains for copy-paste. On **C**: agent performs 1–3 sentence sanity check, then either suggests edits (no append) or confirms and appends.

For **RESUME_ROADMAP**, when the user confirms append (A or equivalent), the agent removes existing RESUME_ROADMAP entries from the queue (per Queue-Sources § Remove stale on RESUME_ROADMAP append), then appends the new line.

### Param order by branch (from Prompt-Crafter-Param-Table)

Ask in this order for each branch. One param per line; `(manual)` / `(manual text)` = ask "What is the [param name]?" in manual-text phase. **Source of truth for question_order and accepts_manual_text:** [[3-Resources/Second-Brain/Prompt-Crafter-Param-Table|Prompt-Crafter-Param-Table]].

- **ROADMAP MODE (setup only)** — ask in this order:
  1. project_id
  2. source_file / seed note path (manual text)
  Ask **both** in order; "few" does not mean skip.

- **RESUME-ROADMAP** — **V4:** Run resume gate, then profile gate, then ask "Which action?" (A. deepen | B. recal | C. Other) to set param 1. Then ask params 2–22 in this order:
  1. action *(already set by "Which action?" — do not ask again)*
  2. project_id
  3. phase
  4. sectionOrTaskLocator (manual)
  5. enable_context_tracking
  6. enable_research
  7. research_queries (manual)
  8. research_result_preference
  9. research_focus
  10. candidate_urls (manual or "none")
  11. research_max_escalations
  12. async_research
  13. research_distill
  14. handoff_gate
  15. min_handoff_conf
  16. inject_extra_state
  17. token_cap
  18. max_depth
  19. branch_factor
  20. profile
  21. userText (manual)
  22. queue_next
  23. roadmap_track

- **CODE → INGEST MODE** — ask in this order (matches Message 1–9 sequence; see "Question sequence — explicit wording" above):
  1. pipeline / mode (Message 2)
  2. context_mode
  3. max_candidates
  4. rationale_style
  5. distill_lens (optional conditional; manual if included)
  6. source_file (manual)
  7. user_guidance / prompt (manual)
  *(profile remains available; add as optional step or merge with Config defaults when not in minimal flow.)*

- **CODE → ORGANIZE MODE** — ask in this order:
  1. source_file (manual)
  2. context_mode
  3. max_candidates
  4. profile
  5. user_guidance / prompt (manual)

- **CODE → DISTILL MODE** — ask in this order:
  1. source_file (manual)
  2. distill_lens (manual)
  3. depth / layers

- **CODE → EXPRESS MODE** — ask in this order:
  1. source_file (manual)
  2. express_view (manual)

- **CODE → ARCHIVE MODE** — ask in this order:
  1. source_file (manual)

- **CODE → Task modes** — ask in this order:
  1. source_file (manual)
  2. task_id (manual, TASK-COMPLETE)
  3. prompt (manual)
  4. sectionOrTaskLocator (manual)
  5. userText (manual)

### Question sequence — explicit wording (CODE → INGEST)

Param order by branch for CODE→INGEST now matches this message sequence (pipeline first, then context_mode, …, user_guidance last). **distill_lens** is added as an optional conditional question.

**Message 1 – Welcome / mode choice**

Hello. You want to start using the Second Brain system.

There are two main sides right now:
- **CODE side** — focused on knowledge management (ingest → organize → distill → express/archive)
- **ROADMAP side** — focused on knowledge utilization & task/project tracking

Which side would you like to configure first?

**A.** CODE side (knowledge management pipelines)
**B.** ROADMAP side (project & task tracking)
**C.** AI reasoning — suggest which side makes most sense for me right now and why

*(If user picks C → agent gives 1–2 sentence reasoning + picks A or B, then continues. If ROADMAP, jump to roadmap-specific questions.)*

**Message 2 – Pipeline**

Assuming CODE side for now (we can switch later).

First question: which pipeline do you want to run?

**A.** INGEST MODE — bring new notes into the vault, classify PARA, propose paths, create Decision Wrappers
**B.** default (usually INGEST if you just captured something)
**C.** AI reasoning — look at recent vault activity and suggest best pipeline + why

**Message 3 – context_mode**

`context_mode` controls how much surrounding context (nearby notes, project docs, etc.) the classifier uses when suggesting PARA paths and subfolders.

- Strict = very focused on the note itself → most stable but can be conservative
- Loose = pulls more vault context → better for interconnected ideas but noisier

Default (when omitted) = strict-para

**A.** strict-para (recommended for most new users & stability)
**B.** default (let system decide)
**C.** AI reasoning — pick best for these notes and explain why

**Message 4 – max_candidates**

`max_candidates` = how many PARA path options to propose per note (Decision Wrapper shows up to 7).

More candidates = more choice but noisier proposals.
Recommended safe range: 3–10. Above 10 often wastes time.

Default = 7

**A.** 7 (balanced default)
**B.** default (7)
**C.** AI reasoning — suggest optimal number for this batch + why

**Message 5 – rationale_style**

`rationale_style` sets how detailed / formatted the reasoning is in proposals (affects readability & length).

Options: concise / detailed / bullet / technical

Default = concise

**A.** concise (short & clear — best starting point)
**B.** default (concise)
**C.** AI reasoning — recommend style for these notes & why

**Message 6 – distill_lens / highlight_perspective** (optional / conditional)

Do you want to run this with a specific **distill lens** or **highlight perspective**? (e.g. "combat systems", "monetization", "technical debt")

This applies color-coded highlighting layers and focuses distillation on that angle.

**A.** yes — ask me for the lens/perspective
**B.** no / default (no special lens)
**C.** AI reasoning — suggest whether a lens makes sense here & which one

*(If A → next message asks for the actual lens string)*

**Message 7 – source_file / batch**

Do you want to target specific notes right now?

**A.** yes — give me file path(s) or folder (can be comma-separated or glob)
**B.** default (process Ingest/ folder or recently captured)
**C.** AI reasoning — suggest which notes to process based on vault state

**Message 8 – user_guidance** (free-text phase)

Anything else you want to tell the system? (guidance, constraints, style notes, etc.)

You can write a short paragraph or bullet list. This gets merged into the prompt.

**A.** yes — here it is: [user pastes text]
**B.** no / skip (clean run)
**C.** AI reasoning — propose some starter guidance based on the notes

**Message 9 – Final confirmation**

Here's what we're about to queue:

- Pipeline: INGEST MODE
- context_mode: strict-para
- max_candidates: 7
- rationale_style: concise
- … (other params)

**A.** yes — append to queue
**B.** no — cancel / edit
**C.** AI reasoning — double-check if anything looks off

*(On A → craft queue line, append to prompt-queue.jsonl, reply "Queued. Run EAT-QUEUE when ready.")*

**RESUME-ROADMAP — question sequence (V4: resume gate + profile gate + params, after "Which action?"):**

1. **Resume gate** (when scratchpad has prior RESUME session with non-empty `explicit_choices`): Show grouped summary of locked params and values. Offer:
   - **A.** Keep previous locks and resume with them.
   - **B.** Discard previous locks and start a completely fresh RESUME-ROADMAP session for this project.
2. **Profile gate:** Show current `active_profile` (if any) and available roadmap profiles. Options: Keep current profile | Switch to another existing profile | Use default (no profile) | Defer new profile to end of run.
3. **Profile change with locks** (when user switches profile or selects default and locks exist): Compute profile-vs-lock diff using `profile_derived`; show diff list (params where new profile default ≠ current locked value). Offer:
   - **A.** Adopt profile and unlock all affected params → re-ask them in order.
   - **B.** Adopt profile but keep current locked values (hybrid) → final summary must label these as "manual override over profile default X."
   - **C.** Keep old profile → cancel profile switch.
   - **D.** Manually adjust selected locked params → ask which params to change, accept fuzzy labels; for each, ask new value and update locks; then adopt profile for non-locked params.
4. action *(already set by "Which action?" — do not ask again)*
5. Ask params 2–22 in order from **Param order by branch** above. When a param is in `explicit_choices` and not unlocked by step 3A, treat as locked and do not re-ask (use stored value). For each unlocked or new param: A/B/C per semantics; for (manual) params ask "What is the [param name]?" in manual-text phase.
6. **Final confirmation** — same as Message 9 (A. yes — append | B. no — cancel | C. AI reasoning). Optionally offer "Save these settings as a new profile (YAML patch)" before or after append.

### Param descriptors (for agents and param_meta overlay)

Agents MAY emit, alongside the primary queue payload, an **optional advisory overlay**:

- `param_meta: { <paramName>: { description: string, defaultWhenC: string, usedBy?: string } }`

This overlay is **read-only decoration**:

- Queue processors and pipelines **ignore** `param_meta` for behavior and validation.
- A valid v2 payload is a v1 payload **plus optional** `param_meta`; consumers that do not know about `param_meta` remain correct.

Use the tables below to populate `param_meta` and to generate the "**It does:** …" lines and C-option explanations when asking questions.

#### ROADMAP MODE (setup)

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| project_id | ROADMAP MODE (setup) | Identifies which project the roadmap belongs to. | Required; no default — ask user. |
| source_file | ROADMAP MODE (setup) | Points to the seed outline / PMG note used to generate the roadmap. | Required; no default — ask user. |

#### RESUME-ROADMAP (continue)

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| action | RESUME-ROADMAP | Chooses what the resume step does (deepen, recal, revert, etc.). | `deepen` when not set; see Parameters § RESUME-ROADMAP. |
| project_id | RESUME-ROADMAP | Binds the resume run to a specific project roadmap. | Inferred from source_file or path when absent; ask when unclear. |
| phase | RESUME-ROADMAP | Selects which phase of the roadmap to work on. | Uses current_phase from roadmap-state when omitted. |
| sectionOrTaskLocator | RESUME-ROADMAP | Narrows work to a specific section or task within the phase. | Whole-phase target when omitted. |
| enable_context_tracking | RESUME-ROADMAP | Turns context-utilization tracking and gating on/off. | Effectively **on by default**; only explicit `false` disables (see Parameters). |
| enable_research | RESUME-ROADMAP | Enables pre-deepen external research for the current phase. | Auto-detected from content and util when omitted (see Queue-Sources/Parameters). |
| research_queries | RESUME-ROADMAP | Supplies explicit research queries for research-agent-run (strings or structured with slot/intent/prefer). | Auto-generated from phase content when omitted. |
| research_result_preference | RESUME-ROADMAP | How to rank/select discovery results: official_docs, recent, with_code, diverse, academic. | Absent = current behavior (e.g. junior-handoff guidance for roadmap-deepen). |
| research_focus | RESUME-ROADMAP | Steers synthesis audience: junior_handoff, cto_brief, spike_proposal, risk_maximal. | Absent = current synthesis style. |
| candidate_urls | RESUME-ROADMAP | URLs to extract first (curated "best options"); research fills gaps with discovery. | None when omitted; manual text or "none". |
| research_max_escalations | RESUME-ROADMAP | How many times the research agent may internally revise queries (request-sanity step) before fetch. Pre-deepen often uses 0. | 1 for crafted entries; pre-deepen may inject 0. **A.** 0 (off — skip sanity) **B.** 1 (one revision) **C.** 2 (two revisions). |
| async_research | RESUME-ROADMAP | Legacy flag for async research scheduling. | **Deprecated/no-op** — accepted but ignored; behaves as if false. |
| research_distill | RESUME-ROADMAP | Controls whether new research notes also get DISTILL MODE queued. | Defaults to `false` unless explicitly enabled. |
| handoff_gate | RESUME-ROADMAP | Enables the hand-off readiness gate for this run. | Uses config defaults when omitted; off unless gate is enabled in config. |
| min_handoff_conf | RESUME-ROADMAP | Sets the minimum handoff readiness score to treat a phase as delegatable. | Uses `min_handoff_conf` from Parameters/Config when omitted. |
| inject_extra_state | RESUME-ROADMAP | When true, injects extra state notes into the deepen context (core, decisions, siblings). | Uses config defaults; off unless explicitly true or aliased mode sets it. |
| token_cap | RESUME-ROADMAP | Upper bound on tokens used for injected extra state. | Uses config default (e.g. 50000) when omitted. |
| max_depth | RESUME-ROADMAP | Caps roadmap tree depth for this run. | Derived from phase / config defaults when omitted (see Parameters). |
| branch_factor | RESUME-ROADMAP | Controls branching factor (children per node) during deepen. | Uses config defaults (e.g. 4 for deeper phases) when omitted. |
| profile | RESUME-ROADMAP | Selects a prompt_defaults.roadmap profile to merge into params. | Uses default profile from Config when omitted. |
| userText | RESUME-ROADMAP | Free-form user instructions for the next roadmap step. | No extra guidance when omitted. |
| queue_next | RESUME-ROADMAP | Controls whether the pipeline auto-queues another RESUME-ROADMAP after this one. | **true** when absent/undefined; only explicit `false` disables auto-queue (see Parameters/Queue-Sources). |
| roadmap_track | RESUME-ROADMAP | Optional **track lock** on the queue line: `conceptual` or `execution`. When present, sets **`effective_track`** for that run regardless of `roadmap-state.md`. | Omitted → resolve **`effective_track`** from `roadmap-state.md` only (see Queue-Sources § **effective_track**). |

#### CODE → INGEST MODE

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| source_file | INGEST MODE | Tells ingest which note or file to process. | Required; no default — ask user. |
| context_mode | INGEST MODE | Adjusts how much surrounding context is used for PARA classification and proposals. | Uses ingest defaults (strict/normal) from Config when omitted or C. |
| max_candidates | INGEST MODE | Caps how many PARA path candidates are proposed. | Uses tool/MCP default (e.g. 7) when omitted or C. **Recommended range:** 3–10; above 10 often wastes time. |
| profile | INGEST MODE | Selects a prompt_defaults.ingest profile (e.g. default vs project-priority). | Uses default profile from Config when omitted or C. |
| user_guidance / prompt | INGEST MODE | Carries user-written guidance to steer ingest decisions. | No extra guidance when omitted. |
| rationale_style | INGEST MODE | Chooses style/verbosity for MCP rationale text. | Uses MCP default style when omitted or C. |

#### CODE → ORGANIZE MODE

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| source_file | ORGANIZE MODE | Note to re-classify and re-organize. | Required; no default — ask user. |
| context_mode | ORGANIZE MODE | How much neighboring context to consider for new path suggestions. | Uses organize defaults from Config when omitted or C. |
| max_candidates | ORGANIZE MODE | Max PARA path candidates to consider for organize. | Uses tool/MCP default when omitted or C. |
| profile | ORGANIZE MODE | Prompt/profile variant for organize behavior. | Uses default organize profile when omitted or C. |
| user_guidance / prompt | ORGANIZE MODE | Optional human guidance for organizing this note. | No extra guidance when omitted. |

#### CODE → DISTILL MODE

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| source_file | DISTILL MODE | Note to run autonomous-distill on. | Required; no default — ask user. |
| distill_lens | DISTILL MODE | Perspective or lens to use when distilling (e.g. beginner, expert). | Uses note/project defaults or generic lens when omitted. |
| depth / layers | DISTILL MODE | Target number of distillation layers / depth. | Auto-chosen by auto-layer-select when omitted or C. |

#### CODE → EXPRESS MODE

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| source_file | EXPRESS MODE | Note to generate expressive output for. | Required; no default — ask user. |
| express_view | EXPRESS MODE | Audience/view to bias outline and related content (e.g. stakeholder vs dev). | Uses default or frontmatter express_view when omitted. |

#### CODE → ARCHIVE MODE

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| source_file | ARCHIVE MODE | Note to evaluate for archive and move to 4-Archives. | Required; no default — ask user. |

#### CODE → Task modes

| param | Used in | It does | Default when C / omitted |
|-------|---------|---------|---------------------------|
| source_file | Task modes | Note that contains the roadmap/task being manipulated. | Required; no default — ask user. |
| task_id | TASK-COMPLETE | Identifies which checklist task to complete. | Required for TASK-COMPLETE; no default. |
| prompt | ADD-ROADMAP-ITEM / EXPAND-ROAD | Human text describing the new roadmap item or expansion intent. | No new narrative added when omitted. |
| sectionOrTaskLocator | EXPAND-ROAD | Locates the section or task that should be expanded. | Whole-note / inferred section when omitted. |
| userText | EXPAND-ROAD | Extra guidance or seed content for expansion. | No extra guidance when omitted. |

---

## 2. Decision Wrappers (ingest, phase-direction, refinements, low-confidence, error)

**When:** Pipeline creates a Decision Wrapper under `Ingest/Decisions/**` (e.g. after classify with mid/low confidence, phase-direction, or error).

**Options (in order):**

| Option | Meaning |
|--------|---------|
| **A, B, C, D, E, F, G** | Ranked PARA paths (or conceptual end-state descriptions for phase-direction); content varies per wrapper. Order is stabilizer-adjusted (PARA-Actionability-Rubric → semantic fit → path depth → alphabetize); exactly 7 via pad-to-7 when fewer candidates. |
| **0** | Reject all. |
| **R** | Re-try with guidance (roadmap/phase-direction wrappers only). Runs re-try branch: re-queue EXPAND-ROAD or TASK-TO-PLAN-PROMPT with guidance; capped by re_try_max_loops. |
| **re-wrap: true** (frontmatter) | Unhappy with all options; archive this wrapper and create a new one with Thoughts as seed. |

**User action:** Check one of A–G (or 0 or R) and set `approved: true` in frontmatter; then run **EAT-QUEUE** to apply path, re-wrap, or re-try.

---

## 3. Cap-hit wrapper (re-try cap exceeded)

**When:** User chose R or re-try and `re_try_count` has reached `re_try_max_loops`; agent creates a cap-hit wrapper.

**Options:**

| Option | Meaning |
|--------|---------|
| **A** | Force approve |
| **B** | Prune branch |
| **0** | Re-wrap full phase |

---

## 4. Roadmap-next-step wrapper

**When:** Agent is uncertain which roadmap action to take; creates a roadmap-next-step wrapper under `Ingest/Decisions/Roadmap-Decisions/`.

**Options (letter → action):**

| Option | Action |
|--------|--------|
| **A** | deepen |
| **B** | recal |
| **C** | advance-phase |
| **D** | raise cap and continue |
| **E** | revert-phase |
| **F** | sync-outputs then deepen |
| **0** | re-wrap |

Wrapper body must include a short **"Why uncertain"** rationale callout before options A–G. See [[3-Resources/Second-Brain/Parameters|Parameters]] § roadmap-next-step wrapper and [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference|Cursor-Skill-Pipelines-Reference]] apply-from-wrapper table.

---

## 5. Commander "Craft Prompt" macro

**When:** User runs the Commander "Craft Prompt" (or "Prompt Craft") macro.

**Questions and options (in order):**

| Question | Options |
|----------|---------|
| Pipeline | **ingest** \| **organize** |
| Profile | **default** \| **project-priority** |
| Then | **Preview Assembly** (paste assembled prompt to temp note; no queue append) \| **Craft and Queue** (validate params, then append one line to `.technical/prompt-queue.jsonl`) |

Sub-macros (e.g. "Craft Ingest Default") fix pipeline/profile; user only chooses Preview vs Craft and Queue and, if queue, source_file.

---

## Cross-references

- [[3-Resources/Second-Brain/Prompt-Crafter-Param-Table|Prompt-Crafter-Param-Table]] — question_order, parentage, accepts_manual_text.
- [[3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed|Prompt-Crafter-Structure-Detailed]] — question-led flow, A/B/C pattern, manual text phase.
- [[3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Rules-Detailed|User-Flow-Rules-Detailed]] — Decision Wrapper full option set, Step 0, re-wrap, re-try.
- [[3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Detailed|User-Flow-Prompt-Crafter-Detailed]] — Commander macro, validation, error paths.
- [[3-Resources/Second-Brain/Parameters|Parameters]] — roadmap-next-step wrapper, cap-hit, re_try_max_loops.
- [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference|Cursor-Skill-Pipelines-Reference]] — apply-from-wrapper table (wrapper_type → Step 0 behavior).
- [[3-Resources/Second-Brain/Queue-Alias-Table|Queue-Alias-Table]] — mode aliases for CODE pipeline picker.
- [[Templates/Decision-Wrapper|Templates/Decision-Wrapper]] — Decision Wrapper template (A–G, 0, R, re-wrap).
