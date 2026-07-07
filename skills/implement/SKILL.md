---
name: implement
description: QRSPI step 5 — orchestrate the plan phase by phase, delegating each phase to a TDD subagent and committing after each completed phase. Assumes you have already prepared the branch or worktree.
disable-model-invocation: true
---

# Implement

Execute the plan phase by phase, delegating all coding to subagents. You are the orchestrator: you track progress,
verify criteria, commit completed phases, and escalate — you do not write code yourself.

This skill assumes the user has already put the session on the branch or worktree where the work should happen. Make
no git-setup moves: no branching, no checkout, no worktree creation.

## 1. Load the plan

Locate `.planning/<slug>/plan/`: take the slug from the invocation; if none was given and exactly one exists, use it;
otherwise ask the user. A plan is this skill's one hard prerequisite — if there is no `plan/`, stop and point the user
at `/write-plan`: implementing without a plan is just `/tdd` on the target change.

Read `plan/index.md` fully and put every phase on your todo list. If any phase file already has checked-off criteria,
previous work exists: trust the commits, and resume from the first incomplete phase.

## 2. Delegate each phase

Work phases in plan order, one at a time. Each phase goes to a fresh subagent whose prompt MUST begin with "/tdd" and
contain the full text of the phase file, the Durable decisions section from `plan/index.md`, and nothing about other
phases — the subagent's context is spent on its own slice, not its neighbours'.

Phase files are self-contained by construction. If one isn't — it leans on another phase, or on context only this
session has — that is a plan defect: STOP and report it to the user rather than paper over it in the prompt.

## 3. Verify, commit, checkpoint

When a subagent reports done:

- Run every command in the phase's automated verification yourself, and check off what passes in the phase file.
- A criterion fails → delegate the fix back with the failure output. A subagent that contradicted a durable decision
  has failed regardless of green checks → delegate to a fresh subagent with the original phase task plus the
  violation. **Two failures on one phase → stop the orchestration and report to the user.**
- All automated criteria pass → commit: one atomic commit for the phase, message naming the plan phase. Never commit a
  phase whose criteria haven't passed — the history should read as one revertible step per completed phase.
- The phase has manual verification steps → pause and ask the user to perform them before starting the next phase.

## 4. Mismatch protocol

When reality contradicts the plan — a file moved, an approach can't work — do not improvise and do not let a subagent
improvise. STOP and report:

```
Issue in Phase N:
Expected: <what the plan says>
Found: <the actual situation>
Why this matters: <explanation>
How should I proceed?
```

## 5. Finish

When every phase is committed, summarise what landed against the plan — including any approved deviations — and point
at `/open-pr` as the next step, best run in a fresh session (`/clear`).
