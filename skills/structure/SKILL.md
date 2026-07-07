---
name: structure
description: Step 3 — slice the approved design into ordered vertical slices with test checkpoints. Produces structure.md (~2 pages), the second human alignment gate.
disable-model-invocation: true
---

# Structure

Decide how to get there: the ordered phases of work and how each will be verified. If the plan is the implementation,
this document is the header file — just enough for the user to see what you intend and correct it, at the point where a
correction costs a sentence rather than a rewrite.

## 1. Load the artifacts

Locate `.planning/<slug>/`: take the slug from the invocation; if none was given and exactly one directory exists, use
it; otherwise ask the user. Read whichever of `design.md`, `task.md`, and `research.md` exist, fully — this skill
depends on nothing outside those files and the conversation. No phase is mandatory: if `design.md` is absent, confirm
with the user that design was deliberately skipped and work from what remains.

If `design.md` exists but still has unresolved open questions, STOP and send the user back to `/design`: structure
built on an unsettled design is waste — every slice cut around an open question gets re-cut when the answer lands.

## 2. Draft vertical slices

Break the work into tracer-bullet slices. Every slice:

- cuts end-to-end through all the layers the behaviour touches — never "all database, then all services, then all UI";
- is demoable or verifiable on its own the moment it lands;
- carries an explicit **test checkpoint** — the test(s) that prove it and the seam they exercise, in
  `codebase-designing` terms;
- is roughly a 200–400-line change: prefer many thin slices over few thick ones;
- is named for its observable behaviour, not for a layer or component.

Where a new type or signature is the clearest way to show intent, sketch it — signatures only, never bodies. The
header file declares; it doesn't define.

## 3. Review the slicing with the user

Present the slices as a numbered list: title, end-to-end behaviour, test checkpoint, depends-on. Ask the user whether
the granularity is right and whether any slice should merge or split. Iterate until the user approves — this is a
deep-review gate, not a formality: the plan that follows is only spot-checked, so a wrong cut that survives this
review travels straight into implementation.

## 4. Write and hand off

Write `structure.md` (~2 pages max): the approved slices in order, each with its checkpoint and dependencies, plus any
signature sketches. The next step is `/write-plan`, best run in a fresh session (`/clear`), rebuilt from the artifacts
rather than this conversation.
