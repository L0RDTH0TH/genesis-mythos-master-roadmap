---
name: Validator tiering phased rollout
overview: "Roll out tiered validator handling (reason-code routing, scoped blocks, Layer 1 pivots) in four phases: document features, implement pipeline/validator behavior from docs, document queue changes, then implement queue orchestration."
todos:
  - id: p1-01-spec-skeleton
    content: "Phase 1: Create 3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md with title, frontmatter, outline headings (no rule edits yet)"
    status: completed
  - id: p1-02-spec-definitions
    content: "Phase 1: Spec § definitions — incoherence (restated-boundary test), contradiction, safety-critical vs safety-unknown, severe state hygiene"
    status: completed
  - id: p1-03-spec-reason-codes
    content: "Phase 1: Spec § closed-set reason_codes + primary_code precedence when multiple codes appear"
    status: completed
  - id: p1-04-spec-action-matrix
    content: "Phase 1: Spec § action matrix — each code → severity/recommended_action → pipeline Success gate → allowed non-blocked pivot"
    status: completed
  - id: p1-05-spec-scoped-block
    content: "Phase 1: Spec § scoped block (project_id, slice, validation_type) + what may run vs forbidden downstream deepen"
    status: completed
  - id: p1-06-spec-repair-first
    content: "Phase 1: Spec § repair-first same-scope — allowed repair actions (recal, handoff-audit, sync-outputs) preempt deepen until done/override"
    status: completed
  - id: p1-07-spec-chains
    content: "Phase 1: Spec § chained queue entries — primary hard-blocked → abort vs deps complete (explicit decision)"
    status: completed
  - id: p1-08-validator-reference
    content: "Phase 1: Edit Validator-Reference.md True BLOCK + split safety + pointer to Validator-Tiered-Blocks-Spec"
    status: completed
  - id: p1-09-layers-diagram
    content: "Phase 1: Edit Subagent-Layers-Reference.md (or Backbone) — diagram/bullets nested validator → IRA → final pass → tiered outcome → pivot"
    status: completed
  - id: p1-10-backbone-pointer
    content: "Phase 1: Add one-line pointer in Rules.md and/or Pipelines.md to Validator-Tiered-Blocks-Spec"
    status: completed
  - id: p2-01-validator-mdc-codes
    content: "Phase 2: validator.mdc — map hostile findings to reason_codes + recommended_action per Phase 1 matrix"
    status: completed
  - id: p2-02-validator-mdc-safety
    content: "Phase 2: validator.mdc — calibrate safety_unknown_gap vs safety_critical_ambiguity; incoherence vs contradictions_detected"
    status: completed
  - id: p2-03-roadmap-tiered
    content: "Phase 2: roadmap.mdc + roadmap.md — final Success gate tiered; needs_work non-blocking where spec says; hard block only listed codes"
    status: completed
  - id: p2-04-roadmap-metadata
    content: "Phase 2: roadmap.mdc + roadmap.md — return blocked_scope metadata; incoherence guided retry per Parameters"
    status: completed
  - id: p2-05-code-pipelines
    content: "Phase 2: ingest/organize/archive/distill/express mdc+md — align mandatory nested validator Success gate with Phase 1 tiered rules"
    status: completed
  - id: p2-06-research-pipeline
    content: "Phase 2: research.mdc + research.md — tiered block / synthesis unsafe follow-ups per spec"
    status: completed
  - id: p2-07-ira-optional
    content: "Phase 2: internal-repair-agent.md — only if spec requires new hand-off fields or priors per reason_code"
    status: completed
  - id: p2-08-parameters-config
    content: "Phase 2: Parameters.md + Second-Brain-Config.md — max_incoherence_retries, optional validator.tiered_blocks_enabled, repair-first keys if any"
    status: completed
  - id: p2-09-tests-validator
    content: "Phase 2: Tests-Validator.md — one worked example per tier (contradiction, incoherence, safety_unknown, state_hygiene, safety_critical)"
    status: completed
  - id: p2-10-sync-changelog
    content: "Phase 2: .cursor/sync + changelog.md for every touched rule/agent under backbone-docs-sync"
    status: completed
  - id: p3-01-queue-sources-schema
    content: "Phase 3: Queue-Sources.md — document optional fields blocked_scope, validator_followup, queue_priority (or chosen tie-break field), incoherence_retries_remaining"
    status: completed
  - id: p3-02-queue-sources-examples
    content: "Phase 3: Queue-Sources.md — JSONL examples for repair follow-up after contradictions_detected + handoff-audit"
    status: completed
  - id: p3-03-queue-postlv
    content: "Phase 3: queue.mdc — post-little-val per reason_code; append follow-up vs queue_failed vs consume+append (A.7)"
    status: completed
  - id: p3-04-queue-repair-sort
    content: "Phase 3: queue.mdc — repair-first ordering spec; RECAL→RESUME_ROADMAP tie; chosen fix (queue_priority | sub-sort | meta-entry | inject)"
    status: completed
  - id: p3-05-auto-eat-sort
    content: "Phase 3: auto-eat-queue.mdc — canonical sort tie-break: same project_id repair lines before deepen; scoped orthogonal continue"
    status: completed
  - id: p3-06-auto-eat-chain-scoped
    content: "Phase 3: auto-eat-queue.mdc — chain primary hard-blocked behavior + dependency rules (align Phase 1 spec)"
    status: completed
  - id: p3-07-logs-watcher
    content: "Phase 3: Logs.md + watcher guidance — log lines when pivot/repair scheduled vs hard-stop vs needs_work-only"
    status: completed
  - id: p3-08-safety-contract-queue
    content: "Phase 3: Subagent-Safety-Contract.md — Layer 1 append follow-up + validator return fields queue must read"
    status: completed
  - id: p4-01-implement-branching
    content: "Phase 4: queue.mdc + auto-eat-queue.mdc — implement post-pipeline + post-little-val branching on severity, recommended_action, reason_codes/primary_code"
    status: completed
  - id: p4-02-implement-repair-sort
    content: "Phase 4: Implement repair-first ordering per Phase 3 (same project_id: repair before deepen)"
    status: completed
  - id: p4-03-implement-a7
    content: "Phase 4: Implement A.7 processed_success_ids vs queue_failed per Phase 3 chosen policy; adjust Phase 3 doc if build diverges"
    status: completed
  - id: p4-04-implement-chains
    content: "Phase 4: Implement chained-mode behavior when primary hard-blocked (per Phase 1/3)"
    status: completed
  - id: p4-05-regression-docs
    content: "Phase 4: Regression — repair-before-deepen scenario + optional Docs queue pivot examples snippet"
    status: completed
  - id: p4-06-sync-changelog
    content: "Phase 4: .cursor/sync + changelog for queue rules touched in Phase 4"
    status: completed
isProject: false
---

# Phased rollout: tiered validator blocks and queue pivots

This plan supersedes the conversational “tiered_validator_block_handling” intent as an **execution roadmap**. It incorporates: **reason-code–aware handling**, **split safety codes**, **contradiction follow-ups via queue**, **bounded incoherence handling**, **hard blocks for severe state**, and **scoped blocks with pivot to non-blocked loops** (a block in one slice does not freeze unrelated work).

### Repair-first queue policy (cross-cutting)

When a validator hard block or surviving **contradiction** applies to a **scoped** area, Layer 1 must **not** imply “stop the whole vault,” but **within the same blocked scope** it **must prefer reconciliation before more deepen** on that spine.

- **Same blocked scope** (same `project_id` and any phase/slice ids in `blocked_scope` / validator report): **repair-first** — schedule **targeted** follow-up entries (e.g. `RESUME_ROADMAP` with `action: recal` or `handoff-audit`, optional `sync-outputs`) **before** any further `RESUME_ROADMAP` **deepen** (or other advancing actions) for that scope. Rationale: contradictions and severe truth forks should not be buried under new narrative.
- **Orthogonal work:** **continue** — other `project_id`s, or entries with **no dependency** on the blocked contract, may run in normal canonical order without waiting for repair of project A.
- **Implementation note:** Today, `RECAL-ROAD` normalizes to `RESUME_ROADMAP`, so **deepen** and **recal** share the same canonical mode bucket; **file order alone does not guarantee repair-before-deepen**. Phase 3/4 must define **explicit tie-breaking** (e.g. `queue_priority` / `validator_repair_followup: true` / sub-sort by `params.action` for same `project_id`, or a pinned meta-entry pattern analogous to `CHECK_WRAPPERS`).

---

## Phase 1 — Document the plan features

**Goal:** Single source of truth in vault docs before any rule/skill edits.

**Deliverables (under [3-Resources/Second-Brain/Docs/](3-Resources/Second-Brain/Docs/) or [3-Resources/Second-Brain/](3-Resources/Second-Brain/) as appropriate):**

1. **Feature spec note** (new), e.g. `Docs/Validator-Tiered-Blocks-Spec.md`:
  - Definitions: **incoherence** (restated-boundary test), **contradiction**, **safety-critical vs safety-unknown**, **severe state hygiene**.
  - **Closed-set `reason_codes`** (extend [Validator-Reference.md](3-Resources/Second-Brain/Validator-Reference.md) by reference): `contradictions_detected`, `state_hygiene_failure`, `safety_critical_ambiguity`, `safety_unknown_gap`, `incoherence` (or equivalent stable id), plus **primary_code** rule when multiple codes appear.
  - **Action matrix:** each code → `recommended_action` (block vs needs_work), pipeline Success gate, and **allowed pivot** (non-blocked loop).
  - **Scoped block contract:** block applies to `(project_id, phase/slice scope, validation_type)`; what may still run (other projects, other phases, recal/handoff-audit/sync-outputs, resource ingest/distill) and what must not (e.g. deepen **downstream of** a contradicted spine without explicit scope).
  - **Repair-first (same scope):** document the rule above; list **allowed repair actions** and that they **preempt** further deepen for the same `project_id` (and slice when specified) until repair completes or human overrides.
  - **Chained queue entries:** behavior when primary is hard-blocked (abort chain vs allow completed deps).
2. **Update [Validator-Reference.md](3-Resources/Second-Brain/Validator-Reference.md)** — “True BLOCK” section aligned with the matrix (split safety; incoherence vs contradiction; pointer to full spec).
3. **Update [Subagent-Layers-Reference.md](3-Resources/Second-Brain/Docs/Subagent-Layers-Reference.md)** (or [Backbone](3-Resources/Second-Brain/Backbone.md) pointer) — one diagram or bullet flow: nested validator → IRA → final pass → **tiered outcome** → optional pivot.
4. **Backbone sync note** in plan: after Phase 1, optionally add a short entry to [Rules.md](3-Resources/Second-Brain/Rules.md) / [Pipelines.md](3-Resources/Second-Brain/Pipelines.md) “see Validator-Tiered-Blocks-Spec” (minimal pointer only in Phase 1).

**Exit criteria:** Spec is reviewable; no implementation dependency beyond reading existing Validator-Reference and queue contracts.

---

## Phase 2 — Build the features designed in the docs

**Goal:** Pipeline and validator **behavior** matches Phase 1 spec (no queue file rewrite logic yet except what already exists).

**Deliverables:**

1. **[.cursor/rules/agents/validator.mdc](.cursor/rules/agents/validator.mdc)** — Hostile pass instructions: map findings to **correct** `reason_codes` and **recommended_action** per spec (e.g. `safety_unknown_gap` → medium / needs_work; `safety_critical_ambiguity` → high / block_destructive).
2. **Pipeline subagent rules + agents** ([roadmap.mdc](.cursor/rules/agents/roadmap.mdc), [roadmap.md](.cursor/agents/roadmap.md), and parallel ingest/distill/express/archive/organize/research as in spec):
  - Final Success gate uses **tiered rules**: hard block only for codes flagged in spec; `needs_work` does not block Success where spec says so.
  - **Incoherence:** `#review-needed` and/or **one guided retry** path per Parameters (decrement counter in return metadata or frontmatter—exact mechanism per Phase 1 spec).
  - **Scoped block:** return metadata includes `blocked_scope` (project_id, paths or phase ids) so downstream consumers (and future queue) know what is frozen vs what remains allowed.
3. **[internal-repair-agent.md](.cursor/agents/internal-repair-agent.md)** / rule — Hand-off fields if new codes need different repair priors (optional; only if spec requires).
4. **[Tests-Validator.md](3-Resources/Second-Brain/Tests-Validator.md)** — Examples for each tier (contradiction vs incoherence vs safety_unknown vs state_hygiene).
5. **Parameters / Config** — e.g. `max_incoherence_retries`, `validator.tiered_blocks_enabled` (if you want a kill-switch), in [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) / [Parameters.md](3-Resources/Second-Brain/Parameters.md) as decided in Phase 1.
6. `**.cursor/sync/`** per [backbone-docs-sync.mdc](.cursor/rules/always/backbone-docs-sync.mdc) for every touched rule/skill.

**Exit criteria:** A human (or test checklist) can run a roadmap/deepen path and see tiered outcomes match the Phase 1 doc.

---

## Phase 3 — Document queue behavior changes

**Goal:** Exact Layer 1 contract **before** code/rule changes to dispatch.

**Deliverables:**

1. **[Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)** — New optional queue entry fields: e.g. `blocked_scope`, `validator_followup`, `queue_priority` (or equivalent tie-break field), `incoherence_retries_remaining`; JSON examples for **follow-up lines** (recal, handoff-audit) after `contradictions_detected`.
2. **[queue.mdc](.cursor/rules/agents/queue.mdc)** + **[auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc)** — Authoritative text for:
  - Post–little-val validator: **per reason_code** — append follow-up vs mark `queue_failed` vs **consume + append** (resolve prior ambiguity with A.7).
  - **Repair-first ordering:** after appending a repair follow-up for `(project_id, scope)`, define how sort/dispatch ensures it runs **before** other `RESUME_ROADMAP` lines for the **same** project (and scope when applicable). Document the **RECAL → RESUME_ROADMAP** normalization tie and the chosen fix (`queue_priority`, sub-sort, meta-entry, or in-run inject).
  - **Scoped block:** processing entry B is allowed when A is blocked if **no dependency** (and chain rules).
  - **Pivot loop:** on hard block, append **explicit** next entry (from spec whitelist: recal, handoff-audit, sync-outputs, alternate `params.phase`, etc.).
3. **[Logs.md](3-Resources/Second-Brain/Logs.md)** / Watcher — What gets logged when a pivot is scheduled vs hard-stop.
4. **Subagent-Safety-Contract** — Queue processor responsibilities for appending follow-ups (if not already implied).

**Exit criteria:** Another agent could implement Phase 4 from these docs alone.

---

## Phase 4 — Build the new queue behavior

**Goal:** Queue/Dispatcher implements Phase 3.

**Deliverables:**

1. **queue.mdc / auto-eat-queue.mdc** — Implement branching after pipeline return and after post–little-val Task return: read `severity`, `recommended_action`, `reason_codes` / `primary_reason_code` from validator return or telemetry; execute **append follow-up**, **processed_success_ids** policy, **chain** behavior.
2. **Repair-first sort** — Implement Phase 3 ordering so repair follow-ups for project P dispatch **before** other `RESUME_ROADMAP` deepen (or advancing) lines for P.
3. **Resolve A.7 tension** — Implement the chosen policy: e.g. **consume** primary entry on contradiction + append recal line, or **retain** with `queue_failed` until ack; document final behavior in Phase 3 doc if adjusted during build.
4. **Chained modes** — Implement “primary hard-blocked → …” per Phase 1 chained contract.
5. **Regression checks** — Repair-before-deepen scenario (same `project_id`) + Tests-Validator cross-checks + optional “Queue pivot examples” in Docs.
6. **Sync** `.cursor/sync/` and **changelog** for queue rules.

**Exit criteria:** End-to-end: queue entry → pipeline → validator → Layer 1 pivot or scoped stop matches Phase 3 doc.

---

## Dependency graph

```mermaid
flowchart LR
  P1[Phase1_DocFeatures]
  P2[Phase2_BuildPipelines]
  P3[Phase3_DocQueue]
  P4[Phase4_BuildQueue]
  P1 --> P2
  P1 --> P3
  P3 --> P4
  P2 --> P4
```



Phase 4 depends on Phase 3 (queue contract) and should align with Phase 2 outputs (`blocked_scope`, reason_code surface in returns).

---

## Risk notes

- **Downstream deepen on a contradicted spine:** Keep the scoped-block / dependency rule prominent in Phase 1 spec to avoid silent debt.
- **Repair-first without sort changes:** Appending a recal line does not help if deepen stays ahead in the sort bucket; Phase 4 must implement Phase 3 tie-break.
- **Validator non-determinism:** Tiering assumes stable `reason_codes`; regression tests in Phase 2 reduce drift.

