# `/implement` — what changed from the source

Adapted from the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer, as written up in
[From RPI to QRSPI](https://alexlavaee.me/blog/from-rpi-to-qrspi/). `/implement` ports the Implement phase — executing
the approved plan against the codebase — but its nearest ancestor is this repo's own `orchestrate-plan`, which it
retires and whose orchestration bones it keeps. This records what was carried, where the port deviates from QRSPI, and
why.

## The orchestration bones come from `orchestrate-plan`

Four things carry over from the retired skill essentially intact:

- **The delegation contract.** The session is purely an orchestrator — it understands the task, tracks progress, and
  delegates "all phase implementation, and by extension code implementation, to dedicated and independent subagents",
  never writing code itself. Every subagent prompt starts with "/tdd", which `orchestrate-plan` already mandated.
- **Complete encapsulation.** `orchestrate-plan` required each subagent to have "a complete encapsulation of the work
  they need to complete, the scope, and necessary context". `/implement` keeps the requirement and makes it
  mechanical: the prompt is the full phase file plus the plan's durable decisions, nothing else — possible now because
  `/write-plan` produces self-contained phase files by construction. What was a judgment call about assembling context
  becomes a defect check: a phase file that isn't self-contained is a plan bug to STOP on and report, not a gap for
  the orchestrator to quietly fill.
- **Acceptance-criteria checking.** When a subagent reports done, the orchestrator checks the plan's criteria and
  ticks them off in the plan document itself; a failed criterion is delegated back, and a subagent that "contradicted
  or violated a durable architectural/design decision … has failed its task" regardless of otherwise green results.
  `/implement` sharpens the verb — run the automated commands yourself — but the loop is the same.
- **Two-strikes escalation.** "If a subagent fails twice for any one phase, cancel the orchestration and respond back
  to the human in the loop to course-correct." Carried whole: two failures on one phase still end the run and hand
  control back to the user.

## The Worktree phase is delegated to the user

QRSPI names Worktree as a phase of the workflow; we deliberately don't ship a skill for it, and `/implement` opens by
assuming the branch or worktree is already prepared. Two reasons. Worktree is the one QRSPI phase that is pure
mechanism — there is no artifact in it for a human to review, so nothing earns a pipeline invocation. And having the
human choose the isolation boundary keeps `/implement` free of git-setup side effects: a skill that branches, checks
out, or creates worktrees on its own initiative is exactly the kind of surprise state-change an orchestrator shouldn't
make on the user's behalf. So the skill makes no git-setup moves at all — where the work lands is the user's decision,
made before the skill is invoked.

## Commit-per-phase replaces checkbox-only progress

V1's `implement_plan` tracked progress by editing `- [x]` checkboxes in the plan file — its closest thing to durable
state. The words "git", "commit", "branch", and "worktree" appear nowhere in it, so a multi-phase run accumulated as
one uncommitted blob with no rollback boundary; `orchestrate-plan` inherited the gap, its state living in the todo
list and the plan's checkmarks. `/implement` keeps the checkbox editing (it is genuinely useful resume state) but
upgrades the recording medium: one atomic commit per completed phase, and never a commit for a phase whose criteria
haven't passed. Progress becomes real, revertible VCS history instead of prose checkmarks — which is also what lets
resumption trust completed work rather than re-verify it.

## TDD subagents retained where QRSPI punts on testing

QRSPI's Implement phase says little about how the code actually gets written or tested. This repo has a stance —
`tdd`'s red-green-refactor loop, the failing test first, plan sketches as targets rather than prescriptions — so
`/implement` keeps `orchestrate-plan`'s rule that every phase subagent runs `/tdd`, rather than inheriting QRSPI's
silence. The plan feeds the loop deliberately: each phase file carries a test checkpoint and split success criteria,
and `tdd` now names the phase document as a source of seams.

## The STOP-and-report mismatch template is V1's, revived

V1 `implement_plan`'s best part was its refusal to execute blindly: on a plan-reality mismatch the agent must "STOP
and think deeply about why the plan can't be followed" and emit a fixed report — Issue in Phase N / Expected / Found /
Why this matters / How should I proceed? `orchestrate-plan` had no equivalent, leaving mismatch handling to the
model's judgment. `/implement` inherits the template verbatim in spirit, extended one step for the orchestration
setting: the orchestrator neither improvises around a mismatch nor lets a subagent improvise around one.
