# Structure: QRSPI migration

> Source design: [qrspi-migration-design.md](qrspi-migration-design.md). Status: **for review**.

## Shape of the migration

Six vertical slices, one per pipeline skill, in pipeline order. Each slice lands a complete,
independently usable skill **plus everything that keeps the repo coherent at that point**: the
README section for it, the `docs/` deviation record for its decisions, and the deletion of
whatever it supersedes. After any slice, the repo is releasable — new skills work standalone,
old skills keep working until their replacement lands.

**Ordering rationale:** pipeline order is also verification order — each slice is verified by
running it on the *previous slice's real output*, so the migration dogfoods itself end-to-end.
It also front-loads the riskiest novel mechanism (the research firewall) and the main alignment
gate (`/design`), where a design flaw would ripple furthest.

**Definition of verified (every slice):** the skill ran end-to-end on a real micro-task in this
repo; its artifact met the design's size/section contract; its instruction count is <40; and it
carries `disable-model-invocation: true` (except where noted).

---

## Slice 1 — `/research` (Question + Research)

**Lands:** `skills/research/` — reads the task from the user/ticket; writes
`.planning/<feature>/task.md` + `questions.md` (neutral decomposition, optional pause offered);
fans out **blind subagents** (locator / analyzer / pattern-finder axes) that receive only
question text; a blind synthesis subagent writes `research.md` (~300 lines, file:line citations,
provenance frontmatter, facts only). Establishes the `.planning/<feature>/` directory convention.

**Also:** `docs/research.md` deviation record (Q+R merge; firewall-via-subagents; synthesis kept
blind). README gains the new pipeline section with this first entry.

**Verify:** run on a real micro-task; `research.md` contains zero recommendations; the spawned
subagent prompts (inspected) contain no task text; citations resolve to real lines.

## Slice 2 — `/design`

**Lands:** `skills/design/` — reads `task.md` + `research.md`; brain-dump (current state,
desired end state, patterns to follow, resolved decisions, open questions); invokes `grilling`
questions-first (+ `domain-modelling` when the project keeps domain docs); writes resolutions
directly into `design.md` (~200 lines). Includes the medium-neutral supporting-artifact rule
(sketch/diagram links when prose can't carry a decision).

**Also:** minor `grilling` edit — when running inside `/design`, the closing decision record
lands in `design.md`, not a Snapshot (Snapshot stays for standalone grills). **Deletes
`to-prd`.** README + credits updated; `docs/design.md` deviation record (grill-as-gate,
Snapshot/PRD subsumed).

**Verify:** run on slice 1's output; grill fires before any design prose is finalized; doc is
~200 lines with all five sections; no Snapshot file created; repo-wide grep shows nothing still
requiring `to-prd`.

## Slice 3 — `/structure`

**Lands:** `skills/structure/` — fresh-window convention (reads only
`design.md` + `task.md` + `research.md` from disk); absorbs `to-plan`'s tracer-bullet /
vertical-slice rules; writes `structure.md` (~2 pages): ordered slices, each end-to-end and
demoable, each with an explicit test checkpoint; the "C header" altitude — signatures and new
types, no bodies.

**Also:** `docs/structure.md` deviation record (slice rules inherited from `to-plan`, which
stays alive until Slice 4). README update.

**Verify:** run on slice 2's output; every slice in `structure.md` is vertical (names observable
end-to-end behaviour, not a layer); checkpoints present; ≤2 pages.

## Slice 4 — `/write-plan`

**Lands:** `skills/write-plan/` — reads all prior artifacts; adapted V1 `create_plan` template
(per-phase changes with code *sketches*, automated/manual success criteria, "What We're NOT
Doing", references) sharded as `plan/index.md` + one **self-contained per-phase file**. Cuts
from V1 recorded: horizontal Common Patterns recipes, org machinery, the process monolith.
States the TDD reconciliation: sketches are targets; tests still come first.

**Also:** **deletes `to-plan`**; retargets `improve-codebase-design`'s closing handoff
(`to-plan`/`tdd` → the pipeline via `/design` or `/research`). README update; `docs/plan.md`
deviation record (sharding for progressive disclosure; code-sketches-vs-TDD).

**Verify:** plan generated from slice 3's structure; a subagent given only the index + one phase
file can restate its phase's task, criteria, and checkpoints without other files; phases mirror
`structure.md`'s slices 1:1; no layer-by-layer phase appears.

## Slice 5 — `/implement`

**Lands:** `skills/implement/` — rework of `orchestrate-plan`: assumes the user has already
prepared the worktree/branch and makes no git-setup moves of its own; per-phase delegation to
subagents that must use `/tdd`, each given exactly its phase file + index; **one commit per
completed phase** after acceptance criteria pass; V1's STOP-and-report template on plan/reality
mismatch; two-strikes escalation to the human retained.

**Also:** **deletes `orchestrate-plan`**; minor `tdd` edit (seams/priorities sourced from the
new phase-file format). README update; `docs/implement.md` deviation record (Worktree phase
delegated to the user; TDD retained where QRSPI punts).

**Verify:** run against a small real plan on a user-prepared branch; `git log` shows one commit
per phase; criteria checked off in the phase files; mismatch template exercised at least once
(can be forced with a deliberately stale plan line).

## Slice 6 — `/open-pr` + coherence pass

**Lands:** `skills/open-pr/` — reads `design.md` + the diff; writes a PR description grounded in
the design (the "why" beside the diff); forge-agnostic (gh / bkt / manual); ends by telling the
human the one non-negotiable: read the code.

**Also:** README full pipeline narrative rewrite (grill→PRD→plan story replaced by the
six-phase story; standalone entries listed separately); `docs/` deviation records indexed;
final sweep — repo-wide grep proves no skill or doc references `to-prd`, `to-plan`, or
`orchestrate-plan`; fresh `install.sh` run smoke-tested.

**Verify:** PR description cites specific design decisions and links `design.md`; the sweep
greps return empty; a fresh install exposes exactly the intended skill set.

---

## Out of scope

No changes to `acli`, `dg`, `skill-creator`, `code-doc`, `initialise-docs`, or the internals of
`codebase-designing` / `domain-modelling`. No eval-harness work (`skill-creator` evals can
follow later). `install.sh` unchanged — directory copy picks up new skills automatically.
`grill-me` / `grill-with-docs` untouched beyond the Slice 2 `grilling` edit.
