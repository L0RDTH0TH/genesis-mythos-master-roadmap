---
name: decisions-preflight
description: Read-only scan of Roadmap decisions-log.md vs rollup surfaces; emit structured YAML for Layer 1 EAT-QUEUE hand-off injection (handoff_addendum.decisions_preflight). No vault writes.
---

# decisions-preflight

## When to use

- **Queue/Dispatcher** (EAT-QUEUE): after parse/order, before `Task(roadmap)`, when Config `queue.decisions_preflight.enabled` is **true**.
- Optional manual runs when reconciling operator picks vs [[3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention|Decisions-Log-Operator-Pick-Convention]].

## Inputs

| Input | Required | Default |
|-------|----------|---------|
| `project_id` | yes | — |
| `roadmap_dir` | no | `1-Projects/<project_id>/Roadmap/` |
| `tracked_decision_ids` | no | From Config `queue.decisions_preflight.tracked_decision_ids` |
| `stale_scan_paths` | no | From Config — filenames relative to `roadmap_dir` |

## Steps (read-only)

1. **Resolve paths:** `decisions_log = <roadmap_dir>/decisions-log.md`. If missing → emit `recommendation: proceed`, `error: decisions_log_missing`, empty maps.
2. **Read** `decisions-log.md` full text.
3. **Extract `resolved_ids`:** For each id in `tracked_decision_ids`, treat as resolved if **either**:
   - a line matches `(?i)Operator pick logged\s*\([^)]+\):` and the **same line or preceding 30 lines** contains that id (e.g. `D-044`), **or**
   - id-specific pattern: **D-044** / **D-032** — `RegenLaneTotalOrder_v0` / `SimulationRunControl` / `Option [AB]` on an Operator pick line; **D-059** — `ARCH-FORK-0[12]` on an Operator pick line; **D-037** — `Operator confirm` or `Operator defer` mentioning `facet-manifest` or **D-037**.
4. **Read** each file in `stale_scan_paths` under `roadmap_dir` (skip if missing).
5. **Heuristic stale surfaces:** For each `resolved_id`, if **roadmap-state.md** (when present) contains that id and any of: `remain **open**`, `until **D-`, `A/B** is logged`, `pending operator`, `HOLD** until **D-` (case-insensitive sufficient) **without** a same-file phrase `Operator pick logged` / `resolved` near that section — append to `stale_surfaces` with `path`, `reason`, `suggested_action`: `recal` | `deepen_with_guidance` | `manual` (default `recal` for rollup drift).
6. **Fingerprint:** `sha256` or short hash of normalized `decisions_log` tail (last 4000 chars) + `resolved_ids` joined — document as opaque string for run-to-run logging.

## Output (required YAML block)

Emit exactly one fenced block the Queue can paste under `## handoff_addendum.decisions_preflight`:

```yaml
decisions_preflight_schema_version: 1
project_id: "<project_id>"
decisions_fingerprint: "<short hash or opaque id>"
resolved_ids:
  - "D-044"
tracked_decision_ids:
  - "D-044"
stale_surfaces:
  - path: "1-Projects/<project_id>/Roadmap/roadmap-state.md"
    reason: "rollup mentions D-044 HOLD while decisions-log records Operator pick"
    suggested_action: "recal"
recommendation: "proceed"   # proceed | warn | block_dispatch (v1: use warn if stale_surfaces non-empty)
preflight_timestamp_utc: "<ISO8601>"
```

- **`recommendation`:** `warn` if `stale_surfaces` non-empty; else `proceed`. **Do not** use `block_dispatch` unless an explicit future Config enables it.

## Invariants

- **No writes** — no MCP move, no queue file, no Watcher from this skill (Queue may append Watcher after reading output).
- **Bounded I/O** — only `decisions-log.md` + listed `stale_scan_paths`; do not crawl the vault.
- **Advisory** — Roadmap subagent uses the block to prioritize narrative reconciliation; it does not auto-clear validator codes.

## See also

- [[3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention]]
- [[3-Resources/Second-Brain/Queue-Sources]] — EAT-QUEUE Step A.4b
- [[.cursor/rules/agents/queue.mdc]]
