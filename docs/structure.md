# `/structure` — what changed from the source

Inspired by the **QRSPI** workflow by [Dex Horthy](https://github.com/dexhorthy) / HumanLayer. `/structure` handles the
Structure phase — "how do we get there?", the second human alignment gate, sitting between the design and the plan. This
documents what survived intact and where this skill deviates, and why.

## What carried over

The phase's altitude and economics are kept whole. Structure is ~2 pages at the **C header file** altitude: if the
plan is the implementation, this document is the `.h` file — new types and signatures, order and checkpoints, just
enough to see what the agent intends and correct it, never implementation bodies. The QRSPI slice specifics survive
too — roughly 200–400 lines per slice, each carrying a test checkpoint — as does the review pricing: `structure.md`
gets a deep read because it is the cheapest point to fix slicing and test order, while the plan that follows is only
spot-checked.

## The slice rules are inherited from this repo's previous `to-plan`

QRSPI's Structure phase exists because of its author's bluntest finding: no amount of prompting or evaluation could
stop models writing horizontal plans — all database, then all services, then all UI — so a dedicated human-reviewed
artifact enforces vertical slicing instead. This repo had already arrived at the same cure independently: `to-plan`'s
tracer-bullet rules require each slice to cut a narrow but complete end-to-end path through the relevant layers, be
demoable or verifiable on its own, and favour many thin slices over few thick ones. Convergent evolution, so
`/structure` inherits the local rules rather than re-deriving them from the blog, and layers on the QRSPI specifics
they lacked: the 200–400-line size heuristic, the per-slice test checkpoint, and naming slices for observable
behaviour rather than for a layer or component.

## The no-open-questions STOP moves upstream

Open questions can't be allowed to survive into structure: every slice cut around an unresolved question gets re-cut
once the answer lands, so slicing before the design settles just throws that work away. `/structure` stops on this
directly — if `design.md` still carries unresolved open questions, it sends the user back to `/design` rather than
slicing around the gap. In this pipeline the gate is a backstop rather than the primary defence (`/design` refuses to
finish with open questions), but designs get edited after the fact, sessions get interrupted, and no phase is
mandatory — the gate catches what the happy path assumes away.

## The quiz-the-user loop carries over from `to-plan`

Reviewing the slicing and checkpoints is the human's job at this gate, but the interaction that gets there needed
defining. `to-plan` already had one: its step 5 presents the proposed breakdown as a numbered list (title, coverage,
depends-on), asks whether the granularity feels right and whether phases should merge or split, and iterates until the
user approves. `/structure` carries that loop over intact as its step 3, swapping the per-slice fields for what this
pipeline actually reviews: end-to-end behaviour and the test checkpoint replace user-story coverage, since the
pipeline has no user stories — the design's resolved decisions took that role. The loop runs *before* `structure.md`
is written, so the review lands on a proposal while changing it is still a conversation, not a file edit.
