---
title: BS-GMM bootstrap, D-060 high-util policy, junior WBS add-on (3.4.9 nested research)
research_query: "Empty-queue A.1b traceability; D-060 recal vs deepen; GMM-BS-01 operator checklist"
linked_phase: "Phase 3.4.9 — Post-recal task decomposition / junior handoff bundle"
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, queue-continuation, d-060, junior-handoff]
research_tools_used: [vault_first]
research_escalations_used: 0
agent-generated: true
origin: roadmap-deepen
---

# BS-GMM bootstrap, D-060 policy, and one junior WBS row (vault synthesis)

**Audience:** Roadmap Layer 2 pre-deepen consumables for **genesis-mythos-master** / **3.4.9**. **Does not** log **D-044** or **D-059** outcomes; dual-track and tree-guard language remain mandatory per upstream phase notes.

## 1. Empty-queue bootstrap / Layer-1 A.1b — traceability patterns

**Normative docs:** [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]] and synced [[.cursor/sync/rules/agents/queue|queue]] § **A.1b**.

| Artifact | Role |
| --- | --- |
| **`queue_continuation`** (YAML tail on Roadmap return) | Machine-readable **suppress_followup**, **suppress_reason**, **`continuation_eligible`**, optional **`suggested_next`**, **`project_id`**, **`queue_entry_id`**, **`completed_iso`**. |
| **`.technical/queue-continuation.jsonl`** | Durable log Layer 1 appends when **`queue_continuation.continuation_log_enabled`** is true ([[3-Resources/Second-Brain-Config|Second-Brain-Config]]). |
| **A.1b reader** | When **`prompt-queue.jsonl`** has **zero** valid lines after parse, tail-read the log, pick newest **eligible** record (not `explicit_queue_next_false`, `target_reached`, `pipeline_failure`, `nested_attestation_failure`), within **TTL** (`empty_queue_bootstrap_max_age_minutes`). |

> **Operator reconciliation (Spec vs Layer-1 rule text):** [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]] describes **four** `suppress_reason` exclusions for bootstrap eligibility. Synced **queue** rule text (e.g. [[.cursor/sync/rules/agents/queue]] § A.1b step 4) may list only **`explicit_queue_next_false`** and **`target_reached`** alongside **`continuation_eligible`** and TTL. When auditing A.1b, **compare both**; treat **runtime** as authoritative for the live queue processor version you are running, and use the Spec as the durable contract checklist — until/unless **queue.mdc** step 4 explicitly enumerates all four exclusions.

**Idempotency (bootstrap line):** `idempotency_key` = **`empty-bootstrap-<queue_entry_id>-<completed_iso>`** so repeat EAT-QUEUE does not duplicate the same bootstrap.

**`suggested_next`:** Optional object e.g. `{ "mode": "RESUME_ROADMAP", "params": { ... } }` — if valid, Layer 1 builds the candidate JSONL from it; else minimal **`RESUME_ROADMAP`** **`deepen`** with **`user_guidance`** citing the continuation record and source **`queue_entry_id`**.

**Layer-1 synthesis (A.5c.1)** when Roadmap Success + **`queue_next !== false`** but **`queue_followups.next_entry`** missing: separate key **`layer1-synth-<queue_entry_id>-<completed_iso>`** — juniors should treat **bootstrap** vs **contract-violation recovery** as different trace rows in audit tables.

**Roadmap-emitted `queue_followups` (primary path):** Layer 2 should return **`queue_followups.next_entry`** with optional **`idempotency_key`** (e.g. `<current_entry_id>-followup-<mode>`) — see plan/changelog references in `.cursor/plans` and Queue-Sources; primary append is **before** post–little-val validator ordering per queue rules.

## 2. High context utilization — two thresholds (≈70% auto-recal vs ~80% narrative) and recal vs deepen (D-060 alignment)

**Authoritative vault narrative:** [[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205|phase-3.4.8 (D-060)]] — **Threshold authority** defers to merged queue params + Config keys (`context_util_threshold`, `context_window_tokens`, `recal_util_high_threshold`, etc.).

**Automation matrix (restated for operators):**

| Signal | Prefer | Notes |
| --- | --- | --- |
| **`context_util_pct ≥ recal_util_high_threshold`** (default often **~70%** after **roadmap-deepen** — verify merged **Parameters** / **Second-Brain-Config** / **roadmap-deepen** SKILL) | **`RESUME_ROADMAP`** with **`params.action: "recal"`** | **Distinct from** the “often **80%**” examples in prose; this is the **automation recal gate** called out on **3.4.8** next-actions / structural audit rows. |
| **estimated_tokens > ~90% × context_window** | **`recal`** then re-queue deepen if dispatch says so | Overflow guardrail; do not stack full-context deepen on a hot run. |
| **Ctx Util at/above ~80%** (example band in recent runs — **always** verify merged config) + **mid-band confidence** | **`recal`**, **`handoff-audit`**, or **narrow deepen** | Must **name the path** on the next **`workflow_state` `## Log`** row — no silent default. |
| **Stale YAML** vs physical last **`## Log`** row | Hygiene repair or **`recal`** before trusting util | See **GMM-HYG-01** / `VerifyWorkflowHygieneAgainstLastLogRow()` on [[phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225|3.4.9]]. |

**3.4.9 explicit follow-up (example pattern):** After shallow deepen with **Ctx Util still > 80%**, **preferred** next queue entry remains **`RESUME_ROADMAP`** with **`params.action: "recal"`** unless **`user_guidance`** overrides (e.g. **`handoff-audit`** on the **3.4.8 / 3.4.9** bundle) — consistent with § **Queue / Layer-1 follow-up** on the phase note.

## 3. Junior WBS — one additional task row (GMM-*)

Add to the **3.4.9** traceability matrix (vault edit is out of scope for this research file — paste row into parent phase note when integrating):

| Task ID | Ladder / origin | Evidence type | Owner |
| --- | --- | --- | --- |
| **GMM-BS-01** | Layer-1 **A.1b** empty-queue bootstrap + continuation eligibility | **Bootstrap audit pack:** (1) tail **`queue-continuation.jsonl`** excerpt or path; (2) appended JSONL line showing **`idempotency_key`** `empty-bootstrap-…`; (3) note whether candidate came from **`suggested_next`** vs minimal deepen; (4) confirm no prior line with same **`idempotency_key`** in **`prompt-queue.jsonl`**. | Operator + automation |

**Explicit non-scope:** **GMM-BS-01** does **not** require **D-044**/**D-059** picks, CI rows, or rollup **HR ≥ 93** — it is **orchestration traceability** only.

## Raw sources (vault)

- [[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]]
- [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec]]
- [[3-Resources/Second-Brain-Config]] (`queue_continuation`, `queue.synthesize_followup_when_queue_next_true`)
- [[.cursor/sync/rules/agents/queue]] (A.1b, A.5c.1)

## Sources

- Vault paths above (normative for this synthesis).
- External CQRS/event-sourcing background (optional cross-read only): [CQRS (Martin Fowler)](https://martinfowler.com/bliki/CQRS.html), [Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html) — already cited on **3.4.8**; not repeated in depth here.
