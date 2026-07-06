---
name: domain-modelling
description: Actively build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. Not for merely consuming the existing glossary — only for changing the model.
user-invocable: false
---

# Domain Modelling

Actively build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and
write the glossary and decisions down the moment they crystallise.

## Orientation (before anything else)

Orient on the project's documented language first, so the lenses below have something to challenge against. If a
`CONTEXT-MAP.md` exists at the repo root, this is a multi-context repo: read it first — it indexes the bounded contexts
and where each module's `LANGUAGE.md` lives. Otherwise this is a single-context repo: read the root `LANGUAGE.md` if
present. If neither exists, proceed silently — don't flag their absence or suggest creating them.

## Reactive lenses (always on during the session)

These are not a separate terminology pass. They fire continuously throughout the session — the moment ambiguous,
conflicting, or overloaded language appears, decision-linked or not. Pure-terminology issues must always be caught.

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `LANGUAGE.md`, call it out immediately. "Your
glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean
the Customer or the User? Those are different things."

### Scenario-test the term

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe
edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code's actual naming and behaviour agree with the proposed
term. Exploration is bounded by the live session — never a proactive full-codebase audit. On a divergence, surface it
and ask which is canonical: "Your code cancels entire Orders, but you just said partial cancellation is possible —
which is right?" Never resolve a divergence by editing code yourself — this skill's durable writes are `LANGUAGE.md`,
ADRs, and `CONTEXT-MAP.md` Relationships. If the language is made canonical and the code is therefore stale, flag the
outstanding change (e.g. a rename) as an open item for the host workflow to act on or record.

## Capturing language inline

When a term resolves, write it to `LANGUAGE.md` right then — at peak attention, never batched at the end. Follow the
format in [references/language-format.md](references/language-format.md); consult it at the moment you write a term.

The file is **live and mutable throughout the session**. Because any session can invite backtracking, every backtrack is
just another inline edit at peak attention:

- **Write on resolve** — the moment a term settles, add its entry.
- **Update on revise** — if a later branch revises a term, re-edit its entry in place, then and there.
- **Remove on abandon** — if a term is dropped, delete its entry.

Create `LANGUAGE.md` lazily — on the first resolved term, not before. In a single-context repo that's the root
`LANGUAGE.md`. In a monorepo (a `CONTEXT-MAP.md` exists), each term goes to its **owning module's** `LANGUAGE.md`, never
a root glossary (see the format reference for the one-owner rule). Resolve the owner before writing: use the module that
was targeted, or infer it from what is being discussed and **confirm before writing**. If you can't tell which module
owns the term, **ask** — never write to a guessed module.

If the owning module has no `LANGUAGE.md` yet, creating it adds a new context to the index: append the matching entry to
`CONTEXT-MAP.md`'s **Contexts** section right then — name, link, one-line description.

If the session resolves how two contexts relate — an event one emits and another consumes, a shared type — append it to
`CONTEXT-MAP.md`'s **Relationships** section right then, under the same write/update/remove discipline.
Beyond that index append, the **Contexts** section is not yours to edit — never rename, merge, remove, or reorder
entries; the human declares boundaries (which is what their owner-confirmation did). Never create `CONTEXT-MAP.md` — if
it doesn't exist, this is a single-context repo and there is no cross-module link to record.

`LANGUAGE.md` is a glossary and nothing else. Keep it free of implementation details — it is not a spec, a scratch pad,
or a place for design decisions.

## Offering ADRs

Some decisions made during the session warrant an Architectural Decision Record. Unlike terms — which you write, then
announce — an ADR is high-stakes and permanent, so you **offer it first and write it only on the user's consent**.

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this
   way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If
there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected
  into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous
  HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library
  — just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID
  only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where
  a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was
  deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must
  be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle
  reasons, record it — otherwise someone will suggest GraphQL again in six months.

When all three hold, offer it ("This looks ADR-worthy — record it?"). On the user's consent, write the ADR following the
format and placement in [references/adr-format.md](references/adr-format.md) — consult it at the moment you write — then
announce the write. Create the target `docs/adr/` lazily, on the first ADR.

## Announcing writes

Never be silent about a durable write. Every mutation emits one ceremony-free line:

```
Added `Order` to LANGUAGE.md
Updated `Order` in LANGUAGE.md
Removed `Order` from LANGUAGE.md
Added ADR-0007
Updated ADR-0004
```

In a monorepo, every reference takes a context-name prefix (the name from `CONTEXT-MAP.md`): the term ack becomes *Added
`Order` to Ordering LANGUAGE.md*, and the ADR ack *Added Ordering ADR-0007* (module-scoped) or *Added root ADR-0003*
(cross-cutting). A relationship ack names the link itself: *Added Ordering → Billing relationship to CONTEXT-MAP.md*
(likewise *Updated…* / *Removed…*). The index append that comes with creating a module's `LANGUAGE.md` acks as *Added
Shipping to CONTEXT-MAP.md Contexts*. The single-context forms above stay bare — there's only one home.

Stay silent only when reading, or when context is absent. The ack is the user's chance to object to a write immediately.
