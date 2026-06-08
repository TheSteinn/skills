# Skills and Plugin Deep Dive: OpenAgentsControl Context System

> Comprehensive documentation of the context-manager skill, Context7 skill, context system guide, and the Claude Code plugin implementation.

---

## Table of Contents

1. [Context Manager Skill](#1-context-manager-skill)
2. [Context7 Skill](#2-context7-skill)
3. [Context System Guide](#3-context-system-guide-user-facing-documentation)
4. [Claude Code Plugin](#4-claude-code-plugin-overview)
5. [Plugin Agents](#5-plugin-agents-detail)
6. [Plugin Skills](#6-plugin-skks-detail)
7. [SessionStart Hook](#7-sessionstart-hook-deep-dive)
8. [Plugin Commands and Hooks](#8-plugin-commands-and-hooks)
9. [Context Discovery Protocol](#9-context-discovery-protocol)
10. [Comparative Analysis: OpenCode vs Claude Code Plugin](#10-comparative-analysis)

---

## 1. Context Manager Skill

**File**: `.opencode/skills/context-manager/SKILL.md` (568 lines)
**Router**: `.opencode/skills/context-manager/router.sh` (133 lines)

### Purpose

The context-manager skill provides 8 operations for managing project context files: discovery, fetching external docs, harvesting summaries, extracting information, compressing, organizing, cleaning up, and guided workflows.

### The 8 Operations

#### Operation 1: DISCOVER

**Purpose**: Find context files using intelligent discovery or direct search.

**When to Use**:
- Need to find all context files in repository
- Looking for specific context by topic
- Mapping context structure
- Understanding what context exists

**Interface**:
```bash
./router.sh discover [target]
```

**Examples**:
```bash
./router.sh discover "authentication patterns"
./router.sh discover "all context files"
./router.sh discover ".opencode/context/core/"
```

**Output**:
- List of discovered files with paths and sizes
- File statistics (count, total size, last updated)
- Categorization by type
- Suggestions for next steps

#### Operation 2: FETCH

**Purpose**: Fetch external documentation using ExternalScout.

**When to Use**:
- Need live documentation from external libraries
- Setting up new external library integration
- Need version-specific documentation
- Want to cache external docs for team

**Interface**:
```bash
./router.sh fetch [libraries] [topics]
```

**Examples**:
```bash
./router.sh fetch "Drizzle ORM" "modular schemas"
./router.sh fetch "Drizzle ORM" "Better Auth" "Next.js" "modular schemas" "integration" "app router"
./router.sh fetch "Better Auth" "Next.js App Router integration with Drizzle adapter"
```

**Output**:
- Fetched files with paths
- File sizes and statistics
- Source URLs
- How to reference in context
- Manifest updates

#### Operation 3: HARVEST

**Purpose**: Extract context from summary files and create permanent context.

**When to Use**:
- Have summary documents that should become context
- Need to convert temporary notes to permanent context
- Want to extract key concepts from larger documents
- Need to organize scattered information

**Interface**:
```bash
./router.sh harvest [source-file]
```

**Examples**:
```bash
./router.sh harvest DEVELOPER_PROFILE_ANALYSIS.md
./router.sh harvest AGENT_NAMING_BRAINSTORM.md
./router.sh harvest UX_ANALYSIS_THREE_MAIN_AGENTS.md
```

**Output**:
- Created context file path
- Space saved (original vs. harvested)
- Content structure
- Updated navigation files
- How to use the new context

#### Operation 4: EXTRACT

**Purpose**: Extract specific information from context files.

**When to Use**:
- Need specific information from context
- Creating summaries or reports
- Building context bundles for subagents
- Validating context completeness

**Interface**:
```bash
./router.sh extract [file] [what-to-extract]
```

**Examples**:
```bash
./router.sh extract code-quality.md "naming conventions"
./router.sh extract test-coverage.md "test patterns"
./router.sh extract ".opencode/context/core/" "all standards"
```

**Output**:
- Extracted information organized by topic
- Source file citations
- Relevance scores
- Usage suggestions
- Next steps

#### Operation 5: COMPRESS

**Purpose**: Compress large context files to save space.

**When to Use**:
- Context files are very large (>100 KB)
- Need to reduce disk space usage
- Archiving old context
- Preparing context for distribution

**Interface**:
```bash
./router.sh compress [target] [size-threshold]
```

**Examples**:
```bash
./router.sh compress ".opencode/context/" "100 KB"
./router.sh compress ".opencode/context/"
./router.sh compress ".opencode/context/development/" "50 KB"
```

**Output**:
- Compressed files with paths
- Space savings (before/after)
- Compression ratio
- Decompression instructions
- Manifest updates

#### Operation 6: ORGANIZE

**Purpose**: Reorganize context files by concern (what you're doing) rather than function.

**When to Use**:
- Context is scattered across multiple locations
- Need to reorganize by concern/topic
- Creating new context structure
- Consolidating related context

**Interface**:
```bash
./router.sh organize [target]
```

**Examples**:
```bash
./router.sh organize ".opencode/context/"
./router.sh organize ".opencode/context/development/"
```

**Output**:
- Current structure analysis
- Proposed new structure
- Files moved and reorganized
- Updated references
- Navigation updates
- New structure overview

#### Operation 7: CLEANUP

**Purpose**: Clean up stale, temporary, or unused context files.

**When to Use**:
- Removing temporary files (.tmp/)
- Deleting old external context (>7 days)
- Removing duplicate context
- Archiving unused context

**Interface**:
```bash
./router.sh cleanup [target] [older-than-days]
```

**Examples**:
```bash
./router.sh cleanup ".tmp/"
./router.sh cleanup ".tmp/external-context/" "7"
./router.sh cleanup ".tmp/sessions/" "3"
```

**Output**:
- Files to be deleted
- Space to be freed
- Impact analysis
- Recovery instructions (`.backup/cleanup-{date}.tar.gz`)
- Manifest updates

#### Operation 8: PROCESS

**Purpose**: Provide guided workflow for processing context.

**When to Use**:
- Need step-by-step guidance on context operations
- Processing multiple context files
- Learning context management workflow
- Automating context processing

**Interface**:
```bash
./router.sh process [goal] [scope]
```

**Examples**:
```bash
./router.sh process "organize authentication context" ".opencode/context/development/"
./router.sh process "organize all development context" ".opencode/context/development/"
./router.sh process "fetch, persist, and reference external context" ".tmp/external-context/"
```

**Output**:
- Step-by-step workflow
- Progress indicators
- Discovered context
- Processing plan
- Execution results
- Validation results
- Summary and next steps

### Router Implementation

The `router.sh` is a Bash CLI entry point that routes to the appropriate operation via a `case` statement. It currently prints a message indicating the operation and references the SKILL.md for full documentation. It provides a `--help` flag and shows all 8 operations with examples.

Key implementation details:
- Uses `set -e` for error handling
- Defines `find_project_root()` function (traverses up to find `.git` or `package.json`)
- Each operation case prints an emoji-prefixed status line and delegates to SKILL.md

### Key Principles

1. **Lazy Loading**: Discover first (glob, grep), load only what's needed, process incrementally
2. **Clear Guidance**: Explain each step, show paths/sizes, provide before/after metrics
3. **Context Reference**: Cite files when discovering, reference standards when processing
4. **Safe Operations**: Ask for confirmation before destructive ops, create backups, verify integrity

### Integration Points

- **With ContextScout**: ContextScout discovers files; this skill organizes what ContextScout finds
- **With ExternalScout**: ExternalScout fetches; this skill persists and organizes fetched docs
- **With TaskManager**: TaskManager references context; this skill ensures context files exist and are valid
- **With Other Subagents**: All subagents depend on context structure; this skill maintains and validates

---

## 2. Context7 Skill

**File**: `.opencode/skills/context7/SKILL.md` (85 lines)
**Registry**: `.opencode/skills/context7/library-registry.md` (290 lines)
**Navigation**: `.opencode/skills/context7/navigation.md` (51 lines)

### Purpose

The Context7 skill enables retrieval of current documentation for software libraries via the Context7 API (`https://context7.com/api/v2/`). It uses curl queries instead of relying on potentially outdated training data.

### Two-Step Workflow

#### Step 1: Search for the Library

```bash
curl -s "https://context7.com/api/v2/libs/search?libraryName=LIBRARY_NAME&query=TOPIC" | jq '.results[0]'
```

**Parameters**:
- `libraryName` (required): Library name (e.g., "react", "nextjs", "fastapi")
- `query` (required): Description of the topic for relevance ranking

**Response fields**:
- `id`: Library identifier for the context endpoint (e.g., `/websites/react_dev_reference`)
- `title`: Human-readable library name
- `description`: Brief description
- `totalSnippets`: Number of documentation snippets available

#### Step 2: Fetch Documentation

```bash
curl -s "https://context7.com/api/v2/context?libraryId=LIBRARY_ID&query=TOPIC&type=txt"
```

**Parameters**:
- `libraryId` (required): Library ID from step 1
- `query` (required): Specific topic to retrieve
- `type` (optional): `json` (default) or `txt` (plain text, more readable)

### Supported Libraries (from registry)

The library registry lists these categories and libraries:

**Database & ORM**:
- Drizzle ORM (`drizzle`, `drizzle-orm`) - schemas, migrations, relations, transactions
- Prisma (`prisma`) - schema, migrations, client, relations

**Authentication**:
- Better Auth (`better-auth`) - Next.js integration, Drizzle adapter, social providers, 2FA
- NextAuth.js (`nextauth`, `next-auth`) - providers, callbacks, sessions, JWT
- Clerk (`clerk`) - authentication, user management, organizations

**Frontend Frameworks**:
- Next.js (`nextjs`, `next.js`) - App Router, Server Actions, Server Components, middleware
- React (`react`, `reactjs`) - hooks, components, state, effects
- TanStack Query (`tanstack query`) - useQuery, useMutation, prefetching, caching
- TanStack Router (`tanstack router`) - routing, type-safe routes, loaders
- TanStack Start (`tanstack start`) - full-stack setup, server functions

**Infrastructure & Deployment**:
- Cloudflare Workers ("cloudflare workers") - routing, KV, Durable Objects
- AWS Lambda ("aws lambda", "lambda") - handlers, layers, triggers
- Vercel ("vercel") - deployment, edge functions, serverless

**UI Libraries & Styling**:
- Shadcn/ui ("shadcn") - components, theming, customization
- Radix UI ("radix") - primitives, accessibility
- Tailwind CSS ("tailwindcss") - configuration, utilities, dark mode

**State Management**:
- Zustand (`zustand`) - store creation, selectors, middleware
- Jotai (`jotai`) - atoms, async atoms

**Validation & Forms**:
- Zod (`zod`) - schema validation, TypeScript inference, parsing
- React Hook Form ("react hook form") - register, validation, errors

**Testing**:
- Vitest (`vitest`) - configuration, testing, mocking, coverage
- Playwright (`playwright`) - browser automation, testing

### Query Optimization Patterns

The registry includes optimized query patterns for major libraries:

- **Drizzle ORM**: e.g., `modular+schema+organization+domain+driven+design` for modular schemas
- **Better Auth**: e.g., `Drizzle+adapter+PostgreSQL+schema+generation+configuration`
- **Next.js**: e.g., `App+Router+file+conventions+layouts+pages+routing`
- **TanStack Query**: e.g., `useQuery+data+fetching+TypeScript+patterns+async`
- **Cloudflare Workers**: e.g., `KV+storage+key+value+bindings+TypeScript`

### Integration with ExternalScout

ExternalScout uses this registry to:
1. **Detect** which library the user is asking about
2. **Load** query optimization patterns for that library
3. **Build** optimized Context7 queries
4. **Fetch** live documentation
5. **Return** filtered, relevant results

### Navigation File

The navigation file provides quick-route access:
- Quick start: `README.md`
- API reference: `SKILL.md`
- Supported libraries: `library-registry.md` (lines 18-181)
- Query patterns: `library-registry.md` (lines 199-261)
- Add new library: `library-registry.md` (lines 264-279)

---

## 3. Context System Guide (User-Facing Documentation)

**File**: `/home/codey/Dev/OpenAgentsControl/CONTEXT_SYSTEM_GUIDE.md` (724 lines)

### What Is Context?

Context is the project's coding standards and patterns stored as markdown files. It tells agents:
- How you write code (naming, architecture)
- What libraries you use (React, Next.js, Tailwind)
- Your security requirements
- Your design system
- Your project-specific patterns

### The Flow

```
Your Request
    → Agent receives request
    → ContextScout discovers relevant context files
    → Agent loads context files
    → Agent follows patterns from context
    → Code matches your standards automatically
```

### Context Directory Structure

```
.opencode/context/
├── core/                           # Universal standards
│   ├── standards/
│   │   ├── code-quality.md        # Modular, functional patterns
│   │   ├── security-patterns.md   # Security best practices
│   │   ├── test-coverage.md       # Testing standards
│   │   └── documentation.md       # Documentation patterns
│   ├── workflows/
│   │   ├── design-iteration.md    # 4-stage UI design
│   │   ├── task-delegation.md     # Task delegation patterns
│   │   ├── external-libraries.md  # Library integration
│   │   └── code-review.md         # Code review process
│   └── task-management/
│       └── standards/
│           └── task-schema.md     # Task JSON schema
├── ui/                             # Design & UX
│   └── web/
│       ├── ui-styling-standards.md
│       ├── animation-patterns.md
│       ├── react-patterns.md
│       └── design-systems.md
├── development/                    # Language-specific
│   ├── backend-navigation.md
│   ├── ui-navigation.md
│   └── [language-specific patterns]
└── project-intelligence/            # YOUR custom patterns
    ├── technical-domain.md          # Tech stack & code patterns
    ├── business-domain.md           # Business context
    └── navigation.md                # Quick overview
```

### What's Included in Core Context

1. **Code Quality Standards** (`code-quality.md`): Modular design, functional patterns, pure functions, composition over inheritance, naming conventions
2. **Security Patterns** (`security-patterns.md`): Input validation, auth checks, authorization, secure error handling
3. **Design Iteration** (`design-iteration.md`): 4-stage UI workflow, approval gates
4. **External Libraries** (`external-libraries.md`): Integration patterns, configuration
5. **UI Styling Standards** (`ui-styling-standards.md`): Tailwind CSS, Flowbite
6. **React Patterns** (`react-patterns.md`): Hooks, composition, state, performance

### Adding Your Own Patterns

```bash
# Interactive wizard
/add-context

# Or edit directly (local project install)
nano .opencode/context/project-intelligence/technical-domain.md

# Global install
# nano ~/.config/opencode/context/project-intelligence/technical-domain.md
```

### Context Hierarchy (Loading Priority)

1. **Core Standards** (universal patterns) - `core/standards/code-quality.md`, `core/standards/security-patterns.md`
2. **Workflows** (how to do things) - `core/workflows/design-iteration.md`, etc.
3. **Domain-Specific** (language/framework) - `development/[language]/patterns.md`, `ui/web/react-patterns.md`
4. **Project-Specific** (YOUR patterns) - `project-intelligence/technical-domain.md`

**Project context overrides everything else!**

### Troubleshooting

- **Agent isn't following patterns**: Run `/add-context`, verify pattern is clearly written, include real example
- **Agent uses old patterns**: Run `/add-context --update` or edit `technical-domain.md`, restart agent
- **Pattern too complex**: Break into smaller patterns, include step-by-step examples

---

## 4. Claude Code Plugin Overview

**File**: `plugins/claude-code/README.md` (532 lines)
**Metadata**: `plugins/claude-code/.claude-plugin/plugin.json`

### Plugin Metadata

```json
{
  "name": "oac",
  "description": "OpenAgentsControl — multi-agent orchestration for Claude Code. Context-aware development with skills, subagents, parallel execution, and automated code review.",
  "version": "1.0.2",
  "author": { "name": "darrenhinde", "url": "https://github.com/darrenhinde" },
  "license": "MIT",
  "repository": "https://github.com/darrenhinde/OpenAgentsControl",
  "keywords": ["code-review", "tdd", "multi-agent", "context-aware", "task-management", "parallel-execution", "workflow"]
}
```

### How the Plugin Differs from OpenCode Native System

The OpenCode native system uses:
- `.opencode/` directory for agents, skills, and context
- Subagent YAML definitions with `---` frontmatter
- Bash `router.sh` scripts for skills
- Context stored in `.opencode/context/`

The Claude Code plugin uses:
- `.claude-plugin/plugin.json` for plugin metadata
- `settings.json` for model configuration (`opusplan`)
- Markdown agent definitions with `---` frontmatter (not YAML)
- `hooks.json` for event-driven automation
- Skills organized as skill-name/SKILL.md directories
- Different context root discovery: `.oac.json` config -> `.claude/context` -> `context` -> `.opencode/context`
- Flat delegation model: only main agent invokes subagents (no nested calls)

### Architecture: Skills + Subagents

**Key Principle**: Only the main agent can invoke subagents. Skills guide orchestration; subagents execute in isolated contexts via `context: fork`.

```
OAC (nested - NOT supported):
  Main Agent → TaskManager → CoderAgent → ContextScout

Claude Code (flat - CORRECT):
  Main Agent → /context-discovery skill → context-scout subagent
  Main Agent → /task-breakdown skill → task-manager subagent
  Main Agent → /code-execution skill → coder-agent subagent
```

### 6-Stage Workflow

1. **Analyze & Discover**: Understand requirements, invoke `/context-discovery`
2. **Plan & Approve**: Present plan, REQUEST APPROVAL before proceeding
3. **LoadContext**: Read all discovered context files (prevents nested discovery)
4. **Execute**: Simple tasks direct; complex tasks invoke `/task-breakdown`
5. **Validate**: Run tests, STOP on failure
6. **Complete**: Update docs, summarize changes

### Model Configuration

```json
{
  "model": "opusplan"
}
```

`opusplan` uses Opus for planning/orchestration (main agent) and Sonnet for execution (subagents). Subagents like `external-scout` and `context-scout` use `haiku` as they are lighter tasks.

### Plugin Directory Structure

```
plugins/claude-code/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── settings.json                # Model config: opusplan
├── agents/                      # 7 custom subagents
│   ├── task-manager.md
│   ├── context-scout.md
│   ├── context-manager.md
│   ├── external-scout.md
│   ├── coder-agent.md
│   ├── test-engineer.md
│   └── code-reviewer.md
├── skills/                      # 12 workflow skills
│   ├── using-oac/SKILL.md
│   ├── context-discovery/SKILL.md
│   ├── context-setup/SKILL.md
│   ├── external-research/SKILL.md
│   ├── task-breakdown/SKILL.md
│   ├── code-execution/SKILL.md
│   ├── test-generation/SKILL.md
│   ├── code-review/SKILL.md
│   ├── install-context/SKILL.md
│   ├── parallel-execution/SKILL.md
│   ├── debugger/SKILL.md
│   ├── oac-approach/SKILL.md
│   └── verification-before-completion/SKILL.md
├── commands/                    # 6 user commands
│   ├── install-context.md
│   ├── oac-help.md
│   ├── oac-status.md
│   ├── oac-cleanup.md
│   ├── brainstorm.md
│   └── debug.md
├── hooks/                       # Event-driven automation
│   ├── hooks.json
│   └── session-start.sh
├── scripts/                     # Utility scripts
│   ├── install-context.ts       # Context installer (TypeScript)
│   ├── install-context.js       # Context installer (JS fallback)
│   └── cleanup-tmp.sh           # Temporary file cleanup
└── .context-manifest.json       # Downloaded context tracking
```

---

## 5. Plugin Agents (Detail)

### 5.1 context-scout

**File**: `agents/context-scout.md` (341 lines)
**Tools**: Read, Glob, Grep (read-only)
**Model**: haiku
**Disallowed**: Write, Edit, Bash, Task

**Mission**: Discover and recommend context files from project context directories ranked by priority.

**Key Rules** (Tier 1 - Critical):
- `context_root`: Discover context root dynamically via .oac config -> .claude/context -> context -> .opencode/context
- `read_only`: ONLY use Read, Grep, Glob tools; NEVER modify files
- `verify_before_recommend`: NEVER recommend a file path not confirmed to exist
- `navigation_driven`: Follow navigation.md files top-down; never hardcode paths

**Workflow**:
1. **Step 0**: Discover Context Root using the OAC Context Discovery Protocol
2. **Step 1**: Understand intent from user request
3. **Step 2**: Follow navigation.md files top-down, verifying files exist
4. **Step 3**: Return ranked recommendations (Critical → High → Medium)

**Response Format**:
```markdown
# Context Files Found
**Context Root**: {context_root} (discovered from {source})

## Critical Priority
**File**: `{context_root}/path/to/file.md`
**Contains**: What this file covers
**Why**: Why it's critical for this task

## High Priority
...

## Medium Priority
...

**Summary**: Found {N} context files across {M} domains.
```

**Integration**: Invoked via `context: fork` by the context-discovery skill. Returns paths for the main agent to load. Does NOT load files itself.

### 5.2 context-manager

**File**: `agents/context-manager.md` (745 lines)
**Tools**: Read, Write, Glob, Grep, Bash
**Model**: sonnet

**Mission**: Manage context files, discover context locations, validate structure, and organize project-specific context.

**Key Rules** (Tier 1):
- `flexible_discovery`: Check .oac -> .claude/context -> context -> .opencode/context
- `validation_first`: Validate before adding/modifying
- `safe_operations`: Approval for destructive ops, backups for modifications
- `navigation_maintenance`: Update navigation.md when adding context

**Core Capabilities**:

1. **Context Root Discovery**: 5-step discovery chain (.oac config -> .claude/context -> context -> .opencode/context -> create fallback)
2. **Add Context from Sources**: Support GitHub repos, Git worktrees, local files/directories, URLs with options for `--category`, `--priority`, `--overwrite`, `--dry-run`
3. **Validate Context Files**: 4 checks (markdown format, metadata header, structure, navigation entry)
4. **Update Navigation**: Auto-generate/update navigation.md files when context is added
5. **Organize Context**: Detect miscategorized files and reorganize by category (core, team, custom, external, personal)

### 5.3 external-scout

**File**: `agents/external-scout.md` (374 lines)
**Tools**: Read, Write, Bash, WebFetch
**Model**: haiku

**Mission**: Fetch current documentation for external libraries, cache locally, return file paths.

**Key Rules** (Tier 1):
- `cache_first`: ALWAYS check .tmp/external-context/{package}/{topic}.md before fetching; if cached and < 7 days old, return immediately
- `read_only_after_cache`: NEVER modify cached files after creation
- `verify_cache`: Confirm every path exists before returning
- `structured_output`: Always return JSON with status, cached file paths, and metadata

**5-Step Workflow**:
1. Parse request (package, topic, context)
2. Check cache (fresh = < 7 days)
3. Fetch from Context7 API (primary) or web (fallback)
4. Cache results to `.tmp/external-context/{package}/{topic}.md` with metadata JSON
5. Return structured JSON with file paths

**Cache Structure**:
```
.tmp/external-context/
├── drizzle/
│   ├── .metadata.json
│   ├── schemas.md
│   └── queries.md
├── react/
│   ├── .metadata.json
│   └── hooks.md
└── express/
    ├── .metadata.json
    └── middleware.md
```

**Cache Freshness**: Fresh < 7 days, Stale > 7 days (re-fetch), Missing = fetch from source.

### 5.4 task-manager

**File**: `agents/task-manager.md` (378 lines)
**Tools**: Read, Write, Glob, Grep
**Model**: sonnet

**Mission**: Transform complex features into atomic, verifiable subtasks with JSON progress management.

**Key Rules** (Tier 1):
- `context_preloaded`: Context is pre-loaded by main agent; never discover yourself
- `atomic_tasks`: Each subtask completable in 1-2 hours with binary acceptance criteria
- `dependency_tracking`: Map dependencies via depends_on array, mark parallel tasks
- `json_schema`: Follow task.json schema exactly

**JSON Schema**:
- `task.json`: id, name, status, objective (max 200 chars), context_files, reference_files, exit_criteria, subtask_count, completed_count, timestamps
- `subtask_NN.json`: id, seq (01, 02...), title, status (pending/in_progress/completed/blocked), depends_on, parallel (bool), suggested_agent, context_files, reference_files, acceptance_criteria (binary), deliverables (specific file paths)

**Storage**: `.tmp/tasks/{feature}/`

### 5.5 coder-agent

**File**: `agents/coder-agent.md` (206 lines)
**Tools**: Read, Write, Edit, Glob, Grep
**Model**: sonnet

**Mission**: Execute a single coding subtask with self-review before handoff.

**7-Step Workflow**:
1. Read subtask JSON from `.tmp/tasks/{feature}/subtask_{seq}.json`
2. Load context files (standards, patterns)
3. Load reference files (existing code)
4. Update status to `in_progress` (edit, NOT write)
5. Implement deliverables following acceptance criteria
6. **Mandatory Self-Review Loop**: Type/import validation, anti-pattern scan, acceptance criteria verification
7. Mark complete via `bash .opencode/skills/task-management/router.sh complete {feature} {seq} "{summary}"`

### 5.6 test-engineer

**File**: `agents/test-engineer.md` (280 lines)
**Tools**: Read, Write, Edit, Bash
**Model**: sonnet

**Mission**: Write comprehensive tests following TDD principles.

**Key Rules**:
- `positive_and_negative`: EVERY testable behavior must have both positive and negative tests
- `arrange_act_assert`: ALL tests follow AAA pattern
- `mock_externals`: Mock ALL external dependencies; tests must be deterministic

### 5.7 code-reviewer

**File**: `agents/code-reviewer.md` (269 lines)
**Tools**: Read, Glob, Grep (read-only)
**Model**: sonnet
**Disallowed**: Write, Edit, Bash, Task

**Mission**: Perform thorough code reviews for correctness, security, and quality.

**Key Rules**:
- `context_preloaded`: Use pre-loaded standards; never request additional
- `read_only`: NEVER modify code; suggest diffs only
- `security_priority`: Security vulnerabilities ALWAYS highest priority
- `output_format`: Start with "Reviewing..., what would you devs do if I didn't check up on you?"

**Review priority**: Security → Correctness → Style → Performance

---

## 6. Plugin Skills (Detail)

### 6.1 using-oac (Auto-loaded on Session Start)

**File**: `skills/using-oac/SKILL.md` (129 lines)

This is the master skill that governs how all OAC skills are invoked. It is loaded automatically via the SessionStart hook.

**Core Rule**: If there is even a 1% chance an OAC skill applies, you ABSOLUTELY MUST invoke it. This is not negotiable or optional.

**Skill Priority Order**:
1. Process skills first (approach, debugger) - determine HOW to approach
2. Implementation skills second (context-discovery, task-breakdown, code-execution) - guide execution

**Available Skills Table**:

| Skill | When to invoke |
|-------|---------------|
| `oac:using-oac` | Loaded at session start |
| `oac:approach` | BEFORE any creative work, building features |
| `oac:context-discovery` | BEFORE implementing anything |
| `oac:task-breakdown` | Breaking complex features into subtasks |
| `oac:code-execution` | Implementing code subtasks |
| `oac:test-generation` | Creating tests |
| `oac:code-review` | Reviewing code changes |
| `oac:external-research` | Working with external libraries |
| `oac:parallel-execution` | Running multiple agents in parallel |
| `oac:debugger` | BEFORE proposing any fix for a bug |
| `oac:verification-before-completion` | BEFORE claiming work is complete |

**Red Flags** (thoughts that mean STOP):
- "This is just a simple question" -> Questions are tasks. Check for skills.
- "I need more context first" -> Skill check comes BEFORE clarifying questions.
- "Let me explore the codebase first" -> Skills tell you HOW to explore.
- "This doesn't need a formal skill" -> If a skill exists, use it.

### 6.2 context-discovery (Plugin Skill)

**File**: `skills/context-discovery/SKILL.md` (113 lines)
**Frontmatter**: `context: fork`, `agent: context-scout`

**Process**:
1. Invoke context-scout with `/context-discovery [topic]`
2. Load Critical Priority files (mandatory)
3. Load High Priority files (strongly recommended)
4. Load Medium Priority files (optional)
5. Apply standards to implementation

**Delegation Pattern**: When invoking subagents, pass discovered context files in the prompt.

**Error Handling**:
- No context files found -> Run `/install-context`
- Too many files -> Be more specific
- Which files to load -> Always Critical → High → Medium

### 6.3 context-setup (Plugin Skill)

**File**: `skills/context-setup/SKILL.md` (128 lines)

**Purpose**: Guide through installing context files from the OAC GitHub repository.

**Process**:
1. Run a quick-check command to verify environment (git, node, context status)
2. Ask two questions together: location (project or global) and profile (standard, extended, all)
3. Run the installer: `bash "{PLUGIN_ROOT}/scripts/install-context.sh" --profile={profile} [--global]`
4. Verify installation and create `.oac.json` if needed
5. Confirm: "You're ready. Every agent will now load these standards automatically."

### 6.4 external-research (Plugin Skill)

**File**: `skills/external-research/SKILL.md` (148 lines)
**Frontmatter**: `context: fork`, `agent: external-scout`

**Process**:
1. Invoke external-scout: `/external-scout <package> <topic>`
2. Check JSON response (status, cached file paths, metadata)
3. Load cached documentation from `.tmp/external-context/{package}/{topic}.md`
4. Apply current API patterns to implementation

### 6.5 oac-approach (Plugin Skill)

**File**: `skills/oac-approach/SKILL.md` (95 lines)

**Purpose**: Plan before you code. Understand request, discover context, propose concise plan, get approval.

**HARD GATE**: Do NOT write any code until user approves the proposed approach.

**Process**:
1. Understand the request (don't interrogate)
2. Discover context via `oac:context-discovery`
3. Ask clarifying questions only if genuinely ambiguous
4. Propose lightweight plan (What, How, Assumptions, Files, Context loaded)
5. Get approval
6. Hand off: Simple (1-3 files) -> implement directly; Complex (4+ files) -> invoke `oac:task-breakdown`

### 6.6 task-breakdown (Plugin Skill)

**File**: `skills/task-breakdown/SKILL.md` (159 lines)
**Frontmatter**: `context: fork`, `agent: task-manager`

Triggers when a feature touches 4+ files or has parallelizable subtasks. Creates task.json + subtask_NN.json files in `.tmp/tasks/{feature}/`.

### 6.7 code-execution (Plugin Skill)

**File**: `skills/code-execution/SKILL.md` (173 lines)
**Frontmatter**: `context: fork`, `agent: coder-agent`

8-step workflow: Read subtask JSON → Load context → Load references → Update status → Implement → Self-review (mandatory) → Mark complete → Return report.

### 6.8 debugger (Plugin Skill)

**File**: `skills/debugger/SKILL.md` (160 lines)

**Iron Law**: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

**4 Phases**:
1. Root Cause Investigation: read errors carefully, reproduce consistently, check recent changes, gather evidence, trace data flow
2. Pattern Analysis: find working examples, compare, identify differences
3. Hypothesis and Testing: form single hypothesis, test minimally, verify
4. Implementation: create failing test case, implement single fix, verify

### 6.9 verification-before-completion (Plugin Skill)

**File**: `skills/verification-before-completion/SKILL.md` (112 lines)

**Iron Law**: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.

**Gate Function**: IDENTIFY command → RUN it → READ full output → VERIFY claim → ONLY THEN make the claim.

### 6.10 parallel-execution (Plugin Skill)

**File**: `skills/parallel-execution/SKILL.md` (168 lines)

Execute multiple independent tasks simultaneously using multiple subagent invocations in a single message. Reduces implementation time by 50-80%.

### 6.11 code-review (Plugin Skill)

**File**: `skills/code-review/SKILL.md` (162 lines)
**Frontmatter**: `context: fork`, `agent: code-reviewer`

### 6.12 test-generation (Plugin Skill)

**File**: `skills/test-generation/SKILL.md` (182 lines)
**Frontmatter**: `context: fork`, `agent: test-engineer`

---

## 7. SessionStart Hook Deep Dive

**Hook config**: `hooks/hooks.json`
**Script**: `hooks/session-start.sh`

### hooks.json

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh\"",
        "timeout": 30
      }]
    }]
  }
}
```

### session-start.sh (91 lines)

This is the most critical piece of the plugin's auto-initialization. Every time a new Claude Code session starts, this script:

1. **Reads the using-oac skill content**: Reads `${PLUGIN_ROOT}/skills/using-oac/SKILL.md`

2. **Builds a skill catalogue**: Iterates over all skill directories in `${PLUGIN_ROOT}/skills/`, reads each `SKILL.md`, and extracts the `description` from frontmatter. Produces a list like:
   ```
   - oac:using-oac — Use when starting any conversation...
   - oac:approach — Use before any implementation...
   - oac:context-discovery — Use when coding standards need to be discovered...
   ...
   ```

3. **Checks for context manifest**: Looks for:
   - `${PROJECT_DIR}/.claude/.context-manifest.json` (project-local)
   - `${HOME}/.claude/.context-manifest.json` (global)
   
   If neither exists, it adds a warning message:
   ```
   <important-reminder>IN YOUR FIRST REPLY AFTER SEEING THIS MESSAGE YOU MUST TELL THE USER: 
   **No context files found.** Invoke the context-setup skill now...
   </important-reminder>
   ```

4. **Builds OAC System Paths block**: Constructs path info including:
   - Plugin Root: `${PLUGIN_ROOT}`
   - Context Discovery Protocol: `${PLUGIN_ROOT}/skills/context-discovery/context-discovery-protocol.md`

5. **Adds Context Scout instruction**: Instructs the model to proactively use `oac:context-discovery` skill at session start for any coding request.

6. **Escapes all content for JSON embedding**: Uses `escape_for_json()` which handles backslashes, double quotes, newlines, carriage returns, and tabs.

7. **Outputs dual-format JSON**: Outputs both `additional_context` and `hookSpecificOutput.additionalContext` for cross-tool compatibility (Claude Code's hookSpecificOutput and OpenCode/Cursor's additional_context).

The final injected context looks like:
```xml
<EXTREMELY_IMPORTANT>
You have OAC (OpenAgents Control).

**Below is the full content of your 'oac:using-oac' skill — your introduction to using OAC skills. 
For all other skills, use the 'Skill' tool:**

[Full using-oac SKILL.md content]

## Available OAC Skills (invoke with the Skill tool):
[Skill catalogue]

## OAC System Paths
- Plugin Root: /path/to/plugins/claude-code
- Context Discovery Protocol: /path/to/context-discovery-protocol.md

## Context Discovery
Before responding to any coding or implementation request this session, use the 'oac:context-discovery' 
skill to locate the project's coding standards. This runs once per session — do not repeat it if already done.

[Optional: No context files found warning]
</EXTREMELY_IMPORTANT>
```

This ensures every Claude Code session automatically:
- Knows about all OAC skills and when to invoke them
- Has the complete using-oac skill content loaded
- Knows the plugin root and context discovery protocol paths
- Is prompted to discover context before coding
- Alerts the user if context files are not installed

---

## 8. Plugin Commands and Hooks

### Commands

| Command | File | Purpose |
|---------|------|---------|
| `/install-context` | `commands/install-context.md` | Download context files from OAC GitHub. Supports `--profile={standard\|extended\|all}`, `--force`, `--dry-run` |
| `/oac:help` | `commands/oac-help.md` | Shows OAC workflow overview and available skills ("disable-model-invocation: true" - just invokes using-oac skill) |
| `/oac:status` | `commands/oac-status.md` | Shows plugin version, context status, .oac.json, available skills, available subagents |
| `/oac:cleanup` | `commands/oac-cleanup.md` | Cleans up `.tmp` directory (sessions >7 days, tasks >30 days, external-context >7 days). Supports `--force` |
| `/brainstorm` | `commands/brainstorm.md` | Alias for invoking oac:approach skill |
| `/debug` | `commands/debug.md` | (Likely alias for invoking debugger skill) |

### Hooks

| Hook | Event | Script | Purpose |
|------|-------|--------|---------|
| SessionStart | Session start | `session-start.sh` | Auto-loads using-oac skill, builds skill catalogue, checks context installation, injects OAC system paths |

---

## 9. Context Discovery Protocol

**File**: `plugins/claude-code/skills/context-discovery/context-discovery-protocol.md` (128 lines)

### Summary

```
.oac.json exists?  YES → read context.root → done (fast path)
                   NO  → run discovery chain
                          Found? YES → signal main agent to write .oac.json (if project-local)
                                 NO  → return setup tips
```

### Step 1: Check .oac.json (Fast Path)

```bash
Glob: .oac.json
```

If found, read `context.root` and use it. **Stop here.** If the path is invalid (no `navigation.md`), fall through.

### Step 2: Discovery Chain

Check in order, stop at first with `navigation.md`:
1. `.claude/context/navigation.md` (project-local)
2. `context/navigation.md` (project-local)
3. `.opencode/context/navigation.md` (project-local)
4. `~/.claude/context/navigation.md` (global install)
5. `{PLUGIN_ROOT}/context/navigation.md` (plugin fallback)

### Step 3: Signal .oac.json Creation

If the resolved root is project-local (`.claude/context`, `context`, `.opencode/context`), signal the main agent to write `.oac.json`:

```json
{
  "version": "1",
  "context": {
    "root": "{resolved_root}"
  }
}
```

Global (`~/.claude/context`) and plugin fallback paths do NOT get `.oac.json`.

### Step 4: No Context Found

Return setup options:
1. Run `/install-context` to download standard context bundles
2. Create `.oac.json` pointing to existing docs
3. Proceed without context

### Return Format

Always return three values:
- `context_root`: Resolved path
- `source`: `oac.json` | `discovery:claude` | `discovery:context` | `discovery:opencode` | `discovery:plugin` | `none`
- `write_oac_json`: `true` if main agent should create `.oac.json`

---

## 10. Comparative Analysis

### ContextScout vs Plugin's context-discovery

| Aspect | OpenCode (Native) | Claude Code (Plugin) |
|--------|-------------------|---------------------|
| **Context Root Discovery** | Hardcoded to `.opencode/context` | Dynamic protocol: .oac.json -> .claude/context -> context -> .opencode/context -> PLUGIN_ROOT/context |
| **Agent Type** | Subagent in `.opencode/agent/subagents/` | Markdown agent with frontmatter in `agents/` |
| **Discovery Method** | Searches `.opencode/context/` | Follows `navigation.md` files dynamically; never hardcodes paths |
| **Verification** | Immediate file search | Verifies every path exists before recommending |
| **Fast Path** | No | Yes - `.oac.json` caches context root |
| **Auto-Setup** | Manual | SessionStart hook auto-detects missing context and prompts `/install-context` |

### context-manager Skill (OpenCode) vs context-manager Agent (Plugin)

| Aspect | OpenCode Skill | Plugin Agent |
|--------|---------------|-------------|
| **Invocation** | `bash .opencode/skills/context-manager/router.sh <operation>` | Invoked via `context: fork` by skills |
| **Capabilities** | 8 operations (discover, fetch, harvest, extract, compress, organize, cleanup, process) | 5 operations (discover root, add context, validate, update navigation, organize) |
| **Tool Access** | Shell script (limited) | Read, Write, Glob, Grep, Bash |
| **Context Sources** | Local files | GitHub repos, Git worktrees, local files, URLs |
| **Validation** | Basic | Full validation (4 checks: markdown format, metadata, structure, navigation) |
| **Navigation** | Basic | Full navigation.md maintenance and auto-generation |

### ExternalScout (OpenCode) vs external-scout (Plugin)

| Aspect | OpenCode | Plugin |
|--------|----------|--------|
| **API** | Uses Context7 API via `[context7]` skill | Uses Context7 API via curl in Bash tool + WebFetch |
| **Caching** | Implicit (stores in `.tmp/external-context/`) | Explicit with metadata JSON files (.metadata.json) |
| **Freshness** | 7-day cache | 7-day cache with explicit age tracking |
| **Response Format** | Varies | Structured JSON (status, files, metadata) |
| **Source Priority** | Context7 only | Context7 (primary), WebFetch (fallback), Manual placeholder |

### Session Lifecycle Differences

**OpenCode Native**:
- No automatic session initialization
- Context discovery manual via `context-manager discover`
- External docs via `context-manager fetch`

**Claude Code Plugin**:
- SessionStart hook auto-injects using-oac skill content
- Skill catalogue built dynamically from installed skills
- Context discovery via `context: fork` to context-scout subagent
- External docs via `context: fork` to external-scout subagent
- `.oac.json` caches context root for fast-path discovery
- First-session prompt to install context if no manifest found
- Flat delegation prevents nested subagent calls

---

## Appendix: File Inventory

### Context Manager Skill
- `.opencode/skills/context-manager/SKILL.md` (568 lines) - Full skill documentation
- `.opencode/skills/context-manager/router.sh` (133 lines) - CLI entry point

### Context7 Skill
- `.opencode/skills/context7/SKILL.md` (85 lines) - API documentation
- `.opencode/skills/context7/library-registry.md` (290 lines) - Supported libraries & query patterns
- `.opencode/skills/context7/navigation.md` (51 lines) - Quick navigation

### Context System Guide
- `CONTEXT_SYSTEM_GUIDE.md` (724 lines) - User-facing documentation

### Claude Code Plugin
- `plugins/claude-code/README.md` (532 lines) - Plugin documentation
- `plugins/claude-code/.claude-plugin/plugin.json` (13 lines) - Plugin metadata
- `plugins/claude-code/settings.json` - Model config (opusplan)

**Agents (7 files)**:
- `agents/context-scout.md` (341 lines)
- `agents/context-manager.md` (745 lines)
- `agents/external-scout.md` (374 lines)
- `agents/task-manager.md` (378 lines)
- `agents/coder-agent.md` (206 lines)
- `agents/test-engineer.md` (280 lines)
- `agents/code-reviewer.md` (269 lines)

**Skills (12 directories)**:
- `skills/using-oac/SKILL.md` (129 lines)
- `skills/context-discovery/SKILL.md` (113 lines)
- `skills/context-discovery/context-discovery-protocol.md` (128 lines)
- `skills/context-setup/SKILL.md` (128 lines)
- `skills/external-research/SKILL.md` (148 lines)
- `skills/task-breakdown/SKILL.md` (159 lines)
- `skills/code-execution/SKILL.md` (173 lines)
- `skills/test-generation/SKILL.md` (182 lines)
- `skills/code-review/SKILL.md` (162 lines)
- `skills/parallel-execution/SKILL.md` (168 lines)
- `skills/debugger/SKILL.md` (160 lines)
- `skills/verification-before-completion/SKILL.md` (112 lines)
- `skills/oac-approach/SKILL.md` (95 lines)

**Commands (6 files)**:
- `commands/install-context.md` (9 lines)
- `commands/oac-help.md` (6 lines)
- `commands/oac-status.md` (25 lines)
- `commands/oac-cleanup.md` (125 lines)
- `commands/brainstorm.md` (6 lines)
- `commands/debug.md`

**Hooks (2 files)**:
- `hooks/hooks.json` (15 lines)
- `hooks/session-start.sh` (91 lines)
