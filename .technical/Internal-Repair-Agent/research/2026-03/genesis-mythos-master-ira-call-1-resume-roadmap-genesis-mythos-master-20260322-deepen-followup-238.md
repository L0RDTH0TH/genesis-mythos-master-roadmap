---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-238
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 3, high: 2 }
validator_report: .technical/Validator/research-synthesis-gmm-316-20260322T233100Z-first.md
parent_run_id: queue-eat-20260322-resume-deepen-238
---

# IRA report — research / validator first pass (ira_call_index 1)

## Context

Research pipeline nested validator (`research_synthesis`, first pass) returned `severity: medium`, `recommended_action: needs_work`, primary code `safety_unknown_gap`. Invocation is **ira_after_first_pass: true** (mandatory IRA cycle). The synthesis note `Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330.md` is sound scaffolding but leaves **replay-breaking** items in §7 “Pending decisions,” marks §4 telemetry as **illustrative**, and anchors strong claims on **blog/Q&A** sources. This IRA proposes **minimal, vault-safe** content repairs **only** under `Ingest/Agent-Research/**` so Research can re-apply edits and the second validator pass can compare against this first report.

## Structural discrepancies (expanded beyond validator text)

1. **Floating replay semantics:** §7 still asks whether zero-intent ticks duplicate hash, skip, or carry-forward — any implementer can diverge on `committed_sim_observable_hash` without violating the note as written.
2. **Unpinned registry:** `facet_manifest_id` has no canonical storage path, schema, or bump rule in-agent-research; “D-027 until stack pinned” is not a registry contract.
3. **Evidence / tone mismatch:** §1–§2 present architectural claims with vendor blog + Stack Overflow; validator correctly flags **safety_unknown_gap** for normative-adjacent text without primary or project-owned harness citations.
4. **Non-normative telemetry:** §4 explicitly defers naming to illustration; deepen/CI cannot treat the object as an RFC without a versioned **draft v0** block.
5. **No falsifiable byte story:** Missing ordered preimage fields + toy golden vector; deterministic bundle claim is not testable from the note alone.
6. **Surface defects:** e.g. “a **explicit** no-op” (§2) undermines trust in normative sections.

## Proposed fixes (see parent return payload `suggested_fixes`)

Ordered **low → medium → high** for apply preference. All `target_path` values stay under `Ingest/Agent-Research/`.

## Notes for future tuning

- Research skill should default to emitting **Normative draft (v0)** vs **Brainstorm** sections so validators can gate on section tags.
- When `safety_unknown_gap` fires on research_synthesis, auto-suggest an IRA fix list aligned with `next_artifacts` checklist to reduce parent-agent drift.
