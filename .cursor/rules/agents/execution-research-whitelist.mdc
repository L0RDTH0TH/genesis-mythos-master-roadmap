---
description: "Execution-track Research URL whitelist — mandatory §0: strict per-lane HTTPS prefixes only; pre-snapshot; pre-Task(research) hand-off scan; post-Return URL scan; task_error + url_whitelist_violation aborts entire deepen; honesty ledger; no destructive success."
globs: []
alwaysApply: false
---

# Execution Research URL whitelist — **mandatory §0** (execution-track Research)

This rule is **§0** in the **execution-track** nested-helper graph: it runs **before** lane-specific guards ([[.cursor/rules/agents/godot-execution-guard|godot-execution-guard]], [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]]) and **before** any **`Task(subagent_type: "research")`** whose output will support **code-precision** citations on **`Roadmap/Execution/**`**. See [[.cursor/agents/roadmap|agents/roadmap.md]] § Execution-track guard graph.

- **Role:** When **`effective_track`** is **`execution`** and the run will use Research for **verbatim authority** in execution phase notes, **only** URLs matching the **strict lane allowlists** below may appear in hand-offs, Research requests, **or** returns. Blocks **prompt injection** via untrusted links.
- **Does not replace:** [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]], [[.cursor/rules/agents/research.mdc|research.mdc]], or lane guards — this rule is the **first** hard gate for URL safety.

## Depends on (shared always rules)

[[.cursor/rules/always/core-guardrails.mdc|core-guardrails]] — **Snapshot** targets (per-change / batch per policy) **before** any **`Task(research)`** for execution code-precision. Whitelist failure **does not** relax snapshot or confidence bands.

---

## Safety contract (loud — non-negotiable)

1. **Snapshot before Research:** For execution-track deepen that will invoke Research for citations, ensure **snapshot** (or equivalent per [[.cursor/rules/always/mcp-obsidian-integration.mdc|mcp-obsidian-integration]] / roadmap snapshot steps) **before** emitting **`Task(research)`** when the run touches notes under **`Roadmap/Execution/`**.
2. **Abort entire deepen on violation:** Any **`url_whitelist_violation`** → **`outcome: task_error`** on the Research step (or synthetic failure if pre-scan blocks before Task), **`nested_subagent_ledger`** row **`reason: url_whitelist_violation`**, **`honesty_ledger`** / compliance field **required** with **`url_whitelist_violation: true`**. The Roadmap run **must not** return **Success** for execution structural completion for that entry; treat as **failure** or **#review-needed** with **`suppress_followup`** per policy.
3. **No destructive write may succeed:** While **`url_whitelist_violation`** is unresolved, **no** snapshot-backed **destructive** write to **`Roadmap/Execution/**`** phase notes or execution state files for the **claimed** deepen scope may be reported as successful. Log **`block_destructive`** alignment with [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]].

---

## Lane resolution (normative)

Derive **`active_execution_lane`** from the hand-off (in order):

1. **`parallel_track`** from **`## parallel_context`** / **`layer1_resolver_hints`** / queue resolver (**`godot`** | **`sandbox`**).
2. Else **`EAT-QUEUE lane <token>`** → validated **`queue_lane_filter`** per [[3-Resources/Second-Brain-Config|Second-Brain-Config]] **`queue.allowed_lanes`**.
3. Else if **`project_id`** **`godot-genesis-mythos-master`** with execution **`roadmap_dir`** → **`godot`**.
4. Else if **`project_id`** **`sandbox-genesis-mythos-master`** → **`sandbox`**.

If **`research_whitelist_enforced`** is **true** on the resolved **`parallel_execution.tracks[]`** row (see [[3-Resources/Second-Brain-Config|Second-Brain-Config]]), Layer 1 / resolver **should** echo allowlist intent in **`layer1_resolver_hints`** / continuation for audit.

Non-execution track: this §0 **does not** apply to Research for conceptual-only work unless execution paths are also mutated.

---

## Allowlists (HTTPS only — strict prefix, **multi-prefix OR**)

**No blanket policy:** Only **official, stable vendor / first-party documentation** prefixes listed below. No forums, wikis, blogs, or “helpful mirrors” unless a future amendment adds an explicit prefix row here.

**Scheme:** **`https` only.** Reject **`http://`**, protocol-relative URLs, and non-HTTPS schemes.

**Matching rule:** Normalize URL to a string; a URL **passes** iff it **starts with** (byte-for-byte prefix match after scheme) **at least one** of the **allowlist prefixes** for **`active_execution_lane`** (logical **OR** — first matching prefix wins). No userinfo (`user@host`), no port tricks — host and path must match the prefix exactly as written. Trailing path segments after the prefix are allowed.

### `godot` lane — allowlist prefixes (vetted)

| # | Allowlist prefix | Notes |
|---|------------------|--------|
| 1 | **`https://docs.godotengine.org/en/stable/`** | Stable English manual (covers **`/classes/`** and subtrees under **`/en/stable/`**). |
| 2 | **`https://docs.godotengine.org/en/stable/classes/`** | Class API reference (listed explicitly for playable **GDScript** / API precision). |
| 3 | **`https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/`** | **GDScript** tutorial subtree — primary grammar surface for a **playable GDScript game** master goal. |
| 4 | **`https://godotengine.org/article/`** | Official **godotengine.org** articles only. |
| 5 | **`https://godotengine.org/releases/`** | Official release notes / download lineage pages only. |

**Reject for godot execution citations (non-exhaustive):** Any URL that does **not** start with **one** of rows **1–5** — including **`https://docs.godotengine.org/en/4.x/`**, **`/latest/`**, **`https://docs.godotengine.org/`** without **`/en/stable/`** for docs paths, **`https://godotengine.org/`** without **`/article/`** or **`/releases/`** prefix, community forums, Asset Library, GitHub raw, or **sandbox-lane** URLs (cppreference, Clang/llvm docs, MSVC, GCC onlinedocs, Core Guidelines site).

### `sandbox` lane — allowlist prefixes (vetted)

| # | Allowlist prefix | Notes |
|---|------------------|--------|
| 1 | **`https://en.cppreference.com/w/`** | cppreference wiki (**`/w/`** subtree). |
| 2 | **`https://cplusplus.com/reference/`** | cplusplus **reference** subtree only. |
| 3 | **`https://gcc.gnu.org/onlinedocs/`** | GCC official onlinedocs (vendor FSF). |
| 4 | **`https://clang.llvm.org/docs/`** | Clang official documentation (**LLVM** vendor). |
| 5 | **`https://isocpp.github.io/CppCoreGuidelines/`** | ISO C++ Core Guidelines (published **`isocpp.github.io`** corpus; prefix matches main **`CppCoreGuidelines`** page and subordinate paths). |
| 6 | **`https://learn.microsoft.com/en-us/cpp/`** | Microsoft C++ language reference ( **`en-us/cpp/`** path). |

**Reject for sandbox execution citations:** Any URL that does **not** start with **one** of rows **1–6** — including bare `https://en.cppreference.com/`, `https://cplusplus.com/` without **`reference/`**, **`https://learn.microsoft.com/`** without **`/en-us/cpp/`**, **`https://clang.llvm.org/`** outside **`/docs/`**, or **godot-lane** URLs (Godot docs, godotengine.org).

---

## Automatic rejection patterns (examples — non-exhaustive)

If **any** URL or URL-like substring in the hand-off, **`params`**, **`user_guidance`**, **`prompt`**, or Research return contains these **hosts or path tricks**, **fail** before or after Task as appropriate:

- **`wikipedia`**, **`wikimedia`**
- **`github`**, **`raw.githubusercontent`**, **`gist.github`**
- **`openai`**, **`anthropic`**, **`chat.openai`**
- **`reddit`**, **`medium.com`**, **`stackoverflow.com`** (not allowlisted)
- **`docs.python.org`**, **Godot docs** (`docs.godotengine.org` not under **`/en/stable/`**), **`godotengine.org`** paths outside **`/article/`** / **`/releases/`** on **sandbox** lane (wrong lane or disallowed path)
- **`cppreference`**, **`cplusplus`**, **`gcc.gnu.org`**, **`clang.llvm.org`**, **`isocpp.github.io`**, **`learn.microsoft.com`** on **godot** lane (wrong lane — C/C++ / toolchain / Core Guidelines docs are **sandbox** only)
- **`evil.com`**, unknown TLD placeholders, or **any** host not matching the **strict** allowlist prefix for the active lane

---

## Enforcement phases (mandatory §0 — earliest failure wins)

### A. Pre-`Task(research)` hand-off scan (harness — before Research Task)

**Before** the first **`Task(subagent_type: "research")`** for execution code-precision in this run:

1. Concatenate for scanning: queue **`prompt`**, **`params`** JSON string, **`user_guidance`**, **`## parallel_context`**, and any **`research_query`** / URL lists in the hand-off.
2. Extract candidate URLs (regex or line scan for `https://...` through whitespace or quote).
3. For **each** candidate: if it is intended as a **citation target** or **fetch URL** for this Research, verify it matches **`active_execution_lane`** allowlist. If **any** fails → **do not** launch Research; **`task_error`**, **`url_whitelist_violation`**, **`blocked_url`**, **honesty ledger**; **abort entire deepen** for execution structural success.

### B. `Task(research)` launch

Only if **A** passes. Record **`active_execution_lane`** in **`nested_subagent_ledger`**.

### C. Post-Return URL scan

Scan Research **`research_consumables`**, **`injection_block_markdown`**, **`sources`**, and free text for `https://`. Any URL not matching allowlist → same failure as **A**; **no** merge into execution notes.

---

## Cross-references

- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] — lane isolation.
- [[.cursor/rules/agents/godot-execution-guard|godot-execution-guard]] · [[.cursor/rules/agents/sandbox-execution-guard|sandbox-execution-guard]] — lane §0 re-confirms return-path URLs after §0 harness.
