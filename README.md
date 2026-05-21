# Skills

A collection of Claude Code skills for my development workflow, inspired
by [Matt Pocock's skills repo](https://github.com/mattpocock/skills/tree/main).

## Credits

The workflow pipeline skills (`/grill-me`, `/to-prd`, `/tdd`) were adapted
from [Matt Pocock](https://github.com/mattpocock)'s work. `/grill-me` and `/to-prd` have been reworked to tighten the
flow; `/tdd` is mostly the same - it's already a great skill, and the only change is to compose the `/code-doc` skill
within. `/to-plan` was originally derived from Pocock's work but has since been rewritten substantially enough to be
considered its own skill. `/code-doc` is original.

`/skill-creator` was copied from Anthropic's [skill](https://github.com/anthropics/skills/tree/main) repo - it works to
a degree, though the eval scripts and handling need work.

`/dg` was adapted from [v1r3n/dinesh-gilfoyle](https://github.com/v1r3n/dinesh-gilfoyle), with the comic panel
capability removed, and Gradle handling and CVE analysis tightened.

---

## Skills

### `/grill-me`

Relentlessly interviews you about a plan or design until you reach a shared understanding. Drills into every decision
point one at a time, resolves cross-cutting dependencies explicitly, and produces a **Decision Snapshot** — a historical
record of what was discussed and agreed. The Snapshot feeds downstream documents like PRDs and plans.

### `/to-prd`

Turns conversation context and a Decision Snapshot into a formal PRD saved to `.planning/`. Best for larger features
that will be broken into multiple plans, or when a standalone requirements document is needed for stakeholders. Small,
well-defined changes can skip this step and go straight to `/to-plan`.

### `/to-plan`

Breaks a PRD or Decision Snapshot into a phased implementation plan using **tracer bullet** vertical slices. Each phase
is a thin, end-to-end slice that cuts through all relevant integration layers and is independently demoable or
verifiable. Produces a plan index and per-phase documents in `.planning/`.

### `/tdd`

Runs the red-green-refactor loop for a given phase or feature. Emphasises testing behaviour through public interfaces
rather than implementation details, and strictly enforces vertical slicing — one test, one implementation, repeat.
Avoids horizontal slicing (writing all tests before writing any code).

### `/code-doc`

Guidelines and review for writing high-quality documentation comments across any language (KDoc, Javadoc, JSDoc,
docstrings, etc.). Focuses on documenting the interface — what callers need to know — rather than restating what the
code does. Includes language-specific reference files where conventions differ.

### `/skill-creator`

Creates new skills and iteratively improves existing ones. Walks through the full loop: capturing intent, drafting the
skill, writing test cases, running evals, reviewing results, and revising. Also runs the skill description optimiser to
improve triggering accuracy.

### `/dg`

An adversarial code review in the style of Dinesh vs. Gilfoyle from HBO's Silicon Valley. Gilfoyle attacks the code with
withering technical precision; Dinesh defends it with flustered competence. The banter entertains; the back-and-forth
produces genuinely better reviews. Includes Gradle dependency analysis and CVE scanning.

```
/dg                              → review local git diff
/dg <path>                       → review a specific file
/dg --pr <branch>                → review a PR branch vs main
/dg --pr <branch> <path>         → PR review scoped to a path
```

---

## Workflow

These skills are designed to work together in a structured development workflow:

```
/grill-me  →  [/to-prd]  →  /to-plan  →  /tdd
```

### 1. `/grill-me` — Stress-test your thinking

Start here when you have an idea but haven't fully worked through the design. The skill drills into every decision
point, resolves dependencies between decisions, and ends with a Decision Snapshot that captures what was agreed.

### 2. `/to-prd` _(optional — skip for small changes)_

If the feature is large enough to warrant a formal requirements document, use this to turn the Decision Snapshot into a
PRD. Useful for cross-team alignment or when a feature will be broken into multiple plans. For smaller changes, you can
feed the Snapshot directly into `/to-plan`.

### 3. `/to-plan` — Slice the work

Break the PRD (or Snapshot) into a phased plan of tracer bullet vertical slices. Each phase should be thin, end-to-end,
and independently verifiable — no big-bang phases.

### 4. `/tdd` — Implement phase by phase

Take each phase into a red-green-refactor loop. One test at a time, one implementation at a time. The skill enforces
vertical slicing and keeps tests focused on public behaviour rather than internal structure.
