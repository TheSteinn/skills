# Phase 2: `/design`

> Source: [index.md](index.md) · structure slice 2. Self-contained: implement from this file +
> the index only.

## Overview

Create the pipeline's main alignment gate: `/design` reads `task.md` + `research.md`, brain-dumps
a ~200-line design, then grills the open questions with the user until every branch resolves —
resolutions land directly in `design.md`. Composes three keepers: `grilling` (questioning
engine), `codebase-designing` (vocabulary), `domain-modelling` (durable docs, when present).
Also: one exact edit to `grilling`, and the deletion of `to-prd` (its decision-carrying role is
subsumed by `design.md`; nothing downstream consumes PRDs after this phase).

## Changes required

### 1. Create `skills/design/SKILL.md`

Target sketch — a floor, not the finished file (index: "sketches are floors"): flesh out into
a polished skill; structure, gates, and voice are fixed.

```markdown
---
name: design
description: QRSPI step 2 — brain-dump a ~200-line design from task + research, then grill the open questions until resolved. Produces design.md, the pipeline's main human alignment gate.
disable-model-invocation: true
---

# Design

Produce `design.md` — the shared understanding forced out of the context window into an
inspectable artifact, deep-reviewed by the human before any code exists.

## 1. Load the artifacts

Locate `.planning/<slug>/` (take the slug from the invocation; if none was given and exactly
one directory exists, use it; otherwise ask the user). Read `task.md` and `research.md` fully.
Either may be absent — no phase is mandatory: without `research.md`, confirm with the user
whether to design from the task and conversation alone or run `/research` first; without
`task.md`, create the directory and capture the task from the invocation or conversation into
`task.md` before designing.

Invoke the `codebase-designing` skill — its vocabulary (module, interface, seam, depth) is the
language for everything below. If the project keeps domain docs (a `LANGUAGE.md` or
`CONTEXT-MAP.md` exists), also invoke `domain-modelling` so terms and ADR-worthy decisions are
captured as they crystallise.

## 2. Brain-dump the draft

Write a first-pass `design.md` with exactly these sections:

- **Current state** — how the relevant system works today. Facts only, cited from research
  (or from code read directly when research was skipped).
- **Desired end state** — the observable behaviour when done, and how it will be verified.
- **Patterns to follow** — the existing idioms this change should copy, with file:line
  examples; name seams and interfaces in `codebase-designing` terms. Flag any pattern the
  research surfaced that should NOT be followed.
- **Resolved decisions** — sparse at first; the grill fills it.
- **Open questions** — everything you are unsure about, everything you believe the user wants
  but hasn't confirmed, every fork in the approach. Err on the side of more questions.

Keep the whole document around 200 lines. It is a design, not a plan: no phase breakdown (that
is `/structure`'s job) and no code beyond interface sketches. When a decision can't be reviewed
in prose — a UI layout, a schema shape — link the cheapest reviewable sketch (an HTML mock, a
diagram file) from the relevant section instead of describing it badly.

## 3. Grill the open questions

Invoke the `grilling` skill on the Open questions section — questions come first; present no
part of the design as settled until its branch is resolved. As each branch resolves, move it
from Open questions into Resolved decisions immediately, in this document's own words with a
one-line rationale. The grill's closing decision record lives in `design.md` itself — do not
write a separate Snapshot file.

## 4. Hand off

`design.md` must end with zero open questions; explicitly parked items are recorded as parked,
with what unblocks them. Ask the user to deep-review the document — this is the pipeline's main
alignment gate; time spent here is the cheapest place to catch a wrong approach. The next step
is `/structure`, best run in a fresh session (`/clear`).
```

### 2. Edit `skills/grilling/SKILL.md` (exact edit)

In the "Closing the grill" section, the final paragraph currently reads:

> Get the user's explicit confirmation of this record. If the user asks to persist it, write it
> as presented to `.planning/decisions-<feature>.md` (creating `.planning/` if needed) —
> downstream planning skills look for it at that path.

Append one sentence to that paragraph:

> If the host workflow that invoked the grill names its own destination for the record (as
> `/design` does with `design.md`'s Resolved decisions section), write it there instead — no
> separate decisions file.

No other change to `grilling`.

### 3. Delete `skills/to-prd/`

`git rm -r skills/to-prd`. Note: `to-plan` (alive until phase 4) references PRDs but degrades
gracefully — it works from a Snapshot or conversation when no PRD exists; do not edit it.

### 4. Create `docs/design.md` (deviation record)

Must cover, with reasons: (a) the grill replaces QRSPI's bare "present open questions first" —
an improvement deviation: QRSPI asks once, we walk the decision tree until every branch
resolves; (b) grill resolutions land in `design.md`, not a Decision Snapshot — one artifact per
phase (Snapshot remains standalone `grill-me`'s output); (c) `to-prd` deleted — QRSPI has no
requirements doc, `design.md` carries decisions, and nothing downstream consumes user stories;
(d) the medium-neutral supporting-artifact rule (sketch links when prose can't carry a
decision) — review economics applied to medium, deliberately not a frontend/backend callout.

### 5. Edit `README.md`

Add `#### /design` under the QRSPI pipeline section. Remove the `#### /to-prd` entry from the
Planning section. In the Credits section, adjust the Matt Pocock line so it stops implying
`/to-prd` still exists (e.g. "…origin of the planning pipeline (`/grill-me`, `/tdd`, and the
since-retired `/to-prd`)…"). Leave `to-plan`'s README entry alone (dies in phase 4).

## Success criteria

### Automated verification

- [ ] `test -f skills/design/SKILL.md && test -f docs/design.md`
- [ ] `grep -q 'disable-model-invocation: true' skills/design/SKILL.md`
- [ ] `test ! -d skills/to-prd`
- [ ] `! grep -rn 'to-prd' skills/` (no skill references the deleted skill; README credits may
      mention it historically)
- [ ] `grep -q 'design.md' skills/grilling/SKILL.md` (the new destination sentence landed)
- [ ] `grep -q '/design' README.md && ! grep -q '#### \`/to-prd\`' README.md`

### Manual verification

- [ ] Instruction count of SKILL.md body < 40.
- [ ] Run `/design` on phase 1's micro-task artifacts: with `research.md` absent it offers to
      proceed from task + conversation instead of hard-failing; with it, the draft carries all
      five sections; the grill fires before any
      design prose is presented as settled; resolutions appear in Resolved decisions with
      rationales; no `decisions-*.md` file is created; final doc ≈ 200 lines.
- [ ] Standalone `grill-me` still persists to `.planning/decisions-<feature>.md` when asked
      (regression check on the `grilling` edit).

## What this phase is NOT doing

No structure/slicing content in `design.md`; no ADR/glossary behaviour changes
(`domain-modelling` is invoked, not modified); no README narrative rewrite.

## Dependencies

Phase 1 (consumes `task.md`/`research.md`; verified against its micro-task output).
