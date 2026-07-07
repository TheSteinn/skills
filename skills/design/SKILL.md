---
name: design
description: QRSPI step 2 — brain-dump a ~200-line design from task + research, then grill the open questions until resolved. Produces design.md, the pipeline's main human alignment gate.
disable-model-invocation: true
---

# Design

Produce `design.md` — the shared understanding forced out of the context window into an inspectable artifact,
deep-reviewed by the user before any code exists. The document starts as a brain-dump that declares every uncertainty,
and is finished only when a grill has walked each one to a resolution.

## 1. Load the artifacts

Locate `.planning/<slug>/`: take the slug from the invocation; if none was given and exactly one directory exists, use
it; otherwise ask the user. Read `task.md` and `research.md` fully. Either may be absent — no phase is mandatory:

- Without `research.md`, confirm with the user whether to design from the task and conversation alone or to run
  `/research` first.
- Without `task.md`, create the directory and capture the task from the invocation or conversation into `task.md`
  before designing — later phases read that file, not this conversation.

Then load the supporting skills — actually invoke each one with the Skill tool; mentioning a skill in prose loads
nothing:

- Invoke `codebase-designing` — its vocabulary (module, interface, seam, depth) is the language for everything below.
- Invoke `domain-modelling` so terms and ADR-worthy decisions are captured as they crystallise. Invoke it whether or
  not domain docs exist: it orients on `LANGUAGE.md`/`CONTEXT-MAP.md` when present, proceeds silently when absent, and
  creates `LANGUAGE.md` lazily on the first resolved term — so a project without domain docs starts keeping them here.

## 2. Brain-dump the draft

Write a first-pass `design.md` with exactly these sections:

- **Current state** — how the relevant system works today. Facts only, cited from research (or from code read directly
  when research was skipped).
- **Desired end state** — the observable behaviour when the change is done, and how it will be verified.
- **Patterns to follow** — the existing idioms this change should copy, with file:line examples; name seams and
  interfaces in `codebase-designing` terms. Flag any pattern the research surfaced that should NOT be followed.
- **Resolved decisions** — sparse at first; the grill fills it.
- **Open questions** — everything you are unsure about, everything you believe the user wants but hasn't confirmed,
  every fork in the approach. Err on the side of more questions: one that turns out trivial costs an exchange; an
  assumption that turns out wrong costs the implementation built on it.

Keep the whole document around 200 lines. It is a design, not a plan: no phase breakdown (that is `/structure`'s job)
and no code beyond interface sketches. When a decision can't be reviewed in prose — a UI layout, a schema shape — link
the cheapest reviewable sketch (an HTML mock, a diagram file) from the relevant section instead of describing it badly.

## 3. Grill the open questions

Invoke the `grilling` skill on the Open questions section. Questions come first: present no part of the design as
settled until its branch is resolved. As each branch resolves, move it from Open questions into Resolved decisions
immediately — in this document's own words, with a one-line rationale — so resolutions land at peak attention rather
than batched at the end. The grill's closing decision record lives in `design.md` itself; do not write a separate
Snapshot file.

## 4. Hand off

`design.md` must end with zero open questions; explicitly parked items are recorded as parked, with what unblocks them.
Ask the user to deep-review the document — this is the pipeline's main alignment gate, and time spent here is the
cheapest place to catch a wrong approach before it becomes working code. The next step is `/structure`, best run in a
fresh session (`/clear`), rebuilt from the artifacts rather than this conversation.
