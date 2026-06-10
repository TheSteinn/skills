# OpenAgents Control - Context Building Feature: Broad Exploration

## Feature Overview

### What the Feature Does

The "context-building" feature in OpenAgents Control (OAC) is a system that allows AI coding agents to learn, persist, and apply project-specific knowledge over time. It enables agents to understand a project's coding patterns, architecture, business domain, technical stack, and decisions, and then use that understanding to generate code that matches the project's existing conventions.

From a user perspective, the feature:

1. **Creates a "navigation.md" and related context files** that serve as a living, structured knowledge base of the project
2. **Teaches agents your patterns** through an interactive wizard (`/add-context`) or manual editing
3. **Automatically discovers relevant context** via the ContextScout subagent before any coding task
4. **Fetches external library documentation** via ExternalScout to avoid outdated training data
5. **Organizes, harvests, and maintains context** through `/context` commands and the ContextManager subagent
6. **Builds context incrementally** over time through the Project Intelligence system

### Goals

- **Consistency**: Generated code matches the project's existing patterns (no refactoring needed)
- **Efficiency**: MVI (Minimal Viable Information) principle reduces token usage by ~80%
- **Team Alignment**: Shared context means all team members' agents generate consistent code
- **Onboarding**: New developers or agents can quickly understand the project
- **Persistence**: Knowledge survives across sessions; agents pick up where they left off

### User Experience Flow

1. **First Setup**: User runs `/add-context` and answers 6 questions about their tech stack, API patterns, component patterns, naming conventions, code standards, and security requirements
2. **Context Files Created**: System creates `technical-domain.md` and `navigation.md` in `.opencode/context/project-intelligence/`
3. **Automatic Discovery**: When user gives a task to an agent, ContextScout discovers relevant context files automatically
4. **Pattern Application**: Agent loads discovered context and generates code following those patterns
5. **Incremental Updates**: User runs `/add-context --update` as their project evolves; system versions updates (1.0 -> 1.1, etc.)
6. **Harvesting**: AI-generated summaries and notes can be harvested into permanent context via `/context harvest`

---

## navigation.md

### What is navigation.md?

`navigation.md` is the **canonical index file** that acts as a table of contents for the entire context system. It exists at multiple levels in the hierarchy (root, category, subcategory), forming a navigation tree that agents traverse to discover relevant context files.

### Structure

Every `navigation.md` follows a consistent template:

```markdown
<!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->

# {Category} Navigation

**Purpose**: {One sentence description}

---

## Structure
```
{directory tree showing file layout}
```

---

## Quick Routes

| Task | Path |
|------|------|
| **{Task}** | `{path}` |

---

## By {Concern/Type}

**{Section}** → {description}
```

### Hierarchy of navigation.md Files

The system uses navigation.md files at every level:

| Location | Purpose |
|----------|---------|
| `.opencode/context/navigation.md` | Root index pointing to all top-level categories |
| `.opencode/context/core/navigation.md` | Core standards and workflows |
| `.opencode/context/project-intelligence/navigation.md` | Project-specific knowledge |
| `.opencode/context/development/navigation.md` | Development context |
| `.opencode/context/ui/navigation.md` | UI/UX context |
| `.opencode/context/data/navigation.md` | Data engineering context |
| `.opencode/context/content-creation/navigation.md` | Content creation context |
| `.opencode/context/product/navigation.md` | Product management context |
| `.opencode/context/learning/navigation.md` | Educational context |
| `.opencode/context/openagents-repo/navigation.md` | OAC repo-specific context |
| Each subcategory also has its own navigation.md | Subcategory-level navigation |

### How It Is Created Initially

1. **Root navigation.md**: Shipped with OAC as part of the default context installation
2. **Project Intelligence navigation.md**: Created by the `/add-context` command wizard
3. **Category navigation.mds**: Created during context system build-out, either by the system-builder, by context organize operations, or manually

### How It Is Updated

- **Manually**: Direct editing of the markdown files
- **By `/add-context --update`**: Updates project-intelligence navigation when patterns change
- **By `/context harvest`**: Updates navigation when knowledge is extracted from summaries
- **By `/context organize`**: Restructures and updates navigation when context is reorganized
- **By ContextManager subagent**: Validates and proposes improvements to navigation structure

### What Triggers Updates

- Running `/add-context` or `/add-context --update`
- Running `/context harvest` (harvesting knowledge from summaries)
- Running `/context organize` (restructuring files)
- Adding new context files or categories
- Deprecating or removing context files
- Running `/context validate` (can flag outdated navigation)

### The Root navigation.md Content

The root `navigation.md` (at `.opencode/context/navigation.md`) contains:

```
Structure: core/, openagents-repo/, development/, ui/, content-creation/, data/, product/, learning/
Quick Routes: Write code → core/standards/code-quality.md, Write tests → core/standards/test-coverage.md, etc.
By Category: core/ → core/navigation.md, openagents-repo/ → openagents-repo/navigation.md, etc.
```

---

## Other Context Files

### Project Intelligence Files

Located in `.opencode/context/project-intelligence/`:

| File | Purpose | Format |
|------|---------|--------|
| `navigation.md` | Quick overview and routes to all PI files | Navigation template with frontmatter |
| `technical-domain.md` | Tech stack, architecture, code patterns, naming conventions, security | Template with Primary Stack table, Code Patterns sections |
| `business-domain.md` | Business context, problem statement, target users, value proposition | Template with business sections |
| `business-tech-bridge.md` | How business needs map to technical solutions | Template with Core Mapping table |
| `decisions-log.md` | Major decisions with rationale, alternatives, impact | Decision template with structured entries |
| `living-notes.md` | Active issues, technical debt, open questions, patterns | Living document with tables for debt, questions, issues |

### Core Context Files

Located in `.opencode/context/core/`:

| Directory | Key Files | Purpose |
|-----------|-----------|---------|
| `standards/` | code-quality.md, security-patterns.md, test-coverage.md, documentation.md, project-intelligence.md, project-intelligence-management.md | Universal coding standards |
| `workflows/` | code-review.md, task-delegation-basics.md, design-iteration-overview.md, feature-breakdown.md, session-management.md | Workflow definitions |
| `guides/` | resuming-sessions.md | Step-by-step guides |
| `task-management/` | Standards, guides, and lookup for task JSON schema | Task management patterns |
| `system/` | context-guide.md | System-level context management guide |
| `context-system/` | **The meta-system**: operations/, standards/, guides/, examples/ | How the context system itself works |

### Context System Internal Files

The context system has its own self-referential documentation:

| Path | Purpose |
|------|---------|
| `core/context-system/context-system.md` | Complete guide to the context system: principles, directory patterns, operations |
| `core/context-system/standards/mvi.md` | Minimal Viable Information principle |
| `core/context-system/standards/frontmatter.md` | HTML comment frontmatter format specification |
| `core/context-system/standards/structure.md` | File organization standards |
| `core/context-system/standards/templates.md` | File templates |
| `core/context-system/standards/codebase-references.md` | Linking context to code |
| `core/context-system/operations/harvest.md` | Harvesting workflow (6-stage) |
| `core/context-system/operations/extract.md` | Extracting context from docs/code |
| `core/context-system/operations/organize.md` | Restructuring context files |
| `core/context-system/operations/update.md` | Updating context when APIs change |
| `core/context-system/operations/migrate.md` | Migrating global → local |
| `core/context-system/guides/compact.md` | How to minimize verbose files to MVI |
| `core/context-system/guides/creation.md` | File creation guide |
| `core/context-system/guides/workflows.md` | Step-by-step context workflows |

### CODEBASE_STANDARDS.md

A very large (~2000+ line) file at `.opencode/context/CODEBASE_STANDARDS.md` that documents detailed TypeScript coding patterns derived from the OpenCode codebase itself, covering function definitions, class usage, array handling, async patterns, race conditions, AI system integration, service architecture, state management, event bus patterns, and more.

### Project-Level Context Files

| Path | Purpose |
|------|---------|
| `.opencode/context/project/navigation.md` | Project-specific navigation |
| `.opencode/context/project/project-context.md` | **DEPRECATED** - replaced by project-intelligence/technical-domain.md |
| `.opencode/context/index.md` | Compatibility shim pointing to navigation.md |

### How These Files Relate to Each Other

The context system follows a **navigation-first, concern-based** hierarchy:

1. **Root navigation.md** → routes to category-specific navigation.md files
2. **Category navigation.md** → routes to subcategory navigation.md files or directly to content
3. **Content files** → contain actual knowledge following MVI format
4. **Project Intelligence** → bridges business and technical domains, serves as "your project's brain"
5. **CODEBASE_STANDARDS.md** → a special case: deep code-level patterns for a specific codebase

The relationship between `navigation.md` and other files:
- `navigation.md` is the entry point; ContextScout reads it first
- Other files are discovered by following the navigation tree
- Each file contains HTML frontmatter with priority levels (critical, high, medium, low)
- Priority determines loading order: critical (80% use cases) → high (15%) → medium (4%) → low (1%)

The relationship between project-intelligence files:
- `navigation.md` is the overview
- `technical-domain.md` is the most frequently used (tech stack, patterns)
- `business-domain.md` provides the "why"
- `business-tech-bridge.md` connects "why" to "how"
- `decisions-log.md` records "why we chose X"
- `living-notes.md` tracks current state and issues

---

## Trigger Mechanism

### What Prompts Context Building/Updating

Context building is triggered through multiple mechanisms:

#### 1. User-Initiated Commands

| Command | Trigger | What Happens |
|---------|---------|--------------|
| `/add-context` | User runs interactively | 6-question wizard creates project-intelligence/technical-domain.md and navigation.md |
| `/add-context --update` | User wants to update existing patterns | Reviews each pattern section, offers Keep/Update/Replace |
| `/add-context --tech-stack` | Quick tech stack update | Updates only tech stack portion |
| `/add-context --patterns` | Quick patterns update | Updates only code patterns |
| `/add-context --global` | Save to global config | Saves to `~/.config/opencode/context/` instead of project-local |
| `/context` | Quick context scan | Scans workspace for summaries, suggests harvest |
| `/context harvest` | Extract knowledge from summaries | 6-stage workflow: Scan → Analyze → Approve → Extract → Cleanup → Report |
| `/context extract from {source}` | Extract from docs/code/URLs | Extract core concepts, minimal examples |
| `/context organize {category}` | Restructure files | Reorganize flat files into function-based folders |
| `/context update for {topic}` | Update for API changes | Find affected files, update concepts/examples/guides |
| `/context error for {error}` | Add error to knowledge base | Capture recurring errors with solutions |
| `/context create {category}` | Create new context area | Create new category with proper structure |
| `/context compact {file}` | Minimize file to MVI format | Compress verbose file |
| `/context map [category]` | View structure | Display context tree |
| `/context validate` | Check integrity | Verify references, file sizes, navigation |
| `/context migrate` | Global → local migration | Copy project-intelligence from global to local |
| `/build-context-system` | Create entire context system | Interactive system builder for new domains/projects |

#### 2. Agent-Initiated (Automatic)

| Agent | Trigger | What Happens |
|-------|---------|--------------|
| **ContextScout** | Every task invocation (Stage 1.5 of OpenAgent/OpenCoder workflow) | Reads navigation.md, discovers relevant context files, returns ranked list |
| **ContextManager** | When invoked for organization/validation | Discovers, catalogs, validates, proposes improvements to context |
| **ExternalScout** | When external libraries detected | Fetches live docs, saves to .tmp/external-context/, returns file paths |

#### 3. Installation-Initiated

| Trigger | What Happens |
|---------|--------------|
| `bash install.sh developer` | Installs OAC locally, sets up context in `.opencode/context/` |
| `bash install.sh` (interactive) | Lets user choose local/global, installs context |
| `/install-context` (Claude Code plugin) | Downloads context files from GitHub repo |
| `/install-context --core` | Downloads only core context files |
| `/install-context --all` | Downloads all context including examples |

#### 4. Session-Initiated

| Hook | Trigger | What Happens |
|------|---------|--------------|
| **SessionStart** (Claude Code plugin) | New Claude Code session | Auto-loads the `using-oac` skill |
| ContextScout *startup* | Every task start | One-time resolution of local vs global core context |

#### 5. Validation Hooks

| Hook | Trigger | What Happens |
|------|---------|--------------|
| `scripts/validation/validate-context-refs.sh` | Pre-commit or manual | Validates context file references |
| `scripts/hooks/pre-commit` | Git pre-commit | Runs validation checks |

---

## Implementation Details

### How the Feature Is Technically Implemented

#### Agents (Markdown Prompt Definitions)

**Primary Agents** (`.opencode/agent/core/`):
- `opencoder.md` - OpenCoder: Development specialist with 6-stage workflow (Discover → Propose → InitSession → Plan → Execute → Validate)
- `openagent.md` - OpenAgent: Universal agent with Discover → Approve → Execute → Validate → Summarize → Confirm workflow

Both agents have a **critical context requirement**: they MUST load context files before any code implementation. This is enforced through:
- `<critical_context_requirement>` XML blocks
- `<critical_rules priority="absolute" enforcement="strict">` rules
- Execution priority tiers where Tier 1 (safety/context) overrides all

**Subagents** (`.opencode/agent/subagents/core/`):
- `contextscout.md` - Discovers context files via navigation-driven search, ranked by priority
- `context-manager.md` - Manages context lifecycle: discover, catalog, validate, propose, organize
- `externalscout.md` - Fetches live external library docs from Context7 API, caches in .tmp/
- `batch-executor.md` - Manages parallel task execution
- `task-manager.md` - Breaks complex features into atomic JSON subtasks
- `documentation.md` - Documentation generation
- `context-retriever.md` - Context retrieval

**Subagents in Other Categories:**
- `.opencode/agent/subagents/development/` - CoderAgent, BuildAgent
- `.opencode/agent/subagents/test/` - TestEngineer
- `.opencode/agent/subagents/planning/` - TaskManager variants
- `.opencode/agent/subagents/utils/` - Utility agents

#### Skills (Executable Skill Definitions)

- `.opencode/skills/context-manager/` - CLI router with 8 operations (discover, fetch, harvest, extract, compress, organize, cleanup, process)
- `.opencode/skills/context7/` - Context7 API integration library (external doc fetching)
- `.opencode/skills/task-management/` - Task management CLI tools
- `.opencode/skills/smart-router-skill/` - Intelligent routing

#### Commands (Slash Command Definitions)

Key context-building commands:
- `.opencode/command/add-context.md` - The main interactive wizard (921 lines, very detailed)
- `.opencode/command/build-context-system.md` - Interactive system builder (861 lines)
- `.opencode/command/context.md` - Context manager command (309 lines)
- `.opencode/command/analyze-patterns.md` - Pattern analysis command
- `.opencode/command/commit.md`, `.opencode/command/test.md`, etc. - Other commands

#### Configuration Files

- `.opencode/opencode.json` - OpenCode configuration (minimal)
- `.opencode/config.json` - Agent configuration (`{"agent": "eval-runner"}`)
- `.opencode/config/agent-metadata.json` - Agent metadata registry

#### The Context Discovery Flow (ContextScout)

1. **Resolve core location** (once per invocation):
   - Check `glob("{local}/core/navigation.md")`
   - If found → use local for everything
   - If not found → check paths.json for global path
   - Set `{core_root}` accordingly

2. **Understand intent** from user request

3. **Follow navigation** - Read `navigation.md` files downward through hierarchy

4. **Return ranked files** - Priority order: Critical → High → Medium

ContextScout is **read-only** (no write, edit, bash, or task permissions). It can only read, grep, and glob.

#### The add-context Command Flow

The `/add-context` command follows a detailed 6-stage workflow:

**Stage 0.5**: Resolve context location (local `.opencode/context/project-intelligence/` or global `~/.config/opencode/context/project-intelligence/`)

**Stage 0**: Check for external context files in `.tmp/`

**Stage 1**: Detect existing context
- If exists: offer Review/Update/Add/Replace/Cancel
- If not: offer to create new

**Stage 1.5**: Pattern review (if updating)
- Show each pattern, offer Keep/Update/Remove

**Stage 2**: Interactive wizard (6 questions):
1. Tech stack?
2. API endpoint example?
3. Component example?
4. Naming conventions?
5. Code standards?
6. Security requirements?

**Stage 3**: Generate/update context with preview

**Stage 4**: Validation against MVI rules (<200 lines, frontmatter, etc.)

**Stage 5**: Confirmation & next steps

#### Project Intelligence Standard

Files follow a strict standard defined in:
- `.opencode/context/core/standards/project-intelligence.md` - What and why
- `.opencode/context/core/standards/project-intelligence-management.md` - How to manage

Every file must have:
- HTML frontmatter: `<!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->`
- Quick Reference section
- Related Files section
- Maximum 200 lines (MVI compliance)
- Codebase references section
- Navigation.md updates when files are created/modified

---

## Persistence Strategy

### How Context Persists Across Sessions

1. **File-Based Storage**: All context is stored as markdown files in `.opencode/context/` (local) or `~/.config/opencode/context/` (global)

2. **Navigation-Driven Discovery**: Agents don't need to remember context; they discover it fresh each session by reading navigation.md files

3. **Context Resolution Priority**:
   - Local `.opencode/context/core/navigation.md` takes precedence
   - If not found locally, falls back to global `~/.config/opencode/context/core/navigation.md`
   - Project intelligence is ALWAYS local (never loaded from global)
   - One-time check per session (max 2 glob checks)

4. **Versioning**: Each file tracks version via HTML frontmatter (`Version: X.Y`)
   - New file = 1.0
   - Content update = minor (1.1, 1.2)
   - Structure change = major (2.0)

5. **External Context Caching**: ExternalScout saves fetched docs to `.tmp/external-context/{package-name}/{topic}.md` with a manifest `.tmp/external-context/.manifest.json`

### How the System Knows What Context Already Exists

- ContextScout reads `navigation.md` files to discover what's available
- The `/add-context` command checks for existing files before creating
- ContextManager catalogs existing files with metadata
- File frontmatter contains version and update date for tracking

### How the System Avoids Duplicating or Conflicting Context

- **Navigation.md as source of truth**: All context files must be listed in navigation.md
- **Project Intelligence independently versioned**: Each file has its own version in frontmatter
- **Deduplication in harvest**: When harvesting, the system checks if content already exists in a context file (marked as Skip/Duplicate)
- **Local vs Global separation**: Local always wins; project-specific context never loaded from global
- **Deprecated handling**: Files are renamed `.deprecated.md` rather than deleted, with forward references

---

## Incremental Building

### How Context Grows Over Time

#### 1. Initial Creation (/add-context)

Creates foundational files:
- `technical-domain.md` (tech stack, patterns)
- `navigation.md` (quick overview)

#### 2. Incremental Updates (/add-context --update)

Reviews each existing pattern section, allows Keep/Update/Replace:
- Version bumps from MINOR (1.2 → 1.3)
- Date updates in frontmatter
- Navigation.md automatically updated

#### 3. Harvesting Knowledge (/context harvest)

AI agents generate summary files during work (OVERVIEW.md, SESSION-*.md, etc.). Harvest:
- Scans for summary patterns
- Analyzes content, categorizes by function
- Presents approval UI (user selects what to extract)
- Extracts knowledge using MVI (Minimal Viable Information)
- Writes to permanent context files
- Archives original summaries

#### 4. Pattern-Based Building (analyze-patterns)

The `/analyze-patterns` command can find recurring patterns in the codebase and suggest extracting them as context.

#### 5. Manual Expansion

Users can:
- Edit files directly
- Add new files to project-intelligence/
- Create new context categories
- Add subfolders with navigation.md

#### 6. External Knowledge Integration (ExternalScout)

When agents detect external libraries:
- Fetches current documentation via Context7 API
- Saves to `.tmp/external-context/`
- Can be harvested into permanent context or referenced temporarily

### How the System Decides What New Information to Add

1. **Harvest rules**: Auto-detects summary files and categorizes:
   - Design decisions → `concepts/`
   - Solutions/patterns → `examples/`
   - Workflows → `guides/`
   - Errors encountered → `errors/`
   - Reference data → `lookup/`

2. **Add-context triggers**: User-driven, with pattern-specific flags (--tech-stack, --patterns)

3. **Update triggers**: When APIs/frameworks change, `/context update for {topic}` finds affected files and updates them

4. **Error capture**: `/context error for {error}` captures recurring errors with solutions

5. **Organize**: `/context organize {category}` restructures flat files into function-based folders

### How It Handles Changes to Existing Context

- **Version tracking**: Each file has `Version: X.Y` in frontmatter
- **Update workflow**: Review current patterns → Keep/Update/Remove → Preview changes → Confirm
- **Deprecation**: Files renamed `.deprecated.md` with deprecation banners
- **Backup on replace**: Before replacing all patterns, backs up to `.tmp/backup/project-intelligence-{timestamp}/`
- **Navigation update**: Must update navigation.md when creating/modifying files (enforced by add-context command)

---

## Configuration

### Settings That Control Context Behavior

**OpenCode Configuration** (`.opencode/opencode.json`):
- Minimal - just `{ "$schema": "https://opencode.ai/config.json" }`
- Agent selection in `.opencode/config.json` (e.g., `{"agent": "eval-runner"}`)

**Agent Configuration** (per-agent frontmatter):
- Model selection (e.g., `model: anthropic/claude-sonnet-4-5`)
- Temperature
- Permissions (bash, edit, write, read, glob, grep, task)
- Mode (primary vs subagent)

**Context Root Configuration**:
- Default: `.opencode/context/`
- Custom: If `paths.json` sets `custom_dir`, use that instead
- Global fallback: `~/.config/opencode/context/`

**Context Resolution Logic** (built into ContextScout):
```
1. Check local: .opencode/context/core/navigation.md
   → Found? → Use local for everything. Done.
   → Not found?
2. Check global: ~/.config/opencode/context/core/navigation.md
   → Found? → Use global for core/ files only.
   → Not found? → Proceed without core context.
```

**Profiles** (`.opencode/profiles/`):
- `essential/`, `developer/`, `advanced/`, `business/`, `full/` - Different amounts of context

**Claude Code Plugin** (`.oac.json` or `.claude/context/`):
- Plugin has its own context discovery paths
- Flexible: `.oac config`, `.claude/context`, `context`, `.opencode/context`

**Frontmatter Fields** (per-file configuration):
- `Context: {category}/{function}` - What this file covers
- `Priority: {critical|high|medium|low}` - When to load (critical = 80% of use cases)
- `Version: X.Y` - Version tracking
- `Updated: YYYY-MM-DD` - Last update date

**File Size Limits** (MVI principle):
- Concepts: max 100 lines
- Examples: max 80 lines
- Guides: max 150 lines
- Navigation: 200-300 tokens
- All files: max 200 lines

---

## Complete File Reference

### Root Level
| Path | Description |
|------|-------------|
| `/home/codey/Dev/OpenAgentsControl/CONTEXT_SYSTEM_GUIDE.md` | User-facing guide to the context system (724 lines) |
| `/home/codey/Dev/OpenAgentsControl/README.md` | Main project README with context system overview |
| `/home/codey/Dev/OpenAgentsControl/context-findings/plan/context-system-implementation-plan.md` | Implementation plan for context system improvements |

### .opencode/context/ (Context Files)
| Path | Description |
|------|-------------|
| `.opencode/context/navigation.md` | Root navigation index for all context |
| `.opencode/context/index.md` | Compatibility shim → redirect to navigation.md |
| `.opencode/context/CODEBASE_STANDARDS.md` | Detailed TypeScript codebase patterns (2000+ lines) |
| `.opencode/context/project-intelligence/navigation.md` | Project intelligence navigation |
| `.opencode/context/project-intelligence/technical-domain.md` | Tech stack, architecture, code patterns (template) |
| `.opencode/context/project-intelligence/business-domain.md` | Business context (template) |
| `.opencode/context/project-intelligence/business-tech-bridge.md` | Business → tech mapping (template) |
| `.opencode/context/project-intelligence/decisions-log.md` | Decision records with rationale |
| `.opencode/context/project-intelligence/living-notes.md` | Active issues, debt, open questions |
| `.opencode/context/project/navigation.md` | Project-specific navigation |
| `.opencode/context/project/project-context.md` | DEPRECATED - replaced by project-intelligence |
| `.opencode/context/core/context-system.md` | Complete context system guide (450 lines) |
| `.opencode/context/core/navigation.md` | Core context navigation |
| `.opencode/context/core/essential-patterns.md` | Essential patterns reference |
| `.opencode/context/core/visual-development.md` | Visual development standards |
| `.opencode/context/core/context-system/` | Self-referential context system documentation |
| `.opencode/context/core/context-system/navigation.md` | Context system navigation |
| `.opencode/context/core/context-system/standards/mvi.md` | MVI principle definition |
| `.opencode/context/core/context-system/standards/frontmatter.md` | Frontmatter format spec |
| `.opencode/context/core/context-system/standards/structure.md` | File organization standards |
| `.opencode/context/core/context-system/standards/templates.md` | File templates |
| `.opencode/context/core/context-system/standards/codebase-references.md` | Linking context to code |
| `.opencode/context/core/context-system/operations/harvest.md` | Harvest operation workflow |
| `.opencode/context/core/context-system/operations/extract.md` | Extract operation |
| `.opencode/context/core/context-system/operations/organize.md` | Organize operation |
| `.opencode/context/core/context-system/operations/update.md` | Update operation |
| `.opencode/context/core/context-system/operations/migrate.md` | Global → local migration |
| `.opencode/context/core/context-system/operations/error.md` | Error capture operation |
| `.opencode/context/core/context-system/guides/compact.md` | How to minimize files |
| `.opencode/context/core/context-system/guides/creation.md` | File creation guide |
| `.opencode/context/core/context-system/guides/workflows.md` | Step-by-step workflows |
| `.opencode/context/core/context-system/guides/navigation-design-basics.md` | Navigation file design |
| `.opencode/context/core/context-system/guides/navigation-templates.md` | Navigation templates |
| `.opencode/context/core/context-system/guides/organizing-context.md` | Organizing context |
| `.opencode/context/core/context-system/examples/` | Example navigation files |
| `.opencode/context/core/standards/` | Universal standards (14 files) |
| `.opencode/context/core/standards/project-intelligence.md` | Project Intelligence standard |
| `.opencode/context/core/standards/project-intelligence-management.md` | PI management guide |
| `.opencode/context/core/standards/code-quality.md` | Code quality standards |
| `.opencode/context/core/standards/security-patterns.md` | Security patterns |
| `.opencode/context/core/standards/test-coverage.md` | Testing standards |
| `.opencode/context/core/standards/documentation.md` | Documentation standards |
| `.opencode/context/core/standards/code-analysis.md` | Code analysis approach |
| `.opencode/context/core/workflows/` | Workflow definitions |
| `.opencode/context/core/system/context-guide.md` | Context loading guide |
| `.opencode/context/development/` | Development-specific context |
| `.opencode/context/ui/` | UI/UX context |
| `.opencode/context/data/` | Data engineering context |
| `.opencode/context/content-creation/` | Content creation context |
| `.opencode/context/product/` | Product management context |
| `.opencode/context/learning/` | Educational content |
| `.opencode/context/openagents-repo/` | OAC repo-specific context |
| `.opencode/context/system-builder-templates/` | Templates for system builder |

### .opencode/agent/ (Agent Definitions)
| Path | Description |
|------|-------------|
| `.opencode/agent/core/opencoder.md` | OpenCoder primary agent (501 lines) |
| `.opencode/agent/core/openagent.md` | OpenAgent primary agent (677 lines) |
| `.opencode/agent/core/0-category.json` | Agent category metadata |
| `.opencode/agent/subagents/core/contextscout.md` | ContextScout subagent (116 lines) |
| `.opencode/agent/subagents/core/context-manager.md` | ContextManager subagent (475 lines) |
| `.opencode/agent/subagents/core/externalscout.md` | ExternalScout subagent (320 lines) |
| `.opencode/agent/subagents/core/batch-executor.md` | BatchExecutor for parallel tasks |
| `.opencode/agent/subagents/core/task-manager.md` | TaskManager for task breakdown |
| `.opencode/agent/subagents/core/stage-orchestrator.md` | Stage orchestrator |
| `.opencode/agent/subagents/core/documentation.md` | Documentation subagent |
| `.opencode/agent/subagents/core/context-retriever.md` | Context retriever |
| `.opencode/agent/subagents/development/` | Development subagents (CoderAgent, BuildAgent) |
| `.opencode/agent/subagents/test/` | Test subagents (TestEngineer) |
| `.opencode/agent/subagents/planning/` | Planning subagents |
| `.opencode/agent/subagents/system-builder/` | System builder subagents |
| `.opencode/agent/subagents/utils/` | Utility subagents |
| `.opencode/agent/eval-runner.md` | Evaluation runner |
| `.opencode/agent/content/` | Content creation agents |
| `.opencode/agent/data/` | Data agents |
| `.opencode/agent/meta/` | Meta-level agents |

### .opencode/command/ (Slash Commands)
| Path | Description |
|------|-------------|
| `.opencode/command/add-context.md` | Interactive context creation wizard (921 lines) |
| `.opencode/command/build-context-system.md` | System builder command (861 lines) |
| `.opencode/command/context.md` | Context manager command (309 lines) |
| `.opencode/command/analyze-patterns.md` | Pattern analysis command (221 lines) |
| `.opencode/command/commit.md` | Smart git commits |
| `.opencode/command/test.md` | Testing workflows |
| `.opencode/command/optimize.md` | Code optimization |
| `.opencode/command/clean.md` | Cleanup command |
| `.opencode/command/validate-repo.md` | Repository validation |
| `.opencode/command/worktrees.md` | Git worktree management |
| `.opencode/command/openagents/` | OpenAgents-specific commands |
| `.opencode/command/prompt-engineering/` | Prompt engineering commands |
| `.opencode/command/commit-openagents.md` | OAC-specific commit command |

### .opencode/skills/ (Skills)
| Path | Description |
|------|-------------|
| `.opencode/skills/context-manager/router.sh` | CLI router for context manager skill |
| `.opencode/skills/context-manager/SKILL.md` | Context manager skill definition (568 lines) |
| `.opencode/skills/context7/SKILL.md` | Context7 API integration (85 lines) |
| `.opencode/skills/context7/library-registry.md` | Supported libraries registry |
| `.opencode/skills/context7/navigation.md` | Context7 navigation |
| `.opencode/skills/context7/README.md` | Context7 documentation |
| `.opencode/skills/task-management/` | Task management skill |
| `.opencode/skills/smart-router-skill/` | Smart routing skill |

### .opencode/skill/ (Alternative Skills Directory)
| Path | Description |
|------|-------------|
| `.opencode/skill/project-orchestration/` | Project orchestration skill |
| `.opencode/skill/task-management/` | Task management skill |

### plugins/claude-code/ (Claude Code Plugin)
| Path | Description |
|------|-------------|
| `plugins/claude-code/README.md` | Plugin documentation (532 lines) |
| `plugins/claude-code/agents/` | 7 Claude Code subagents |
| `plugins/claude-code/skills/` | 12 Claude Code skills (using-oac, context-discovery, etc.) |
| `plugins/claude-code/commands/` | 4 user commands |
| `plugins/claude-code/hooks/` | SessionStart hook |
| `plugins/claude-code/scripts/` | Install/cleanup scripts |
| `plugins/claude-code/.claude-plugin/plugin.json` | Plugin metadata |
| `plugins/claude-code/.context-manifest.json` | Context download tracking |
| `plugins/claude-code/context/` | Claude Code plugin context (mirrors main context) |

### Scripts (Supporting Shell Scripts)
| Path | Description |
|------|-------------|
| `scripts/external-context/manage-external-context.sh` | Manage external context files |
| `scripts/check-context-logs/` | Context log inspection scripts |
| `scripts/validation/validate-context-refs.sh` | Validate context references |
| `scripts/validation/setup-pre-commit-hook.sh` | Setup pre-commit validation |

### Other Relevant Files
| Path | Description |
|------|-------------|
| `.opencode/prompts/` | Prompt templates organized by category |
| `.opencode/profiles/` | Installation profiles (essential, developer, advanced, business, full) |
| `.opencode/docs/` | Agent documentation, guides, workflows |
| `.opencode/tool/` | TypeScript tool implementation |
| `docs/getting-started/context-aware-system/QUICK_START_SYSTEM_BUILDER.md` | Quick start for system builder |
| `dev/docs/context-reference-convention.md` | Context reference convention documentation |

---

## Open Questions / Ambiguities

### 1. How exactly does the "learning over time" aspect work in practice?

The system has the infrastructure for incremental learning (harvest, update, living-notes, add-context --update), but there is no explicit automatic mechanism that observes agent sessions and automatically adds new patterns. The "learning" appears to be entirely user-initiated or driven by manual `/add-context --update` commands and `/context harvest`. The "slowly, over time" aspect mentioned in the task description seems to rely on users noticing patterns and updating context, rather than an automatic learning loop.

### 2. Is there truly automatic context building during sessions?

While ContextScout discovers context automatically at the start of every task, there is no evidence of a mechanism that automatically creates or updates context files based on what happens during a session. The harvest operation requires explicit user approval. The session files in `.tmp/sessions/` store context, but there's no documented automatic pipeline that turns session learnings into permanent context.

### 3. How does the proposed ADR (Architecture Decision Records) system relate?

The `context-findings/plan/context-system-implementation-plan.md` proposes migrating from the single `decisions-log.md` to an ADR-index system with per-record files and supersession/conflict protection. This appears to be a planned but not-yet-implemented enhancement.

### 4. What is the relationship between the two skills directories?

There are two skill directories: `.opencode/skills/` (with context-manager/ and context7/) and `.opencode/skill/` (with project-orchestration/ and task-management/). The singular `skill/` directory appears to be an older convention, while `skills/` is the current one. This may cause confusion.

### 5. How does the Claude Code plugin's context system differ from the OpenCode native system?

The Claude Code plugin (`plugins/claude-code/`) has its own agents, skills, commands, and context directory that largely mirrors the main system. However, it has some differences:
- Uses `context: fork` for subagent delegation (not nested calls)
- Has a `using-oac` skill that auto-invokes on session start
- Has its own `.oac.json` configuration
- Has its own context manifest tracking (`.context-manifest.json`)
- Has install scripts that download context from the main repo

The relationship between these two systems and how they stay in sync is not fully clear.

### 6. How are profiles used in context loading?

The profiles directory (`.opencode/profiles/`) has essential, developer, advanced, business, and full subdirectories, but I haven't read their contents to understand how they affect context loading. This likely controls how much context is loaded (essential = minimal, full = everything).

### 7. What triggers ExternalScout vs ContextScout?

Both agents are always available, but the logic for when to invoke ExternalScout seems to be:
- ContextScout runs on every task (Stage 1.5 in OpenAgent/OpenCoder)
- If ContextScout finds that a framework/library has no internal coverage, it recommends ExternalScout
- ExternalScout is also triggered when external packages are detected (Stage 1.5b in OpenAgent workflow)

### 8. How portable is project-intelligence across projects?

The project-intelligence system is designed to be project-specific (always local, never loaded from global). But the `/add-context --global` flag saves to `~/.config/opencode/context/project-intelligence/` as a fallback. The `/context migrate` command copies from global to local. The exact semantics of cross-project reuse need further investigation.

### 9. What is the `project/` directory's role vs `project-intelligence/`?

The `.opencode/context/project/` directory contains `project-context.md` (now deprecated) and `navigation.md`. This appears to be a predecessor to `project-intelligence/`. The deprecated file has a clear migration reference: "Replaced by project-intelligence/technical-domain.md". It's unclear whether the `project/` directory is still actively used or if it's purely legacy.

### 10. How does the context system handle conflicts between concurrent agents?

If multiple OpenCoder agents are running simultaneously updating context, there's no apparent conflict resolution mechanism beyond file-level locking (which the OpenCode base system handles via `Lock` utilities). The context system assumes single-writer access to context files.

### 11. What is the `.opencode/context/openagents-repo/` category?

This appears to be repo-specific context for the OpenAgentsControl repository itself (not for user projects). It has its own navigation.md, guides, standards, concepts, etc. This is meta-context about the OAC project.

### 12. How is the `CODEBASE_STANDARDS.md` maintained?

The 2000+ line `CODEBASE_STANDARDS.md` appears to be analytically generated (it references specific source files and line numbers from the OpenCode codebase). There's no documented mechanism for keeping it in sync with codebase changes. The content seems statically derived rather than dynamically updated.
