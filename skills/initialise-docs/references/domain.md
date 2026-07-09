# Domain docs

How skills and agents should consume this repo's domain documentation.

## Before exploring, read these

- **`LANGUAGE.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `LANGUAGE.md` per context. Read each one
  relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. In multi-context repos, also check
  `<module>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them
upfront. Producer skills (`/grill-with-docs`, or any skill maintaining the domain model) create them lazily when
terms or decisions actually get resolved.

## File structure

Single-context repo (most repos):

```
/
├── LANGUAGE.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← cross-cutting decisions
└── packages/
    ├── ordering/
    │   ├── LANGUAGE.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── LANGUAGE.md
        └── docs/adr/
```

Module paths follow whatever the repo uses (`packages/` `apps/` `services/` `src/` …).

## Use the glossary's vocabulary

When your output names a domain concept (in a PRD, a plan, a test name, a doc comment), use the term as defined in
`LANGUAGE.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project
doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
