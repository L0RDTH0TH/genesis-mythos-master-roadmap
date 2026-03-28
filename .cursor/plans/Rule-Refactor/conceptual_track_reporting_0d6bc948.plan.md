---
name: Conceptual track reporting
overview: "Align **observable behavior** with the already-documented policy: conceptual completion does not require execution closure (rollup/REGISTRY-CI/HR). Changes focus on **mandatory reporting** (Watcher-Result + validator reports), and **turning off or redefining** the one rule that still **pushes** execution artifacts on conceptual (`A.5b.5` + Config)."
todos:
  - id: queue-watcher-messaging
    content: "Update queue.mdc A.5b.0 / A.6: mandatory VALIDATE message prefix for conceptual + execution-deferred primary_codes; mixed-code wording"
    status: completed
  - id: validator-report-banner
    content: "Update validator.mdc roadmap_handoff_auto: conceptual-track report banner + mixed-case clarification"
    status: completed
  - id: config-a5b5
    content: Set conceptual_force_build_on_repeated_gap false (and/or rewrite A.5b.5 to forbid execution artifact force on conceptual)
    status: completed
  - id: docs-sync
    content: Document contract in Queue-Sources or Parameters; optional Gate-Catalog pointer; sync .cursor/sync + changelog
    status: completed
isProject: false
---

# Migrate conceptual-track behavior (reporting + anti-churn)

## Problem

- **Policy is written** ([Dual-Roadmap-Track](3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md), [Roadmap-Gate-Catalog-By-Track](3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track.md)): on `effective_track === conceptual`, execution-shaped gaps (`missing_roll_up_gates`, `safety_unknown_gap`, REGISTRY-CI, HR, etc.) are **informational**, not the bar for conceptual completion.
- **Runtime still *feels* wrong** because:
  1. **[Watcher-Result](3-Resources/Watcher-Result.md)** lines lead with `medium/needs_work; primary_code missing_roll_up_gates` (same “checklist failed” tone every run).
  2. **[Second-Brain-Config](3-Resources/Second-Brain-Config.md)** has `conceptual_force_build_on_repeated_gap: true` and `medium_gap_escalation_threshold: 1`, which drives **[queue.mdc A.5b.5](.cursor/rules/agents/queue.mdc)** to escalate into **named rollup/CI/registry artifact directives**—i.e. it **actively chases** execution closure on conceptual, contradicting the advisory frame.

## Target behavior

- **Validators may still emit** full handoff reason codes for traceability (verbose logs, reports under `Validator-Reports/`).
- **Human-facing surfaces** must **lead** with: execution-deferred = **advisory**, **not** conceptual completion criteria—so Watcher does not sound like repeated failure.
- **No default auto-escalation** on conceptual that forces building rollup/registry/CI evidence **unless** the operator explicitly wants that path (Config off or narrowed).

## Implementation plan

### 1. Mandatory Watcher-Result phrasing (Layer 1)

**File:** [.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)

- Under **A.5b.0** (conceptual + execution-only primary) and **A.6 → Validator messaging**, replace the soft “note *advisory* when helpful” with a **hard requirement** for the **segment `VALIDATE`** line when **all** of the following hold:
  - `effective_track === conceptual`
  - Post–little-val verdict is **needs-work-only** (not hard block per existing A.5b definition)
  - Resolved `primary_code` is in `queue.conceptual_skip_auto_repair_primary_codes` (today: `missing_roll_up_gates`, `safety_unknown_gap`)

**Message template (lead string):** Require an explicit prefix such as:  
`execution-deferred (advisory); out of scope for conceptual completion —`  then the existing severity/primary_code/report path.

- **Mixed codes:** When `reason_codes` includes a **hard-block** code **and** execution-deferred codes, message must **first** state the hard-block outcome, then a short clause that execution-deferred codes remain advisory on conceptual (avoid implying rollup gates block conceptual progress).

### 2. Validator report banner (Layer 2)

**File:** [.cursor/rules/agents/validator.mdc](.cursor/rules/agents/validator.mdc) — `roadmap_handoff_auto` section (~lines 202–217)

- When `effective_track === conceptual` and the **only** blocking-class findings are execution-shaped (rollup/registry/CI/junior bundle rows per [Roadmap-Gate-Catalog-By-Track](3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track.md)), require a **visible one-line banner** near the top of the written report, e.g. “Execution-deferred — advisory on conceptual track; not required for conceptual completion.”
- When **mixed** (coherence block + execution codes), banner clarifies which family is gate vs advisory.

### 3. Stop (or redefine) conceptual “force build” escalation

**Files:** [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md), [.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc) **A.5b.5**

- **Preferred minimal fix:** Set `conceptual_force_build_on_repeated_gap: false` and raise `medium_gap_escalation_threshold` (e.g. 4+) if re-enabled later, so conceptual runs do **not** auto-escalate into rollup/CI artifact construction.
- **Rule fix (if keeping any escalation):** Rewrite **A.5b.5** bullet that names `G-P4.1-ROLLUP-GATE-02`, CI registry stubs, etc., so that on `**effective_track === conceptual`** escalation **never** mandates execution artifacts; optional alternatives: deepen to next structural target, decisions-log deferral line, or Conceptual-Amendments scaffold only.

### 4. Docs and sync

- **[Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)** or **[Parameters.md](3-Resources/Second-Brain/Parameters.md):** one short subsection documenting the **Watcher-Result prefix** contract and Config knobs (`conceptual_skip_auto_repair_primary_codes`, `conceptual_force_build_on_repeated_gap`).
- **[Roadmap-Gate-Catalog-By-Track.md](3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track.md):** add a bullet under “Verbose logging (conceptual)” pointing to Watcher + validator banner as **human framing** (not new gates).
- **Backbone sync:** mirror [.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc) → [.cursor/sync/rules/agents/queue.md](.cursor/sync/rules/agents/queue.md) and [.cursor/rules/agents/validator.mdc](.cursor/rules/agents/validator.mdc) → sync per [backbone-docs-sync.mdc](.cursor/rules/always/backbone-docs-sync.mdc); append [.cursor/sync/changelog.md](.cursor/sync/changelog.md) one line.

## Non-goals (this pass)

- Changing **little-val** structural checks or removing execution codes from validator **outputs** entirely (traceability stays useful).
- Reworking **gate_streak** / `queue-gate-compute.py` math unless you want a follow-up to avoid “gate block” spin from advisory codes alone.

## Verification

- After edits, a conceptual RESUME_ROADMAP run that only surfaces `missing_roll_up_gates` should produce Watcher **VALIDATE** lines that **start** with the execution-deferred framing, not raw `needs_work` alone.
- With `conceptual_force_build_on_repeated_gap: false`, repeated conceptual runs should **not** append repair lines that demand rollup/CI builds by default.

