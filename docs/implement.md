# `/implement` — what changed from the source

Inspired by the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer. `/implement` handles the
Implement phase — executing the approved plan against the codebase — but its nearest ancestor is this repo's own
`orchestrate-plan`, which it retires and whose orchestration bones it keeps. This records what was carried, where
this skill deviates from QRSPI, and why.

## The orchestration bones come from `orchestrate-plan`

Four things carry over from the retired skill essentially intact:

- **The delegation contract.** The session is purely an orchestrator — it understands the task, tracks progress, and
  delegates "all phase implementation, and by extension code implementation, to dedicated and independent subagents",
  never writing code itself. Every subagent prompt starts with "/tdd", which `orchestrate-plan` already mandated.
- **Complete encapsulation.** `orchestrate-plan` required each subagent to have "a complete encapsulation of the work
  they need to complete, the scope, and necessary context". `/implement` keeps the requirement and makes it
  mechanical: a fixed prompt template that hands the subagent two paths — `plan/index.md` and its one phase file —
  with an instruction to read both fully, plus a `<critical>` element pinning it to its own phase. Paths instead of
  pasted text give the subagent persisted memory: when its context degrades mid-phase, the files are still on disk to
  re-read. The durable decisions travel inside the index it reads — possible because `/write-plan` builds plans to
  exactly this contract: an agent given only the index and one phase file can implement the phase. What was a
  judgment call about assembling context becomes a defect check, with sequencing carved out: building on earlier
  phases' committed work is normal order-of-operations, but a phase file whose *text* can't be understood from the
  index and itself is a plan bug to STOP on and report, not a gap for the orchestrator to quietly fill.
- **Acceptance-criteria checking.** When a subagent reports done, the orchestrator checks the plan's criteria and
  ticks them off in the plan document itself; a failed criterion is delegated back, and a subagent that "contradicted
  or violated a durable architectural/design decision … has failed its task" regardless of otherwise green results.
  `/implement` sharpens the verb and doubles the run — the subagent executes its phase's automated criteria before
  reporting, and the orchestrator re-runs them itself, trust but verify — but the loop is the same.
- **Two-strikes escalation.** "If a subagent fails twice for any one phase, cancel the orchestration and respond back
  to the human in the loop to course-correct." Carried whole: two failures on one phase still end the run and hand
  control back to the user.

## The Worktree phase is delegated to the user

QRSPI names Worktree as a phase of the workflow; we deliberately don't ship a skill for it, and `/implement` opens by
assuming the branch or worktree is already prepared. Two reasons:

1. Worktree is the one QRSPI phase that is pure mechanism — there is no artifact in it for a human to review, so nothing
   earns a pipeline invocation
2. Having the human choose the isolation boundary keeps `/implement` free of git-setup side effects: a skill that
   branches, checks out, or creates worktrees on its own initiative is exactly the kind of surprise state-change an
   orchestrator shouldn't make on the user's behalf.

So the skill makes no git-setup moves at all — where the work lands is the user's decision, made before the skill is
invoked.

## Commit-per-phase replaces checkbox-only progress

`orchestrate-plan` tracked progress by editing `- [x]` checkboxes in the plan file, with its state otherwise living in
the todo list — no commit, branch, or worktree boundary marked a phase as done, so a multi-phase run accumulated as
one uncommitted blob with no rollback boundary. `/implement` keeps the checkbox editing (it is genuinely useful resume
state) but upgrades the recording medium: one atomic commit per completed phase, and never a commit for a phase whose
criteria haven't passed. Progress becomes real, revertible VCS history instead of prose checkmarks — which is also
what lets resumption trust completed work rather than re-verify it.

## TDD subagents retained

This repo has a stance — `tdd`'s red-green-refactor loop, the failing test first, plan sketches as targets rather than
prescriptions — so `/implement` keeps `orchestrate-plan`'s rule that every phase subagent runs `/tdd`. The plan feeds
the loop deliberately: each phase file carries a test checkpoint and split success criteria, and `tdd` now names the
phase document as a source of seams.

## The mismatch protocol is split across the two roles

Neither extreme works for a mismatch between plan and codebase: executing blindly papers over real problems, and
stalling on every trivial deviation makes the orchestration useless. `/implement` refuses to be robotic in either
direction, and gives that judgment to the role it fits. The subagent inherits it first: minor mismatches — a moved
file, a renamed symbol, a sketch that doesn't compile as written — are adapted around with judgment and reported,
never silently absorbed and never stopped on; anything that would change a seam or the design is beyond adaptation,
so the subagent stops and reports instead of implementing it. The orchestrator widens that binary into a three-way
triage of every reported mismatch: **hard stop** — the plan is irreconcilable with the codebase, so the
orchestration ends, reporting the issue, what was expected, what was found, why it matters, and how to proceed, and
the fix goes back up the pipeline; **soft stop** — the plan holds but the adaptation deserves a human look, so the
user confirms before the next phase starts; **silent proceed** — the adaptation is minor, neither seam nor design
change, so it is noted and named in the final summary's deviations.
