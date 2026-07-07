# Plan templates

> **Three things from the ancestral V1 template are cut on purpose — do not reintroduce them.**
>
> - **No "Common Patterns" recipes.** The originals were horizontal, layer-by-layer build orders ("schema → store →
>   business logic → API → UI") — the disease `/structure` exists to cure. Phase order comes from the approved
>   slices, never from a recipe.
> - **No org-specific machinery.** No thoughts sync, no ticket tooling, no hardcoded `make` targets — success
>   criteria use the project's actual commands, discovered from the project itself.
> - **No process steps.** Research and alignment live in earlier pipeline phases; the plan records their outcomes and
>   carries no instructions for re-running them.
>
> These three cuts are the only ones — every other section of the source template carries over.

Two templates: one `plan/index.md` per plan, one `plan/phase-N-<slug>.md` per phase. Reading them, and filling them
in:

- Angle-bracket `<placeholders>` take a value inline. *Italic lines* are whole-section guidance — replace each with
  real content. Neither survives into the artifact.
- Everything else is fixed wording and ships verbatim — in particular the sketch disclaimer that opens `## Changes`
  and the pause-point note under manual verification.
- Restating design and research content in the plan is intended, not duplication: `/implement`'s subagents read only
  `index.md` plus their one phase file, so self-containment requires the restatement.

## Index template — `plan/index.md`

The index holds everything shared across phases; phase files cite it rather than repeating it.

````markdown
# Plan: <feature name> — index

> Status: <one line, e.g. "ready for implementation">. Audience: the implementing agent; humans spot-check.

## Overview

*What is being built and why — 3–5 sentences.*

## Current state

*How the relevant system works as implementation begins. Key facts restated from design and research with file:line
citations — an implementer must not need the other artifacts open.*

## Desired end state

*The observable behaviour once the whole plan lands, and how it is verified — from `design.md`.*

## Key discoveries

*The research findings that shaped the approach, each with a file:line citation.*

## Durable decisions

*The binding judgments every phase inherits — technology choices, patterns, integration boundaries. Number them so
phase files can cite them. Violating one fails the phase.*

## What we're NOT doing

*Explicit scope exclusions, from the design — the things a well-meaning implementer might otherwise add.*

## Implementation approach

*The strategy across the phases — one short section, not a restatement of the phase index.*

## Testing strategy

*How verification layers across the phases — what unit tests cover, what integration tests cover, what stays manual.
Per-phase checkpoints reference this rather than restating it.*

## Performance and migration notes

*Only when the work genuinely has them — data migrations, load concerns, rollout ordering. Omit the section
otherwise; never write "N/A".*

## Phase index

| Phase | Title | End-to-end behaviour | Depends on | Document |
|---|---|---|---|---|
| 1 | <title> | <one line — what becomes observable> | — | [phase-1-<slug>.md](phase-1-<slug>.md) |
| 2 | <title> | <one line — what becomes observable> | Phase 1 | [phase-2-<slug>.md](phase-2-<slug>.md) |

## References

*Paths to `task.md`, `research.md`, `design.md`, `structure.md` — whichever exist.*
````

## Phase template — `plan/phase-N-<slug>.md`

One file per phase, self-contained: an agent given only `index.md` and this file implements the phase. The sketch
disclaimer under `## Changes` is fixed wording — every phase file carries it, above the first sketch.

````markdown
# Phase <N>: <title>

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

*This slice's end-to-end behaviour, and why it comes at this point in the sequence.*

## Context

*The restated background this phase's implementer needs — how the touched code works today, the patterns to follow,
the durable decisions that bear on this slice (cite them by number) — with file:line citations. Self-containment
test: an agent reading only `index.md` and this file could implement the phase without opening research or design.*

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

*Group the changes by the slice's end-to-end path — the order the behaviour flows, not layer by layer. Each change
names its file(s), summarises the change, and sketches the intended shape.*

### 1. <first step on the end-to-end path>

**File**: `path/to/file.ext`
**Change**: <one-line summary>

```<language>
<intended shape — signatures and key logic, not a finished diff>
```

### 2. <next step on the path>

*Same shape as above; as many numbered changes as the path needs.*

## Success criteria

### Automated verification

*Checkbox list of commands an agent can run, using the project's actual commands. Include the slice's test checkpoint
from `structure.md`.*

- [ ] <what it proves>: `<command>`

### Manual verification

*Checkbox list of steps a human performs — behaviour observed in the running system, edge cases hard to automate. If
the phase truly has none, write "None" and drop the pause-point note below.*

- [ ] <step a human performs, and what they should observe>

A phase with manual steps is a pause point: the orchestrator must wait for the user to confirm them before starting
the next phase.

## Dependencies

- **Depends on**: <phase number(s), or "None">
- **Blocks**: <phase number(s), or "None">
````
