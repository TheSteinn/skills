# `/design` — what changed from the source

Inspired by the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer. `/design` handles the
Design phase — the pipeline's main human alignment gate. This documents what survived intact and where this skill
deviates, and why.

## What carried over

The artifact and its economics are kept whole: a ~200-line `design.md` with QRSPI's five sections — current state,
desired end state, patterns to follow, resolved decisions, open questions — written before any code exists and
deep-reviewed by the human, because 200 lines of design is the cheapest artifact that can catch a wrong approach. So
is the phase's distinctive permission: Design is the first context window allowed to hold both the task and the
research facts, since forming an opinion is now its job and that opinion goes straight to human review. And the
design/plan split survives untouched — no phase breakdown, no code beyond interface sketches; slicing belongs to
`/structure`.

## The grill replaces "open questions first"

QRSPI mandates that the design lead with its open questions — but it asks them once, as a list for the human to react
to. This repo already had a stronger questioning engine, so `/design` composes it: the `grilling` skill walks the
decision tree one branch at a time, recommends an answer with every question, resolves dependencies between decisions
explicitly, and doesn't stop until every branch is resolved or deliberately parked. This is an *improvement*
deviation, not a fidelity one: where QRSPI surfaces the unknowns, the grill retires them — the document the human
deep-reviews holds decisions with rationales, not a pile of open threads.

## Resolutions land in `design.md`, not a Decision Snapshot

This repo's standalone grills used to close by persisting a Decision Snapshot to `.planning/decisions-<feature>.md`.
Inside`/design` that would mean two decision-carrying artifacts for one phase, and every downstream phase reconciling
them. The pipeline keeps one artifact per phase: as each branch resolves, the grill writes it straight into
`design.md`'s Resolved decisions section, and no Snapshot file is created.

## `to-prd` is deleted

The original `to-prd` stated it created a PRD, but it was more of a high-level spec. That file's decision-carrying role
is subsumed by `design.md`, and its user-stories format would feed nothing — no downstream phase consumes user stories;
structure and plan build from the design's resolved decisions. Keeping the skill anyway would have been the "preserve
because it exists" trap, so it is deleted outright rather than left as an orphaned side path.

## Supporting artifacts are medium-neutral

Some decisions can't be judged in prose — a UI layout, a schema shape. `/design` handles these with one deliberately
medium-neutral rule: when prose can't carry a decision, link the cheapest reviewable sketch (an HTML mock, a diagram
file) from the relevant section instead of describing it badly. We chose a general rule over a frontend/backend
callout ("for UI work, produce an HTML mock") on purpose — it is review economics applied to medium: whatever the
domain, the reviewer gets the decision in the form they can actually evaluate.
