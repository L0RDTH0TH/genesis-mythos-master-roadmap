---
title: Spin and anti-spin (canonical)
created: 2026-04-08
tags: [second-brain, queue, roadmap, gates, operator]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]]"
---

# Spin and anti-spin (canonical)

## Purpose

This note fixes the **operator mental model** for **spin** so it does not have to be reinvented from telemetry names (`flat_delta`, `suspected_spin`, etc.). Implementation details live in [[.cursor/rules/agents/queue.mdc|queue.mdc]] and [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]; this doc states **intent**.

---

## Spin (what it means)

**Spin** is when automation **repeatedly hits a designed gate that it is not supposed to pass** on the current path, and instead of accepting that block, the stack **keeps trying to move forward through the same choke point** (same action class, same target, same “pass the gate” story).

- A **gate** here is any deliberate **stop** or **non-pass** outcome that policy encodes as correct (validator, little-val, handoff gate, track contract, etc.): the system **should** stop *that* progression until humans or other prerequisites change.
- **Spin** is the *orchestration failure*: treating “try again the same way” as progress when the gate is doing its job.

**Correct response to spin:** **Do not** automate a forced pass through the gate. **Do** look at the **rest of the project** and **expand or advance elsewhere** (different slice, sibling phase, alternate track, structural work that does not require clearing this gate on this run).

---

## What “spin” is not (disambiguation)

| Not this | Notes |
|----------|--------|
| **Roadmaps that contain only gates** | Spin is **not** defined as “the roadmap is nothing but checkpoints.” Normal roadmaps mix open work and gates; spin is about **behavior when a gate blocks**, not about catalog size. |
| **`spin_signal` fields alone** | Telemetry such as `flat_delta_streak` or `suspected_spin` is a **detector layer**. It approximates stagnation; the **meaning** of spin is **gate-block + repeated same-path attempts**. |
| **Busy CPU / hung UI** | Informal “the system is spinning” in other domains is unrelated. |

---

## Anti-spin (what the machinery is for)

**Anti-spin** logic exists so that when **gate-block** or equivalent evidence appears, Layer 1 and roadmap dispatch **prefer lateral motion** instead of hammering the blocked axis:

- **Next-Need Resolver** (`need_class`, `effective_action`, `effective_target`): structural snapshot → hints that point at **missing structure, stale outputs, other phases**, not only “retry deepen at cursor.”
- **`gate_block_signal` / `blocked_track` / `pivot_to_track`**: when the **same track** is repeatedly blocked, **pivot** (e.g. conceptual ↔ execution) instead of re-dispatching the same failing pass on the blocked track.
- **EAT-QUEUE BREAK-SPIN** ([[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]): operator-triggered merge that prefers **alternate deepen targets** before **`recal`** fallback; **`no_gain_pending_user_gates`** when there is no safe alternate and policy forbids noisy automation.

So: anti-spin is **aligned** with the mental model **expand without passing the gate**; telemetry names are **instrumentation**, not the definition.

---

## Related docs

- [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] — BREAK-SPIN, `blocked_track`, Next-Need Resolver
- [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]] — `spin_signal`, `gate_block_signal`, `no_gain_pending_user_gates`
- [[3-Resources/Second-Brain/Docs/Queue-Gate-State-Spec|Queue-Gate-State-Spec]] — durable gate streaks
- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] — where “elsewhere” often is (execution mirror vs conceptual tree)
- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]] — what “gate” means per track
