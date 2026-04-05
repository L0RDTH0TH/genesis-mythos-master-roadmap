---
title: Phase 3.3.2 — Consequence durability matrix and persistence invariants
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.3.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 55
handoff_readiness: 85
created: 2026-04-03
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]]"
  - "[[Phase-3-3-1-Vitality-Consequence-Persistence-Cohesion-Seams-Roadmap-2026-04-03-0012]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.3.2** — **consequence durability matrix** + **persistence invariants** downstream of **3.3.1** seams (VitalitySnapshot / ConsequenceRecord); aligns **distilled-core** canonical routing. **Next structural cursor:** **secondary 3.3 rollup** (NL + GWT vs **3.3.1–3.3.2**) — `workflow_state` **`current_subphase_index: "3.3"`**. Queue: `followup-deepen-phase3-332-gmm-20260403T002000Z` \| `parent_run_id: q-eatq-20260330-gmm-332-deepen`.

## Phase 3.3.2 — Consequence durability matrix and persistence invariants

This **tertiary** turns **3.3.1** seam vocabulary into a **decision table** for **which consequences survive which gates** and a **short invariant list** that execution can implement without inventing a second checkpoint story. It **binds** **ConsequenceRecord.durability_class** to **3.1.4** ordering, **3.1.2** merge lineage, and **3.2.1** `authority_class` so **replay**, **audit**, and **operator preview** stay aligned.

## Scope

**In scope:**

- **Consequence durability matrix** — rows = **durability_class** (`must_persist` \| `ephemeral_ux` \| `replay_only`) × columns = **merge outcome** (admitted / deferred / denied) × **checkpoint tick-close** (eligible / ineligible) × **observation surface** (`committed_session` \| `preview_shadow`) — **NL cells** state **allowed** or **forbidden** exposure (no wire IDs).
- **Persistence invariants** — numbered rules that **must** hold in any engine that claims **Phase 3** conceptual compliance (see § Invariants).
- **Roll-forward** semantics — what happens to **deferred** consequences across ticks **without** closing **D-3.1.5-*** (execution-deferred).

**Out of scope:**

- Binary save formats, net sync, Merkle proofs (**execution-deferred**).
- Resolving **D-3.1.5-*** operator picks — remain **execution-deferred** per [[decisions-log]].

## Behavior (natural language)

1. **Matrix use:** For each **ConsequenceRecord**, the matrix answers: *May this record appear on a **committed_session** channel after a **deny_commit** merge outcome?* (default **no** for **must_persist**; **ephemeral_ux** may **only** appear on **preview_shadow** after deny, with **3.2.2** drift disclosure.)
2. **Checkpoint gate:** **must_persist** consequences **must** have **checkpoint_sequence_ref** filled **before** any **committed_session** observation claims them (**3.1.4** ordering is authoritative).
3. **replay_only:** Allowed **only** in **replay** / **audit** surfaces — **not** as **preview_shadow** “fake durability”; **3.2.1** channels that are **replay_only**-scoped must **not** use **authority_class** to imply checkpoint eligibility.

## Consequence durability matrix (NL)

| durability_class | Merge: admitted | Merge: deferred | Merge: denied | Checkpoint: eligible tick | Observation: committed_session | Observation: preview_shadow |
| --- | --- | --- | --- | --- | --- | --- |
| **must_persist** | Yes — **must** attach **merge_lineage_id** + **checkpoint_sequence_ref** before exposure | Hold until merge resolves or explicit cancel — **no** committed_session until resolved | **No** committed_session truth — audit may record **deny** fact | Yes — **only** after merge + checkpoint ordering | Yes — **only** if checkpoint row exists for tick | **No** — preview cannot authoritatively show **must_persist** as durable |
| **ephemeral_ux** | Yes — **UX-only**; may appear **before** checkpoint if labeled **non_authoritative** | May show on **preview_shadow** with **stale** semantics | **Yes** on preview — **drift disclosure** per **3.2.2** | No — **must not** appear in checkpoint slice | **No** unless promoted by **3.1.5** + **3.1.4** in a later tick | **Yes** — primary home |
| **replay_only** | Yes — **audit/replay** exports only | Same — **no** live-session claim | **Yes** — **deny** path visible in replay bundle | **N/A** for live checkpoint — **not** in **VitalitySnapshot** checkpoint slice | **No** unless **replay** channel type is explicitly **replay** (not live session) | **No** — do not masquerade as **preview** durability |

## Persistence invariants (checklist)

1. **I-3.3-A:** No **checkpoint_sequence_ref** is assigned to a **preview_shadow**-only consequence path.
2. **I-3.3-B:** Every **must_persist** **ConsequenceRecord** has **merge_lineage_id** + **checkpoint_sequence_ref** before **committed_session** **ObservationChannel** emission.
3. **I-3.3-C:** **3.1.4** checkpoint ordering remains **strictly before** any **committed_session** observation that claims **post-tick** durability.
4. **I-3.3-D:** **ephemeral_ux** **never** upgrades to **must_persist** without a **new** tick + **3.1.5** admission + **3.1.4** gate (no silent promotion).
5. **I-3.3-E:** **replay_only** facts **do not** advance **checkpoint sequence** and **do not** appear as **checkpoint_eligible** in **VitalitySnapshot** (per **3.3.1** Seam A).

## Interfaces

**Upstream:**

- **3.3.1** — [[Phase-3-3-1-Vitality-Consequence-Persistence-Cohesion-Seams-Roadmap-2026-04-03-0012]] — **VitalitySnapshot** / **ConsequenceRecord** sketches + **GWT-3.3-A–F**.
- **3.1.4** / **3.1.5** / **3.2.1** — same as **3.3.1** (checkpoint, agency, observation).

**Parent:**

- **3.3** — [[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]].

**Downstream:**

- **Secondary 3.3 rollup** — NL checklist + **GWT** parity vs **3.3.1–3.3.2** (next **deepen** target **3.3**).

## Edge cases

- **Deferred merge spans ticks:** **must_persist** stays **quarantined** from **committed_session** until merge resolves — **3.2.2** may show **stale** preview.
- **Operator rollback:** **Replay** may show **revoked** pre-checkpoint rows — **no** contradiction with **3.1.4** if **checkpoint never committed** (execution-deferred detail).

## Open questions

- Whether **replay_only** channels get a **distinct** **ObservationChannel** family vs **committed_session** (**execution-deferred**).
- Minimum **matrix** cell tests before execution (scenario ids — **execution-deferred**).

## Pseudo-code readiness

**Mid-technical (depth 3):** matrix + invariants are **NL**; **no** production API.

## GWT (3.3.2 — matrix / invariants)

| ID | Gate | Evidence |
| --- | --- | --- |
| GWT-3.3-G | **must_persist** + **deny** merge → **no** **committed_session** claim | Matrix row |
| GWT-3.3-H | **I-3.3-B** enforced before **3.2.1** committed exposure | Invariants |
| GWT-3.3-I | **ephemeral_ux** after **deny** only on **preview_shadow** with drift | Matrix + **3.2.2** |
| GWT-3.3-J | **replay_only** does not advance checkpoint sequence | Invariants E |
| GWT-3.3-K | **No silent promotion** **ephemeral_ux** → **must_persist** | I-3.3-D |

## Risk register v0

| Risk | Mitigation | Owner / defer |
| --- | --- | --- |
| Matrix drift vs **3.1.2** merge enum | **merge_lineage_id** mandatory for **must_persist** | Rollup + RECAL if needed |
| **Preview** shows **must_persist** early | **GWT-3.3-G** + **I-3.3-C** | **3.3** rollup audit |
