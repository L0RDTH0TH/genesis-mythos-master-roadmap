---
name: prompt-crafter-v2-param-meta-and-shielding
overview: Redesign the question-led prompt crafter to emit an optional param_meta overlay for CODE and ROADMAP params and harden rules so sensitive triggers never partially apply without a full, valid Q&A run.
todos: []
isProject: false
---

## Prompt Crafter v2 — Param Meta + Shielding

### Objectives

- **Expose param semantics to chat/agents** by adding a machine-readable `param_meta` overlay (descriptions + defaults) for all CODE and ROADMAP params.
- **Keep queue behavior stable**: existing payload schema, modes, and processors remain unchanged; `param_meta` is advisory and ignorable.
- **Harden the rules around the sensitive prompt-crafter trigger** so that partial or accidental activations cannot write to the queue or mutate roadmap state.

### 1. Define the v2 output contract

- **Primary payload unchanged**
  - Preserve the current JSONL line structure for prompt-crafter outputs (e.g. `{ mode, params: { ... } }`).
  - Do not rename params, do not change their types, and do not alter how the queue processor reads them.
- **Add optional `param_meta` overlay**
  - Specify a parallel object in the spec, e.g.:
    - `param_meta: { <paramName>: { description: string, defaultWhenC: string, usedBy?: string } }`.
  - Keys MUST match param names from `Prompt-Crafter-Param-Table.md`.
  - Mark `param_meta` as **advisory only**: queue processors and pipelines must treat it as read-only decoration, safe to ignore.
- **Document invariants**
  - A valid v2 payload = a v1 payload **plus optional** `param_meta`.
  - Any consumer that does not know about `param_meta` continues to function without change.

### 2. Map all CODE and ROADMAP params to descriptors

- **Collect param universe**
  - From `User-Questions-and-Options-Reference.md` §1 "Param order by branch" and `Prompt-Crafter-Param-Table.md`, list all params for:
    - ROADMAP MODE (setup): `project_id`, `source_file`.
    - RESUME-ROADMAP: `action`, `project_id`, `phase`, `sectionOrTaskLocator`, `enable_context_tracking`, `enable_research`, `research_queries`, `async_research`, `research_distill`, `handoff_gate`, `min_handoff_conf`, `inject_extra_state`, `token_cap`, `max_depth`, `branch_factor`, `profile`, `userText`, `queue_next`.
    - CODE → INGEST, ORGANIZE, DISTILL, EXPRESS, ARCHIVE, Task modes (all params from the param table).
- **Draft concise semantics and defaults**
  - For each param, define:
    - **What it does** in one short phrase/sentence (enough for a user-facing tooltip).
    - **Default when C / omitted** — explicitly reference existing behavior (e.g. use prompt defaults, disable feature, or no-op).
  - Ensure all defaults match `Parameters.md` and `Queue-Sources.md`; where behavior is deprecated (e.g. `async_research`), mark clearly as such.
- **Add a descriptors section for agents**
  - Extend `User-Questions-and-Options-Reference.md` with a `### Param descriptors (for agents)` subsection:
    - Group rows by branch (ROADMAP MODE, RESUME-ROADMAP, CODE sub-modes).
    - Columns: **param**, **Used in**, **It does**, **Default when C / omitted**.
  - Note that agents use these descriptors to populate `param_meta` and to render "It does …" explanations while asking questions.

### 3. Update rules to accept v2 output safely

- **Prompt-crafter rules: v2 support**
  - In the always/context rules that govern prompt crafting:
    - Explicitly describe the v2 payload shape (primary payload + optional `param_meta`).
    - State that validation and queue writes depend **only** on the primary payload; `param_meta` must not affect correctness.
    - Clarify that missing or partially filled `param_meta` is never an error condition.
- **Strengthened fail conditions**
  - Extend existing failure cases (skipped question, wrong wording, missing Final question) so that:
    - Even if `param_meta` is present and well-formed, any violation of the Q&A contract yields a **hard abort with no writes**.
    - The agent may still present a human-readable preview (including descriptors) but must not append to `.technical/prompt-queue.jsonl` or `Task-Queue.md`.
  - Add an explicit invariant to the rule text:
    - "Queue append and RESUME-ROADMAP stale-removal are allowed only when the run both (a) satisfies all Q&A requirements and (b) produces a valid primary payload; `param_meta` alone never authorizes writes."

### 4. Harden the trigger and shielding behavior

- **Clarify the sensitive trigger**
  - Keep existing trigger phrases (e.g. "We are making a prompt", "We are making a CODE prompt", "We are making a ROADMAP prompt").
  - Document that these phrases enter a **strict mode**: either the agent can honor the full Q&A contract, or it must decline and stay in regular chat.
- **Shield against partial activations**
  - Add rule language:
    - If at any point the agent detects that the flow cannot continue as strict prompt crafting (e.g. user diverges into general chat, system context missing), it must:
      - Exit prompt-crafter mode.
      - Treat the rest of the exchange as normal chat.
      - Optionally use param descriptors informally (explanations only), but **never emit or partially apply** a prompt-crafter queue payload.
  - Make this explicit in the Fail conditions section as a required behavior rather than a best-effort heuristic.

### 5. Guidance for agents using v2

- **How to populate `param_meta`**
  - When assembling a v2 payload, agents:
    - Copy the chosen param values into `params` exactly as before.
    - Optionally, construct `param_meta` from the descriptors section, filling in `description` and `defaultWhenC` for each param that appears in `params`.
  - For agents that do not need param-by-param help, allow emitting no `param_meta` at all.
- **How to talk to the user**
  - Encourage agents, when asking each A/B/C question, to:
    - Use the existing "It does …" line backed by the descriptor.
    - Optionally summarize the default for C ("If you choose C, I will …").
  - Make clear that this is a **presentation enhancement only**; underlying decisions, thresholds, and queue modes come from the same sources as v1.

### 6. Maintenance and shields against drift

- **Sync checklist for future param changes**
  - Document a short checklist (in either `User-Questions-and-Options-Reference.md` or `Prompt-Crafter-Param-Table.md`):
    - When adding/updating a param, you must:
      1. Update `Prompt-Crafter-Param-Table.md` (parentage, used_by, question_order, accepts_manual_text).
      2. Update the descriptors table (It does, Default when C / omitted).
      3. Ensure it is present in the appropriate branch in `User-Questions-and-Options-Reference.md` §1.
      4. If defaults or behavior changed, update `Parameters.md` / `Queue-Sources.md` first, then sync descriptors.
    - Only after all four steps are complete should agents rely on the param.
- **Drift detection mindset**
  - Recommend periodic manual or scripted checks that:
    - Every param in `Prompt-Crafter-Param-Table.md` has a corresponding descriptor row.
    - Every descriptor row maps to a known param and branch.
  - Treat discrepancies as high-priority doc bugs, since they can mislead both human users and agents even if runtime behavior is unchanged.

### Todos

- **collect-params-v2**: Enumerate all CODE/ROADMAP params from the existing docs, mark any that are deprecated or special-case.
- **design-param-meta-schema**: Finalize the `param_meta` object shape and write it into the rules/spec.
- **draft-descriptor-text**: Write concise "It does" and "Default when C" text for every param.
- **insert-descriptor-section**: Add the param descriptors section and overlay contract to `User-Questions-and-Options-Reference.md`.
- **update-rules-v2**: Update the prompt-crafter rules to describe v2 payloads, strict trigger behavior, and strengthened fail conditions.
- **sync-supporting-docs**: Align `Prompt-Crafter-Param-Table.md`, `Parameters.md`, and `Queue-Sources.md` with the new descriptors and defaults checklist.

