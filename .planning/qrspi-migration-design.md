# Design: Restructuring the skills repo around QRSPI

Sources: `.planning/qrspi-understanding.md` (primary), the five `humanlayer-*.md` V1 analyses,
and the current `skills/` inventory. Status: **open questions resolved with Codey — awaiting
design sign-off**.

## 1. Current state

The repo's core pipeline is `grill(-me|-with-docs)` → Decision Snapshot → `to-prd` → `to-plan` →
`orchestrate-plan` (+ `tdd` per phase). Supporting skills: `codebase-designing`, `domain-modelling`,
`initialise-docs`, `improve-codebase-design`, `code-doc`. Utilities: `acli`, `dg`, `skill-creator`.

Measured against QRSPI, the pipeline already has real overlap:

- **Vertical slices are native.** `to-plan`'s tracer-bullet rules are QRSPI's Structure-phase
  cure for horizontal plans, already written down.
- **State lives in `.planning/` artifacts** (Snapshot, PRD, plan index, phase docs) — QRSPI's
  static-artifact principle, already the convention.
- **Human-driven questioning exists** (`grilling`) — stronger than QRSPI's bare "present open
  questions first" gate, because it walks the whole decision tree.
- **Subagent delegation exists** (`orchestrate-plan`, `improve-codebase-design`).

What's missing entirely: a **Question** phase (task → neutral research questions), a firewalled
**Research** phase, a **design.md** artifact (the main alignment gate), **worktree isolation**,
**commit-per-phase**, and a **PR** phase grounded in the design. And the current pipeline's
review economics are inverted relative to QRSPI: the human's deep-review artifacts today are the
PRD and the plan — exactly the artifacts QRSPI demotes.

## 2. Desired end state

A six-invocation pipeline, each skill user-invoked (`disable-model-invocation: true`), each under
40 instructions, each reading only its permitted artifacts from `.planning/<feature>/` and writing
its artifact(s) before stopping:

| Invocation | QRSPI phase(s) | Reads | Writes | Human gate |
|---|---|---|---|---|
| `/research` | Question + Research | the task (from user/ticket) | `task.md`, `questions.md`, `research.md` | optional pause on questions; skim research |
| `/design` | Design | task + research | `design.md` (~200 lines) | **deep review** — grill runs here |
| `/structure` | Structure | design + task + research | `structure.md` (~2 pages) | **deep review** of slicing |
| `/write-plan` | Plan | all prior artifacts | `plan.md` index + per-phase docs | spot-check |
| `/implement` | Implement | plan (+ structure checkpoints) | code; one commit per phase, in a user-prepared worktree/branch | verify at checkpoints |
| `/open-pr` | PR | design + the diff | a pull request | **read the code** |

Names: bare verbs where unambiguous; `/write-plan` and `/open-pr` renamed to dodge collisions
with built-ins and common skill names (`/plan`, `/pr`).

**No phase is mandatory.** Each skill consumes whatever upstream artifacts exist and sources
the rest from the invocation, conversation, or the user — prompting, never hard-failing, when
something is absent. Research can be skipped when there is little to research; design and/or
structure can be skipped for small changes. The one hard prerequisite: `/implement` requires a
plan (implementing without one is just `/tdd` on the target change). When structure is
skipped, `/write-plan` proposes its own vertical breakdown and gets the user's approval before
writing, so the slicing discipline survives the skip.

Existing keepers (`grilling`, `codebase-designing`, `domain-modelling`, `tdd`, `code-doc`, etc.)
plug into phases rather than being replaced — see §4.

## 3. Resolved design decisions

**D1 — Phase-per-skill topology, reconciled with the context-cost rule.**
QRSPI wants each phase as a separate small invocation; the repo rule ("inline-steps-over-subskills")
says every skill description costs context in every session. These don't actually conflict: the
cost applies to *model-invocable* skills. Pipeline phases are **human-invoked gates by design** —
the human deciding "design is approved, run /structure" *is* QRSPI's control flow. So every phase
skill carries `disable-model-invocation: true`: zero per-session description cost, and phase
transitions stay where QRSPI puts them — with the human. No dispatcher skill: a dispatcher would
re-create V1's monolith (one context window holding all phases, gates as prose).
*(Mechanics verified against Claude Code docs: `disable-model-invocation: true` keeps the
description out of context entirely; the full skill loads only on explicit `/name`.)*

**D2 — Six invocations, not eight.** Two QRSPI phases have no mandatory human gate and merge into
their neighbours, recorded as deliberate deviations:
- *Question + Research merge into `/research`.* QRSPI's human check on questions is optional
  ("sanity-check"). The skill decomposes the task into neutral questions, offers the pause, then
  runs research. The firewall survives the merge (see D3).
- *Worktree leaves skill scope entirely.* Worktree is a mechanism, not an alignment gate —
  nothing to review. `/implement` assumes the user has already configured the worktree/branch
  before invoking it and makes no git-setup moves of its own; isolation is the human's setup
  step. (Deviation: QRSPI names Worktree as a phase; we delegate it to the user.)

**D3 — The research firewall maps onto subagents, not fresh top-level windows.**
Claude Code skills run in the main conversation, which by then has seen the task — so the main
window plays QRSPI's *query planner* role (allowed to see the task; authors the neutral
questions), and **blind subagents play the executor**: each research subagent receives only
`questions.md` content, never `task.md`, never conversation history (verified: general-purpose
subagents start with fresh context — no parent conversation). Synthesis is also done by a blind subagent (reads questions + sub-findings,
writes `research.md`) so opinion can't leak back in at synthesis time — the V1 failure where
decomposition and synthesis lived in the contaminated window. Research fan-out keeps V1's
surviving pattern: locator / analyzer / pattern-finder axes, file:line citations, self-contained
doc with provenance frontmatter.

**D4 — "Fresh window per phase" becomes a documented convention, not a mechanism.**
Skills cannot force `/clear`. Instead: every artifact is self-contained (QRSPI's own invariant),
every phase skill begins by reading its permitted artifacts from disk and depends on nothing in
the conversation, and each skill's closing line recommends clearing before the next phase. This
is a deviation with a reason: the enforcement Claude Code *can* give (artifacts on disk, blind
subagents) covers the contamination risks that matter; a stale main window merely wastes context,
it doesn't corrupt artifacts.

**D5 — `grilling` becomes the Design phase's questioning engine.** QRSPI's Design phase mandates
"open questions first." This repo already has a stronger version — the relentless decision-tree
walk. `/design` composes it: brain-dump (current state, desired end state, patterns to follow,
resolved decisions) + grill the open questions + write `design.md`. `codebase-designing`
supplies the vocabulary for "patterns to follow" and seam decisions; `domain-modelling` rides
along for durable glossary/ADR writes when the project keeps domain docs. The skill stays
domain-neutral — no frontend/backend bias; instead, one medium-neutral rule: when a decision
can't be reviewed in prose (a UI layout, a schema shape), `design.md` links the cheapest
reviewable supporting artifact (an HTML sketch, a diagram) — review economics applied to
medium. This is a deliberate
*improvement* deviation: QRSPI asks questions once; we grill until resolved. `grill-me` /
`grill-with-docs` stay as standalone entries for non-pipeline use (they cost no context).
Constraint (verified): a skill can only compose a target that remains model-invocable, so
`grilling` keeps `user-invocable: false` and keeps paying its description cost — justified by
its four consumers.

**D6 — TDD stays the implementation engine.** QRSPI explicitly punts on testing ("a whole other
talk"). This repo has a stance: `/implement` delegates each phase to a subagent that must use
`/tdd`, inheriting `orchestrate-plan`'s delegation contract (complete encapsulation, acceptance
criteria, two-strikes escalation) and adding commit-per-phase in the user-prepared
worktree/branch. Structure's test checkpoints become the seams `/tdd` already asks for.

**D7 — Review economics move to QRSPI's pricing.** Deep review: `design.md`, `structure.md`, the
code at PR. Spot-check: the plan. The PRD is deleted outright — QRSPI has no requirements doc and
`design.md` carries the decisions; its user-stories format would feed nothing downstream. The
Decision Snapshot's pipeline role is subsumed by `design.md`: inside `/design` the grill writes
resolutions directly into design.md's "Resolved decisions" section (one artifact per phase);
`decisions-<feature>.md` remains only as standalone `grill-me`'s output.

**D8 — The Plan artifact: V1-comprehensive, sharded for progressive disclosure.** Adapt V1
`create_plan`'s template — including per-phase "changes required" with code sketches and the
automated/manual success-criteria split — rather than `to-plan`'s deliberately light phase docs,
whose downside (too little tactical detail reaching the implementing subagent) is known from use.
Layout: a plan index plus one **self-contained per-phase file**, so `/implement`'s subagents load
exactly one phase — progressive disclosure; recorded as a deviation from QRSPI's single ~8-page
`plan.md`. Cut from V1 as objectively bad practice: the horizontal "Common Patterns" recipes
(they prescribed the disease Structure exists to cure), org-specific machinery (thoughts sync,
Linear coupling), and the surrounding ~130-instruction process (only the template and
success-criteria machinery survive; process now lives across the pipeline). Code-in-plan is
reconciled with D6's TDD mandate explicitly: plan code blocks are *target sketches* — the
implementing subagent still writes the failing test first and implements toward the sketch, and
on plan/reality mismatch uses V1's STOP-and-report template rather than improvising.

**D9 — Conventions.** Claude-Code-first: the pipeline uses Claude Code mechanics (blind
subagents, `disable-model-invocation`) with graceful-degradation notes for other agents — the
firewall is the point. Artifacts live in a **directory per feature**:
`.planning/<feature>/{task,questions,research,design,structure}.md` + `plan/` (index + phases).
Names: `/research`, `/design`, `/structure`, `/implement` bare; `/write-plan`, `/open-pr`
renamed to dodge collisions.

## 4. Skill-by-skill disposition

| Skill | Disposition | Reason |
|---|---|---|
| `grilling` | **Keep** (minor edit) | Powers `/design`'s questioning gate; standalone grills unchanged. Stays model-invocable — 4 consumers justify the sub-skill cost. |
| `grill-me` | **Keep** | Zero-cost standalone wrapper. |
| `grill-with-docs` | **Keep** | Ditto; also the docs-aware grill inside `/design` when wanted. |
| `to-prd` | **Delete** | QRSPI has no requirements doc; `design.md` carries decisions (D7). |
| `to-plan` | **Absorb** | Vertical-slice / tracer-bullet rules move to `/structure`; index + self-contained phase-file layout survives inside the Plan artifact (D8). |
| `orchestrate-plan` | **Rework → `/implement`** | Keep delegation contract + escalation; add commit-per-phase and structure checkpoints. Assumes a user-prepared worktree/branch. |
| `tdd` | **Keep** (minor edit) | Implementation engine; update artifact references (plan/phase docs → QRSPI artifacts). |
| `codebase-designing` | **Keep** | Vocabulary for Design's "patterns to follow" and tdd's seams. |
| `domain-modelling` | **Keep** | Cross-cutting durable-docs writer; active inside `/design` when docs-aware. |
| `improve-codebase-design` | **Keep** (retarget handoff) | Entry point that generates tasks; closing handoff points at `/research`–`/design` instead of `to-plan`. |
| `initialise-docs` | **Keep** | Orthogonal setup skill. |
| `code-doc` | **Keep** | Orthogonal; used by tdd's green step. |
| `dg`, `acli`, `skill-creator` | **Keep** | Orthogonal utilities. |
| **New:** `/research`, `/design`, `/structure`, `/write-plan`, `/implement`, `/open-pr` | **Create** | The pipeline itself. `/implement` and `/structure` are reworks of `orchestrate-plan` / `to-plan` rather than green-field. |

Also affected: `README.md` (pipeline narrative), `docs/` (deviation records — this repo already
has the convention of documenting divergence from sources; QRSPI deviations D2–D6 land there).

## 5. Resolution log (agreed with Codey, 2026-07-07)

1. **`to-prd`: delete.** The "preserve because it exists" trap; nothing downstream consumes it.
2. **Plan detail: V1-comprehensive, including code sketches** — not 100% faithful where the
   source is objectively bad practice (cuts listed in D8). Rationale: `to-plan`'s light phase
   docs under-serve implementing subagents in practice; the unknown V2 prompt is approximated by
   "V1 template + QRSPI's demotion of audience".
3. **Plan layout: index + per-phase files**, objective = progressive disclosure.
4. **Grill output lands directly in `design.md`**; Decision Snapshot only for standalone grills.
5. **Naming: mixed** — bare `/research`, `/design`, `/structure`, `/implement`; renamed
   `/write-plan`, `/open-pr` (exact renames vetoable at sign-off).
6. **Claude-Code-first** with graceful-degradation notes.
7. **`.planning/<feature>/` directory per feature.**
8. **Worktree setup is the user's job** — `/implement` assumes the worktree/branch is already
   configured and does no git setup (structure review, 2026-07-07).
9. **No phase is mandatory** — skills degrade gracefully on missing upstream artifacts;
   `/implement`'s plan is the only hard prerequisite (plan review, 2026-07-07).
10. **Skill voice: no first person** — skills address the agent as "you" and call the human
    "the user", matching `tdd` and the `design-it-twice` reference (plan review, 2026-07-07).
