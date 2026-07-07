# `/grill-me` — what changed from the source

Adapted from [Matt Pocock](https://github.com/mattpocock)'s grilling skill. This documents what his original did well,
where we saw room for improvement, and what was added and why.

## What worked well

The interview core is kept essentially verbatim — it's the whole reason the skill exists:

- **Relentless, one-question-at-a-time interviewing.** No batching of unrelated questions; each answer lands before
  the next question is asked.
- **A recommended answer with every question.** The grill isn't an interrogation — the agent does the analysis and
  you accept, override, or push back.
- **Explore the codebase instead of asking.** Anything answerable from the code is answered from the code; your
  attention is spent only on questions the code can't settle.

## Areas identified for improvement

- **The session's output was ephemeral.** A long grill resolves dozens of decisions, but everything lived in the
  conversation. Once the context aged out or the session ended, the reasoning trail — including which alternatives
  were considered and why they lost — evaporated, and downstream documents had to be reconstructed from a compressed
  memory of the chat.
- **Long sessions revisit decisions.** Grills backtrack: a position adopted early is often superseded three branches
  later. Without an explicit reconciliation step, an end-of-session summary tends to blend early rejected positions
  with final ones.
- **Dependencies between decisions were implicit.** Two decisions that constrain each other would each get probed,
  but the constraint itself was never resolved as a first-class step.

## What we added and why

- **An explicit workflow spine** — understand the plan → probe each branch → resolve dependencies → confirm shared
  understanding. Dependency resolution is its own step with its own confirmation, so interlocking decisions are
  settled deliberately rather than incidentally.
- **The Decision Snapshot** (step 5). After confirmation, the session compiles a snapshot to
  `.planning/decisions-<feature>.md`: a *historical record of the brainstorm*, explicitly non-authoritative —
  downstream PRD/plan documents are the source of truth, and divergence during implementation is accepted and noted
  rather than treated as a violation. This is what fed `/to-prd` and `/to-plan` (both since retired) without
  re-deriving the session; today the QRSPI pipeline consumes the persisted record the same way.
  This implementation outputs what is essentially a handover document for the same or next agent, so that when moving
  onto PRD/Plan/implementation, the exact decisions are available in a persisted file, not floating within the context
  window.
- **The reconciliation preamble.** Before writing the snapshot, the agent must list every topic discussed, every
  position taken on it in chronological order (marked accepted / rejected / superseded), and the final resolution.
  This directly targets the long-context failure mode above: rejected alternatives can't quietly resurface in the
  record, because each topic appears exactly once with only its final resolution.
- **Snapshot rules that keep the record honest.** Contracts (schemas, interfaces) are included only when one was
  explicitly proposed *and* confirmed during the session — the snapshot never invents code shapes for decisions made
  in prose. Topics without a clear resolution go under Open Questions rather than being rounded up to decisions.
