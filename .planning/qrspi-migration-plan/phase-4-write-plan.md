# Phase 4: `/write-plan`

> Source: [index.md](index.md) · structure slice 4. Self-contained: implement from this file +
> the index only.

## Overview

Create the tactical-plan generator: `/write-plan` expands the approved structure into a plan
**for the agent** — the human spot-checks. The artifact is V1 `create_plan`'s template adapted
near-fully (QRSPI reused that template verbatim and changed only its audience): overview,
current and desired state, key discoveries, implementation approach, testing strategy,
per-phase changes with code sketches, automated/manual success criteria, what-we're-NOT-doing.
The one deliberate inheritance from this repo's `to-plan` is the **layout** — index +
self-contained per-phase files (resolution 3: progressive disclosure for `/implement`'s
subagents). `to-plan`'s detail-lightness is explicitly NOT carried forward. This phase
completes `to-plan`'s replacement, so **`to-plan` is deleted here**, and
`improve-codebase-design`'s closing handoff is retargeted off it.

## Changes required

### 1. Create `skills/write-plan/SKILL.md`

Target sketch — a floor, not the finished file (index: "sketches are floors"): flesh out into
a polished skill; structure, gates, and voice are fixed.

```markdown
---
name: write-plan
description: QRSPI step 4 — expand the approved structure into a tactical plan for the implementing agent - an index plus one self-contained file per phase, with code sketches and success criteria. Humans spot-check; deep review already happened.
disable-model-invocation: true
---

# Write Plan

Expand `structure.md` into the tactical plan `/implement` executes. The audience is an agent,
not a human — the human spot-checks it. Alignment already happened at design and structure;
your job here is completeness, not persuasion.

## 1. Load the artifacts

Locate `.planning/<slug>/` (take the slug from the invocation; if none was given and exactly
one directory exists, use it; otherwise ask the user; if none exists, create it and capture
the task from the invocation or conversation into `task.md`). Read whichever of `task.md`,
`research.md`, `design.md`, and `structure.md` exist, fully. No upstream phase is mandatory —
source missing context from the conversation and the user rather than refusing; planning is
the pipeline's one near-universal phase.

## 2. Phase breakdown: mirror structure, or earn approval

When `structure.md` exists: one plan phase per approved slice, same order, same scope — do not
re-slice. If detailed planning reveals a genuine slicing problem, STOP, explain it, and send
the user back to `/structure`; never silently restructure.

When structure was skipped: draft the phase breakdown yourself under the same discipline —
every phase end-to-end and demoable with a test checkpoint, never a layer — and get the user's
approval on the breakdown before writing any phase file.

## 3. Write the plan

Follow the templates in [references/plan-template.md](references/plan-template.md) exactly:
`plan/index.md` plus one `plan/phase-N-<slug>.md` per phase. Four rules trump everything in the
templates:

- **Self-containment.** An agent given only `index.md` and one phase file must be able to
  implement that phase — restate whatever context it needs; cite research and design by
  file:line rather than assuming they'll be read.
- **Code sketches are targets, not prescriptions.** They show intended shape; the implementing
  agent still writes the failing test first, and reports mismatches instead of improvising.
  Say this above the first sketch in every phase file (the template has the wording).
- **Success criteria are split** per phase: automated verification (commands an agent runs)
  and manual verification (steps a human performs). Fold the slice's test checkpoint from
  `structure.md` into the automated half wherever possible.
- **No open questions.** If you hit a decision the artifacts don't answer, STOP and ask the
  user — every decision is made before the plan is final.

## 4. Hand off

Tell the user the plan is ready for a spot-check (deep review already happened upstream), list
the phase files, and point at `/implement` as the next step — best run in a fresh session
(`/clear`) once the user has prepared the branch or worktree the implementation should happen
on.
```

### 2. Create `skills/write-plan/references/plan-template.md`

Adapted from V1 `create_plan.md`'s template, lines 182–277 (path in the index References).
QRSPI reused that template deliberately — carry its sections over rather than slimming them.
Restating design/research content in the plan is intended, not duplication: `/implement`'s
subagents read only the plan, so self-containment requires it.

**Index template** (`plan/index.md`), tracking V1's top-level sections:

- Title + one-line status; `## Overview` — what is being built and why (3–5 sentences).
- `## Current state` — how the relevant system works as implementation begins; key facts
  restated from design/research with file:line citations.
- `## Desired end state` — observable behaviour when the whole plan lands, and how it is
  verified (from `design.md`).
- `## Key discoveries` — the research findings that shaped the approach, with citations.
- `## Durable decisions` — the binding judgments every phase inherits (technology choices,
  patterns, integration boundaries); violating one fails a phase.
- `## What we're NOT doing` — explicit scope exclusions (from the design).
- `## Implementation approach` — the strategy across the phases, one short section.
- `## Testing strategy` — how verification layers across phases (unit / integration / manual);
  per-phase checkpoints reference this.
- `## Performance and migration notes` — only when the work genuinely has them; omit the
  section otherwise.
- `## Phase index` — table: N, title, end-to-end behaviour, depends-on, link.
- `## References` — task/research/design/structure paths.

**Phase template** (`plan/phase-N-<slug>.md`), the V1 per-phase shape:

- Title + link to index; `## Overview` — this slice's end-to-end behaviour and why it's next.
- `## Context` — the restated background an implementer needs, with file:line citations; must
  pass the self-containment test (index + this file only).
- `## Changes` — grouped by the slice's end-to-end path; each change names files and shows a
  code sketch in a fenced block, under the fixed wording: *"Sketches are targets, not
  prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
  mismatch protocol rather than improvising."*
- `## Success criteria` — `### Automated verification` (checkbox list of runnable commands,
  including the structure checkpoint's test command) and `### Manual verification` (checkbox
  list of human steps). A phase with manual steps is a pause point: the template notes the
  orchestrator must wait for the user before the next phase — V1's per-phase "Implementation
  Note" carried into the artifact.
- `## Dependencies` — depends-on / blocks.

**Cuts from V1, stated at the top of the reference so future editors don't reintroduce them** —
these three only; every other V1 section carries over:

- no "Common Patterns" recipes (V1's were horizontal, layer-by-layer — the disease `/structure`
  exists to cure);
- no org-specific machinery (thoughts sync, ticket tooling, hardcoded `make` targets — success
  criteria use the project's actual commands);
- no process steps (research/alignment live in earlier pipeline phases, not in the plan
  prompt).

### 3. Delete `skills/to-plan/`

`git rm -r skills/to-plan`.

### 4. Edit `skills/improve-codebase-design/SKILL.md` (exact edit)

The closing paragraph currently ends:

> …can persist it to `.planning/decisions-<feature>.md` — from there, `/to-plan` turns the
> chosen deepening into a phased plan and `/tdd` drives the implementation.

Replace the part after the em-dash with:

> — from there, the QRSPI pipeline takes over: run `/research` with the chosen deepening as the
> task, and bring the persisted decision record into `/design` as already-resolved input.

### 5. Create `docs/write-plan.md` (deviation record)

Must cover, with reasons: (a) the plan is demoted from human review artifact to tactical
document for the agent — QRSPI's re-pricing, unchanged; (b) sharded as index + self-contained
phase files instead of QRSPI's single ~8-page plan.md — progressive disclosure: `/implement`'s
subagents load exactly one phase; (c) V1 template adapted with three cuts (horizontal recipes,
org machinery, process monolith) as objectively bad practice; (d) code sketches retained from
V1 but reconciled with this repo's TDD mandate — sketches are targets, tests come first; (e)
`to-plan` retired: slicing rules moved to `/structure` (phase 3), layout absorbed here; its
deliberate detail-lightness is the one part not carried forward, by explicit decision.

### 6. Edit `README.md`

Add `#### /write-plan` under the QRSPI pipeline section; remove the `#### /to-plan` entry;
adjust any Planning-section prose that names `to-plan` as the pipeline's plan step. Leave
`orchestrate-plan`'s entry alone (dies in phase 5).

## Success criteria

### Automated verification

- [ ] `test -f skills/write-plan/SKILL.md && test -f skills/write-plan/references/plan-template.md && test -f docs/write-plan.md`
- [ ] `grep -q 'disable-model-invocation: true' skills/write-plan/SKILL.md`
- [ ] `test ! -d skills/to-plan`
- [ ] `! grep -rn 'to-plan' skills/` (in particular, `improve-codebase-design` no longer
      references it)
- [ ] `grep -qi 'targets, not prescriptions' skills/write-plan/references/plan-template.md`
- [ ] `grep -qi 'Testing strategy' skills/write-plan/references/plan-template.md && grep -qi 'Key discoveries' skills/write-plan/references/plan-template.md` (the V1 sections survived adaptation)
- [ ] `grep -q '/write-plan' README.md && ! grep -q '#### \`/to-plan\`' README.md`

### Manual verification

- [ ] Instruction count of SKILL.md body < 40.
- [ ] Run `/write-plan` on phase 3's micro-task structure: phases mirror slices 1:1; each phase
      file passes the self-containment test — read one in isolation (plus index) and confirm
      you could implement it without the other artifacts open; criteria are split
      automated/manual; the sketch disclaimer appears above the first sketch.
- [ ] Confirm no phase in the generated plan is a layer ("the database phase") rather than a
      behaviour.
- [ ] Skip test: run once with `structure.md` absent — it drafts its own vertical breakdown
      and gets the user's approval before writing any phase file.

## What this phase is NOT doing

No execution logic (that is `/implement`); no README narrative rewrite; no changes to `tdd`
(phase 5) or to the grill family.

## Dependencies

Phase 3 (consumes `structure.md`; verified against its micro-task output).
