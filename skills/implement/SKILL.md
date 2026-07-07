---
name: implement
description: Step 5 — orchestrate the plan phase by phase, delegating each phase to a TDD subagent and committing after each completed phase. Assumes you have already prepared the branch or worktree.
disable-model-invocation: true
---

# Implement

Execute the plan phase by phase, delegating all coding to subagents. Two roles run this skill, and every instruction
here is scoped to one of them:

- **The orchestrator — you.** The whole body of this file addresses you: you load the plan, delegate each phase,
  verify results, triage mismatches, commit completed phases, and escalate. You do not write code.
- **The phase subagent** — a fresh agent per phase, implementing exactly one phase. It never reads this file: its
  entire contract travels in its prompt, built from the template in step 2 — the one part of this file where "you"
  means the subagent.

This skill assumes the user has already put the session on the branch or worktree where the work should happen. Make
no git-setup moves: no branching, no checkout, no worktree creation.

## 1. Load the plan

Locate `.planning/<slug>/plan/`: take the slug from the invocation; if none was given and exactly one exists, use it;
otherwise ask the user. A plan is this skill's one hard prerequisite — if there is no `plan/`, stop and point the user
at `/write-plan`: implementing without a plan is just `/tdd` on the target change.

Read `plan/index.md` fully and put every phase on your todo list. If any phase file already has checked-off criteria,
previous work exists: trust the commits, and resume from the first incomplete phase. Loading the plan is yours alone —
each subagent reads only the index and its own phase file, at the paths you pass it.

## 2. Delegate each phase

Work phases in plan order, one at a time, each to a fresh subagent — its context is spent on its own slice, not its
neighbours'. Build every prompt from this template, filling the placeholders and changing nothing else:

```
/tdd

You are implementing Phase <N> of a plan: <phase title>.

Read both of these files fully before doing anything else. They are your persisted memory — return to them whenever
you lose the thread:

- Plan index (shared context, durable decisions): <path to plan/index.md>
- Your phase (the work): <path to the phase file>

<critical>Only work on your specified phase. Do not implement, fix, or prepare work that belongs to any other
phase.</critical>

Plans are carefully designed, but reality can be messy. Follow the plan's intent while adapting to what you find;
implement your phase fully, and verify your work makes sense in the broader codebase context. When things don't
match the plan exactly, think about why and report clearly:

- Minor mismatches — a moved file, a renamed symbol, a sketch that doesn't compile as written — adapt around with
  judgment and record in your report. Never absorb one silently, and never stop for one.
- A mismatch that would change a seam or the design is beyond adaptation: stop and report it instead of
  implementing it.

Honour every durable decision in the index — violating one fails the phase regardless of green tests. Derive your
test seams from the phase document and the durable decisions, and state them before your first test.

Before reporting done, run every command in your phase's Automated verification list; all must pass. Leave the
Manual verification steps to the user, and do not tick any checkboxes — the orchestrator owns those. Report back
with exactly:

1. **Criteria** — each automated verification command and its result.
2. **Seams** — the seams you tested at.
3. **Mismatches** — every adaptation you made and anything you stopped on: what the plan expected, what you found,
   what you did. Write "none" if the plan matched reality.
```

A phase that builds on earlier phases' completed, committed work is normal sequencing, not a defect — by the time you
delegate phase N, its predecessors are already in the codebase, where the subagent will find them. The defect is
textual: a phase file that cannot be understood and implemented from `index.md` plus itself, because it narrates
another phase's file or leans on context only the planning session had. STOP and report that to the user as a plan
defect rather than paper over it in the prompt.

The template binds the subagent to adapt-and-report, never design: it absorbs no mismatch silently, stops on anything
seam- or design-shaped, and verifies its own phase before reporting. Its report is input to your verification, not a
substitute for it.

## 3. Verify, commit, checkpoint

When a subagent reports done:

- Run every command in the phase's automated verification yourself — trust the report, but verify — and check off
  what passes in the phase file.
- Triage every mismatch in the report (step 4) before committing anything.
- A criterion fails → delegate the fix back with the failure output. A subagent that contradicted a durable decision
  has failed regardless of green checks → delegate to a fresh subagent with the original phase task plus the
  violation. **Two failures on one phase → stop the orchestration and report to the user.**
- All automated criteria pass → commit: one atomic commit for the phase, message naming the plan phase. Never commit a
  phase whose criteria haven't passed — the history should read as one revertible step per completed phase.
- The phase has manual verification steps → pause and ask the user to perform them before starting the next phase.

## 4. Triage reported mismatches

Reality will sometimes contradict the plan. Neither role improvises design around it: the subagent adapts within the
plan's intent and reports every mismatch; you triage each one into exactly one of three outcomes.

- **Hard stop** — the plan is irreconcilable with the codebase (typically what a subagent stopped on: a seam change,
  a design change). Stop the orchestration and report with the template below — the fix lies back up the pipeline,
  not in improvisation here.
- **Soft stop** — the plan still holds, but the adaptation deserves a human look. Present it to the user and get
  their confirmation before starting the next phase.
- **Silent proceed** — the adaptation is minor: not a seam change, not a design change. Note it and carry on; it
  belongs in the final summary's deviations.

```
Issue in Phase N:
Expected: <what the plan says>
Found: <the actual situation>
Why this matters: <explanation>
How should I proceed?
```

## 5. Finish

When every phase is committed, summarise what landed against the plan — including approved deviations and every
silent-proceed adaptation — and point at `/open-pr` as the next step, best run in a fresh session (`/clear`).
