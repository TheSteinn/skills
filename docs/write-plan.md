# `/write-plan` — what changed from the source

Inspired by the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer. `/write-plan` handles the
Plan phase — the tactical expansion of the approved structure into the document the implementing agent executes. This
records what survived intact and where this skill deviates, and why.

## The plan's re-pricing carries over unchanged

In RPI, the plan was the human review artifact: the place where approach, phasing, and detail all got judged at
once, at the moment the document was biggest and the reviewer's attention thinnest. QRSPI's central move was to re-price
that review — alignment happens upstream at the cheap artifacts (`design.md`, `structure.md`, each deep-reviewed), and
the plan is demoted to a tactical document written *for the agent*, which the human only spot-checks. We carry that
re-pricing over whole: `/write-plan` opens by telling the agent its job is completeness, not persuasion, and closes by
asking the user for a spot-check, not a review.

## Sharded: an index plus self-contained phase files

QRSPI writes the plan as a single document of roughly eight pages. We shard it instead: `plan/index.md` holds
everything shared — durable decisions, current and desired state, testing strategy — and each phase gets its own
self-contained file. The reason is progressive disclosure for `/implement`, which delegates each phase to a subagent:
a subagent loads exactly the index and its one phase file, never the other N−1 phases, so its context is spent on the
slice it is implementing. The cost is deliberate restatement — each phase file repeats the background its implementer
needs rather than pointing at research or design — and the template says so explicitly, because to a reviewer it looks
like duplication and to a subagent it is the whole point. The layout itself is the one structural inheritance from
this repo's retired `to-plan`, which had already arrived at index-plus-self-contained-phase-files for exactly this
delegation reason.

## The template survives, minus two cuts

The plan artifact's shape is adapted near-fully. The sections all carry over: overview, current state, desired end
state, key discoveries, what-we're-NOT-doing, implementation approach, testing strategy, per-phase changes with
sketches, and the automated/manual success-criteria split. Two things are cut, each as objectively bad practice rather
than taste:

- **The "Common Patterns" recipes.** A layer-per-phase build order — "schema → store → business logic → API → UI" —
  is precisely the pathology `/structure` exists to prevent. Phase order now comes from the approved vertical slices,
  never from a recipe.
- **The process monolith.** A ~130-instruction research-and-alignment pipeline wrapped around the template, with
  buried buy-in gates that were skipped about half the time. Those steps aren't slimmed here — they're gone, because
  they live as earlier QRSPI phases with their own invocations and their own review gates.

This record is where that reasoning lives — deliberately not in the template reference itself. The reference is
loaded into the implementing agent's context at runtime, and a skill doesn't need its own change history to do its
job; it needs its instructions. A future editor reaching for a "helpful" patterns section should find this record
before the temptation.

## Code sketches, reconciled with TDD

Embedding "specific code to add/modify" in every phase runs headlong into this repo's `tdd` skill, which forbids
writing implementation before a failing test. Both survive because the sketches are re-labelled rather than removed: they are
**targets, not prescriptions**, showing intended shape so the implementing agent starts oriented, while the failing test
still comes first and a sketch that disagrees with reality is reported, not silently patched around. Every phase file
carries that disclaimer verbatim above its first sketch, so the contract travels with the artifact instead of relying on
the implementing agent having read this skill.

## `to-plan` is retired

This skill completes the replacement of this repo's `to-plan`, so the skill is deleted rather than left as a parallel
path to a weaker plan. Its durable contributions had already found homes: the tracer-bullet slicing rules moved to
`/structure` (where the slicing is deep-reviewed with the user), and its index-plus-self-contained-phase-files layout
is absorbed here. The one part deliberately not carried forward is its detail-lightness — `to-plan` kept phases free
of file names, signatures, and implementation specifics on the grounds that details "may change as later phases are
built". That was the right call when the plan was written straight from a brainstorm; under QRSPI's pricing it is
backwards. The plan is now written after design and structure have settled every decision, and is consumed by
subagents that see nothing else — so the plan is exactly where the detail belongs, and a detail-light phase file would
just push rediscovery work onto every implementer.
