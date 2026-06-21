# LANGUAGE.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A bill generated for an Order once its Fulfillment is confirmed.
_Avoid_: Bill, statement

**Customer**:
A person or organization that places Orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under
  `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types,
  utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept
  unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat
  list is fine.
- **Fold relationships into definitions — only where essential.** There is no standalone relationships section. Name
  another term inside a definition only when the term cannot be defined without it: the `Invoice` entry above names
  `Order` and `Fulfillment` because an Invoice is meaningless without them. Don't add relationships that aren't
  load-bearing.

## Single vs multi-context repos

**Single context (most repos):** one `LANGUAGE.md` at the repo root. Create it lazily — only when the first term
resolves.

**Multiple contexts (monorepo):** each bounded context owns its own `LANGUAGE.md` at its module root, indexed by a
`CONTEXT-MAP.md` at the repo root. **There is no root `LANGUAGE.md`.**

`CONTEXT-MAP.md` keeps two sections — **Contexts** (each pointing to that module's `LANGUAGE.md`) and **Relationships**
(the inter-context links: events or shared types flowing between modules):

```md
# Context Map

## Contexts

- [Ordering](./packages/ordering/LANGUAGE.md) — receives and tracks customer orders
- [Billing](./packages/billing/LANGUAGE.md) — generates invoices and processes payments

## Relationships

- **Ordering → Billing**: Ordering emits `OrderPlaced` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: shared types for `CustomerId` and `Money`
```

Module paths follow whatever the repo uses (`packages/` `apps/` `services/` `src/` …).

**One owner per term.** Every term is owned by exactly one module and lives only in that module's `LANGUAGE.md`. A term
used across modules is **not** duplicated or given a global home — append the cross-module link to `CONTEXT-MAP.md`'s
**Relationships** section instead, announced like any other write. Only the Relationships section is freely writable;
the Contexts section takes just the index append that comes with creating a module's `LANGUAGE.md`. (Intra-context
relationships still fold into definitions, as above; only inter-context ones live in `CONTEXT-MAP.md`.)
