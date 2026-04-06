---
name: Pass 3 contract clarity
overview: Add a concise, operator-facing guide (with mermaid visuals) on why EAT-QUEUE Pass 3 often appears to do nothing when a repair line already exists on the prompt queue, aligned with queue.mdc A.5.0 — docs-only unless you later opt into a spec RFC.
todos:
  - id: add-pass3-doc
    content: Create 3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Pass-3-Operator-Guide.md with visuals (mermaid), entry conditions, pending-flag sources, anti-pattern, ordering, telemetry, remediation (incl. Grok immediate-remediation block).
    status: pending
  - id: crosslink-queue-sources
    content: Add short misconception callout + link in Queue-Sources.md (roadmap multi-dispatch / Pass 3 area).
    status: pending
  - id: crosslink-validator-spec
    content: Add one sentence + link in Validator-Tiered-Blocks-Spec.md Pass 3 bullet.
    status: pending
  - id: index-docs-readme
    content: Add row to 3-Resources/Second-Brain/Docs/README.md Document map (User-Flows table) next to EAT-QUEUE-Flow; optional Pipelines touch if needed.
    status: pending
  - id: optional-queue-mdc
    content: "Optional: one See-also line in queue.mdc A.5.0 + sync .cursor/sync/rules/agents/queue.md + changelog if edited."
    status: pending
isProject: false
---

# Pass 3 operator clarity (documentation plan)

## Problem statement

Validated analysis (Grok + line-level check against `[queue.mdc](.cursor/rules/agents/queue.mdc)`):

- **Pass 3** runs only when `**(inline_a5b_repair_drain_enabled !== false && inline_repair_pending)`** OR `**(inline_forward_followup_drain_enabled === true && inline_forward_followup_pending)`** (see **A.5.0** ~lines 305–306).
- `**inline_repair_pending`** is set by **same-run events** (repair-class mid-run append via **A.5b**, **A.5d** `recovery_auto_append`, PromptCraft success path, etc. — ~lines 260, 409, 425, 543), **not** because a repair JSONL row was already on disk at run start.
- `**repair_first`** can leave a **pre-existing** repair line **non-dispatchable** for that project if a **forward-class** line wins the single **initial_pass** slot (~lines 254–255).

Existing docs mention Pass 3 in places (`[Validator-Tiered-Blocks-Spec.md](3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md)`, `[Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)`, `[Parameters.md](3-Resources/Second-Brain/Parameters.md)`) but the **intuition trap** (“repair already in PQ → Pass 3 must drain it”) is easy to miss.

## Placement and filename (Grok rec)

- **Path:** `[3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Pass-3-Operator-Guide.md](3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Pass-3-Operator-Guide.md)` — same folder as `[EAT-QUEUE-Flow.md](3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Flow.md)`.
- **Reason:** `[Docs/README.md](3-Resources/Second-Brain/Docs/README.md)` positions **User-Flows/** as operator journeys around queue processing; discoverable via backbone index and **Docs** map.

## Recommended approach (docs-only)

### 1. Add the operator guide (content + visuals)

Create the file above with:

- **What Pass 3 is:** combined inline drain after passes 1–2, with optional forward follow-up when enabled.
- **Entry condition:** pending flags + Config gates (mirror **A.5.0** wording; cite `[queue.mdc](.cursor/rules/agents/queue.mdc)` **A.5.0** / **Pass 3 re-tag**).
- **Anti-pattern box:** “Pre-existing repair line on `prompt-queue.jsonl` does **not** set `inline_repair_pending` by itself.”
- **Where pending is set:** bullet list: **A.5b** repair append, **A.5d** repair recovery append, PromptCraft append path (cross-link to **A.5b** / **A.5d** sections in `queue.mdc` by heading).
- **Ordering:** short paragraph on `**repair_first`** vs `**forward_first`** and why a repair row may not run in pass 1/2 (pointer to **A.4c**).
- **Telemetry:** `queue_pass_phase=inline_skipped_no_slots`, `inline_drain_incomplete`, stall-skip family — pointers to `[Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` observability and `[Logs.md](3-Resources/Second-Brain/Logs.md)`.
- **Remediation (operator):** adjust `**queue.roadmap_pass_order`** / caps / lane; use `[Python-Queue-Orchestrator.md](3-Resources/Second-Brain/Docs/Python-Queue-Orchestrator.md)` full-cycle when applicable.
- **Immediate remediation (Grok — include verbatim for completeness):**
  - **Immediate remediation:** Run another **EAT-QUEUE** after any mid-run append (the new repair line will be tagged in the next Pass 1–2 if it wins the slot). For stubborn stalls, temporarily set `queue.inline_a5b_repair_drain_enabled: true` and `queue.inline_forward_followup_drain_enabled: true` in `Second-Brain-Config.md` (balance or extreme profile), then re-run.

Keep prose under ~2 screens where possible; link out for full spec.

### 2. Visuals (required — user asked for graphs)

Include **at least two** Mermaid diagrams in the guide (Obsidian/Cursor render Mermaid in preview):


| Diagram                                    | Purpose                                                                                                                                                                                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A — Pass 3 gate**                        | Decision: repair/forward pending flags + Config vs skip Pass 3; branch “mid-run append sets pending” vs “stale repair row only → no pending”. Use `flowchart` / node IDs without spaces; quote edge labels if they need punctuation.    |
| **B — repair_first slot (intuition trap)** | One **initial_pass** roadmap slot per project under default **repair_first**; show forward line consuming the slot while an older repair row waits (non-dispatchable that pass). Optional third mini-diagram only if it stays readable. |


Cross-reference diagrams from the “Anti-pattern” and “Ordering” sections so the doc stays scannable.

### 3. Wire the map (lightweight cross-links)

- Add a **short “Common misconception”** subsection or callout in `[Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` under **Roadmap multi-dispatch** / generate-eat parity — **one paragraph + link** to the new guide.
- In `[Validator-Tiered-Blocks-Spec.md](3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md)` § Pass 3 bullet (~line 119), add **one sentence + link**: pending flags are required; pre-existing rows alone are insufficient.

### 4. Backbone index

- Add a **Document map** row in `[3-Resources/Second-Brain/Docs/README.md](3-Resources/Second-Brain/Docs/README.md)` next to **User-Flows/EAT-QUEUE-Flow** (User-Flows table in “Document map”).
- Per `[backbone-docs-sync.mdc](.cursor/rules/always/backbone-docs-sync.mdc)`, touch parent index if your workflow also mirrors `[Pipelines.md](3-Resources/Second-Brain/Pipelines.md)` — only if needed for discoverability.

### 5. Sync folder (if any rule text changes)

- If you **edit** `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)` (optional: one “See also” under **A.5.0** → new guide), update `[.cursor/sync/rules/agents/queue.md](.cursor/sync/rules/agents/queue.md)` and `[.cursor/sync/changelog.md](.cursor/sync/changelog.md)`.

### 6. Optional cross-link from EAT-QUEUE-Flow

- One sentence + link at the end of `[EAT-QUEUE-Flow.md](3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Flow.md)` pointing advanced readers to Pass 3 semantics (keeps the main flow short).

## Out of scope (unless you request a follow-up)

- **Behavior change:** optional Config to set `inline_repair_pending` from “orphan repair rows” — **spec RFC** (A.4c / A.7 / audit impact).
- **Python harness:** contract tests in `scripts/eat_queue_core` — **separate** task.

