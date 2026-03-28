---
name: Plan-mode Q&A-first and queue append
overview: Migrate Plan-mode prompt crafting so (1) all questions are asked and answered in conversation before any plan document or queue write, (2) the agent may then output a plan that tracks Q&A and shows the crafted payload at the bottom, and (3) the agent must append the payload to the queue (prompt-queue.jsonl or Task-Queue.md) after confirmation.
todos:
  - id: rule-plan-mode-crafter
    content: Update plan-mode-prompt-crafter.mdc with order invariant, step 7 (summary + Append? Y/n, validate, route, read-append-write), invariants (single write, no write on decline, read-then-append), routing table, Defenses cross-ref, description.
    status: completed
  - id: doc-prompt-crafter-detailed
    content: Update Prompt-Crafter-Structure-Detailed.md Protocol (8) and Funnel/Output for Q&A before plan/queue and append after confirm.
    status: completed
  - id: doc-chat-prompts
    content: Update Chat-Prompts.md Plan-mode crafting flow with Append? (Y/n), confirm/decline behavior.
    status: completed
  - id: doc-rules
    content: Update Rules.md context table row for plan-mode-prompt-crafter (Q&A first, append after confirm).
    status: completed
  - id: doc-queue-sources
    content: Add to Queue-Sources.md Plan-mode routing table, Task-Queue.md structure, validation/decline/read-then-append.
    status: completed
  - id: doc-vault-layout
    content: Optional one-line pointer in Vault-Layout.md to Queue-Sources for Task-Queue and Plan-mode append.
    status: completed
  - id: sync-rule-and-changelog
    content: Mirror .mdc changes to .cursor/sync/rules/context/plan-mode-prompt-crafter.md; add changelog entry with defenses.
    status: completed
  - id: doc-backbone
    content: Optional one-line note in Backbone.md that Plan-mode appends to queue after confirm.
    status: completed
isProject: false
---

# Plan-mode Q&A-first and queue append migration

## Target behavior (strict order)

```mermaid
sequenceDiagram
  participant User
  participant Agent
  Note over Agent: No plan file, no queue write
  User->>Agent: "We are making a prompt"
  Agent->>User: Which kind? A. CODE B. ROADMAP
  User->>Agent: B (ROADMAP)
  Agent->>User: Setup or continue? A. ROADMAP MODE B. RESUME-ROADMAP
  User->>Agent: B
  Agent->>User: [Ask each optional in param table order, A/B/C + "It does ..."]
  User->>Agent: [Answer each]
  Agent->>User: [Manual text phase for any included text params]
  User->>Agent: [Confirm each]
  Note over Agent: All Q&A complete
  Agent->>Agent: Resolve C choices
  Agent->>User: Summary + optional plan (questions/choices + payload at bottom). Append to queue? (Y/n)
  alt User confirms
    User->>Agent: Y
    Agent->>Agent: Validate payload; route to file; read file; append one line; write back
    Agent->>User: Done. Payload appended to queue.
  else User declines
    User->>Agent: n / skip / copy only
    Agent->>User: Payload not appended. Copy from above or add manually.
  end
```



- **Before** the "Summary + optional plan" step: no plan document, no write to any queue file.
- **After** user confirms: (1) optionally output a plan that lists questions asked and choices made, with the crafted payload at the bottom; (2) **must** append the payload to the correct queue file.

---

## Defenses (five gaps)

**1. Task-Queue.md structure and append location**

- **Canonical structure** (document in [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) or [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md)): Optional YAML frontmatter (`---` … `---`), then optional `# Task Queue` (or similar) heading, then **body**: one JSON object per line. Queue entries are **lines in the body only**; do not insert inside frontmatter or inside a heading line.
- **Append rule**: Agent must append the new JSONL line **after the last line of the body** (i.e. after the closing `---` of frontmatter and any heading/content; if the file has only frontmatter and a heading, append after the heading line with a newline, then the JSON line).
- **File missing**: If Task-Queue.md or prompt-queue.jsonl does not exist, create it with minimal parseable structure so auto-eat-queue / auto-queue-processor can read it later. For **Task-Queue.md**: e.g. `---\n---\n\n` (empty frontmatter + body) or `# Task Queue\n\n` then the JSON line; body = lines after the first `---\n---`. For **prompt-queue.jsonl**: write only the single JSON line (no leading newline). Do not write content inside frontmatter.
- **Reference**: Current [3-Resources/Task-Queue.md](3-Resources/Task-Queue.md) is frontmatter + `# Task Queue` + empty body; append goes after `# Task Queue` (and any existing JSON lines in body).

**2. Validation before append**

- Before writing to any queue file, the agent must **validate** the assembled payload: (a) `mode` is present and a non-empty string; (b) `mode` is one of the known modes (per Queue-Sources: INGEST MODE, RESUME-ROADMAP, TASK-ROADMAP, etc.); (c) if `params` is present, it is an object (no array or primitive); (d) payload serializes to valid one-line JSON.
- If validation fails: **do not append**. Surface a short error (e.g. "Payload invalid: [reason]. Fix and confirm again, or copy payload below to add manually.") and leave the payload in the summary/plan for user correction. Optionally align with [sb_contracts/queue.py](3-Resources/Second-Brain/tests/sb_contracts/queue.py) `parse_queue_line` / `validate_entry` semantics so the same contract applies at append time.

**3. Explicit routing rule (which file)**

- **Routing table** (add to the rule and to Queue-Sources so the agent does not re-interpret each time):
  - **Append to `3-Resources/Task-Queue.md`** if and only if `mode` is one of: **TASK-ROADMAP**, **TASK-COMPLETE**, **ADD-ROADMAP-ITEM**, **EXPAND-ROAD**, **REORDER-ROADMAP**, **DUPLICATE-ROADMAP**, **MERGE-ROADMAPS**, **EXPORT-ROADMAP**, **PROGRESS-REPORT**.
  - **Otherwise append to `.technical/prompt-queue.jsonl`** (all other modes, e.g. INGEST MODE, RESUME-ROADMAP, DISTILL MODE, EXPRESS MODE, ORGANIZE MODE, ARCHIVE MODE, RESEARCH-AGENT, SEEDED-ENHANCE, etc.).
- No other files. Document this table in [plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc) step 7 and in Queue-Sources § "When to use which" or a new "Plan-mode queue routing" bullet.

**4. User declines append**

- If the user **declines** to append (e.g. "no", "skip", "don't add to queue", "copy only"): **do not write** to any queue file. The payload remains in the summary and/or plan output for copy-paste or manual addition. Tell the user: "Payload not appended. You can copy it from above or add it manually to the queue file."
- Only on explicit confirm (e.g. "Y", "yes", "append", "add to queue") does the agent perform the append.

**5. Read-then-append safety**

- **Invariant**: Queue append must be **read current contents → append exactly one newline + one JSONL line → write back**. The agent must never overwrite the file without preserving all existing lines.
- **Implementation**: Read the full file; if it is prompt-queue.jsonl, append `\n` + JSON line to the string; if it is Task-Queue.md, parse to locate end of body (after last `---` and any heading/content), then append `\n` + JSON line to the body; write the result. Do not replace the file with only the new line.
- **On failure**: If the append fails (e.g. path not writable, file locked, or write error): do not retry indefinitely. Report the error and leave the payload in the plan for manual paste or file creation; optionally log to [Errors.md](3-Resources/Errors.md) with pipeline `plan-mode-crafter`, stage `queue_append`.

---

## 1. Rule: [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)

Implement step 7 in line with the **Defenses** section above (validation, routing, decline behavior, read-then-append, Task-Queue structure).

**1.1 Order invariant (new)**

Add an explicit **"Q&A before plan or queue"** invariant:

- Do **not** create a plan document (outline, steps, todos) and do **not** append to the queue until **all** of the following are complete: kickoff resolved, mode narrowed, every optional asked and answered in param table order, C choices resolved, and manual text phase completed for every included text-accepting param.
- Only after that may the agent: present summary, optionally output a plan (questions + choices + payload at bottom), and append the payload to the queue.

**1.2 Behavior steps**

Keep steps 1–6 as-is (resolve kickoff → load schema → narrow mode → ask optionals → resolve C → manual text phase). Replace step 7 with:

- **Summary, plan (optional), and queue append**: Present the assembled payload for confirmation. Optionally output a plan that lists the questions asked and user choices (A/B/C and manual text), with the **crafted payload at the bottom**. Ask: "Append to queue? (Y/n)".
  - **If user declines (no / skip / copy only)**: Do not write. State that the payload is in the plan for copy-paste or manual add.
  - **If user confirms (Y / yes / append)**: (1) **Validate** payload (mode present and known, params object if present, valid JSON). If invalid, report error and do not append. (2) **Route** using the explicit table (Task-Queue.md only for TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT; else prompt-queue.jsonl). (3) **Read** current file contents, **append** exactly one newline and the JSONL line (for Task-Queue.md, append after body; see Defenses § Task-Queue structure), **write** back. If file is missing, create it (and parent for `.technical/`) with minimal structure. On write failure, report error and leave payload in plan; do not retry indefinitely. No other vault writes.

**1.3 Invariants section**

- Remove "Readonly: no direct vault writes" and "only emits a payload".
- Add: **Single allowed write**: The only vault write in this flow is **appending the crafted payload** (one JSONL line) to the queue file (prompt-queue.jsonl or Task-Queue.md). No other vault writes. Queue append happens only after all Q&A is complete and user confirms.
- Add: **No write on decline**: If the user declines to append (no / skip / copy only), do not write to any file; payload remains in plan for copy-paste.
- Add: **Read-then-append only**: Append = read full file → append one newline + one JSONL line → write back. Never overwrite the file with only the new line; preserve all existing lines.
- Keep: Queue and crafting are laptop-only; mobile = observe + fill Ingest.

**1.4 Description (frontmatter)**

Update the rule `description` to say: run Q&A first (all questions and answers before plan or queue); then optionally output plan (Q&A + payload at bottom) and **append** payload to queue after confirm.

---

## 2. Docs: [3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)

**2.1 Protocol (sequence)**

In the "Protocol (sequence)" bullet (around line 47):

- Insert after step (4): **"Do not create a plan document or append to the queue until steps (4)(5)(6) are complete."**
- Change step (8) from "Emit prompt/queue payload (readonly; no direct vault writes)" to: **"(8) Present summary for confirmation; optionally output a plan that lists questions and choices with the crafted payload at the bottom. After user confirms, append the payload as one line to `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md` as appropriate (see Queue-Sources). No other vault writes in this flow."**

**2.2 Funnel / Output**

- In the "Funnel" paragraph (around line 25): Add that the agent must **not** build a plan or write to the queue until all optionals and the manual text phase are finished; only then may it present summary, optional plan (Q&A + payload at bottom), and append to queue.
- In CODE funnel "Output" (around line 70): Change "One JSONL line for prompt-queue.jsonl or Task-Queue.md, plus optional ready-to-paste" to: "After Q&A complete: summary, optional plan (questions/choices + payload at bottom), then **append** one line to prompt-queue.jsonl or Task-Queue.md after user confirms."

---

## 3. Docs: [3-Resources/Second-Brain/Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md)

- In the Plan-mode crafting table (or the paragraph that describes the flow): State that all questions are asked and answered **before** any plan is produced or queue is written; then the agent may show a plan (Q&A + payload at bottom) and asks "Append to queue? (Y/n)". On **confirm**: validate, route, read-append-write. On **decline**: do not write; payload remains in plan for copy-paste or manual add.

---

## 4. Docs: [3-Resources/Second-Brain/Rules.md](3-Resources/Second-Brain/Rules.md)

- In the context table row for `plan-mode-prompt-crafter.mdc`: Update the responsibilities cell to say: Q&A first (no plan/queue until all questions answered); then optional plan (Q&A + payload at bottom) and append payload to queue after confirm. Only vault write = queue append.

---

## 5. Sync and backbone

- **[.cursor/sync/rules/context/plan-mode-prompt-crafter.md](.cursor/sync/rules/context/plan-mode-prompt-crafter.md)**: Apply the same Behavior and Invariants changes as in the .mdc so the sync copy matches.
- **[.cursor/sync/changelog.md](.cursor/sync/changelog.md)**: One entry: Plan-mode prompt crafter — Q&A must complete before plan or queue write; optional plan (Q&A + payload at bottom); must append payload to queue after confirm; only vault write = queue append.
- **Backbone / Parameters**: No change to crafted_params_conf_boost; optional one-line note in [3-Resources/Second-Brain/Backbone.md](3-Resources/Second-Brain/Backbone.md) that Plan-mode crafting appends to queue after Q&A and confirmation (if a "Prompt-Crafter" or "Queue" subsection exists).

---

## 6. Queue append mechanics and doc updates

- **How the agent appends**: Read file → append one newline + one JSONL line to body → write back (see Defenses § read-then-append and Task-Queue structure). No MCP tool; file read/write only.
- **Queue-Sources.md**: Add (1) **Plan-mode queue routing** — explicit table: Task-Queue.md for the nine task modes (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT); prompt-queue.jsonl for all other modes. (2) **Task-Queue.md structure** — frontmatter optional, then body (one JSON per line); Plan-mode crafter appends after last body line; when file is missing, minimal creation (e.g. `---` `---` + newline or `# Task Queue` + newline, then JSON line) so file stays parseable. (3) **Validation before append** — mode required and known; params object if present; valid one-line JSON. (4) **On decline** — no write; payload in plan for copy-paste. (5) **Read-then-append** — read file, append one newline + line, write back; never overwrite without preserving existing lines.
- **Vault-Layout.md** (optional): If Queue-Sources is the single source for queue format, a one-line pointer under .technical or 3-Resources that "Task-Queue.md body format and Plan-mode append rules: see Queue-Sources."

---

## 7. Optional: "No plan before Q&A" reminder in rule

- In the rule Body section, add one short sentence after the Behavior list: **"Order: Complete all of steps 1–6 (all questions asked and answered, C resolved, manual text done) before step 7. Do not create a plan or append to the queue until then."**

---

## Summary of file changes


| File                                                     | Change                                                                                                                                                                                                                                                        |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.cursor/rules/context/plan-mode-prompt-crafter.mdc`     | Order invariant; step 7 = summary + "Append? (Y/n)", confirm/decline, validate, route, read-append-write; invariants = single write = append only, no write on decline, read-then-append only; explicit routing table; Defenses cross-ref; description update |
| `Prompt-Crafter-Structure-Detailed.md`                   | Protocol step (8) and Funnel/Output: Q&A before plan/queue; append after confirm; optional plan format                                                                                                                                                        |
| `Chat-Prompts.md`                                        | Plan-mode description: Q&A first, then plan + queue append; on decline no write                                                                                                                                                                               |
| `Rules.md`                                               | Context table row: Q&A first, append to queue after confirm; validate before append                                                                                                                                                                           |
| `Queue-Sources.md`                                       | Plan-mode queue routing table (Task-Queue.md vs prompt-queue.jsonl by mode); Task-Queue.md body structure and append location                                                                                                                                 |
| `Vault-Layout.md`                                        | Optional: one-line pointer to Queue-Sources for Task-Queue structure and Plan-mode append                                                                                                                                                                     |
| `.cursor/sync/rules/context/plan-mode-prompt-crafter.md` | Mirror .mdc changes                                                                                                                                                                                                                                           |
| `.cursor/sync/changelog.md`                              | One changelog entry (include defenses: validation, routing, decline, read-then-append, Task-Queue structure)                                                                                                                                                  |
| `Backbone.md`                                            | Optional one-line note (Plan-mode appends to queue after confirm)                                                                                                                                                                                             |


No new skills or MCP tools; queue append is read then append one line then write back, with validation and routing per Defenses section.