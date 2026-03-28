---
title: Phase 3.2.4 — Phase 3.2 secondary closure rollup & advance readiness
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, secondary-closure, handoff-readiness, dm, regeneration]
para-type: Project
subphase-index: "3.2.4"
handoff_readiness: 92
handoff_readiness_scope: "Authoritative G-P3.2-* inventory for Phase 3.2 secondary closure (updated **2026-03-23**): **G-P3.2-REPLAY-LANE** **PASS** — **D-044** **RegenLaneTotalOrder_v0 Option A** logged on [[decisions-log]]; **G-P3.2-REGISTRY-CI** remains **HOLD** — rollup **HR 92** remains below **min_handoff_conf 93** until registry/CI row clears — not advance-eligible under strict **handoff_gate** — operator deepen (**GMM-3324-DEEPEN**): junior CI bundle + **ReplayAndVerify** interface sketch appended (vault-only; no fabricated PASS)"
execution_handoff_readiness: 61
handoff_gaps:
  - "**HOLD — G-P3.2-REGISTRY-CI:** Golden / **ReplayAndVerify** rows for regen ordering per **D-045** + **2.2.3** remain **TBD** — sole rollup **HOLD** after **REPLAY-LANE** cleared **2026-03-23**"
  - "**D-032** field literals + **D-043** canonical preimage freeze + **D-045** golden deferral block execution closure and CI asserts (unchanged)"
links:
  - "[[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]"
  - "[[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]"
  - "[[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]]"
  - "[[phase-2-2-4-phase-2-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-21-2000]]"
  - "[[decisions-log]]"
---

## Phase 3.2.4 — Phase 3.2 secondary closure rollup & advance readiness

**TL;DR:** This note is the **single authoritative rollup** for **Phase 3.2** (DM overwrite + regeneration gates), mirroring **G-P2.2** and **G-P3.1** patterns. Per-tertiary `handoff_readiness` values on **3.2.1–3.2.3** remain **92**; this rollup records **which gate rows are PASS vs HOLD** for **vault-normative** contract completeness vs **execution / CI** debt (**D-039**-style split). **G-P3.2-REGISTRY-CI** clearing work is now decomposed into a **junior execution bundle** plus a **ReplayAndVerify** harness sketch below — **HR stays 92** until live registry/CI evidence lands.

### Whole-tick ordering (restated once)

1. **Regen lane** completes **`regen_apply_sequence`** per **3.2.3** / **D-044** before **`StableMergeKey_v0`** merge of post-regen player+DM intents (**3.2.1**).
2. **`RegenRequest_v0`** preconditions and regen-before-merge ordering per **3.2.2** / **D-042**.
3. **`TickCommitRecord_v0`** closes only after the above; field alignment with **3.1.1** + **`replay_row_version`** per **D-043** — **TBD**.

### G-P3.2-* gate inventory (vault-normative)

| Gate ID | Scope | Evidence | Verdict |
|--------|--------|----------|---------|
| **G-P3.2-DM-TAX** | Channel split `DmOverrideIntent_v0` vs `RegenRequest_v0`, fail-closed codes vs **2.2.1** | [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]] · **D-041** | **PASS** (normative draft) |
| **G-P3.2-REGEN-PRE** | P1–P6, **regen-before-merge**, **2.2.2** coupling, ledger idempotency sketch | [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]] · **D-042** | **PASS** (normative draft) |
| **G-P3.2-REPLAY-LANE** | `regen_apply_sequence` + **RegenLaneTotalOrder_v0** + tick-close coupling | [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]] · **D-044** | **PASS** (normative draft) — **Option A** logged **2026-03-23** on [[decisions-log]] |
| **G-P3.2-REGISTRY-CI** *(draft, **D-040**-style)* | Registry / **ReplayAndVerify** rows for regen ordering | **D-045** + **2.2.3** reconcile | **HOLD** — explicit golden deferral |

**Rollup score:** **3 / 3** core gates **PASS** (contract text) on **DM-TAX** / **REGEN-PRE** / **REPLAY-LANE** + **G-P3.2-REGISTRY-CI** **HOLD** until **D-045** / **2.2.3** — rollup **HR** stays **92** until that row clears.

### Advance readiness vs `handoff_gate`

- Under **`handoff_gate: true`** and **`min_handoff_conf: 93`**, this rollup **`handoff_readiness: 92`** is **below** threshold — **`advance-phase` (3.2 → next macro slice under Phase 3)** is **not** eligible until **G-P3.2-REGISTRY-CI** **HOLD** clears or policy overrides min (document any override in [[roadmap-state]] / queue).
- **Composite `execution_handoff_readiness: 61`** — golden rows, **D-032** header, **D-043** preimage, **D-045** still open.

### Open risks (non-HOLD wording smuggle)

- **D-032** — replay header **shape** **Option A** logged **2026-03-23**; **field encoding** (q16 vs table) + golden + **`replay_row_version`** still block literal CI.
- **D-043** — `CanonicalIntentBytes_v0` / sort preimage **TBD**.
- **D-045** — no **ReplayAndVerify** assert on **`regen_apply_sequence`** until gates clear.
- **3.1.1** — literal **`TickCommitRecord_v0`** field names must be reconciled before **`replay_row_version`** bump.

### Junior execution bundle (G-P3.2-REGISTRY-CI)

Engineering checklist to flip **G-P3.2-REGISTRY-CI** from **HOLD** → **PASS** (no vault wording smuggle):

1. **Registry row (2.2.3)** — Add or extend the wiki/registry entry that names the **ReplayAndVerify** case ID for **`regen_apply_sequence`** ordering, linked to **D-045** and the **D-040**-style registry discipline used elsewhere in the project.
2. **Golden fixture** — Publish vectors that prove **`regen_apply_sequence`** completes **before** **`StableMergeKey_v0`** merge for at least one tick boundary; CI must **fail** if the implementation inverts that order.
3. **Job wiring** — CI README must link this rollup and [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]] as narrative authority (traceability, not a substitute for code).
4. **HR bump rule** — Rollup **`handoff_readiness` → ≥ `min_handoff_conf` (93)** only after the inventory table above shows **PASS** on **G-P3.2-REGISTRY-CI** **and** attestation is recorded on [[decisions-log]] if your process requires it.

### ReplayAndVerify harness — interface sketch

Mid-technical sketch only; engine types are illustrative.

```pseudo
// CI-owned harness; contracts from 3.2.1–3.2.3 / D-044
type RegenApplySequence = OrderedList<RegenOpId>;

function ReplayAndVerify_RegenLane(
  tick: TickId,
  golden: GoldenFixtureRow   // pointer from 2.2.3 registry
) -> Verdict {
  // 1) Parse tick ledger: assert regen_apply_sequence closed before merge boundary.
  // 2) Deterministic replay tick N-1 → N reproduces regen op order exactly.
  // 3) Mismatch → FAIL with fail-closed code aligned to 3.2.1 taxonomy (e.g. REGEN_ORDER_DRIFT).
  return Verdict.PASS | Verdict.FAIL(code, evidence);
}
```

### Acceptance criteria (rollup HR ≥ min_handoff_conf)

- **G-P3.2-REGISTRY-CI** shows **PASS** in the gate table with a **live** VCS or CI reference (or explicit operator attestation on [[decisions-log]] consistent with project norms).
- **D-032** / **D-043** / **D-045** may still suppress **`execution_handoff_readiness`** even when vault **HR** reaches **93**; restate that split in `handoff_readiness_scope` when closing.
- Under strict **`handoff_gate`**, do not treat **macro** advance as automatic when only narrative checkboxes move — **registry/CI** evidence is the hard gate for **G-P3.2-REGISTRY-CI**.

### Operator batch sequencing (chat)

| Step | Artifact | Queue id pattern (operator batch) |
|------|----------|-----------------------------------|
| Done | **3.1.7** rollup | `operator-deepen-phase3-3-1-rollup-gmm-20260323T233237Z` |
| **This run** | **3.2.4** rollup (this note) | `operator-deepen-phase3-3-2-rollup-gmm-20260323T233237Z` |
| **Next enqueue** | **3.3.4** rollup | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200.md` |
| Then | **advance-phase** + **Phase 4** first deepen | Per operator policy after **3.3** rollup |

## Research integration

- **[[Ingest/Agent-Research/phase-3-2-4-secondary-closure-rollup-research-2026-03-22-2205]]** — Draft **G-P3.2-\*** pattern, normative vs execution split, whole-tick narrative, **D-027** stack-agnostic.
- **[[Ingest/Agent-Research/phase-3-1-7-secondary-closure-rollup-advance-readiness-research-2026-03-22-1430]]** — Secondary-closure vocabulary / V&V-style split (external cites on that note; non-binding for engine).

## Tasks

- [x] Authoritative **G-P3.2-\*** table + rollup HR / EHR on this note
- [x] **Operator — D-044:** **RegenLaneTotalOrder_v0** **Option A** logged **2026-03-23** on [[decisions-log]]; **G-P3.2-REPLAY-LANE** → **PASS** on this note
- [x] **GMM-3324-DEEPEN:** Junior **REGISTRY-CI** bundle + **ReplayAndVerify** sketch + operator batch table (**2026-03-23**)
- [ ] **Eng — advance-phase:** Queue **`advance-phase`** only after rollup **`handoff_readiness` ≥ `min_handoff_conf`** (or documented policy exception)
- [ ] **Eng — handoff-audit (optional):** Bundle trace **3.2** secondary → **3.2.1 → 3.2.2 → 3.2.3 → 3.2.4** when preparing next macro transition
