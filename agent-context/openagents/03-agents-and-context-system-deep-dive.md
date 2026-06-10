# OpenAgentsControl: Context-Related Agents & Context System Deep Dive

**Research Date**: 2026-05-03
**Repository**: `/home/codey/Dev/OpenAgentsControl/`
**Scope**: ContextScout, ContextManager, ExternalScout subagents; OpenCoder/OpenAgent primary agents; context system auto-discovery, navigation, operations, frontmatter, and priority system

---

## Table of Contents

1. [ContextScout Subagent](#1-contextscout-subagent)
2. [ContextManager Subagent](#2-contextmanager-subagent)
3. [ExternalScout Subagent](#3-externalscout-subagent)
4. [OpenCoder Primary Agent (Context Loading)](#4-opencoder-primary-agent-context-loading)
5. [OpenAgent Primary Agent (Context Loading)](#5-openagent-primary-agent-context-loading)
6. [The Context System Architecture](#6-the-context-system-architecture)
7. [Context Resolution Logic (Local vs Global)](#7-context-resolution-logic-local-vs-global)
8. [Priority System](#8-priority-system)
9. [Harvest Operation (6 Stages)](#9-harvest-operation-6-stages)
10. [Extract Operation (7 Stages)](#10-extract-operation-7-stages)
11. [Organize Operation (8 Stages)](#11-organize-operation-8-stages)
12. [Update Operation (8 Stages)](#12-update-operation-8-stages)
13. [Auto-Discovery at Task Start](#13-auto-discovery-at-task-start)
14. [Navigation.md as Discovery Mechanism](#14-navigationmd-as-discovery-mechanism)
15. [Frontmatter Format & Parsing Rules](#15-frontmatter-format--parsing-rules)

---

## 1. ContextScout Subagent

**File**: `.opencode/agent/subagents/core/contextscout.md`

### Mission

> **Mission**: Discover and recommend context files from `.opencode/context/` (or custom_dir from paths.json) ranked by priority. Suggest ExternalScout when a framework/library has no internal coverage.

### Permissions (Read-Only Agent)

```yaml
permission:
  read:
    "*": "allow"
  grep:
    "*": "allow"
  glob:
    "*": "allow"
  bash:
    "*": "deny"
  edit:
    "*": "deny"
  write:
    "*": "deny"
  task:
    "*": "deny"
```

ContextScout is strictly **read-only** -- it can only read, grep, and glob. It cannot write, edit, run bash, or delegate tasks.

### Core Rules (Tier 1 -- Absolute)

```xml
<rule id="context_root">
  The context root is determined by paths.json (loaded via @ reference). Default is `.opencode/context/`. If custom_dir is set in paths.json, use that instead. Start by reading `{context_root}/navigation.md`. Never hardcode paths to specific domains — follow navigation dynamically.
</rule>

<rule id="global_fallback">
  **One-time check on startup**: If `{local}/core/` does NOT exist (glob returns nothing), AND paths.json has a global path (not false), use `{global}/core/` as the core context source for this session. This handles users who installed OAC globally but work in a local project.

  Resolution steps (run ONCE, at the start of every invocation):
  1. `glob("{local}/core/navigation.md")` — if found → local has core, use `{local}` for everything. Done.
  2. If not found → read paths.json `global` value. If false or missing → no fallback, proceed with local only.
  3. If global path exists → `glob("{global}/core/navigation.md")` — if found → use `{global}/core/` for core files only.
  4. Set `{core_root}` = whichever path has core. All other context (project-intelligence, ui, etc.) stays `{local}`.

  **Limits**: This is ONLY for `core/` files (standards, workflows, guides). Never fall back to global for project-intelligence — that's project-specific. Maximum 2 glob checks. No per-file fallback.
</rule>

<rule id="read_only">
  Read-only agent. NEVER use write, edit, bash, task, or any tool besides read, grep, glob.
</rule>

<rule id="verify_before_recommend">
  NEVER recommend a file path you haven't confirmed exists. Always verify with read or glob first.
</rule>

<rule id="external_scout_trigger">
  If the user mentions a framework or library (e.g. Next.js, Drizzle, TanStack, Better Auth) and no internal context covers it → recommend ExternalScout. Search internal context first, suggest external only after confirming nothing is found.
</rule>
```

### Tier Structure

```xml
<tier level="1" desc="Critical Operations">
  - @context_root: Navigation-driven discovery only — no hardcoded paths
  - @global_fallback: Resolve core location once at startup (max 2 glob checks)
  - @read_only: Only read, grep, glob — nothing else
  - @verify_before_recommend: Confirm every path exists before returning it
  - @external_scout_trigger: Recommend ExternalScout when library not found internally
</tier>

<tier level="2" desc="Core Workflow">
  - Understand intent from user request
  - Follow navigation.md files top-down
  - Return ranked results (Critical → High → Medium)
</tier>

<tier level="3" desc="Quality">
  - Brief summaries per file so caller knows what each contains
  - Match results to intent — don't return everything
  - Flag frameworks/libraries for ExternalScout when needed
</tier>

<conflict_resolution>Tier 1 always overrides Tier 2/3. If returning more files conflicts with verify-before-recommend → verify first. If a path seems relevant but isn't confirmed → don't include it.</conflict_resolution>
```

### EXACT Algorithm (4 Steps)

> **4 steps. That's it.**
>
> 1. **Resolve core location** (once) — Check if `{local}/core/navigation.md` exists. If not, check `{global}/core/navigation.md` per @global_fallback. Set `{core_root}` accordingly.
> 2. **Understand intent** — What is the user trying to do?
> 3. **Follow navigation** — Read `navigation.md` files from `{local}` (and `{core_root}` if different) downward. They are the map.
> 4. **Return ranked files** — Priority order: Critical → High → Medium. Brief summary per file. Use the actual resolved path (local or global) in file paths.

### Response Format

```markdown
# Context Files Found

## Critical Priority

**File**: `.opencode/context/path/to/file.md`
**Contains**: What this file covers

## High Priority

**File**: `.opencode/context/another/file.md`
**Contains**: What this file covers

## Medium Priority

**File**: `.opencode/context/optional/file.md`
**Contains**: What this file covers
```

If a framework/library was mentioned and not found internally, append:

```markdown
## ExternalScout Recommendation

The framework **[Name]** has no internal context coverage.

→ Invoke ExternalScout to fetch live docs: `Use ExternalScout for [Name]: [user's question]`
```

### Anti-Patterns (What NOT to Do)

- ❌ Don't hardcode domain→path mappings — follow navigation dynamically
- ❌ Don't assume the domain — read navigation.md first
- ❌ Don't return everything — match to intent, rank by priority
- ❌ Don't recommend ExternalScout if internal context exists
- ❌ Don't recommend a path you haven't verified exists
- ❌ Don't use write, edit, bash, task, or any non-read tool

---

## 2. ContextManager Subagent

**File**: `.opencode/agent/subagents/core/context-manager.md`

### Mission

> **Mission**: Discover, catalog, validate, and maintain project context structure with dependency tracking and lifecycle management.

### Permissions

```yaml
permission:
  read:
    "*": "allow"
  grep:
    "*": "allow"
  glob:
    "*": "allow"
  bash:
    "find .opencode/context*": "allow"
    "ls -la .opencode/context*": "allow"
    "mkdir -p .opencode/context*": "allow"
    "mv .opencode/context*": "allow"
    "*": "deny"
  edit:
    ".opencode/context/**/*.md": "allow"
    ".opencode/context/**/*.json": "allow"
    "**/*.env*": "deny"
    "**/*.key": "deny"
    "**/*.secret": "deny"
  write:
    ".opencode/context/**/*.md": "allow"
    ".opencode/context/**/*.json": "allow"
    "**/*.env*": "deny"
    "**/*.key": "deny"
    "**/*.secret": "deny"
  task:
    "*": "deny"
    "contextscout": "allow"
```

Key: ContextManager can read/edit/write within `.opencode/context/`, run limited bash commands on context directories, and delegate to ContextScout. It is forbidden from touching secrets, env files, or key files.

### Core Rules (Tier 1)

```xml
<rule id="context_root">
  The ONLY entry point is `.opencode/context/`. All operations start from navigation.md files. Never hardcode paths — follow navigation dynamically.
</rule>

<rule id="navigation_driven">
  ALWAYS read navigation.md files to understand context structure before making changes. Navigation files are the source of truth for context organization.
</rule>

<rule id="verify_before_modify">
  NEVER modify or create context files without verifying the structure and dependencies. Always check what exists before making changes.
</rule>

<rule id="catalog_integrity">
  Maintain catalog integrity by tracking:
  - File paths and locations
  - Dependencies between context files
  - Last modified dates
  - Content summaries
  - Usage patterns
</rule>

<rule id="propose_before_execute">
  Always propose changes to context structure BEFORE executing. Get confirmation on:
  - New context areas to create
  - Files to reorganize
  - Navigation updates needed
  - Deprecations or archival
</rule>
```

### Process Flow (6 Steps)

```xml
<step_1> Discover Context Structure
  1. Read `.opencode/context/navigation.md` to understand root structure
  2. For each domain/area in navigation:
     - Read its navigation.md file
     - Identify all files and subdirectories
     - Note relationships and dependencies
  3. Build mental map of context hierarchy
  4. Identify any gaps or orphaned areas
</step_1>

<step_2> Catalog Context Inventory
  1. For each context file discovered:
     - Record full path
     - Extract purpose/description from frontmatter or first section
     - Note any dependencies on other context files
     - Record last modified date if available
  2. Identify usage patterns:
     - Which files are referenced by subagents
     - Which files are referenced by other context files
     - Which files appear unused
  3. Create catalog structure:
     - By domain/area
     - By file type (standards, guides, examples, templates)
     - By usage frequency
</step_2>

<step_3> Validate Context Integrity
  1. Check navigation.md accuracy:
     - Verify all listed files exist
     - Verify all files in directory are listed
     - Check for broken links
  2. Validate file references:
     - Check that referenced files exist
     - Identify circular dependencies
     - Flag missing context areas
  3. Check naming consistency:
     - Verify kebab-case naming
     - Check for duplicate content
     - Identify naming conflicts
  4. Report validation results
</step_3>

<step_4> Propose Context Improvements
  1. Based on discovery and validation, identify:
     - New context areas needed
     - Reorganization opportunities
     - Deprecated context to archive
     - Navigation updates required
  2. For each improvement:
     - Explain why it's needed
     - Show impact on existing structure
     - Provide specific steps to implement
  3. Propose in priority order:
     - Critical (blocking issues)
     - High (significant improvements)
     - Medium (nice-to-have enhancements)
</step_4>

<step_5> Execute Approved Changes
  1. Wait for user approval on proposals
  2. For each approved change:
     - Create new context files if needed
     - Update navigation.md files
     - Reorganize files if needed
     - Archive deprecated context
  3. Verify changes:
     - Run validation again
     - Confirm navigation is accurate
     - Check all references are valid
  4. Report completion
</step_5>

<step_6> Maintain Context Lifecycle
  1. Track context status:
     - Active: Currently used and maintained
     - Deprecated: Scheduled for removal
     - Archived: No longer used but kept for reference
  2. Update metadata:
     - Last modified dates
     - Usage frequency
     - Dependency changes
  3. Generate reports:
     - Context health summary
     - Usage statistics
     - Maintenance recommendations
</step_6>
```

### Request Types (Parameters)

```xml
<parameter name="request_type" type="enum">
  - "discover": Discover and map context structure
  - "catalog": Create/update context inventory
  - "validate": Check context integrity
  - "propose": Suggest improvements
  - "execute": Implement approved changes
  - "health": Generate context health report
  - "search": Find context by keyword or domain
</parameter>

<parameter name="scope" type="string">
  - "all": Entire context structure
  - "{domain}": Specific domain (e.g., "core", "ui", "development")
  - "{area}": Specific area (e.g., "core/standards", "ui/web")
  - Default: "all"
</parameter>

<parameter name="details" type="string">
  - For discover: Areas to focus on
  - For validate: Specific checks to run
  - For propose: Types of improvements to suggest
  - For search: Keywords or patterns to find
</parameter>
```

### Context Management Principles

1. **Navigation-Driven Discovery**: Always follow navigation.md files as the source of truth. Never hardcode paths or assume structure.
2. **Catalog Everything**: Maintain a complete inventory of all context with metadata, relationships, and usage patterns.
3. **Validate Continuously**: Regular validation ensures context integrity and catches issues early.
4. **Propose Before Executing**: Always propose changes and get approval before modifying context structure.
5. **Track Lifecycle**: Monitor context status (active, deprecated, archived) and maintain history.
6. **Maintain Relationships**: Document and preserve dependencies between context files and areas.
7. **Consistent Organization**: Use consistent naming, structure, and conventions across all context.
8. **Lazy Loading**: Reference context files by path, don't embed content. Let consumers load what they need.

### Output Specification

```yaml
status: "success" | "partial" | "failure"
request_type: "{request_type}"
scope: "{scope}"

result:
  # For discover requests
  structure:
    domains: [{name, path, description, subdomain_count}]
    total_files: number
    total_areas: number

  # For catalog requests
  inventory:
    total_files: number
    by_domain: {domain: count}
    by_type: {type: count}

  # For validate requests
  validation:
    valid_files: number
    issues_found: number
    issues: [{file, issue_type, description}]

  # For propose requests
  proposals:
    critical: [{title, description, impact, steps}]
    high: [{title, description, impact, steps}]
    medium: [{title, description, impact, steps}]

  # For health requests
  health:
    overall_score: "0-100"
    active_areas: number
    deprecated_areas: number
    archived_areas: number
    recommendations: [string]

metadata:
  execution_time: "X.Xs"
  files_processed: number
  areas_analyzed: number
  warnings: [string]
  next_steps: [string]
```

---

## 3. ExternalScout Subagent

**File**: `.opencode/agent/subagents/core/externalscout.md`

### Mission

> Fetch version-specific docs from Context7 (primary) or official sources (fallback), filter to relevant sections, persist to `.tmp`, and return file locations + brief summary.

### Permissions

```yaml
permission:
  read:
    "**/*": "deny"
    ".opencode/skills/context7/**": "allow"
    ".tmp/external-context/**": "allow"
  bash:
    "*": "deny"
    "curl -s https://context7.com/*": "allow"
    "jq *": "allow"
  skill:
    "*": "deny"
    "*context7*": "allow"
  task:
    "*": "deny"
```

Highly restricted: can ONLY read context7 skill files and .tmp/external-context, use curl to hit Context7 API, and invoke context7 skills.

### Critical Rules

```xml
<rule id="tool_usage">
  ALLOWED:
  - read: ONLY .opencode/skills/context7/** and .tmp/external-context/**
  - bash: ONLY curl to context7.com
  - skill: ONLY context7
  - grep: ONLY within .tmp/external-context/
  - webfetch: Any URL
  - write: ONLY to .tmp/external-context/**
  - edit: ONLY .tmp/external-context/**
  - glob: ONLY .opencode/skills/context7/** and .tmp/external-context/**

  NEVER use: task | todoread | todowrite
  NEVER read: Project files, source code, or any files outside allowed paths
</rule>

<rule id="always_use_tools">
  ALWAYS use tools to fetch live documentation
  NEVER fabricate or assume documentation content
  NEVER rely on training data for library APIs
</rule>

<rule id="mandatory_persistence">
  You MUST write fetched documentation to files using the Write tool
  Fetching without writing = FAILURE
  Stage 4 (PersistToTemp) is MANDATORY and cannot be skipped
</rule>

<rule id="check_cache_first">
  ALWAYS check .tmp/external-context/ for existing docs before fetching
  If recent docs exist (< 7 days), return cached files instead of re-fetching
  Only fetch if docs are missing or stale
</rule>

<rule id="tech_stack_awareness">
  Understand tech stack context from user query
  Libraries behave differently in different frameworks (e.g., TanStack Query in Next.js vs TanStack Start)
  Include tech stack context in fetch queries for accurate, relevant documentation
</rule>
```

### 6-Stage Workflow

```
Stage 0: CheckCache
  1. Check if `.tmp/external-context/` directory exists
  2. List existing library directories: `glob ".tmp/external-context/*"`
  3. If library directory exists, check for relevant topic files
  4. If recent docs found (< 7 days old), return existing file locations
  5. If docs missing or stale, proceed to Stage 1

Stage 1: DetectLibrary
  1. Read `.opencode/skills/context7/library-registry.md`
  2. Match query against library names, package names, and aliases
  3. Extract library ID and official docs URL
  4. Detect tech stack context from user query:
     - Is this for Next.js? TanStack Start? Vanilla React?
     - What other libraries are mentioned?
     - What's the deployment target?
  5. Identify common integration patterns:
     - TanStack Query + Next.js = SSR hydration patterns
     - TanStack Query + TanStack Start = server functions
     - Drizzle + Better Auth = adapter configuration

Stage 2: FetchDocumentation
  Build context-aware query:
  - Base query: User's original question
  - Add tech stack context: "with {framework}"
  - Add integration context: "and {other-lib}"
  - Add common pitfalls: "common mistakes", "gotchas", "troubleshooting"

  Example enhanced queries:
  - Original: "TanStack Query setup"
  - Enhanced: "TanStack Query setup with Next.js App Router SSR hydration common mistakes"
  
  - Original: "Drizzle schema"
  - Enhanced: "Drizzle schema with PostgreSQL modular patterns common pitfalls"

  Primary: Use Context7 API with enhanced query:
    curl -s "https://context7.com/api/v2/context?libraryId=LIBRARY_ID&query=ENHANCED_QUERY&type=txt"

  Fallback: If Context7 fails → fetch from official docs with multiple URLs

Stage 3: FilterRelevant
  1. Keep only sections answering the user's question
  2. Remove navigation, unrelated content, and padding
  3. Preserve code examples and key concepts

Stage 4: PersistToTemp (MANDATORY - CANNOT be skipped)
  1. Create directory: `.tmp/external-context/{package-name}/`
  2. Generate filename from topic (kebab-case): `{topic}.md`
  3. Write file using Write tool with metadata header:
     ---
     source: Context7 API
     library: {library-name}
     package: {package-name}
     topic: {topic}
     fetched: {ISO timestamp}
     official_docs: {link}
     ---
     
     {filtered documentation content}
  4. Confirm file written by checking it exists
  5. Update `.tmp/external-context/.manifest.json` with file metadata

  ⚠️ If you skip writing files, you have FAILED the task

Stage 5: ReturnLocations (MANDATORY - only after Stage 4 is complete)
  Return format:
  ✅ Fetched: {library-name}
  📁 Files written to:
     - .tmp/external-context/{package-name}/{topic-1}.md
     - .tmp/external-context/{package-name}/{topic-2}.md
  📝 Summary: {1-2 line summary}
  🔗 Official Docs: {link}
```

### Success Criteria

```
✅ Documentation is fetched from Context7 or official sources
✅ Results are filtered to only relevant sections
✅ Files are WRITTEN to `.tmp/external-context/{package-name}/{topic}.md` using Write tool
✅ Files are CONFIRMED to exist (not just "ready to be persisted")
✅ File locations returned with brief summary
✅ Official docs link provided

❌ You FAIL if you:
- Fetch docs but don't write files
- Say "ready to be persisted" without actually writing
- Skip Stage 4 (PersistToTemp)
- Return summary without file locations
```

### Supported Libraries

Drizzle | Prisma | Better Auth | NextAuth.js | Clerk | Next.js | React | TanStack Query/Router | Cloudflare Workers | AWS Lambda | Vercel | Shadcn/ui | Radix UI | Tailwind CSS | Zustand | Jotai | Zod | React Hook Form | Vitest | Playwright

---

## 4. OpenCoder Primary Agent (Context Loading)

**File**: `.opencode/agent/core/opencoder.md`

### Critical Context Requirement Block (Verbatim)

```xml
<critical_context_requirement>
PURPOSE: Context files contain project-specific coding standards that ensure consistency, 
quality, and alignment with established patterns. Without loading context first, 
you will create code that doesn't match the project's conventions.

CONTEXT PATH CONFIGURATION:
- paths.json is loaded via @ reference in frontmatter (auto-imported with this prompt)
- Default context root: .opencode/context/
- If custom_dir is set in paths.json, use that instead (e.g., ".context", ".ai/context")
- ContextScout automatically uses the configured context root

BEFORE any code implementation (write/edit), ALWAYS load required context files:
- Code tasks → {context_root}/core/standards/code-quality.md (MANDATORY)
- Language-specific patterns if available

WHY THIS MATTERS:
- Code without standards/code-quality.md → Inconsistent patterns, wrong architecture
- Skipping context = wasted effort + rework

CONSEQUENCE OF SKIPPING: Work that doesn't match project standards = wasted effort
</critical_context_requirement>
```

### Critical Rules (Verbatim)

```xml
<critical_rules priority="absolute" enforcement="strict">
  <rule id="approval_gate" scope="all_execution">
    Request approval before ANY implementation (write, edit, bash). Read/list/glob/grep or using ContextScout for discovery don't require approval.
    ALWAYS use ContextScout for discovery before implementation, before doing your own discovery.
  </rule>
  
  <rule id="stop_on_failure" scope="validation">
    STOP on test fail/build errors - NEVER auto-fix without approval
  </rule>
  
  <rule id="report_first" scope="error_handling">
    On fail: REPORT error → PROPOSE fix → REQUEST APPROVAL → Then fix (never auto-fix)
    For package/dependency errors: Use ExternalScout to fetch current docs before proposing fix
  </rule>
  
  <rule id="incremental_execution" scope="implementation">
    Implement ONE step at a time, validate each step before proceeding
  </rule>
</critical_rules>
```

### ContextScout Integration in OpenCoder's Workflow

OpenCoder's **Stage 1 (Discover)** mandates:

```xml
<stage id="1" name="Discover" required="true">
  Goal: Understand what's needed. Nothing written to disk.

  1. Call `ContextScout` to discover relevant project context files.
     - ContextScout has paths.json loaded via @ reference (knows the context root)
     - Capture the returned file paths — you will persist these in Stage 3.
  2. **For external packages/libraries**:
     a. Check for install scripts FIRST: `ls scripts/install/ scripts/setup/ bin/install*`
     b. If scripts exist: Read and understand them before fetching docs.
     c. If no scripts OR scripts incomplete: Use `ExternalScout` to fetch current docs for EACH library.
     d. Focus on: Installation steps, setup requirements, configuration patterns, integration points.
  3. Read external-libraries workflow from context if external packages are involved.

  *Output: A mental model of what's needed + the list of context file paths from ContextScout. Nothing persisted yet.*
</stage>
```

### Constraints (Verbatim)

```xml
<constraints enforcement="absolute">
  These constraints override all other considerations:
  
  1. NEVER execute write/edit without loading required context first
  2. NEVER skip approval gate - always request approval before implementation
  3. NEVER auto-fix errors - always report first and request approval
  4. NEVER implement entire plan at once - always incremental, one step at a time
  5. ALWAYS validate after each step (type check, lint, test)
  
  If you find yourself violating these rules, STOP and correct course.
</constraints>
```

---

## 5. OpenAgent Primary Agent (Context Loading)

**File**: `.opencode/agent/core/openagent.md`

### Critical Context Requirement Block (Verbatim)

```xml
<critical_context_requirement>
PURPOSE: Context files contain project-specific standards that ensure consistency, 
quality, and alignment with established patterns. Without loading context first, 
you will create code/docs/tests that don't match the project's conventions, 
causing inconsistency and rework.

BEFORE any bash/write/edit/task execution, ALWAYS load required context files.
(Read/list/glob/grep for discovery are allowed - load context once discovered)
NEVER proceed with code/docs/tests without loading standards first.
AUTO-STOP if you find yourself executing without context loaded.

WHY THIS MATTERS:
- Code without standards/code-quality.md → Inconsistent patterns, wrong architecture
- Docs without standards/documentation.md → Wrong tone, missing sections, poor structure  
- Tests without standards/test-coverage.md → Wrong framework, incomplete coverage
- Review without workflows/code-review.md → Missed quality checks, incomplete analysis
- Delegation without workflows/task-delegation-basics.md → Wrong context passed to subagents

Required context files:
- Code tasks → .opencode/context/core/standards/code-quality.md
- Docs tasks → .opencode/context/core/standards/documentation.md  
- Tests tasks → .opencode/context/core/standards/test-coverage.md
- Review tasks → .opencode/context/core/workflows/code-review.md
- Delegation → .opencode/context/core/workflows/task-delegation-basics.md

CONSEQUENCE OF SKIPPING: Work that doesn't match project standards = wasted effort + rework
</critical_context_requirement>
```

### Automatic Context Loading (Step 3.0) -- Verbatim

```xml
<step id="3.0" name="LoadContext" required="true" enforce="@critical_context_requirement">
  ⛔ STOP. Before executing, check task type:
  
  1. Classify task: docs|code|tests|delegate|review|patterns|bash-only
  2. Map to context file:
     - code (write/edit code) → Read .opencode/context/core/standards/code-quality.md NOW
     - docs (write/edit docs) → Read .opencode/context/core/standards/documentation.md NOW
     - tests (write/edit tests) → Read .opencode/context/core/standards/test-coverage.md NOW
     - review (code review) → Read .opencode/context/core/workflows/code-review.md NOW
     - delegate (using task tool) → Read .opencode/context/core/workflows/task-delegation-basics.md NOW
     - bash-only → No context needed, proceed to 3.2
     
     NOTE: Load all files discovered by ContextScout in Stage 1.5 if not already loaded.
  
  3. Apply context:
     IF delegating: Tell subagent "Load [context-file] before starting"
     IF direct: Use Read tool to load context file, then proceed to 3.2
  
  <automatic_loading>
    IF code task → .opencode/context/core/standards/code-quality.md (MANDATORY)
    IF docs task → .opencode/context/core/standards/documentation.md (MANDATORY)
    IF tests task → .opencode/context/core/standards/test-coverage.md (MANDATORY)
    IF review task → .opencode/context/core/workflows/code-review.md (MANDATORY)
    IF delegation → .opencode/context/core/workflows/task-delegation-basics.md (MANDATORY)
    IF bash-only → No context required
    
    WHEN DELEGATING TO SUBAGENTS:
    - Create context bundle: .tmp/context/{session-id}/bundle.md
    - Include all loaded context files + task description + constraints
    - Pass bundle path to subagent in delegation prompt
  </automatic_loading>
  
  <checkpoint>Context file loaded OR confirmed not needed (bash-only)</checkpoint>
</step>
```

### Stage 1.5 (Discover) -- Verbatim

```xml
<stage id="1.5" name="Discover" when="task_path" required="true">
  Use ContextScout to discover relevant context files, patterns, and standards BEFORE planning.
  
  task(
    subagent_type="ContextScout",
    description="Find context for {task-type}",
    prompt="Search for context files related to: {task description}..."
  )
  
  <checkpoint>Context discovered</checkpoint>
</stage>
```

### Stage 1.5b (DiscoverExternal) -- Verbatim

```xml
<stage id="1.5b" name="DiscoverExternal" when="external_packages_detected" required="false">
  If task involves external packages (npm, pip, gem, cargo, etc.), fetch current documentation.
  
  <process>
    1. Detect external packages:
       - User mentions library/framework (Next.js, Drizzle, React, etc.)
       - package.json/requirements.txt/Gemfile/Cargo.toml contains deps
       - import/require statements reference external packages
       - Build errors mention external packages
    
    2. Check for install scripts (first-time builds):
       bash: ls scripts/install/ scripts/setup/ bin/install* setup.sh install.sh
       
       If scripts exist:
       - Read and understand what they do
       - Check environment variables needed
       - Note prerequisites (database, services)
    
    3. Fetch current documentation for EACH external package:
       task(
         subagent_type="ExternalScout",
         description="Fetch [Library] docs for [topic]",
         prompt="Fetch current documentation for [Library]: [specific question]
         
         Focus on:
         - Installation and setup steps
         - [Specific feature/API needed]
         - [Integration requirements]
         - Required environment variables
         - Database/service setup
         
         Context: [What you're building]"
       )
    
    4. Combine internal context (ContextScout) + external docs (ExternalScout)
       - Internal: Project standards, patterns, conventions
       - External: Current library APIs, installation, best practices
       - Result: Complete context for implementation
  </process>
</stage>
```

### ContextScout + ExternalScout Decision Table (Verbatim)

| Scenario | ContextScout | ExternalScout | Both |
|----------|--------------|---------------|------|
| Project coding standards | ✅ | ❌ | ❌ |
| External library setup | ❌ | ✅ MANDATORY | ❌ |
| Project-specific patterns | ✅ | ❌ | ❌ |
| External API usage | ❌ | ✅ MANDATORY | ❌ |
| Feature w/ external lib | ✅ standards | ✅ lib docs | ✅ |
| Package installation | ❌ | ✅ MANDATORY | ❌ |
| Security patterns | ✅ | ❌ | ❌ |
| External lib integration | ✅ project | ✅ lib docs | ✅ |

### Constraints (Verbatim)

```xml
<constraints enforcement="absolute">
  These constraints override all other considerations:
  
  1. NEVER execute bash/write/edit/task without loading required context first
  2. NEVER skip step 3.1 (LoadContext) for efficiency or speed
  3. NEVER assume a task is "too simple" to need context
  4. ALWAYS use Read tool to load context files before execution
  5. ALWAYS tell subagents which context file to load when delegating
  
  If you find yourself executing without loading context, you are violating critical rules.
  Context loading is MANDATORY, not optional.
</constraints>
```

---

## 6. The Context System Architecture

**File**: `.opencode/context/core/context-system.md`

### 6 Core Principles

1. **Minimal Viable Information (MVI)**: Extract only core concepts (1-3 sentences), key points (3-5 bullets), minimal example, and reference link. Goal: Scannable in <30 seconds. Reference full docs, don't duplicate them.

2. **Concern-Based Structure**: Organize by **what you're doing** (concern), then by **how** (approach/tech). Two patterns:
   - **Pattern A: Function-Based** (for repository-specific context): `concepts/`, `examples/`, `guides/`, `lookup/`, `errors/`
   - **Pattern B: Concern-Based** (for development context): `{concern}/{approach}/` or `{concern}/{tech}/`

3. **Token-Efficient Navigation**: Every category/subcategory has `navigation.md` with ASCII tree (~50 tokens), Quick Routes table (~100 tokens), and By concern/type sections (~50 tokens). Total: ~200-300 tokens per navigation file.

4. **Specialized Navigation Files**: For cross-cutting concerns, create specialized navigation (e.g., `development/ui-navigation.md`).

5. **Self-Describing Filenames**: `code-quality.md` not `code.md`; `test-coverage.md` not `tests.md`.

6. **Knowledge Harvesting**: Extract valuable context from AI summaries/overviews, then delete them. Workspace stays clean, knowledge persists.

### Directory Structure

#### Pattern A: Function-Based (Repository-Specific)

```
.opencode/context/{category}/
├── navigation.md              # Fast, token-efficient navigation
├── quick-start.md             # Optional: 2-minute orientation
│
├── core-concepts/             # Foundational concepts (optional)
│   ├── navigation.md
│   └── {concept}.md
│
├── concepts/                  # What it is
│   ├── navigation.md
│   └── {concept}.md
│
├── examples/                  # Working code
│   ├── navigation.md
│   └── {example}.md
│
├── guides/                    # How to do it
│   ├── navigation.md
│   └── {guide}.md
│
├── lookup/                    # Quick reference
│   ├── navigation.md
│   └── {lookup}.md
│
└── errors/                    # Common issues
    ├── navigation.md
    └── {error}.md
```

#### Pattern B: Concern-Based (Development Context)

```
.opencode/context/{category}/
├── navigation.md                       # Main navigation
├── {concern}-navigation.md             # Specialized navigation (optional)
│
├── principles/                         # Universal principles (optional)
│   ├── navigation.md
│   └── {principle}.md
│
├── {concern}/                          # Organize by concern
│   ├── navigation.md
│   │
│   ├── {approach}/                     # Then by approach
│   │   ├── navigation.md
│   │   └── {pattern}.md
│   │
│   └── {tech}/                         # Or by tech
│       ├── navigation.md
│       └── {pattern}.md
```

### Operations (Quick Reference)

```bash
/context                      # Quick scan, suggest actions
/context harvest              # Clean up summaries → permanent context
/context extract {source}     # From docs/code/URLs
/context organize {category}  # Restructure flat files → function folders
/context update {what}        # When APIs/frameworks change
/context migrate              # Move global project-intelligence → local project
/context create {category}    # Create new context category
/context error {error}        # Add recurring error to knowledge base
/context compact {file}       # Minimize verbose file to MVI format
/context map [category]       # View context structure
/context validate             # Check integrity, references, sizes
```

---

## 7. Context Resolution Logic (Local vs Global)

This is defined exclusively in the ContextScout's `global_fallback` rule. The resolution logic operates as follows:

### Resolution Steps (Run ONCE at the start of every invocation)

1. **Check Local Core**: `glob("{local}/core/navigation.md")` — if found → local has core, use `{local}` for everything. **Done.**

2. **Check paths.json**: If local core not found → read paths.json `global` value. If `false` or missing → no fallback, proceed with local only.

3. **Check Global Core**: If global path exists → `glob("{global}/core/navigation.md")` — if found → use `{global}/core/` for core files only.

4. **Set `{core_root}`**: Assign whichever path has core. All other context (project-intelligence, ui, etc.) stays `{local}`.

### Key Constraints on Global Fallback

- **ONLY for `core/` files** (standards, workflows, guides). Never fall back to global for project-intelligence -- that's project-specific.
- **Maximum 2 glob checks** (one for local, one for global).
- **No per-file fallback** -- the resolution is all-or-nothing for the core directory.
- The `local` path defaults to `.opencode/context/` (or `custom_dir` from paths.json).
- The `global` path comes from paths.json's `global` key.

### How It Works in Practice

```
Scenario 1: User has local .opencode/context/core/navigation.md
  → Local core found. Use local for everything.

Scenario 2: User has local .opencode/context/ but NO core/ subdirectory
  → Check paths.json for global path.
  → If global exists AND has core/navigation.md:
    → Use global/core/ for standards, workflows, guides
    → Use local/ for everything else (project-intelligence, ui, etc.)

Scenario 3: No local context at all
  → Check paths.json global. If available and has core, use that.
  → Otherwise, no context available.
```

---

## 8. Priority System

### Definition (from context-system.md frontmatter)

The priority system is defined in context file frontmatter as:

```
<!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->
```

Where `{level}` is one of:

| Priority | % of Use Cases | When to Apply |
|----------|----------------|---------------|
| **critical** | 80% | Business logic, core concepts, foundational standards |
| **high** | 15% | Common workflows, examples, frequently-used patterns |
| **medium** | 4% | Edge cases, less common scenarios |
| **low** | 1% | Rare scenarios, niche use cases |

### How Priority Affects Loading

From ContextScout's algorithm:

> 4. **Return ranked files** — Priority order: Critical → High → Medium

The priority determines:

1. **Discovery Order**: ContextScout returns results sorted by priority (Critical first, then High, then Medium). Low priority is rarely included unless specifically requested.

2. **Automatic Loading**: OpenAgent's `<automatic_loading>` block always loads critical-priority files:
   - `core/standards/code-quality.md` (critical)
   - `core/standards/documentation.md` (critical)
   - `core/standards/test-coverage.md` (critical)
   - `core/workflows/code-review.md` (critical)
   - `core/workflows/task-delegation-basics.md` (critical)

3. **Navigation Priority**: The root `navigation.md` and `core/navigation.md` are both marked `Priority: critical`, ensuring they are always found first.

4. **ContextScout Output Format**: Results are grouped by priority tier:

```markdown
## Critical Priority
**File**: `.opencode/context/path/to/file.md`
**Contains**: What this file covers

## High Priority
**File**: `.opencode/context/another/file.md`
**Contains**: What this file covers

## Medium Priority
**File**: `.opencode/context/optional/file.md`
**Contains**: What this file covers
```

5. **ContextManager Proposals**: When ContextManager proposes improvements, it uses the same priority ordering (Critical → High → Medium).

### Frontmatter Priority Examples (Verbatim)

```markdown
<!-- Context: ecommerce/concepts | Priority: critical | Version: 1.0 | Updated: 2026-01-27 -->
<!-- Context: payments/guides | Priority: high | Version: 1.2 | Updated: 2026-01-27 -->
<!-- Context: development/examples | Priority: medium | Version: 1.0 | Updated: 2026-01-27 -->
```

---

## 9. Harvest Operation (6 Stages)

**File**: `.opencode/context/core/context-system/operations/harvest.md`

### Purpose

> Extract knowledge from AI summaries → permanent context, then clean workspace

### Core Problem

AI agents create summary files (OVERVIEW.md, SESSION-*.md, SUMMARY.md) that contain valuable knowledge but clutter the workspace. These files "plague" the codebase. **Solution**: Harvest the knowledge → permanent context, then delete the summaries.

### Auto-Detection Patterns (Verbatim)

```xml
<rule id="summary_patterns" enforcement="strict">
  Harvest automatically detects these patterns:
  
  Filename patterns:
  - *OVERVIEW.md
  - *SUMMARY.md
  - SESSION-*.md
  - CONTEXT-*.md
  - *NOTES.md
  
  Location patterns:
  - Files in .tmp/ directory
  - Files with "Summary", "Overview", "Session" in title
  - Files >2KB in root directory (likely summaries)
</rule>
```

### Stage 1: Scan

**Action**: Find all summary files in workspace

**Process**:
1. Search for auto-detection patterns
2. Check .tmp/ directory
3. List files with sizes
4. Sort by modification date (newest first)

**Output**: List of candidate files

```
Found 3 summary documents:
1. CONTEXT-SYSTEM-OVERVIEW.md (4.2 KB, modified 1 hour ago)
2. SESSION-auth-work.md (1.8 KB, modified today)
3. .tmp/IMPLEMENTATION-NOTES.md (800 bytes, modified today)
```

### Stage 2: Analyze

**Action**: Categorize content by function

**Mapping Rules**:

| Content Type | Target Folder | How to Identify |
|--------------|---------------|-----------------|
| Design decisions | `concepts/` | "We decided to...", "Architecture", "Pattern" |
| Solutions/patterns | `examples/` | Code snippets, "Here's how we..." |
| Workflows | `guides/` | Numbered steps, "How to...", "Setup" |
| Errors encountered | `errors/` | Error messages, "Fixed issue", "Gotcha" |
| Reference data | `lookup/` | Tables, lists, paths, commands |

**Process**:
1. Read each file
2. Identify valuable sections (skip planning/conversation)
3. Categorize by function
4. Determine target file path
5. Generate preview (first 60 chars)

**Output**: Categorized items with letter IDs

### Stage 3: Approve (CRITICAL)

```xml
<rule id="approval_gate" enforcement="strict">
  ALWAYS show approval UI before extracting/deleting.
  NEVER auto-harvest without user confirmation.
</rule>
```

**Format**:
```
### CONTEXT-SYSTEM-OVERVIEW.md (4.2 KB)

✓ [A] Design: Function-based context organization
    → Would add to: core/concepts/context-organization.md
    Preview: "Organize by function (concepts/, examples/...)..."

✓ [B] Pattern: Minimal Viable Information
    → Would add to: core/concepts/mvi-principle.md
    Preview: "Extract core only (1-3 sentences), 3-5 key points..."

✓ [C] Workflow: Harvesting summary documents
    → Would create: core/guides/harvesting.md
    Preview: "Scan for summaries → Extract → Approve → Delete"

✗ [D] Skip: Planning discussion notes (temporary knowledge)

---

### SESSION-auth-work.md (1.8 KB)

✓ [E] Error: JWT token expiration not handled
    → Would add to: development/errors/auth-errors.md
    Preview: "Symptom: 401 after 1 hour. Cause: No refresh flow..."

✓ [F] Example: JWT refresh token implementation
    → Would create: development/examples/jwt-refresh.md
    Preview: "Store refresh token → Check expiry → Request new..."

---

### .tmp/IMPLEMENTATION-NOTES.md (800 bytes)

✗ [G] Skip: Duplicate info (already in development/concepts/api-design.md)

---

Quick options:
- Type 'A B C E F' - Approve specific items
- Type 'all' - Approve all ✓ items (A B C E F)
- Type 'none' - Skip harvesting, delete files anyway
- Type 'cancel' - Keep files, don't harvest
```

### Stage 4: Extract

```xml
<rule id="extraction" enforce="@mvi_principle">
  Apply MVI to all extracted content:
  - Core concept: 1-3 sentences
  - Key points: 3-5 bullets
  - Minimal example: <10 lines
  - Reference link: to original source
  - Files: <200 lines each
</rule>
```

Process:
1. For each approved item, extract core content, apply MVI minimization
2. Show extraction preview (APPROVAL REQUIRED)
3. On approval: Write files to disk, add cross-references, update navigation.md maps

### Stage 5: Cleanup (APPROVAL REQUIRED)

Options:
1. **Archive (safe)** — move to `.tmp/archive/harvested/{date}/`
2. **Delete** — permanently remove harvested files
3. **Keep** — leave source files in place

```xml
<rule id="cleanup_safety" enforcement="strict">
  ONLY cleanup files that had content successfully harvested.
  If extraction failed, keep the original file.
</rule>
```

### Stage 6: Report

```
✅ Harvested 5 items into permanent context:
   - Added to core/concepts/context-organization.md
   - Added to core/concepts/mvi-principle.md
   - Created core/guides/harvesting.md
   - Added to development/errors/auth-errors.md
   - Created development/examples/jwt-refresh.md

🗑️ Cleaned up workspace:
   - Archived: CONTEXT-SYSTEM-OVERVIEW.md → .tmp/archive/harvested/2026-01-06/
   - Archived: SESSION-auth-work.md → .tmp/archive/harvested/2026-01-06/
   - Deleted: .tmp/IMPLEMENTATION-NOTES.md (no valuable content)

📊 Updated navigation maps:
   - .opencode/context/core/navigation.md
   - .opencode/context/development/navigation.md

💾 Disk space freed: 6.8 KB
```

### Smart Content Detection

**Extract (Valuable Knowledge)**:
- Design decisions ("We chose X because...")
- Patterns that worked ("This pattern solved...")
- Errors encountered + solutions
- API changes ("Updated from v1 to v2...")
- Performance findings ("Optimization reduced...")
- Core concepts explained

**Skip (Temporary/Noise)**:
- Planning discussion ("Should we...?", "Maybe try...")
- Conversational notes ("I think...", "We talked about...")
- Duplicate info (already in context)
- TODO lists (move to task system instead)
- Timestamps and session metadata

---

## 10. Extract Operation (7 Stages)

**File**: `.opencode/context/core/context-system/operations/extract.md`

### Purpose

> Extract context from docs, code, or URLs into organized context files

### When to Use

- Extracting from documentation (React docs, API docs, etc.)
- Extracting from codebase (patterns, conventions)
- Extracting from URLs (blog posts, guides)
- Creating initial context for new topics

### Stage 1: Read Source

```
/context extract from https://react.dev/hooks
  ↓
Agent: "Reading source (8,500 lines)...
Analyzing content for extractable items..."
```

### Stage 2: Analyze & Categorize

**Categorization**:
- Design decisions → `concepts/`
- Working code → `examples/`
- Step-by-step workflows → `guides/`
- Reference data (commands, paths) → `lookup/`
- Errors/gotchas → `errors/`

### Stage 3: Select Category (APPROVAL REQUIRED)

```
Found 12 extractable items from {source}:

Concepts (8):
  ✓ [A] useState - State management hook
  ✓ [B] useEffect - Side effects hook
  ... (6 more)

Errors (4):
  ✓ [I] Hooks called conditionally
  ✓ [J] Hooks in loops
  ... (2 more)

Which category?
  [1] development/
  [2] core/
  [3] Create new category: ___

Select items (A B I or 'all') + category (1/2/3):
```

### Stage 4: Preview (APPROVAL REQUIRED)

Shows:
- CREATE (new files)
- ADD TO (existing files)
- CONFLICT (file already exists) with merge/skip/overwrite options
- NAVIGATION UPDATE plan
- Total file count and size

Must get approval before proceeding.

### Stage 5: Create

1. Apply MVI format (1-3 sentences, 3-5 key points, minimal example)
2. Create files in correct function folders
3. Ensure all files <200 lines
4. Add cross-references

Enforcement: `@critical_rules.mvi_strict` + `@critical_rules.function_structure`

### Stage 6: Update Navigation

1. Update category navigation.md with new files (as previewed in Stage 4)
2. Add priority levels (critical/high/medium/low)
3. Add cross-references between related files
4. Update "Last Updated" dates

### Stage 7: Report

```
✅ Extracted X items into {category}
📄 Created Y files
📊 Updated {category}/README.md

Files created:
  - {category}/concepts/ (N files)
  - {category}/examples/ (N files)
  - {category}/errors/ (N files)
```

---

## 11. Organize Operation (8 Stages)

**File**: `.opencode/context/core/context-system/operations/organize.md`

### Purpose

> Restructure flat context files into function-based folder structure

### When to Use

- Migrating from flat structure to function-based
- Cleaning up disorganized context directories
- Splitting ambiguous files into proper categories
- Resolving duplicate/conflicting files

### Categorization Rules

- Explains concept? → `concepts/`
- Shows working code? → `examples/`
- Step-by-step instructions? → `guides/`
- Reference data (tables, commands)? → `lookup/`
- Errors/issues? → `errors/`

### Stage 1: Scan
Scan category for all files and detect structure type (flat vs organized).

### Stage 2: Categorize
Categorize each file by function. Flag ambiguous files.

### Stage 3: Resolve Conflicts (APPROVAL REQUIRED)

```
Organizing {category}/ (23 files, flat structure)

Clear categorization (18 files):
  concepts/ (8):
    ✓ authentication.md → concepts/authentication.md
  
  examples/ (5):
    ✓ jwt-example.md → examples/jwt-example.md

Ambiguous files (5 - need your input):
  
  [?] api-design.md (contains concepts AND steps)
      → [A] Split: concepts/api-design.md + guides/api-design-guide.md
      → [B] Keep as concepts/api-design.md
      → [C] Keep as guides/api-design-guide.md

Conflicts (2):
  
  [!] authentication.md → concepts/auth.md
      Target already exists (120 lines)
      → [J] Merge into existing
      → [K] Rename to concepts/authentication-v2.md
      → [L] Skip (keep flat)

Select resolutions (A J or 'auto'):
```

### Stage 4: Preview (APPROVAL REQUIRED)

Shows:
- CREATE directories (concepts/, examples/, guides/, lookup/, errors/)
- MOVE files (count)
- SPLIT files (count)
- MERGE files (count)
- UPDATE README.md and fix references

Dry-run option available.

### Stage 5: Backup
Create backup at `.tmp/backup/organize-{category}-{timestamp}/`

### Stage 6: Execute
1. Create function folders
2. Move files to correct locations
3. Split ambiguous files if requested
4. Merge conflicts if requested

### Stage 7: Update
1. Update README.md with navigation tables
2. Fix all internal references to moved files
3. Validate all links work
4. Update "Last Updated" dates

### Stage 8: Report

```
✅ Organized X files into function folders
📁 Created Y new folders
🔀 Split Z ambiguous files
🔗 Fixed N references
💾 Backup: .tmp/backup/organize-{category}-{timestamp}/

Rollback available if needed.
```

---

## 12. Update Operation (8 Stages)

**File**: `.opencode/context/core/context-system/operations/update.md`

### Purpose

> Update context when APIs, frameworks, or contracts change

### When to Use

- Framework version updates (Next.js 14 → 15)
- API changes (breaking changes, deprecations)
- New features added to existing topics
- Migration guides needed

### Stage 1: Identify Changes (APPROVAL REQUIRED)

```
What changed in {topic}?
  [A] API changes
  [B] Deprecations
  [C] New features
  [D] Breaking changes
  [E] Other (describe)

Select all that apply (A B C D or describe):
```

### Stage 2: Find Affected Files

1. Grep for topic references across all context
2. Count references per file
3. Show impact analysis

```
Found 5 files referencing {topic}:
  📄 concepts/routing.md (3 references, 145 lines)
  📄 examples/app-router-example.md (7 references, 78 lines)
  📄 guides/setting-up-nextjs.md (2 references, 132 lines)
  📄 errors/nextjs-errors.md (1 reference, 98 lines)
  📄 lookup/nextjs-commands.md (4 references, 54 lines)

Total impact: 17 references across 5 files
```

### Stage 3: Preview Changes (APPROVAL REQUIRED)

Shows line-by-line diff for each file. Edit mode available for line-by-line approval.

### Stage 4: Backup
Create backup at `.tmp/backup/update-{topic}-{timestamp}/`

### Stage 5: Update Files
1. Update concepts, examples, guides, lookups
2. Maintain MVI format (<200 lines)
3. Update "Last Updated" dates
4. Preserve file structure

Enforcement: `@critical_rules.mvi_strict`

### Stage 6: Add Migration Notes

Add to `{category}/errors/{topic}-errors.md`:

```markdown
## Migration: {Old Version} → {New Version}

**Breaking Changes**:
- Change 1
- Change 2

**Migration Steps**:
1. Step 1
2. Step 2

**Reference**: [Link to changelog]
```

### Stage 7: Validate
- All internal references still work
- No broken links
- All files still <200 lines
- MVI format maintained

### Stage 8: Report

```
✅ Updated X files
📝 Modified Y references
🔄 Added migration notes to errors/
💾 Backup: .tmp/backup/update-{topic}-{timestamp}/

All files still under 200 line limit ✓

Rollback available if needed.
```

### Change Types

- **API Changes**: Method signatures changed, parameters added/removed, return types changed
- **Deprecations**: Features marked deprecated, replacement APIs available, timeline for removal
- **New Features**: New capabilities added, new APIs introduced, new patterns available
- **Breaking Changes**: Incompatible changes, migration required, old code won't work

---

## 13. Auto-Discovery at Task Start

### What Triggers Auto-Discovery

Auto-discovery is triggered at **two points** in the primary agent workflows:

1. **OpenCoder Stage 1 (Discover)**: Before any code implementation, as the very first step.
2. **OpenAgent Stage 1.5 (Discover)**: After analyzing whether the task is conversational or task-path, before planning.

### What Auto-Discovery Reads

#### Step 1: ContextScout Resolves Context Root

```
1. glob("{local}/core/navigation.md")
   - If found → local has core, use {local} for everything. Done.
   - If not found → read paths.json global value
     - If false or missing → no fallback, proceed with local only
     - If global path exists → glob("{global}/core/navigation.md")
       - If found → use {global}/core/ for core files only
       - {core_root} = whichever path has core
```

#### Step 2: ContextScout Reads Navigation Files

Starting from `{context_root}/navigation.md`, ContextScout follows the hierarchy top-down:

1. **Root navigation**: `{context_root}/navigation.md` -- the master index
2. **Category navigations**: Follows links to `core/navigation.md`, `development/navigation.md`, etc.
3. **Sub-category navigations**: Follows deeper as needed based on user intent

The actual root `navigation.md` at `.opencode/context/navigation.md` looks like:

```markdown
## Structure

.opencode/context/
├── core/                   # Universal standards & workflows
├── openagents-repo/        # OpenAgents Control repository work
├── development/            # Software development (all stacks)
├── ui/                     # Visual design & UX
├── content-creation/       # Content creation (all formats)
├── data/                   # Data engineering & analytics
├── product/                # Product management
└── learning/               # Educational content

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
```

#### Step 3: ContextScout Understands Intent

Based on what the user is asking, ContextScout matches intent to context categories:
- Code task → `core/standards/code-quality.md` (critical)
- Test task → `core/standards/test-coverage.md` (critical)
- Documentation → `core/standards/documentation.md` (critical)
- External packages → ExternalScout recommendation

#### Step 4: ContextScout Returns Ranked Files

Priority order: Critical → High → Medium. Only verified paths (confirmed to exist via read or glob).

### How OpenCoder Uses Discovery Results

In **Stage 3 (InitSession)**, OpenCoder persists the context file paths discovered by ContextScout into a `context.md` file:

```markdown
## Context Files (Standards to Follow)
{Paths discovered by ContextScout in Stage 1 — these are the standards}
- {discovered context file paths}
```

This file is the single source of truth for all downstream agents (TaskManager, CoderAgent, TestEngineer, CodeReviewer).

### How OpenAgent Uses Discovery Results

In **Stage 3.0 (LoadContext)**, OpenAgent:

1. Classifies the task type (docs|code|tests|delegate|review|patterns|bash-only)
2. Maps to the MANDATORY context file for that type
3. Loads ALL files discovered by ContextScout in Stage 1.5 (if not already loaded)
4. For delegation: creates a context bundle at `.tmp/context/{session-id}/bundle.md` containing all loaded context files + task description + constraints

### `/context` Command Routing

OpenAgent also defines a `/context` command system that routes to specialized subagents:

```xml
<context_retrieval>
  <operations>
    /context harvest     - Extract knowledge from summaries → permanent context
    /context extract     - Extract from docs/code/URLs
    /context organize    - Restructure flat files → function-based
    /context map         - View context structure
    /context validate    - Check context integrity
  </operations>
  
  <routing>
    /context operations automatically route to specialized subagents:
    - harvest/extract/organize/update/error/create → context-organizer
    - map/validate → contextscout
  </routing>
</context_retrieval>
```

---

## 14. Navigation.md as Discovery Mechanism

### The Hierarchy

Navigation files form a hierarchical discovery tree. ContextScout traverses this tree top-down:

```
.opencode/context/
└── navigation.md                          # ROOT (entry point)
    ├── core/navigation.md                  # Category navigation
    │   ├── standards/navigation.md
    │   ├── workflows/navigation.md
    │   ├── guides/navigation.md
    │   ├── task-management/navigation.md
    │   ├── system/
    │   └── context-system/navigation.md
    │       ├── examples/navigation.md
    │       ├── guides/navigation.md
    │       ├── operations/navigation.md
    │       └── standards/navigation.md
    ├── development/navigation.md
    ├── ui/navigation.md
    ├── project-intelligence/navigation.md
    ├── openagents-repo/navigation.md
    └── ... (other categories)
```

### Navigation Template (Verbatim from navigation-templates.md)

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

**Target**: ~200-250 tokens per category navigation, ~250-300 for specialized navigation

### Root Navigation.md (Actual Content, Verbatim)

```markdown
<!-- Context: core/navigation | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->

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

### Core Navigation.md (Actual Content, Verbatim)

```markdown
<!-- Context: core/navigation | Priority: critical | Version: 1.0 | Updated: 2026-02-15 -->

# Core Context Navigation

**Purpose**: Universal standards and workflows for all development

---

## Structure

```
core/
├── navigation.md
├── context-system.md
├── essential-patterns.md
│
├── standards/
│   ├── navigation.md
│   ├── code-quality.md
│   ├── test-coverage.md
│   ├── documentation.md
│   ├── security-patterns.md
│   └── code-analysis.md
│
├── workflows/
│   ├── navigation.md
│   ├── code-review.md
│   ├── task-delegation-basics.md
│   ├── feature-breakdown.md
│   ├── session-management.md
│   └── design-iteration-overview.md
│
├── guides/
│   ├── navigation.md
│   └── resuming-sessions.md
│
├── task-management/
│   ├── navigation.md
│   ├── standards/
│   │   └── navigation.md
│   ├── guides/
│   │   └── navigation.md
│   └── lookup/
│       └── navigation.md
│
├── system/
│   └── context-guide.md
│
└── context-system/
    ├── navigation.md
    ├── examples/
    │   └── navigation.md
    ├── guides/
    │   └── navigation.md
    ├── operations/
    │   └── navigation.md
    └── standards/
        └── navigation.md
```

---

## Quick Routes

| Task | Path |
|------|------|
| **Write code** | `standards/code-quality.md` |
| **Write tests** | `standards/test-coverage.md` |
| **Write docs** | `standards/documentation.md` |
| **Security patterns** | `standards/security-patterns.md` |
| **Review code** | `workflows/code-review.md` |
| **Delegate task** | `workflows/task-delegation-basics.md` |
| **Break down feature** | `workflows/feature-breakdown.md` |
| **Resume session** | `guides/resuming-sessions.md` |
| **Manage tasks** | `task-management/navigation.md` |
| **Task CLI commands** | `task-management/lookup/task-commands.md` |
| **Context system** | `context-system.md` |

---

## By Type

**Standards** → Code quality, testing, docs, security (critical priority)
**Workflows** → Review, delegation, task breakdown (high priority)
**Task Management** → JSON-driven task tracking with CLI (high priority)
**System** → Context management and guides (medium priority)

---

## Related Context

- **Development** → `../development/navigation.md`
- **OpenAgents Control Repo** → `../openagents-repo/navigation.md`
```

### How ContextScout Traverses Navigation

1. **Start**: Read `{context_root}/navigation.md` (the root navigation)
2. **Match intent**: Identify which categories match the user's request
3. **Read sub-navigation**: Follow relevant category navigation files
4. **Drill down**: Continue following navigation.md files deeper into the tree
5. **Quick Routes**: Use Quick Routes tables for direct jumps to commonly needed files
6. **Verify**: Confirm every recommended file path exists using read or glob

### Navigation Design Principles

1. **Token Efficiency**: 200-300 tokens per navigation file
2. **Scannable Structure**: ASCII tree → Quick Routes table → By Concern/Type sections
3. **Self-Contained**: Include paths and brief descriptions (3-5 words); exclude file contents and detailed explanations
4. **Three-Section Format**: Structure (ASCII tree), Quick Routes (table), By Concern/Type (sections)

---

## 15. Frontmatter Format & Parsing Rules

### Format Definition (Verbatim)

```xml
<rule id="frontmatter_required" enforcement="strict">
  ALL context files MUST start with:
  
  <!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->
</rule>
```

### Components

1. **Category/Function**: `{category}/{function}`
   - Examples: `ecommerce/concepts`, `development/examples`, `core/standards`
   - Category = domain (ecommerce, payments, development)
   - Function = file type (concepts, examples, guides, lookup, errors)

2. **Priority**: `critical` | `high` | `medium` | `low`
   - **critical**: 80% of use cases (business logic, core concepts)
   - **high**: 15% of use cases (common workflows, examples)
   - **medium**: 4% of use cases (edge cases)
   - **low**: 1% of use cases (rare scenarios)

3. **Version**: `X.Y` (start 1.0, increment on changes)

4. **Updated**: `YYYY-MM-DD` (ISO 8601, must match metadata section)

### Validation Checklist

- [ ] Frontmatter is first line?
- [ ] Format exact: `<!-- Context: ... -->`?
- [ ] Priority is critical|high|medium|low?
- [ ] Version is X.Y?
- [ ] Date is YYYY-MM-DD?

### Examples (Verbatim)

```markdown
<!-- Context: ecommerce/concepts | Priority: critical | Version: 1.0 | Updated: 2026-01-27 -->
<!-- Context: payments/guides | Priority: high | Version: 1.2 | Updated: 2026-01-27 -->
<!-- Context: development/examples | Priority: medium | Version: 1.0 | Updated: 2026-01-27 -->
```

### Parsing Context

The frontmatter is parsed by ContextScout and ContextManager to:
1. **Determine priority**: Files with `Priority: critical` are always returned first in discovery results
2. **Categorize content**: The `{category}/{function}` field tells agents where the file fits in the knowledge hierarchy
3. **Track staleness**: The `Updated` field helps determine if context needs refreshing (used by Update operation)
4. **Version tracking**: The `Version` field enables change tracking across context file revisions

### How Priority Maps to Auto-Loading

When a primary agent (OpenCoder or OpenAgent) calls ContextScout, the results are grouped and presented as:

- **Critical Priority**: Always recommended, auto-loaded for matching task types
- **High Priority**: Recommended for the specific task at hand
- **Medium Priority**: Optional, load if relevant to the task
- **Low Priority**: Only loaded on explicit request

The frontmatter priority directly determines where a file appears in ContextScout's ranked output, which in turn determines whether a primary agent auto-loads it or only loads it on demand.
