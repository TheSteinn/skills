# Skills adapted from Matt Pocock

Six skills in this repo are adapted from [Matt Pocock](https://github.com/mattpocock)'s
[skills repo](https://github.com/mattpocock/skills): `grilling`, `domain-modelling`, `codebase-designing`,
`improve-codebase-design`, `grill-with-docs`, and `tdd`. This record documents what survived from the originals, where
each one deviates, and why. It is a faithful adaptation — the intent is to re-home Pocock's skills into this repo's
ecosystem and pipeline, not to reinvent them, so the deviations below are deliberate and bounded.

## Common adaptations

The same mechanical changes were applied across the whole family; they are recorded once here rather than repeated per
skill:

- **Reference files moved and renamed.** Top-level `UPPER-CASE.md` reference files move into a `references/`
  subdirectory with lowercase kebab-case names (e.g. `ADR-FORMAT.md` → `references/adr-format.md`), with links
  repathed accordingly.
- **`CONTEXT.md` → `LANGUAGE.md`.** The glossary artifact is renamed throughout — `LANGUAGE.md` names the file after
  the ubiquitous-language concept and avoids confusion with the multi-context index `CONTEXT-MAP.md`, which keeps its
  name.
- **Naming normalised to British / gerund forms.** `domain-modeling` → `domain-modelling`, `codebase-design` →
  `codebase-designing`, `improve-codebase-architecture` → `improve-codebase-design`; `grilling` and `tdd` unchanged.
- **Voice and invocation.** Bodies use "you"/"the user" (no first person), and one skill referencing another uses
  explicit Skill-tool invocation wording rather than `/slash`-command prose, which gets skimmed.
- **One owner per shared concept.** `codebase-designing` owns the deep-module vocabulary; the other skills defer to it
  rather than re-listing terms, so a term has exactly one canonical definition.

## `grilling`

*Source: `skills/productivity/grilling/`.*

The interview core is kept essentially verbatim — it is the whole reason the skill exists: relentless,
one-question-at-a-time interviewing; a recommended answer with every question; the facts-vs-decisions split (look up
anything the environment can answer, put every decision to the user); and don't-act-until-confirmed.

What the adaptation adds:

- **A "Closing the grill" protocol.** The source ends when shared understanding is reached but says nothing about what
  the session leaves behind. The adaptation closes with a decision record in chat — one entry per topic (final
  resolution plus a one-line rationale, superseded positions collapsed so each topic appears exactly once), a contract
  included *only* if one was explicitly proposed and confirmed (never invented), references to durable docs rather than
  restating them, cross-topic dependencies, open questions, and explicit user confirmation of the record.
- **A subject-presentation guard** ("if the subject hasn't been presented yet, ask the user to present it first") and
  an **explicit dependency-resolution step**, both needed once grilling can be invoked programmatically by another
  skill with no conversational antecedent.
- **First-class, composable standalone status.** The source is model-invocable; the adaptation keeps that and is
  composed by `/design`, `/grill-with-docs`, and `/improve-codebase-design`. This skill replaces the old thin
  `grill-me` wrapper, which has been deleted.

## `domain-modelling`

*Source: `skills/engineering/domain-modeling/`.*

Reused near-verbatim: the four reactive lenses (with their example phrasings), the three ADR criteria and the
"what qualifies" list, the `LANGUAGE.md` format rules, and the ADR template.

What the adaptation adds or changes:

- **Orientation before writing** — read `CONTEXT-MAP.md` (or the root glossary) first, and if neither exists proceed
  silently rather than flagging their absence.
- **Reactive lenses framed as always-on** — they fire continuously the moment ambiguous or conflicting language
  appears, decision-linked or not, so pure-terminology issues are always caught.
- **A write/update/remove discipline** — the durable files are live and mutable all session (write on resolve, update
  on revise, remove on abandon), so backtracking is handled at peak attention rather than re-synthesised from a
  transcript at the end.
- **Announcing writes** — every durable mutation emits one ceremony-free ack line (`Added \`Order\` to LANGUAGE.md`),
  giving the user the chance to object immediately.
- **Monorepo one-owner governance** — every term lives in exactly one module's glossary, the human owns context
  boundaries, and the skill asks rather than writing to a guessed module.
- **Bounded, read-only code cross-referencing** — exploration is scoped to the live session (never a proactive
  full-repo audit), and a code/language divergence is recorded as an open item rather than resolved by editing code.
- **ADR placement by blast radius** — module-scoped ADRs go under the module, cross-cutting ones at the root. The
  decision *criteria* were moved up into the SKILL body; the reference file is now format and placement only.

## `codebase-designing`

*Source: `skills/engineering/codebase-design/`.*

Reused, largely verbatim: the glossary (Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality),
the deep-vs-shallow treatment with its diagrams, principles 1–4, the rejected framings, and the `deepening.md` and
`design-it-twice.md` references.

What the adaptation adds or changes:

- **A complexity foundation.** A new `references/complexity.md` captures Ousterhout's treatment (definition, the three
  symptoms, the two causes, the zero-tolerance stance), and Complexity is promoted to a glossary term and a fifth
  principle — judge every design idea by whether it reduces complexity. This deepens the skill into the theory its
  vocabulary rests on.
- **Language-neutral examples.** The source's concrete TypeScript in the testability examples is rewritten as
  pseudocode so the vocabulary stays language-agnostic.

## `improve-codebase-design`

*Source: `skills/engineering/improve-codebase-architecture/`.*

Reused: the three-phase spine (explore → present as an HTML report → grill the chosen candidate), the HTML report
design system almost wholesale (self-contained file, diagram catalogue, candidate-card fields, recommendation badges),
the wins-named-in-glossary-terms discipline, and the "don't propose interfaces yet — ask which to explore" gate. The
compose-other-skills pattern is inherited from the source, not invented here.

What the adaptation adds or changes:

- **Fan-out exploration.** The source used a single `Explore` agent plus a `git log` hot-spot heuristic. The adaptation
  forbids `Explore` agents (they locate code from excerpts, but judging module depth needs whole-interface reading) and
  instead fans out general-purpose subagents driven by a new portable `references/explore-prompt.md`, then aggregates
  and re-ranks their candidates itself.
- **Vocabulary externalised.** The inline preferred/banned term lists are removed; the report defers to the
  `codebase-designing` glossary as the single source of truth.
- **Composed, not inlined, grilling.** The grill step invokes `grilling` and `domain-modelling` together, with the
  durable writes delegated to `domain-modelling`.
- **Pipeline handoff.** The tail can persist the decision record to `.planning/decisions-<feature>.md` and suggest
  running `/research`, feeding the record into `/design` as already-resolved input.

## `grill-with-docs`

*Source: `skills/engineering/grill-with-docs/`.*

The composing architecture is **Pocock's own** — the source is already a two-line composer with
`disable-model-invocation: true`, not a monolith. That shape is preserved. The adaptation makes it real: where the
source's `/grilling` and `/domain-modeling` were referenced, this repo ships actual `grilling` and `domain-modelling`
skills, so "invoke the grilling and domain-modelling skills together" resolves. The body is rewritten to explicit
Skill-invocation wording. All substantive behaviour lives in the two composed skills — see their sections above.

## `tdd`

*Source: `skills/engineering/tdd/`.*

Reused: "what a good test is" (behaviour through public interfaces), the anti-patterns section, the `mocking.md` and
`tests.md` skeletons, and the red-before-green / one-slice-at-a-time loop rules.

What the adaptation adds or changes:

- **Refactor is back in the loop.** The single biggest deviation: the source explicitly excludes refactoring from the
  cycle ("it belongs to the review stage, not the red → green loop"). The adaptation restores the classic
  red → green → refactor loop with a dedicated Refactor section, fenced against design creep — tidying only; anything
  that would touch a test or add a new seam means design is leaking in, so stop and take it back to the design stage.
- **Language-neutral examples.** The TypeScript/Jest concreteness in `mocking.md` and `tests.md` is rewritten as
  pseudocode.
- **Seams delegated.** Rather than defining a seam inline, the skill uses `codebase-designing`'s glossary definition,
  and treats seams as a pre-existing design decision the loop starts from.
- **Pipeline and ecosystem integration** — delegated-run guidance for when no user is reachable, behaviour
  prioritisation taken from the plan, "if a test is hard to write the design is wrong, not the test", applying
  `/code-doc` to changed interfaces before moving on, and a never-refactor-while-red rule.
