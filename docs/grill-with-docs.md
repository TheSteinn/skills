# `/grill-with-docs` — what changed from the source

Adapted from [Matt Pocock](https://github.com/mattpocock)'s `grill-with-docs`. This is deliberately *not* a clone:
it's Pocock's domain-language and ADR production layer rebuilt on top of my own [`/grill-me`](grill-me.md) workflow,
so the docs-producing grill inherits the decision-tree walk, dependency resolution, and Decision Snapshot that skill
added. This documents what survived from Pocock unchanged, where I saw room for improvement, and what was added.

## What worked well

Kept, mostly verbatim:

- **The interview core.** The same "interview me relentlessly" opening drives both skills.
- **The four session behaviours**, carried over as four "reactive lenses": challenge terms against the glossary,
  sharpen fuzzy language, stress-test terms with concrete scenarios, and cross-reference claims with the code.
- **Inline capture.** Pocock's "update the glossary right there — don't batch" is a key insight:
  re-synthesising a glossary from a long transcript at the end is exactly where models compress, drop, or merge
  terms. Writing at the moment of resolution captures peak fidelity.
- **The ADR system, wholesale.** File format verbatim, `docs/adr/` location, sequential numbering, and the
  three-criteria gate — only offer an ADR when the decision is hard to reverse *and* surprising without context
  *and* the result of a real trade-off.
- **Glossary purity.** "It is a glossary and nothing else" — no specs, no scratch pads, no implementation decisions.
- **Lazy file creation.** Nothing is scaffolded upfront; files appear when there's something to write.

## Areas identified for improvement

- **`CONTEXT.md` is an inviting bucket.** A file named "context" reads as "anything the agent should know" — the
  exact scope creep the glossary rule exists to prevent. Renamed to **`LANGUAGE.md`**: nobody dumps design patterns
  into a file with that name, and it's *more* DDD-coherent — each bounded context owns a ubiquitous language, and the
  context map relates contexts.
- **Middle-tier decisions had no home.** A grill resolves real choices that are neither glossary terms nor
  ADR-worthy ("paginate with cursors", "cart uses optimistic locking"). In the original they evaporated with the
  session. The adaptation keeps `/grill-me`'s Decision Snapshot alongside the durable docs, with a strict **content
  boundary**:
  the snapshot *references* terms and ADRs (`→ LANGUAGE.md`, `→ ADR-0004`), never restates them — every piece of
  content has exactly one canonical copy.
- **Writes were silent.** Inline mutation of durable files needs an audit trail. Every write now announces itself in
  one ceremony-free line (`Added \`Order\` to LANGUAGE.md`), giving you the chance to object immediately.
- **Backtracking needed first-class support.** A decision-tree walk invites revisiting earlier branches, so the
  durable files are live and mutable all session under a **write-on-resolve / update-on-revise / remove-on-abandon**
  discipline — a revised term is re-edited then and there, also at peak attention.
- **Consent was uniform; the stakes aren't.** Terms are cheap to correct, so they're written then announced — no
  per-term consent gate, which would drag the flow back toward batching. ADRs are permanent and high-stakes, so they
  are offered first and written only on consent (a sharpening of Pocock's implicit "offer").
- **Monorepo semantics were thin.** The adaptation adds the strict one-owner-per-term model (no root glossary; every
  term lives in exactly one module's `LANGUAGE.md`), `CONTEXT-MAP.md` as the index with an inter-context Relationships
  section, ADR placement by blast radius, and — when lazily creating a new module's glossary — appending its entry to
  the map's Contexts section, wiki-style, so the index never goes stale.
- **Code divergence handling.** The cross-reference lens never edits code: on a code/language mismatch it asks which
  is canonical, and if the language wins, the outstanding code rename is recorded as a finding in the snapshot
  rather than silently acted on.

## Structural notes

- **Verbs in `SKILL.md`, shapes in `references/`.** Always-on behaviour (the lenses, the write discipline, the ADR
  gate) lives in the skill body where it stays in attention; point-of-use artifact specs (`language-format.md`,
  `adr-format.md`, `decision-snapshot.md`) are consulted at the concrete moment they're needed.
- **Two grills, one boundary.** `/grill-with-docs` exists *separately* from `/grill-me` so that plain stress-test
  grills — proofs of concept, early high-level plans — can never mutate a project's canonical docs by accident. The
  glossary's relationships section was also cut relative to Pocock's earlier format: intra-context relationships fold
  into term definitions only where essential; only inter-context relationships live in `CONTEXT-MAP.md`.
