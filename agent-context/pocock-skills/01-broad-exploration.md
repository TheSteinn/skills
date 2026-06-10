# Pocock Skills - Context Building Feature: Broad Exploration

## Feature Overview

The pocock-skills repository implements a "project context/knowledge building" feature that enables an AI agent (specifically Claude Code) to slowly, over time, build and persist a structured understanding of the project it is working in. This manifests in two concrete, persistent artifacts:

1. **CONTEXT.md** — A domain glossary that defines the project's ubiquitous language: canonical terms, their definitions, terms to avoid, relationships between terms, example dialogues, and flagged ambiguities. It acts as a shared vocabulary between the human and the AI, enabling concise, precise communication.

2. **ADRs (Architecture Decision Records)** — Lightweight markdown files stored in `docs/adr/` (sequentially numbered as `0001-slug.md`) that capture significant, hard-to-reverse, surprising architectural decisions alongside the reasoning and alternatives that were considered.

From the user's perspective, the flow works like this:
- The user invokes `/grill-with-docs` (or `/improve-codebase-architecture`) to have an interactive session where the agent interviews them about a plan or design.
- During this session, the agent challenges terminology against the existing glossary, sharpens fuzzy language, and proposes canonical terms.
- When terms are resolved, the agent **immediately updates `CONTEXT.md`** — it doesn't batch these up but captures them as they happen.
- When a significant architectural decision surfaces (one that is hard to reverse, surprising without context, and the result of a genuine trade-off), the agent offers to create an ADR.
- Other skills (`tdd`, `diagnose`, `to-issues`, `to-prd`, `triage`, `zoom-out`) **consume** this context as input, using the glossary terms in their output and respecting past ADRs.

The result is that, over successive sessions, the project accumulates a richer and richer understanding that makes downstream skills more effective — they use the right vocabulary, respect past decisions, and produce more consistent output. The README explicitly calls this out: "It might be the single coolest technique in this repo."

## CONTEXT.md

### What It Is

`CONTEXT.md` is a domain glossary file that lives at the root of a project (or, in multi-context repos, inside each bounded context's directory). It defines the project's shared language — canonical terms, definitions, terms to avoid, relationships, and ambiguities. It serves as a bridge between the human domain expert's vocabulary and the AI agent's output.

The name evolved from the deprecated `UBIQUITOUS_LANGUAGE.md` (see the deprecated `/ubiquitous-language` skill which used that filename). The current name is `CONTEXT.md`.

### Structure and Sections

Defined in `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md`, the canonical structure is:

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

The sections are:
1. **Title** — Name of the context/bounded context
2. **One-line description** — What this context is and why it exists
3. **Language** — Canonical term definitions, each with an `_Avoid_` list of synonyms to reject
4. **Relationships** — How terms relate to each other, using bold term names and cardinality
5. **Example dialogue** — A short conversation between a dev and domain expert demonstrating term usage and clarifying boundaries
6. **Flagged ambiguities** — Historical records of terms that were used ambiguously and how they were resolved

### Rules for CONTEXT.md

From `CONTEXT-FORMAT.md`:
- **Be opinionated.** Pick the best word and list others as aliases to avoid.
- **Flag conflicts explicitly.** If a term is used ambiguously, call it out with a clear resolution.
- **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
- **Show relationships.** Use bold term names and express cardinality.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong.
- **Group terms under subheadings** when natural clusters emerge.
- **Write an example dialogue.** 3-5 exchanges between a dev and domain expert clarifying boundaries.

### Single vs Multi-Context Layout

- **Single context (most repos)**: One `CONTEXT.md` at the repo root.
- **Multiple contexts**: A `CONTEXT-MAP.md` at the repo root lists the contexts, their locations, and their relationships. Each context then has its own `CONTEXT.md` and `docs/adr/` directory.

The `CONTEXT-MAP.md` format:
```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them
```

The skill infers which structure applies:
- If `CONTEXT-MAP.md` exists, read it to find contexts.
- If only a root `CONTEXT.md` exists, single context.
- If neither exists, create a root `CONTEXT.md` lazily when the first term is resolved.

### How It Is Created

`CONTEXT.md` is created **lazily** — only when the first term gets resolved during a grilling session. There's no upfront scaffolding step; the file appears organically when there's actual content to write.

### How It Is Updated

Updates happen **inline** during a `/grill-with-docs` session. The instruction says: "When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen." This means every resolved term is immediately written to the file.

Additionally, `/improve-codebase-architecture` can update `CONTEXT.md`:
- When naming a deepened module after a concept not yet in `CONTEXT.md`, it adds the term.
- When sharpening a fuzzy term during conversation, it updates `CONTEXT.md` right there.

### The Actual CONTEXT.md in This Repo

The repo's own `CONTEXT.md` is self-referentially an example of the feature in action. It defines:
- **Issue tracker**: The tool hosting a repo's issues
- **Issue**: A single tracked unit of work
- **Triage role**: A canonical state-machine label applied during triage

It also records a flagged ambiguity about "backlog" being resolved to "Issue tracker."

## ADRs (Architecture Decision Records)

### What They Are

ADRs are lightweight markdown files that capture significant architectural decisions — why a particular choice was made, what alternatives were considered, and why those alternatives were rejected. They are stored in `docs/adr/` with sequential numbering (`0001-slug.md`, `0002-slug.md`, etc.).

### Format

Defined in `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/ADR-FORMAT.md`:

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's the minimal format. An ADR can be literally a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out templates.

**Optional sections** (only when they add genuine value):
- **Status frontmatter** (`proposed | accepted | deprecated | superseded by ADR-NNNN`)
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need calling out

### Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

### Creation Triggers

ADRs are offered **sparingly** — only when ALL THREE of these conditions are true:
1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives, and you picked one for specific reasons

If any of the three is missing, skip the ADR. The instructions are explicit: "If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond 'we did the obvious thing.'"

### What Qualifies for an ADR

From `ADR-FORMAT.md`:
- **Architectural shape** ("We're using a monorepo.")
- **Integration patterns between contexts** ("Ordering and Billing communicate via domain events, not synchronous HTTP.")
- **Technology choices that carry lock-in** (databases, message buses, auth providers — not every library)
- **Boundary and scope decisions** ("Customer data is owned by the Customer context; others reference it by ID only.")
- **Deliberate deviations from the obvious path** ("We're using manual SQL instead of an ORM because X.")
- **Constraints not visible in the code** ("We can't use AWS because of compliance requirements.")
- **Rejected alternatives when the rejection is non-obvious**

### Storage

- Single-context repos: `docs/adr/` at the project root
- Multi-context repos: System-wide ADRs in root `docs/adr/`, context-specific ADRs in `src/<context>/docs/adr/`

### Creation

ADRs are created lazily — the `docs/adr/` directory is only created when the first ADR is needed. They are created during `/grill-with-docs` sessions and `/improve-codebase-architecture` sessions, offered to the user when a significant decision crystallizes.

### Relationship to CONTEXT.md

ADRs and `CONTEXT.md` are complementary:
- `CONTEXT.md` defines the **language** (what terms mean)
- ADRs record the **decisions** (why certain choices were made)
- Both are consumed by the same set of downstream skills
- ADRs can be cross-referenced in context: when an `/improve-codebase-architecture` candidate contradicts an ADR, it's flagged explicitly

### The Actual ADR in This Repo

The repo has one ADR: `docs/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`, which documents why only hard-dependency skills get an explicit `/setup-matt-pocock-skills` pointer while soft-dependency skills reference context in vague prose.

## Trigger Mechanism

The context-building feature is **NOT automatic on every interaction**. It is triggered by specific, user-initiated skill invocations. Here's how each trigger works:

### Primary Triggers

1. **`/grill-with-docs`** — This is the primary context-building skill. When invoked, it:
   - Starts an interview/grilling session about the user's plan
   - Looks for existing `CONTEXT.md` and `CONTEXT-MAP.md` to understand the current domain glossary
   - Challenges user terminology against the existing glossary
   - Updates `CONTEXT.md` inline as terms are resolved
   - Offers to create ADRs when significant decisions crystallize
   - Creates `CONTEXT.md` lazily if it doesn't exist yet
   - Creates `docs/adr/` lazily if it doesn't exist yet

2. **`/improve-codebase-architecture`** — A secondary context-building trigger. When invoked, it:
   - Reads `CONTEXT.md` and ADRs before exploring
   - Uses `CONTEXT.md` vocabulary in suggestions
   - Updates `CONTEXT.md` inline when naming a new deepened module or sharpening a term
   - Offers ADRs when candidates are rejected with load-bearing reasons
   - Creates `CONTEXT.md` lazily if it doesn't exist

### Context Consumers (Not Triggers, But Readers)

These skills **consume** context but don't create it:
- **`/tdd`** — Uses domain glossary vocabulary in test names; respects ADRs
- **`/diagnose`** — Uses domain glossary to understand modules; checks ADRs
- **`/zoom-out`** — Uses domain glossary vocabulary
- **`/to-issues`** — Uses domain glossary vocabulary in issue titles/descriptions; respects ADRs
- **`/to-prd`** — Uses domain glossary vocabulary throughout the PRD; respects ADRs
- **`/triage`** — Uses domain glossary and checks ADRs; can also trigger `/grill-with-docs` during step 4

### Setup Trigger

3. **`/setup-matt-pocock-skills`** — Sets up the per-repo configuration that tells other skills where to find context docs. It:
   - Explores the repo for existing `CONTEXT.md`, `CONTEXT-MAP.md`, and `docs/adr/`
   - Creates `docs/agents/domain.md` with consumer rules for how to read context
   - Writes an `## Agent skills` block in `CLAUDE.md` or `AGENTS.md` that points to `docs/agents/domain.md`
   - Does NOT create `CONTEXT.md` itself — that's left for the lazy creation by `/grill-with-docs`

### The Consumption Path

The `docs/agents/domain.md` file (created by setup) instructs all skills:
> "Before exploring, read these: CONTEXT.md at the repo root, or CONTEXT-MAP.md if it exists. Also read docs/adr/. If these don't exist, proceed silently — don't flag their absence."

This means that even without explicit `/grill-with-docs` invocation, a skill that has been told to consume domain docs will read them if they exist.

## Implementation Details

### The Flow of Context Creation

The implementation is distributed across multiple skills and configuration files:

#### 1. Setup Phase (`/setup-matt-pocock-skills`)

The setup skill creates the infrastructure that makes context consumption possible:

- **Explores** the repo for existing `CONTEXT.md`, `CONTEXT-MAP.md`, and `docs/adr/`
- **Creates `docs/agents/domain.md`** — a consumer-rules document that tells other skills:
  - Read `CONTEXT.md` (or `CONTEXT-MAP.md` + per-context `CONTEXT.md` files) before exploring
  - Read ADRs relevant to the area being worked on
  - If these files don't exist, proceed silently
  - Use the glossary's vocabulary in output
  - If a needed concept isn't in the glossary, note it for `/grill-with-docs`
  - Flag ADR conflicts explicitly
- **Creates `docs/agents/issue-tracker.md`** — tells skills which issue tracker to use
- **Creates `docs/agents/triage-labels.md`** — maps canonical triage roles to actual label strings
- **Writes an `## Agent skills` block** in `CLAUDE.md` or `AGENTS.md` with pointers to these three docs

#### 2. Context Building Phase (`/grill-with-docs`)

The primary context-building skill:

**SKILL.md** (`/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/SKILL.md`) defines:
- Frontmatter with `name` and `description` (used by Claude Code for skill selection)
- `<what-to-do>` section: the core interview prompt
- `<supporting-info>` section: domain awareness behaviors

The `<what-to-do>` section gives the agent these instructions:
> "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. Ask the questions one at a time. If a question can be answered by exploring the codebase, explore the codebase instead."

The `<supporting-info>` section adds context-aware behaviors:
- **Challenge against the glossary**: Call out terms conflicting with existing `CONTEXT.md` language
- **Sharpen fuzzy language**: Propose precise canonical terms when the user is vague
- **Discuss concrete scenarios**: Stress-test domain relationships with edge-case scenarios
- **Cross-reference with code**: Check whether code agrees with user's statements
- **Update CONTEXT.md inline**: Write resolved terms immediately, not batched
- **Offer ADRs sparingly**: Only when all three criteria (hard to reverse, surprising, real trade-off) are met

**CONTEXT-FORMAT.md** provides the canonical format for `CONTEXT.md`:
- Template structure with all sections
- Rules for content (opinionated, tight definitions, domain-specific only)
- Single vs multi-context repo handling
- Example showing `CONTEXT-MAP.md` for multi-context repos

**ADR-FORMAT.md** provides the canonical format for ADRs:
- Minimal template (just title + 1-3 sentences)
- Optional sections guidance
- Numbering scheme (sequential)
- The three-criteria test for when to offer an ADR
- Examples of what qualifies

#### 3. Context Enhancement Phase (`/improve-codebase-architecture`)

This skill also builds context:

**SKILL.md** (`/home/codey/Dev/pocock-skills/skills/engineering/improve-codebase-architecture/SKILL.md`) defines:
- Step 1 (Explore): Read the project's domain glossary and ADRs first
- Step 2 (Present candidates): Use CONTEXT.md vocabulary and LANGUAGE.md vocabulary
- Step 3 (Grilling loop): Side effects include:
  - Naming a new concept not in `CONTEXT.md`? Add it (lazy creation if needed)
  - Sharpening a fuzzy term? Update `CONTEXT.md` inline
  - User rejects a candidate with a load-bearing reason? Offer an ADR
  - Cross-references `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` from `grill-with-docs/`

The supporting reference files:
- **LANGUAGE.md** — Defines the architecture-specific vocabulary (module, interface, seam, adapter, leverage, locality, depth)
- **INTERFACE-DESIGN.md** — Process for exploring alternative interfaces using parallel sub-agents
- **DEEPENING.md** — How to classify dependencies and deepen modules

#### 4. Context Consumption Phase (All Skills)

Skills that consume context follow the rules in `docs/agents/domain.md`:

- **`/tdd`**: "Use the project's domain glossary so that test names and interface vocabulary match the project's language, and respect ADRs in the area you're touching."
- **`/diagnose`**: "Use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching."
- **`/zoom-out`**: "Give me a map of all the relevant modules and callers, using the project's domain glossary vocabulary."
- **`/to-issues`**: "Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching."
- **`/to-prd`**: "Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching."
- **`/triage`**: "Explore the codebase using the project's domain glossary, respecting ADRs."

### The `domain.md` Consumer Rules Template

The seed template at `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/domain.md` defines how skills should consume domain docs:

1. **Before exploring, read these**: `CONTEXT.md`, or `CONTEXT-MAP.md` if it exists, plus relevant ADRs
2. **If these don't exist, proceed silently** — no flagging, no suggesting creation
3. **Use the glossary's vocabulary** in all output
4. **If a needed concept isn't in the glossary**, note it for `/grill-with-docs`
5. **Flag ADR conflicts** explicitly rather than silently overriding
6. **File structure** reference for both single and multi-context repos

### The `/setup-matt-pocock-skills` Configuration Skill

This is the foundational setup that must run before other skills work properly. It:

1. **Explores** the repo (git remote, existing AGENTS.md/CLAUDE.md, existing CONTEXT.md, existing docs/adr/, existing docs/agents/)
2. **Walks the user through three decisions** one at a time:
   - Section A: Issue tracker (GitHub, GitLab, local markdown, or custom)
   - Section B: Triage label vocabulary (mapping 5 canonical roles to actual labels)
   - Section C: Domain docs (single-context or multi-context layout)
3. **Presents a draft** of all configuration for user review
4. **Writes configuration**:
   - `## Agent skills` block in `CLAUDE.md` or `AGENTS.md`
   - `docs/agents/issue-tracker.md`
   - `docs/agents/triage-labels.md`
   - `docs/agents/domain.md`
5. Does NOT create `CONTEXT.md` or `docs/adr/` — those are created lazily

### Skill Selection Mechanism

Skills are registered in `.claude-plugin/plugin.json` with their paths. Each SKILL.md has YAML frontmatter with `name` and `description` fields. The `description` field is what the agent sees when deciding which skill to load — it must include trigger keywords ("Use when...").

The `disable-model-invocation: true` flag on some skills (e.g., `setup-matt-pocock-skills`, `grill-me`, `zoom-out`) means these skills are only triggered by explicit user invocation (`/skill-name`), not by the agent deciding on its own to invoke them.

### The Deprecated ubiquitous-language Skill

The deprecated `/ubiquitous-language` skill (`/home/codey/Dev/pocock-skills/skills/deprecated/ubiquitous-language/SKILL.md`) is an earlier iteration of the context-building feature. It:
- Wrote to `UBIQUITOUS_LANGUAGE.md` (not `CONTEXT.md`)
- Used table format instead of the current definition-list format
- Was a standalone "extract and formalize" skill rather than an inline update mechanism
- Had its own re-running logic (read existing file, incorporate new terms, update, re-flag ambiguities)

This was deprecated in favor of the inline approach used by `/grill-with-docs`, where context is built incrementally during active grilling sessions rather than as a separate extraction step.

### The Deprecated /qa Skill

The deprecated `/qa` skill referenced `UBIQUITOUS_LANGUAGE.md` rather than `CONTEXT.md`, showing the old naming convention before the rename.

## Persistence Strategy

### How Context Persists Between Sessions

Context persistence is file-based and relies on standard version control:

1. **`CONTEXT.md`** is a plain markdown file at the project root (or within each bounded context subdirectory for multi-context repos). It persists because it's committed to the repo alongside the code.

2. **ADRs** are plain markdown files in `docs/adr/` (or `src/<context>/docs/adr/` for multi-context repos). They persist as part of the codebase.

3. **`docs/agents/`** configuration files (`domain.md`, `issue-tracker.md`, `triage-labels.md`) persist in the repo and are referenced from `CLAUDE.md`/`AGENTS.md`.

4. **`CLAUDE.md`/`AGENTS.md`** contains an `## Agent skills` section that points to the three config files. This is the entry point that all new sessions read.

### How the System Knows What Context Already Exists

The setup skill explicitly checks for existing files during its exploration phase. But more importantly, the consumer rules in `domain.md` say:

> "If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved."

And the `/grill-with-docs` skill infers the structure:
- If `CONTEXT-MAP.md` exists, read it to find contexts
- If only a root `CONTEXT.md` exists, single context
- If neither exists, create a root `CONTEXT.md` lazily when the first term is resolved

### How the System Avoids Duplicating or Conflicting Context

Several mechanisms prevent duplication and conflict:

1. **The glossary is opinionated**: Each term has exactly one canonical name with explicit "Avoid" aliases. This prevents the same concept from being added under multiple names.

2. **Flagged ambiguities section**: When a term is used ambiguously, it's flagged in CONTEXT.md with a clear resolution. This prevents drift.

3. **Challenge against the glossary**: When the user uses a term conflicting with existing language, the agent calls it out: "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

4. **Cross-reference with code**: The agent checks whether the code agrees with the user's statements and surfaces contradictions.

5. **ADR numbering**: ADRs use sequential numbering, and the instruction says "scan `docs/adr/` for the highest existing number and increment by one."

6. **ADR conflict flagging**: When an output contradicts an existing ADR, skills are instructed to surface it explicitly rather than silently override.

7. **Lazy creation**: Files are only created when there's content to write, preventing empty shell files that might confuse later sessions.

## Incremental Building

### How Context Grows Over Time

The context builds incrementally through multiple sessions:

1. **First `/setup-matt-pocock-skills` run**: Creates `docs/agents/domain.md` and the `## Agent skills` block. No CONTEXT.md or ADRs yet.

2. **First `/grill-with-docs` invocation**: When the first term is resolved, `CONTEXT.md` is created. When the first ADR-worthy decision crystallizes, `docs/adr/` is created. Each subsequent term and ADR is added to the respective files.

3. **Subsequent `/grill-with-docs` sessions**: The agent reads the existing `CONTEXT.md`, challenges new terminology against it, and adds new terms or updates existing ones inline.

4. **`/improve-codebase-architecture` sessions**: These also read and update `CONTEXT.md`, adding terms when new deepened modules are named, and updating fuzzy terms.

5. **`/triage` sessions**: Can trigger `/grill-with-docs` during step 4 ("Grill if needed"), which feeds back into context building.

### How the System Decides What New Information to Add

The system does NOT automatically decide what to add. It is driven by human interaction:

- **Terms are added when they are resolved** during a grilling session. The user and agent discuss, reach agreement on a canonical term, and the agent writes it immediately.
- **ADRs are offered only when all three criteria are met** (hard to reverse, surprising, real trade-off). The agent proposes them; the user decides whether to create them.
- **`CONTEXT.md` is updated when terminology is sharpened** — if a fuzzy term becomes precise during conversation, it's updated inline.

### How It Handles Changes to Existing Context

- **Term updates**: If understanding evolves, the definition can be updated. The `/improve-codebase-architecture` skill explicitly says "When sharpening a fuzzy term during the conversation? Update `CONTEXT.md` right there."
- **Ambiguity resolution**: Contradictions or ambiguities are flagged in the "Flagged ambiguities" section with their resolution.
- **ADR conflicts**: If a new proposal contradicts an existing ADR, it must be flagged explicitly (e.g., "_contradicts ADR-0007 — but worth reopening because..._"). ADRs are not silently overridden.
- **ADR supersession**: ADRs can have a `Status: superseded by ADR-NNNN` frontmatter if a later decision replaces them.

### The Deprecated Approach vs Current Approach

The deprecated `/ubiquitous-language` skill had an explicit re-running mechanism:
1. Read existing `UBIQUITOUS_LANGUAGE.md`
2. Incorporate any new terms from subsequent discussion
3. Update definitions if understanding has evolved
4. Re-flag any new ambiguities
5. Rewrite the example dialogue to incorporate new terms

The current approach (`/grill-with-docs`) is more organic — it updates inline during conversation rather than requiring a separate "re-extract" step.

## Configuration

The context-building behavior is controlled by several configuration points:

### `/setup-matt-pocock-skills` Configuration

The primary configuration skill. It creates three files:

1. **`docs/agents/issue-tracker.md`** — Which issue tracker to use (GitHub, GitLab, Local, or custom)
2. **`docs/agents/triage-labels.md`** — Maps 5 canonical triage roles to actual label strings
3. **`docs/agents/domain.md`** — Domain doc consumer rules and layout (single-context vs multi-context)

plus an `## Agent skills` section in `CLAUDE.md` or `AGENTS.md` that points to these files.

### `CLAUDE.md` / `AGENTS.md` Entry Point

The `## Agent skills` block written by setup is what agent sessions read at the start. It contains:
- Issue tracker reference
- Triage labels reference
- Domain docs reference (single or multi-context layout)

### Single vs Multi-Context Choice

During setup, the user chooses between:
- **Single-context**: One `CONTEXT.md` + `docs/adr/` at repo root (most repos)
- **Multi-context**: `CONTEXT-MAP.md` at root pointing to per-context `CONTEXT.md` files (for monorepos)

This choice affects how all skills locate and read context.

### Hard vs Soft Dependency Configuration

ADR 0001 documents the split between skills:
- **Hard dependency** (`to-issues`, `to-prd`, `triage`) — include explicit "should have been provided to you — run `/setup-matt-pocock-skills` if not" wording
- **Soft dependency** (`diagnose`, `tdd`, `improve-codebase-architecture`, `zoom-out`) — reference domain docs in "vague prose only"; they degrade gracefully without setup

### `CLAUDE.md` at the Repository Root

The repo's own `CLAUDE.md` contains project-level instructions about how the skills repo itself is organized (bucket folders, README references, plugin.json entries). This is not about the context-building feature per se but shows how Claude Code instructions work.

### No External Configuration Files

There are no JSON/YAML config files for the context-building feature. All configuration is embedded in the skill markdown files and the `docs/agents/` markdown files. The configuration is plain markdown that the agent reads and interprets.

## Complete File Reference

### Core Context-Building Files (Producers)

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/SKILL.md` | Primary context-building skill. Defines the grilling session behavior, domain awareness, glossary challenge, inline CONTEXT.md updates, and ADR creation triggers. |
| `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md` | Defines the canonical structure and rules for CONTEXT.md files: sections, formatting, single vs multi-context repos, and content guidelines. |
| `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/ADR-FORMAT.md` | Defines the canonical structure for ADR files: minimal template, optional sections, numbering scheme, three-criteria test for when to offer an ADR, and examples of what qualifies. |
| `/home/codey/Dev/pocock-skills/skills/engineering/improve-codebase-architecture/SKILL.md` | Secondary context-building skill. Finds architectural deepening opportunities, reads CONTEXT.md and ADRs, updates CONTEXT.md inline when naming new modules or sharpening terms, offers ADRs for rejected candidates. |
| `/home/codey/Dev/pocock-skills/skills/engineering/improve-codebase-architecture/LANGUAGE.md` | Architecture-specific vocabulary definitions (module, interface, implementation, depth, seam, adapter, leverage, locality) used by improve-codebase-architecture. |
| `/home/codey/Dev/pocock-skills/skills/engineering/improve-codebase-architecture/INTERFACE-DESIGN.md` | Process for designing interfaces using parallel sub-agents ("Design It Twice" approach). |
| `/home/codey/Dev/pocock-skills/skills/engineering/improve-codebase-architecture/DEEPENING.md` | How to classify dependencies and deepen modules safely. |

### Setup/Configuration Files

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/SKILL.md` | Setup skill that scaffolds per-repo configuration: issue tracker, triage labels, and domain doc layout. Must be run before other engineering skills. |
| `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/domain.md` | Seed template for `docs/agents/domain.md`. Defines how skills should consume domain docs: read CONTEXT.md (or CONTEXT-MAP.md), read ADRs, use glossary vocabulary, flag ADR conflicts. |
| `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md` | Seed template for `docs/agents/issue-tracker.md` when using GitHub. |
| `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md` | Seed template for `docs/agents/issue-tracker.md` when using GitLab. |
| `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md` | Seed template for `docs/agents/issue-tracker.md` when using local markdown files. |
| `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/triage-labels.md` | Seed template for `docs/agents/triage-labels.md`. Maps 5 canonical triage roles to actual label strings. |

### Context Consumers (Skills That Read CONTEXT.md/ADRs)

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/skills/engineering/tdd/SKILL.md` | Uses domain glossary vocabulary in test names and interface design; respects ADRs. |
| `/home/codey/Dev/pocock-skills/skills/engineering/diagnose/SKILL.md` | Uses domain glossary for mental model of modules; checks ADRs in the area being worked on. |
| `/home/codey/Dev/pocock-skills/skills/engineering/zoom-out/SKILL.md` | Instructs agent to use "the project's domain glossary vocabulary" when giving broader context. |
| `/home/codey/Dev/pocock-skills/skills/engineering/to-issues/SKILL.md` | Uses domain glossary vocabulary in issue titles and descriptions; respects ADRs. |
| `/home/codey/Dev/pocock-skills/skills/engineering/to-prd/SKILL.md` | Uses domain glossary vocabulary throughout the PRD; respects ADRs. |
| `/home/codey/Dev/pocock-skills/skills/engineering/triage/SKILL.md` | Explores codebase using domain glossary; respects ADRs; can trigger `/grill-with-docs` during triage. |

### Context-Related Files in the Repo Itself

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/CONTEXT.md` | The repo's own domain glossary, defining Issue tracker, Issue, and Triage role with flagged ambiguities. |
| `/home/codey/Dev/pocock-skills/docs/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md` | The repo's own ADR documenting the hard/soft dependency split for setup pointers. |
| `/home/codey/Dev/pocock-skills/CLAUDE.md` | Repo-level instructions about skill organization. Not directly about context-building, but shows the CLAUDE.md pattern. |

### Deprecated/Superseded Context Files

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/skills/deprecated/ubiquitous-language/SKILL.md` | Earlier version of the context-building feature. Wrote to `UBIQUITOUS_LANGUAGE.md` using table format. Deprecated in favor of `/grill-with-docs` inline approach. |
| `/home/codey/Dev/pocock-skills/skills/deprecated/qa/SKILL.md` | Referenced `UBIQUITOUS_LANGUAGE.md` (old naming for CONTEXT.md). |

### Infrastructure Files

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/.claude-plugin/plugin.json` | Plugin manifest listing all active skills. Used by Claude Code for skill discovery. |
| `/home/codey/Dev/pocock-skills/scripts/list-skills.sh` | Lists all skill directories (finds all SKILL.md files). |
| `/home/codey/Dev/pocock-skills/scripts/link-skills.sh` | Symlinks all skills to `~/.claude/skills` for local development use. |
| `/home/codey/Dev/pocock-skills/README.md` | Top-level documentation including the context-building feature explanation. |

### Context-Adjacent Files

| Path | Description |
|------|-------------|
| `/home/codey/Dev/pocock-skills/skills/engineering/triage/AGENT-BRIEF.md` | Defines how to write agent briefs for `ready-for-agent` issues. Not directly about context-building but uses context vocabulary in briefs. |
| `/home/codey/Dev/pocock-skills/skills/engineering/triage/OUT-OF-SCOPE.md` | Defines `.out-of-scope/` directory for rejected feature requests. A form of persistent context (institutional memory), but separate from CONTEXT.md/ADR system. |
| `/home/codey/Dev/pocock-skills/.out-of-scope/setup-skill-verify-mode.md` | Example of an out-of-scope file in this repo (rejected feature request). |
| `/home/codey/Dev/pocock-skills/.out-of-scope/mainstream-issue-trackers-only.md` | Another out-of-scope file (rejected feature request about niche issue trackers). |
| `/home/codey/Dev/pocock-skills/skills/productivity/grill-me/SKILL.md` | The non-docs version of grilling. No context-building — just interviews without updating CONTEXT.md or creating ADRs. |
| `/home/codey/Dev/pocock-skills/skills/engineering/tdd/tests.md` | TDD supporting reference about good vs bad tests. |
| `/home/codey/Dev/pocock-skills/skills/engineering/tdd/mocking.md` | TDD supporting reference about when to mock. |
| `/home/codey/Dev/pocock-skills/skills/engineering/tdd/deep-modules.md` | TDD supporting reference about deep modules. |
| `/home/codey/Dev/pocock-skills/skills/engineering/tdd/refactoring.md` | TDD supporting reference about refactor candidates. |
| `/home/codey/Dev/pocock-skills/skills/engineering/tdd/interface-design.md` | TDD supporting reference about interface design for testability. |

## Open Questions / Ambiguities

1. **Merge conflict handling**: There is no explicit mechanism for handling merge conflicts in `CONTEXT.md` when multiple sessions update it concurrently. Since updates are inline and not structured data, this could lead to conflicts in team environments.

2. **Version control integration**: The system treats `CONTEXT.md` and ADRs as ordinary files in the repo. There's no explicit guidance about commit practices — should you commit each term addition separately? Each ADR in its own commit? The system doesn't specify.

3. **CONTEXT.md staleness**: There's no mechanism for detecting when `CONTEXT.md` becomes stale. The deprecated `/ubiquitous-language` skill had an explicit re-running mechanism (read existing, incorporate new, update), but the current approach relies on the `/grill-with-docs` skill being invoked again. If no one runs grilling sessions for a while, the glossary could drift from the codebase.

4. **ADR update/amendment**: ADRs have an optional `Status` field that can be `superseded by ADR-NNNN`, but there's no explicit process for this. When does an ADR get superseded? Who decides? How is this communicated outside of reading the ADR itself?

5. **Multi-context detection**: The system infers multi-context mode by the presence of `CONTEXT-MAP.md`. But what happens if someone creates a `CONTEXT-MAP.md` after a `CONTEXT.md` already exists at the root? The migration path isn't documented.

6. **Relationship between `/grill-with-docs` and `/grill-me`**: The `grill-me` skill is described as "same as grill-me but adds more goodies" in the README. But `grill-me` doesn't reference or update CONTEXT.md at all — it's a pure interview skill. The README's phrasing could be confusing; `grill-with-docs` is more than just `grill-me` + goodies.

7. **`domain.md` consumer rules propagation**: The consumer rules in `domain.md` are created once by `/setup-matt-pocock-skills`. If the grill-with-docs skill changes its CONTEXT.md format or adds new sections, how do existing `domain.md` files get updated? There's no migration path documented. The `.out-of-scope/setup-skill-verify-mode.md` actually addresses this — the stance is that verification should be done by re-running setup and telling it to check existing files.

8. **The `proceed silently` instruction for missing context**: Consumer skills are told to "proceed silently" if CONTEXT.md or ADRs don't exist. This is sensible for avoiding noise, but it means a skill might produce suboptimal output without the user realizing CONTEXT.md is missing. There's no gentle nudge like "No CONTEXT.md found — consider running /grill-with-docs."

9. **Drift between CONTEXT.md and code**: There's no automated mechanism to detect when the codebase uses terms not in CONTEXT.md, or when CONTEXT.md defines terms that no longer exist in the code. The deprecated `/ubiquitous-language` skill had some of this via "scan the conversation" but the current approach is purely conversational.

10. **`CONTEXT-MAP.md` context selection**: When multiple contexts exist, the `/grill-with-docs` skill says "infer which one the current topic relates to. If unclear, ask." But there's no documented heuristic for how to make this inference.

11. **Template vs. actual files**: The seed templates in `setup-matt-pocock-skills/` (domain.md, triage-labels.md, etc.) are templates that get customized per-repo. But there's no versioning or update mechanism. If the templates change in a future version of pocock-skills, existing repos won't automatically get the updates.

12. **`docs/agents/` vs skill-consumed path**: The `domain.md` consumer template says to read `CONTEXT.md` at the repo root (or `CONTEXT-MAP.md`), but some skills also directly reference `CONTEXT.md` in their instructions. Is there a risk of the two paths diverging? The `domain.md` template is the canonical one, but the skills also hardcode the path in their SKILL.md files.
