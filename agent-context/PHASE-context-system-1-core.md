# Phase 1: Core Context System

> Source Plan: [PLAN-context-system.md](IMPLEMENTATION-PLAN.md)
> Source Research: [Pocock Skills](../pocock-skills/01-broad-exploration.md) and [OpenAgents Control](../openagents/01-broad-exploration.md)

## User Stories

- US1: As a developer, I can invoke `/context-grill` on a project with no context and have a conversational session that produces `.context/CONTEXT.md` with domain vocabulary.
- US2: As a developer, other skills use `/discover-context` to load task-relevant vocabulary and apply it in their output.
- US11: As a developer, consuming skills load only task-relevant context, keeping token cost low regardless of project size.
- US12: As a developer, I can invoke `/discover-context` directly to preview what context would be loaded for a given task description.

## What to Build

The minimum end-to-end slice: a user can grill a project to produce a domain vocabulary (CONTEXT.md), optionally create ADRs, and other skills can discover and use that context without loading entire files.

### Deliverables

#### 1. `/context-grill` Skill

Location: `skills/context-grill/SKILL.md` + `skills/context-grill/references/`

The primary context-building skill. A conversational grilling session that:

- Discovers existing context: checks for `.context/CONTEXT.md`, `.context/CONTEXT-MAP.md` (monorepo), and `.context/adr/`
- If no context exists, creates `.context/CONTEXT.md` lazily when the first term is resolved
- Challenges user terminology against existing glossary
- Proposes canonical terms when the user is vague
- Updates CONTEXT.md inline as terms are resolved (not batched)
- Offers ADRs sparingly (3-criteria test: hard to reverse, surprising, real trade-off)
- Creates `.context/adr/` directory and ADR files lazily
- For monorepos: infers which bounded context relates to the current topic, offers to create per-context CONTEXT.md files

References to include:
- `references/CONTEXT-FORMAT.md` — The canonical structure and rules for CONTEXT.md files (sections, formatting, single vs multi-context, content guidelines)
- `references/ADR-FORMAT.md` — The canonical structure for ADR files (minimal template, numbering, 3-criteria test, qualifying decisions)

#### 2. `/discover-context` Skill

Location: `skills/discover-context/SKILL.md`

The context discovery skill that other skills invoke as step 1. It:

- Takes a task description as input (the current task the calling skill is working on)
- Checks if `.context/` directory exists — if not, returns nothing
- For monorepos: reads `.context/CONTEXT-MAP.md` to identify which bounded context(s) relate to the task
- Reads `.context/CONTEXT.md` (or the relevant bounded context's CONTEXT.md) and selects vocabulary relevant to the task
- Scans PATTERNS.md section headings for relevant patterns (Phase 2 — in Phase 1, PATTERNS.md doesn't exist yet, but the skill should handle its absence gracefully)
- Scans `.context/adr/` titles for decisions relevant to the task
- Returns a compact summary of relevant context (~500-800 tokens)
- If no relevant context is found, returns nothing — the calling skill proceeds silently

The skill should be designed so that its output is structured for easy consumption by other skills:

```
## Task-Relevant Context

### Vocabulary
- **Order**: A customer's request for products. (Avoid: Purchase, transaction)
- **Fulfillment**: The process of preparing and shipping an Order. (Avoid: Delivery, shipment)

### Relationships
- An Order produces one or more Invoices

### Relevant Decisions
- ADR-0003: Use Exposed for database access (relates to: data layer patterns)

### No Relevant Patterns
(PATTERNS.md not found in this project)
```

#### 3. Update Existing Skills to Use Discovery

Update the following existing skills to invoke `/discover-context` as step 1:
- `tdd/SKILL.md` — Add: "Before starting work, invoke `/discover-context` with a brief description of the feature being tested. Use the returned context vocabulary in test names and interface design. Follow any patterns provided. If no context is returned, proceed without it."
- `to-prd/SKILL.md` — Same pattern, adapted for PRD writing
- `to-plan/SKILL.md` — Same pattern, adapted for planning
- `code-doc/SKILL.md` — Same pattern, adapted for documentation
- `grill-me/SKILL.md` — Does NOT need context discovery (pure interview, no domain work)

#### 4. CONTEXT.md and ADR Format Specifications

These are reference documents that `/context-grill` uses to write files correctly:

- `skills/context-grill/references/CONTEXT-FORMAT.md` — Based on Pocock's format but adapted for `.context/` directory structure and version frontmatter
- `skills/context-grill/references/ADR-FORMAT.md` — Based on Pocock's format with version frontmatter added

### What is NOT in Phase 1

- PATTERNS.md (Phase 2)
- `/initial-context-grill` (Phase 2)
- Context proposals from other skills (Phase 3)
- Monorepo support via CONTEXT-MAP.md (Phase 4)
- Context review / staleness detection (Phase 5)

## Acceptance Criteria

- [ ] Invoking `/context-grill` on a project with no `.context/` directory creates `.context/CONTEXT.md` with correct format and version frontmatter
- [ ] Invoking `/context-grill` on a project with existing `.context/CONTEXT.md` reads it, challenges terminology, and updates it inline
- [ ] The grilling session produces domain vocabulary with canonical terms, avoid-lists, relationships, and example dialogue
- [ ] ADRs are offered only when the 3-criteria test is met, with correct sequential numbering
- [ ] ADRs are created in `.context/adr/` with version frontmatter
- [ ] Invoking `/discover-context "implementing user authentication"` on a project with CONTEXT.md + ADRs returns only task-relevant context (~500-800 tokens)
- [ ] Invoking `/discover-context "anything"` on a project with no `.context/` directory returns nothing and the calling skill proceeds silently
- [ ] Existing skills (tdd, to-prd, to-plan) invoke `/discover-context` as step 1 and use returned vocabulary in their output
- [ ] Version frontmatter is correctly set to `1.0` on new files and incremented on updates

## Dependencies

- **Depends on**: None (this is Phase 1)
- **Blocks**: Phase 2 (Patterns and Bootstrapping), Phase 3 (Context Proposals), Phase 4 (Monorepo Support), Phase 5 (Context Review)