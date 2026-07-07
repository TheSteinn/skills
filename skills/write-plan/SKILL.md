---
name: write-plan
description: QRSPI step 4 — expand the approved structure into a tactical plan for the implementing agent - an index plus one self-contained file per phase, with code sketches and success criteria. Humans spot-check; deep review already happened.
disable-model-invocation: true
---

# Write Plan

Expand `structure.md` into the tactical plan `/implement` executes. The audience is an agent, not a human — the human
spot-checks it. Alignment already happened at design and structure; your job here is completeness, not persuasion:
each phase file must carry everything a fresh subagent needs to implement that phase well.

## 1. Load the artifacts

Locate `.planning/<slug>/`: take the slug from the invocation; if none was given and exactly one directory exists, use
it; otherwise ask the user. If no directory exists, create it and capture the task from the invocation or conversation
into `task.md` — later phases read that file, not this conversation. Read whichever of `task.md`, `research.md`,
`design.md`, and `structure.md` exist, fully. No upstream phase is mandatory — source missing context from the
conversation and the user rather than refusing; planning is the pipeline's one near-universal phase.

## 2. Phase breakdown: mirror structure, or earn approval

When `structure.md` exists: one plan phase per approved slice, same order, same scope — do not re-slice. The slicing
was deep-reviewed at `/structure`; it is not this phase's decision to remake. If detailed planning reveals a genuine
slicing problem, STOP, explain it, and send the user back to `/structure` — never silently restructure.

When structure was skipped: draft the phase breakdown yourself under the same discipline — every phase end-to-end and
demoable with a test checkpoint, never a layer — and get the user's approval on the breakdown before writing any phase
file.

## 3. Write the plan

Follow the templates in [references/plan-template.md](references/plan-template.md) exactly: `plan/index.md` plus one
`plan/phase-N-<slug>.md` per phase. Four rules trump everything in the templates:

- **Self-containment.** An agent given only `index.md` and one phase file must be able to implement that phase —
  restate whatever context it needs; cite research and design by file:line rather than assuming they'll be read.
- **Code sketches are targets, not prescriptions.** They show intended shape; the implementing agent still writes the
  failing test first, and reports mismatches instead of improvising. Say this above the first sketch in every phase
  file (the template has the wording).
- **Success criteria are split** per phase: automated verification (commands an agent runs) and manual verification
  (steps a human performs). Fold the slice's test checkpoint from `structure.md` into the automated half wherever
  possible.
- **No open questions.** If you hit a decision the artifacts don't answer, STOP and ask the user — every decision is
  made before the plan is final.

## 4. Hand off

Tell the user the plan is ready for a spot-check (deep review already happened upstream), list the phase files, and
point at `/implement` as the next step — best run in a fresh session (`/clear`) once the user has prepared the branch
or worktree the implementation should happen on.
