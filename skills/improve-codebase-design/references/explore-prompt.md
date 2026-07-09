# Explore Subagent Prompt

Subagents start from fresh context — no loaded skills, no conversation history. Everything the walk depends on must
travel in the prompt: the template below makes the subagent load the design vocabulary itself and report in it. Fill
the placeholders from your orientation in step 1; one prompt per area.

---

Invoke the `codebase-designing` skill first and use its vocabulary and principles for everything you report — depth,
seams, leverage, locality, the deletion test. Also read its deepening reference (`references/deepening.md` inside that
skill) for the four dependency categories.

Domain language: read <LANGUAGE.md path(s) from orientation>. Use those names for domain concepts. ADRs at <docs/adr
path(s)> record settled decisions — note when a candidate would contradict one, citing the ADR number.

Walk <area/paths>. Explore organically — don't follow rigid heuristics. Your own navigation friction is the
instrument:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules shallow — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, while the real bugs hide in how they're called (no
  locality)?
- Where do tightly-coupled modules leak across their seams?
- Which parts are untested, or hard to test through their current interface?

Apply the deletion test to anything you suspect is shallow: would deleting it concentrate complexity, or just move it?
"Concentrates" is the signal you want.

Read whole interfaces against whole implementations before judging depth — never judge from excerpts.

Return a structured list of deepening candidates. For each:

- **Files/modules** involved
- **Friction observed** — in glossary terms, citing specific code
- **Dependency category** — one of the four from the deepening reference
- **ADR conflict** — if any, with the ADR number
- **Confidence** — strong / worth exploring / speculative
