# Comparative Report: Project Context/Knowledge Building Feature

## Two Approaches to the Same Problem

**Pocock Skills** and **OpenAgents Control** both solve the same fundamental problem: enabling an AI coding agent to slowly, over time, learn, build, and persist an understanding of the project it is working in. They approach this problem from radically different angles, with different philosophies, scopes, and trade-offs.

---

## 1. Feature Overview

### What Problem Both Solve

When an AI agent works in a codebase, it has no memory between sessions. Every new session starts from scratch. Both systems address this by creating persistent, structured knowledge artifacts that the agent can read at the start of each session to regain project understanding.

### Pocock Skills Approach: Domain Language + Decision Records

Pocock's approach is **minimal and language-centric**. The core idea is that the biggest source of misunderstanding between humans and AI is terminology. If you can nail down the exact vocabulary of the domain - which words mean which things, which words to avoid, and how terms relate - then every downstream skill (TDD, diagnosis, PRD writing, triage) becomes more effective.

The system produces two artifacts:
1. **`CONTEXT.md`** — A domain glossary defining canonical terms, their definitions, terms to avoid, relationships, example dialogues, and flagged ambiguities
2. **ADRs** — Lightweight Architecture Decision Records capturing hard-to-reverse, surprising, trade-off-laden decisions

The philosophy is: **Be opinionated. Pick the best word. Flag conflicts explicitly. Keep definitions tight.** A CONTEXT.md for a typical project might be 30-80 lines.

### OpenAgents Control Approach: Multi-Layered Project Intelligence

OpenAgents' approach is **comprehensive and system-centric**. The core idea is that an agent needs many different kinds of knowledge to work effectively: not just domain vocabulary, but coding patterns, tech stack details, architecture decisions, business context, error solutions, and much more.

The system produces a **hierarchical tree of context files**:
1. **`navigation.md`** — A canonical index at every level that agents traverse to discover relevant context
2. **Project Intelligence files** — `technical-domain.md`, `business-domain.md`, `business-tech-bridge.md`, `decisions-log.md`, `living-notes.md`
3. **Core standards** — Code quality, security patterns, test coverage, documentation standards
4. **Category-specific context** — Development, UI, data, product, learning, content-creation categories
5. **`CODEBASE_STANDARDS.md`** — Detailed code-level patterns (2000+ lines for a specific codebase)

The philosophy is: **Load the right context at the right time. Keep each file under 200 lines (MVI principle). Let agents discover what they need via navigation.**

---

## 2. Architecture Comparison

### Scope and Complexity

| Dimension | Pocock Skills | OpenAgents Control |
|-----------|--------------|-------------------|
| **Files created for context** | 1-2 (CONTEXT.md + ADRs) | 50+ (navigation tree + PI + core + categories) |
| **Total context file count** | ~3-10 (CONTEXT.md, ADRs, domain.md, issue-tracker.md, triage-labels.md) | ~80+ (full context tree) |
| **Lines of skill definition** | ~300 (grill-with-docs SKILL.md) | ~921 (add-context) + 861 (build-context-system) + 309 (context) + agent definitions |
| **Number of skills/commands involved** | 3 producers, 6 consumers, 1 setup | 2 primary commands, 10+ subcommands, 3+ agents, 2 skills |
| **Setup requirement** | `/setup-matt-pocock-skills` (5 min) | Multiple install paths, extensive initial context |
| **Learning curve** | Low (single skill, single file) | High (many commands, many file types, many agents) |

### Information Model

| Dimension | Pocock Skills | OpenAgents Control |
|-----------|--------------|-------------------|
| **Primary artifact** | `CONTEXT.md` (domain glossary) | `navigation.md` (discovery index) + `technical-domain.md` (patterns) |
| **Decision records** | ADRs (sequential numbered files) | `decisions-log.md` (structured entries in single file) |
| **Organizing principle** | Single flat file per context | Hierarchical navigation tree |
| **Discovery mechanism** | Read one file (or CONTEXT-MAP.md) | Traverse navigation.md hierarchy |
| **Scoping** | Single-context or multi-context (bounded contexts) | Category/function-based hierarchy |
| **Format strictness** | Opinionated but human-readable | Strict HTML frontmatter + MVI compliance + line limits |

### Context Building Flow

**Pocock Skills:**
```
User invokes /grill-with-docs
  → Agent reads existing CONTEXT.md (or infers structure)
  → Agent interviews user about plan/design
  → Agent challenges terminology against existing glossary
  → When term is resolved → immediately update CONTEXT.md
  → When significant decision surfaces → offer ADR (3-criteria test)
  → Repeat until user is satisfied
```

**OpenAgents Control:**
```
Multiple paths:
Path A: /add-context (interactive wizard)
  → 6 questions about tech stack, API patterns, components, naming, standards, security
  → Generate technical-domain.md + navigation.md
  → Validate against MVI rules (< 200 lines)
  → Confirm and write

Path B: /add-context --update (incremental update)
  → Detect existing context
  → Review each pattern section (Keep/Update/Remove)
  → Version bump (MINOR for content, MAJOR for structure)
  → Update navigation.md

Path C: Auto-discovery (ContextScout on every task)
  → Read navigation.md hierarchy
  → Find relevant context files by priority
  → Return ranked list to main agent

Path D: /context harvest (extract from session summaries)
  → 6 stages: Scan → Analyze → Approve → Extract → Cleanup → Report
  → Categorize by function (concepts, examples, guides, etc.)
  → MVI compress and write to permanent context

Path E: /build-context-system (full system creation)
  → 12-question interview
  → Domain type classification
  → Generate entire context tree
```

---

## 3. Detailed Feature Comparison

### 3.1 Context Discovery

**Pocock Skills — Explicit Read:**
- Consumer skills are told: "Before exploring, read CONTEXT.md at the repo root, or CONTEXT-MAP.md if it exists."
- If context files don't exist: "Proceed silently. Don't flag their absence."
- Single read at task start, no dynamic loading during task
- No ranking or prioritization — all context is loaded or none

**OpenAgents Control — Navigation-Driven Discovery:**
- ContextScout reads `navigation.md` hierarchy on every task (Stage 1.5)
- Files are ranked by priority: Critical (80% use cases) → High (15%) → Medium (4%) → Low (1%)
- Discovery is automatic and happens before every coding task
- ContextScout is read-only (cannot write, edit, or create files)
- Falls back to global context if local context is missing

**Comparison:**
| Aspect | Pocock | OpenAgents |
|--------|--------|------------|
| **Discovery timing** | Task start (manual) | Every task start (automatic) |
| **Granularity** | All or nothing | Ranked by priority |
| **Scope control** | None (single file) | Priority-based loading |
| **Auto-trigger** | No | Yes (ContextScout) |
| **Fallback** | Proceed silently | Global context fallback |

### 3.2 Context Creation

**Pocock Skills — Conversational/Lazy:**
- CONTEXT.md is created lazily when the first term is resolved
- No scaffolding step — the file appears organically
- Content is entirely driven by the user-agent conversation
- ADRs are created only when all three criteria are met (hard to reverse, surprising, real trade-off)
- The agent offers ADRs but the user decides

**OpenAgents Control — Interactive Wizard:**
- `/add-context` runs a 6-question wizard upfront
- Creates a structured `technical-domain.md` + `navigation.md` immediately
- Content is driven by both user answers and pattern detection
- All Project Intelligence files follow strict templates with frontmatter
- Version tracking from creation (1.0)
- Multiple creation paths: wizard, build-context-system, manual, harvest

**Comparison:**
| Aspect | Pocock | OpenAgents |
|--------|--------|------------|
| **Creation trigger** | Lazy (first term resolved) | Eager (6-question wizard) |
| **Initial investment** | Minimal (start grilling) | Moderate (answer 6 questions) |
| **Template strictness** | Opinionated guidelines | Strict templates with frontmatter |
| **What's created first** | Single term in CONTEXT.md | Full `technical-domain.md` + `navigation.md` |
| **Who decides content** | User + agent dialogue | User answers + agent generation |

### 3.3 Context Update

**Pocock Skills — Inline During Conversation:**
- Terms are updated immediately during grilling: "Don't batch these up — capture them as they happen."
- No version tracking — plain markdown, no frontmatter
- Ambiguities are flagged in a dedicated section with resolutions
- ADR conflicts must be flagged explicitly, never silently overridden
- No explicit update command — just invoke `/grill-with-docs` again

**OpenAgents Control — Multiple Update Mechanisms:**
- `/add-context --update`: Incremental review with Keep/Update/Remove for each section
- Version tracking: MINOR for content changes, MAJOR for structure changes, PATCH for typos
- `/context harvest`: Extract knowledge from session summaries
- `/context extract`: Extract from external docs/URLs
- `/context organize`: Restructure files
- `/context update for {topic}`: Targeted update for API changes
- Backup before replace, deprecation handling (`.deprecated.md`)
- Navigation.md must be updated when any file changes

**Comparison:**
| Aspect | Pocock | OpenAgents |
|--------|--------|------------|
| **Update model** | Inline during conversation | Dedicated update commands |
| **Version tracking** | None | Frontmatter Version: X.Y |
| **Change history** | Git only | Frontmatter Updated dates + backups |
| **Deprecation** | Not formalized | `.deprecated.md` with forward references |
| **Selective update** | Not applicable | `--tech-stack`, `--patterns` flags |
| **Harvest from sessions** | No | Yes (6-stage workflow) |

### 3.4 Context Consumption

**Pocock Skills — Fixed Consumer Rules:**
- `docs/agents/domain.md` (created by setup) contains consumer rules
- All consumer skills read CONTEXT.md and relevant ADRs
- Consumer skills are told to: use glossary vocabulary, flag ADR conflicts, note missing terms
- 6 consumer skills: `tdd`, `diagnose`, `to-issues`, `to-prd`, `triage`, `zoom-out`
- Consumption is passive — skills read what exists, proceed silently if nothing exists

**OpenAgents Control — Active Agent Discovery:**
- ContextScout discovers relevant context automatically on every task
- Priority-based ranking ensures most relevant context is loaded first
- OpenCoder/OpenAgent enforce context loading as a "critical requirement" (Tier 1)
- ExternalScout fetches live library documentation when external packages are detected
- All agents have strict XML rule blocks mandating context loading
- Navigation-driven: agents follow `navigation.md` → find relevant files → load by priority

**Comparison:**
| Aspect | Pocock | OpenAgents |
|--------|--------|------------|
| **Consumer count** | 6 skills | All agents (OpenCoder, OpenAgent, all subagents) |
| **Discovery** | Read one file | Navigate tree + rank |
| **Priority loading** | None | Critical → High → Medium → Low |
| **External docs** | No | Yes (Context7 API via ExternalScout) |
| **Missing context** | Proceed silently | Proceed without context, but flag |
| **Enforcement** | Soft (guidelines in domain.md) | Hard (Tier 1 critical requirement) |

### 3.5 Context Scope and Coverage

**Pocock Skills — Domain Vocabulary Focus:**
- CONTEXT.md covers: Term definitions, terms to avoid, relationships, example dialogue, flagged ambiguities
- ADRs cover: Hard-to-reverse, surprising, trade-off-laden architectural decisions
- Total scope: Domain language + architectural decisions
- What it intentionally excludes: Tech stack patterns, coding standards, error solutions, business logic, UI patterns
- Rationale: Other skills produce their own specialized artifacts (test specs, PRDs, etc.)

**OpenAgents Control — Full Project Intelligence:**
- `technical-domain.md`: Tech stack, API patterns, component patterns, naming conventions, code standards, security
- `business-domain.md`: Problem statement, target users, value proposition, business context
- `business-tech-bridge.md`: How business needs map to technical solutions
- `decisions-log.md`: Major decisions with rationale, alternatives, impact
- `living-notes.md`: Active issues, technical debt, open questions, patterns
- `CODEBASE_STANDARDS.md`: Detailed code-level patterns (2000+ lines)
- Core standards: Code quality, security, testing, documentation
- Plus: Development, UI, data, product, content-creation categories
- What it includes that Pocock excludes: Everything
- Rationale: Agents need comprehensive knowledge to generate consistent, project-aligned code

**Comparison:**
| Aspect | Pocock | OpenAgents |
|--------|--------|------------|
| **What it captures** | Domain language + decisions | Everything about the project |
| **Domain vocabulary** | Yes (primary focus) | Partially (in technical-domain) |
| **Tech stack patterns** | No | Yes (technical-domain) |
| **Business context** | No | Yes (business-domain) |
| **Code patterns** | No | Yes (CODEBASE_STANDARDS) |
| **Error solutions** | No | Yes (living-notes, `/context error`) |
| **External docs** | No | Yes (ExternalScout + Context7) |
| **Living notes** | No | Yes (active issues, debt, questions) |

### 3.6 File Organization

**Pocock Skills:**
```
project-root/
  CONTEXT.md                  # Domain glossary (or CONTEXT-MAP.md for multi-context)
  docs/
    adr/
      0001-slug.md            # Architecture Decision Records
      0002-slug.md
      ...
    agents/
      domain.md               # Consumer rules
      issue-tracker.md        # Issue tracker config
      triage-labels.md        # Triage label config
```

For multi-context repos:
```
project-root/
  CONTEXT-MAP.md              # Lists all contexts and their relationships
  src/
    ordering/
      CONTEXT.md              # Ordering context glossary
      docs/
        adr/
          0001-*.md           # Ordering-specific ADRs
    billing/
      CONTEXT.md              # Billing context glossary
      docs/
        adr/
          0001-*.md           # Billing-specific ADRs
```

**OpenAgents Control:**
```
.opencode/
  context/
    navigation.md                        # Root index
    CODEBASE_STANDARDS.md                 # Detailed code patterns
    project-intelligence/
      navigation.md                      # PI index
      technical-domain.md                # Tech stack & patterns
      business-domain.md                 # Business context
      business-tech-bridge.md            # Business ↔ tech mapping
      decisions-log.md                   # Decision records
      living-notes.md                    # Active issues & debt
    core/
      navigation.md
      standards/                         # 14+ standard files
      workflows/                          # Workflow definitions
      guides/                             # Step-by-step guides
      context-system/                     # Self-referential docs
        navigation.md
        standards/ (mvi, frontmatter, structure, templates, codebase-references)
        operations/ (harvest, extract, organize, update, migrate, error)
        guides/ (compact, creation, workflows, navigation-design, navigation-templates, organizing-context)
        examples/
    development/ navigation.md + content
    ui/                navigation.md + content
    data/              navigation.md + content
    product/           navigation.md + content
    content-creation/  navigation.md + content
    learning/          navigation.md + content
```

**Comparison:**
| Aspect | Pocock | OpenAgents |
|--------|--------|------------|
| **Total files** | 1-10 | 50-80+ |
| **Depth** | 1 level (flat) | 3+ levels (hierarchical) |
| **Discovery** | Read one file | Navigate tree |
| **Location** | Project root + `docs/` | `.opencode/context/` (hidden dir) |
| **Self-documentation** | Minimal | Extensive (context-system self-references) |
| **Multi-context** | CONTEXT-MAP.md + per-context dirs | Category/function-based hierarchy |

---

## 4. Strengths and Positives

### Pocock Skills Positives

1. **Radical simplicity**: A single CONTEXT.md file and a handful of ADRs. Anyone can understand the system in 5 minutes. No learning curve for the format, no templates to learn, no frontmatter to fill in.

2. **Conversational emergence**: Context is built naturally through the grilling conversation. The user doesn't need to answer a questionnaire or fill in templates. Terms appear in CONTEXT.md because they were actually discussed and agreed upon, not because a form required them.

3. **Opinionated vocabulary enforcement**: The `_Avoid_` convention is powerful. By listing synonyms to reject, it prevents the most common source of confusion: different people using different words for the same thing. This is the system's superpower.

4. **Lazy creation**: No scaffolding, no empty files, no boilerplate. CONTEXT.md only appears when there's actual content to write. This prevents the "blank file problem" where you create structure that never gets filled in.

5. **Inline updates**: Terms are updated as they're discussed, not batched. This means CONTEXT.md always reflects the current state of understanding during a session.

6. **ADRs with high bar**: The 3-criteria test (hard to reverse + surprising + real trade-off) prevents ADR proliferation. Most decisions don't need to be recorded, and the system explicitly says so.

7. **Low token cost**: Reading one small CONTEXT.md file is cheap. Even with ADRs, you're looking at maybe 100-200 lines total for most projects. This matters for every skill invocation.

8. **Graceful degradation**: Consumer skills proceed silently if CONTEXT.md doesn't exist. The system doesn't break or complain — it just works without the glossary, less effectively but still functional.

9. **Multi-context support**: The CONTEXT-MAP.md pattern for bounded contexts is elegant and follows DDD principles. Each context gets its own vocabulary, and the map shows how they relate.

10. **Example dialogue section**: Including actual example conversations in CONTEXT.md teaches both humans and AI how terms should be used in practice, not just what they mean.

### OpenAgents Control Positives

1. **Comprehensiveness**: Captures every aspect of project knowledge — not just vocabulary, but patterns, standards, business context, tech stack, security requirements, error solutions, and more. This gives agents a much richer understanding.

2. **Automatic discovery**: ContextScout runs on every task, automatically finding relevant context without the user needing to configure anything. This is a significant UX improvement over requiring manual skill invocations.

3. **Priority-based loading**: The Critical/High/Medium/Low system means agents load the most important context first, and can skip low-priority context when tokens are scarce. This is token-efficient.

4. **MVI principle**: The Minimal Viable Information standard (max 200 lines per file) prevents context bloat while still capturing essential knowledge. Each file must pass a "30-second scan" test.

5. **Multiple update paths**: Whether you want to do an interactive wizard (`/add-context`), extract from a session (`/context harvest`), update for a specific topic (`/context update for {topic}`), or manually edit, there's a path for every workflow.

6. **Navigation-first discovery**: The navigation.md hierarchy means agents don't need to know about all context files — they follow the tree to find what's relevant. This scales well to large projects with many categories.

7. **External documentation integration**: ExternalScout fetches live library documentation via the Context7 API, solving the problem of outdated training data for libraries. This is a capability Pocock's system simply doesn't have.

8. **Version tracking**: Each file has a version number and update date in frontmatter. This makes it possible to detect staleness and track when context was last reviewed.

9. **Deprecation handling**: Files are renamed `.deprecated.md` rather than deleted, with forward references to replacements. This preserves institutional memory.

10. **Self-documenting system**: The context system documents itself (`context-system/` contains standards, operations, guides, and examples for the context system). This meta-quality means the system can evolve its own documentation.

11. **Harvesting from sessions**: The ability to extract knowledge from AI-generated session summaries and turn them into permanent context is powerful. It means the system can learn from its own work.

12. **Backup before destructiveness**: `/add-context --replace-all` backs up to `.tmp/backup/` before replacing. This safety net prevents accidental context loss.

13. **Business-tech bridge**: The `business-tech-bridge.md` explicitly maps business needs to technical solutions, which is a capability that purely technical context systems lack.

---

## 5. Drawbacks and Weaknesses

### Pocock Skills Drawbacks

1. **Vocabulary-only scope**: CONTEXT.md captures domain vocabulary and ADRs capture decisions, but there's no mechanism for capturing coding patterns, tech stack specifics, error solutions, business context, or any of the other knowledge that makes an agent effective. Other skills must figure these out from scratch each session.

2. **Manual trigger requirement**: Context is only built when the user explicitly invokes `/grill-with-docs`. There's no automatic detection of "hey, we're using a term that's not in the glossary" or "this pattern keeps recurring." The system is entirely reactive.

3. **No automatic context consumption**: Consumer skills merely read CONTEXT.md if it exists. There's no ranking, no priority, no dynamic loading based on the task at hand. Every consumer loads the same file regardless of what they're doing.

4. **Staleness detection gap**: There's no mechanism to detect when CONTEXT.md has drifted from the codebase. If nobody runs `/grill-with-docs` for a while, the glossary becomes outdated with no warning.

5. **No version tracking**: CONTEXT.md has no version numbers, no update dates, no change history beyond git. There's no way to know if the glossary was last updated yesterday or six months ago.

6. **Merge conflict risk**: In a team environment, multiple people running `/grill-with-docs` and updating CONTEXT.md could create merge conflicts. The system has no conflict resolution mechanism.

7. **ADR proliferation prevention has no override**: The 3-criteria test is deliberately strict, but there's no way for a user to say "I want an ADR for this even though it doesn't meet all criteria." The system can only offer, not be requested.

8. **No external knowledge integration**: There's no equivalent of ExternalScout. The system can't fetch external library documentation, so it relies entirely on the LLM's training data.

9. **No harvesting mechanism**: Session learnings aren't automatically captured. Every session starts with the same static context, and any patterns discovered during the session are lost unless the user manually invokes `/grill-with-docs` and discusses them.

10. **Deprecation handling**: The only deprecation mechanism is ADR status (`superseded by ADR-NNNN`). There's no way to mark a term in CONTEXT.md as deprecated or to handle vocabulary evolution.

11. **No size management**: CONTEXT.md grows indefinitely as terms are added. There's no MVI principle, no compaction step, no way to identify and remove stale terms.

12. **Single-format rigidity**: Every term gets the same format: canonical name, definition, and avoid list. There's no way to capture different kinds of knowledge (patterns, decisions, errors) in different formats.

### OpenAgents Control Drawbacks

1. **Overwhelming complexity**: The system has 80+ files, 10+ commands, 3+ agents, and extensive self-referential documentation. The learning curve for a new user is steep. Simply understanding what `/add-context` does requires reading a 921-line command file.

2. **High initial investment**: The 6-question wizard requires the user to describe their entire tech stack, API patterns, component patterns, naming conventions, code standards, and security requirements upfront. This is a significant time investment before seeing any value.

3. **Template rigidity**: Every file must follow strict templates with HTML frontmatter, Quick Reference sections, Related Files sections, and MVI compliance. This is bureaucratic overhead for simple projects.

4. **File proliferation**: Even a simple project ends up with dozens of context files across multiple directories. This is hard to navigate manually and creates maintenance burden.

5. **No conversational context building**: The primary context building mechanism is the wizard, not a conversation. You answer questions in a form, not discuss your domain with an AI that challenges your thinking.

6. **No forced vocabulary alignment**: The system captures patterns and standards, but it doesn't have the equivalent of Pocock's "challenge against the glossary" mechanism. There's no active process of sharpening terminology and rejecting synonyms.

7. **Maintenance overhead**: With 80+ files, keeping context up to date requires active maintenance. The `/add-context --update` command helps, but someone has to remember to run it.

8. **Token cost for discovery**: ContextScout reads navigation.md files at every task start, which adds tokens to every interaction. For a project with extensive context, this could be significant.

9. **No natural ADR equivalent**: The `decisions-log.md` is a flat list of decisions in a single file. It lacks the independent identification, sequential numbering, and lightweight format of Pocock's ADR system. (An ADR system was planned but not yet implemented.)

10. **Self-referential complexity**: The context system documents itself in the context system, creating a rabbit hole of meta-documentation. While self-referential, this adds complexity without necessarily adding clarity for users.

11. **Dual implementation**: The OpenCode native system and the Claude Code plugin duplicate much of the same functionality with different implementations. This creates maintenance burden and potential drift between the two.

12. **CODEBASE_STANDARDS.md problem**: The 2000+ line CODEBASE_STANDARDS file violates MVI's own rules (200 line limit). There's no documented mechanism for keeping it in sync with codebase changes.

13. **No "proceed silently" option**: The system is vocal about context — ContextScout loads context on every task, agents are mandated to read context files. There's no way to say "I don't need context for this simple task."

14. **Approval gates add friction**: The harvest operation requires explicit user approval at multiple stages. While this is good for quality, it adds significant friction to the "learn over time" promise.

---

## 6. Design Philosophy Comparison

### Pocock Skills: Less is More

Pocock's philosophy is **minimalist and opinionated**:
- The best context is the least context that's still effective
- Domain vocabulary is the highest-leverage investment
- Conversations generate better context than forms
- The system should be invisible until you need it
- If context files don't exist, just keep working

This is the "Ubiquitous Language" approach from Domain-Driven Design: if you get the vocabulary right, everything else follows. It's elegant, lightweight, and easy to adopt.

### OpenAgents Control: More is More

OpenAgents' philosophy is **comprehensive and systematic**:
- Agents need comprehensive knowledge to produce consistent output
- Every kind of knowledge has its own file type and location
- Navigation-driven discovery scales to any project size
- MVI keeps individual files lean while the system covers everything
- Automatic loading ensures context is always available

This is the "Taxonomy" approach: organize everything, classify everything, make everything discoverable. It's thorough, scalable, and systematic, but at the cost of complexity.

---

## 7. Key Architectural Decisions

### Pocock Skills: Decisions That Define the System

1. **Vocabulary over everything**: The core insight is that naming is the hardest problem. By focusing on domain vocabulary, the system captures the highest-leverage knowledge type.

2. **Conversational over form-based**: Context emerges from grilling sessions, not questionnaires. This produces more nuanced, more accurate, and more useful context.

3. **Lazy creation over scaffolding**: Don't create structure until there's content to fill it. This prevents empty files and boilerplate.

4. **Inline updates over batch**: Update context as terms are resolved, not at the end of a session. This keeps context current.

5. **Manual trigger over automatic**: Context is built when the user chooses to grill, not automatically during every session. This gives users control.

6. **ADRs with a high bar**: Only record decisions that are genuinely hard to reverse, genuinely surprising, and genuinely the result of a trade-off. This prevents noise.

7. **Proceed silently**: If context doesn't exist, don't complain — just keep working without it. This prevents friction.

### OpenAgents Control: Decisions That Define the System

1. **Hierarchy over flat files**: A navigation tree with priority ranking scales better than a single file. This supports large, complex projects.

2. **MVI over comprehensive**: Each file should be minimal viable information. This prevents bloat at the file level, even though the system has many files.

3. **Automatic discovery over manual**: ContextScout runs on every task. This ensures context is always available without user intervention.

4. **Priority loading over all-or-nothing**: Critical context loads first, then high, then medium, then low. This is token-efficient.

5. **Templates over freeform**: Strict templates with frontmatter ensure consistency. This makes context machine-readable and discoverable.

6. **Multiple creation paths**: Wizard, harvest, extract, organize, manual. This supports different workflows and skill levels.

7. **Version tracking over git-only**: Frontmatter versions and dates enable staleness detection. This addresses the maintenance problem.

8. **Separation of concerns**: Business domain, technical domain, bridge, decisions, and living notes are in separate files. This makes updates targeted.

---

## 8. Reproducing the Feature: Requirements Synthesis

If you were to implement this feature from scratch, here's what you'd need based on both systems' approaches:

### Core Requirements (Both Systems Address These)

1. **Persistent knowledge storage**: Some mechanism to store project understanding that survives between sessions
2. **Discovery mechanism**: A way for the agent to find and load relevant context at task start
3. **Creation mechanism**: A way to create new context (whether conversational or form-based)
4. **Update mechanism**: A way to update context as understanding evolves
5. **Format specification**: Clear rules for what context files look like and what they contain

### Pocock-Specific Requirements

6. **Vocabulary enforcement**: Canonical terms with "avoid" lists and active challenge against existing glossary
7. **ADR creation with quality gate**: A 3-criteria test for when to record architectural decisions
8. **Example dialogue**: Conversational examples that demonstrate term usage
9. **Multi-context support**: Bounded contexts with CONTEXT-MAP.md
10. **Lazy creation**: Don't create files until there's content
11. **Inline updates**: Update context as it's discussed, not in batches
12. **Graceful degradation**: Proceed silently if context doesn't exist

### OpenAgents-Specific Requirements

13. **Hierarchical navigation**: Index files at every level that agents traverse
14. **Priority-based loading**: Critical/High/Medium/Low ranking for efficient token usage
15. **MVI compliance**: Each file stays under 200 lines
16. **HTML frontmatter**: Structured metadata in each file (context, priority, version, date)
17. **Harvesting from sessions**: Extract knowledge from AI summaries
18. **External documentation fetching**: Live library doc lookup via API
19. **Multiple update paths**: Wizard, targeted update, harvest, extract, organize
20. **Version tracking**: Version numbers and update dates for staleness detection
21. **Deprecation handling**: Rename to `.deprecated.md` rather than delete
22. **Self-documenting system**: The context system documents its own standards and operations

### Hybrid Opportunities

23. **Conversational context building with structured output**: Use Pocock's grilling approach to produce OpenAgents' structured knowledge artifacts
24. **Vocabulary enforcement within a comprehensive system**: Add Pocock's "challenge against glossary" mechanism to OpenAgents' broader context
25. **Lazy creation with MVI**: Create files only when needed (Pocock) but keep them lean (OpenAgents MVI)
26. **ADRs with Pocock's quality gate + OpenAgents' versioning**: Pocock's 3-criteria test but with frontmatter tracking
27. **Auto-discovery (OpenAgents) + Proceed silently (Pocock)**: Automatically find context when it exists, but don't complain when it doesn't
28. **Harvesting (OpenAgents) with conversational emergence (Pocock)**: Extract knowledge from sessions, but let grilling sessions challenge and refine existing vocabulary

---

## 9. Summary Assessment

### Pocock Skills: Best For

- Small to medium projects where domain vocabulary is the primary source of misunderstanding
- Teams that prefer lightweight, conversational tools over structured systems
- Projects where the friction of answering a 6-question wizard would prevent adoption
- Developers who believe "naming is the hardest problem" and want to focus on that
- Situations where token efficiency is paramount (one small file vs. dozens)

### OpenAgents Control: Best For

- Large, complex projects where comprehensive knowledge is needed
- Teams that want agents to produce consistent code that matches existing patterns
- Projects with multiple developers where institutional memory is critical
- Situations where automatic context discovery is important (no manual invocation needed)
- Codebases where external library documentation is frequently needed
- Projects that need different kinds of knowledge (patterns, standards, errors, business context) not just vocabulary

### The Core Trade-off

**Pocock Skills trades completeness for simplicity.** One file. Three sections. Immediate value. But it only captures vocabulary and decisions — not patterns, standards, or business logic.

**OpenAgents Control trades simplicity for completeness.** Dozens of files. Multiple commands. Rich knowledge. But it requires significant upfront investment and ongoing maintenance.

The ideal system would combine Pocock's **conversational, lazy, vocabulary-focused approach** with OpenAgents' **comprehensive, auto-discovering, priority-ranked system** — and would do so with a fraction of the complexity of either.

---

## Research Artifacts

All detailed research is in `/home/codey/Dev/research/`:

**Pocock Skills:**
- `pocock-skills/01-broad-exploration.md` — Feature overview, CONTEXT.md, ADRs, triggers, persistence, incremental building
- `pocock-skills/02-grill-with-docs-deep-dive.md` — Exact prompts, flows, decision trees, format specifications
- `pocock-skills/03-setup-and-consumption-deep-dive.md` — Setup flow, consumer rules, bootstrap sequence, hard/soft dependencies
- `pocock-skills/04-improve-architecture-and-deprecated-deep-dive.md` — Secondary producer, LANGUAGE.md, deprecated ubiquitous-language, evolution

**OpenAgents Control:**
- `openagents/01-broad-exploration.md` — Feature overview, navigation.md, other context files, triggers, persistence
- `openagents/02-add-context-deep-dive.md` — Exact 6-stage flow, 6 wizard questions, flags, templates, validation
- `openagents/03-agents-and-context-system-deep-dive.md` — ContextScout, ContextManager, OpenCoder/OpenAgent context loading, harvest/extract/organize
- `openagents/04-commands-and-standards-deep-dive.md` — All commands, MVI principle, frontmatter, structure, templates, navigation design
- `openagents/05-skills-and-plugin-deep-dive.md` — Context-manager skill, Context7, Claude Code plugin, SessionStart hook