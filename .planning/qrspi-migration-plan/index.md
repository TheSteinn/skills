# Plan: QRSPI migration — index

> Source design: [../qrspi-migration-design.md](../qrspi-migration-design.md) (signed off)
> Source structure: [../qrspi-migration-structure.md](../qrspi-migration-structure.md) (signed off)
> Status: ready for implementation. Audience: the implementing agent. Humans spot-check.
> This plan deliberately uses the format it introduces (D8): index + self-contained phase files.

## Objective

Restructure this skills repo around the QRSPI workflow (Question → Research → Design →
Structure → Plan → Worktree → Implement → PR): six new user-invoked pipeline skills, three
skill deletions, minor edits to three keepers, per-slice README updates and `docs/` deviation
records. Deliverable is skill/document content only — no application code.

## Durable decisions (violating any of these fails the phase)

1. **Phase-per-skill, human as control flow.** Each pipeline skill is a separate invocation
   carrying `disable-model-invocation: true` (zero per-session context cost — verified). No
   dispatcher skill. Phase transitions happen because the human invokes the next skill.
2. **Instruction budget.** Every new SKILL.md stays **under 40 discrete instructions** (count
   imperatives, not template/example lines). Bulky templates and subagent prompts go in
   `references/` files loaded on demand.
3. **Research firewall.** Research and synthesis subagents never receive task content — their
   prompts are built from templates that have no task slot. The main window is the query
   planner; only questions travel downstream.
4. **State in artifacts.** Every phase reads only its permitted files from
   `.planning/<slug>/` and writes its artifact(s). Every skill's closing line recommends a
   fresh session (`/clear`) before the next phase. Artifacts are self-contained.
5. **Review economics.** Deep review: `design.md`, `structure.md`, the code at PR.
   Spot-check: the plan. State this framing in the skills where the human is addressed.
6. **TDD retained.** `/implement` delegates each phase to a subagent whose prompt starts with
   `/tdd`. Plan code sketches are targets, not prescriptions — failing test first, always.
7. **Worktree is the user's job.** `/implement` assumes the branch/worktree is already
   prepared and makes no git-setup moves (no branching, checkout, or worktree creation).
8. **Deviations are recorded, never silent.** Each phase lands a `docs/<skill>.md` deviation
   record (repo convention, cf. `docs/grill-me.md`) covering the deviations listed in its
   phase file.
9. **Keepers are untouchable except where a phase names an exact edit**: `grilling` (phase 2),
   `improve-codebase-design` (phase 4), `tdd` (phase 5). Nothing else in
   `codebase-designing`, `domain-modelling`, `initialise-docs`, `code-doc`, `acli`, `dg`,
   `skill-creator`, `grill-me`, `grill-with-docs`, or `install.sh` changes.
10. **No phase is mandatory.** Every pipeline skill consumes whatever upstream artifacts exist
    in `.planning/<slug>/` and sources missing context from the invocation, conversation, or
    the user — prompting, never hard-failing, on absence. The one hard prerequisite:
    `/implement` requires a plan (implementing without one is just `/tdd` on the target
    change). When `structure.md` is absent, `/write-plan` proposes its own vertical breakdown
    and gets the user's approval before writing any phase file.
11. **Skill voice: no first person.** Skills address the agent as "you" and refer to the human
    as "the user" — never "I", "me", "we", or "my invocation" — matching the voice of `tdd`
    and the `design-it-twice` reference. This applies to SKILL.md bodies, reference files, and
    templates alike.

## Conventions binding every phase

- **Artifact contract** (established phase 1, consumed by all later skills):
  `.planning/<slug>/task.md`, `questions.md`, `research.md`, `design.md`, `structure.md`,
  `plan/index.md`, `plan/phase-N-<slug>.md`.
- **Frontmatter**: every new skill has `name`, `description`, `disable-model-invocation: true`.
  Descriptions begin "QRSPI step N — …" so the `/` menu reads as a pipeline.
- **SKILL.md sketches are floors, not finished files.** Each sketch fixes the skill's
  structure, gates, decisions, and voice — do not change what it says, drop a gate, or add
  one. But do NOT ship a sketch verbatim either: the phase is only done when the sketch has
  been fleshed out into a polished skill in this repo's register — consistent formatting and
  cross-linking, fully-authored `references/` files where the phase specifies them (the plan
  gives their required content, not their final prose), and complete deviation-record and
  README prose written from the phase's bullet requirements. Recount the instruction budget
  (< 40) after fleshing out; if polish pushed it over, cut polish, not gates.
- **README per slice**: each phase adds/updates its own README entry so the repo is coherent
  after every phase; phase 6 does the full narrative rewrite.
- **Deletions ride with replacements**: `to-prd` dies in phase 2, `to-plan` in phase 4,
  `orchestrate-plan` in phase 5 — each in the phase that completes its replacement.

## Verification

Each phase file carries an **Automated verification** list (commands to run) and a **Manual
verification** list. The manual list dogfoods the pipeline on one standard micro-task, carried
across phases so each new skill runs on the previous skill's genuine output:

> **Standard micro-task**: “Add a `--dry-run` flag to `install.sh` that prints what would be
> installed without copying anything.”

Phase 1 researches it, phase 2 designs it, phase 3 structures it, phase 4 plans it, phase 5
implements it (on a scratch branch), phase 6 drafts (not necessarily opens) its PR. The
micro-task's `.planning/install-dry-run/` artifacts are working files; whether they are kept or
cleaned up afterwards is the human's call at phase 6.

## Phase index

| Phase | Title | Creates | Deletes | Edits | Document |
|---|---|---|---|---|---|
| 1 | `/research` | `skills/research/` (+ refs), `docs/research.md` | — | README | [phase-1-research.md](phase-1-research.md) |
| 2 | `/design` | `skills/design/`, `docs/design.md` | `skills/to-prd/` | `grilling`, README | [phase-2-design.md](phase-2-design.md) |
| 3 | `/structure` | `skills/structure/`, `docs/structure.md` | — | README | [phase-3-structure.md](phase-3-structure.md) |
| 4 | `/write-plan` | `skills/write-plan/` (+ refs), `docs/write-plan.md` | `skills/to-plan/` | `improve-codebase-design`, README | [phase-4-write-plan.md](phase-4-write-plan.md) |
| 5 | `/implement` | `skills/implement/`, `docs/implement.md` | `skills/orchestrate-plan/` | `tdd`, README | [phase-5-implement.md](phase-5-implement.md) |
| 6 | `/open-pr` + coherence | `skills/open-pr/`, `docs/open-pr.md` | — | README (full rewrite) | [phase-6-open-pr.md](phase-6-open-pr.md) |

Phases land in order; each leaves the repo releasable.

## What we're NOT doing

- No eval-harness work (`skill-creator` evals may follow later, out of scope).
- No changes to `install.sh` (directory copy picks up new skills automatically).
- No worktree/branch automation anywhere (decision 7).
- No changes to keeper skills beyond the three named edits (decision 9).
- No `.claude/` project config, hooks, or settings changes.
- No CI, no packaging, no version stamping.

## References

- QRSPI synthesis: `.planning/qrspi-understanding.md`
- V1 archaeology (template ancestry, STOP template, success-criteria split):
  `.planning/humanlayer-create_plan.md`, `humanlayer-research_codebase.md`,
  `humanlayer-implement_plan.md`, `humanlayer-iterate_plan.md`, `humanlayer-validate_plan.md`
- Raw V1 plan template (adapted in phase 4):
  `/Users/codey.byrne/dev/personal/humanlayer/.claude/commands/create_plan.md` lines 182–277
