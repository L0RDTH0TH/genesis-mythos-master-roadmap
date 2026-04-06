---
name: config-resolve-profile
description: Expands familial profile keys (speed_mode, repair_strategy, validator_tier) into flat Second-Brain-Config-shaped params via deepMerge for queue entries and Prompt Crafter summaries. Supports single-key, combo (+) syntax, bare tokens, default bundle when absent, and graceful unknown-token handling with config_profile_unknown telemetry.
---

# config-resolve-profile

## When to use

- **Prompt Crafter** — step 9 payload assembly: **always** run the resolver for modes that emit **`params`** (at minimum roadmap-related queue modes), even when **`params`** omits familial keys (default bundle applies).
- **Queue Layer 1** — **A.2**: **always** run the resolver for every parsed JSONL line **after** `JSON.parse`, before **A.2a** lane filter and before any dispatch / **A.4c** / Pass 3 reads of **`queue.*`** / **`validator.*`**.

## Input formats (normative)

Familial keys may appear on **`params`** (or top-level, if your parser hoists them) in any of these forms. **Combine** using one or more mechanisms below; **later-assigned values win** within the same family when duplicates appear.

### 1. Separate JSON fields (canonical)

```json
"params": {
  "speed_mode": "balance",
  "repair_strategy": "repair_first",
  "validator_tier": "forgiving"
}
```

### 2. Single family, scalar value

```json
"params": { "speed_mode": "extreme" }
```

Only **`speed_mode`** is set; **`repair_strategy`** and **`validator_tier`** come from the **default familial bundle** (see **Default familial bundle**) unless also set elsewhere.

### 3. Combo string (`+`)

Put multiple assignments in **one** string value using **`+`** as separator. Trim each segment; split on **`+`** outside of quoted regions (if your implementation supports quotes; otherwise split on **`+`** only).

**Explicit keys:**

```text
speed_mode: balance + repair_strategy: repair_first + validator_tier: forgiving
```

**Valid placements:** the combo may live in **`params.speed_mode`**, **`params.repair_strategy`**, **`params.validator_tier`**, or inside **`params.profiles.<any>`** as a string — parsers should scan any familial field whose value is a string containing **`+`** and treat the **entire** string as a combo to flatten into family assignments.

**Example (single field carries full combo):**

```json
"params": {
  "speed_mode": "balance + repair_strategy: repair_first + validator_tier: forgiving"
}
```

### 4. Bare token segments

A segment **without** `family: value` is resolved by **token lookup** against known value sets (first match in this order):

1. **`speed_mode`**: `fast`, `balance`, `extreme`
2. **`repair_strategy`**: `repair_first`, `forward_first`
3. **`validator_tier`**: `aggressive`, `forgiving`

Example:

```text
balance + repair_first + forgiving
```

assigns all three families. If a token matches **no** known value, treat as **unknown** (see **Unknown families and values**).

### 5. Nested `profiles` object

```json
"params": {
  "profiles": {
    "speed_mode": "balance + repair_first",
    "validator_tier": "forgiving"
  }
}
```

Merge **`profiles`** with top-level **`speed_mode` / `repair_strategy` / `validator_tier`** after each side is normalized; **top-level keys override `profiles`** when the same family is set on both.

## Default familial bundle

If **after parsing** no familial family is set (no `speed_mode`, `repair_strategy`, `validator_tier`, and no usable `profiles` / combo content), apply:

| Family            | Value            |
|-------------------|------------------|
| `speed_mode`      | `balance`        |
| `repair_strategy` | `repair_first`   |
| `validator_tier`  | `forgiving`      |

This matches the documented **default** labels in **[[3-Resources/Second-Brain/Docs/Core/Config-Profiles|Config-Profiles]]** and **[[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]]** § `profiles` (Option B: canonical three-line **default familial bundle** in Config for human parity).

## Merge order (normative)

Same as **Config-Profiles** § deepMerge — **later wins** at the same path:

1. **Implicit defaults** (Parameters / Queue-Sources when Config omits a key).
2. **Second-Brain-Config** flat sections (`queue`, `validator`, `snapshot`, `pipeline_mode`, `validator_profiles`, …).
3. **Profile expansion** from normalized familial keys (including the default bundle when nothing was specified).
4. **Explicit flat keys** on the queue entry / assembled **`params`** (highest precedence).

**Arrays** replace as a whole unless a spec says otherwise.

## Unknown families and values

- **Unknown family name** in `key: value` (e.g. typo in key): emit telemetry event **`config_profile_unknown`** (include raw segment, queue entry id if any); **skip** that segment; continue.
- **Unknown value** for a known family: emit **`config_profile_unknown`**; for that family, fall back to the **default familial bundle** value for that family only (e.g. unknown `speed_mode` → use `balance`).
- **Ambiguous bare token** (matches more than one family — rare if lists stay disjoint): emit **`config_profile_unknown`** with context; prefer **`speed_mode`** if listed first in the resolution pass, or skip segment.

Do **not** fail the queue line solely for unknown profile tokens; **graceful** degradation keeps Layer 1 moving.

## Telemetry

Record **`config_profile_unknown`** in **Run-Telemetry** (or the pipeline log entry for this parse) with: **`timestamp`**, **`queue_entry_id`** (if present), **`raw_segment`**, **`reason`** (`unknown_family` \| `unknown_value` \| `ambiguous_token`). Optional: append a one-line note to **[[3-Resources/Second-Brain/Logs|Logs]]** when high-churn debugging is enabled.

## Inputs (implementation)

- **`familial`**: normalized object with keys `speed_mode`, `repair_strategy`, `validator_tier` (after combo parsing + default injection).
- **`explicit_flat`** (optional): explicit flat overrides already on the queue line (`pipeline_mode`, `queue.*`, `validator.*`, …).
- **Config**: read **Second-Brain-Config** and **Config-Profiles** for mapping tables.

## Output

- **`expanded_flat`**: nested object mirroring Config paths for Layer 1 (e.g. `pipeline_mode`, `queue.roadmap_pass_order`, `queue.inline_a5b_repair_drain_enabled`, `validator.tiered_blocks_enabled`, `snapshot.batch_size_for_snapshot`).
- **`profile_derived`**: map `param_path → boolean` — **true** if value came from profile expansion (including default bundle), **false** if from explicit queue entry (for crafter summary annotations).

## Reference

- **[[3-Resources/Second-Brain/Docs/Core/Config-Profiles|Config-Profiles]]** — families, mapping tables, resolution flow, examples.
