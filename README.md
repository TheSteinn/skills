# Skills

A collection of agent skills for a structured development workflow — from a raw task, through researched facts and a
deep-reviewed design, to test-driven implementation and a pull request. Supporting skills cover domain documentation,
doc comments, and code review.

The heart of the repo is the **QRSPI pipeline** — Question → Research → Design → Structure → Plan → Implement → PR,
run as six separate invocations. Its economics are the point: you deep-review the design, the structure, and the code
at PR — never the long plan, which is written for the implementing agent and only spot-checked. Each run's artifacts
live in `.planning/<feature>/`, so every phase can start from a fresh session and rebuild from disk.

## Credits

This repo is a collection of skills inspired by and adapted from the following creators:

- **[Dex Horthy](https://github.com/dexhorthy) / HumanLayer** — the QRSPI workflow, as written up in
  [From RPI to QRSPI](https://alexlavaee.me/blog/from-rpi-to-qrspi/), is the origin of the six pipeline skills
- **[Matt Pocock](https://github.com/mattpocock)** — his [skills repo](https://github.com/mattpocock/skills) is the
  origin of `/grill-me`, `/tdd`, and this repo's original planning pipeline (the since-retired `/to-prd`, whose
  Decision Snapshot → PRD → plan → orchestrate flow the QRSPI pipeline replaced), and of the domain-docs approach
  (`LANGUAGE.md`, ADRs) that `/grill-with-docs` and `/initialise-docs` build on
- **[Anthropic](https://github.com/anthropics/skills)** — `/skill-creator`
- **[v1r3n](https://github.com/v1r3n/dinesh-gilfoyle)** — `/dg`

Where a skill deliberately diverges from its source, the reasoning lives in [docs/](docs) — see
[grill-me](docs/grill-me.md) and [grill-with-docs](docs/grill-with-docs.md), and one record per pipeline skill:
[research](docs/research.md), [design](docs/design.md), [structure](docs/structure.md),
[write-plan](docs/write-plan.md), [implement](docs/implement.md), and [open-pr](docs/open-pr.md).

---

## Installation

The [install script](install.sh) will install the skills into the `.agents/skills/` directory. For agents that use a
different directory, you can symlink the skills into the correct location.

Alternatively, clone the repo to the appropriate agent skills directory.

---

## Skills

### QRSPI pipeline

A port of Dex Horthy's QRSPI workflow — each phase a separate small invocation, reviewed by the human at the cheap
artifacts. There is no dispatcher: a phase runs because you invoke it, and each one consumes whatever upstream
artifacts exist in `.planning/<feature>/`.

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

#### `/implement`

Executes the plan phase by phase as a pure orchestrator: each phase goes to a fresh subagent whose prompt starts with
`/tdd` and hands it two file paths — the plan index and its own phase file — as persisted memory, hard-scoped to
exactly that phase. Subagents follow the plan's intent while adapting to what they find, reporting every mismatch; the
orchestrator triages each one — a hard stop with a structured report, a soft stop for your confirmation, or a noted
deviation. It re-runs the automated success criteria itself, lands **one atomic commit per completed phase**, and
pauses for your manual verification steps. Assumes you have already prepared the branch or worktree: it makes no
git-setup moves of its own.

#### `/open-pr`

Delivers the work as a pull request whose description is grounded in `design.md` — Why, What changed, Decisions
exercised, and Verification, pitched at behaviour and design choices rather than file-by-file detail — so review is
**confirmation of decisions you already approved**, not discovery. Uses whatever forge CLI is available and
authenticated, and confirms the title, description, and target branch with you before pushing anything. Ends with the
pipeline's one non-negotiable: now read the code.

#### A typical run

```
/research <task>   → task.md, questions.md, research.md
/clear
/design            → design.md                      ← deep-review this
/clear
/structure         → structure.md                   ← deep-review this
/clear
/write-plan        → plan/index.md + phase files    ← spot-check only
/clear             (and prepare the branch or worktree yourself)
/implement         → one commit per completed phase
/clear
/open-pr           → the pull request               ← now read the code
```

Every artifact lands in `.planning/<feature>/`, and each phase rebuilds from those files rather than the previous
conversation — that's what the `/clear` between phases buys: a fresh context at no cost to continuity. The branch or
worktree is your job: prepare it before `/implement`, which makes no git-setup moves of its own.

### Standalone

#### `/grill-me`

Relentlessly interviews you about a plan or design until you reach a shared understanding. Drills into every decision
point one at a time, recommends an answer with each question, resolves cross-cutting dependencies explicitly, and
closes with a decision record — one entry per topic, final resolution and rationale. On request it persists the record
to `.planning/decisions-<feature>.md`, ready to seed the pipeline as already-resolved input to `/design`.

#### `/grill-with-docs`

Everything `/grill-me` does, with the project's documented domain language as a live participant. It challenges your
plan against `LANGUAGE.md`, sharpens fuzzy terminology the moment it appears, writes resolved terms into the glossary
inline — at peak attention, never batched at the end — and offers an ADR when a decision genuinely warrants one (hard
to reverse, surprising without context, a real trade-off). Use it when the grill should leave durable docs behind;
use plain `/grill-me` when it shouldn't.

#### `/improve-codebase-design`

Scans the codebase for **deepening opportunities** — shallow modules that could hide more behaviour behind smaller
interfaces — and presents the candidates as a visual HTML report: before/after diagrams, benefits in terms of locality
and leverage, and a top recommendation. Pick one and it grills through the design with you, recording glossary terms
and ADRs as decisions crystallise; from there the pipeline takes over, with the chosen deepening as `/research`'s
task.

#### `/initialise-docs`

One-time bootstrap for a repo's domain documentation. Wires up the consumer pointer (`docs/agents/domain.md` plus a
`## Domain docs` block in `CLAUDE.md`/`AGENTS.md`), confirms context boundaries with you (with monorepo module
detection), and proposes a draft `LANGUAGE.md` per chosen module from a codebase scan. Breadth, not depth — it gets a
reasonable starting glossary in place fast and hands refinement to `/grill-with-docs`. Requires `/grill-with-docs` to
be installed (it owns the shared format specs), and only ever runs when you invoke it explicitly.

#### `/tdd`

Runs the red-green-refactor loop for a given phase or feature. Emphasises testing behaviour through public interfaces
rather than implementation details, and strictly enforces vertical slicing — one test, one implementation, repeat.
Avoids horizontal slicing (writing all tests before writing any code).

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

### Utilities

#### `/acli`

A verified reference for Atlassian's official CLI (`acli`) covering Jira and Confluence Cloud: JQL searches, work
items, transitions, comments, sprints, boards, and Confluence pages, plus the rules that keep generated commands from
breaking — long-form flags always, `--json` everywhere, `--yes` on bulk operations. Org specifics (site, project keys,
board IDs, workflow statuses) live in a user-maintained setup file outside the skill directory; the skill reads it and
asks you rather than guessing.

#### `/skill-creator`

Creates new skills and iteratively improves existing ones. Walks through the full loop: capturing intent, drafting the
skill, writing test cases, running evals, reviewing results, and revising. Also runs the skill description optimiser
to improve triggering accuracy.
