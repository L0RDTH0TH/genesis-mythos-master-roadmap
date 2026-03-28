---
name: little-val-v2-multi-tier-contract-safety
overview: "Refine the structural validation architecture with a tiered repair flow: pipeline self-checks, little val skill with up to three repair attempts, then validator-assisted repair with up to three more attempts before declaring a true failure."
todos:
  - id: v2-define-outcome-taxonomy
    content: Lock in the formal definitions and tags for review needed, unrepairable, and true failure across pipelines.
    status: pending
  - id: v2-little-val-loop-design
    content: Specify little val’s v2 contract and 3-attempt repair loop inside each pipeline subagent.
    status: pending
  - id: v2-validator-repair-flow
    content: Design the validator-assisted repair flow with up to 3 structural fix attempts before declaring unrepairable/true failure.
    status: pending
  - id: v2-quality-validator-integration
    content: Describe how quality validators consult little val and how they behave when underlying structure is not ok.
    status: pending
isProject: false
---

## Little val v2 multi-tier structural safety

### Definitions (shared vocabulary)

- **review needed**: A run where the pipeline and little val could not reach structural `ok` after little val’s three attempts, so the system **loops in the validator** for assisted repair rather than treating it as a hard failure.
- **unrepairable**: A run that has been through both little val’s three attempts **and** up to three validator-assisted repair attempts and **still** has structural contract failures.
- **true failure**: A run classified as unrepairable after validator assistance fails to produce a structurally valid success; this is the point where automation stops trying to fix it and you must intervene.
- **little val max tries**: 3 structural check/repair cycles inside the pipeline subagent.
- **validator fix max tries**: 3 structural repair attempts coordinated via the validator/audit subagent.

### Phase 1: Pipeline + little val tier (up to 3 attempts)

- **1. Establish the v2 structural contract per pipeline**
  - For each pipeline (Roadmap, Ingest, Archive, Organize, Distill, Express), define:
    - **Success artifacts**: the minimal set of files/logs/snapshots that must exist and be internally consistent when the run is genuinely successful.
    - **Allowed non-success outcomes**:
      - `review needed` (after little val and/or validator attempts, no structural `ok` yet but state is still interpretable),
      - `true failure` (after validator assistance, system cannot find a safe path to `ok`).
    - **Non-goals**: content quality; those remain the domain of the big validator modes.
- **2. Design little val v2 skill contract**
  - Inputs (from a pipeline subagent at the end of its normal steps):
    - `mode`, `params`, `project_id`, `queue_entry_id`, optional `parent_run_id`.
    - Paths to the key artifacts for this run (e.g. workflow_state, pipeline logs, target note, known snapshot paths).
  - Outputs (conceptual):
    - `ok: boolean` — current artifacts vs claimed outcome status.
    - `missing: string[]` — structural items that are absent or malformed (e.g. "workflow_state log row for this deepen", "snapshot before move", "Express-Log entry").
    - `hint: string` — concise guidance on how the pipeline should repair (e.g. "append a log row with phase N+1 and context metrics").
    - Optional `severity` or `category` for future auditing (e.g. `"missing-log"`, `"missing-snapshot"`).
- **3. Integrate little val with a 3-attempt repair loop in each subagent**
  - **Roadmap subagent example**:
    - Step A: Run the requested action (e.g. `deepen`): update notes, append workflow_state row, compute context-tracking metrics.
    - Step B: Call little val with roadmap-specific artifacts.
    - Step C: If `ok: true`, finalize Run-Telemetry and return `Success`.
    - Step D: If `ok: false`:
      - Use `missing`/`hint` to perform a targeted repair (e.g. re-write the last workflow_state row, backfill missing metrics, adjust snapshot markers).
      - Call little val again to re-check.
      - Track the number of attempts (1–3).
    - Step E: After **3 attempts**, if little val still returns `ok: false`:
      - Do **not** call this `Success`.
      - Return a status of `**review needed`**, explicitly flagged as a **structural glitch** and including the last little val verdict in the summary.
  - **Other pipelines (Ingest, Archive, Organize, Distill, Express)**:
    - Mirror the same pattern: run core work → little val check → up to 3 repair attempts guided by `missing`/`hint` → escalate as `review needed` if structural `ok` is still not achievable.
- **4. Mapping outcomes after Phase 1**
  - If little val reaches `ok: true` at any attempt:
    - Pipeline may return `**Success`**; queue can treat it as structurally sound.
  - If little val still says `ok: false` after attempt 3:
    - Pipeline returns `**review needed`**, tagged with something like `structural_glitch: true` and the little val verdict; this becomes input to Phase 2.
  - **Invariant**: no pipeline run may return `Success` when the final little val verdict is `ok: false`.

### Phase 2: Validator-assisted repair tier (up to 3 attempts)

- **5. Define validator-assisted structural repair flow**
  - **Trigger condition**:
    - A run is marked `review needed` due to a structural glitch after little val’s 3 attempts.
  - **Queue orchestration (conceptually)**:
    - When EAT-QUEUE or a dedicated audit mode sees such a run, it enqueues or dispatches a **structural-validator** invocation (either via a new mode or an extended `validation_type` on the existing Validator).
  - **Validator’s responsibilities**:
    - Read the run’s telemetry, logs, and state files, plus little val’s last verdict.
    - Re-run the same shared little val core logic in its own context to confirm the structural discrepancies.
    - Propose **specific repair actions** that a future pipeline run (or the validator, if allowed) could apply safely.
- **6. Validator fix max tries: 3 repair-focused passes**
  - Each **validator-assisted attempt** can:
    - Either be a **pure diagnostic pass** that outputs a report and a recommended repair recipe; or
    - In a more advanced variant, coordinate a small, constrained fix (e.g. rewriting a malformed workflow_state section, regenerating a missing log entry), if allowed by your safety rules.
  - Up to **3 such validator-assisted cycles** may be run, each time checking via the shared little val core whether the structure is now acceptable.
  - After each validator attempt:
    - If the next pipeline run (or a dry-run check) brings little val to `ok: true`, that run can finally be marked `**Success`**.
    - If not, the validator may revise its repair suggestions and try again (up to its max of 3).
- **7. Classifying unrepairable and true failure**
  - **Unrepairable**:
    - A run for which:
      - little val’s 3 attempts have all failed **and**
      - validator’s **3 repair-oriented attempts** also fail to reach a consistent `ok: true` state when re-checked by little val.
    - At this point, the best the system can do is produce a detailed report describing why the structure cannot be auto-repaired.
  - **True failure**:
    - The final classification for unrepairable runs.
    - The pipeline/validator must:
      - Record this with an explicit `true_failure` tag and `error_type` like `structural_contract_unrepairable` in Errors.md or an audit log.
      - Avoid additional automated attempts on the same broken state unless you explicitly trigger them.

### Phase 2+: Tying little val into quality validators

- **8. Make little val a prerequisite lens for quality validators**
  - For quality-focused validators (e.g. roadmap handoff, distill readability, express summary):
    - Before judging quality, call the shared little val core (in read-only mode) to confirm the underlying state is structurally sound.
    - Behaviours:
      - If little val says `ok: true`:
        - Proceed with normal quality validation.
      - If little val says `ok: false`:
        - Either:
          - Return a quality report that is explicitly blocked/prefaced by structural issues ("cannot meaningfully grade handoff while workflow_state is inconsistent"), or
          - Short-circuit and treat this as a structural issue that must be addressed via the Phase 1+2 repair path before quality is assessed.
- **9. Observability for the multi-tier flow**
  - Ensure logs and telemetry distinguish:
    - Runs where little val repaired glitches internally (e.g. `contract_glitch_repaired: true`, `lv_attempts: 2`).
    - Runs where little val escalated to `**review needed`** and validator took over.
    - Runs that ended as **unrepairable / true failure**.
  - This will let you track, over time:
    - How often hallucinated completions occur.
    - How effective little val and validator are at repairing them.
    - Which pipelines are most fragile structurally.

### Invariants across v2

- **No Success without structure**: final status `Success` is only allowed when the last little val verdict is `ok: true`.
- **Repair-first mindset**: structural mismatches first trigger up to 3 little val repair attempts, then up to 3 validator-assisted repair cycles, before the system accepts a `true failure`.
- **Clear outcome taxonomy**: every problematic run is labeled as either `review needed` (validator in play), `unrepairable`, or `true failure`, with logs explaining which tier failed and why.
- **Single shared logic**: little val’s core contract-checking logic is reused consistently in both in-pipeline checks and validator/audit flows, so the definition of “structurally ok” stays unified.

