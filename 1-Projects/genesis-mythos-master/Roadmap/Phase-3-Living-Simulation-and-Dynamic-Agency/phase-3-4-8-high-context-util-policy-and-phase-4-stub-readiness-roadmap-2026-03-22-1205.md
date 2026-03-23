---
title: Phase 3.4.8 — High context utilization policy and Phase 4.1 stub readiness
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, living-world, context-util, recal, phase-4, presentation, policy]
para-type: Project
subphase-index: "3.4.8"
handoff_readiness: 83
handoff_readiness_scope: "Vault-normative automation policy after 3.4.7 WBS — when to recal / handoff-audit / narrow deepen at Ctx Util ≥ threshold; does not resolve D-044/D-059 — still < min_handoff_conf 93"
execution_handoff_readiness: 35
handoff_gaps:
  - "Operator picks still open: **D-044** **RegenLaneTotalOrder_v0** A/B; **D-059** **ARCH-FORK-01** vs **ARCH-FORK-02** — first Phase 4.1 tertiary *tree* remains blocked until **D-059** logs a pick"
  - "Lane-C / ReplayAndVerify and literal goldens remain **@skipUntil(D-032)** / **D-043** / **D-045**"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.4.8 — High context utilization policy and Phase 4.1 stub readiness

**TL;DR:** After **3.4.7** minted checkable **T-P4-01…05** leaves, this tertiary captures **automation-facing policy** when **Ctx Util** sits at/near the **queue/Config-merge** threshold (often **80%** in recent runs — see **Threshold authority** below), **execution gating** while **D-044** / **D-059** remain open, and **CQRS-style read/write vocabulary** for the **adapter → rig** split (**labeling only** — **D-027** still blocks engine/stack claims).

## Research integration

**Scope:** Policy + patterns for minting **3.4.8** after **3.4.7** — does not replace the WBS on [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]].

### Key takeaways

- **High Ctx Util (at threshold ~80%):** Re-read [[1-Projects/genesis-mythos-master/Roadmap/workflow_state]] before copying numbers. Prefer **shallow deepen** (reduced pulls / `token_cap`), **`handoff-audit`** on the current phase bundle when HR/trace is uncertain, or **`recal`** when estimated context approaches **90%** of window or overflow policy fires — and **state explicitly** in the next log row which path you took.
- **Hygiene before trust:** If YAML `last_ctx_util_pct` / `last_conf` disagrees with the last `## Log` row, fix alignment first (see validator examples in synthesis note).
- **Precedent:** **2026-03-20 07:50** row — **`handoff-audit`** at **32%** util with **HR below min_handoff_conf** — same table as current cursor.
- **D-044 / D-059 gating:** **T-P4-05**-style DM→**`MutationIntent_v0`** work stays **DEFERRED/dual-track** until **D-044** operator pick; do not mint a conflicting **Phase 4.1** tertiary **tree** until **D-059** picks **ARCH-FORK-01** or **ARCH-FORK-02**.
- **CQRS vocabulary:** Presentation path = **read model / projection**; sim tick + ledger = **write model**; aligns with **adapter → rig** and **T-P4-03** package wall.

### Decisions / constraints

- Do not narrate **RegenLaneTotalOrder_v0** A vs B until logged under **D-044**.
- Do not assume **ARCH-FORK** until logged under **D-059**.
- **CI / golden** claims remain under **D-032**, **D-043**, **D-045** regardless of WBS progress.

### Links

- [[Ingest/Agent-Research/phase-3-4-8-high-ctx-util-execution-gates-cqrs-presentation-research-2026-03-22-1215]]
- [[3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260322T203000Z-research-synthesis-phase-3-4-8-second]]

### Sources

- [CQRS (Martin Fowler)](https://martinfowler.com/bliki/CQRS.html)
- [Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html)

## Automation decision matrix (machine-facing)

| Signal | Prefer | Rationale |
| --- | --- | --- |
| **estimated_tokens > 90% × context_window** | **`recal`** then re-queue deepen | Overflow guardrail; do not stack full-context deepen on a hot run. |
| **Ctx Util at/above threshold** and **last_conf mid (70–85)** | **Narrow deepen**, **`handoff-audit`**, or **`recal`** | Bandwidth-limited; log the explicit choice on the next `## Log` row. |
| **Stale YAML vs last `## Log` row** | **Hygiene / `recal`** before trusting util | Avoid false **state_hygiene_failure** loops. |
| **HR unknown or stale for bundle** | **`handoff-audit`** | Produces trace + `handoff_gaps` consumable. |

### Automation matrix → queue action → log artifact

| Signal | Preferred `RESUME_ROADMAP` `params.action` | Required hint in next `workflow_state` `## Log` **Status / Next** | Owner |
| --- | --- | --- | --- |
| **estimated_tokens > 90% × context_window** | `recal` (then re-queue `deepen` if dispatch says so) | Explicit `recal` / overflow language + `queue_entry_id` of the run that fired | Automation |
| **Ctx Util at/above threshold** + **mid-band conf** | `recal`, `handoff-audit`, or narrow `deepen` | Name the chosen path (no silent default) | Automation (+ operator when ambiguous) |
| **Stale YAML** vs physical last log row | `recal` or in-run hygiene repair | `workflow_log_authority: last_table_row` + reconciled `last_ctx_util_pct` / `last_conf` | Automation |
| **HR unknown or stale** for phase bundle | `handoff-audit` | Trace path + `handoff_gaps` summary | Automation |

## Threshold authority (Config vs prose)

Percentages and token ceilings in this tertiary are **non-authoritative** if they disagree with the **merged** queue entry + [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] / [[3-Resources/Second-Brain/Parameters|Parameters]] / `prompt_defaults.roadmap` keys consumed by **roadmap-deepen** (e.g. `context_util_threshold`, high-util **`recal`** gate threshold, `context_window_tokens`, `context_token_per_char`). **Queue `params` override** Config for that run. **Do not** change backbone defaults from this note to match prose — cite keys and align narrative instead.

## Next actions (human or queue)

- **Operator:** Log **D-044** A/B and **D-059** fork when ready (see [[decisions-log]] templates).
- **Queue (post-this-run):** **`RESUME_ROADMAP`** with **`action: recal`** recommended when **roadmap-deepen** high-util gate fires (**Ctx Util ≥ recal_util_high_threshold**, default **70%**) — this run’s follow-up obeys that contract after minting **3.4.8**.

## Dependencies

- **D-058** / **3.4.7** — upstream WBS authoritative.
- **D-060** (this slice) — policy tertiary authority in [[decisions-log]].
- **D-055** — **G-P3.4-*** rollup **PASS** rows **not** reopened by policy text here.

## Deferred CI / analyzer binding (3.4.8 scope)

> Empty or unchecked items here are **expected** until repo + operator gates land. Does **not** downgrade **D-055** **PASS** language for vault-normative rows.

- [ ] **D-032** / **D-043** / **D-045:** No `ReplayAndVerify` or registry golden asserting replay header / regen lane / preimage until those decisions freeze — hold per [[decisions-log]].
- [ ] **G-P3.4-REGISTRY-CI** (**D-055**): Mixed-tick / ambient golden rows materialized under repo + **2.2.3** registry policy — placeholder targets only in vault.
- [ ] **T-P4-03** (**SCOPED_VAULT**): When a game repo exists, checklist: CI workflow path (or analyzer job id), scoped package boundary evidence, link to PR — remain unchecked until **D-032**/**D-043** lanes clear.

## Tasks

### Structural audit — task ladder (validator)

> **Note (IRA 2026-03-22):** `workflow_state` **Status / Next** and tertiary summaries must **not** claim **L1 closure** or **full ladder PASS** until **this** section’s checkboxes reflect **PASS** per the **Definition of done** below (cited paths + `queue_entry_id` where required). **3.4.9** may mint **WBS / handoff artifacts** while **decisions-log / operator / repo** rows remain **`[ ]`**.

- **reason_code:** `missing_task_decomposition` (nested **`roadmap_handoff_auto`** after **recal** — first pass **20260322T120000Z-recal-first**).
- **Status:** **Post-`recal` hygiene** rows **1–2** are **PASS** with vault-cited evidence (**2026-03-22** dispatch **`gmm-post-a1b-deepen-recal-20260322T123500Z`**). **Decisions-log verification**, **Phase 4.1 tree guard**, **T-P4-03 ladder**, and **Operator** rows stay **`[ ]`** until repo picks or logged **D-044** / **D-059**.
- **Definition of done:** At least one **Post-`recal` hygiene** or **Decisions-log verification** row moves to **PASS** with **cited evidence** (path + queue id), or operator logs **D-044** / **D-059** per [[decisions-log]] templates.

**Post-`recal` hygiene**

- [x] **Given** a completed **`RESUME_ROADMAP`** `recal` run **When** reading [[workflow_state]] **Then** compare frontmatter `last_ctx_util_pct`, `last_conf`, `current_subphase_index`, `last_auto_iteration` to the **physical last** `## Log` data row — **PASS** only if all match; else open hygiene repair or re-queue `recal`. **Evidence (baseline structural pass):** original cited `queue_entry_id` **`gmm-post-a1b-deepen-recal-20260322T123500Z`**. **Evidence (live parity as-of 2026-03-22 21:05 UTC bootstrap `recal`):** frontmatter **84 / 73 / 3.4.9 / `gmm-deepen-post-recal-followup-20260322T1925Z`** matches physical last **`## Log`** **deepen** row **`2026-03-22 19:25`**; **`recal`** reaffirmation row **`queue_entry_id` `2b8a47f4-f18e-44c0-9c08-2aa7a07fb02e`**, **`parent_run_id` `l1-eatq-20260322-bootstrap-recal-2b8a`** appears **above** that deepen row per **`workflow_log_authority: last_table_row`**.
- [x] Record the **`queue_entry_id`** of the `recal` run in **Notes** when reconciling (traceability). **Evidence:** logged on **`workflow_state`** **`## Log`** rows **`2026-03-22 13:05`**, **`18:00`**, and **`21:05`** (`2b8a47f4-f18e-44c0-9c08-2aa7a07fb02e`) alongside baseline **`gmm-post-a1b-deepen-recal-20260322T123500Z`** citations.

**Decisions-log verification (no fabricated picks)**

- [ ] **Given** [[decisions-log]] **D-044** **When** scanning for `Operator pick logged` sub-bullet **Then** **PASS** if absent (still pending) or present with **Option A** or **B**; **FAIL** if narrative implies a pick without sub-bullet.
- [ ] **Given** **D-059** **When** scanning for **`ARCH-FORK-01`** or **`ARCH-FORK-02`** label **Then** **PASS** if still “pending”; **FAIL** if Phase 4.1 tertiary *tree* files exist without logged fork.

**Phase 4.1 tree guard**

- [ ] Confirm **no new** Phase **4.1** tertiary *tree* under `Roadmap/` until **D-059** logs **`ARCH-FORK-01`** or **`ARCH-FORK-02`** (stub secondary mint only when D-059 satisfied per **D-060**).

**T-P4-03 ladder (repo-absent)**

- [ ] **Given** no game repo **When** reviewing **T-P4-03** **Then** vault package-boundary spec row remains authoritative; no CI job names asserted.

**Operator**

- [ ] Log **D-044** A/B and **D-059** fork when ready (see [[decisions-log]] templates).

**Automation**

- [ ] After next **`recal`**, verify **workflow_state** **Notes** + YAML agree with last `## Log` row (`workflow_log_authority: last_table_row`).
- [ ] When **D-059** picks a fork, mint **Phase 4.1** stub secondary under [[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]] (do not pre-empt from vault narrative alone).
