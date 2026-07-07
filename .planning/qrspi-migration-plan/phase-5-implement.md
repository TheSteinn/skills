# Phase 5: `/implement`

> Source: [index.md](index.md) · structure slice 5. Self-contained: implement from this file +
> the index only.

## Overview

Rework `orchestrate-plan` into the pipeline's execution phase. Keeps its good bones —
orchestrator-never-codes, per-phase subagent delegation with `/tdd`, acceptance-criteria
checking, two-strikes escalation — and adds what QRSPI adds: **one commit per completed phase**
(real, atomic, revertible state instead of checkbox-only tracking) and V1's STOP-and-report
mismatch protocol. Per index decision 7, it assumes the user has already prepared the
branch/worktree and makes **no git-setup moves**. `orchestrate-plan` is deleted; `tdd` gets one
retargeting edit.

## Changes required

### 1. Create `skills/implement/SKILL.md`

Target sketch — a floor, not the finished file (index: "sketches are floors"): flesh out into
a polished skill; structure, gates, and voice are fixed.

```markdown
---
name: implement
description: QRSPI step 5 — orchestrate the plan phase by phase, delegating each phase to a TDD subagent and committing after each completed phase. Assumes you have already prepared the branch or worktree.
disable-model-invocation: true
---

# Implement

Execute the plan phase by phase, delegating all coding to subagents. You are the orchestrator:
you track progress, verify criteria, commit completed phases, and escalate — you do not write
code yourself.

This skill assumes the user has already put the session on the branch or worktree where the
work should happen. Make no git-setup moves: no branching, no checkout, no worktree creation.

## 1. Load the plan

Locate `.planning/<slug>/plan/` (take the slug from the invocation; if none was given and
exactly one exists, use it; otherwise ask the user). A plan is this skill's one hard
prerequisite: if there is no `plan/`, stop and point at `/write-plan` — implementing without a
plan is just `/tdd` on the target change. Read `index.md` fully and put every phase on your
todo list. If any phase file already has checked-off criteria, previous work exists: trust the
commits, and resume from the first incomplete phase.

## 2. Delegate each phase

Work phases in plan order, one at a time. Each phase goes to a fresh subagent whose prompt
MUST begin with "/tdd" and contain: the full text of the phase file, the Durable decisions
section from `index.md`, and nothing about other phases. Phase files are self-contained by
construction — if one isn't, that is a plan defect: STOP and report it rather than paper over
it in the prompt.

## 3. Verify, commit, checkpoint

When a subagent reports done:

- Run every command in the phase's automated verification yourself and check off what passes
  in the phase file.
- Criteria fail → delegate the fix back with the failure output. A subagent that contradicted
  a durable decision has failed regardless of green checks → delegate to a fresh subagent with
  the original phase task plus the violation. **Two failures on one phase → stop the
  orchestration and report to the user.**
- All automated criteria pass → commit: one atomic commit for the phase, message naming the
  plan phase. Never commit a phase whose criteria haven't passed.
- The phase has manual verification steps → pause and ask the user to perform them before
  starting the next phase.

## 4. Mismatch protocol

When reality contradicts the plan — a file moved, an approach can't work — do not improvise
and do not let a subagent improvise. STOP and report:

    Issue in Phase N:
    Expected: <what the plan says>
    Found: <the actual situation>
    Why this matters: <explanation>
    How should I proceed?

## 5. Finish

When every phase is committed, summarise what landed against the plan — including any approved
deviations — and point at `/open-pr` as the next step.
```

### 2. Delete `skills/orchestrate-plan/`

`git rm -r skills/orchestrate-plan`.

### 3. Edit `skills/tdd/SKILL.md` (exact edit)

In "Where tests go", the second sentence currently reads:

> Seams are a design decision, so they should already exist when the loop starts: take them
> from the plan, design docs, or the conversation.

Replace with:

> Seams are a design decision, so they should already exist when the loop starts: take them
> from the phase document's test checkpoint, the design doc's patterns to follow, or the
> conversation.

No other change to `tdd` (its later "Take priorities from the plan when it has them" already
fits the new phase files).

### 4. Create `docs/implement.md` (deviation record)

Must cover, with reasons: (a) QRSPI's Worktree phase is delegated to the user — worktree is a
mechanism with nothing to review, and the human choosing the isolation boundary keeps the
skill free of git-setup side effects (deliberate deviation: QRSPI names it as a phase); (b)
commit-per-phase replaces checkbox-only progress — V1's `implement_plan` never mentioned git;
(c) TDD subagents retained where QRSPI punts on testing — this repo has a stance; (d) the
STOP-and-report mismatch template is inherited verbatim in spirit from V1 `implement_plan` —
one of its good parts; (e) two-strikes escalation carried from `orchestrate-plan`.

### 5. Edit `README.md`

Add `#### /implement` under the QRSPI pipeline section; remove the `#### /orchestrate-plan`
entry and any prose pointing at it.

## Success criteria

### Automated verification

- [ ] `test -f skills/implement/SKILL.md && test -f docs/implement.md`
- [ ] `grep -q 'disable-model-invocation: true' skills/implement/SKILL.md`
- [ ] `test ! -d skills/orchestrate-plan`
- [ ] `! grep -rn 'orchestrate-plan' skills/ README.md`
- [ ] `grep -q 'no git-setup moves\|no branching, no checkout, no worktree' skills/implement/SKILL.md`
- [ ] `grep -q 'test checkpoint' skills/tdd/SKILL.md`

### Manual verification

- [ ] Instruction count of SKILL.md body < 40.
- [ ] Dogfood on the micro-task plan from phase 4, on a scratch branch you create by hand
      first: confirm the skill makes no git-setup moves of its own; each phase goes to a
      subagent whose prompt starts with "/tdd" and contains only its phase file + durable
      decisions; `git log` afterwards shows one commit per phase; criteria are checked off in
      the phase files.
- [ ] Force the mismatch protocol once: pre-edit one plan line to contradict reality (e.g. a
      wrong file path) and confirm the orchestrator STOPs with the four-line template instead
      of improvising. Revert the edit after.

## What this phase is NOT doing

No PR creation (phase 6); no changes to `tdd` beyond the one sentence; no parallel-phase
execution (phases run sequentially — their dependency order is the plan's).

## Dependencies

Phase 4 (consumes `plan/`; verified against its micro-task output).
