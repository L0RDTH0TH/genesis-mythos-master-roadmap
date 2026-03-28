---
name: Complete Validator Subagent (integrated)
overview: Full Validator subagent with validation-type dispatch, config-driven model selection, roadmap handoff as first type; integrated improvements — structured JSON + markdown report, severity tiers and auto-escalation, cross-reference prior artifacts, model fallback and telemetry, extensibility helpers, test harness, and doc polish.
todos: []
isProject: false
---

# Complete Validator Subagent Plan (Integrated)

## Goal

Build the **complete Validator subagent**: a dedicated hostile-review subagent that performs one or more **validation types**, with config-driven model selection (fixed model for high-stakes, e.g. Grok for roadmap handoff). **First type**: roadmap handoff (final pass when roadmap is complete → one handoff-readiness validation report). Design is extensible for future types (research synthesis, ingest classification, security scan). This plan integrates high-ROI improvements: structured JSON + markdown, severity tiers and escalation, prior-artifact cross-reference, model fallback, shared critique helpers, test harness, and doc polish.

---

## Part A — Validator subagent (generic)

### A.1 Role and contract

- **Name**: Validator subagent (ValidatorSubagent).
- **Role**: Run a **hostile senior engineer** pass on pipeline or artifact output: flag contradictions, overconfidence, missing edges, weak sourcing; produce a structured validation report or verdict.
- **Invocation**: Queue only (or direct trigger that enqueues). Never called by other subagents; queue is the single caller. **Terminal subagent** — no chaining, no chain_request.
- **Contract**: Per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md): hand-off includes task, telemetry block, state files, return format. Return: one-paragraph summary, **Success / failure / #review-needed** (explicit for queue and Run-Telemetry).
- **Read-only invariant**: Validator subagents **MUST** be read-only on input artifacts except the **explicit output path** (report note). No edits to phase notes, roadmap-state, or other inputs. Add this to Subagent-Safety-Contract.

### A.2 Validation types (concept)

Each **validation type** has: scope, inputs, output (report/verdict), and model (fixed or Auto from config). Validator receives `validation_type` + type-specific params in hand-off; branches on type; runs that check only (no pipeline execution).

### A.3 Config: validation types and model selection

**File**: [3-Resources/Second-Brain/Second-Brain-Config.md](3-Resources/Second-Brain/Second-Brain-Config.md)

```yaml
validator:
  roadmap_handoff:
    model: "grok-code"   # Cursor model id for Grok code; high-stakes → fixed model
  # Future: research_synthesis: { model: "grok-code" }; ingest_classification: { model: "auto" }
```

- **Parameters.md**: Add note — **high-stakes types use fixed models** (no sampling variance); **low-stakes** can use `"auto"` for cost.

### A.4 Hand-off shape (validator-specific)

- Task, telemetry block, **validation_type** (required), type-specific params, relevant state files, **output path**, critical invariants (read-only except output path).
- For **roadmap_handoff**: project_id (required), optional roadmap_dir, phase_range. Queue includes prior-artifact paths when present (see Part C.3).

### A.5 Validator agent rule (generic structure)

**New file**: [.cursor/rules/agents/validator.mdc](.cursor/rules/agents/validator.mdc)

- Branch by **validation_type**; unknown type → return failure, log to Errors.md.
- **roadmap_handoff** branch: run Part C check; emit **both** JSON summary and markdown report (see Part C.4–C.5).
- **Shared critique helpers** (for DRY and future types): In validator.mdc, document a small set of reusable prompt snippets or structured checks that branches can reference:
  - **check_contradictions(artifact_a, artifact_b)** — compare claims/goals across artifacts.
  - **check_sourcing_strength(claim_block)** — assess evidence (RFC, repo, blog-only).
  - **score_readiness(phase_content)** — readiness score 0–10 with gap list.
  Each new validation type can reuse these and add type-specific checks.

---

## Part B — Queue integration (generic)

### B.1 Mode and dispatch

- **ROADMAP_HANDOFF_VALIDATE**: params `project_id` (required), optional `phase_range`, optional `dry_run` (test harness).
- **Mode → subagent_type**: ROADMAP_HANDOFF_VALIDATE → **validator**. Canonical order: after HANDOFF-AUDIT (11c).
- **Dispatch**: Build hand-off with validation_type, project_id, state paths, **prior-artifact paths** (see C.3), output path (or Temp/ when dry_run). Read **model** from `validator.roadmap_handoff.model`; call the **Task** subagent tool with subagent_type **validator**, prompt = hand-off, **model** = that value.
- **Model fallback**: If configured model is unavailable (tool/config error), **fallback to "auto"** and record in Run-Telemetry: `model_used: "grok-code (fallback: auto)"` so traceability is preserved. Report note frontmatter: `model_used: "<actual>"` (config value or "auto").

### B.2 Pipeline list and Subagent-Safety-Contract

- system-funnels / dispatcher: add **validator** to the Task-tool pipeline list; note model pass from config.
- **Subagent-Safety-Contract**: (1) Validator is invoked with explicit **model** when validation type has a fixed model. (2) **Validator subagents MUST be read-only on input artifacts except the explicit output path.**

---

## Part C — Roadmap handoff validation check (first type)

### C.1 When it runs

- Queue mode **ROADMAP_HANDOFF_VALIDATE** with `project_id`. Optional **dry_run: true** → test harness (report to Temp/, JSON + markdown in Run-Telemetry).

### C.2 Inputs (from hand-off)

- project_id (required), optional roadmap_dir, phase_range.
- State files: roadmap-state.md, workflow_state.md, phase notes 1..current_phase, decisions-log.md.

### C.3 Cross-reference prior artifacts (improvement #3)

Queue **always includes** in hand-off when they exist:

- Latest **handoff-audit** output or report path (if a handoff-audit-report.md exists).
- Last **handoff-validation-report-*.md** (previous validator run).
- **decisions-log.md** excerpt (e.g. last 200 lines or filtered by project/phase).

Validator prompt addition:

- *"Compare against prior handoff-audit and previous validation reports. Flag **regressions** (issues fixed before but reappeared) or **ignored prior warnings**."*

Reduces "same gap flagged every time" loops.

### C.4 Severity tiers and auto-escalation (improvement #2)

Standardize issue types and severities:

| Type              | Severity   | Triggers auto-escalation hint? | Example |
|-------------------|------------|--------------------------------|---------|
| contradiction     | high       | Yes                            | Phase goal conflicts with master objective |
| overconfidence    | high/medium| Yes if high                    | Claim without sourcing or pseudo-code |
| missing_edge      | medium     | Yes                            | No acceptance criteria or migration path |
| weak_sourcing     | medium/low | No                             | Research claim with only blog, no RFC/repo |
| structural        | high       | Yes                            | No clear dependency graph or timeline |

- In **report**: group findings by severity; add **"Escalation recommended"** bullet when any high-severity issue exists.
- In **JSON**: `escalation_recommended: true/false` and list of trigger issue types. Enables future queue rules (e.g. verdict=review_needed and escalation_recommended → enqueue human-review task).

### C.5 Structured JSON + markdown report (improvement #1 — ship with MVP)

Every validation run produces **both**:

1. **Machine-readable JSON summary** (for automation, telemetry, Commander macros).
2. **Human-readable markdown report** (the main artifact).

**JSON schema** (emit in memory → write alongside report or embed key fields in report frontmatter):

```json
{
  "validation_type": "roadmap_handoff",
  "project_id": "abc123",
  "timestamp": "2026-03-15T19:16:00Z",
  "verdict": "success" | "failure" | "review_needed",
  "overall_readiness_score": 8.2,
  "phase_findings": [
    {
      "phase": "Phase 3",
      "readiness": "partial",
      "score": 6.5,
      "issues": [
        {
          "type": "contradiction",
          "severity": "high",
          "description": "...",
          "evidence": ["roadmap-state.md:42", "phase3.md:18"]
        },
        { "type": "overconfidence", "severity": "medium", "description": "..." }
      ]
    }
  ],
  "cross_phase_issues": [],
  "recommendations": ["Revisit Phase 2 cancellation handling", "..."],
  "escalation_recommended": true
}
```

- Validator: **write JSON first** → use it to generate markdown sections (DRY, single source of truth).
- **Report note frontmatter**: Include key fields — `verdict`, `overall_readiness_score`, `escalation_recommended`, `model_used`, `issue_counts` by severity (e.g. high: 2, medium: 3) for quick Dataview/overview.
- **Benefit**: Auto-triage (e.g. Commander macro re-queues ROADMAP_HANDOFF_VALIDATE if review_needed and score < 7), trend tracking, dashboard integration.

### C.6 Output paths and filename

- **Normal run**: Report (and optional JSON sidecar or embedded) at `1-Projects/<project_id>/Roadmap/handoff-validation-report-<timestamp_iso>.md`. **Vault-Layout.md**: Standardize filename → **handoff-validation-report-{timestamp_iso}.md** (sortable, unique). Example: `handoff-validation-report-2026-03-15T191600Z.md`.
- **dry_run / test harness**: Write report to **Temp/** (e.g. `Temp/validator-roadmap_handoff-<project_id>-<timestamp>.md`); return **full JSON + markdown preview** in Run-Telemetry or hand-off return for manual verification. Queue mode **VALIDATOR_TEST** (or param `dry_run: true` on ROADMAP_HANDOFF_VALIDATE) triggers this path.

### C.7 Test harness (improvement #6)

- **Trigger**: Queue mode **VALIDATOR_TEST** with same params as ROADMAP_HANDOFF_VALIDATE, **or** param **dry_run: true** on ROADMAP_HANDOFF_VALIDATE.
- **Behavior**: Run the same check; write report (and JSON) to **Temp/** instead of Roadmap/; include full JSON + short markdown excerpt in Run-Telemetry or subagent return for manual verification. Critical for safe iteration when adding new validation types.

---

## Part D — Docs, sync, and polish

### D.1 Queue-Sources example (improvement — minor polish)

```yaml
ROADMAP_HANDOFF_VALIDATE:
  project_id: "my-rust-async-project"
  # optional: phase_range: "1..5"
  # optional: dry_run: true   # test harness → Temp/, JSON in telemetry
```

### D.2 Parameters.md

- Validator subsection: validation types, config keys, **high-stakes vs auto** (fixed model for stability; low-stakes can use auto for cost). Report path template, JSON schema reference, severity tiers.

### D.3 Vault-Layout.md

- Report filename: **handoff-validation-report-{timestamp_iso}.md** (sortable, unique). Path: `1-Projects/<project_id>/Roadmap/`.

### D.4 Subagent-Safety-Contract

- Add: **"Validator subagents MUST be read-only on input artifacts except the explicit output path (report/verdict)."**

### D.5 Cursor-Skill-Pipelines-Reference / Skills.md

- Validator subagent: trigger (ROADMAP_HANDOFF_VALIDATE, VALIDATOR_TEST), validation type roadmap_handoff, outputs (JSON + markdown report), model from config, fallback to auto and telemetry note.

### D.6 Sync

- .cursor/sync/rules/agents/validator.md, .cursor/sync/changelog.md.

---

## Summary: improvements integrated

| # | Improvement | Where in plan |
|---|-------------|----------------|
| 1 | Structured JSON + markdown report | C.5 — schema, frontmatter, write JSON first → markdown |
| 2 | Severity tiers + auto-escalation | C.4 — table, escalation_recommended, report grouping |
| 3 | Cross-reference prior artifacts | C.3 — queue includes prior reports + decisions-log; validator flags regressions |
| 4 | Model fallback + telemetry | B.1 — fallback to auto, model_used in Run-Telemetry and report frontmatter |
| 5 | Extensibility helpers | A.5 — check_contradictions, check_sourcing_strength, score_readiness in validator.mdc |
| 6 | Test harness | C.6–C.7 — VALIDATOR_TEST / dry_run, Temp/ output, JSON in telemetry |
| — | Queue-Sources example | D.1 |
| — | Parameters high-stakes vs auto | A.3, D.2 |
| — | Vault-Layout report filename | C.6, D.3 |
| — | Subagent-Safety-Contract read-only | A.1, B.2, D.4 |

---

## Files to add or change

| Item | Action |
|------|--------|
| Second-Brain-Config.md | Add `validator.roadmap_handoff.model` (grok-code) |
| Parameters.md | Validator subsection: types, high-stakes vs auto, severity tiers, report path, JSON ref |
| queue.mdc | ROADMAP_HANDOFF_VALIDATE, VALIDATOR_TEST or dry_run; dispatch validator + model; fallback to auto and log model_used |
| Queue-Sources.md | Document mode, params (project_id, phase_range, dry_run); example D.1 |
| validator.mdc | Full subagent: contract, read-only invariant, branch roadmap_handoff; JSON then markdown; severity; prior-artifact compare; shared helpers (check_contradictions, check_sourcing_strength, score_readiness) |
| legacy-agents/validator.mdc | Same for fallback |
| system-funnels / dispatcher | validator in pipeline list; model pass |
| Subagent-Safety-Contract | Validator explicit model; **read-only except output path** |
| Vault-Layout.md | Report filename handoff-validation-report-{timestamp_iso}.md |
| Cursor-Skill-Pipelines-Reference, Skills.md | Validator + roadmap_handoff, test harness, model fallback |
| .cursor/sync/* | Sync validator rule, changelog |
