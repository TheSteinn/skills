# Deep Dive: `/grill-with-docs` Skill — Excruciating Detail

## 1. Skill Identity and Metadata

- **Name**: `grill-with-docs`
- **Invocation**: `/grill-with-docs` (via slash-command in Claude Code)
- **Location**: `skills/engineering/grill-with-docs/`
- **Plugin registration**: Listed in `.claude-plugin/plugin.json` at `"./skills/engineering/grill-with-docs"`
- **Frontmatter description** (verbatim):

  > "Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions."

- **`disable-model-invocation`: NOT present** — this skill CAN be invoked by the model autonomously (unlike `ubiquitous-language`, `setup-matt-pocock-skills`, and `zoom-out`, which all have `disable-model-invocation: true`). This is a significant distinction: the LLM may proactively suggest this skill.

- **Composed files** (3 total):
  1. `SKILL.md` — the core prompt/instructions
  2. `CONTEXT-FORMAT.md` — specification for CONTEXT.md structure and rules
  3. `ADR-FORMAT.md` — specification for ADR file structure and rules

---

## 2. Relationship to `/grill-me`

The `README.md` describes the relationship explicitly:

> `/grill-with-docs` - same as `/grill-me`, but adds more goodies (see below)

### What `/grill-me` does (verbatim):

```
Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

### What `/grill-with-docs` inherits and extends

The `<what-to-do>` block in `/grill-with-docs` is nearly identical to `/grill-me`:

```
Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.
```

The ONLY textual difference from `/grill-me` is the addition of the phrase **", waiting for feedback on each question before continuing"** in the second paragraph. This clarifies that the turn-by-turn interaction is mandatory — the LLM should not batch multiple questions.

The entire `<supporting-info>` block (lines 16–88) is what `/grill-with-docs` adds on top of `/grill-me`. This is the "more goodies" referenced in the README.

---

## 3. Exact Prompt/Instructions the Skill Gives the LLM

The skill MMdl is divided into two XML-tagged sections: `<what-to-do>` and `<supporting-info>`.

### 3.1 `<what-to-do>` (verbatim, lines 6–14)

```xml
<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>
```

### 3.2 `<supporting-info>` (verbatim, lines 16–88)

```xml
<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

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

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

Don't couple `CONTEXT.md` to implementation details. Only include terms that are meaningful to domain experts.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

</supporting-info>
```

---

## 4. Step-by-Step Flow: What Happens When a User Invokes `/grill-with-docs`

### Phase 0: Invocation and Skill Loading

1. User types `/grill-with-docs` in Claude Code.
2. The skill system loads `skills/engineering/grill-with-docs/SKILL.md` as the primary prompt.
3. The LLM also receives `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` as supporting resources (linked via relative markdown links in the SKILL.md). The exact mechanism of how these are loaded depends on the agent platform's resource-bundling behavior, but the skill references them as `[CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)` and `[ADR-FORMAT.md](./ADR-FORMAT.md)`.
4. No `disable-model-invocation` flag is set, so the LLM may also suggest this skill on its own initiative when the trigger conditions match.

### Phase 1: Domain Discovery (Before the Interview Starts)

The skill's `<supporting-info>` section begins with "During codebase exploration, also look for existing documentation." This is a directive that BEFORE the first question, the LLM must:

1. **Check for `CONTEXT-MAP.md`** at the repo root:
   - If it exists → multi-context repo. Read the map to discover all sub-contexts and their `CONTEXT.md` locations.
   - If it does not exist → check for a root `CONTEXT.md`.
   
2. **Check for `CONTEXT.md`** at the repo root:
   - If it exists → single-context repo. Read it to learn the existing glossary, relationships, flagged ambiguities, and example dialogue.
   - If neither `CONTEXT-MAP.md` nor root `CONTEXT.md` exist → the project has no domain documentation yet. Create a root `CONTEXT.md` lazily "when the first term is resolved."

3. **Check for `docs/adr/`** directory:
   - If it exists → read existing ADRs for relevant past decisions.
   - If it does not exist → create the directory "when the first ADR is needed."

4. **In multi-context repos**: After reading `CONTEXT-MAP.md`, the LLM infers which specific context the current topic relates to. If unclear, it must **ask** the user which context they're discussing.

### Phase 2: The Grilling Interview (Core Behavioral Loop)

Once the LLM has gathered existing domain context, it begins the interview. The behavioral contract is:

1. **Ask one question at a time** — wait for feedback on each question before continuing. Never batch.
2. **Provide a recommended answer** for each question — the LLM is not neutral; it proposes what it believes is right.
3. **Walk down each branch of the design tree, resolving dependencies between decisions one-by-one** — the interview is structured as a depth-first traversal of the decision tree.
4. **If a question can be answered by exploring the codebase, explore the codebase instead** — the LLM should prefer self-answering via code exploration over asking the user something the codebase already knows.

During this interview, **five active behaviors** run simultaneously:

#### Behavior 2a: Challenge Against the Glossary

> "When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately."

The example given (verbatim): `"Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"`

This is an **interruptive** behavior — it must happen "immediately" when a conflict is detected, not queued for later.

#### Behavior 2b: Sharpen Fuzzy Language

> "When the user uses vague or overloaded terms, propose a precise canonical term."

The example given (verbatim): `"You're saying 'account' — do you mean the Customer or the User? Those are different things."`

This is also an **immediate** intervention. It proposes canonical terms from the glossary or suggests new ones.

#### Behavior 2c: Discuss Concrete Scenarios

> "When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts."

The LLM must **invent** scenarios proactively — this is a creative, not merely reactive, behavior.

#### Behavior 2d: Cross-Reference with Code

> "When the user states how something works, check whether the code agrees."

Example given (verbatim): `"Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"`

This requires the LLM to actively explore the codebase during the conversation and surface contradictions.

#### Behavior 2e: Update CONTEXT.md Inline

> "When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen."

This is the critical documentation production behavior. It requires:
- Writing to CONTEXT.md **immediately** when a term is resolved (not at session end)
- Using the format specified in `CONTEXT-FORMAT.md`
- Only including terms "meaningful to domain experts" — NOT implementation details
- Preserving and extending the existing CONTEXT.md (if any), not rewriting from scratch

### Phase 3: ADR Offer (Conditional)

Throughout the session, when a decision crystallises, the LLM evaluates it against a strict three-part test. An ADR is offered **only** when ALL THREE conditions are true:

1. **Hard to reverse** — "the cost of changing your mind later is meaningful"
2. **Surprising without context** — "a future reader will wonder 'why did they do it this way?'"
3. **The result of a real trade-off** — "there were genuine alternatives and you picked one for specific reasons"

**If ANY of the three is missing, the ADR is skipped.** The ADR-FORMAT.md reinforces this:

> "If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond 'we did the obvious thing.'"

When an ADR is warranted, the LLM:
1. Offers to create it (the user may decline)
2. Creates `docs/adr/` directory if it doesn't exist (lazy creation)
3. Numbers the ADR by scanning existing ADRs and incrementing the highest number
4. Uses the minimal format from `ADR-FORMAT.md`

### Phase 4: Session Continuation

The skill has no explicit termination condition. The interview continues until:
- The user stops responding
- The LLM has exhausted all branches of the design tree
- The user explicitly ends the session

There is no "you're done" marker or wrap-up protocol specified in the skill.

---

## 5. CONTEXT.md Format — Exact Specification

### Structure (from CONTEXT-FORMAT.md, verbatim)

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

### Rules (7 rules, from CONTEXT-FORMAT.md)

1. **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
2. **Flag conflicts explicitly.** If a term is used ambiguously, call it out in "Flagged ambiguities" with a clear resolution.
3. **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
4. **Show relationships.** Use bold term names and express cardinality where obvious.
5. **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
6. **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.
7. **Write an example dialogue.** A conversation between a dev and a domain expert that demonstrates how the terms interact naturally and clarifies boundaries between related concepts.

---

## 6. ADR Format — Exact Specification

### ADR Template (from ADR-FORMAT.md)

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That is the entire mandatory template. The ADR-FORMAT.md explicitly states:

> "That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections."

### Optional Sections (only when they add "genuine value")

- **Status frontmatter** (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

### Numbering

> "Scan `docs/adr/` for the highest existing number and increment by one."

### What Qualifies for an ADR (7 categories)

1. **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
2. **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
3. **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — just the ones that would take a quarter to swap out.
4. **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
5. **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
6. **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
7. **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it — otherwise someone will suggest GraphQL again in six months.

---

## 7. Decision Tree: Create vs. Update CONTEXT.md

```
START: User invokes /grill-with-docs
│
├── Check for CONTEXT-MAP.md at repo root
│   ├── EXISTS → Multi-context repo
│   │   └── Read CONTEXT-MAP.md to find all sub-contexts
│   │       └── Determine which context the current topic relates to
│   │           ├── Clear → Use that context's CONTEXT.md
│   │           └── Unclear → ASK the user which context
│   │
│   └── DOES NOT EXIST
│       └── Check for root CONTEXT.md
│           ├── EXISTS → Single-context repo, read existing CONTEXT.md
│           │   └── During session: UPDATE the existing file inline
│           │       (extend, don't rewrite from scratch)
│           │
│           └── DOES NOT EXIST → No domain documentation yet
│               └── CREATE CONTEXT.md lazily when the first term is resolved
│                   └── Use the format from CONTEXT-FORMAT.md
```

**Key rules for the create/update decision:**

- **Never create CONTEXT.md proactively.** The skill creates it "when the first term is resolved" — not before, not on invocation.
- **Never batch updates.** "When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen."
- **Never include implementation details.** "Don't couple `CONTEXT.md` to implementation details. Only include terms that are meaningful to domain experts."
- **Never overwrite existing content.** Extend existing glossary, relationships, and flagged ambiguities. The real-world example (`CONTEXT.md` in this repo) shows a living document that was incrementally built.

---

## 8. Decision Tree: When to Offer an ADR

```
During session, a decision crystallises
│
├── Is it HARD TO REVERSE?
│   ├── NO → Skip ADR. "You'll just reverse it."
│   └── YES ↓
│
├── Is it SURPRISING WITHOUT CONTEXT?
│   ├── NO → Skip ADR. "Nobody will wonder why."
│   └── YES ↓
│
├── Is it the RESULT OF A REAL TRADE-OFF?
│   ├── NO → Skip ADR. "There's nothing to record beyond 'we did the obvious thing.'"
│   └── YES → OFFER to create an ADR
│       │
│       ├── User declines → Do not create
│       └── User accepts → Create ADR
│           ├── If docs/adr/ doesn't exist → CREATE the directory
│           ├── Scan for highest existing number → increment
│           └── Write ADR using the minimal format
```

**Implicit behaviors:**
- The "offer" is a question to the user, not an automatic action. The user must consent.
- The skill says "Offer ADRs **sparingly**" — the three-part test is meant to be a high bar.
- ADRs are only created during the grilling session, not as a post-session wrap-up.

---

## 9. Multi-Context Repos: CONTEXT-MAP.md Handling

### Detection Logic

```
Check repo root for CONTEXT-MAP.md
│
├── EXISTS → Multi-context repo
│   ├── Read CONTEXT-MAP.md
│   ├── Discover all sub-contexts and their CONTEXT.md paths
│   ├── During grilling: infer which context the topic relates to
│   │   ├── Can infer → Use that context's CONTEXT.md and docs/adr/
│   │   └── Cannot infer → ASK the user "Which context does this relate to?"
│   │
│   └── ADR placement rules:
│       ├── System-wide decisions → root docs/adr/
│       └── Context-specific decisions → src/<context>/docs/adr/
│
└── DOES NOT EXIST → Check for root CONTEXT.md
    ├── EXISTS → Single-context repo
    └── DOES NOT EXIST → Create lazily on first term resolution
```

### CONTEXT-MAP.md Format (from CONTEXT-FORMAT.md)

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

### ADR Placement in Multi-Context Repos

The file structure shown in SKILL.md makes the placement explicit:

```
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

- **Root `docs/adr/`**: System-wide decisions (e.g., "we use a monorepo")
- **Per-context `docs/adr/`**: Context-specific decisions (e.g., "Ordering uses event sourcing")

The consumer skill (`setup-matt-pocock-skills/domain.md`) reinforces this: "In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions."

---

## 10. Interaction with the Deprecated `/ubiquitous-language` Approach

### What `/ubiquitous-language` Was

The deprecated skill (at `skills/deprecated/ubiquitous-language/SKILL.md`) had `disable-model-invocation: true` set, meaning it cannot be auto-invoked by the LLM. It is listed in `skills/deprecated/README.md` and is excluded from both `README.md` references and `plugin.json`.

### Key Differences from `/grill-with-docs`

| Aspect | `/ubiquitous-language` (deprecated) | `/grill-with-docs` (current) |
|--------|--------------------------------------|-------------------------------|
| **Output file** | `UBIQUITOUS_LANGUAGE.md` | `CONTEXT.md` |
| **Content format** | Markdown tables (`\| Term \| Definition \| Aliases to avoid \|`) | Bold-term glossary (`**Term**: Definition\n_Avoid_: synonyms`) |
| **Trigger** | Explicit invocation only (`disable-model-invocation: true`) | Can be auto-suggested by the LLM |
| **When run** | Standalone glossary extraction after a conversation | Inline during an active grilling session |
| **Update mode** | Rewrites the entire file on re-invocation | Updates incrementally "right there" as terms are resolved |
| **ADR integration** | None | Decisions trigger ADR creation |
| **Interview behavior** | None (passive extraction) | Active interview with the five behaviors (challenge glossary, sharpen language, discuss scenarios, cross-reference code, update inline) |
| **Multi-context** | Not supported | Full CONTEXT-MAP.md support |
| **Example dialogue** | Generated as output within the file | Generated as output within the file (same concept, different format) |
| **Relationships section** | Included (same concept) | Included (same concept) |
| **Flagged ambiguities** | Included (same concept) | Included (same concept) |
| **"Be opinionated" rule** | Included (verbatim) | Included (verbatim) |

### What Changed and Why

The fundamental shift is from **passive glossary extraction** to **active grilling with inline documentation**. The deprecated skill ran after the conversation was over and extracted terms from it. The new skill runs IN the conversation, actively shaping it, and documents decisions as they happen.

The format also shifted from tables (which are rigid and harder to read in raw markdown) to bold-term definitions with `_Avoid_:` aliases, which are more natural and scannable.

---

## 11. Consumer Skills: Who Reads CONTEXT.md and ADRs?

### `/setup-matt-pocock-skills` (Producer of the layout, not of content)

The setup skill (`domain.md`) records the repo's context layout (single vs. multi). It explicitly states:

> "If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved."

This creates a clean separation: `setup-matt-pocock-skills` documents WHERE domain files live; `grill-with-docs` creates and populates them.

### Consumer Skills

The following skills read CONTEXT.md and/or ADRs:

1. **`improve-codebase-architecture`** — reads CONTEXT.md for domain vocabulary, reads ADRs for past decisions. References CONTEXT-FORMAT.md and ADR-FORMAT.md from grill-with-docs's directory for the format specs. Also UPDATES CONTEXT.md when naming deepened modules after concepts not in the glossary.

2. **`triage`** — reads CONTEXT.md for "the project's domain glossary, respecting ADRs in the area." Can invoke `/grill-with-docs` as a sub-procedure during triage when an issue "needs fleshing out."

3. **`diagnose`** — reads CONTEXT.md (via domain.md consumer rules) to understand domain language.

4. **`tdd`** — reads CONTEXT.md (via domain.md consumer rules).

5. **`zoom-out`** — reads CONTEXT.md (via domain.md consumer rules).

### The Consumer Rules (from domain.md)

All consumer skills follow these rules:

1. **Read CONTEXT.md** (or CONTEXT-MAP.md for multi-context repos) before exploring the codebase
2. **Use the glossary's vocabulary** in all output — "Don't drift to synonyms the glossary explicitly avoids"
3. **Flag ADR conflicts** — "If your output contradicts an existing ADR, surface it explicitly rather than silently overriding"
4. **If a concept isn't in the glossary yet**, that's a signal: "either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`)"

---

## 12. Real-World Examples

### This Repo's CONTEXT.md (verbatim)

```md
# Matt Pocock Skills

A collection of agent skills (slash commands and behaviors) loaded by Claude Code. Skills are organized into buckets and consumed by per-repo configuration emitted by `/setup-matt-pocock-skills`.

## Language

**Issue tracker**:
The tool that hosts a repo's issues — GitHub Issues, Linear, a local `.scratch/` markdown convention, or similar. Skills like `to-issues`, `to-prd`, `triage`, and `qa` read from and write to it.
_Avoid_: backlog manager, backlog backend, issue host

**Issue**:
A single tracked unit of work inside an **Issue tracker** — a bug, task, PRD, or slice produced by `to-issues`.
_Avoid_: ticket (use only when quoting external systems that call them tickets)

**Triage role**:
A canonical state-machine label applied to an **Issue** during triage (e.g. `needs-triage`, `ready-for-afk`). Each role maps to a real label string in the **Issue tracker** via `docs/agents/triage-labels.md`.

## Relationships

- An **Issue tracker** holds many **Issues**
- An **Issue** carries one **Triage role** at a time

## Flagged ambiguities

- "backlog" was previously used to mean both the *tool* hosting issues and the *body of work* inside it — resolved: the tool is the **Issue tracker**; "backlog" is no longer used as a domain term.
- "backlog backend" / "backlog manager" — resolved: collapsed into **Issue tracker**.
```

Notable: This example CONTEXT.md has NO `Example dialogue` section. This suggests the section may be optional in practice, despite being listed as a rule in CONTEXT-FORMAT.md.

### This Repo's ADR 0001 (verbatim)

```md
# Explicit `/setup-matt-pocock-skills` pointer only for hard dependencies

Engineering skills depend on per-repo config (issue tracker, triage label vocabulary, domain doc layout) seeded by `/setup-matt-pocock-skills`. Some skills cannot meaningfully function without that config — they have to publish to a specific issue tracker or apply a specific label string. Others only use it to sharpen output (vocabulary, ADR awareness) and degrade gracefully without it.

We split these into **hard-dependency** and **soft-dependency** skills:

- **Hard dependency** (`to-issues`, `to-prd`, `triage`) — include an explicit one-liner: _"… should have been provided to you — run `/setup-matt-pocock-skills` if not."_ Without the mapping, output is wrong, not just fuzzy.
- **Soft dependency** (`diagnose`, `tdd`, `improve-codebase-architecture`, `zoom-out`) — reference "the project's domain glossary" and "ADRs in the area you're touching" in vague prose only. If the docs aren't there, the skill still works; output is just less sharp.

The split keeps soft-dependency skills token-light and avoids cargo-culting the setup pointer into places where it isn't load-bearing.
```

This ADR exemplifies the minimal format: a title and 1-3 sentences of context/decision/why. It has no optional sections (no Status, Considered Options, or Consequences). It passes all three ADR tests:
1. **Hard to reverse**: Yes — the split between hard/soft dependency is an architectural decision that affects all skill prompts.
2. **Surprising without context**: Yes — a reader might wonder why some skills have an explicit setup pointer and others don't.
3. **Result of a real trade-off**: Yes — the alternative (always include the setup pointer) was considered and rejected for being verbose in soft-dependency skills.

---

## 13. Edge Cases, Limitations, and Implicit Behaviors

### Edge Case: No Existing Documentation

When a user invokes `/grill-with-docs` on a project with no `CONTEXT.md`, no `CONTEXT-MAP.md`, and no `docs/adr/`:
- The LLM proceeds with the interview normally.
- When the first term is resolved, the LLM creates `CONTEXT.md` from scratch using the CONTEXT-FORMAT.md template.
- If a decision warrants an ADR, the LLM creates the `docs/adr/` directory and the first ADR file.
- There is no "bootstrapping" step — the skill trusts lazy creation entirely.

### Edge Case: Multi-Context Ambiguity

When `CONTEXT-MAP.md` exists and the current topic could span multiple contexts:
- The LLM must **ask the user** which context the topic relates to.
- This is the only situation where the skill explicitly instructs the LLM to ask a meta-question about context scope rather than a domain question.

### Edge Case: Conflicting Terms Across Contexts

The skill does not explicitly address what happens when two sub-contexts define the same term differently. The `CONTEXT-MAP.md` format includes a "Relationships" section that documents inter-context communication patterns, but there is no conflict-resolution protocol for overlapping terminology.

### Edge Case: Updating vs. Overwriting

The CONTEXT-FORMAT.md does not specify a merge strategy for updates. The directive "update CONTEXT.md right there" combined with "Don't batch these up" implies:
- Individual terms are added or refined in-place.
- The entire file is NOT rewritten from scratch on each update.
- The existing example in this repo shows a file that was incrementally extended (the flagged ambiguities reference "was previously used" — indicating evolution over time).

### Implicit Behavior: No Termination Protocol

The skill does not specify when the grilling session ends. There is no "all branches resolved" signal, no maximum question count, and no explicit completion protocol. The session ends when the user stops responding or explicitly ends it. This contrasts with `/triage`, which has a clear outcome protocol (apply a state role).

### Implicit Behavior: CONTEXT.md Format Enforcement

The CONTEXT-FORMAT.md includes formatting rules that aren't explicitly enforced by the skill's prompt:
- "Group terms under subheadings when natural clusters emerge" — this is a soft rule ("when natural clusters emerge")
- "If all terms belong to a single cohesive area, a flat list is fine" — flat lists are the default
- The real-world CONTEXT.md in this repo uses a flat list with no subheadings, suggesting the skill defaults to flat lists unless there's an obvious clustering

### Implicit Behavior: The "Example Dialogue" Section

The CONTEXT-FORMAT.md requires an "Example dialogue" section, but the repo's own CONTEXT.md does not have one. This suggests either:
- The section was removed during a later update (the skill says to update, not rewrite)
- The section is considered optional in practice despite being listed as a rule
- The repo's CONTEXT.md is a minimal example that was never fully populated

### Implicit Behavior: ADR Numbering Concurrency

The ADR numbering rule ("Scan `docs/adr/` for the highest existing number and increment by one") has a theoretical race condition: if two ADR-creating sessions ran simultaneously, they could both read the same highest number and generate conflicting files. In practice, since the skill is interactive and single-threaded (one user, one session), this is unlikely to be a problem.

### Limitation: No Versioning or Change Log for CONTEXT.md

There is no mechanism for tracking changes to CONTEXT.md over time. Terms can be added, refined, or removed without any record of what changed. The "Flagged ambiguities" section partially serves this purpose by recording resolved conflicts, but general term evolution is not tracked.

### Limitation: No Explicit Conflict Resolution Between New Terms and Code

The skill says "Cross-reference with code" and "When the user states how something works, check whether the code agrees," but it does not specify what happens when the code contradicts the domain model and the code is correct. Should the CONTEXT.md be updated to match the code? Should the code be refactored? The skill only says to "surface" the contradiction ("which is right?") — it's an investigative behavior, not a prescriptive one.

### Limitation: Source-Code-Only External References

The skill references `[CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)` and `[ADR-FORMAT.md](./ADR-FORMAT.md)` using relative links. The skill system must resolve these links and include the referenced files as context for the LLM. If the skill system does not follow these links, the LLM would lack the format specifications. This is an assumption about the agent platform's behavior that is not explicitly documented in the skill itself.

### Implicit Behavior: The Skill Assumes Git-Based Repos

While not stated explicitly, the skill's references to "repo root" and its file structure conventions (root `CONTEXT.md`, `docs/adr/`) assume a standard Git repository layout. The skill does not account for monorepo tools (Turborepo, Nx, etc.) where the "root" may be ambiguous, or for non-Git项目的.

### Implicit Behavior: Dual ADR Location Awareness

In multi-context repos, the skill is aware of two ADR locations:
1. Root `docs/adr/` for system-wide decisions
2. Per-context `src/<context>/docs/adr/` for context-specific decisions

But the ADR-FORMAT.md only specifies "ADRs live in `docs/adr/`" without mentioning the multi-context variant. The SKILL.md's file structure diagram is the only place that shows both locations. This means the ADR creation logic must determine scope (system-wide vs. context-specific) and place the ADR accordingly — but this routing logic is implicit, not explicitly documented.

---

## 14. Summary: The Complete Behavioral Contract

When `/grill-with-docs` is invoked, the LLM agrees to:

1. **Discover** existing domain context (CONTEXT.md or CONTEXT-MAP.md, ADRs)
2. **Interview** the user relentlessly, one question at a time, with recommended answers
3. **Self-answer** by exploring the codebase when possible, instead of asking the user
4. **Challenge** terms that conflict with the existing glossary
5. **Sharpen** fuzzy or overloaded terms by proposing canonical alternatives
6. **Invent** concrete scenarios to stress-test domain relationships
7. **Cross-reference** user claims against actual code
8. **Update** CONTEXT.md immediately as terms are resolved (never batch)
9. **Offer** ADRs sparingly, only when all three criteria (hard to reverse, surprising, real trade-off) are met
10. **Create** files and directories lazily — only when there's something to write
11. **Infer** which context a topic relates to in multi-context repos, asking when unclear
12. **Never** couple CONTEXT.md to implementation details
13. **Never** include general programming concepts in the glossary

This makes `/grill-with-docs` the primary **producer** of domain documentation in the Pocock Skills ecosystem, with all other engineering skills (`diagnose`, `tdd`, `improve-codebase-architecture`, `zoom-out`, `triage`) acting as **consumers** that read and respect the documentation it produces.
