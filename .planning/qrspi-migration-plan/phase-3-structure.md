# Phase 3: `/structure`

> Source: [index.md](index.md) · structure slice 3. Self-contained: implement from this file +
> the index only.

## Overview

Create the second alignment gate: `/structure` turns the approved design into ~2 pages of
ordered **vertical slices with test checkpoints** — QRSPI's dedicated cure for horizontal
plans, at the "C header file" altitude. Absorbs `to-plan`'s tracer-bullet rules and its
quiz-the-user review loop (the good parts of `to-plan`; the skill itself dies in phase 4). Adds
the hard gate V1 buried: no structure on top of an unsettled design.

## Changes required

### 1. Create `skills/structure/SKILL.md`

Target sketch — a floor, not the finished file (index: "sketches are floors"): flesh out into
a polished skill; structure, gates, and voice are fixed.

```markdown
---
name: structure
description: QRSPI step 3 — slice the approved design into ordered vertical slices with test checkpoints. Produces structure.md (~2 pages), the second human alignment gate.
disable-model-invocation: true
---

# Structure

Decide how to get there: the ordered phases of work and how each will be verified. If the plan
is the implementation, this document is the header file — just enough for a human to see what
you intend and correct it.

## 1. Load the artifacts

Locate `.planning/<slug>/` (take the slug from the invocation; if none was given and exactly
one directory exists, use it; otherwise ask the user). Read whichever of `design.md`,
`task.md`, and `research.md` exist, fully — this skill depends on nothing outside those files
and the conversation. No phase is mandatory: if `design.md` is absent, confirm with the user
that design was deliberately skipped and work from what remains. If `design.md` exists but
still has unresolved open questions, STOP and send the user back to `/design`: structure built
on an unsettled design is waste.

## 2. Draft vertical slices

Break the work into tracer-bullet slices. Every slice:

- cuts end-to-end through all the layers the behaviour touches — never "all database, then all
  services, then all UI";
- is demoable or verifiable on its own the moment it lands;
- carries an explicit **test checkpoint** — the test(s) that prove it and the seam they
  exercise, in `codebase-designing` terms;
- is roughly a 200–400-line change: prefer many thin slices over few thick ones;
- is named for its observable behaviour, not for a layer or component.

Where a new type or signature is the clearest way to show intent, sketch it — signatures only,
never bodies.

## 3. Review the slicing with the user

Present the slices as a numbered list: title, end-to-end behaviour, test checkpoint,
depends-on. Ask the user whether the granularity is right and whether any slice should merge
or split. Iterate until the user approves — this is a deep-review gate, not a formality.

## 4. Write and hand off

Write `structure.md` (~2 pages max): the approved slices in order, each with its checkpoint and
dependencies, plus any signature sketches. The next step is `/write-plan`, best run in a fresh
session (`/clear`).
```

### 2. Create `docs/structure.md` (deviation record)

Must cover, with reasons: (a) the vertical-slice rules are inherited from this repo's `to-plan`
(tracer bullets) — convergent with QRSPI's Structure phase, which exists because prompting
cannot cure horizontal plans, so a dedicated human-reviewed artifact enforces slicing; (b) the
hard STOP on unresolved design questions — V1 had this force only at the plan stage
("No Open Questions… STOP"); we apply it at the structure gate where it is cheaper; (c) the
quiz-the-user review loop carried over from `to-plan` step 5.

### 3. Edit `README.md`

Add `#### /structure` under the QRSPI pipeline section. No other README changes.

## Success criteria

### Automated verification

- [ ] `test -f skills/structure/SKILL.md && test -f docs/structure.md`
- [ ] `grep -q 'disable-model-invocation: true' skills/structure/SKILL.md`
- [ ] `grep -qi 'test checkpoint' skills/structure/SKILL.md`
- [ ] `grep -q '/structure' README.md`

### Manual verification

- [ ] Instruction count of SKILL.md body < 40.
- [ ] Run `/structure` on phase 2's micro-task design: it reads only the named artifacts;
      every proposed slice names observable behaviour and carries a checkpoint; the
      quiz/iterate loop runs before the file is written; result ≤ 2 pages.
- [ ] Negative test: temporarily add an open question to `design.md` — `/structure` must STOP
      and point back to `/design` (then revert the edit).
- [ ] Skip test: with `design.md` absent, it confirms the skip with the user and proceeds from
      the remaining artifacts instead of hard-failing.

## What this phase is NOT doing

No per-slice implementation detail (that is `/write-plan`); no deletion of `to-plan` yet — it
must remain functional until its full replacement (structure + plan) exists at the end of
phase 4.

## Dependencies

Phase 2 (consumes `design.md`; verified against its micro-task output).
