# Implementation Plan: Context System

> Source: Research findings from Pocock Skills and OpenAgents Control comparative analysis
> Decision Snapshot: See decisions below

## Architectural Decisions

Durable decisions that apply across all phases:

- **File structure**: All context files in `.context/` at project root. Monorepo sub-projects as subdirectories within it.
- **Splitting axis**: 2-3 files per context (vocabulary, patterns, decisions). Not by knowledge type (OpenAgents) or single file (Pocock).
- **Index/navigation**: Light structure with version frontmatter. Not OpenAgents-heavy navigation hierarchy.
- **Monorepo support**: Day one via CONTEXT-MAP.md pointing to bounded context subdirectories.
- **Creation approach**: Both lazy and initial-context-grill available from day one.
- **Creation trigger**: Skills propose, context skill writes. Organic discovery with authoritative writing.
- **Patterns location**: In context system (PATTERNS.md), not AGENTS.md.
- **ADR quality gate**: Pocock's 3-criteria test (hard to reverse + surprising + real trade-off).
- **Version tracking**: `<!-- Version: X.Y | Updated: YYYY-MM-DD -->` light frontmatter on all context files.
- **Missing context**: Proceed silently (Pocock's approach). Don't complain, just work without context.
- **Skill format**: `SKILL.md` + optional `references/` directory, matching existing skill system at `/home/codey/Dev/skills/`.
- **Context consumption model**: Skills do NOT read context files directly. Instead, skills invoke `/discover-context` as a first step, which returns only task-relevant context. This keeps token cost proportional to task relevance, not project size.

---

## Phase Index

| Phase | Title | Description | User Stories | Depends On | Document |
|-------|-------|------------|-------------|------------|----------|
| 1 | Core Context System | CONTEXT.md + ADRs + `/discover-context` skill + `/context-grill` skill + consuming skills using discovery | US1, US2, US11, US12 | — | [Phase 1](PHASE-context-system-1-core.md) |
| 2 | Patterns and Bootstrapping | PATTERNS.md + `/initial-context-grill` | US3, US4 | Phase 1 | [Phase 2](PHASE-context-system-2-patterns.md) |
| 3 | Context Proposals | Skills propose context additions during regular work | US5, US6 | Phase 1 | [Phase 3](PHASE-context-system-3-proposals.md) |
| 4 | Monorepo Support | Bounded contexts with CONTEXT-MAP.md | US7, US8 | Phase 1, 2 | [Phase 4](PHASE-context-system-4-monorepo.md) |
| 5 | Context Review | Staleness detection and maintenance | US9, US10 | Phase 1, 2 | [Phase 5](PHASE-context-system-5-review.md) |

---

## User Stories

1. US1: As a developer, I can invoke `/context-grill` on a project with no context and have a conversational session that produces `.context/CONTEXT.md` with domain vocabulary.
2. US2: As a developer, other skills (tdd, to-prd, to-plan, etc.) use `/discover-context` to load task-relevant vocabulary and apply it in their output.
3. US3: As a developer starting on a new project, I can invoke `/initial-context-grill` to bootstrap both CONTEXT.md and PATTERNS.md through a focused conversational session.
4. US4: As a developer, skills follow my project's coding patterns (from PATTERNS.md) in their output.
5. US5: As a developer working on a feature, the TDD skill notices a naming pattern not in CONTEXT.md and proposes adding it.
6. US6: As a developer, I can address proposals in my next `/context-grill` session.
7. US7: As a developer on a monorepo, each bounded context gets its own CONTEXT.md, PATTERNS.md, and ADRs.
8. US8: As a developer, skills automatically find the right context for my current work area via CONTEXT-MAP.md.
9. US9: As a developer, I can see when my context was last reviewed and identify stale sections.
10. US10: As a developer, I can run `/context-review` to get proposals for updating outdated context.
11. US11: As a developer, consuming skills load only task-relevant context, keeping token cost low regardless of project size.
12. US12: As a developer, I can invoke `/discover-context` directly to preview what context would be loaded for a given task description.

---

## File Structure (Final Design)

### Single-context repo

```
project-root/
  .context/
    CONTEXT.md            # Domain vocabulary
    PATTERNS.md           # Tech stack, coding patterns, naming conventions
    adr/
      0001-slug.md        # Architecture Decision Records
```

### Monorepo

```
project-root/
  .context/
    CONTEXT-MAP.md        # Lists bounded contexts and their relationships
    PATTERNS.md           # Shared/cross-cutting patterns (global)
    adr/                  # Cross-cutting decisions (global)
      0001-slug.md
    ordering/             # Bounded context subdirectory
      CONTEXT.md
      PATTERNS.md         # Only if diverging from root PATTERNS.md
      adr/
    billing/
      CONTEXT.md
      PATTERNS.md
      adr/
```

### CONTEXT.md Format

```markdown
<!-- Version: 1.3 | Updated: 2026-05-04 -->
# Ordering

Language for the ordering bounded context.

## Language

**Order**: A customer's request for products.
_Avoid_: Purchase, transaction

**Fulfillment**: The process of preparing and shipping an Order.
_Avoid_: Delivery, shipment

## Relationships

- An **Order** produces one or more **Invoices**
- A **Fulfillment** belongs to exactly one **Order**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — resolved: these are distinct.
```

### PATTERNS.md Format

```markdown
<!-- Version: 1.1 | Updated: 2026-05-04 -->
# Ordering Patterns

Tech stack, conventions, and patterns for the ordering context.

## Tech Stack

- Runtime: Kotlin 1.9 on JVM 21
- Framework: Spring Boot 3.2
- Database: PostgreSQL 16 via Exposed
- Serialization: Jackson (module: kotlin, features: FAIL_ON_UNKNOWN_PROPERTIES)
- Testing: JUnit 5 + Strikt (assertions) + Testcontainers (integration)

## Coding Patterns

- **Repository pattern**: Domain logic lives in service classes; data access through repository interfaces. Services use repositories, never direct DB calls.
- **Error handling**: Domain errors use sealed class hierarchies. API errors use RFC 7807 Problem Details.
- **Null safety**: Use Kotlin's type system. Prefer `Require<NotNull>` over `!!`. Use `Result<>` for operations that can fail.
- **Testing**: Unit tests for domain logic, integration tests with Testcontainers for repos. No mocks for repositories — use fakes.

## Naming Conventions

- Files: PascalCase for classes, camelCase for functions
- Database: snake_case for tables and columns
- API: kebab-case for URLs, camelCase for JSON

## Key Decisions

- See ADR-0002 for why we chose Exposed over Hibernate
- See ADR-0003 for our error handling strategy
```

### ADR Format

```markdown
<!-- Version: 1.0 | Updated: 2026-03-15 -->
# Use Exposed for Database Access

We use JetBrains Exposed as our ORM instead of Hibernate. Exposed is Kotlin-first,
type-safe, and has lower overhead for our query patterns. Hibernate's session model
adds complexity we don't need since we don't have complex object graphs.

## Considered Options

- **Hibernate**: Full ORM, mature, but heavy and Java-centric
- **Exposed**: Lightweight, Kotlin DSL, type-safe queries
- **Raw SQL**: Maximum control, no type safety

## Status: accepted
```

### CONTEXT-MAP.md Format (Monorepos)

```markdown
<!-- Version: 1.0 | Updated: 2026-05-04 -->
# Context Map

## Contexts

- [Ordering](./ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./billing/CONTEXT.md) — generates invoices and processes payments

## Relationships

- **Ordering → Billing**: Ordering emits `OrderPlaced` events; Billing consumes them
```

### Version Tracking Rules

- `<!-- Version: X.Y | Updated: YYYY-MM-DD -->` on CONTEXT.md, PATTERNS.md, and each ADR
- New file = 1.0
- Content update (term added, pattern updated) = MINOR (1.0 → 1.1)
- Structure change (sections reorganized) = MAJOR (1.0 → 2.0)
- Typo fix = PATCH (not tracked in version, just fix)

### Context Consumption Model

Skills do NOT read context files directly. Instead, they invoke `/discover-context` as a first step.

**Why a discovery skill?**

At scale, a mature project might have:
- CONTEXT.md: ~150 lines (~750 tokens)
- PATTERNS.md: ~300 lines (~1500 tokens)
- 25 ADRs: ~500 lines (~2500 tokens)
- Total: ~4750 tokens loaded per skill invocation — before the skill even starts

Reading all context on every invocation makes token cost proportional to project size, not task relevance. The discovery skill makes token cost proportional to what's actually needed for the current task.

**`/discover-context` workflow:**

1. Skill invokes `/discover-context` with a description of the current task
2. `/discover-context` reads `.context/CONTEXT-MAP.md` (if monorepo) to identify the relevant bounded context
3. Scans CONTEXT.md headings/terms for vocabulary related to the task
4. Scans PATTERNS.md sections for patterns related to the task
5. Scans ADR titles for decisions related to the task
6. Returns a compact summary of relevant context (~500-800 tokens instead of ~4750)
7. If `.context/` doesn't exist, returns nothing — skill proceeds silently

**Which skills invoke `/discover-context`:**

| Skill | Invokes discovery? | Uses what context? |
|-------|---------------------|-------------------|
| `/context-grill` | No (reads + writes all context) | Full context (it's creating/updating) |
| `/initial-context-grill` | No (reads + writes all context) | Full context (it's creating) |
| `/discover-context` | N/A (it IS the discovery) | All context (to select relevant) |
| `tdd` | Yes | Relevant vocabulary + patterns + ADRs |
| `to-prd` | Yes | Relevant vocabulary + ADRs |
| `to-plan` | Yes | Relevant vocabulary + ADRs |
| `grill-me` | No | No context needed (pure interview) |
| `code-doc` | Yes | Relevant vocabulary + patterns |

**Skill instruction pattern (for consuming skills):**

Each consuming skill includes this in its SKILL.md:

> Before starting work, invoke `/discover-context` with a brief description of this task. Use the returned context vocabulary in your output and follow any patterns provided. If no context is returned, proceed without it — do not flag its absence.

This replaces per-skill "read CONTEXT.md" instructions with a single, consistent entry point.

### ADR Quality Gate (3-Criteria Test)

Only offer an ADR when ALL THREE are true:
1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives, and you picked one for specific reasons

If any of the three is missing, skip the ADR.

---

## Why No `domain.md` Equivalent

Pocock's system creates a per-repo `docs/agents/domain.md` file with static consumer rules telling skills where to find context and how to behave. Our system doesn't need this because:

1. **Fixed paths replace path configuration**: Pocock needs `domain.md` because it has to tell skills "read CONTEXT.md at the repo root, or CONTEXT-MAP.md if it exists." Our system has a single canonical path (`.context/`) — no per-repo configuration needed.

2. **The discovery skill replaces static consumer rules**: Instead of every skill having duplicated instructions like "read CONTEXT.md, read ADRs, use vocabulary," each skill simply invokes `/discover-context`. The discovery skill is the single authoritative source for how context is loaded and filtered. Update it once, all consuming skills benefit.

3. **Lazy creation replaces setup**: Pocock needs `/setup-matt-pocock-skills` to create `domain.md` before other skills can consume context. Our system creates `.context/` lazily when the first grilling session writes to it. No setup step required.