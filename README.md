# Skills

A collection of agent skills for a structured development workflow — from stress-testing an idea, through decision
records and phased plans, to test-driven implementation. Supporting skills cover domain documentation, doc comments,
and code review.

The heart of the repo is a pipeline: grill a design until it holds up, capture what was decided, slice it into a plan,
and implement it phase by phase. Each skill works standalone, but they're designed to hand off to each other.

## Credits

This repo is a collection of skills inspired by and adapted from the following creators:

- **[Matt Pocock](https://github.com/mattpocock)** — his [skills repo](https://github.com/mattpocock/skills) is the
  origin of the planning pipeline (`/grill-me`, `/tdd`, and the since-retired `/to-prd`) and of the domain-docs
  approach (`LANGUAGE.md`, ADRs) that `/grill-with-docs` and `/initialise-docs` build on
- **[Anthropic](https://github.com/anthropics/skills)** — `/skill-creator`
- **[v1r3n](https://github.com/v1r3n/dinesh-gilfoyle)** — `/dg`

Where a skill deliberately diverges from its source, the reasoning lives in [docs/](docs) — see
[grill-me](docs/grill-me.md) and [grill-with-docs](docs/grill-with-docs.md).

---

## Installation

The [install script](install.sh) will install the skills into the `.agents/skills/` directory. For agents that use a
different directory, you can symlink the skills into the correct location.

Alternatively, clone the repo to the appropriate agent skills directory.

---

## Skills

### QRSPI pipeline

A port of Dex Horthy's QRSPI workflow — each phase a separate small invocation, reviewed by the human at the cheap
artifacts.

#### `/research`

Decomposes a task into neutral research questions, then answers them with **task-blind subagents** — researcher
prompts never contain the task, so the findings describe what the codebase is rather than evidence for the change you
have in mind. Produces `task.md`, `questions.md`, and a cited, recommendation-free `research.md` in
`.planning/<feature>/`, ready for the design step to build on.

#### `/design`

Brain-dumps a ~200-line design — current state, desired end state, patterns to follow, resolved decisions, open
questions — from `task.md` and `research.md`, then **grills the open questions** until every branch is resolved or
explicitly parked, writing resolutions straight into the document as they land. Produces `design.md` in
`.planning/<feature>/`: the pipeline's main alignment gate, deep-reviewed by you before any code exists.

#### `/structure`

Slices the approved design into ordered **tracer-bullet vertical slices** — each cutting end-to-end through the layers
it touches, named for its observable behaviour, and carrying a test checkpoint — then reviews the granularity with
you, merging and splitting until it's right. Produces `structure.md` (~2 pages) in `.planning/<feature>/`: the second
alignment gate, at header-file altitude — order, checkpoints, and signature sketches, never implementation.

#### `/write-plan`

Expands the approved structure into the tactical plan the implementing agent executes — one plan phase per approved
slice, written as an index plus **self-contained phase files** that restate the context each implementer needs, show
code sketches as targets (not prescriptions — the failing test still comes first), and split success criteria into
automated and manual checks. Produces `plan/index.md` and per-phase files in `.planning/<feature>/`: the artifact you
spot-check rather than deep-review, because the deep review already happened at design and structure.

### Planning

#### `/grill-me`

Relentlessly interviews you about a plan or design until you reach a shared understanding. Drills into every decision
point one at a time, resolves cross-cutting dependencies explicitly, and produces a **Decision Snapshot** — a
historical record of what was discussed and agreed. The Snapshot feeds downstream documents like PRDs and plans.

#### `/grill-with-docs`

Everything `/grill-me` does, with the project's documented domain language as a live participant. It challenges your
plan against `LANGUAGE.md`, sharpens fuzzy terminology the moment it appears, writes resolved terms into the glossary
inline — at peak attention, never batched at the end — and offers an ADR when a decision genuinely warrants one (hard
to reverse, surprising without context, a real trade-off). Use it when the grill should leave durable docs behind;
use plain `/grill-me` when it shouldn't.

### Implementation

#### `/tdd`

Runs the red-green-refactor loop for a given phase or feature. Emphasises testing behaviour through public interfaces
rather than implementation details, and strictly enforces vertical slicing — one test, one implementation, repeat.
Avoids horizontal slicing (writing all tests before writing any code).

#### `/orchestrate-plan`

Implements a multi-phase plan by delegation: the session acts purely as an orchestrator, handing each phase to a
dedicated subagent that runs `/tdd`, verifying acceptance criteria as phases complete, and re-delegating when a
criterion fails. If a phase fails twice, it stops and hands back to you to course-correct. An alternative to driving
`/tdd` phase by phase yourself.

### Domain documentation

#### `/initialise-docs`

One-time bootstrap for a repo's domain documentation. Wires up the consumer pointer (`docs/agents/domain.md` plus a
`## Domain docs` block in `CLAUDE.md`/`AGENTS.md`), confirms context boundaries with you (with monorepo module
detection), and proposes a draft `LANGUAGE.md` per chosen module from a codebase scan. Breadth, not depth — it gets a
reasonable starting glossary in place fast and hands refinement to `/grill-with-docs`. Requires `/grill-with-docs` to
be installed (it owns the shared format specs), and only ever runs when you invoke it explicitly.

### Review

#### `/code-doc`

Guidelines and review for writing high-quality documentation comments across any language (KDoc, Javadoc, JSDoc,
docstrings, etc.). Focuses on documenting the interface — what callers need to know — rather than restating what the
code does. Includes language-specific reference files where conventions differ.

#### `/dg`

An adversarial code review in the style of Dinesh vs. Gilfoyle from HBO's Silicon Valley. Gilfoyle attacks the code
with withering technical precision; Dinesh defends it with flustered competence. The banter entertains; the
back-and-forth produces genuinely better reviews. Includes Gradle dependency analysis and CVE scanning.

```
/dg                              → review local git diff
/dg <path>                       → review a specific file
/dg --pr <branch>                → review a PR branch vs main
/dg --pr <branch> <path>         → PR review scoped to a path
```

### Meta

#### `/skill-creator`

Creates new skills and iteratively improves existing ones. Walks through the full loop: capturing intent, drafting the
skill, writing test cases, running evals, reviewing results, and revising. Also runs the skill description optimiser
to improve triggering accuracy.

---

## Workflow

The pipeline runs from idea to implementation:

```
/grill-me ───────────┐
                     ├──→  [/to-prd]  ──→  /to-plan  ──→  /tdd  or  /orchestrate-plan
/grill-with-docs ────┘
```

With `/initialise-docs` as a one-time precursor in repos that document their domain language.

### 0. `/initialise-docs` — once per repo _(optional)_

Bootstrap the domain docs: consumer wiring, context boundaries, and a draft starting glossary. After this, the
project's language is something every later session can read — and `/grill-with-docs` has something to challenge
your plans against.

### 1. `/grill-me` or `/grill-with-docs` — stress-test your thinking

Start here when you have an idea but haven't fully worked through the design. Both run the same relentless interview —
one question at a time, dependencies resolved explicitly, ending in a Decision Snapshot. The difference is what they
leave behind: `/grill-with-docs` also maintains the durable docs (`LANGUAGE.md`, ADRs) as decisions crystallise, while
`/grill-me` mutates nothing — the right choice for proofs of concept and plans that shouldn't touch the project's
canonical language.

### 2. `/to-prd` _(optional — skip for small changes)_

If the feature is large enough to warrant a formal requirements document, turn the Decision Snapshot into a PRD.
Useful for cross-team alignment or when a feature will be broken into multiple plans. For smaller changes, feed the
Snapshot directly into `/to-plan`.

### 3. `/to-plan` — slice the work

Break the PRD (or Snapshot) into a phased plan of tracer bullet vertical slices. Each phase should be thin,
end-to-end, and independently verifiable — no big-bang phases.

### 4. `/tdd` or `/orchestrate-plan` — implement phase by phase

Take each phase through a red-green-refactor loop with `/tdd` — one test at a time, one implementation at a time. Or
hand the whole plan to `/orchestrate-plan` and let it delegate each phase to a `/tdd` subagent while it tracks
acceptance criteria.

Along the way: `/code-doc` keeps doc comments honest (it's composed into `/tdd`), and `/dg` reviews the result with
maximum prejudice.
