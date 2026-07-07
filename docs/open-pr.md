# `/open-pr` — what changed from the source

Adapted from the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer, as written up in
[From RPI to QRSPI](https://alexlavaee.me/blog/from-rpi-to-qrspi/). `/open-pr` ports the PR phase — the delivery step,
where the pipeline finally spends the human's deep attention on the code itself. Its nearest V1 ancestor is
`validate_plan` (chained into `describe_pr`): the command that had the model check whether the model had finished.
This records what survived, what was overruled, and why.

## The human replaces the self-grading `validate_plan`

V1's `validate_plan` ran after implementation and asked the model to verify its own work — explicitly so: "If you were
part of the implementation: review the conversation history… focus validation on work done in this session." The
verifier and the implementer shared the same blind spots, so a model that misunderstood a requirement would validate
its own misunderstanding as correct; the only safeguard was an exhortation to "be honest," which has no teeth against
a shared misconception. The command also never defined what outcome counted as validated — its report template shows
partially-implemented phases and failing lint as acceptable states, with no threshold and no blocking condition. And
it added review burden instead of reducing it: another model-written artifact (the Validation Report) layered on top
of an already-heavy plan, produced by the very agent whose work was in question.

QRSPI's answer is kept whole: a model cannot certify its own completion, so the human sits at the one gate that
matters — reading the code at PR. The verification instincts V1 got right are not discarded; they are relocated to
where they bind. Pass/fail checkpoints are defined per slice in `structure.md` *before* any code exists; the plan
splits automated from manual criteria per phase; `/implement` runs the automated half twice (subagent, then
orchestrator) before each phase commit. By the time `/open-pr` runs, "did the automated checks pass?" is settled
history recorded in the plan and the commits — the only question still open is the one only a human can close, and
the skill's closing line refuses to let it be skipped: now read the code, no exceptions.

## The description is grounded in `design.md`, so review is confirmation

The reviewer already deep-reviewed `design.md` and `structure.md` while they were short and cheap to change. The PR
description is written from those artifacts plus the actual diff so that review at the PR is *confirmation, not
discovery*: the Why section speaks in the design's own terms, referencing the sections they come from, and Decisions
exercised lists the resolved decisions the diff embodies — decisions the reviewer has already approved once. What
remains for the human is checking that the code is what those decisions look like when built, which is precisely the
review QRSPI reserves their attention for. V1 gestured at this artifact — its Validation Report, chained into
`/describe_pr`, is the PR description's direct ancestor — but had the model narrate its own report; the port keeps
the artifact and swaps the actor it serves.

The altitude is a deliberate decision, not a style preference. Description entries are behaviour-level — what the
system now does, which decisions the change exercises — never file-by-file minutiae. The diff already carries the low
level perfectly; restating it in prose doubles the reading without adding information, and buries the seams and
design choices a reviewer needs under noise they would skim anyway. A description that induces skimming defeats its
own purpose at the exact gate the pipeline exists to protect.

## Forge-agnostic, and nothing pushed without consent

Opening a PR is the pipeline's one outward-facing action — the first moment anything leaves the user's machine. So
consent is explicit: the title, description, and target branch are confirmed with the user before anything is pushed
or created, mirroring the reasoning that kept git setup out of `/implement` — outward or state-changing moves are the
user's call, made deliberately, never a side effect of invoking a skill.

The skill is deliberately forge-agnostic: it uses whatever forge CLI is available and already authenticated (`gh`,
`bkt`, …), because hardcoding a forge would couple the pipeline to one host for no benefit — the same trap as V1's
hardcoded `make` targets, which any repo without a Makefile fell through. And when no CLI is present, the skill
outputs the title and description for the user to paste, names the missing tool, and stops. It never installs one:
installing tooling is a surprise state change on the user's machine, made to save the user a paste that costs
seconds. Reporting the gap keeps the human in charge of what lands in their environment.
