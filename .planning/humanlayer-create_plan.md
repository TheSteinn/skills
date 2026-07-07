# Analysis: HumanLayer V1 `create_plan.md`

**Artifact:** `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/create_plan.md` (450 lines)
**Frontmatter:** `description: Create detailed implementation plans through interactive research and iteration`, `model: opus`
**Context:** V1 command from the "Research → Plan → Implement" (RPI) methodology, later replaced by "QRSPI" (Question → Research → Design → Structure → Plan → Worktree → Implement → PR). Analyzed as an archaeological artifact for inferring how QRSPI came to be.

---

## 1. Purpose

This is a **single slash command** (`/create_plan`) that drives an LLM agent through producing a detailed, phased implementation plan document. The opening framing (line 8):

> "You are tasked with creating detailed implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications."

How it's meant to run:
- **Invoked with or without parameters.** With a ticket/file path (`/create_plan thoughts/allison/tickets/eng_1234.md`) it skips the greeting and starts research immediately (lines 14-18). Without, it prints a canned prompt asking for task description, context/constraints, and links, then waits (lines 19-34).
- **Extended-thinking escalation is a documented trigger:** line 31 tells the user "For deeper analysis, try: `/create_plan think deeply about ...`".
- The intended output is a Markdown plan written to `thoughts/shared/plans/YYYY-MM-DD-ENG-XXXX-description.md` (line 172), then indexed via `humanlayer thoughts sync` (line 282).
- The command itself only **plans** — it does not implement (that was RPI's separate `implement_plan.md`). But it defines the per-phase pause gates and success criteria that an implementation agent later consumes.

The control flow is a linear five-step pipeline under `## Process Steps`: **Step 1 Context Gathering & Initial Analysis → Step 2 Research & Discovery → Step 3 Plan Structure Development → Step 4 Detailed Plan Writing → Step 5 Sync and Review**, followed by five reference sections (`Important Guidelines`, `Success Criteria Guidelines`, `Common Patterns`, `Sub-task Spawning Best Practices`, `Example Interaction Flow`).

---

## 2. What it does well

**Sub-agent / parallel-research architecture.** The strongest design element. It delegates research to seven named read-only specialist agents rather than doing it inline: `codebase-locator`, `codebase-analyzer`, `codebase-pattern-finder`, `thoughts-locator`, `thoughts-analyzer`, `linear-ticket-reader`, `linear-searcher` (lines 51-54, 108-117). It insists on **parallel spawning** ("use specialized agents to research in parallel", line 50; "Spawn multiple tasks in parallel for efficiency", line 404) with a concrete pseudo-example (lines 425-433), and demands **`file:line` references** in returns (lines 62, 124, 417). The dedicated `## Sub-task Spawning Best Practices` section (lines 400-433) is genuinely good agent-orchestration guidance — especially "Be EXTREMELY specific about directories" (line 411, e.g. `humanlayer-wui/` not "UI") and "Verify sub-task results... Don't accept results that seem incorrect" (lines 419-422).

**Skepticism / anti-sycophancy instructions.** "Be Skeptical: Question vague requirements... Don't assume - verify with code" (lines 308-312). The best instance is Step 2.1 (lines 95-99): **"If the user corrects any misunderstanding: DO NOT just accept the correction — Spawn new research tasks to verify... Only proceed once you've verified the facts yourself."** That actively resists a user overriding ground truth.

**"Read files FULLY" discipline.** Repeated hard-line anti-laziness rules: "read entire files" without limit/offset (line 45), "**CRITICAL**: DO NOT spawn sub-tasks before reading these files yourself in the main context" (line 46), "**NEVER** read files partially" (line 47), and again at lines 63-66 and 321.

**The automated-vs-manual success-criteria split.** Distinctive and durable. Every phase must carry two checklists (lines 227-238), and there's a whole `## Success Criteria Guidelines` section (lines 345-376) defining "Automated Verification (can be run by execution agents)" vs "Manual Verification (requires human testing)" with a worked example. It even nudges toward `make` targets over raw commands (line 325). This is the machine/human contract an implementer needs.

**Scope control and completeness gates.** The template mandates a **"What We're NOT Doing"** section (lines 202-204) against scope creep, and the `## Important Guidelines` include **"No Open Questions in Final Plan"** (lines 338-343): "If you encounter open questions during planning, STOP... Every decision must be made before finalizing the plan."

**Alignment steps exist (in intent).** Two collaboration gates are present: Step 2.4 "Present findings and **design options**" with Option A/B pros/cons and "Which approach aligns best with your vision?" (lines 128-145), and Step 3 "Create initial plan **outline**" + "**Get feedback on structure** before writing details" (lines 151-166). The philosophy is stated explicitly: "Be Interactive: **Don't write the full plan in one shot** — Get buy-in at each major step" (lines 314-318). The *idea* was right; the problem was enforcement (see §3).

**Artifact conventions.** A concrete dated, kebab-case, ticket-numbered filename scheme with worked examples (lines 172-179), a fixed template (lines 182-277), and a sync/indexing step (`humanlayer thoughts sync`, lines 282, 302).

---

## 3. What it does poorly

**Instruction-budget overflow — the count is worse than the "85+" critique claims.** Counting discrete imperative directives (top-level numbered items plus their instructional sub-bullets, excluding template/example body text), I get **roughly 120-135 instructions**. Section-by-section tally:

| Section | ~Instructions |
|---|---|
| Initial Response | 6 |
| Step 1: Context Gathering | 20 |
| Step 2: Research & Discovery | 17 |
| Step 3: Plan Structure | 2 |
| Step 4: Detailed Plan Writing | 3 (+ large template) |
| Step 5: Sync and Review | 10 |
| Important Guidelines (6 categories × ~4 sub-bullets) | 31 |
| Success Criteria Guidelines | 10 |
| Common Patterns (3 × ~5) | 17 |
| Sub-task Spawning Best Practices | 16 |
| **Total** | **~130** |

Even a conservative "top-level only" count clears 85. Against the known ceiling that LLMs reliably follow only ~150-200 instructions *total* (and this is one command competing with the system prompt, tool docs, CLAUDE.md, etc.), the prompt is over budget on its own. Predictable consequence: instructions get probabilistically dropped, and the ones most likely to drop are the mid-pipeline collaboration gates.

**The alignment gates are buried and get skipped.** The two "get buy-in" steps (Step 2.4 design options, Step 3 structure feedback) sit in the *middle* of a ~130-instruction monolith with no hard STOP enforcing them — they read as narrative flow, not blocking gates. This is exactly the ~50%-skip failure mode: unless the user supplies "magic words" like *"work back and forth with me starting with your open questions and outline before writing the plan"*, the model races from research straight to writing the file (Step 4). The prompt **relies on user behavior** to trigger its own alignment steps. Contrast the *hard* STOP that does exist — "No Open Questions... STOP" (line 339) — which shows the author knew how to write a blocking gate but didn't apply that force to the alignment steps.

**Actively encourages HORIZONTAL (layer-by-layer) plans.** The `## Common Patterns` section is the smoking gun:
- *For New Features* (lines 388-392): "Start with data model → Build backend logic → Add API endpoints → **Implement UI last**."
- *For Database Changes* (lines 380-385): "Start with schema/migration → Add store methods → Update business logic → Expose via API → Update clients."

Both are bottom-up, one-layer-per-phase recipes — the antithesis of vertical, end-to-end testable slices. The template reinforces this: each phase's "Changes Required" is organized as "**#### 1. [Component/File Group]** → **File:** `path/to/file.ext`" (lines 217-219), i.e. grouped by component/layer, not by user-visible behavior. Nothing in the prompt says "each phase should be independently shippable/testable end-to-end." This is precisely the horizontal-plan pathology QRSPI set out to fix.

**Encourages 1000-line plans not worth reviewing.** The template (lines 182-277) demands ~13 top-level sections — Overview, Current State Analysis, Desired End State, Key Discoveries, What We're NOT Doing, Implementation Approach, N × Phases (each with Overview + Changes + dual Success Criteria + Implementation Note), Testing Strategy (Unit/Integration/Manual), Performance Considerations, Migration Notes, References. Critically, phases embed **actual code**: "```[language] // Specific code to add/modify ```" (lines 221-223). Writing real code into the plan is the fastest path to a 1000-line artifact that duplicates the eventual diff and is too heavy to review.

**Monolithic control flow with maintenance rot.** All research, design, structure, writing, and review live in one prompt with an implicit "do them in order" contract and no state machine. A visible symptom of the monolith being hard to maintain: **Step 2 has two items numbered "3"** — "3. Spawn parallel sub-tasks" (line 103) and "3. Wait for ALL sub-tasks to complete" (line 126). Minor, but it's evidence the mega-prompt wasn't carefully edited.

**Research is duplicated.** RPI already had a separate research command, yet `create_plan` runs its *own* full research pass across Steps 1-2 (locate, analyze, read fully, verify). One command doing both research and planning blurs the phase boundary and re-does work.

**Redundancy inflates the count.** "Read files FULLY" is stated ~4 times (lines 40, 45-47, 63-66, 321); "spawn in parallel / wait for all" appears in Step 1, Step 2, and the Best Practices section. Repetition spends instruction budget without adding new behavior.

---

## 4. Foreshadowing QRSPI

The overhaul's core move is visible here in embryo: **QRSPI took the internal, ordered, skippable Steps 1-5 of this one mega-prompt and promoted each alignment gate into its own first-class phase/command.** Once a gate is a separate invocation, it can't be silently skipped mid-flow and it stops competing for instruction budget inside a single prompt — which directly dissolves the "magic words" problem. Mapping the seams:

- **Q — Question.** Step 1.5 "Present informed understanding and focused questions" + "Only ask questions that you genuinely cannot answer through code investigation" (lines 74-89), reinforced by "No Open Questions in Final Plan... STOP" (lines 338-343). The open-questions/clarification discipline that was a buried sub-step (and needed magic words) became QRSPI's dedicated opening phase.

- **R — Research.** Step 1 (Context Gathering) + Step 2 (Research & Discovery), including the entire seven-agent parallel-research machinery and the `## Sub-task Spawning Best Practices` section (lines 400-433). This carries forward almost intact as QRSPI's standalone Research phase — and separating it removes the duplication noted in §3.

- **D — Design.** Step 2.4 "Present findings and **design options**" — Option A/B with pros/cons and "Which approach aligns best with your vision?" (lines 128-145). This ~50%-skipped inline gate became QRSPI's dedicated **Design** phase, so choosing an approach is now a mandatory checkpoint rather than a paragraph the model can skim past.

- **S — Structure.** Step 3 "Create initial plan **outline**" + "**Get feedback on structure** before writing details" (lines 147-166). Promoted to QRSPI's dedicated **Structure** phase. This is almost certainly where the horizontal→vertical fix lives: structure is where phase slicing is decided, and making it a first-class phase (instead of a two-line buried step against the layer-by-layer `Common Patterns` recipes) is how QRSPI enforces vertical, testable slices.

- **P — Plan.** Step 4 Detailed Plan Writing + the template (lines 168-277). Survives as the **Plan** phase, presumably slimmed — dropping the "write actual code into the plan" instinct (lines 221-223) and the ~13-section template that produced 1000-line artifacts.

- **W — Worktree.** Genuinely new, but its ancestor concern is here: Step 5.1 "Sync the thoughts directory" via `humanlayer thoughts sync` (lines 281-282) — the "manage/index the artifact and its environment" step. QRSPI formalizes environment isolation into a Worktree phase.

- **I — Implement.** `create_plan` doesn't implement, but it writes the implementer's contract: the per-phase **"Implementation Note: ... pause here for manual confirmation from the human ... before proceeding to the next phase"** (line 240) and the dual automated/manual success criteria (lines 227-238, 345-376). Those human checkpoints and machine/human verification splits become the backbone of QRSPI's Implement phase.

- **PR.** Essentially absent — the closest is the `## References` section linking ticket/research/similar implementations (lines 272-277). The PR phase is a net-new addition in QRSPI, not an extraction.

**Net reading:** V1 `create_plan` already contained *most* of QRSPI's conceptual phases (Q, R, D, S, P) and even the intent behind them ("get buy-in at each major step"). What it lacked was **enforcement and separation** — the phases were sub-steps in one ~130-instruction monolith, ordered but not gated, so they overflowed the instruction budget and got skipped without magic words. QRSPI's overhaul is less an invention of new ideas than a **re-architecture**: extract each buried gate into its own invocation with a hard checkpoint, split research from planning, add explicit vertical-slice structuring, and add the missing Worktree/PR bookends.
