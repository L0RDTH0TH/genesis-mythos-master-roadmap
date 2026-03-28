---
created: 2026-03-22
title: Phase 3.2.1 — DM override channel vs structural regeneration gates (vault synthesis)
source: "Nested Research helper; hand-off queue_entry_id resume-roadmap-genesis-mythos-master-20260322-deepen-followup-240; parent_run_id queue-eat-20260322-genesis-resume-001"
project-id: genesis-mythos-master
tags:
  - agent-research
  - genesis-mythos-master
  - phase-3-2-1
  - dm-override
  - regeneration
  - determinism
  - intent
para-type: Resource
---

## Phase 3.2.1 — DM override vs regeneration (synthesis)

**Scope:** First tertiary under Phase 3.2 — separate **DM live override** (authoritative, ordered commands) from **structural regeneration** (replay-derived subgraph recompute) without breaking the Phase 2.2 `IntentPlan` consumption boundary or Phase 3.1 tick commit / observable bundle contracts.

### Executive read

Vault-normative work in [[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]] and [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]] already pins **canonicalization**, **fixed denial reason_codes**, **manifest-emission boundary**, **golden + fail-closed replay vectors**, and **idempotent ledger** semantics. Phase 3.2’s stub correctly warns that **overrides must not change manifest hash preimage without a documented gate bump** — this synthesis proposes how **3.2.1** operationalizes that split: overrides enter the same class of **deterministically ordered, replay-logged commands** as tick-scoped intents (see [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]] and [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]), while regeneration is a **policy-gated** path that either (a) re-executes a **closed** subgraph with stable seed + stage graph + gate version identifiers, or (b) emits a **fail-closed denial** per an explicit taxonomy (extend the 2.2.1 style; avoid free-text reasons in replay assertions).

### Alignment matrix

| Concern | Phase 2.2.x anchor | Implication for 3.2.1 |
|--------|-------------------|----------------------|
| Denials | [[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]] | New DM/regen failure modes get **closed** `reason_code` strings + stable ids (`intent_id` / `error_fingerprint` pattern), never silent fallback |
| Consumption boundary | [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]] | DM override that affects manifest/spawn ordering must be visible **before** `ManifestEmit` as a first-class envelope (or be rejected) |
| Replay / idempotency | Same 2.2.2 harness pseudo-code | Overrides participate in **ledger_key** / double-apply semantics; regen jobs carry **`deterministic_gate_version_id`**-style versioning when outputs feed the hash chain |
| Tick observable closure | [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]], [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]] | **`TickCommitRecord_v0`** and **`committed_sim_observable_hash`** only after ordered apply; DM edits either land in **`MutationIntent_v0` / apply ledger order** for that tick or in a **documented parallel channel** that still serializes into the replay row |

### Proposed design patterns (for tertiary spec text)

1. **Intent envelope for DM override** — Treat DM “god mode” not as a direct world poke but as **`DmOverrideIntent_v0`** (name TBD) that passes canonicalization + schema validation, hashes into the same **domain-separated** family as `IntentPlan_v0`, and is ordered relative to player intents in the **vault-visible apply order** (parallel to 3.1.5/3.1.6). Reject or deny with a fixed code if the override would skip canonicalization.

2. **Regeneration as gated subgraph replay** — Structural regen is **`RegenRequest_v0`** with explicit inputs: seed snapshot id, stage graph semver, **regen_scope** (allow-listed facets), and output **artifact refs** that feed manifest/lattice only through the pinned boundary. If prerequisites are missing, emit **`REGEN_PRECONDITIONS_FAILED`** (example code — finalize in taxonomy table) instead of partial application.

3. **Fail-closed gate taxonomy (sketch)** — Mirror 3.1.6’s style (`OBSERVABLE_PREMATURE_HASH`, etc.): e.g. **`OVERRIDE_MANIFEST_BYPASS`**, **`REGEN_HASH_CHAIN_DRIFT`**, **`REGEN_SCOPE_OVERFLOW`**, **`LEDGER_ORDER_VIOLATION`**. Each maps to **exactly one** deterministic denial or audit event and **stop-consumption** for the affected id.

4. **Preimage bump contract** — Any override or regen path that changes bytes wired into `manifest_hash` / `TickCommitRecord_v0` preimage must bump **`replay_row_version`** or **`DETERMINISTIC_GATE_Vx`** (analogous to 2.2.2) in a single documented policy table — satisfies Phase 3.2 stub line on hash preimage.

5. **Deterministic ordering log** — Maintain an append-only **override/regen segment** in the replay log (or merge into existing tick rows with typed sub-entries) so “DM then regen” vs “regen then DM” is testable with golden rows, matching the research query themes: *deterministic ordering*, *replay hash*, *fail-closed taxonomy*.

### Parent roadmap links

- [[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]
- [[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]

### Non-normative external hooks (optional reading)

Industry practice (event-sourced systems, deterministic simulation clients) often separates **commands** from **derived replays** and uses **versioned projection rebuilds** — conceptually aligned with the vault split above; no external source is required for vault closure.
