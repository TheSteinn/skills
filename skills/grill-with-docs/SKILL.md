---
name: grill-with-docs
description: Grilling session that challenges your plan against the project's documented domain language, sharpens terminology, and updates the docs (`LANGUAGE.md`, ADRs) inline as decisions crystallise. Use when the user wants to stress-test a plan against their project's language and documented decisions.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch
of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended
answer. As we go, challenge the plan against the project's documented domain language and capture resolved terminology
into `LANGUAGE.md` inline — so the vocabulary is recorded at peak attention, not reconstructed in a pass at the end.

## Workflow

### 1. Understand the plan

If I haven't already, ask me to present my plan. Identify all major decision points and assumptions.

Orient on the project's documented language first, so the glossary lens has something to challenge against. If a
`CONTEXT-MAP.md` exists at the repo root, read it first — it indexes the bounded contexts and where each module's
`LANGUAGE.md` lives (this is a monorepo). Otherwise read the root `LANGUAGE.md` if present (single context). If neither
exists, proceed silently — don't flag their absence or suggest creating them.

### 2. Probe each branch

Drill down on each decision point.

If a question can be answered by exploring the codebase, explore the codebase instead of asking.

As you probe, the four reactive lenses (below) fire continuously — the moment the language gets fuzzy, conflicting, or
overloaded, whether or not it's tied to the decision in front of you. When a term resolves, capture it right then (see
[Capturing language inline](#capturing-language-inline)).

### 3. Resolve dependencies

When two decisions depend on each other, resolve the dependency explicitly. Confirm the resolution with me before moving
on.

### 4. Confirm shared understanding

Summarize the final state of the plan, listing all resolved decisions and remaining open questions. Get explicit
confirmation from me.

**Interaction Rules**

- Ask one question at a time – do not batch several unrelated questions into one message. Wait for feedback on each
  question before continuing.

### 5. Compile Decision Snapshot

After I confirm the shared understanding, compile a **Decision Snapshot** — the brainstorm record of the session — and
save it to `.planning/decisions-<feature>.md`, per
[references/decision-snapshot.md](references/decision-snapshot.md) (it references the durable docs, never restates them).

## Reactive lenses (always on)

These are not a separate terminology pass. They fire continuously throughout the workflow above — the moment ambiguous,
conflicting, or overloaded language appears, decision-linked or not. Pure-terminology issues with no decision branch
must still be caught.

### Challenge against the glossary

When I use a term that conflicts with the existing language in `LANGUAGE.md`, call it out immediately. "Your glossary
defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When I use vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the
Customer or the User? Those are different things."

### Scenario-test the term

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe
edge cases and force me to be precise about the boundaries between concepts.

### Cross-reference with code

Use the code two ways. As an **oracle** — anything answerable from the codebase, explore rather than ask (step 2). As a
**language check** — when I state how something works, check whether the code's actual naming and behaviour agree with
the proposed term.

Exploration here is bounded by the live grill — never a proactive full-codebase audit. On a divergence, surface it and
ask which is canonical: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is
right?" Never edit code — your durable writes are `LANGUAGE.md`, ADRs, and `CONTEXT-MAP.md` Relationships, never source
files. If I make the *language* canonical and the *code* is therefore stale, take no code action — record the divergence
in the Decision Snapshot (step 5) as a finding flagging the outstanding code rename.

## Capturing language inline

When a term resolves, write it to `LANGUAGE.md` right then — at peak attention, never batched at the end. Follow the
format in [references/language-format.md](references/language-format.md); consult it at the moment you write a term.

The file is **live and mutable throughout the session**. Because the decision-tree walk invites backtracking, every
backtrack is just another inline edit at peak attention:

- **Write on resolve** — the moment a term settles, add its entry.
- **Update on revise** — if a later branch revises a term, re-edit its entry in place, then and there.
- **Remove on abandon** — if a term is dropped, delete its entry.

Create `LANGUAGE.md` lazily — on the first resolved term, not before. In a single-context repo that's the root
`LANGUAGE.md`. In a monorepo (a `CONTEXT-MAP.md` exists), each term goes to its **owning module's** `LANGUAGE.md`, never
a root glossary (see the format reference for the one-owner rule). Resolve the owner before writing: use the module I
targeted ("grill me on the ordering domain"), or infer it from what we're discussing and **confirm before writing**. If
you can't tell which module owns the term, **ask** — never write to a guessed module.
If the owning module has no `LANGUAGE.md` yet, creating it adds a new context to the index: append the matching entry to 
`CONTEXT-MAP.md`'s **Contexts** section right then — name, link, one-line description.

If the grill resolves how two contexts relate — an event one emits and another consumes, a shared type — append it to
`CONTEXT-MAP.md`'s **Relationships** section right then, under the same write/update/remove discipline.
Beyond that index append, the **Contexts** section is not yours to edit — never rename, merge, remove, or reorder entries; 
the human declares boundaries (which is what their owner-confirmation did). Never create `CONTEXT-MAP.md` — if it doesn't 
exist, this is a single-context repo and there is no cross-module link to record.

`LANGUAGE.md` is a glossary and nothing else. Keep it free of implementation details — it is not a spec, a scratch pad,
or a place for design decisions.

## Offering ADRs

Some decisions made during the grill warrant an Architectural Decision Record. Unlike terms — which you write, then
announce — an ADR is high-stakes and permanent, so you **offer it first and write it only on my consent**.

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

When all three hold, offer it ("This looks ADR-worthy — record it?"). On my consent, write the ADR following the format
and placement in [references/adr-format.md](references/adr-format.md) — consult it at the moment you write — then
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

Stay silent only when reading, or when context is absent. The ack is my chance to object to a write immediately.
