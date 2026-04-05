---
name: Task proof wording patches
overview: Tightened proof-on-failure contract (single canonical section + short cross-refs), parallel-lane note, GitForge/tail Task proof, precise sync/changelog steps for dispatcher + system-funnels.
todos:
  - id: ssc-canonical-proof
    content: Add § Proof-on-failure (canonical); trim probe/guardrail/§6 to reference it
    status: completed
  - id: dispatcher-system-funnels
    content: Patch dispatcher.mdc + system-funnels.mdc (short refs + parallel + tail agents)
    status: completed
  - id: comms-spec
    content: Patch Task-Handoff-Comms-Spec (failed invocation; extend fallback_reason list)
    status: completed
  - id: queue-gitforge-optional
    content: Optional one-line in queue.mdc A.7a / agents/queue.md re GitForge proof (if not already implied)
    status: completed
  - id: dispatcher-rule-doc
    content: Replace stale legacy fallback in Docs/Rules/Dispatcher-Rule.md
    status: completed
  - id: sync-changelog
    content: Mirror dispatcher.mdc → sync/dispatcher.md; system-funnels.mdc → sync/system-funnels.md; changelog row
    status: completed
isProject: false
---

# Concrete wording patches: proof-of-failure for Task (revised)

## Design principles (iteration)

- **One canonical block** in Subagent-Safety-Contract defines proof requirements; dispatcher, system-funnels, Task-Handoff-Comms, and §6 guardrails **reference** it instead of repeating four full paragraphs.
- **Parallel / dual-lane:** When `parallel_execution` is on, proof records must land on the **same technical bundle** as the PQ that chat processed (per [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x** resolved paths). Multi-chat runs increase contention on JSONL — proof is **per chat**, not merged by narrative.
- **Tail agents:** **GitForge** (queue **A.7a**), **PromptCraft** (Layer 0 / **A.5d**), and any other post-queue `Task` use the **same** proof pattern as pipeline dispatch (comms + Errors on failure).
- **Sync:** Update **both** [.cursor/sync/rules/always/dispatcher.md](.cursor/sync/rules/always/dispatcher.md) and [.cursor/sync/rules/always/system-funnels.md](.cursor/sync/rules/always/system-funnels.md) to match the `.mdc` sources after edits; append **one** changelog row with the exact file list.

---

## 1. [3-Resources/Second-Brain/Subagent-Safety-Contract.md](3-Resources/Second-Brain/Subagent-Safety-Contract.md)

### 1a. New subsection **Proof-on-failure (normative)** — insert after **Task-`attempt-before-skip` invariant** (after ~line 75) or at start of **Task harden pass**

Single canonical text (keep this as the only long form):

```markdown
## Proof-on-failure (normative)

When any mandated `Task(subagent_type)` **does not complete successfully** (host rejection, tool error, timeout, or no `Task` tool in the session’s callable tool set):

1. **Do not** substitute inline pipeline or queue work as “success.”
2. **Record proof** before user-facing prose:
   - When **`task_handoff_comms.enabled`** is not **false**: append **`return_in`** for the same **`task_correlation_id`** as the preceding **`handoff_out`**, with **`body`** = verbatim or sanitized host/tool error, **or** the fixed attestation string below when no `Task` exists; set **`fallback_reason`** to **`task_tool_call_failed`** or **`task_tool_not_exposed_in_session`**.
   - Always append **Errors.md** per Error Handling Protocol: **`error_type`** = **`task_tool_launch_failed`** or **`task_tool_not_exposed_in_session`**; **Trace** = same error text or fixed string.
3. **Fixed attestation** (only when `Task` is not in the session tool set): `task_tool_not_exposed_in_session: no Task invocation possible in this chat tool set` — not a creative paraphrase.
4. **Applies to:** Layer 0 → `queue`; Layer 1 → pipelines; Layer 1 → post-queue **`gitforge`** / **`prompt_craft`**; Layer 2 → nested helpers — same pattern, appropriate `from_actor` / `subagent_type`.

**Parallel tracks:** Resolve `.technical/task-handoff-comms.jsonl` (and PQ) via the active track’s **`technical_bundle_root`** from **parallel_context** / **A.0x** so forensic rows sit next to the queue that run consumed.

Narrative-only claims of unavailability without (2) are **contract violations**.
```

### 1b. **Interpreting probe results** — short replacement (references § Proof-on-failure)

Replace current lines 147–151 with:

```markdown
- **Interpreting probe results**
  - **available:** `Task` probe call succeeds (ignore subagent prose).
  - **unavailable:** attempted `Task` failed and host error is in `raw_errors[type]` — see **Proof-on-failure** for what counts as proof.
  - **No-call path:** `Task` not in session tool set → use fixed `task_tool_not_exposed_in_session` string in `raw_errors[type]` and full **Proof-on-failure** logging.
  - Do not infer unavailability from docs, schema, or model narrative without (a) attempt outcome + `raw_errors` or (b) fixed attestation + Errors.md per **Proof-on-failure**.
```

### 1c. **Guardrail** (lines 161–164) — keep two bullets; **replace** any Layer 0 duplication with:

```markdown
  - Layer 0 and all tail launches: satisfy **Proof-on-failure** before asserting failure to the user.
```

### 1d. **§6 Guardrails** — **one** added bullet (drop separate “narrative phrases” if redundant with Proof-on-failure closing line):

```markdown
- Claims that `Task(...)` failed or was unavailable MUST be auditable via **Proof-on-failure** artifacts (`raw_errors`, comms `return_in`, or Errors.md trace).
```

---

## 2. [.cursor/rules/always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc)

### 2a. Queue step **4** — **short** form

```markdown
4. **Do not** read the prompt queue or Task-Queue yourself; **do not** run queue logic in this context. If `Task(subagent_type: "queue")` fails or cannot run, follow **[[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] § Proof-on-failure** (comms `return_in` when enabled + Errors.md + correct `fallback_reason`). When **parallel_context** / lane resolves a per-track **PQ**, use that track’s **`technical_bundle_root`** for **task-handoff-comms.jsonl** if your hand-off specifies it (see queue.mdc **A.0x**).
```

### 2b. **Other triggers** — one sentence

```markdown
Direct pipeline triggers without EAT-QUEUE: launch via `Task` + hand-off; on failure, **Proof-on-failure** as in Subagent-Safety-Contract (same Errors.md / comms rules).
```

### 2c. **PromptCraft block** (~line 65) — append

```markdown
On `Task(prompt_craft)` failure: **Proof-on-failure** (Subagent-Safety-Contract § Proof-on-failure); Layer 0 does not append PQ.
```

### 2d. **Delegation** bullet for Layer 1 — after GitForge sentence (~line 31), add

```markdown
- **`Task(gitforge)`** after **A.7a**: on failure, **Proof-on-failure**; GitForge failure MUST NOT roll back queue consumption (existing rule unchanged).
```

---

## 3. [.cursor/rules/always/system-funnels.mdc](.cursor/rules/always/system-funnels.mdc)

- Replace the “Task unavailable / call fails” fragment with: failures require **Proof-on-failure** (Subagent-Safety-Contract) before Watcher-Result / queue semantics; **no narrative-only** failure.
- Add **one** sentence: **Parallel lanes:** each chat/run uses its resolved **PQ** and matching **task-handoff-comms** path per **queue.mdc A.0x** / **parallel_context**; do not assume a single global JSONL when dual-track is enabled.

---

## 4. [3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec.md](3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec.md)

- Add `**## Failed or impossible Task invocation`** with **two** bullets: (1) always `return_in` + `fallback_reason` when comms enabled; (2) pointer to **Subagent-Safety-Contract § Proof-on-failure** (avoid duplicating the long list).
- In **Scope** table, add a row: **Layer 1 → `gitforge` (post A.7a)** | same comms pair | proof-on-failure on tail failure.
- Extend `**fallback_reason`** description: add `**task_tool_call_failed`**, `**task_tool_not_exposed_in_session`** for any Layer 0/1/tail launch.

---

## 5. [3-Resources/Second-Brain/Docs/Rules/Dispatcher-Rule.md](3-Resources/Second-Brain/Docs/Rules/Dispatcher-Rule.md)

Replace **Delegation and fallback** with compact Task-only + **Proof-on-failure** pointer (no legacy fallback). Optionally one line: parallel lanes → resolved comms path per queue **A.0x**.

---

## 6. Optional micro-add: [.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc) / [.cursor/agents/queue.md](.cursor/agents/queue.md)

If **A.7a** does not already say “log comms on GitForge failure”: add **one** sentence — failed `**Task(gitforge)`** → **Proof-on-failure** (Subagent-Safety-Contract); no queue rollback. **Only if** absent after grep.

---

## 7. Sync and changelog (precise)

**After all edits:**

1. **Convert/copy** [.cursor/rules/always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc) → [.cursor/sync/rules/always/dispatcher.md](.cursor/sync/rules/always/dispatcher.md) (sync copy mirrors `.mdc` body per [.cursor/rules/always/backbone-docs-sync.mdc](.cursor/rules/always/backbone-docs-sync.mdc); strip YAML frontmatter if the sync file uses plain markdown only — match existing `dispatcher.md` style in repo).
2. **Convert/copy** [.cursor/rules/always/system-funnels.mdc](.cursor/rules/always/system-funnels.mdc) → [.cursor/sync/rules/always/system-funnels.md](.cursor/sync/rules/always/system-funnels.md) the same way.
3. **Append** to [.cursor/sync/changelog.md](.cursor/sync/changelog.md) one row, e.g.:

`| <date> | Subagent-Safety-Contract, dispatcher.mdc, system-funnels.mdc, Task-Handoff-Comms-Spec, Dispatcher-Rule.md, sync dispatcher.md + system-funnels.md, changelog | — | Task proof-on-failure (canonical §); parallel lane comms path; GitForge/PromptCraft tail proof; remove legacy Dispatcher-Rule fallback text |`

**No** `.cursor/sync/` copies for `Subagent-Safety-Contract.md` or `Task-Handoff-Comms-Spec.md` (not under sync map unless you add them — default: do not).

---

## 8. Optional follow-ups

- Second-Brain-Config / Docs: recommend `**task_handoff_comms.enabled: true`** for production and parallel tracks.
- Nested-Subagent-Ledger-Spec: allowlist `**task_tool_not_exposed_in_session`** / `**task_tool_call_failed`** if enums exist.

---

## Dependency note

Still **policy-only**; forensic value is in **JSONL + Errors.md** when agents comply. Tighter wording reduces contradiction risk across files.