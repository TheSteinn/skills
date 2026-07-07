---
name: open-pr
description: QRSPI step 6 — open a pull request grounded in the design doc, putting the "why" beside the diff. Ends with the one non-negotiable - the human reads the code.
disable-model-invocation: true
---

# Open PR

Deliver the work as a pull request whose description is grounded in `design.md`, so the reviewer confirms decisions
they already approved instead of discovering them in the diff. Everything upstream priced the user's attention toward
this moment: the code is the review that matters, and the description exists to make it fast.

## 1. Load

Locate `.planning/<slug>/`: take the slug from the invocation; if none was given and exactly one directory exists, use
it; otherwise ask the user. Read the alignment artifacts that exist — `design.md` when the design phase ran, otherwise
`plan/index.md` and `task.md` — plus the full diff against the base branch (`git diff <base>...HEAD`) and the phase
commits (`git log`). Draft nothing until all three are in hand: the description is an account of the diff in the
design's terms, and neither half can come from memory of an implementation session this session never had.

## 2. Write the description

Hold the altitude: the description carries the high level — the seams, the design choices, the behaviour the diff
embodies — never file-by-file minutiae. The diff itself carries the low level; the description exists so the reviewer
confirms decisions they already approved, not so they re-derive them from a changelog.

Write the description from this template — one markdown header per section:

```markdown
## Why

<the problem and the desired end state — in the design's own terms when `design.md` exists, referencing the sections
they come from; otherwise from the plan index and the task>

## What changed

- <one entry per plan phase (or commit, when no plan exists), stated as observable behaviour — what the system now
  does, never which files moved>

## Decisions exercised

- <a resolved decision this diff embodies, and how the diff honours it>
- <any deviation the implementation surfaced, with its rationale>

## Verification

- Automated: <the criteria that passed>
- Manual: <the steps a reviewer can rerun, stated so they can be followed verbatim>
```

## 3. Open it

Use whatever forge CLI is available and already authenticated (`gh`, `bkt`, …). Confirm the title, the description,
and the target branch with the user before pushing or creating anything — this is the pipeline's outward-facing step,
and outward-facing actions need explicit consent. If no forge CLI is available, output the title and description for
the user to paste, say which tool was missing, and stop — never install one.

## 4. The gate

Close with the reminder the whole pipeline priced everything toward: the alignment artifacts that were produced were
the cheap reviews; the code is the one that matters. Tell the user — **now read the code. No exceptions.**
