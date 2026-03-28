# Prompt-Crafter User Flow

**Version: 2026-03 – post-subagent migration**

Describes the question-led Prompt-Crafter flow: triggers, Q&A order, manual text phase, and queue append. The Crafter is a **context rule**, not a subagent; it produces a single queue payload after user confirmation.

---

## Purpose

Single reference for how the Prompt Crafter runs when you say "We are making a prompt" (or CODE/ROADMAP variant): which mode to use, question order, when the payload is written, and where it is appended (prompt-queue.jsonl vs Task-Queue.md).

---

## Trigger

- **"We are making a prompt"** — agent asks Q0 (Which kind? CODE vs ROADMAP) first.
- **"We are making a CODE prompt"** — skip Q0; go to CODE mode-narrowing (INGEST, ORGANIZE, DISTILL, EXPRESS, ARCHIVE, or task modes).
- **"We are making a ROADMAP prompt"** — skip Q0; go to ROADMAP mode-narrowing (ROADMAP MODE setup vs RESUME-ROADMAP).

Equivalent phrases: "craft a queue entry", "build a prompt for ROADMAP", etc.

**Important:** Use **Chat or Agent mode** for this flow. Do **not** use Cursor Plan mode — in Plan mode the agent creates a `.plan.md` file instead of asking questions. The Crafter must ask questions first and never create a plan file before Q&A is complete.

---

## Rule and references

- **Rule:** `.cursor/rules/context/plan-mode-prompt-crafter.mdc` (context rule, not a subagent).
- **Questions and order:** **Only** from [User-Questions-and-Options-Reference](../../User-Questions-and-Options-Reference.md) **§1 (Question-led Prompt Crafter)**. Param order by branch in [Prompt-Crafter-Param-Table](../../Prompt-Crafter-Param-Table.md); exact wording and sequence from §1.
- **Structure and protocol:** [Prompt-Crafter-Structure-Detailed](../../Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md), [Prompt-Crafter-Implementation-Notes-V4](../../Prompt-Crafter-Implementation-Notes-V4.md) (resume gate, profile gate, lock precedence, session safety).

---

## Flow overview

1. **Load questions reference** — Read User-Questions-and-Options-Reference.md §1. If unreadable → FAIL; do not proceed.
2. **Load schema and scratchpad** — Queue-Sources, Parameters, Second-Brain-Config (prompt_defaults), crafting.tmp_prompt_path, crafting.max_reasoning_sentences. Load or initialize tmp-prompt scratchpad (e.g. `.technical/tmp-prompt.json`). If scratchpad is corrupt → abort with clear error; do not auto-repair.
3. **Mid-session (V4)** — If scratchpad has an unfinished session (e.g. rail_index < rail length), offer: resume from next step, start fresh, or show summary then decide. If start fresh, do not overwrite scratchpad until the new run completes or is cancelled.
4. **Kickoff** — If user did not specify CODE or ROADMAP, ask **Q0** ("Which kind?" A. CODE / B. ROADMAP). Otherwise skip Q0.
5. **Mode-narrowing** — Ask the mode-narrowing question(s) from §1 for the chosen branch (CODE: e.g. INGEST / ORGANIZE / Other; ROADMAP: ROADMAP MODE setup / RESUME-ROADMAP). For **RESUME-ROADMAP**, before params 2–18 run **resume gate** (if prior RESUME session with locks: offer keep locks / discard) and **profile gate** (keep / switch / default / defer profile). Lock precedence: explicit_choices always win over profile or Config.
6. **Param questions (A/B/C)** — For each param in "Param order by branch" for the current branch: if not already fixed by scratchpad locks (resume gate), ask **exactly one question per message** with options **A.**, **B.**, **C.** only. Record A → explicit_choices + payload; B/C → omit key (C also appends to agent_reasoning_log). No skips; optional = whether user includes the param, not whether the question is asked.
7. **Resolve C** — After all optionals, resolve C semantics; write reasoning only to agent_reasoning_log and payload `agent_reasoning` (never into user_guidance).
8. **Manual text phase** — For every param that was included (A) and has **accepts_manual_text** true, ask "What is the [param name]?" in §1 order (e.g. project_id, source_file for ROADMAP MODE; source_file for CODE modes). One per message; wait for answer.
9. **Summary and Final question** — Present assembled payload (mode + params; lock precedence; agent_reasoning separate from user_guidance). **Always** ask the **Final question** from §1: "Append to queue?" — A. yes (append) | B. no (cancel) | C. AI reasoning. Do **not** append without asking.
10. **If user confirms (A / yes)** — Validate payload; route per Queue-Sources: append to **Task-Queue.md** only if mode is one of TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT; **otherwise** append to **`.technical/prompt-queue.jsonl`**. For **RESUME-ROADMAP** append: read prompt-queue.jsonl, **remove all lines** whose parsed `mode === "RESUME-ROADMAP"` (keep others), then append the new line. Read full file → append one newline + one JSONL line → write back. Commit scratchpad; output session-end message; **end session** (no follow-up questions).
11. **If user declines (B / no)** — Do not write to any file. Payload remains in chat/plan for copy-paste.

---

## Key points

- **No .plan.md** — The Crafter does not create or write a plan document before Q&A is complete. Plan mode is disabled for this flow.
- **One question per message** — Format with real line breaks; options A., B., C. on separate lines so Cursor can show the question box with click-to-answer.
- **Session end** — After a successful append, the agent outputs the standard closing message ("Queued successfully… Run EAT-QUEUE… Crafting session complete. If you need another one, just say 'We are making a prompt' again.") and does not ask follow-up questions. To craft a RESUME-ROADMAP entry after a ROADMAP MODE setup, the user starts a **new** crafting run and chooses RESUME-ROADMAP.
- **Laptop-only** — Queue writes are from the laptop only. Mobile = observe + fill Ingest; crafting is not run from mobile.

---

## Fail conditions

- Cannot read User-Questions-and-Options-Reference.md §1 → FAIL; report and stop.
- Skips any question §1 requires for the branch → FAIL.
- Skips or reorders params → FAIL.
- Skips the Final "Append to queue?" question → FAIL.
- Creates or writes a .plan.md file before Q&A complete → FAIL.

---

## References

- [User-Questions-and-Options-Reference](../../User-Questions-and-Options-Reference.md) §1
- [Queue-Sources](../../Queue-Sources.md) § Plan-mode queue routing, Task-Queue structure, Remove stale on RESUME-ROADMAP append
- [Prompt-Crafter-Param-Table](../../Prompt-Crafter-Param-Table.md)
- [Prompt-Crafter-Implementation-Notes-V4](../../Prompt-Crafter-Implementation-Notes-V4.md)
- `.cursor/rules/context/plan-mode-prompt-crafter.mdc`
