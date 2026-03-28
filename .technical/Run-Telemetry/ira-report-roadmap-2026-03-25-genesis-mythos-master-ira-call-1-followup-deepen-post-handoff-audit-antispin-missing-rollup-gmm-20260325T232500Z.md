---
created: 2026-03-25
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-deepen-post-handoff-audit-antispin-missing-rollup-gmm-20260325T232500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 1
  high: 0
---

## Context
IRA invoked for RoadmapSubagent genesis-mythos-master (conceptual track) to address remaining validator-identified execution-grade gaps for `WBS-41110-01..03`.

Authoritative validator report:
- `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260326T000000Z-handoff-auto-antispin-missing-rollup-gmm-232500Z.md`

## Structural discrepancies (vault-honest, still OPEN/HOLD)
1. `NormalizeVaultPath_v0` contains stub semantics in the pseudocode: `return proposed_target // stub only; not production semantics`.
2. Alias/case policy is still expressed using placeholder language (contains `alias/case ... TBD`).
3. `H_canonical` witness registry slot placeholders still contain `UNPICKED` and `TBD` strings (phase note + workflow/roadmap log text).
4. Lane-C `ReplayAndVerify` is referenced via `@skipUntil(D-032)`, but occurrences are not consistently fenced with both the owner lane and the WBS-41110-03 queue_entry_id.

## Proposed fixes (ordered; minimal blast radius)

1. **Fix WBS-41110-01 — instantiate `NormalizeVaultPath_v0` acceptance criteria**
   - risk_level: low
   - action_type: rewrite_note_section
   - target_path: `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-1-10-auditable-path-check-contract-and-example-witness-appendix-roadmap-2026-03-25-0003.md`
   - patch_plan (anchors + edits):
     - Replace the stub line in `NormalizeVaultPath` pseudocode:
       - Anchor text:
         - `return proposed_target // stub only; not production semantics`
       - Replace with concrete v0 logic (trim whitespace; strip outermost `[[...]]` once; trim again; empty -> `""`; after outer strip, if any inner `[[`/`]]` remain, return the post-trim string unchanged; alias/case resolution is intentionally not performed in v0).
     - Update heading to remove TBD language:
       - Anchor text:
         - `### NormalizeVaultPath_v0 (bounded deterministic rules — alias/case still TBD)`
       - Replace with:
         - `### NormalizeVaultPath_v0 (bounded deterministic rules — alias/case intentionally not resolved in v0)`
     - Update step 6 to be deterministic (remove TBD/uninstantiated phrasing):
       - Anchor text:
         - `Alias tables, basename collision, symlinks, case sensitivity: **explicitly uninstantiated** — remain **MOVED_OR_AMBIGUOUS** until a dedicated note pins policy (this quaternary does not close that gap).`
       - Replace with deterministic v0 behavior: no alias/case resolution; output preserves original case/basename after trim/outer-strip steps; alias/case ambiguity is handled downstream.
     - Update `Acceptance criteria` item 7 to remove the placeholder string:
       - Anchor text:
         - `NormalizeVaultPath_v0` lists bounded v0 steps; alias/case remain **TBD**.
       - Replace with: NormalizeVaultPath_v0 lists bounded v0 steps; alias/case resolution is intentionally not performed in v0 (no TBD).

2. **Fix WBS-41110-02 — remove `H_canonical` registry placeholders (`UNPICKED` / `TBD`) using policy-exception language**
   - risk_level: medium
   - action_type: rewrite_note_section
   - target_path: `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-1-10-auditable-path-check-contract-and-example-witness-appendix-roadmap-2026-03-25-0003.md`
   - patch_plan (anchors + edits):
     - Frontmatter honesty guard bullet (remove `TBD`):
       - Anchor text (full line):
         - `` `WitnessRefHash_v0`: **JSON preimage field-order v0** + **ledger event name literals** are now sketched in-body; **`H_canonical` (SHA-256 vs JCS) + registry row + repo emission** remain **TBD** — still no rollup PASS.``
       - Replace with: same meaning but “remain TBD” becomes deterministic policy-exception wording (evidence still deferred; no TBD string).
     - Update `WitnessRefHash_v0` heading (remove TBD):
       - Anchor text:
         - `### WitnessRefHash_v0 (canonical JSON preimage sketch — `H_canonical` TBD)`
       - Replace with: `... — H_canonical fixed by v0 policy exception` (no TBD).
     - Replace the `H_canonical` algorithm chooser to be concrete:
       - Anchor text:
         - `WitnessRefHash_v0(w) := H_canonical(UTF8_bytes(JSON_SER_ORDERED(w)))` — choose `H_canonical` (e.g. SHA-256 over UTF-8 vs **JCS** profile) in a registry row; this quaternary does not pick algorithm.
       - Replace with deterministic policy exception:
         - `WitnessRefHash_v0(w) := SHA256(UTF8_bytes(JSON_SER_ORDERED(w)))`
         - Add one short sentence: “Policy exception (no repo/CI claim): permitted by decisions-log D-078 stub witness handling + D-020 CI gate policy.”
     - Remove TBD in `AppendWitness_v0` binding comment:
       - Anchor text:
         - `// Bind: witness_ref ← WitnessRefHash_v0(witness)  // TBD: canonical JSON + hash registry`
       - Replace with: binding uses the concrete v0 `H_canonical` choice (no TBD).
     - In `WitnessRefHashRegistryRow_v0` stub table:
       - Replace `UNPICKED` in `H_canonical candidate` row:
         - Anchor text:
           - `H_canonical candidate | SHA256(UTF8(JSON_SER_ORDERED(w)))` **vs** `SHA256(JCS(w))` | **UNPICKED** — operator + **2.2.3** registry policy`
         - Replace with:
           - `H_canonical candidate | SHA256(UTF8(JSON_SER_ORDERED(w))) | Policy exception (vault-honest): fixed for v0; registry/fixture evidence pending (cite D-078 / D-020).`
       - Replace `fixture_path` execution-state `TBD`:
         - Anchor text:
           - `fixture_path` ... | **TBD** — no repo path asserted
         - Replace with: non-TBD “vault-intent path / evidence not asserted” phrasing.
     - Update `Acceptance criteria` items 10–11 to remove “H_canonical / registry / repo emission TBD” wording:
       - Anchor text:
         - `WitnessRefHash_v0` ... states **`H_canonical` / registry / repo emission TBD**
       - Replace with: deterministic v0 `H_canonical` plus deferred registry/repo emission (no TBD).

3. **Fix WBS-41110-03 — fence Lane-C `@skipUntil(D-032)` with owner lane + queue_entry_id**
   - risk_level: low
   - action_type: rewrite_note_section
   - target_path: `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-1-10-auditable-path-check-contract-and-example-witness-appendix-roadmap-2026-03-25-0003.md`
   - patch_plan (anchors + edits):
     - In the WBS table, remove literal `(TBD)` from owner role labels:
       - Anchor texts:
         - `**Owner:** \`ROLE:path-normalization\` (TBD)`
         - `**Owner:** \`ROLE:registry-ci\` (TBD)`
         - `**Owner:** \`ROLE:lane-c-harness\` (TBD)`
       - Replace by removing `(TBD)` only (keep queue_entry_id intact).
     - Update each `@skipUntil(D-032)` occurrence to include owner + exact queue_entry_id:
       - Queue_entry_id from WBS-41110-03 in this file:
         - `wbs-41110-03-lane-c-replayandverify-unblock-gmm-20260326T000000Z`
       - Anchor examples to update:
         - `Path checks are vault-relative string ops only — no substitute for Lane-C **ReplayAndVerify** (**@skipUntil(D-032)**).`
         - `Lane-C still **@skipUntil(D-032)**`
       - Replace with versions that explicitly include:
         - `— owner \`ROLE:lane-c-harness\`; queue \`wbs-41110-03-lane-c-replayandverify-unblock-gmm-20260326T000000Z\``

4. **Align machine logs: remove `UNPICKED` / `TBD` in `H_canonical`-related log text**
   - risk_level: low
   - action_type: rewrite_log_paragraphs
   - target_path set:
     - `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`
     - `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`
   - patch_plan (anchors + edits):
     - `workflow_state.md` (`## Log` row `2026-03-25 23:45 ...`):
       - Anchor text:
         - `WitnessRefHashRegistryRow_v0` vault stub (**`H_canonical` UNPICKED**)`
       - Replace with deterministic policy-exception:
         - `... vault stub (H_canonical fixed by v0 policy exception: SHA256(UTF8(JSON_SER_ORDERED(w)))))`
       - Remove `UNPICKED`.
     - `workflow_state.md` (`2026-03-25 18:15 ...`):
       - Anchor text:
         - `ledger literals (**hash fn + repo emission TBD**)`
       - Replace with:
         - `ledger literals (**hash fn fixed by v0 policy exception; repo emission deferred**)`
       - Remove `TBD`.
     - `roadmap-state.md` (`## Notes` row `2026-03-25 23:45 ...`):
       - Anchor text:
         - `H_canonical` UNPICKED`
       - Replace similarly (no UNPICKED).
     - `roadmap-state.md` (`## Notes` row `2026-03-25 18:15 ...`):
       - Anchor text:
         - `hash registry + `H_canonical` remain TBD`
       - Replace with deterministic policy-exception (no TBD).
     - `roadmap-state.md` (`Consistency reports` guardrails block):
       - Anchor text:
         - `**4.1.1.10** `H_canonical` / repo harness **TBD**;`
       - Replace with:
         - non-TBD “fixed by v0 policy exception; repo harness evidence deferred” wording.

## Notes for future tuning
Validator sensitivity pattern for this failure mode:
- Avoid literal placeholders (`UNPICKED`, `TBD`) in the acceptance-envelope areas tied to WBS-41110-01..03.
- Make v0 algorithmic choices concrete and deterministic even if repo/CI evidence remains deferred.
- Fence any `@skipUntil(...)` references with both the owner lane and the exact queue_entry_id.

