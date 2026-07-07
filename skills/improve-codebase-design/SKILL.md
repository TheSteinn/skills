---
name: improve-codebase-design
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick — recording terms and decisions (LANGUAGE.md, ADRs) as they crystallise.
disable-model-invocation: true
---

# Improve Codebase Design

Surface design friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones.
The aim is testability and AI-navigability.

Invoke the `codebase-designing` skill first — it owns the design vocabulary and principles that every suggestion,
subagent prompt, and report in this skill must use. Use its terms exactly; avoid its banned substitutes.

## Process

### 1. Orient, then explore

Orient before exploring: read the project's domain glossary (`LANGUAGE.md`) and the ADRs for the areas you'll walk,
wherever the project keeps them. The domain language gives names to good seams; ADRs record decisions this skill
should not re-litigate. If the project documents neither, proceed silently.

Then delegate the walk to general-purpose subagents — one for a small codebase, fanned out by area for a large one.
Don't use `Explore` agents: they locate code from excerpts, and judging depth means reading whole interfaces against
whole implementations. Subagents start with fresh context — no loaded skills, no conversation — so everything the walk
depends on must travel in the prompt. Build each prompt from
[references/explore-prompt.md](references/explore-prompt.md).

Aggregate the candidates across subagents, dedupe, and re-rank them yourself — subagent confidence is input, not
verdict.

### 2. Present candidates as an HTML report

Write a single HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`,
falling back to `/tmp`, and write to `<tmpdir>/design-review-<timestamp>.html` so each run gets a fresh file. Open it
for the user — `open <path>` on macOS, `xdg-open <path>` on Linux — and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a
graph/flow/sequence reliably communicates the structure — it needs network access to render. Mix Mermaid with
hand-crafted CSS/SVG visuals — Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences),
hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each
candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files** — which files/modules are involved
- **Problem** — why the current design is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge
- **Dependency category** — the subagent's classification, one of the four categories from `codebase-designing`'s
  deepening reference

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use LANGUAGE.md vocabulary for the domain, and the `codebase-designing` vocabulary for the design.** If `LANGUAGE.md`
defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to
warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007 — but worth
reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [references/html-report.md](references/html-report.md) for the full HTML scaffold, diagram patterns, and styling
guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grill the chosen candidate

Invoke the `grilling` and `domain-modelling` skills together and walk the design tree of the chosen candidate —
constraints, dependencies, the shape of the deepened module, what sits behind the seam, which tests survive.
`domain-modelling` owns the durable writes as decisions crystallise (glossary terms, ADRs); note that a candidate the
user rejects for a load-bearing reason is its "rejected alternatives" case — recording it stops future runs of this
skill re-suggesting the same thing.

To explore alternative interfaces for the deepened module, use `codebase-designing`'s design-it-twice pattern
(parallel sub-agent designs compared on depth, locality, and seam placement).

When the grill closes, `grilling` presents its decision record and can persist it to `.planning/decisions-<feature>.md`
— from there, the QRSPI pipeline takes over: run `/research` with the chosen deepening as the task, and bring the
persisted decision record into `/design` as already-resolved input.
