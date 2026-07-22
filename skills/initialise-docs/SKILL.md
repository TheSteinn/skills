---
name: initialise-docs
description: Bootstrap a repo's domain documentation — set up `docs/agents/domain.md` and the `CLAUDE.md`/`AGENTS.md` pointer, then scan the codebase and propose a draft `LANGUAGE.md` (per module in a monorepo). Setup only; refinement and new terms happen in `domain-modelling`.
disable-model-invocation: true
---

Bootstrap this repo's domain documentation: wire up the consumer pointer, then scan the codebase and propose a draft
glossary for my review. Breadth, not depth — get a reasonable starting `LANGUAGE.md` in place fast; relentless
sharpening is `domain-modelling`'s job. This is an initial-setup skill: act only where setup is missing, and never
refresh or re-scan content that already exists.

## 0. Dependency check

`domain-modelling` is a required install — it owns the format specs you write against. Before any scanning or writing:

1. Check the available-skills list for `domain-modelling`. Not listed → stop: "`initialise-docs` requires the
   `domain-modelling` skill (it owns the shared format specs) — install it first."
2. Resolve `domain-modelling/references/language-format.md` on disk: as a sibling of this skill's base directory first,
   then project `.claude/skills/`, then user `~/.claude/skills/`. Listed but unresolvable → stop and say the skill is
   installed but its references couldn't be located.

Never half-initialise: no work happens before this check passes.

## 1. Assess what's missing

Coverage, not content. Check the repo's state:

- `docs/agents/domain.md` — present?
- The `## Domain docs` pointer block — present in `CLAUDE.md`/`AGENTS.md`?
- Glossary — root `LANGUAGE.md` (single context), or `CONTEXT-MAP.md` with each listed module's `LANGUAGE.md`
  (monorepo)?

**Everything present → do nothing.** Reply with one line: "Already initialised — for refinement or new terms, run
`domain-modelling`." Don't offer a re-scan; hunting for missed language is not this skill's job.

**Anything missing → complete just that**, without asking me to re-confirm the parts already done — idempotency is the
point (wiring the pointer for a hand-created `LANGUAGE.md`, covering a module added since bootstrap).

In a monorepo, checking coverage already means resolving each Contexts entry's path — this is the coverage check
itself, not a validation pass. If an entry's path no longer exists, say so in one line — "the map lists
`packages/shipping` but that path doesn't exist — fix by hand or re-point it" — and leave the entry alone. Never modify
existing map entries, and never report "already initialised" from a map you can see is wrong.

## 2. Wire up the consumers

Create whichever of these is missing. Each seed file is the exact content — copy it verbatim:

- `docs/agents/domain.md` ← [references/domain.md](references/domain.md)
- the `## Domain docs` pointer block in `CLAUDE.md`/`AGENTS.md` ←
  [references/agent-pointer-block.md](references/agent-pointer-block.md)

Where the pointer block goes:

- Only one of the two files exists → that one.
- Both exist and one is a symlink of the other → edit the real target, never the link.
- Both exist as independent real files → ask me which owns the block; never silently pick.
- Neither exists → ask me which to create.

If a `## Domain docs` block already exists in the chosen file, update its contents in-place rather than appending a
duplicate. Don't overwrite user edits to the surrounding sections.

## 3. Confirm the context boundaries

If `CONTEXT-MAP.md` already exists, its entries are declared boundaries — never re-litigate them; detection applies
only to modules not yet covered.

Scan for physical multi-module signals: JS/TS (`workspaces` in `package.json`, `pnpm-workspace.yaml`, `lerna.json`,
`nx.json`, `turbo.json`, `rush.json`), JVM (`include`/`includeBuild` in `settings.gradle(.kts)`, `<modules>` in a
parent `pom.xml`), Rust (`[workspace]` in `Cargo.toml`), Go (`go.work`, multiple `go.mod`), Python (multiple
`pyproject.toml`/`setup.py`; Pants/Bazel `BUILD`/`WORKSPACE`), and generic conventions (multiple independent
manifests; `packages|apps|services|libs|modules` dirs).

- Signals fire → propose a context-per-module mapping and ask me to confirm, merge, or split. Never auto-declare —
  physical structure is a hint; only I know the real boundaries.
- No signals → propose the single-context default and ask me to confirm.

## 4. Draft the language

In a monorepo, ask which confirmed modules to draft glossaries for — "none" is a legitimate answer; not everyone wants
to backfill language. If I named a target in my invoking prompt, skip the question for it. Single context: the one
target is the repo root.

For each chosen target, spawn a dedicated Explore subagent — in parallel across targets. Each subagent gets the
target's path, the resolved path to `language-format.md` (instruct it to read the format first), and these extraction
rules:

- Candidates come from domain-model and entity types (classes, structs, DB tables, GraphQL/OpenAPI types), aggregate
  and bounded-context names, recurring domain nouns in identifiers, and any existing README/docs glossary.
- Exclude general programming concepts — timeouts, error types, utility patterns don't belong.
- Return full draft entries: canonical term, a 1–2 sentence definition inferred from how the code actually uses it,
  and `_Avoid_` synonyms spotted in the code.
- Fewer, high-signal candidates over exhaustive lists.
- In a monorepo, also report observed cross-module signals — imports of another module's types, events produced or
  consumed, shared schemas. Observations only: no ADR candidates, no design commentary.

Review with me module-by-module, sequentially — a light review, not a grill: I prune and accept, then you write that
target's `LANGUAGE.md` per the format spec. I can stop at any point; unreached modules stay uncovered and a later run
picks them up as missing setup.

## 5. Index the map (monorepo only)

`CONTEXT-MAP.md` lists a context iff its `LANGUAGE.md` exists — it indexes glossaries, never aspirations. Create the
map with the first module glossary you write; on each subsequent one, append its Contexts entry (name, link, one-line
description, per the format spec). Modules I chose not to cover stay out of the map.

Then propose draft Relationships entries from the subagents' cross-module observations — same review discipline:
fewer, high-signal entries; I confirm or prune before you write them.

## 6. Finish

End with one line: "For deeper refinement of any area, run `domain-modelling`."

Out of scope, always: ADRs (no candidate surfacing, no `docs/adr/` — that is `domain-modelling` territory), software
design patterns (human-owned in `AGENTS.md`/`CLAUDE.md`), and modifying existing glossary or map entries.
