# Analysis: `iterate_plan.md` (HumanLayer RPI V1 command)

**Source file:** `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/iterate_plan.md`
**Sibling compared:** `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/create_plan.md`
**Length:** 250 lines. Frontmatter sets `model: opus` and `description: Iterate on existing implementation plans with thorough research and updates`.

**Structure at a glance** — 6 top-level `##` sections after the title:
1. `## Initial Response`
2. `## Process Steps` (contains 5 `###` steps)
3. `## Important Guidelines` (6 numbered guidelines)
4. `## Success Criteria Guidelines`
5. `## Sub-task Spawning Best Practices` (7 numbered practices)
6. `## Example Interaction Flows` (3 scenarios)

The 5 process steps are: **Step 1** Read and Understand Current Plan, **Step 2** Research If Needed, **Step 3** Present Understanding and Approach, **Step 4** Update the Plan, **Step 5** Sync and Review.

---

## 1. Purpose

This is a **revision command**: it takes an *already-written* implementation plan plus user feedback and surgically edits the plan file in place. The opening line states the job directly: *"You are tasked with updating existing implementation plans based on user feedback. You should be skeptical, thorough, and ensure changes are grounded in actual codebase reality."* (line 8).

**How it's meant to be run** — the `## Initial Response` section (lines 10–44) parses two inputs — a *"Plan file path (e.g., `thoughts/shared/plans/2025-10-16-feature.md`)"* and *"Requested changes/feedback"* — and branches on three input scenarios:
- **No plan file** → prompt for the path (with the tip `ls -lt thoughts/shared/plans/ | head`) and *"Wait for user input, then re-check for feedback."*
- **Plan file but no feedback** → ask *"What changes would you like to make?"* with four canned examples ("Add a phase for migration handling", "Update the success criteria...", "Adjust the scope to exclude feature X", "Split Phase 2 into two separate phases") and *"Wait for user input."*
- **Both provided** → *"Proceed immediately to Step 1 / No preliminary questions needed."*

The example flows at the end (lines 225–249) confirm the intended invocation, e.g. `User: /iterate_plan thoughts/shared/plans/2025-10-16-feature.md - add phase for error handling`.

The loop is: read the whole plan (Step 1) → optionally research (Step 2) → confirm understanding and get sign-off (Step 3) → Edit-tool surgical changes (Step 4) → `humanlayer thoughts sync` and present a changelog, *"be ready to iterate further"* (Step 5).

---

## 2. What it does well

- **Grounds edits in codebase reality, not just the user's words.** The `## Important Guidelines` "Be Skeptical" block (lines 158–162) says *"Don't blindly accept change requests that seem problematic"*, *"Verify technical feasibility with code research"*, and *"Point out potential conflicts with existing plan phases."* Step 2 gates research on genuine need: *"**Only spawn research tasks if the changes require new technical understanding.**"* (line 62).
- **Surgical-edit discipline.** Step 4 mandates *"Make focused, precise edits"* with *"the Edit tool for surgical changes"* and *"Maintain the existing structure unless explicitly changing it"* (lines 115–120); the "Be Surgical" guideline reinforces *"Make precise edits, not wholesale rewrites"* and *"Preserve good content that doesn't need changing"* (lines 165–166). This is sensible for a large existing artifact.
- **A confirmation gate before writing.** Step 3 (lines 91–111) requires presenting understanding + research findings + intended edits, then *"Get user confirmation before proceeding."* This prevents wasted edits on a misread.
- **Consistency maintenance across coupled sections.** Step 4 lists the ripple effects of a change: *"If modifying scope, update 'What We're NOT Doing' section"* and *"If changing approach, update 'Implementation Approach' section"* (lines 123–124), and *"Keep all file:line references accurate"* (line 118).
- **The Automated vs. Manual success-criteria split** (lines 193–208) is genuinely useful and carries a good concrete rule: *"Prefer `make` commands: `make -C humanlayer-wui check` instead of `cd humanlayer-wui && bun run fmt`"* (line 199).
- **Anti-loose-ends rule.** "No Open Questions" (lines 187–191): *"Do NOT update the plan with unresolved questions... Every change must be complete and actionable."*

---

## 3. What it does poorly

### 3a. Instruction-budget overflow
Counting discrete imperative directives (numbered items and normative sub-bullets, not the descriptive template lines) yields roughly **60–75 instructions** in this single file. Rough breakdown: Initial Response ~5, Step 1 ~7, Step 2 ~7, Step 3 ~2, Step 4 ~12, Step 5 ~3, Important Guidelines ~23 (6 guidelines × 3–4 sub-bullets), Success Criteria ~8, Sub-task Spawning ~7. That is under the ~150–200 hard ceiling from Dex Horthy's talk but **well over the QRSPI target of <40 instructions per prompt** — and this command never runs alone; it presupposes a plan produced by `create_plan.md` (another opus-heavy prompt), so the effective budget the agent carries is the *union* of the two.

### 3b. Iterating on the finished plan is late and low-leverage
Step 1 orders: *"Read the existing plan file COMPLETELY — Use the Read tool WITHOUT limit/offset parameters"* (lines 50–51). Every iteration re-ingests the entire plan — which, per the V1 failure mode, can be ~1000 lines — then makes point edits, presents a changelog, waits for feedback, and repeats. The command is structurally the *"plans have surprises / reviewing the plan costs as much as reviewing the code"* problem made into a workflow: the artifact being iterated is the most expensive one in the pipeline, and it only exists *after* `create_plan` has done all the research and drafting. The four example feedback prompts it seeds are all late-stage structural churn — *"Add a phase for migration handling"*, *"Split Phase 2 into two separate phases"*, *"Adjust the scope to exclude feature X"* (lines 36–38) — exactly the decisions that are cheap to change in a design sketch and expensive to change in a full plan.

### 3c. Heavy duplication with `create_plan.md`
`iterate_plan.md` is largely a clone of the back half of `create_plan.md`:
- **`create_plan` already iterates.** Its Step 5 (lines 297–304) says *"Iterate based on feedback - be ready to: Add missing phases, Adjust technical approach, Clarify success criteria..., Add/remove scope items"* and *"Continue refining until the user is satisfied."* So a dedicated iterate command duplicates a loop `create_plan` claims to own.
- **`## Success Criteria Guidelines`** — the Automated/Manual two-category structure is near-verbatim in both (iterate lines 193–208 vs. create lines 345–376).
- **`## Sub-task Spawning Best Practices`** — near-identical numbered lists (iterate 209–223 vs. create 400–423), including the same *"Be EXTREMELY specific about directories"* rule with the identical `humanlayer-wui/` / `hld/` examples (iterate 82–84, create 411–414).
- **Same research-agent roster** (codebase-locator / -analyzer / -pattern-finder, thoughts-locator / -analyzer), same `humanlayer thoughts sync` step, same `make -C humanlayer-wui check` preference, and a parallel `## Important Guidelines` block (both share Be Skeptical, Be Thorough, Be Interactive, Track Progress, No Open Questions; create adds "Be Practical", iterate adds "Be Surgical").

### 3d. Structurally coupled to `create_plan`'s template, but ships none of its own
iterate_plan references sections by name — *"What We're NOT Doing"* and *"Implementation Approach"* (lines 123–124) — and the two-category success criteria, all of which are defined only in `create_plan`'s template (create lines 182–277). iterate_plan carries **no template of its own**, so it silently assumes the plan already conforms to create_plan's shape. Feed it a plan from any other source and the "maintain the existing pattern" instructions (line 122) have nothing to anchor to.

### 3e. Reliance on user prompting / "magic words"
The whole command is a manually-invoked, prose-fed loop: it does nothing until the user supplies a path *and* free-text feedback, and its interactive gates (*"Does this align with your intent?"* line 108; *"Would you like any further adjustments?"* line 151) depend entirely on the user typing the next nudge. There is no first-class artifact or state that drives the iteration — the user is the state machine. (The sibling `create_plan.md` makes the "magic words" pattern explicit at line 31: *"For deeper analysis, try: `/create_plan think deeply about ...`"* — behavior toggled by an incantation in the prompt string.) The very existence of a *separate* `/iterate_plan` command is itself a manual mode-switch: the user has to know to say "now iterate" rather than the workflow naturally supporting revision.

### 3f. Minor
- The "Be Surgical" instruction *"Only research what's necessary"* (line 167) partially contradicts the "Be Thorough" framing and the skeptical *"Verify technical feasibility with code research"* — the prompt leaves the agent to referee thorough-vs-surgical itself.
- 3 worked example scenarios (lines 225–249) restate branching logic already fully specified in `## Initial Response`, adding tokens without new information.

---

## 4. Foreshadowing QRSPI

**What this command's existence implies about V1's pain.** You only build a dedicated, opus-powered, ~250-line command for *revising* plans if plans routinely needed heavy revision after being written. That is the tell: in V1 the **plan was the first place decisions became concrete and reviewable**, so essentially all substantive feedback — approach, phasing, scope — landed on the largest, most expensive artifact in the pipeline. The seeded feedback examples (add a phase, split a phase, cut scope) are architecture-level decisions that should have been settled *before* a detailed plan was drafted. iterate_plan is a bandage over "we aligned too late."

**Why plans needed so much iteration.** Both plan commands bury an alignment gate *inside* the plan-writing flow — create_plan Step 3 asks *"Does this phasing make sense?"* (line 163) and iterate_plan Step 3 asks *"Does this align with your intent?"* (line 108) — but these gates are transient chat turns, not durable artifacts. There was no short, cheap, reviewable document capturing "the approach" or "the phase breakdown" on its own. So disagreement surfaced only once the 1000-line plan materialized, and the only remedy was to re-read and surgically rewrite that plan — i.e., run this command.

**Which QRSPI phases replaced this.** QRSPI (Question → Research → **Design** → **Structure** → Plan → Worktree → Implement → PR) moves alignment *earlier* and onto *cheaper* artifacts:
- The **Design phase (~200-line `design.md`)** is where "the approach" gets reviewed and iterated — replacing iterate_plan's late "change the technical approach / adjust scope" churn. Iterating a 200-line design is cheap; iterating a 1000-line plan is not.
- The **Structure phase (~2-page `structure.md`)** is where the phase/file breakdown gets agreed — replacing iterate_plan's "split Phase 2", "add a phase for migration" churn, and create_plan's embryonic *"Does this phasing make sense?"* gate. Both are promoted from throwaway chat turns into first-class, sign-off-able artifacts.
- By the time QRSPI reaches **Plan**, the expensive decisions are already locked, so the plan is largely mechanical and there is little left to "iterate" — which is why QRSPI has no `iterate_plan` equivalent. Revision moved upstream to design/structure review.

**Continuities that survived.** The Automated-vs-Manual success-criteria split and the *"pause here for manual confirmation from the human"* gate (defined in create_plan line 240) are good V1 ideas that carry forward conceptually into QRSPI's Implement phase. iterate_plan's surgical-edit discipline is really a *coping mechanism* for oversized plans; QRSPI addresses the root cause by keeping every artifact small (<40 instructions per prompt; ~200-line and ~2-page artifacts), so "surgical vs. rewrite" stops being a dilemma.
