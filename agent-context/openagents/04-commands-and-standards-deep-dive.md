# OpenAgentsControl: Commands & Standards Deep Dive

> Exhaustive documentation of the `/context` command interface, `/build-context-system` and `/analyze-patterns` commands, the MVI principle, frontmatter/structure/template/navigation standards, creation/compact/organize workflows, and the context system's self-referential architecture.

---

## Table of Contents

1. [The `/context` Command Interface](#1-the-context-command-interface)
2. [The `/build-context-system` Command](#2-the-build-context-system-command)
3. [The `/analyze-patterns` Command](#3-the-analyze-patterns-command)
4. [The MVI Principle (Minimal Viable Information)](#4-the-mvi-principle-minimal-viable-information)
5. [The Frontmatter Standard](#5-the-frontmatter-standard)
6. [The Structure Standard](#6-the-structure-standard)
7. [The Template Standard](#7-the-template-standard)
8. [The Codebase References Standard](#8-the-codebase-references-standard)
9. [The Creation Guide & Workflow](#9-the-creation-guide--workflow)
10. [The Compact Guide & Compaction Techniques](#10-the-compact-guide--compaction-techniques)
11. [The Organizing Context Guide](#11-the-organizing-context-guide)
12. [Navigation Design](#12-navigation-design)
13. [The Workflows Guide (Interactive Operations)](#13-the-workflows-guide-interactive-operations)
14. [Root Navigation File](#14-root-navigation-file)
15. [CODEBASE_STANDARDS.md Format](#15-codebase_standardsmd-format)
16. [Self-Referential Architecture](#16-self-referential-architecture)

---

## 1. The `/context` Command Interface

**File**: `.opencode/command/context.md` (309 lines)

### 1.1 Frontmatter

```yaml
---
description: Context system manager - harvest summaries, extract knowledge, organize context
tags:
  - context
  - knowledge-management
  - harvest
dependencies:
  - subagent:context-organizer
  - subagent:contextscout
---
```

### 1.2 Critical Rules (Absolute Priority)

The command defines four critical rules enforced with `priority="absolute"` and `enforcement="strict"`:

| Rule ID | Rule | Description |
|---------|------|-------------|
| `mvi_strict` | Files `<200 lines` | Extract core concepts only (1-3 sentences), 3-5 key points, minimal example, reference link |
| `approval_gate` | Always present approval UI before deleting/archiving | Letter-based selection (A B C or 'all'). NEVER auto-delete |
| `function_structure` | Always organize by function | concepts/, examples/, guides/, lookup/, errors/ (not flat files) |
| `lazy_load` | Always read required context files BEFORE executing | From `.opencode/context/core/context-system/` |

### 1.3 Execution Priority Tiers

```xml
<execution_priority>
  <tier level="1" desc="Safety & MVI">
    - Files <200 lines (@critical_rules.mvi_strict)
    - Show approval before cleanup (@critical_rules.approval_gate)
    - Function-based structure (@critical_rules.function_structure)
    - Load context before operations (@critical_rules.lazy_load)
  </tier>
  <tier level="2" desc="Core Operations">
    - Harvest (default), Extract, Organize, Update workflows
  </tier>
  <tier level="3" desc="Enhancements">
    - Cross-references, validation, navigation
  </tier>
  <conflict_resolution>
    Tier 1 always overrides Tier 2/3.
  </conflict_resolution>
</execution_priority>
```

**Conflict Resolution**: Tier 1 always overrides Tier 2/3.

### 1.4 Default Behavior (No Arguments)

When invoked as `/context` (no arguments), a two-stage workflow runs:

**Stage 1: QuickScan**
- Scans workspace for: `*OVERVIEW.md`, `*SUMMARY.md`, `SESSION-*.md`, `CONTEXT-*.md`
- Scans files in `.tmp/` directory
- Scans files >2KB in root directory

**Stage 2: Report**
- Displays what was found with file sizes
- Recommends `/context harvest` as default action
- Lists alternative options: `extract`, `organize`, `help`

**Purpose**: Quick tidy-up. Default assumes you want to harvest summaries and compact workspace.

### 1.5 All Subcommands (Verbatim Definitions)

#### Primary Operations

**`/context harvest [path]`** (marked as Most Common)
- Extract knowledge from AI summaries → permanent context
- Clean workspace (archive/delete summaries)
- **Reads**: `operations/harvest.md` + `standards/mvi.md`

**`/context compact {file}`**
- Minimize verbose file to MVI format
- **Reads**: `guides/compact.md` + `standards/mvi.md`

#### Secondary: Custom Context Creation

**`/context extract from {source}`**
- Extract context from docs/code/URLs
- **Reads**: `operations/extract.md` + `standards/mvi.md` + `guides/compact.md`

**`/context organize {category}`**
- Restructure flat files → function-based folders
- **Reads**: `operations/organize.md` + `standards/structure.md`

**`/context update for {topic}`**
- Update context when APIs/frameworks change
- **Reads**: `operations/update.md` + `guides/workflows.md`

**`/context error for {error}`**
- Add recurring error to knowledge base
- **Reads**: `operations/error.md` + `standards/templates.md`

**`/context create {category}`**
- Create new context category with structure
- **Reads**: `guides/creation.md` + `standards/structure.md` + `standards/templates.md`

#### Migration

**`/context migrate`**
- Copy project-intelligence from global (`~/.config/opencode/context/`) to local (`.opencode/context/`)
- For users who installed globally but want project-specific, git-committed context
- Shows diff if local files already exist, asks before overwriting
- Optionally cleans up global project-intelligence after migration
- **Reads**: `standards/mvi.md`

#### Utility Operations

**`/context map [category]`**
- View current context structure, file counts

**`/context validate`**
- Check integrity, references, file sizes

**`/context help`**
- Show all operations with examples

### 1.6 Lazy Loading Map (Verbatim)

Every operation only loads the context files it needs:

```xml
<lazy_load_map>
  <operation name="default">
    Read: operations/harvest.md, standards/mvi.md
  </operation>
  
  <operation name="harvest">
    Read: operations/harvest.md, standards/mvi.md, guides/workflows.md
  </operation>
  
  <operation name="compact">
    Read: guides/compact.md, standards/mvi.md
  </operation>
  
  <operation name="extract">
    Read: operations/extract.md, standards/mvi.md, guides/compact.md, guides/workflows.md
  </operation>
  
  <operation name="organize">
    Read: operations/organize.md, standards/structure.md, guides/workflows.md
  </operation>
  
  <operation name="update">
    Read: operations/update.md, guides/workflows.md, standards/mvi.md
  </operation>
  
  <operation name="error">
    Read: operations/error.md, standards/templates.md, guides/workflows.md
  </operation>
  
  <operation name="create">
    Read: guides/creation.md, standards/structure.md, standards/templates.md
  </operation>
  
  <operation name="migrate">
    Read: standards/mvi.md
  </operation>
</lazy_load_map>
```

**All files located in**: `.opencode/context/core/context-system/`

### 1.7 Subagent Routing

```xml
<route operations="harvest|extract|organize|update|error|create|migrate" to="ContextOrganizer">
  Pass: operation name, arguments, lazy load map
  Subagent loads: Required context files from .opencode/context/core/context-system/
  Subagent executes: Multi-stage workflow per operation
</route>

<route operations="map|validate" to="ContextScout">
  Pass: operation name, arguments
  Subagent executes: Read-only analysis and reporting
</route>
```

### 1.8 Quick Reference (Verbatim)

**Structure:**
```
.opencode/context/core/context-system/
├── operations/     # How to do things (harvest, extract, organize, update)
├── standards/      # What to follow (mvi, structure, templates)
└── guides/         # Step-by-step (workflows, compact, creation)
```

**MVI Principle (Quick):**
- Core concept: 1-3 sentences
- Key points: 3-5 bullets
- Minimal example: <10 lines
- Reference link: to full docs
- File size: <200 lines

**Function-Based Structure (Quick):**
```
{category}/
├── navigation.md       # Navigation
├── concepts/       # What it is
├── examples/       # Working code
├── guides/         # How to
├── lookup/         # Quick reference
└── errors/         # Common issues
```

### 1.9 Success Criteria

After any operation:
- [ ] All files <200 lines? (@critical_rules.mvi_strict)
- [ ] Function-based structure used? (@critical_rules.function_structure)
- [ ] Approval UI shown for destructive ops? (@critical_rules.approval_gate)
- [ ] Required context loaded? (@critical_rules.lazy_load)
- [ ] navigation.md updated?
- [ ] Files scannable in <30 seconds?

### 1.10 Examples (Verbatim)

```bash
# Default (Quick Scan)
/context
# Scans workspace, suggests harvest if summaries found

# Harvest Summaries
/context harvest
/context harvest .tmp/
/context harvest OVERVIEW.md

# Extract from Docs
/context extract from docs/api.md
/context extract from https://react.dev/hooks

# Organize Existing
/context organize development/
/context organize development/ --dry-run

# Update for Changes
/context update for Next.js 15
/context update for React 19 breaking changes

# Migrate Global to Local
/context migrate
# Copies project-intelligence from ~/.config/opencode/context/ to .opencode/context/
# Shows what will be copied, asks for approval before proceeding
```

---

## 2. The `/build-context-system` Command

**File**: `.opencode/command/build-context-system.md` (861 lines)

### 2.1 Purpose

An interactive system builder that creates complete context-aware AI architectures tailored to user domains. It guides users through an interview process and then generates a full `.opencode/` folder system with orchestrators, subagents, context files, workflows, and commands.

### 2.2 Frontmatter

```yaml
---
description: "Interactive system builder that creates complete context-aware AI architectures tailored to user domains"
---
```

### 2.3 Context & Role

```xml
<context>
  <system_context>AI-powered context-aware system builder using hierarchical agent patterns, XML optimization, and research-backed architecture</system_context>
  <domain_context>System architecture design with modular context management, intelligent routing, and workflow orchestration</domain_context>
  <task_context>Transform user requirements into complete .opencode folder systems with orchestrators, subagents, context files, workflows, and commands</task_context>
  <execution_context>Interactive interview process followed by automated generation of tailored architecture</execution_context>
</context>

<role>Expert System Architect specializing in context-aware AI systems, hierarchical agent design, and modular knowledge organization</role>
```

### 2.4 Complete Stage-by-Stage Flow

#### Stage 0: DetectExistingProject

| Step | Action |
|------|--------|
| 1 | Check if `.opencode/` directory exists |
| 2 | Scan for existing agents (`agent/*.md`, `agent/subagents/*.md`) |
| 3 | Scan for existing commands (`command/*.md`) |
| 4 | Scan for existing context files (`context/*/*.md`) |
| 5 | Scan for existing workflows (`workflows/*.md`) |
| 6 | Identify existing system capabilities |
| 7 | Present merge options to user |

**Known agents and their capabilities**:
- `opencoder`: Code analysis, file operations
- `task-manager`: Task tracking, project management
- `workflow-orchestrator`: Workflow coordination
- `image-specialist`: Image generation/editing
- `build-agent`: Build validation, type checking
- `tester`: Test authoring, TDD
- `reviewer`: Code review, quality assurance
- `documentation`: Documentation authoring
- `coder-agent`: Code generation

**Merge Strategy Options**:

| Option | Name | Behavior |
|--------|------|----------|
| 1 | **Extend Existing System** (Recommended) | Keep all existing files; Add new agents/workflows/commands; Merge context files intelligently; Integrate new with existing capabilities; Create unified orchestrator |
| 2 | **Create Separate System** | Keep existing system intact; Create new system in separate namespace; Both systems coexist independently |
| 3 | **Replace Existing System** | Backup existing to `.opencode.backup.{timestamp}/`; Create fresh system |
| 4 | **Cancel** | Exit without changes |

#### Stage 1: InitiateInterview

- Greet user and explain the system building process
- Parse initial domain from `$ARGUMENTS` if provided
- Present interview structure (5-6 phases)
- Set expectations for output

For fresh builds, the process is:
- Phase 1: Domain & Purpose (2-3 questions)
- Phase 2: Use Cases & Workflows (3-4 questions)
- Phase 3: Complexity & Scale (2-3 questions)
- Phase 4: Integration & Tools (2-4 questions)
- Phase 5: Review & Confirmation

Deliverables for fresh build:
- Complete `.opencode/` folder structure
- Main orchestrator agent for domain
- 3-5 specialized subagents
- Organized context files (domain, processes, standards, templates)
- 2-3 primary workflows
- Custom slash commands
- Documentation and testing guide

#### Stage 2: GatherDomainInfo (Questions 1-3)

| Question | What It Asks | What It Captures |
|----------|-------------|-----------------|
| Q1 | What is your primary domain or industry? | `domain_name`, `industry_type` |
| Q2 | What is the primary purpose of your AI system? | `primary_purpose`, `automation_goals` |
| Q3 | Who are the primary users of this system? | `user_personas`, `expertise_level` |

#### Stage 2.5: DetectDomainType

Classifies the domain:

| Classification | Keywords | Purpose | Users | Existing Agent Match |
|---------------|----------|---------|-------|---------------------|
| `development` | software, code, devops, testing, build, deploy, API, programming, git, CI/CD | generate code, review, test, build, deploy | developers, engineers, QA | opencoder, build-agent, tester, reviewer, coder-agent, documentation |
| `business` | e-commerce, retail, customer, support, sales, marketing, content, finance, HR | automate processes, customer service, content, reports, analytics | business users, marketers, support teams, executives | task-manager, workflow-orchestrator, image-specialist, documentation |
| `hybrid` | data engineering, product management, analytics, platform | both technical and business outcomes | mix of technical and business | All agents may be relevant |

Adapts subsequent interview questions based on detected domain type.

#### Stage 3: IdentifyUseCases (Questions 4-6)

| Question | What It Asks | What It Captures |
|----------|-------------|-----------------|
| Q4 | What are your top 3-5 use cases or tasks? | `use_cases[]`, `task_descriptions[]` |
| Q5 | For each use case, what is the typical complexity? | `complexity_map{use_case: complexity_level}` (simple/moderate/complex) |
| Q6 | Are there dependencies or sequences between use cases? | `workflow_dependencies[]`, `task_sequences[]` |

#### Stage 4: AssessComplexity (Questions 7-9)

| Question | What It Asks | What It Captures |
|----------|-------------|-----------------|
| Q7 | How many specialized agents do you anticipate needing? | `estimated_agent_count`, `specialization_areas[]` (guidance: 2-3 simple, 4-6 moderate, 7+ complex) |
| Q8 | What types of knowledge does your system need? | `knowledge_types[]`, `context_categories[]` (domain/process/standards/template knowledge) |
| Q9 | Will your system need to maintain state or history? | `state_management_level`, `history_requirements` (stateless/project_based/full_history) |

#### Stage 5: IdentifyIntegrations (Questions 10-12)

| Question | What It Asks | What It Captures |
|----------|-------------|-----------------|
| Q10 | What external tools or platforms to integrate with? | `integrations[]`, `api_requirements[]`, `tool_dependencies[]` |
| Q11 | What file operations will your system perform? | `file_operations_level`, `storage_requirements` (read_only/read_write/full_management) |
| Q12 | Do you need custom slash commands? | `custom_commands[]`, `command_patterns[]` |

#### Stage 6: ReviewAndConfirm

Compiles all gathered info into a system architecture summary including:
- Domain, Purpose, Users
- Use Cases with complexity ratings
- System Components (agents, context files, workflows, commands)
- Integrations
- Estimated file counts and structure
- Total files, agent files, context files, workflow files, command files, documentation files

User chooses: Proceed / Revise / Cancel

#### Stage 7: GenerateSystem

Routes to `@system-builder` with Level 2 (Filtered Context):
- Passes: interview responses, architecture summary, component specifications, file structure plan
- Expects back: complete file structure, validation report, documentation
- Validates generated structure

#### Stage 8: DeliverSystem

Presents completed system with:
- Generated folder structure visualization
- Quick Start commands
- Key Components listing (orchestrator, subagents, workflows, commands)
- Testing Checklist (7 items)
- Documentation locations
- Next Steps (5 items)
- Tips for Success

### 2.5 Routing Intelligence

Three levels of context allocation:
- **Level 1**: User provides clear, complete requirements → Requirements only, minimal guidance
- **Level 2** (most common): Standard interview → Interview questions + architecture patterns + examples
- **Level 3**: Complex domain requiring extensive guidance → Full interview + detailed examples + reference architectures

Two routing targets:
- `@system-builder`: When user confirms architecture (Level 2 context)
- `@DomainAnalyzer`: When domain unclear or complex (Level 1 context)

### 2.6 Interview Patterns

| Pattern | Description |
|---------|-------------|
| Progressive Disclosure | Start broad, then drill into specifics based on responses |
| Adaptive Questioning | Adjust question complexity based on user's technical level |
| Example Driven | Provide concrete examples for every question |
| Validation Checkpoints | Summarize and confirm understanding after each phase |

### 2.7 Architecture Principles

| Principle | Description |
|-----------|-------------|
| Modular Design | Generate small, focused files (50-200 lines) |
| Hierarchical Organization | Main orchestrator coordinates specialized subagents (manager-worker pattern) |
| Context Efficiency | 3-level allocation (80% Level 1, 20% Level 2, rare Level 3) |
| Workflow Driven | Design workflows first, then create agents to execute |
| Research Backed | Apply Stanford/Anthropic XML patterns and optimal component ordering |

---

## 3. The `/analyze-patterns` Command

**File**: `.opencode/command/analyze-patterns.md` (221 lines)

### 3.1 Frontmatter

```yaml
---
id: analyze-patterns
name: analyze-patterns
description: "Analyze codebase for patterns and similar implementations"
type: command
category: analysis
version: 1.0.0
---
```

### 3.2 Usage & Parameters

```bash
/analyze-patterns [--pattern=<pattern>] [--language=<lang>] [--depth=<level>] [--output=<format>]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--pattern` | string | No | Pattern name or regex (e.g., "singleton", "factory", "error-handling") |
| `--language` | string | No | Filter by language: js, ts, py, go, rust, java, etc. |
| `--depth` | string | No | `shallow` (current dir) \| `medium` (src/) \| `deep` (entire repo) |
| `--output` | string | No | `text` (default) \| `json` \| `markdown` |

### 3.3 Behavior

**Pattern Search**:
- Searches codebase for pattern matches using regex + semantic analysis
- Identifies similar implementations across files
- Groups results by pattern type + similarity score
- Suggests refactoring opportunities

**Analysis Output**:
- Pattern occurrences with file locations + line numbers
- Similarity metrics (how similar implementations are)
- Refactoring suggestions (consolidate, extract, standardize)
- Code quality insights (duplication, inconsistency)

### 3.4 Result Format

```
Pattern Analysis Report
=======================

Pattern: [pattern_name]
Occurrences: [count]
Files: [file_list]

Implementations:
  1. [file:line] - [description] (similarity: X%)
  2. [file:line] - [description] (similarity: Y%)
  ...

Refactoring Suggestions:
  - [suggestion 1]
  - [suggestion 2]
  ...

Quality Insights:
  - [insight 1]
  - [insight 2]
  ...
```

### 3.5 Processing Steps

1. Parse command parameters
2. Validate pattern syntax (regex or predefined)
3. Search codebase using glob + grep tools
4. Analyze semantic similarity of matches
5. Group results by pattern + similarity
6. Generate refactoring suggestions
7. Format output per requested format
8. Return analysis report

### 3.6 Predefined Patterns

**JavaScript/TypeScript**: `singleton`, `factory`, `observer`, `error-handling`, `async-patterns`, `api-endpoint`, `middleware`

**Python**: `decorator`, `context-manager`, `error-handling`, `async-patterns`, `class-patterns`

**Go**: `interface-patterns`, `error-handling`, `goroutine-patterns`, `middleware`

Users can also provide custom regex patterns for domain-specific analysis.

### 3.7 Output Formats

**JSON**:
```json
{
  "pattern": "error-handling",
  "occurrences": 12,
  "files": ["file1.ts", "file2.ts"],
  "implementations": [
    {
      "file": "file1.ts",
      "line": 42,
      "description": "try-catch block",
      "similarity": 0.95
    }
  ],
  "suggestions": ["Consolidate error handling", "Extract to utility"]
}
```

**Markdown**: Formatted for documentation + sharing

### 3.8 Integration

- **Delegates to**: `opencoder` (primary agent)
- **Profile Assignment**: Included in Developer, Full, Advanced profiles; NOT in Business profile

### 3.9 Registry Entry

```json
{
  "id": "analyze-patterns",
  "name": "analyze-patterns",
  "type": "command",
  "category": "analysis",
  "description": "Analyze codebase for patterns and similar implementations",
  "delegates_to": ["opencoder"],
  "parameters": ["pattern", "language", "depth", "output"]
}
```

---

## 4. The MVI Principle (Minimal Viable Information)

**File**: `.opencode/context/core/context-system/standards/mvi.md` (151 lines)
**Context Header**: `<!-- Context: core/mvi | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->`

### 4.1 Core Idea

> Extract the **minimum information** needed for an AI agent to understand and use a concept.

The formula is:
```
Core Concept (1-3 sentences)
  ↓
Key Points (3-5 bullets)
  ↓
Quick Example (5-10 lines)
  ↓
Reference Link (full docs)
  ↓
Related Files (cross-refs)
```

**Goal**: Scannable in <30 seconds. Reference full docs, don't duplicate them.

### 4.2 What to Extract (Whitelist)

| Category | Rule |
|----------|------|
| Core definitions | 1-3 sentences |
| Key properties | 3-5 bullets |
| Minimal example | 5-10 lines of code |
| Common patterns | 2-3 bullets |
| Critical gotchas | 1-2 bullets |
| Reference links | Where to learn more |

### 4.3 What to Skip (Blacklist)

| Category | Rule |
|----------|------|
| Verbose explanations | Link to docs instead |
| Complete API docs | Summarize + reference |
| Implementation details | Show minimal example + reference |
| Historical context | Unless critical to understanding |
| Marketing content | Just the facts |
| Duplicate information | Say it once, reference elsewhere |

### 4.4 MVI Example: JWT Authentication

**Too Verbose** (400+ lines): Full RFC explanation of JWT, every algorithm, every edge case.

**MVI Compliant** (~50 lines):
```markdown
# Concept: JWT Authentication

**Core Idea**: Stateless authentication using JSON Web Tokens signed
with a secret key. Token contains user data (payload) that server can
trust because signature is verified.

**Key Points**:
- Token has 3 parts: header.payload.signature (Base64 encoded)
- Server verifies signature to trust payload without database lookup
- No session storage needed (stateless)
- Tokens expire (include `exp` claim)
- Store in httpOnly cookie or Authorization header

**Quick Example**:
```js
// Sign token
const token = jwt.sign(
  { userId: 123, role: 'admin' },
  SECRET_KEY,
  { expiresIn: '1h' }
)

// Verify token
const decoded = jwt.verify(token, SECRET_KEY)
console.log(decoded.userId) // 123
```

**Reference**: https://jwt.io/introduction

**Related**:
- examples/jwt-auth-example.md
- guides/implementing-jwt.md
- errors/auth-errors.md
```

### 4.5 File Size Limits (Strict Enforcement)

| File Type | Maximum Lines |
|-----------|--------------|
| Concept files | **100 lines** |
| Example files | **80 lines** |
| Guide files | **150 lines** |
| Lookup files | **100 lines** |
| Error files | **150 lines** |
| README files | **100 lines** |

**Rationale**: Forces brevity. If you need more, split into multiple files or reference external docs.

### 4.6 Validation Checklist

- [ ] Core concept is 1-3 sentences?
- [ ] Key points are 3-5 bullets?
- [ ] Example is <10 lines of code?
- [ ] Reference link is included?
- [ ] File is <200 lines total?
- [ ] Can be scanned in <30 seconds?

If any answer is "no", apply more compression.

### 4.7 Related Files

- `structure.md` - Where files go
- `compact.md` - How to minimize
- `templates.md` - Standard formats
- `creation.md` - File creation rules

---

## 5. The Frontmatter Standard

**File**: `.opencode/context/core/context-system/standards/frontmatter.md` (64 lines)

### 5.1 Required Format (Strict Enforcement)

**ALL context files MUST start with:**

```markdown
<!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->
```

This is enforced via:
```xml
<rule id="frontmatter_required" enforcement="strict">
  ALL context files MUST start with:
  
  <!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->
</rule>
```

### 5.2 Component Definitions

| Component | Format | Description | Examples |
|-----------|--------|-------------|---------|
| **Category/Function** | `{category}/{function}` | Category = domain, Function = file type | `ecommerce/concepts`, `development/examples`, `core/standards` |
| **Priority** | `critical` \| `high` \| `medium` \| `low` | Triggers loading priority | See below |
| **Version** | `X.Y` | Start 1.0, increment on changes | `1.0`, `1.2`, `2.0` |
| **Updated** | `YYYY-MM-DD` | ISO 8601 format, must match metadata section | `2026-01-27` |

### 5.3 Priority Level Definitions

| Priority | % Use Cases | Meaning |
|----------|------------|---------|
| `critical` | 80% | Business logic, core concepts — always loaded |
| `high` | 15% | Common workflows, examples — frequently referenced |
| `medium` | 4% | Edge cases — useful but not essential |
| `low` | 1% | Rare scenarios — nice-to-have |

### 5.4 Examples

```markdown
<!-- Context: ecommerce/concepts | Priority: critical | Version: 1.0 | Updated: 2026-01-27 -->
<!-- Context: payments/guides | Priority: high | Version: 1.2 | Updated: 2026-01-27 -->
<!-- Context: development/examples | Priority: medium | Version: 1.0 | Updated: 2026-01-27 -->
```

### 5.5 Validation Checklist

- [ ] Frontmatter is first line?
- [ ] Format exact: `<!-- Context: ... -->`?
- [ ] Priority is critical\|high\|medium\|low?
- [ ] Version is X.Y?
- [ ] Date is YYYY-MM-DD?

---

## 6. The Structure Standard

**File**: `.opencode/context/core/context-system/standards/structure.md` (240 lines)
**Context Header**: `<!-- Context: core/structure | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->`

### 6.1 Core Structure Rule (Strict Enforcement)

```xml
<rule id="function_structure" enforcement="strict">
  ALWAYS organize by function (what info does), not just by topic.
  
  Required folders:
  - concepts/  - Core ideas, definitions, "what is it?"
  - examples/  - Minimal working code
  - guides/    - Step-by-step workflows
  - lookup/    - Quick reference tables, commands, paths
  - errors/    - Common issues, gotchas, fixes
</rule>
```

### 6.2 Canonical Directory Layout

```
.opencode/context/{category}/
├── navigation.md              # Navigation map (REQUIRED)
├── concepts/              # What it is
│   └── {topic}.md
├── examples/              # Working code
│   └── {example}.md
├── guides/                # How to do it
│   └── {guide}.md
├── lookup/                # Quick reference
│   └── {reference}.md
└── errors/                # Common issues
    └── {framework}.md
```

### 6.3 Folder Purposes

#### concepts/
- **Purpose**: Core ideas, definitions, "what is it?"
- **Contains**: Fundamental concepts, design patterns, architecture decisions, system principles
- **Examples**: `authentication.md`, `state-management.md`, `mvi-principle.md`

#### examples/
- **Purpose**: Minimal working code examples
- **Contains**: Code snippets that work as-is, minimal reproductions, common patterns in action
- **Examples**: `jwt-auth-example.md`, `react-hooks-example.md`, `api-call-example.md`
- **Rule**: Examples should be <30 lines of code, fully functional

#### guides/
- **Purpose**: Step-by-step workflows, "how to do X"
- **Contains**: Numbered procedures, setup instructions, implementation workflows, migration guides
- **Examples**: `setting-up-auth.md`, `deploying-api.md`, `migrating-to-v2.md`
- **Rule**: Steps should be actionable (not theoretical)

#### lookup/
- **Purpose**: Quick reference tables, commands, paths
- **Contains**: Command lists, file locations, API endpoints, configuration options, keyboard shortcuts
- **Examples**: `cli-commands.md`, `file-locations.md`, `api-endpoints.md`
- **Rule**: Must be in table/list format (scannable)

#### errors/
- **Purpose**: Common errors, gotchas, edge cases
- **Contains**: Error messages + fixes, common pitfalls, edge cases, troubleshooting
- **Examples**: `react-errors.md`, `nextjs-build-errors.md`, `auth-errors.md`
- **Rule**: Group by framework/topic, not one file per error

### 6.4 navigation.md Requirement (Strict)

```xml
<rule id="readme_required" enforcement="strict">
  Every context category MUST have navigation.md at its root with:
  1. Purpose (1-2 sentences)
  2. Navigation tables for each function folder
  3. Priority levels (critical/high/medium/low)
  4. Loading strategy (what to load for common tasks)
</rule>
```

### 6.5 Categorization Decision Table

| Question | Folder |
|----------|--------|
| Does it explain **what** something is? | `concepts/` |
| Does it show **working code**? | `examples/` |
| Does it explain **how to do** something? | `guides/` |
| Is it **quick reference** data? | `lookup/` |
| Does it document an **error/issue**? | `errors/` |

### 6.6 Anti-Patterns

**Flat Structure** (BAD):
```
development/
├── authentication.md     # Is this a concept or guide?
├── jwt-example.md
├── setting-up-auth.md
├── auth-errors.md
└── api-endpoints.md
```
Problem: Hard to discover. File purpose is ambiguous.

**Function-Based** (GOOD):
```
development/
├── navigation.md
├── concepts/
│   └── authentication.md
├── examples/
│   └── jwt-example.md
├── guides/
│   └── setting-up-auth.md
├── lookup/
│   └── api-endpoints.md
└── errors/
    └── auth-errors.md
```
Benefit: Instantly know file purpose by location.

### 6.7 Validation Checklist

- [ ] All categories have navigation.md?
- [ ] Files are in function folders (not flat)?
- [ ] README has navigation tables?
- [ ] Priority levels assigned?
- [ ] Loading strategy documented?

---

## 7. The Template Standard

**File**: `.opencode/context/core/context-system/standards/templates.md` (396 lines)

### 7.1 Template Overview

| Type | Max Lines | Required Sections |
|------|-----------|-------------------|
| Concept | 100 | Purpose, Core Idea (1-3 sentences), Key Points (3-5), Example (<10 lines), Reference, Related |
| Example | 80 | Purpose, Use Case, Code (10-30 lines), Explanation, Related |
| Guide | 150 | Purpose, Prerequisites, Steps (4-7), Verification, Related |
| Lookup | 100 | Purpose, Tables/Lists, Commands, Related |
| Error | 150 | Purpose, Per-error: Symptom, Cause, Solution, Prevention, Reference, Related |
| Navigation | 100 → 200-300 tokens | Purpose, Navigation tables (all 5 folders), Loading Strategy, Statistics |

### 7.2 Template 1: Concept

```markdown
<!-- Context: {category}/concepts | Priority: {critical|high|medium|low} | Version: 1.0 | Updated: YYYY-MM-DD -->
# Concept: {Name}

**Purpose**: [1 sentence]
**Last Updated**: {YYYY-MM-DD}

## Core Idea
[1-3 sentences]

## Key Points
- Point 1
- Point 2
- Point 3

## When to Use
- Use case 1
- Use case 2

## Quick Example
```lang
[<10 lines]
```

## 📂 Codebase References

**Business Logic** (if business domain):
- `path/to/rules.ts` - {3-10 word description}

**Implementation**:
- `path/to/main.ts` - {3-10 word description}

**Models/Types**:
- `path/to/model.ts` - {3-10 word description}

**Tests**:
- `path/to/test.ts` - {3-10 word description}

## Deep Dive
**Reference**: [Link or "See implementation above"]

## Related
- concepts/x.md
- examples/y.md
```

### 7.3 Template 2: Example

```markdown
<!-- Context: {category}/examples | Priority: {high|medium} | Version: 1.0 | Updated: YYYY-MM-DD -->
# Example: {What It Shows}

**Purpose**: [1 sentence]
**Last Updated**: {YYYY-MM-DD}

## Use Case
[2-3 sentences]

## Code
```lang
[10-30 lines]
```

## Explanation
1. Step 1
2. Step 2
3. Step 3

**Key points**:
- Detail 1
- Detail 2

## 📂 Codebase References

**Full Implementation**:
- `path/to/real-implementation.ts` - {Production version}

**Related Code**:
- `path/to/helper.ts` - {Helper utilities}

**Tests**:
- `path/to/test.ts` - {Tests demonstrating pattern}

## Related
- concepts/x.md
```

### 7.4 Template 3: Guide

```markdown
<!-- Context: {category}/guides | Priority: {critical|high|medium} | Version: 1.0 | Updated: YYYY-MM-DD -->
# Guide: {Action}

**Purpose**: [1 sentence]
**Last Updated**: {YYYY-MM-DD}

## Prerequisites
- Requirement 1
- Requirement 2

**Estimated time**: X min

## Steps

### 1. {Step}
```bash
{command}
```
**Expected**: [result]
**Implementation**: `path/to/step.ts`

### 2. {Step}
[Repeat 4-7 steps]

## Verification
```bash
{verify command}
```

## 📂 Codebase References

**Workflow Orchestration**:
- `path/to/workflow.ts` - {Main workflow coordinator}

**Business Logic** (if applicable):
- `path/to/rules.ts` - {Process validation rules}

**Integration Points**:
- `path/to/api-client.ts` - {External integration}

**Tests**:
- `path/to/workflow.test.ts` - {End-to-end tests}

## Troubleshooting
| Issue | Solution |
|-------|----------|
| Problem | Fix |

## Related
- concepts/x.md
```

### 7.5 Template 4: Lookup

```markdown
<!-- Context: {category}/lookup | Priority: {high|medium} | Version: 1.0 | Updated: YYYY-MM-DD -->
# Lookup: {Reference Type}

**Purpose**: Quick reference for {desc}
**Last Updated**: {YYYY-MM-DD}

## {Section}
| Item | Value | Desc | Code |
|------|-------|------|------|
| x | y | z | `path/to/file.ts` |

## Commands
```bash
# Description
{command}
```

## Paths
```
{path} - {desc}
```

## 📂 Codebase References

**Validation/Enforcement**:
- `path/to/validator.ts` - {Validation logic}

**Configuration**:
- `path/to/config.ts` - {Configuration settings}

**Tests**:
- `path/to/test.ts` - {Validation tests}

## Related
- concepts/x.md
```

### 7.6 Template 5: Error

```markdown
<!-- Context: {category}/errors | Priority: {high|medium} | Version: 1.0 | Updated: YYYY-MM-DD -->
# Errors: {Framework}

**Purpose**: Common errors for {framework}
**Last Updated**: {YYYY-MM-DD}

## Error: {Name}

**Symptom**:
```
{error message}
```

**Cause**: [1-2 sentences]

**Solution**:
1. Step 1
2. Step 2

**Code**:
```lang
// ❌ Before
{bad}

// ✅ After
{fixed}
```

**Prevention**: [how to avoid]
**Frequency**: common/occasional/rare

**Code References**:
- Error thrown: `path/to/error-source.ts`
- Error handler: `path/to/error-handler.ts`
- Prevention: `path/to/validator.ts`

---

[Repeat for 5-10 errors]

## 📂 Codebase References

**Error Definitions**:
- `path/to/error-types.ts` - {Error class definitions}

**Error Handling**:
- `path/to/error-handler.ts` - {Error handler}

**Prevention Logic**:
- `path/to/validator.ts` - {Validation preventing errors}

**Tests**:
- `path/to/error-handling.test.ts` - {Error handling tests}

## Related
- concepts/x.md
```

### 7.7 Template 6: Navigation (Replaces README.md)

**Note**: Use `navigation.md` instead of `README.md` for better discoverability.
**Target**: 200-300 tokens.

```markdown
# {Category} Navigation

**Purpose**: [1 sentence]

---

## Structure

```
{category}/
├── navigation.md
├── {subcategory}/
│   ├── navigation.md
│   └── {files}.md
```

---

## Quick Routes

| Task | Path |
|------|------|
| **{Task 1}** | `{path}` |
| **{Task 2}** | `{path}` |
| **{Task 3}** | `{path}` |

---

## By {Concern/Type}

**{Section 1}** → {description}
**{Section 2}** → {description}
**{Section 3}** → {description}

---

## Related Context

- **{Category}** → `../{category}/navigation.md`
```

### 7.8 Template 7: Specialized Navigation

**Use for**: Cross-cutting concerns (e.g., `ui-navigation.md`).
**Target**: 250-300 tokens.

```markdown
# {Domain} Navigation

**Scope**: [What this covers]

---

## Structure

```
{Relevant directories across multiple categories}
```

---

## Quick Routes

| Task | Path |
|------|------|
| **{Task 1}** | `{path}` |
| **{Task 2}** | `{path}` |

---

## By {Framework/Approach}

**{Tech 1}** → `{path}`
**{Tech 2}** → `{path}`

---

## Common Workflows

**{Workflow 1}**:
1. `{file1}` ({purpose})
2. `{file2}` ({purpose})
```

### 7.9 Universal Template Requirements

All templates MUST have:
1. Title with type prefix (# Concept:, # Example:, etc.)
2. **Purpose** (1 sentence)
3. **Last Updated** (YYYY-MM-DD)
4. **Related** section (cross-references)

### 7.10 Template Validation Checklist

- [ ] Correct template for file type?
- [ ] Has required sections?
- [ ] Under max line limit?
- [ ] Cross-references added?
- [ ] Added to navigation.md?

---

## 8. The Codebase References Standard

**File**: `.opencode/context/core/context-system/standards/codebase-references.md` (145 lines)
**Context Header**: `<!-- Context: core/codebase-references | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->`

### 8.1 Core Principle

```xml
<rule id="link_to_code" enforcement="critical">
  ALL context files SHOULD include `📂 Codebase References` section linking to relevant code.
  Use sections that apply to your context type (not all files need all sections).
</rule>
```

**Why**: Agents need to find actual implementation, not just read about it.

### 8.2 Section Types (Use What's Relevant)

**Business Domain Context**:
- `**Business Logic**`: (MOST IMPORTANT for business domains)
- `**Implementation**`
- `**Models/Types**`
- `**Tests**`
- `**Configuration**`

**Technical/Code Context**:
- `**Implementation**`: (MOST IMPORTANT for technical contexts)
- `**Examples**`
- `**Types**`
- `**Tests**`

**Standards/Quality Context**:
- `**Validation/Enforcement**`: (MOST IMPORTANT for standards)
- `**Examples**`
- `**Tests**`

**Operational Context**:
- `**Scripts/Tools**`: (MOST IMPORTANT for operations)
- `**Configuration**`

### 8.3 Path Format Rules (Strict Enforcement)

```xml
<rule id="path_format" enforcement="strict">
  1. Use project-relative paths (src/..., not /Users/...)
  2. Use forward slashes (/)
  3. Include file extension (.ts, .js, .sh)
  4. Brief description (3-10 words) for each file
  5. Verify files exist (warn if not found)
  6. Use relevant sections only (not all files need all sections)
</rule>
```

### 8.4 Validation Checklist

- [ ] Has "📂 Codebase References" section?
- [ ] Most important section for context type included?
- [ ] Paths are project-relative?
- [ ] Paths include extensions?
- [ ] Each path has 3-10 word description?

---

## 9. The Creation Guide & Workflow

**File**: `.opencode/context/core/context-system/guides/creation.md` (173 lines)
**Context Header**: `<!-- Context: core/creation | Priority: high | Version: 1.1 | Updated: 2026-02-15 -->`

### 9.1 Critical Rules

```xml
<critical_rules priority="absolute" enforcement="strict">
  <rule id="size_limit">Files MUST be under line limits (see below)</rule>
  <rule id="mvi_required">All files MUST follow MVI principle</rule>
  <rule id="function_placement">Files MUST be in correct folder</rule>
  <rule id="navigation_update">MUST update navigation.md when creating files</rule>
</critical_rules>
```

### 9.2 Creation Workflow (6 Steps)

| Step | Action | Detail |
|------|--------|--------|
| 1 | **Determine Function** | Is this a concept, example, guide, lookup, or error? Place in correct folder |
| 2 | **Apply Template** | Use standard template for file type (see templates.md) |
| 3 | **Apply MVI** | Core: 1-3 sentences; Key points: 3-5 bullets; Example: <10 lines; Reference: Link to docs |
| 4 | **Validate Size** | Ensure file under limit. If not, split or reference external |
| 5 | **Add Cross-References** | Link to related concepts/, examples/, guides/, errors/ |
| 6 | **Update Navigation** | Add entry to navigation.md in parent directory |

### 9.3 File Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Concept | `{concept-name}.md` | `authentication.md` |
| Example | `{example-name}.md` | `jwt-example.md` |
| Guide | `{action-name}.md` | `creating-agents.md` |
| Lookup | `{reference-name}.md` | `commands.md` |
| Error | `{error-category}.md` | `auth-errors.md` |

**Rules**: kebab-case (lowercase with hyphens), descriptive but concise, avoid redundant category in name.

### 9.4 Standard Metadata (Frontmatter)

```html
<!-- Context: {path} | Priority: {level} | Version: {X.Y} | Updated: {YYYY-MM-DD} -->
```

Priority levels:
- **critical**: Core system files, always needed
- **high**: Frequently referenced, important patterns
- **medium**: Useful but not essential
- **low**: Nice-to-have, rarely needed

### 9.5 File Size Limits (Strict)

| File Type | Max Lines |
|-----------|-----------|
| Concept | 100 |
| Example | 80 |
| Guide | 150 |
| Lookup | 100 |
| Error | 150 |

**Enforcement**: Strict. If over limit, split into multiple files or reference external docs.

### 9.6 Cross-Reference Guidelines

**Format**: `See {type}/{filename}.md for {what}`

**Examples**:
- `See concepts/authentication.md for JWT details`
- `See examples/jwt-example.md for working code`
- `See errors/auth-errors.md for troubleshooting`

**Best practices**:
- Link to related concepts
- Link to examples from guides
- Link to errors from guides
- Create bidirectional links when relevant

### 9.7 Navigation Update Process

When creating a file, add entry to parent `navigation.md`:
```markdown
| File | Description | Priority |
|------|-------------|----------|
| new-file.md | Brief description | high |
```

Keep navigation:
- Alphabetical within priority groups
- Grouped by priority (critical → high → medium → low)
- Descriptions <10 words

### 9.8 Validation Before Commit

- [ ] File under line limit?
- [ ] MVI format applied?
- [ ] Frontmatter added?
- [ ] In correct folder?
- [ ] Navigation.md updated?
- [ ] Cross-references added?
- [ ] Can be scanned in <30 seconds?

### 9.9 Common Creation Mistakes

| Mistake | Fix |
|---------|-----|
| File too long | Split into multiple files or compress |
| Missing frontmatter | Add HTML comment at top |
| Wrong folder | Move to correct function folder |
| No cross-references | Add links to related files |
| Verbose explanations | Apply MVI compression |
| Missing from navigation | Update navigation.md |

---

## 10. The Compact Guide & Compaction Techniques

**File**: `.opencode/context/core/context-system/guides/compact.md` (122 lines)
**Context Header**: `<!-- Context: core/compact | Priority: high | Version: 1.1 | Updated: 2026-02-15 -->`

### 10.1 Core Idea

> Transform verbose explanations → core concepts following MVI principle.

**Formula**: Verbose Content → Core Concept (1-3 sentences) → Key Points (3-5 bullets) → Minimal Example (<10 lines) → Reference Link → Compact File

### 10.2 The 5 Compression Techniques

| # | Technique | From | To | Rule |
|---|-----------|------|----|------|
| 1 | **Extract Core Concept** | Paragraphs | 1-3 sentences | If you can't explain it in 3 sentences, simplify further |
| 2 | **Bulletize Key Points** | Long paragraphs | 3-5 bullet points | Each bullet = one key fact. No sub-bullets |
| 3 | **Minimize Examples** | Full implementations | Smallest working example (<10 lines) | Show the simplest case. Link to full examples |
| 4 | **Replace Repetition with References** | Same info repeated | Define once, reference with links | Say it once in concepts/, reference everywhere else |
| 5 | **Convert Prose to Tables** | Paragraphs listing things | Scannable tables | If listing >3 items, use a table or bullets |

### 10.3 Compaction Checklist

- [ ] Core concept is 1-3 sentences?
- [ ] Key points are 3-5 bullets (no sub-bullets)?
- [ ] Example is <10 lines of code?
- [ ] No repeated explanations?
- [ ] Reference link added for deep dive?
- [ ] File is under line limit?
- [ ] Can be scanned in <30 seconds?

### 10.4 Common Bloat Patterns to Remove

| Bloat Type | Bad (Avoid) | Good (Use Instead) |
|------------|-------------|-------------------|
| Over-Explaining | "This is important because it allows you to manage state in a more efficient way..." | "Manages state efficiently" |
| Historical Context | "Before React 16.8, we used class components..." | Skip history unless critical |
| Multiple Examples | Example 1, 2, 3, 4... | ONE simple example + link |
| Implementation Details | "The internal implementation uses a fiber architecture..." | Skip internals, show usage |

### 10.5 Target Line Counts

| File Type | Target | Max |
|-----------|--------|-----|
| Concept | 40-60 | 100 |
| Example | 30-50 | 80 |
| Guide | 60-100 | 150 |
| Lookup | 20-40 | 100 |
| Error | 50-80 | 150 |

**Philosophy**: If you hit max lines, split into multiple files or reference external docs.

### 10.6 The 30-Second Rule

```xml
<rule id="thirty_second_rule" enforcement="strict">
  Every context file must be scannable in <30 seconds.
</rule>
```

**Test**: Can someone unfamiliar explain it back in 30 seconds?

### 10.7 Example of Compaction

**Before (150 lines)**: Long authentication system explanation.
**After (45 lines)**:

```markdown
# Concept: Authentication

**Core Idea**: JWT-based stateless auth. Token in httpOnly cookie, verified on every request.

**Key Points**:
- Token has userId + role claims
- Expires in 1 hour (refresh token for renewal)
- Stored in httpOnly cookie (XSS protection)
- Verified via middleware on protected routes

**Quick Example**:
```js
const token = jwt.sign({ userId: 123 }, SECRET, { expiresIn: '1h' })
res.cookie('auth', token, { httpOnly: true })
```

**Reference**: https://docs.company.com/auth
**Related**: examples/jwt-auth.md, errors/auth-errors.md
```

---

## 11. The Organizing Context Guide

**File**: `.opencode/context/core/context-system/guides/organizing-context.md` (152 lines)
**Context Header**: `<!-- Context: core/organizing-context | Priority: high | Version: 1.1 | Updated: 2026-02-15 -->`

### 11.1 Two Organizational Patterns

#### Pattern A: Function-Based

**Use for**: Repository-specific context

```
{repo}/
├── concepts/     # What it is
├── examples/     # Working code
├── guides/       # How to do it
├── lookup/       # Quick reference
└── errors/       # Troubleshooting
```

**Example**: `openagents-repo/`

#### Pattern B: Concern-Based

**Use for**: Multi-technology development context

```
{concern}/
├── {approach}/   # How you're doing it
└── {tech}/       # What you're using
```

**Example**: `development/frontend/react/`, `ui/web/design/`

### 11.2 Decision Tree

| Question | Answer | Use Pattern |
|----------|--------|-------------|
| Is this repository-specific? | YES | **Pattern A** (Function-Based) |
| Does content span multiple technologies? | YES | **Pattern B** (Concern-Based) |
| Single domain/technology? | YES | **Pattern A** (Function-Based) |

### 11.3 Quick Steps to Organize

1. **Audit Existing Content**: List all files, identify natural groupings, note overlaps/duplicates
2. **Choose Pattern**: Use decision tree, consider future growth, check existing patterns
3. **Create Directory Structure**: `mkdir -p {category}/{subcategory}`
4. **Move Files**: Move to new structure, keep filenames descriptive, follow naming conventions
5. **Create Navigation Files**: Add `navigation.md` to each directory, follow navigation template, keep to 200-300 tokens
6. **Update References**: Update links in moved files, update parent navigation.md, test navigation paths

### 11.4 Pattern Examples

**Function-Based (openagents-repo/)**:
```
openagents-repo/
├── concepts/agents.md
├── examples/subagent-example.md
├── guides/creating-agents.md
├── lookup/commands.md
└── errors/tool-errors.md
```

**Concern-Based (development/)**:
```
development/
├── frontend/
│   ├── react/
│   └── vue/
├── backend/
│   ├── node/
│   └── python/
└── data/
    └── postgres/
```

**Hybrid (ui/)**:
```
ui/
├── web/
│   ├── design/
│   ├── animation/
│   └── react-patterns.md
└── terminal/
    └── cli-design.md
```

### 11.5 Verification Checklist

- [ ] Every directory has navigation.md?
- [ ] Navigation files follow template?
- [ ] All files have frontmatter?
- [ ] Links updated and working?
- [ ] Pattern is consistent?
- [ ] Files under line limits?

### 11.6 Troubleshooting

| Issue | Solution |
|-------|----------|
| File fits multiple categories | Choose primary purpose, reference from others |
| Too many files in one directory | Create subcategories |
| Unclear hierarchy | Use concern-based pattern |
| Navigation too complex | Simplify structure, use specialized navigation |

---

## 12. Navigation Design

### 12.1 Navigation Design Basics

**File**: `.opencode/context/core/context-system/guides/navigation-design-basics.md` (133 lines)
**Context Header**: `<!-- Context: core/navigation-design-basics | Priority: high | Version: 1.0 | Updated: 2026-02-15 -->`

#### Core Principles

1. **Token Efficiency**: Goal of 200-300 tokens per navigation file
   - Use ASCII trees (not verbose descriptions)
   - Use tables (not paragraphs)
   - Be concise (not comprehensive)

2. **Scannable Structure**: Goal of finding information in <5 seconds
   - Structure section (ASCII tree) → See what exists
   - Quick Routes (table) → Jump to common tasks
   - By Concern/Type (sections) → Browse by category

3. **Self-Contained**:
   - Include: paths, brief descriptions (3-5 words), when to use
   - Exclude: file contents, detailed explanations, duplicates

#### Design Process (6 Steps)

| Step | Action | Detail |
|------|--------|--------|
| 1 | **Determine Navigation Type** | Category-level, subcategory-level, or specialized (cross-cutting) |
| 2 | **Create Structure Section** | ASCII tree showing directory layout (~50-100 tokens) |
| 3 | **Create Quick Routes Table** | **Bold** tasks, relative paths, 5-10 common tasks |
| 4 | **Create By Concern/Type Sections** | One-line per section with arrow notation |
| 5 | **Add Related Context** (Optional) | Links to related category navigation files |
| 6 | **Validate Token Count** | Target 200-300 tokens; `wc -w navigation.md` then multiply by 1.3 |

#### Navigation Types

| Type | Path | Purpose |
|------|------|---------|
| Category-level | `{category}/navigation.md` | Overview of category |
| Subcategory-level | `{category}/{sub}/navigation.md` | Files in subcategory |
| Specialized | `{category}/{domain}-navigation.md` | Cross-cutting (e.g., ui-navigation.md) |

### 12.2 Navigation Templates

**File**: `.opencode/context/core/context-system/guides/navigation-templates.md` (185 lines)
**Context Header**: `<!-- Context: core/navigation-templates | Priority: high | Version: 1.0 | Updated: 2026-02-15 -->`

#### Good Example (Token-Efficient, ~180 tokens)

```markdown
# Development Navigation

**Purpose**: Software development across all stacks

---

## Structure

```
development/
├── navigation.md
├── ui-navigation.md
├── principles/
├── frontend/
├── backend/
└── data/
```

---

## Quick Routes

| Task | Path |
|------|------|
| **UI/Frontend** | `ui-navigation.md` |
| **Backend/API** | `backend-navigation.md` |
| **Clean code** | `principles/clean-code.md` |

---

## By Concern

**Principles** → Universal practices
**Frontend** → React, Vue, state
**Backend** → APIs, Node, auth
**Data** → SQL, NoSQL, ORMs
```

#### Bad Example (Too Verbose, 500+ tokens)

Long paragraphs of introduction, comprehensive descriptions, etc. This violates the 200-300 token target.

#### Troubleshooting

| Issue | Solution |
|-------|----------|
| Too many tokens | Remove verbose descriptions, shorten entries |
| Hard to scan | Use tables instead of paragraphs |
| Missing files | Add to structure and quick routes |
| Unclear paths | Use relative paths, add brief descriptions |

---

## 13. The Workflows Guide (Interactive Operations)

**File**: `.opencode/context/core/context-system/guides/workflows.md` (573 lines)
**Context Header**: `<!-- Context: core/workflows | Priority: high | Version: 1.0 | Updated: 2026-02-15 -->`

### 13.1 Extract Workflow (5 Stages)

**Stage 1: Read Source**
```
/context extract from https://react.dev/hooks
  →
Agent: "Reading source (8,500 lines)...
Analyzing content for extractable items..."
```

**Stage 2: Analyze & Categorize**
Found items are categorized as: core concepts, common errors, workflows.

**Stage 3: Select Category (APPROVAL REQUIRED)**
Letter-based selection (A B C or 'all') + category number.

**Stage 4: Preview (APPROVAL REQUIRED)**
Shows what files will be created, with line counts. Options: yes/no/preview/dry-run.

**Stage 5-7: Create, Update, Report**
Creates files, updates navigation.md, reports totals.

### 13.2 Organize Workflow (8 Stages)

**Stages 1-2: Scan & Categorize**
Scans a directory, categorizes files by function.

**Stage 3: Resolve Conflicts (APPROVAL REQUIRED)**
Three types of issues:
- **Clear categorization**: Moves file to correct folder
- **Ambiguous files**: Offers split or choose-primary options (letter-based)
- **Conflicts**: Target file already exists → merge, rename, or skip

**Stage 4: Preview (APPROVAL REQUIRED)**
Shows: CREATE directories, MOVE files, SPLIT files, MERGE files, UPDATE navigation and references.

**Stages 5-8: Backup, Execute, Update, Report**
Creates backup at `.tmp/backup/{operation}-{topic}-{timestamp}/`, executes all changes, fixes references, updates navigation.

### 13.3 Update Workflow (8 Stages)

**Stage 1: Identify Changes (APPROVAL REQUIRED)**
Asks what changed: API changes, deprecations, new features, breaking changes, other.

**Stage 2: Find Affected Files**
Searches for files referencing the topic, shows count and line numbers.

**Stage 3: Preview Changes (APPROVAL REQUIRED)**
Shows line-by-line diffs. Options: yes/no/edit.

**Stages 4-8: Backup, Update, Add Migration, Validate, Report**
Creates backup, applies updates, adds migration notes to errors files, validates references, ensures files stay under 200 lines.

### 13.4 Error Workflow (6 Stages)

**Stage 1: Search Existing**
Searches for similar existing errors.

**Stage 2: Check Duplication (APPROVAL REQUIRED)**
Options: Add as new error, Update existing error, Skip. Also selects framework/category.

**Stage 3: Preview (APPROVAL REQUIRED)**
Shows current vs. proposed changes with NEW/UPDATED markers.

**Stages 4-6: Add, Update, Report**
Updates the error file, cross-references, validates file size.

### 13.5 Common Interaction Patterns

**Approval Gates**: All operations with destructive potential must:
1. Show clear preview of what will happen
2. Wait for explicit user input
3. Provide options (yes/no/edit/preview/dry-run)
4. Never proceed without confirmation

**Conflict Resolution**: Present all options clearly, use letter-based selection (A/B/C), show impact of each option.

**Previews**: Show what will be created/modified/deleted, file sizes (before → after), line-by-line diffs for updates, validation status.

**Backups**: Operations that modify files must create backup at `.tmp/backup/{operation}-{topic}-{timestamp}/`, report backup location, keep backups for rollback.

---

## 14. Root Navigation File

**File**: `.opencode/context/navigation.md` (49 lines)
**Context Header**: `<!-- Context: core/navigation | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->`

### 14.1 Content (Verbatim)

```markdown
# Context Navigation

**New here?** → `openagents-repo/quick-start.md`

---

## Structure

```
.opencode/context/
├── core/                   # Universal standards & workflows
├── openagents-repo/        # OpenAgents Control repository work
├── development/            # Software development (all stacks)
├── ui/                     # Visual design & UX
├── content-creation/       # Content creation (all formats)
├── data/                   # Data engineering & analytics
├── product/                # Product management
└── learning/               # Educational content
```

---

## Quick Routes

| Task | Path |
|------|------|
| **Write code** | `core/standards/code-quality.md` |
| **Write tests** | `core/standards/test-coverage.md` |
| **Write docs** | `core/standards/documentation.md` |
| **Review code** | `core/workflows/code-review.md` |
| **Delegate task** | `core/workflows/task-delegation-basics.md` |
| **Add agent** | `openagents-repo/guides/adding-agent.md` |
| **UI development** | `development/ui-navigation.md` |
| **API development** | `development/backend-navigation.md` |

---

## By Category

**core/** - Standards, workflows, patterns → `core/navigation.md`
**openagents-repo/** - Repository-specific → `openagents-repo/navigation.md`
**development/** - All development → `development/navigation.md`
**ui/** - Design & UX → `ui/navigation.md`
**content-creation/** - Content creation (all formats) → `content-creation/navigation.md`
**data/** - Data engineering → `data/navigation.md`
**product/** - Product management → `product/navigation.md`
**learning/** - Educational → `learning/navigation.md`
```

The root navigation follows the exact navigation template pattern: Structure (ASCII tree), Quick Routes (table), By Category (sections with arrows). It's notable for its "New here?" entry point pointing to `openagents-repo/quick-start.md`.

---

## 15. CODEBASE_STANDARDS.md Format

**File**: `.opencode/context/CODEBASE_STANDARDS.md` (3,795 lines)
**Context Header**: `<!-- Context: core/standards | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->`

### 15.1 Format Analysis (First 100 Lines)

The file is a comprehensive reference guide covering 24 sections:

1. Function Definition Standards
2. Class Usage Standards
3. Array Handling Standards
4. Variable & Destructuring Standards
5. Control Flow Standards
6. Async & Concurrency Standards
7. Race Condition Prevention
8. AI System Integration Standards
9. Service Architecture Standards
10. State Management Standards
11. Event Bus Standards
12. Configuration Management Standards
13. Storage & Persistence Standards
14. Error Handling Standards
15. Type System Standards
16. Import Organization Standards
17. Naming Conventions
18. Testing Standards
19. Documentation Standards
20. Schema Definition Standards
21. Dependency Management Standards
22. Build & Development Standards
23. Performance Standards
24. Security Standards

Each section follows a consistent pattern:
- **Rule statement** at the top (e.g., "Prefer single-word function names")
- **Compliance percentage** (e.g., "Compliance: 95%+")
- **Good/Bad/Avoid examples** with `// ✅ GOOD`, `// ✅ ACCEPTABLE`, `// ❌ AVOID` comments
- **File References** listing actual source files and line numbers
- Sub-sections with pattern-specific rules

The header shows: `_Analyzed: 206+ TypeScript files across packages/opencode/src/_`

This file itself significantly exceeds the MVI 200-line limit (3,795 lines), serving as a "kitchen sink" reference that other context files can point to via `📂 Codebase References` sections. It represents the one comprehensive document in the system, with all other files strictly adhering to MVI principles.

---

## 16. Self-Referential Architecture

The context system is deeply self-referential. Here is how every standard, guide, and command references the others:

### 16.1 Cross-Reference Network

```
mvi.md
  ├── References: structure.md, compact.md, templates.md, creation.md

frontmatter.md
  └── References: structure.md, templates.md, codebase-references.md

structure.md
  └── References: mvi.md (as mvi-principle.md), templates.md, creation.md

templates.md
  └── References: creation.md, mvi.md (as mvi-principle.md), compact.md

codebase-references.md
  └── References: frontmatter.md, templates.md, structure.md, templates/ (directory)

creation.md
  └── References: templates.md, mvi.md, compact.md, structure.md

compact.md
  └── References: mvi.md, harvest.md, templates.md

organizing-context.md
  └── References: structure.md, navigation-templates.md, creation.md

navigation-design-basics.md
  └── References: navigation-templates.md, ../standards/mvi.md, ../examples/navigation-examples.md

navigation-templates.md
  └── References: navigation-design-basics.md, ../standards/mvi.md, ../examples/navigation-examples.md

workflows.md
  └── References: context.md, harvest.md, mvi-principle.md, compact.md
```

### 16.2 The `/context` Command References Standards and Guides

The context command's lazy load map directly references the file system:
```
.opencode/context/core/context-system/
├── operations/     # How to do things
│   ├── harvest.md
│   ├── extract.md
│   ├── organize.md
│   ├── update.md
│   └── error.md
├── standards/      # What to follow
│   ├── mvi.md
│   ├── structure.md
│   ├── templates.md
│   ├── frontmatter.md
│   └── codebase-references.md
└── guides/         # Step-by-step
    ├── workflows.md
    ├── compact.md
    ├── creation.md
    ├── organizing-context.md
    ├── navigation-design-basics.md
    └── navigation-templates.md
```

Every command (`harvest`, `compact`, `extract`, `organize`, `update`, `error`, `create`, `migrate`) explicitly loads only the relevant subset of these files before executing, as defined in the lazy load map.

### 16.3 The Self-Enforcement Loop

The system enforces itself through multiple overlapping mechanisms:

1. **MVI Constraint**: All files must be <200 lines, scannable in <30 seconds
2. **Structure Constraint**: All files must live in function-based folders (concepts/, examples/, guides/, lookup/, errors/)
3. **Frontmatter Constraint**: All files must start with the HTML comment frontmatter
4. **Approval Constraint**: All destructive operations require explicit user confirmation
5. **Lazy Load Constraint**: Operations must load only their required context files
6. **Navigation Constraint**: Every category must have a navigation.md
7. **Cross-Reference Constraint**: All files must link to related files
8. **Codebase Reference Constraint**: All context files should include `📂 Codebase References`
9. **Template Constraint**: All files must use the appropriate type template
10. **Priority Constraint**: All frontmatter must specify one of critical/high/medium/low

The **critical rules** in the `/context` command are declared with `priority="absolute"` and `enforcement="strict"`, meaning Tier 1 (Safety & MVI) always overrides Tier 2 (Core Operations) and Tier 3 (Enhancements).

### 16.4 The Three-Tier Priority System in Practice

**Tier 1 (Always Enforced)**:
- Files <200 lines
- Show approval before cleanup
- Function-based structure
- Load context before operations

**Tier 2 (Core Operations)**:
- Harvest (default), Extract, Organize, Update

**Tier 3 (Enhancements)**:
- Cross-references, validation, navigation

When there is a conflict (e.g., a user wants to skip approval for cleanup), Tier 1 wins and approval is still required.

### 16.5 The Context System Serves Itself

The most remarkable aspect is that the context system uses itself:
- The standards (`mvi.md`, `structure.md`, `templates.md`, `frontmatter.md`, `codebase-references.md`) define rules that they themselves follow
- Each standard file has the proper frontmatter HTML comment
- Each standard file stays within the line limits it prescribes
- Each standard file cross-references its related files
- The root `navigation.md` follows the very navigation design pattern it prescribes
- The `/context` command's lazy load map references these exact files by relative path
- The workflows guide shows interactive workflows that reference these exact standards

This creates a fully self-consistent, self-documenting system where the standards are not just described but actively embodied in every file.
