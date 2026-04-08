---
title: Amendment — Frontend player UX (PC swap, schedules, non-goals, lore surface)
created: 2026-04-08
tags:
  - conceptual-amendment
  - sandbox-genesis-mythos-master
  - roadmap
  - frontend-ux
para-type: Resource
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]]"
amends_section: "## Phase 4.2 - Session orchestration and perspective control coherence"
amendment_kind: operator-design-capture
source: chat-thread-2026-04-08
links:
  - "[[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]]"
  - "[[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]]"
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
---

# Amendment — Frontend player UX (2026-04-08)

**Authority:** This note captures **operator-authored design direction** that was previously **chat-only**. It amends the **behavioral intent** of session/perspective orchestration ([[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]]) for **player-facing** flows and **long-horizon** play. Execution-track mirrors must implement these as **AC rows and interfaces** when Phase **4** execution notes exist; until then, this amendment is the **conceptual hook** for deepen/expand.

**Scope:** Consumer-session UX for **multi-character** play in a **persistent world** (hundreds of hours, multiple campaigns, multiple PCs per player where allowed). **Out of scope:** shrinking or replacing the **developer** Second Brain PARA/queue tooling — the product may **borrow patterns** (Markdown vault, links, append-only chronicle) as a **serialization and human-audit surface**, not as shipping the para-zettel autopilot inside the VTT.

## Binding UX decisions

### 1. Multi-PC swap (GTA V–style)

- **Gesture:** When switching the active player character, use a **zoom-out → aerial/map traverse → zoom-in possess** sequence (same *class* of transition as GTA V character switch): the camera leaves the current body, travels to the target character’s location in the world, then **possesses** the new body.
- **Continuity:** Prior character becomes **NPC / off-camera** per existing orchestration rules; **no** hard session reload for swap.
- **Interface expectation:** Perspective transition graph ([[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]) must admit this transition **class** as a first-class **PerspectiveTransition** (labels + ordering vs session hooks).

### 2. Schedules — propose / approve / override

- **Players** may **propose** in-world schedules (when their characters are active, what they intend to do, recurring commitments, etc.).
- **DM** has **exclusive approval**: schedules take effect only after **DM approve** or are applied as **DM override** (including veto or rewrite).
- **No** player-unilateral hard commitment that bypasses DM authority lane (aligns with Phase 4 **single authority lane** + Phase 3 scheduling seams).

### 3. Non-goals (explicit)

- **Mobile / tablet spectator client** (read-only codex + 2D minimap while host runs 3D): **explicitly deprioritized** — not a roadmap commitment until a future operator/product decision elevates it.

### 4. Lore and history (product layer)

- **Markdown** / **Obsidian-compatible** trees are a **serialization and authoring surface** for chronicle, faction history, and audit — suitable for **multi-session, multi-campaign** persistence and LLM-friendly parse.
- **Not** a proposal to embed the vault’s **automation spine** (queues, MCP, PARA pipelines) in the shipped runtime.

## Living-world context (ties to prior design threads)

- Worlds are **multi-session, multi-campaign**; players may run **more than one character** in the same persistent world.
- **Player → DM feedback** and **living simulation** remain governed by the modular spine; this amendment only fixes **how swapping and scheduling feel** at the consumer surface and **what we do not build** (mobile spectator) in the near term.

## Conceptual → execution handoff checklist (self-check)

Per [[3-Resources/Second-Brain/Docs/Conceptual-Execution-Handoff-Checklist|Conceptual-Execution-Handoff-Checklist]] for the **delta** this amendment introduces:

| # | Requirement | Status |
|---|-------------|--------|
| 1 | **Scope** | In: PC swap class, schedule gate, lore serialization *pattern*, long-horizon play. **Not in:** dev PARA reduction, mobile client. |
| 2 | **Behavior** | Actors: player, DM, system orchestration. Ordering: propose → DM gate → commit to session hooks. |
| 3 | **Interfaces** | Binds to **PerspectiveTransitionGraph**, session orchestration envelope, Phase 3 scheduling/checkpoint seams. |
| 4 | **Edge cases** | Mid-swap disconnect; DM reject; concurrent proposals — **TBD** at execution leaves with explicit AC. |
| 5 | **Open questions** | Animation budget; max swap distance; anti-grief on proposals — list at execution deepen. |
| 6 | **Pseudo-code readiness** | Execution mirror Phase 4.2+ should add **typed transition** + **schedule intent** stubs. |

## Next steps for operators

1. **Fold** this amendment into the **conceptual** Phase 4.2 note body (via **`RESUME_ROADMAP` `expand`**) or keep as standalone **linked authority** until expand runs.
2. When **execution** Phase **4** mirror exists, **`deepen`** leaves with `user_guidance` citing this path + Dual-Roadmap **mirror block** (see [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track#Execution path hand-off (queue / operator)|Dual-Roadmap-Track § Execution path hand-off]]).
3. **Do not** re-queue **`bootstrap-execution-track`** if [[Execution/roadmap-state-execution]] already shows a live execution tree (sandbox: **first mint 2026-04-10** per [[decisions-log]] **D-Exec-operator-reset-2026-04-10**).

## Link back

Parent: [[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120#Phase 4.2 - Session orchestration and perspective control coherence]].
