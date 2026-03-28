---
title: "Research — Phase 2.3.4 EMG-2 execution closure (fixtures, freeze, registry parity)"
research_query: "EMG-2 second fixture root; CODEOWNERS; CI path filters; floor-F promotion; wiki registry row materialization"
linked_phase: "Phase-2-3-4 (EMG-2 execution closure)"
project_id: genesis-mythos-master
created: 2026-03-21
tags: [research, agent-research, genesis-mythos-master, EMG-2, CI, golden-fixtures]
agent-generated: true
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-followup-next
parent_run_id: queue-eat-20260321-gmm-deepen-1
---

# EMG-2 execution closure — fixtures, CI gates, freeze, registry (vault spine + cited references)

**Scope:** Complements vault work in [[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]], [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]], and [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]. **Fixture-tree split and EMG-2 tables are vault-owned**; sections below add **cited** CI/ownership/golden-testing references and execution-closure checklists—without redefining project schemas or D-020–D-026.

## Do not duplicate (vault already states)

- Separate root `fixtures/emg2_alignment/v0/` vs `fixtures/intent_replay/v0/`; row schema, `AlignAndVerify` pseudo, WA-1…WA-4 matrix, and wiki **G-EMG2-*** deferral until VCS paths exist.
- PR-reviewed golden refresh, no CI auto-update; `emg2_floor_F_status: frozen` gated on WA runs.

## 1) Second fixture root + CODEOWNERS + CI path filters

**Layout (vault-derived, not an external standard):** This repo already splits **`fixtures/emg2_alignment/v0/`** vs **`fixtures/intent_replay/v0/`** (see scope links above). The recommendation here is to **keep that separation** so CODEOWNERS and workflow `paths:` / `paths-ignore` can stay **narrow**—avoiding one broad fixtures glob that retriggers unrelated jobs. This is **project-shaped consistency**, not a cited industry survey.

**CODEOWNERS:** GitHub evaluates **last matching pattern wins**; patterns are gitignore-like and **case-sensitive**; invalid lines are skipped. Place `CODEOWNERS` under `.github/` first so it is found reliably, and **assign an owner to `CODEOWNERS` itself** to prevent bypass. Teams need **explicit write** access to receive review requests.

[Source: About code owners (GitHub Docs)](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

**CI path filters:** Define path filters in workflow YAML using GitHub’s **`on.<event>.paths`** and **`paths-ignore`** (same glob semantics as described in Actions workflow syntax). Enumerate **each fixture root** plus **shared harness** paths (e.g. verifier crate, shared JSON schema). For monorepos, the community action **`dorny/paths-filter`** can emit boolean outputs per area so `intent_replay` jobs skip when only `emg2_alignment` changes, while a thin **“schema or gate version”** job still runs when shared constants change—see the action README for inputs/outputs.

[Source: Workflow syntax for GitHub Actions — paths and paths-ignore](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore)

[Source: dorny/paths-filter (GitHub)](https://github.com/dorny/paths-filter)

[Source: Path filtering in GitHub Actions — third-party overview (OneUptime)](https://oneuptime.com/blog/post/2025-12-20-path-filtering-github-actions/view) *(illustrative; prefer first-party syntax above for behavior)*

**Practical split for EMG-2:**

| Concern | Suggested pattern |
|--------|-------------------|
| Ownership | `/fixtures/emg2_alignment/` → sim/alignment owners; `/fixtures/intent_replay/` → parser/canonicalization owners |
| CI | `paths:` include both roots + `tools/replay_verify/**` + `tools/align_verify/**` (example) |
| Cross-cutting | Changes to shared **gate version** file or **JSON Schema** trigger **both** jobs |

## 2) Promotion: normative draft → frozen floor F (bounded worst-acceptable)

**Golden / snapshot discipline:** Golden tests treat the file as the assertion; updates are **code review** for behavioral change. Normalize volatile fields **before** diff; fail closed on drift in CI. For additional perspective on curating a **golden set** (coverage vs. cost), see the linked write-up below—treat as **one secondary lens**, not a substitute for your WA matrix.

[Source: Golden file testing overview](https://www.application-architect.com/posts/golden-file-testing-output-comparison/)

[Source: Designing a golden set (HeavyThoughtCloud)](https://heavythoughtcloud.com/knowledge/designing-a-golden-set)

**Promotion checklist (maps to your WA matrix + D-023/D-024):**

1. **Schema closure** — Vector JSON validates; enum strings for `golden_expectations` / `reason_code` match harness tables in the phase note.
2. **Determinism** — Lore/sim slices and scores are stable under pinned normalization (Tier C policy explicit).
3. **WA matrix evidence** — WA-1…WA-4 each logged with **expected vs actual** outcome; failures block freeze.
4. **Version pins** — `emg2_gate_version_id`, `emg2_alignment_floor_version`, and numeric **F** consistent across fixtures + 2.3.2 note frontmatter.
5. **Status flip** — Set `emg2_floor_F_status: frozen` only after (3)+(4); prefer tightening shapes over lowering **F** (per 2.3.3).
6. **Registry row** — Wiki row and decisions-log adoption row reference **concrete** repo paths (next section).

**Property-based testing (PBT) as safety net around goldens:** The **small command alphabet** and **invariant** pattern here is **standard PBT practice** (generate structured inputs; assert properties)—your phase **2.3.1** note is the **vault anchor** for how that applies to EMG-2. Goldens remain the **contractual** floor; PBT is a **surrounding** regression net, not a replacement for reviewed vectors. For an **external example of strict golden-style testing** in another stack (illustrative discipline only), see TensorFlow Federated’s golden tests doc.

[Source: TensorFlow Federated — golden tests](https://www.tensorflow.org/federated/golden_tests)

## 3) Registry / wiki row materialization (documentation parity)

**Goal:** Every **G-*** / **F-*** row in the vault registry table should carry **stable repo pointers** once files exist: primary vector path, optional denial fixtures, harness entrypoint name, and **phase note** wiki-link.

**Parity pattern:**

| Registry column | Materialization rule |
|----------------|---------------------|
| Vector id | Immutable id matching JSON `id` or filename stem |
| Repo path | Relative path from repo root; no “TBD” after merge |
| Phase anchor | `[[phase-2-3-3-...]]` (implementation) + `[[phase-2-2-3-...]]` (wiki rollup) |
| CI proof | Link to workflow name + job id; log excerpt optional |
| Owner | Matches CODEOWNERS line for that subtree |

**Mechanics:** On first merged PR under `fixtures/emg2_alignment/v0/`, open a **paired vault PR** (or same human session) that: (1) fills **G-EMG2-ALIGN** row in 2.2.3 note, (2) updates 2.3.3 WA log if needed, (3) promotes D-022 stub if D-023/D-024 conditions met—so **wiki, decisions-log, and tree** move together.

## Raw sources (vault)

- (none — external URLs only this run)

## Sources

- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore
- https://github.com/dorny/paths-filter
- https://oneuptime.com/blog/post/2025-12-20-path-filtering-github-actions/view
- https://www.application-architect.com/posts/golden-file-testing-output-comparison/
- https://heavythoughtcloud.com/knowledge/designing-a-golden-set
- https://www.tensorflow.org/federated/golden_tests
