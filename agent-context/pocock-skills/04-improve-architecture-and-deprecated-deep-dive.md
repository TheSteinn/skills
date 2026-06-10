# `/improve-codebase-architecture` & Departed Ubiquitous-Language — Deep Dive

## Table of Contents

1. [How `/improve-codebase-architecture` Reads CONTEXT.md and ADRs](#1-how-improve-codebase-architecture-reads-contextmd-and-adrs)
2. [How It Updates CONTEXT.md Inline and When It Offers ADRs](#2-how-it-updates-contextmd-inline-and-when-it-offers-adrs)
3. [The Complete LANGUAGE.md Vocabulary](#3-the-complete-languagemd-vocabulary)
4. [Cross-Referencing with `/grill-with-docs` Format Files](#4-cross-referencing-with-grill-with-docs-format-files)
5. [The Deprecated Ubiquitous-Language Skill — Complete Flow](#5-the-deprecated-ubiquitous-language-skill--complete-flow)
6. [Evolution from Ubiquitous-Language to CONTEXT.md — What Changed and Why](#6-evolution-from-ubiquitous-language-to-contextmd--what-changed-and-why)
7. [How `/grill-me` Differs from `/grill-with-docs`](#7-how-grill-me-differs-from-grill-with-docs)
8. [Appendices](#appendices)

---

## 1. How `/improve-codebase-architecture` Reads CONTEXT.md and ADRs

### 1.1 The Skill's Opening Instruction

The skill definition in `SKILL.md` begins by anchoring itself to domain documentation:

> "Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability."

And the glossary section states explicitly:

> "This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate."

This single sentence establishes the entire reading relationship: the skill **consumes** CONTEXT.md for vocabulary and **consumes** ADRs for constraints, but it does not re-litigate either.

### 1.2 Process Step 1: Explore — Reading the Domain Glossary and ADRs

The first process step is "Explore." Instructions verbatim:

> "Read the project's domain glossary and any ADRs in the area you're touching first."

This is **the very first instruction** before any codebase exploration. The skill mandates reading CONTEXT.md (the "domain glossary") and ADRs **before** the sub-agent exploration begins. The word "first" is load-bearing — it means the domain language must be loaded into context so that when the sub-agent walks the codebase, it already knows the names for things.

The sub-agent then uses `subagent_type=Explore` to walk the codebase organically, noting friction:

- Where understanding one concept requires bouncing between many small modules
- Where modules are **shallow** (interface nearly as complex as implementation)
- Where pure functions have been extracted for testability but the real bugs hide in how they're called (no **locality**)
- Where tightly-coupled modules leak across their seams
- Which parts are untested or hard to test through their current interface

### 1.3 How CONTEXT.md Vocabulary Constrains Naming

Step 2 of the process ("Present candidates") has an explicit instruction:

> "**Use CONTEXT.md vocabulary for the domain, and LANGUAGE.md vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service.""

This is a dual-vocabulary discipline:

| Vocabulary Source | Domain | What It Controls |
|---|---|---|
| `CONTEXT.md` | Domain language | Names for business concepts (Order, Customer, Invoice) |
| `LANGUAGE.md` | Architecture language | Names for structural concepts (Module, Interface, Seam, Adapter, Depth) |

The skill strictly forbids "service" (which conflates with the LANGUAGE.md term "module"), "component" (too vague), or "boundary" (overloaded with DDD's bounded context). It also forbids using code-level names like `FooBarHandler` when the domain has a term for the concept.

### 1.4 How ADRs Act as Constraints

The skill treats ADRs as **settled decisions**, not suggestions. From Step 2:

> "**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly (e.g. _'contradicts ADR-0007 — but worth reopening because…'_). Don't list every theoretical refactor an ADR forbids."

This means:

- ADRs are **read** during Step 1 alongside CONTEXT.md
- ADRs **constrain** what deepening candidates are proposed
- Contradicting an ADR is allowed **only** when real friction justifies reopening the decision
- Every ADR-conflicting candidate must be **marked explicitly**

The ADR format file (`grill-with-docs/ADR-FORMAT.md`) also clarifies which ADRs are worth having in the first place — all three criteria must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

This triple filter means the `/improve-codebase-architecture` skill is reading a curated set of high-bar decisions, not a dump of every design choice.

### 1.5 File Layout CONTEXT.md and ADRs Are Expected In

From `grill-with-docs/SKILL.md`, which the architecture skill references for its CONTEXT.md and ADR work:

**Single-context repos (most repos):**

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

**Multi-context repos:**

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

The skill infers structure:
- If `CONTEXT-MAP.md` exists, read it to find contexts
- If only a root `CONTEXT.md` exists, single context
- If neither exists, create a root `CONTEXT.md` lazily when the first term is resolved

---

## 2. How It Updates CONTEXT.md Inline and When It Offers ADRs

### 2.1 Inline Updates During the Grilling Loop (Step 3)

The grilling loop is where the user selects a deepening candidate and walks through the design tree. Side effects happen **inline** — not batched, but captured as they crystallize. There are three side-effect triggers:

#### Trigger 1: Naming a Deepened Module After a Concept Not in CONTEXT.md

Verbatim from the SKILL.md:

> "**Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md` — same discipline as `/grill-with-docs` (see [CONTEXT-FORMAT.md](../grill-with-docs/CONTEXT-FORMAT.md)). Create the file lazily if it doesn't exist."

This means the architecture skill can **create** CONTEXT.md if it doesn't exist (lazy creation), and it uses the same format specified in `grill-with-docs/CONTEXT-FORMAT.md` (see Section 4 below for the full format).

#### Trigger 2: Sharpening a Fuzzy Term During Conversation

Verbatim:

> "**Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there."

This is immediate, unbatched. The moment a term becomes precise through discussion, it goes into CONTEXT.md.

#### Trigger 3: User Rejects a Candidate with a Load-Bearing Reason

Verbatim:

> "**User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _'Want me to record this as an ADR so future architecture reviews don't re-suggest it?'_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ('not worth it right now') and self-evident ones. See [ADR-FORMAT.md](../grill-with-docs/ADR-FORMAT.md)."

The ADR offer has a specific gating condition: only when the rejection reason would be **useful to a future explorer** to avoid re-suggesting the same thing. This is narrower than the `/grill-with-docs` ADR offer. Two filter conditions are added on top of the standard three:

1. **Not ephemeral** — "not worth it right now" is not recorded
2. **Not self-evident** — obvious reasons are not recorded

This gives the architecture skill a more conservative ADR policy than `grill-with-docs` alone, because the architecture skill is explicitly iterating on rejected candidates, and most rejections during an architecture review are exploratory rather than load-bearing.

#### The Framing of the ADR Offer

The skill gives an exact phrasing template:

> "Want me to record this as an ADR so future architecture reviews don't re-suggest it?"

This phrasing is significant: it frames the ADR as serving **future runs of this same skill**, not just future humans. The ADR becomes a way to prevent the architecture skill from proposing the same rejected refactor on the next run.

### 2.2 How CONTEXT.md Updates Are Formatted (Cross-Reference to grill-with-docs)

The architecture skill delegates to `grill-with-docs/CONTEXT-FORMAT.md` for the format. The full format is detailed in Section 4 below. Key rules:

- Be opinionated: pick the best term, list others as aliases to avoid
- Flag conflicts explicitly in a "Flagged ambiguities" section
- Keep definitions to one sentence max: define what it IS, not what it does
- Show relationships using bold term names with cardinality
- Only include terms specific to the project's context, not general programming concepts
- Group terms under subheadings when natural clusters emerge
- Write an example dialogue

### 2.3 How ADRs Are Formatted

ADRs live in `docs/adr/` with sequential numbering (`0001-slug.md`, etc.). The template is intentionally minimal:

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

Optional sections (only when they add genuine value):
- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`)
- **Considered Options** — only when rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need calling out

---

## 3. The Complete LANGUAGE.md Vocabulary

### 3.1 Full Term Definitions

These are the exact definitions from `LANGUAGE.md`, which the skill mandates using "exactly in every suggestion" and never drifting from into substitute terms.

---

**Module**

> Anything with an interface and an implementation. Deliberately scale-agnostic — applies equally to a function, class, package, or tier-spanning slice.
> _Avoid_: unit, component, service.

---

**Interface**

> Everything a caller must know to use the module correctly. Includes the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics.
> _Avoid_: API, signature (too narrow — those refer only to the type-level surface).

---

**Implementation**

> What's inside a module — its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

---

**Depth**

> Leverage at the interface — the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface. A module is **shallow** when the interface is nearly as complex as the implementation.

---

**Seam** _(from Michael Feathers)_

> A place where you can alter behaviour without editing in that place. The *location* at which a module's interface lives. Choosing where to put the seam is its own design decision, distinct from what goes behind it.
> _Avoid_: boundary (overloaded with DDD's bounded context).

---

**Adapter**

> A concrete thing that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).

---

**Leverage**

> What callers get from depth. More capability per unit of interface they have to learn. One implementation pays back across N call sites and M tests.

---

**Locality**

> What maintainers get from depth. Change, bugs, knowledge, and verification concentrate at one place rather than spreading across callers. Fix once, fixed everywhere.

---

### 3.2 Full Principles

From LANGUAGE.md:

> - **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts — they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
> - **The deletion test.** Imagine deleting the module. If complexity vanishes, the module wasn't hiding anything (it was a pass-through). If complexity reappears across N callers, the module was earning its keep.
> - **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
> - **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a seam unless something actually varies across it.

### 3.3 Relationships Diagram (Verbatim from LANGUAGE.md)

> - A **Module** has exactly one **Interface** (the surface it presents to callers and tests).
> - **Depth** is a property of a **Module**, measured against its **Interface**.
> - A **Seam** is where a **Module**'s **Interface** lives.
> - An **Adapter** sits at a **Seam** and satisfies the **Interface**.
> - **Depth** produces **Leverage** for callers and **Locality** for maintainers.

### 3.4 Rejected Framings (Verbatim from LANGUAGE.md)

> - **Depth as ratio of implementation-lines to interface-lines** (Ousterhout): rewards padding the implementation. We use depth-as-leverage instead.
> - **"Interface" as the TypeScript `interface` keyword or a class's public methods**: too narrow — interface here includes every fact a caller must know.
> - **"Boundary"**: overloaded with DDD's bounded context. Say **seam** or **interface**.

### 3.5 How the Vocabulary Flows Through the Skill's Process

The SKILL.md's glossary section (lines 10-28) gives a compressed version of the LANGUAGE.md definitions, with this directive:

> "Use these terms exactly in every suggestion. Consistent language is the point — don't drift into 'component,' 'service,' 'API,' or 'boundary.' Full definitions in LANGUAGE.md."

This creates a two-tier vocabulary system:
1. **SKILL.md glossary** — the compact reference the agent sees at the top of every invocation
2. **LANGUAGE.md** — the full definitions with rationale, "avoid" lists, and rejected framings

The INTERFACE-DESIGN.md and DEEPENING.md sub-documents each reference LANGUAGE.md independently, meaning the vocabulary is a shared dependency across all four files in the skill.

---

## 4. Cross-Referencing with `/grill-with-docs` Format Files

### 4.1 The Architecture Skill Explicitly Delegates to grill-with-docs Formats

The `/improve-codebase-architecture` SKILL.md contains two explicit cross-references to `grill-with-docs` documentation:

1. **Line 68**: `"[...] same discipline as /grill-with-docs (see [CONTEXT-FORMAT.md](../grill-with-docs/CONTEXT-FORMAT.md))"`
2. **Line 70**: `"[...] See [ADR-FORMAT.md](../grill-with-docs/ADR-FORMAT.md)"`

This means `/improve-codebase-architecture` is not just a consumer of CONTEXT.md and ADRs — it is also a **producer** that writes in the same format.

### 4.2 CONTEXT-FORMAT.md — The Full Specification

The architecture skill uses this format when creating or updating CONTEXT.md. The complete specification from `grill-with-docs/CONTEXT-FORMAT.md`:

**Structure template:**

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A concise description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account

## Relationships

- An **Order** produces one or more **Invoices**
- An **Invoice** belongs to exactly one **Customer**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — resolved: these are distinct concepts.
```

**Rules for CONTEXT.md (verbatim):**

> - **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
> - **Flag conflicts explicitly.** If a term is used ambiguously, call it out in "Flagged ambiguities" with a clear resolution.
> - **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
> - **Show relationships.** Use bold term names and express cardinality where obvious.
> - **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
> - **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.
> - **Write an example dialogue.** A conversation between a dev and a domain expert that demonstrates how the terms interact naturally and clarifies boundaries between related concepts.

**Single vs multi-context repos:**

Most repos have a single `CONTEXT.md` at the root. Multi-context repos use a `CONTEXT-MAP.md` at the root that lists contexts, where they live, and how they relate:

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

The architecture skill infers which structure applies:
- If `CONTEXT-MAP.md` exists, read it to find contexts
- If only a root `CONTEXT.md` exists, single context
- If neither exists, create a root `CONTEXT.md` lazily when the first term is resolved

When multiple contexts exist, the architecture skill should infer which one the current topic relates to. If unclear, ask.

### 4.3 ADR-FORMAT.md — The Full Specification

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc. The `docs/adr/` directory is created lazily — only when the first ADR is needed.

**Template (minimal by default):**

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

"That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections."

**Optional sections** (only when they add genuine value):

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

**When to offer an ADR — all three must be true:**

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

**What qualifies for an ADR (examples from the format doc):**

> - **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
> - **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
> - **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
> - **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
> - **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite.
> - **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
> - **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it.

### 4.4 The Architecture Skill's Additional ADR Constraints

The architecture skill adds two constraints on top of the standard ADR qualifying criteria:

1. **Skip ephemeral reasons** — "not worth it right now" is not ADR-worthy
2. **Skip self-evident reasons** — obvious reasons don't need recording

Plus the ADR offer is specifically framed around preventing future architecture reviews from re-suggesting the same thing:

> "Want me to record this as an ADR so future architecture reviews don't re-suggest it?"

This is narrower than the grill-with-docs ADR offer, which is broader:

> "Only offer to create an ADR when all three are true: hard to reverse, surprising without context, result of a real trade-off."

The architecture skill inherits these three criteria AND adds the ephemeral/self-evident filter AND the future-architecture-review framing.

---

## 5. The Deprecated Ubiquitous-Language Skill — Complete Flow

### 5.1 Metadata

From `/home/codey/Dev/pocock-skills/skills/deprecated/ubiquitous-language/SKILL.md`:

```yaml
name: ubiquitous-language
description: Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD".
disable-model-invocation: true
```

The `disable-model-invocation: true` means the skill does NOT spawn sub-agents or use tools — it works purely within the conversation context.

### 5.2 Full Process

**Step 1: Scan the conversation** for domain-relevant nouns, verbs, and concepts

**Step 2: Identify problems** — three specific categories:
- Same word used for different concepts (ambiguity)
- Different words used for the same concept (synonyms)
- Vague or overloaded terms

**Step 3: Propose a canonical glossary** with opinionated term choices

**Step 4: Write to `UBIQUITOUS_LANGUAGE.md`** in the working directory using the specified format

**Step 5: Output a summary** inline in the conversation

### 5.3 Output Format

The skill writes a `UBIQUITOUS_LANGUAGE.md` file with this exact structure:

```md
# Ubiquitous Language

## Order lifecycle

| Term        | Definition                                              | Aliases to avoid      |
| ----------- | ------------------------------------------------------- | --------------------- |
| **Order**   | A customer's request to purchase one or more items      | Purchase, transaction |
| **Invoice** | A request for payment sent to a customer after delivery | Bill, payment request |

## People

| Term         | Definition                                  | Aliases to avoid       |
| ------------ | ------------------------------------------- | ---------------------- |
| **Customer** | A person or organization that places orders | Client, buyer, account |
| **User**     | An authentication identity in the system    | Login, account         |

## Relationships

- An **Invoice** belongs to exactly one **Customer**
- An **Order** produces one or more **Invoices**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed. A single **Order** can produce multiple **Invoices** if items ship in separate **Shipments**."
> **Dev:** "So if a **Shipment** is cancelled before dispatch, no **Invoice** exists for it?"
> **Domain expert:** "Exactly. The **Invoice** lifecycle is tied to the **Fulfillment**, not the **Order**."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — these are distinct concepts: a **Customer** places orders, while a **User** is an authentication identity that may or may not represent a **Customer**.
```

### 5.4 Rules (Verbatim)

> - **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
> - **Flag conflicts explicitly.** If a term is used ambiguously in the conversation, call it out in the "Flagged ambiguities" section with a clear recommendation.
> - **Only include terms relevant for domain experts.** Skip the names of modules or classes unless they have meaning in the domain language.
> - **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
> - **Show relationships.** Use bold term names and express cardinality where obvious.
> - **Only include domain terms.** Skip generic programming concepts (array, function, endpoint) unless they have domain-specific meaning.
> - **Group terms into multiple tables** when natural clusters emerge (e.g. by subdomain, lifecycle, or actor). Each group gets its own heading and table. If all terms belong to a single cohesive domain, one table is fine — don't force groupings.
> - **Write an example dialogue.** A short conversation (3-5 exchanges) between a dev and a domain expert that demonstrates how the terms interact naturally. The dialogue should clarify boundaries between related concepts and show terms being used precisely.

### 5.5 Re-Running Behavior

When invoked again in the same conversation:

1. Read the existing `UBIQUITOUS_LANGUAGE.md`
2. Incorporate any new terms from subsequent discussion
3. Update definitions if understanding has evolved
4. Re-flag any new ambiguities
5. Rewrite the example dialogue to incorporate new terms

### 5.6 Key Differences from the Current Approach

| Aspect | `/ubiquitous-language` (deprecated) | Current approach (`CONTEXT.md` via `/grill-with-docs`) |
|---|---|---|
| **Output file** | `UBIQUITOUS_LANGUAGE.md` | `CONTEXT.md` |
| **When it runs** | Explicit invocation only | Inline during `/grill-with-docs` and `/improve-codebase-architecture` |
| **Is it standalone?** | Yes — a standalone skill with `disable-model-invocation: true` | No — integrated into the grilling and architecture workflows |
| **How terms are discovered** | Scans the current conversation | Terms are discovered and resolved during the grilling loop as decisions crystallize |
| **Relationships** | Flat list of relationships | Same, but in CONTEXT.md |
| **Scope** | Single-file, single-context only | Supports multi-context repos via `CONTEXT-MAP.md` |
| **ADR integration** | None | Integrated: CONTEXT.md and ADRs are maintained together during `/grill-with-docs` |
| **Architecture vocabulary** | None | LANGUAGE.md provides a parallel architecture vocabulary |
| **Term format** | Markdown tables with term/definition/aliases columns | Bold-header paragraphs with `_Avoid_` annotations |
| **Grouping** | By subdomain via `##` headings with tables | By subdomain via `##` headings with bold-header lists |

---

## 6. Evolution from Ubiquitous-Language to CONTEXT.md — What Changed and Why

### 6.1 The Core Shift: From Standalone Glossary to Living Context

The deprecated `/ubiquitous-language` was a **standalone extraction tool** — you invoke it, it scans the conversation, and it produces a glossary file. It was inspired by DDD's "ubiquitous language" concept and saved to `UBIQUITOUS_LANGUAGE.md`.

The current approach replaces this with `CONTEXT.md`, which is:

1. **Not a standalone skill** — it's maintained **inline** during grilling sessions and architecture reviews
2. **Not just a glossary** — it's positioned as the project's "context," encompassing language, relationships, and ambiguities
3. **Not invoked separately** — it's updated as a side effect of other skills, not as its own skill

### 6.2 What Changed

#### 6.2.1 File Name and Concept

`UBIQUITOUS_LANGUAGE.md` became `CONTEXT.md`. The name change is significant:

- **"Ubiquitous Language"** is a DDD term that connotes a specific methodology. It signals "this is a glossary built using domain-driven design practices."
- **"Context"** is a broader, more neutral term. It signals "this is the context you need to understand this project — including its language, relationships, and ambiguities." The word also maps to the DDD concept of a "Bounded Context" when multi-context repos are involved.

#### 6.2.2 Term Format

`UBIQUITOUS_LANGUAGE.md` used **Markdown tables**:

```md
| Term        | Definition                              | Aliases to avoid |
| ----------- | --------------------------------------- | ---------------- |
| **Order**   | A customer's request to purchase items  | Purchase, transaction |
```

`CONTEXT.md` uses **bold-header paragraphs**:

```md
**Order**:
{A concise description of the term}
_Avoid_: Purchase, transaction
```

This change makes the file more scannable and easier to edit inline. Tables are rigid to maintain; bold-header paragraphs flow naturally and are easier to update in a text editor.

#### 6.2.3 Invocation Model

`/ubiquitous-language` was a **discrete invocation** — you call the skill, it produces the file. It was disabled from model invocation (`disable-model-invocation: true`), meaning the agent could not invoke it automatically.

`CONTEXT.md` is maintained **inline** as a continuous side effect. Both `/grill-with-docs` and `/improve-codebase-architecture` write to it during their workflows:

- `/grill-with-docs`: "When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen."
- `/improve-codebase-architecture`: "Naming a deepened module after a concept not in `CONTEXT.md`? Add the term to `CONTEXT.md` — same discipline as `/grill-with-docs`."

#### 6.2.4 Multi-Context Support

`/ubiquitous-language` had no concept of multiple bounded contexts. A single `UBIQUITOUS_LANGUAGE.md` was always at the working directory root.

`CONTEXT.md` introduces a `CONTEXT-MAP.md` concept for repos with multiple bounded contexts. The map lists contexts, their locations, and their relationships. This aligns with DDD's Context Map pattern but in a lightweight, markdown-native way.

#### 6.2.5 ADR Integration

`/ubiquitous-language` had **no ADR integration whatsoever**. It was purely a glossary tool.

The current approach (via `/grill-with-docs`) integrates CONTEXT.md with ADRs. ADRs are maintained lazily during the same session, with a strict three-criterion test (hard to reverse, surprising without context, result of a real trade-off).

`/improve-codebase-architecture` adds ADRs with **even stricter gating**: only when a user rejects a deepening candidate with a load-bearing reason, and only when that reason would prevent future architecture reviews from re-suggesting the same thing.

#### 6.2.6 Architecture Vocabulary

`/ubiquitous-language` was purely about **domain language** — the terms business experts use.

The current approach introduces a **parallel architecture vocabulary** via `LANGUAGE.md`. This vocabulary (Module, Interface, Implementation, Depth, Seam, Adapter, Leverage, Locality) is used alongside the domain vocabulary when discussing architecture:

> "Use CONTEXT.md vocabulary for the domain, and LANGUAGE.md vocabulary for the architecture."

The README explains why this matters:

> "A shared language has many other benefits than reducing verbosity:
> - **Variables, functions and files are named consistently**, using the shared language
> - As a result, the **codebase is easier to navigate** for the agent
> - The agent also **spends fewer tokens on thinking**, because it has access to a more concise language"

### 6.3 Why It Changed

The evolution addresses several shortcomings of the `/ubiquitous-language` approach:

1. **Glossary extraction is too late.** If you have to invoke a skill to build a glossary, you've already had the conversation without it. The current approach builds the glossary **during** the conversation, capturing terms as they're resolved.

2. **Glossary extraction is too separate.** A standalone skill doesn't interact with other parts of the workflow. The current approach weaves term resolution into the grilling and architecture review workflows, making the glossary a living document that evolves with the project.

3. **Domain language alone isn't enough.** Architecture discussions need their own precise vocabulary. The `LANGUAGE.md` file gives a shared architecture vocabulary that prevents drift into fuzzy terms like "component," "service," "API," or "boundary."

4. **Decisions need recording too.** A glossary doesn't capture architectural decisions. ADRs fill this gap, and they're maintained in the same session as the glossary.

5. **The DDD framing was too heavy.** "Ubiquitous Language" is a loaded DDD term. "Context" is lighter and maps to the bounded context pattern when needed, without requiring full DDD adoption.

---

## 7. How `/grill-me` Differs from `/grill-with-docs`

### 7.1 `/grill-me` — The Non-Docs Version

Full text of `/home/codey/Dev/pocock-skills/skills/productivity/grill-me/SKILL.md`:

```yaml
---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---
```

Body:

> Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time.
>
> If a question can be answered by exploring the codebase, explore the codebase instead.

### 7.2 `/grill-with-docs` — The Docs-Aware Version

Full text of `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/SKILL.md`:

```yaml
---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
---
```

Body (core instruction):

> Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.
>
> Ask the questions one at a time, waiting for feedback on each question before continuing.
>
> If a question can be answered by exploring the codebase, explore the codebase instead.

Plus the entire `<supporting-info>` section (lines 16-88) covering:
- Domain awareness (reading CONTEXT.md, CONTEXT-MAP.md, ADRs)
- File structure conventions
- Challenging against the glossary
- Sharpening fuzzy language
- Discussing concrete scenarios
- Cross-referencing with code
- Updating CONTEXT.md inline
- Offering ADRs sparingly

### 7.3 Comparison Table

| Aspect | `/grill-me` | `/grill-with-docs` |
|---|---|---|
| **Invocation** | `/grill-me` | `/grill-with-docs` |
| **Bucket** | `productivity/` | `engineering/` |
| **Core behavior** | Relentless interview about a plan or design | Same relentless interview, plus documentation side effects |
| **Reads CONTEXT.md?** | No | Yes — reads existing CONTEXT.md, CONTEXT-MAP.md, and ADRs |
| **Writes CONTEXT.md?** | No | Yes — updates inline as terms are resolved |
| **Writes ADRs?** | No | Yes — offers ADRs when decisions meet the three criteria |
| **Challenges glossary?** | No | Yes — flags when user's terms conflict with CONTEXT.md |
| **Sharpens fuzzy language?** | No | Yes — proposes precise canonical terms |
| **Discusses concrete scenarios?** | No | Yes — stress-tests domain relationships with edge cases |
| **Cross-references with code?** | No | Yes — checks if code agrees with stated behavior |
| **Codebase exploration** | Yes — "If a question can be answered by exploring the codebase, explore the codebase instead" | Same — plus it reads domain docs first |
| **disable-model-invocation** | Not set | Not set |
| **Use case** | Non-code grilling (plans, strategies, designs where you don't need to maintain a shared language document) | Code-adjacent grilling where you want to build and maintain a shared language |
| **Output** | Just the conversation | The conversation PLUS updated CONTEXT.md and optionally new ADRs |

### 7.4 The Key Insight

`/grill-me` is the **pure grilling protocol** — it's the core interview technique. `/grill-with-docs` wraps that same technique in a **documentation maintenance workflow**. Every feature `/grill-with-docs` adds is about capturing decisions and language into persistent files that survive across sessions.

The README makes this explicit:

> - [`/grill-me`](./skills/productivity/grill-me/SKILL.md) - for non-code uses
> - [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md) - same as [`/grill-me`](./skills/productivity/grill-me/SKILL.md), but adds more goodies (see below)

And:

> These are my most popular skills. They help you align with the agent before you get started, and think deeply about the change you're making. Use them _every_ time you want to make a change.

### 7.5 How `/improve-codebase-architecture` Relates to Both

The architecture skill's grilling loop (Step 3) inherits the grilling protocol from `/grill-me` (relentless interview, one question at a time, resolve dependencies) but adds documentation side effects from `/grill-with-docs`:

- Update CONTEXT.md when naming new concepts
- Update CONTEXT.md when sharpening fuzzy terms
- Offer ADRs when load-bearing rejections occur

It does NOT, however, use `/grill-with-docs` directly. It references its **file formats** (CONTEXT-FORMAT.md and ADR-FORMAT.md) but has its own grilling context focused on architecture deepening, not general plan alignment.

---

## 8. Other Context Consumers — `/zoom-out` and `/to-issues`

### 8.1 `/zoom-out`

Full text of `/home/codey/Dev/pocock-skills/skills/engineering/zoom-out/SKILL.md`:

> I don't know this area of code well. Go up a layer of abstraction. Give me a map of all the relevant modules and callers, using the project's domain glossary vocabulary.

This skill is a **pure consumer** of CONTEXT.md vocabulary. It does not write to CONTEXT.md or create ADRs. Its instruction to use "the project's domain glossary vocabulary" means it reads CONTEXT.md and uses the canonical terms defined there to describe the module map.

It's listed as a context consumer in the README:

> [`/zoom-out`](./skills/engineering/zoom-out/SKILL.md) tells the agent to explain code in the context of the whole system

### 8.2 `/to-issues`

From `/home/codey/Dev/pocock-skills/skills/engineering/to-issues/SKILL.md`, Step 2:

> "Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching."

And from Step 1:

> "Work from whatever is already in the conversation context."

This skill is also a **consumer** of CONTEXT.md vocabulary and ADRs. It reads them to ensure issue titles and descriptions use the right terms and don't contradict recorded decisions. It does not write to either.

### 8.3 The Deprecated `/qa` Skill

The deprecated QA skill (`/home/codey/Dev/pocock-skills/skills/deprecated/qa/SKILL.md`) references `UBIQUITOUS_LANGUAGE.md`:

> "Learn the domain language used in that area (check UBIQUITOUS_LANGUAGE.md)"

And in its rules:

> "Use the project's domain language (check UBIQUITOUS_LANGUAGE.md if it exists)"

This confirms that the deprecated QA skill was still using the old `UBIQUITOUS_LANGUAGE.md` convention, not the current `CONTEXT.md` convention. This is another sign that the skill was deprecated before the transition to CONTEXT.md was made.

---

## 9. The Complete Architecture Skill Process — End-to-End

For completeness, here is the full end-to-end flow of `/improve-codebase-architecture`:

### Step 1: Explore

1. Read the project's domain glossary (CONTEXT.md) and any ADRs in the area being touched
2. Use an Agent tool with `subagent_type=Explore` to walk the codebase organically
3. Note friction: shallow modules, missing locality, leaked seams, untestable interfaces
4. Apply the **deletion test** to anything suspected of being shallow

### Step 2: Present Candidates

1. Present a numbered list of deepening opportunities, each with:
   - **Files** — which files/modules are involved
   - **Problem** — why the current architecture causes friction
   - **Solution** — plain English description of what would change
   - **Benefits** — explained in terms of locality and leverage, and how tests would improve
2. Use CONTEXT.md vocabulary for domain terms and LANGUAGE.md vocabulary for architecture terms
3. Flag ADR conflicts only when friction is real enough to warrant revisiting
4. Do NOT propose interfaces yet — ask the user which candidates to explore

### Step 3: Grilling Loop

1. Walk the design tree with the user for each chosen candidate
2. Side effects inline:
   - New domain concept not in CONTEXT.md? → Add it
   - Fuzzy term sharpened? → Update CONTEXT.md
   - User rejects candidate with load-bearing reason? → Offer an ADR
3. Optionally enter INTERFACE-DESIGN.md process for exploring alternative interfaces
4. Optionally use DEEPENING.md process for implementing the deepened module

### DEEPENING.md — Dependency Categories

When implementing a deepening, classify dependencies:

1. **In-process** — Pure computation, no I/O. Always deepenable. Test directly.
2. **Local-substitutable** — Has local test stand-ins (PGLite, in-memory FS). Deepenable if the stand-in exists. Seam is internal.
3. **Remote but owned (Ports & Adapters)** — Own services across network. Define a port at the seam, inject adapters.
4. **True external (Mock)** — Third-party services you don't control. Inject port; provide mock adapter for tests.

### INTERFACE-DESIGN.md — "Design It Twice" Process

1. Frame the problem space (constraints, dependencies, rough sketch)
2. Spawn 3+ sub-agents in parallel, each with a different design constraint
3. Present designs sequentially and compare by depth, locality, and seam placement
4. Give an opinionated recommendation

---

## 10. Summary of the Context Ecosystem

The `/improve-codebase-architecture` skill sits at the center of a context ecosystem:

```
                        ┌──────────────────────┐
                        │     CONTEXT.md       │◄──── Written by /grill-with-docs
                        │   (domain language)  │◄──── Written by /improve-codebase-architecture
                        │                      │
                        │   Read by:           │
                        │   /zoom-out          │
                        │   /to-issues         │
                        │   /improve-codebase-architecture
                        │   /grill-with-docs   │
                        └──────────────────────┘

                        ┌──────────────────────┐
                        │     LANGUAGE.md       │◄──── Standalone file in the skill directory
                        │   (architecture vocab)│      (not in the project repo)
                        │                      │
                        │   Read by:           │
                        │   /improve-codebase-architecture
                        │   (SKILL.md, DEEPENING.md, INTERFACE-DESIGN.md)
                        └──────────────────────┘

                        ┌──────────────────────┐
                        │     docs/adr/         │◄──── Written by /grill-with-docs
                        │   (architectural     │◄──── Written by /improve-codebase-architecture
                        │    decisions)         │
                        │                      │
                        │   Read by:           │
                        │   /improve-codebase-architecture
                        │   /grill-with-docs   │
                        │   /to-issues         │
                        └──────────────────────┘

                        ┌──────────────────────┐
                        │ UBIQUITOUS_LANGUAGE  │◄──── DEPRECATED — no longer used
                        │       .md            │      Was written by /ubiquitous-language
                        │                      │      Was read by /qa (also deprecated)
                        └──────────────────────┘
```

The key architectural decision is that `/improve-codebase-architecture` is both a **consumer and a producer** of CONTEXT.md and ADRs. It reads them first (Step 1) to understand the domain and constraints, then writes to them during the grilling loop (Step 3) as new terms crystallize and decisions are rejected with load-bearing reasons.
