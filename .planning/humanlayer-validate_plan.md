# Archaeology: HumanLayer V1 `validate_plan.md`

Source: `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/validate_plan.md` (167 lines)

An artifact from the V1 "Research → Plan → Implement" (RPI) command set, later superseded by
the QRSPI workflow (Question → Research → Design → Structure → Plan → Worktree → Implement → PR).
This is the command that had **the model check whether the model finished the plan** — which
sits right on the fault line QRSPI was built to fix.

---

## 1. Purpose

This command validates that an **already-implemented** plan was executed correctly. It runs
**after** implementation, not before — it is *not* a pre-implementation review of a plan's
quality.

The evidence is unambiguous:

- Frontmatter description (line 2): *"Validate implementation against plan, verify success
  criteria, identify issues"*.
- Opening charge (line 7): *"You are tasked with validating that an implementation plan was
  **correctly executed**, verifying all success criteria and identifying any deviations or
  issues."*
- The whole flow presumes code already exists: it *"Gather[s] implementation evidence"* via
  `git log`, `git diff HEAD~N..HEAD`, and `make check test` (lines 20-28); it looks for
  completed checkmarks *"`- [x]`"* in the plan (line 65); and it *"can analyze the git history
  to understand what was implemented"* (line 164).
- The stated position in the pipeline (lines 158-164) places it **third**, after execution and
  commits:
  1. `/implement_plan` — Execute the implementation
  2. `/commit` — Create atomic commits
  3. `/validate_plan` — Verify implementation correctness
  4. `/describe_pr` — Generate PR description
  ...with the note (line 164): *"The validation works best after commits are made."*

Note the naming tension: the command is called **`validate_plan`** but what it actually
validates is the **implementation against the plan**. The plan is treated as the trusted spec;
the code is the thing on trial.

How it's meant to be run: invoked either inside the same conversation that did the
implementation, or *"fresh"* (line 12-14), in which case it reconstructs what happened from git
history and codebase analysis. It ends by emitting a structured **Validation Report** (lines
86-127).

---

## 2. What it does well

**Real automated verification, not vibes.** It insists on actually *running* checks, not
asserting they pass. It shells out to `make check test` (line 27) up front and, per phase,
*"Execute[s] each command from 'Automated Verification'"* and *"Document[s] pass/fail status"*
(lines 69-71). Guideline #2 (line 140) is blunt: *"Run all automated checks - Don't skip
verification commands."* The report template models a genuine failure (line 97:
*"✗ Linting issues: `make lint` (3 warnings)"*), i.e. it's allowed to report red.

**Distrusts the checkbox.** The strongest single instruction is lines 64-66: *"Look for
checkmarks in the plan (`- [x]`)"* **and then** *"Verify the actual code matches claimed
completion."* It explicitly refuses to take a `- [x]` at face value and cross-checks it against
the code. Validation checklist item 1 (line 149) repeats this: *"All phases marked complete are
actually done."*

**Separates automated from manual verification.** It treats *"Automated Verification"* (line 68)
and *"manual criteria"* (line 73) as distinct classes, and for manual work it doesn't pretend to
test — it *"Provide[s] clear steps for user verification"* (line 76) and emits a
*"Manual Testing Required"* checklist for a human (lines 114-121). This is an honest admission
that some things only a person can confirm.

**Honesty about deviations, with nuance.** The report has a dedicated *"Deviations from Plan"*
section (line 106) and — notably — distinguishes *bad* drift from *good* drift: line 108 flags
*"Added extra validation in [file:line] (improvement)."* The "Working with Existing Context"
section closes with *"Be honest about any shortcuts or incomplete items"* (line 135). It
partitions findings into three clean buckets: *"Matches Plan"*, *"Deviations from Plan"*,
*"Potential Issues"* (lines 101-113).

**Git as ground truth.** Rather than trusting narrative memory, it anchors on commit history
(`git log --oneline -n 20`, `git diff`, lines 23-24), which is a stronger evidentiary base than
"what the agent remembers doing."

**Looks past the plan for regressions.** It doesn't only check that planned things happened; it
asks whether the change *broke* unplanned things — *"Could the implementation break existing
functionality?"* (line 80) and checklist item *"No regressions introduced"* (line 152).

---

## 3. What it does poorly

**Instruction load is heavy.** Counting explicit directives: ~11 numbered process steps across
Initial Setup + Steps 1-3, plus 4 "Working with Existing Context" bullets, 5 "Important
Guidelines", and a 7-item "Validation Checklist" — roughly **25-30 top-level directives**.
Counting the nested sub-bullets (each step carries 2-3), it's **50+ discrete instructions**, on
top of a mandated report template with **6 required sub-sections** (Implementation Status,
Automated Verification Results, Code Review Findings [3 sub-buckets], Manual Testing Required,
Recommendations). That's a lot of simultaneous demands for a single pass, and much of it is
overlapping (e.g. "all phases marked complete are actually done" appears as both a Step-2
instruction and a checklist item).

**Self-grading — the core problem.** The command is explicitly designed to be run by the same
agent that did the work: *"If you were part of the implementation: Review the conversation
history... Focus validation on work done in this session"* (lines 131-134). The model that
misunderstood a requirement will "validate" its own misunderstanding as correct — the verifier
and the implementer share the same blind spots. Even run *"fresh"*, it's the **same model**
grading the same class of output. The whole exercise is the agent checking its own homework, and
the only safeguard offered is an exhortation to *"Be honest"* (line 135) and to *"Think
critically - Question if the implementation truly solves the problem"* (line 142). Honesty as a
control has no teeth against a shared misconception.

**Aspirational, unverifiable instructions.** Several directives ask for cognition that can't be
observed or checked: *"Think deeply about edge cases"* (line 77), *"Think critically"* (line
142), *"Be thorough but practical - Focus on what matters"* (line 139). A model can emit the
*claim* of having thought deeply while doing nothing of the sort, and nothing in the command
detects the difference.

**No definition of "validated" — no gate.** This is the biggest conceptual gap. The command
produces a report with ✓ / ⚠️ / ✗ markers (lines 90-97) but **never says what outcome constitutes
pass vs fail**, nor what to do about a ⚠️. The template literally shows *"⚠️ Phase 3: [Name] -
Partially implemented"* (line 92) and *"✗ Linting issues"* (line 97) as acceptable report
states — with no threshold, no blocking condition, no "stop and fix before merge" gate. The
closest thing is a soft *"Recommendations"* list (*"Address linting warnings before merge"*, line
124). "Validated" is left as a subjective narrative rather than a decidable predicate.

**Missing / minimized human touchpoints.** The human's only structural role is to *execute* the
"Manual Testing Required" steps (lines 114-121) — steps the model itself wrote. No human reviews
the validation report for honesty; no human confirms the model's self-assessment; no human reads
the *code*. The command effectively **substitutes model self-assessment for human
plan-completion review**.

**It adds review burden instead of reducing it.** Recall the V1 failure mode: humans were asked
to review 1000-line plans at a cost comparable to reviewing the code, and were surprised anyway
("don't read the plans, read the code"). This command inherits that world — it assumes a big
multi-phase plan with many success criteria — and then generates *yet another artifact* (the
Validation Report) on top of it. It's another document to trust/review, produced by the very
agent whose work is in question.

**Brittle environment assumptions.** It hardcodes a Make-based toolchain (`make check test`,
`make build`, `make test`, `make lint`, lines 27 / 95-97). Any repo without those targets falls
through.

---

## 4. Foreshadowing QRSPI

`validate_plan` and QRSPI are trying to answer the **same question** — *"did the implementation
actually match the intent, and can we trust that it's done?"* — but they place the answer in
different hands. Tracing the evolution:

**The thing V1 got right, QRSPI kept.** The instinct to run real automated checks, to separate
automated from manual verification, to be honest about deviations, and to use git as ground
truth are all sound. QRSPI doesn't discard verification — it **relocates and decomposes** it.

**"What does validated mean?" → predefined test checkpoints per vertical slice.** The command's
fatal vagueness (no pass/fail definition, one monolithic post-hoc pass) is exactly what QRSPI's
`structure.md` fixes. Instead of the model deciding after the fact whether a 1000-line plan is
"done," QRSPI defines objective **test checkpoints per vertical slice up front**. Verification
becomes continuous and incremental — each slice has its own gate that either passes or doesn't —
rather than a single subjective judgment call at the end. `validate_plan`'s *"For each phase in
the plan... Run automated verification"* (lines 62-71) is the embryonic, retrofitted version of
that idea; QRSPI moves the checkpoint definition *before* implementation and makes it binary.

**Self-grading → human code review at PR.** The command's deepest flaw — the model validating
its own work (lines 131-135) — is precisely what QRSPI overrules. QRSPI's answer to "don't read
the plans, read the code" is to reserve the human's expensive attention for **deep review of the
actual code at PR time**, not for grading a report the model wrote about itself. QRSPI implicitly
concedes that a model cannot be trusted to certify its own completion, so it puts a human at the
one gate that matters.

**Redistribution of review cost.** `validate_plan` sits inside the V1 economics that QRSPI
rejected: heavy plans, heavy artifacts, model-generated summaries layered on top. QRSPI pushes
human review *earlier and cheaper* — a ~200-line `design.md` and a ~2-page `structure.md`, read
while they're still short and cheap to change — and *later and deeper* — the code at PR. The
Validation Report (lines 86-127) is a direct ancestor of the PR artifact, and the workflow
already gestures at this by chaining `/validate_plan → /describe_pr` (lines 160-162). QRSPI keeps
the PR gate but swaps the actor: the **human** reads the code there, rather than the **model**
narrating its own report.

**Net read.** `validate_plan` is the "let the model check its own homework" experiment. It
carries good verification instincts but locates judgment in the wrong place (the model, after the
fact, against a huge plan, with no pass/fail bar). QRSPI's redesign is the lesson learned: define
objective checkpoints *before* you implement, run them *per slice*, and spend the human's
attention on the *code at PR* — not on a self-graded validation report.
