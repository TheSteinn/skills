# `/add-context` Command — Deep Dive

> Exhaustive analysis of the OpenAgentsControl `/add-context` command, its wizard flow, validation, templates, flags, and relationships to the Project Intelligence system.

---

## Table of Contents

1. [Command Overview](#1-command-overview)
2. [Frontmatter & Metadata](#2-frontmatter--metadata)
3. [Critical Rules (Tier 1 — Absolute Enforcement)](#3-critical-rules-tier-1--absolute-enforcement)
4. [Execution Priority & Conflict Resolution](#4-execution-priority--conflict-resolution)
5. [Step-by-Step Flow (Verbatim Stage Descriptions)](#5-step-by-step-flow-verbatim-stage-descriptions)
6. [The 6 Wizard Questions — Exact Prompts & Capture](#6-the-6-wizard-questions--exact-prompts--capture)
7. [The `--update` Flag](#7-the---update-flag)
8. [The `--global` Flag](#8-the---global-flag)
9. [Existing Context Detection & Offer to Review/Update/Add/Replace/Cancel](#9-existing-context-detection--offer-to-reviewupdateaddreplacecancel)
10. [Validation Rules (MVI, Frontmatter, etc.)](#10-validation-rules-mvi-frontmatter-etc)
11. [Navigation.md Update Process](#11-navigationmd-update-process)
12. [Version Tracking](#12-version-tracking)
13. [Frontmatter Format — Exact Specification](#13-frontmatter-format--exact-specification)
14. [Template/Format for Each Project Intelligence File](#14-templateformat-for-each-project-intelligence-file)
15. [Relationship Between technical-domain.md and Other PI Files](#15-relationship-between-technical-domainmd-and-other-pi-files)
16. [Delegation to ContextOrganizer](#16-delegation-to-contextorganizer)
17. [Error Handling](#17-error-handling)
18. [Success Criteria Checklist](#18-success-criteria-checklist)

---

## 1. Command Overview

**Purpose** (verbatim from the file):

> Help users add project patterns using Project Intelligence standard. **Easiest way** to teach agents YOUR coding patterns.

**Value Proposition** (verbatim):

> Answer 6 questions (~5 min) → properly structured context files → agents generate code matching YOUR project.

**Invocation**:

```bash
/add-context                 # Interactive wizard (recommended, saves to project)
/add-context --update        # Update existing context
/add-context --tech-stack    # Add/update tech stack only
/add-context --patterns      # Add/update code patterns only
/add-context --global        # Save to global config (~/.config/opencode/) instead of project
```

**What the command creates** (verbatim from Quick Start):

> 1. Saves to `.opencode/context/project-intelligence/` in your project (always local)
> 2. Checks for external context files in `.tmp/` (if found, offers to extract)
> 3. Checks for existing project intelligence
> 4. Asks 6 questions (~5 min) OR reviews existing patterns
> 5. Shows full preview of files to be created before writing
> 6. Generates/updates technical-domain.md + navigation.md
> 7. Agents now use YOUR patterns

**Dependencies** (from frontmatter):
- `subagent:context-organizer`
- `context:core/context-system/standards/mvi.md`
- `context:core/context-system/standards/frontmatter.md`
- `context:core/standards/project-intelligence.md`

---

## 2. Frontmatter & Metadata

The `add-context.md` file itself has YAML frontmatter:

```yaml
---
description: Interactive wizard to add project patterns using Project Intelligence standard
tags: [context, onboarding, project-intelligence, wizard]
dependencies:
  - subagent:context-organizer
  - context:core/context-system/standards/mvi.md
  - context:core/context-system/standards/frontmatter.md
  - context:core/standards/project-intelligence.md
---
```

It also contains an XML `<context>` block and a `<role>` definition:

```xml
<context>
  <system>Project Intelligence onboarding wizard for teaching agents YOUR coding patterns</system>
  <domain>Project-specific context creation w/ MVI compliance</domain>
  <task>Interactive 6-question wizard → structured context files w/ 100% pattern preservation</task>
</context>

<role>Context Creation Wizard applying Project Intelligence + MVI + frontmatter standards</role>

<task>6-question wizard → technical-domain.md w/ tech stack, API/component patterns, naming, standards, security</task>
```

---

## 3. Critical Rules (Tier 1 — Absolute Enforcement)

The command defines a `<critical_rules>` block with `priority="absolute"` and `enforcement="strict"`:

| Rule ID | Rule |
|---------|------|
| `project_intelligence` | MUST create technical-domain.md in project-intelligence/ dir (NOT single project-context.md) |
| `frontmatter_required` | ALL files MUST start w/ HTML frontmatter: `<!-- Context: {category}/{function} \| Priority: {level} \| Version: X.Y \| Updated: YYYY-MM-DD -->` |
| `mvi_compliance` | Files MUST be <200 lines, scannable <30s. MVI formula: 1-3 sentence concept, 3-5 key points, 5-10 line example, ref link |
| `codebase_refs` | ALL files MUST include "📂 Codebase References" section linking context→actual code implementation |
| `navigation_update` | MUST update navigation.md when creating/modifying files (add to Quick Routes or Deep Dives table) |
| `priority_assignment` | MUST assign priority based on usage: critical (80%) \| high (15%) \| medium (4%) \| low (1%) |
| `version_tracking` | MUST track versions: New file→1.0 \| Content update→MINOR (1.1, 1.2) \| Structure change→MAJOR (2.0, 3.0) |

---

## 4. Execution Priority & Conflict Resolution

**Tier 1 — Project Intelligence + MVI + Standards** (highest):
- `@project_intelligence` (technical-domain.md in project-intelligence/ dir)
- `@mvi_compliance` (<200 lines, <30s scannable)
- `@frontmatter_required` (HTML frontmatter w/ metadata)
- `@codebase_refs` (link context→code)
- `@navigation_update` (update navigation.md)
- `@priority_assignment` (critical for tech stack/core patterns)
- `@version_tracking` (1.0 for new, incremented for updates)

**Tier 2 — Wizard Workflow**:
- Detect existing context→Review/Add/Replace
- 6-question interactive wizard
- Generate/update technical-domain.md
- Validation w/ MVI checklist

**Tier 3 — User Experience**:
- Clear formatting w/ ━ dividers
- Helpful examples
- Next steps guidance

**Conflict Resolution** (verbatim):

> Tier 1 always overrides Tier 2/3 - standards are non-negotiable

---

## 5. Step-by-Step Flow (Verbatim Stage Descriptions)

### Stage 0.5: Resolve Context Location

**Description** (verbatim):

> Determine where project intelligence files should be saved. This runs BEFORE anything else.

**Default behavior**: Always use local `.opencode/context/project-intelligence/`.

**Override**: `--global` flag saves to `~/.config/opencode/context/project-intelligence/` instead.

**Resolution logic**:
1. If `--global` flag → `$CONTEXT_DIR = ~/.config/opencode/context/project-intelligence/`
2. Otherwise → `$CONTEXT_DIR = .opencode/context/project-intelligence/` (always local)

**If `.opencode/context/` doesn't exist yet**: create it silently — no prompt needed. The directory structure is part of the output shown in Stage 4.

**Variable**: `$CONTEXT_DIR` is set here and used in all subsequent stages.

---

### Stage 0: Check for External Context Files

**Description** (verbatim):

> Check: `.tmp/` directory for external context files (e.g., `.tmp/external-context.md`, `.tmp/context-*.md`)

**Process** (from Implementation Details):
1. Check: `ls .tmp/external-context.md .tmp/context-*.md .tmp/*-context.md 2>/dev/null`
2. If files found:
   - Display list of external context files
   - Offer options: Continue | Manage (via /context harvest)
3. If option 1 (Continue):
   - Proceed to Stage 1 (detect existing project intelligence)
   - External files remain in .tmp/ for later processing via `/context harvest`
4. If option 2 (Manage):
   - Guide user to `/context harvest` command
   - Explain what harvest does (extract, organize, clean)
   - Exit add-context
   - User runs `/context harvest` to process external files
   - User runs `/add-context` again after harvest completes

**If external files found** (verbatim output):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found external context files in .tmp/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files found:
  📄 .tmp/external-context.md (2.4 KB)
  📄 .tmp/api-patterns.md (1.8 KB)
  📄 .tmp/component-guide.md (3.1 KB)

These files can be extracted and organized into permanent context.

Options:
  1. Continue with /add-context (ignore external files for now)
  2. Manage external files first (via /context harvest)

Choose [1/2]: _
```

**If the user chooses to manage external files**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Manage External Context Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To manage external context files, use the /context command:

  /context harvest

This will:
  ✓ Extract knowledge from .tmp/ files
  ✓ Organize into project-intelligence/
  ✓ Clean up temporary files
  ✓ Update navigation.md

After harvesting, run /add-context again to create project intelligence.

Ready to harvest? [y/n]: _
```

- If yes: Exit and run `/context harvest`
- If no: Continue with `/add-context` (Stage 1)

---

### Stage 1: Detect Existing Context

**Description** (verbatim):

> Check: `$CONTEXT_DIR` (set in Stage 0.5 — either `.opencode/context/project-intelligence/` or `~/.config/opencode/context/project-intelligence/`)

**Process** (from Implementation Details — "Pattern Detection"):
1. Check: `ls $CONTEXT_DIR/` (path determined in Stage 0.5)
2. Read: `cat technical-domain.md` (if exists)
3. Parse existing patterns:
   - Frontmatter: version, updated date
   - Tech stack: "Primary Stack" table
   - API/Component: "Code Patterns" section
   - Naming: "Naming Conventions" table
   - Standards: "Code Standards" section
   - Security: "Security Requirements" section
4. Display summary
5. Offer options: Review/Add/Replace/Cancel

**If existing PI found** (verbatim output):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found existing project intelligence!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files found:
  ✓ technical-domain.md (Version: 1.2, Updated: 2026-01-15)
  ✓ business-domain.md (Version: 1.0, Updated: 2026-01-10)
  ✓ navigation.md

Current patterns:
  📦 Tech Stack: Next.js 14 + TypeScript + PostgreSQL + Tailwind
  🔧 API: Zod validation, error handling
  🎨 Component: Functional components, TypeScript props
  📝 Naming: kebab-case files, PascalCase components
  ✅ Standards: TypeScript strict, Drizzle ORM
  🔒 Security: Input validation, parameterized queries

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options:
  1. Review and update patterns (show each one)
  2. Add new patterns (keep all existing)
  3. Replace all patterns (start fresh)
  4. Cancel

Choose [1/2/3/4]: _
```

**If user chooses option 3 ("Replace all")** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Replace All: Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Will BACKUP existing files to:
  .tmp/backup/project-intelligence-{timestamp}/
    ← technical-domain.md (Version: 1.2)
    ← business-domain.md (Version: 1.0)
    ← navigation.md

Will DELETE and RECREATE:
  $CONTEXT_DIR/technical-domain.md (new Version: 1.0)
  $CONTEXT_DIR/navigation.md (new Version: 1.0)

Existing files backed up → you can restore from .tmp/backup/ if needed.

Proceed? [y/n]: _
```

**If no existing PI found** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No project intelligence found. Let's create it!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Saving to: $CONTEXT_DIR

Will create:
  - project-intelligence/technical-domain.md (tech stack & patterns)
  - project-intelligence/navigation.md (quick overview)

Takes ~5 min. Follows @mvi_compliance (<200 lines).

Ready? [y/n]: _
```

---

### Stage 1.5: Review Existing Patterns (if updating)

**Description** (verbatim):

> **Only runs if user chose "Review and update" in Stage 1.**
>
> For each pattern, show current→ask Keep/Update/Remove:

**Pattern 1: Tech Stack** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern 1/6: Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current:
  Framework: Next.js 14
  Language: TypeScript
  Database: PostgreSQL
  Styling: Tailwind

Options: 1. Keep | 2. Update | 3. Remove
Choose [1/2/3]: _

If '2': New tech stack: _
```

**Pattern 2: API Pattern** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern 2/6: API Pattern
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current API pattern:
```typescript
export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = schema.parse(body)
    return Response.json({ success: true })
  } catch (error) {
    return Response.json({ error: error.message }, { status: 400 })
  }
}
```

Options: 1. Keep | 2. Update | 3. Remove
Choose [1/2/3]: _

If '2': Paste new API pattern: _
```

**Pattern 3-6: Component, Naming, Standards, Security**:

> *(Same format: show current→Keep/Update/Remove)*

**After reviewing all patterns** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changes:
  ✓ Tech Stack: Updated (Next.js 14 → Next.js 15)
  ✓ API: Kept
  ✓ Component: Updated (new pattern)
  ✓ Naming: Kept
  ✓ Standards: Updated (+2 new)
  ✓ Security: Kept

Version: 1.2 → 1.3 (content update per @version_tracking)
Updated: 2026-01-29

Proceed? [y/n]: _
```

---

### Stage 2: Interactive Wizard (for new patterns)

This is the 6-question wizard, covered in detail in [Section 6](#6-the-6-wizard-questions--exact-prompts--capture) below.

---

### Stage 3: Generate/Update Context

**Description**: Preview what will be written before writing it.

**Preview of `technical-domain.md`** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preview: technical-domain.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- Context: project-intelligence/technical | Priority: critical | Version: 1.0 | Updated: 2026-01-29 -->

# Technical Domain

**Purpose**: Tech stack, architecture, development patterns for this project.
**Last Updated**: 2026-01-29

## Quick Reference
**Update Triggers**: Tech stack changes | New patterns | Architecture decisions
**Audience**: Developers, AI agents

## Primary Stack
| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Framework | {framework} | {version} | {why} |
| Language | {language} | {version} | {why} |
| Database | {database} | {version} | {why} |
| Styling | {styling} | {version} | {why} |

## Code Patterns
### API Endpoint
```{language}
{user_api_pattern}
```

### Component
```{language}
{user_component_pattern}
```

## Naming Conventions
| Type | Convention | Example |
|------|-----------|---------|
| Files | {file_naming} | {example} |
| Components | {component_naming} | {example} |
| Functions | {function_naming} | {example} |
| Database | {db_naming} | {example} |

## Code Standards
{user_code_standards}

## Security Requirements
{user_security_requirements}

## 📂 Codebase References
**Implementation**: `{detected_files}` - {desc}
**Config**: package.json, tsconfig.json

## Related Files
- Business Domain (example: business-domain.md)
- Decisions Log (example: decisions-log.md)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Size: {line_count} lines (limit: 200 per @mvi_compliance)
Status: ✅ MVI compliant

Save to: $CONTEXT_DIR/technical-domain.md

Looks good? [y/n/edit]: _
```

**Post-preview actions** (verbatim):

> - Confirm: Write file per @project_intelligence
> - Edit: Open in editor→validate after
> - Update: Show diff→highlight new→confirm

---

### Stage 4: Validation & Creation

**Validation output** (verbatim):

```
Running validation...

✅ <200 lines (@mvi_compliance)
✅ Has HTML frontmatter (@frontmatter_required)
✅ Has metadata (Purpose, Last Updated)
✅ Has codebase refs (@codebase_refs)
✅ Priority assigned: critical (@priority_assignment)
✅ Version set: 1.0 (@version_tracking)
✅ MVI compliant (<30s scannable)
✅ No duplication
```

**navigation.md preview** (also created/updated) (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preview: navigation.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Project Intelligence

| File | Description | Priority |
|------|-------------|----------|
| technical-domain.md | Tech stack & patterns | critical |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Full creation plan** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files to write:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  CREATE  $CONTEXT_DIR/technical-domain.md ({line_count} lines)
  CREATE  $CONTEXT_DIR/navigation.md ({nav_line_count} lines)

Total: 2 files

Proceed? [y/n]: _
```

---

### Stage 5: Confirmation & Next Steps

**Final output** (verbatim):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Project Intelligence created successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files created:
  $CONTEXT_DIR/technical-domain.md
  $CONTEXT_DIR/navigation.md

Location: $CONTEXT_DIR
Agents now use YOUR patterns automatically!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What's next?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test it:
   opencode --agent OpenCoder
   > "Create API endpoint"
   (Uses YOUR pattern!)

2. Review: cat $CONTEXT_DIR/technical-domain.md

3. Add business context: /add-context --business

4. Build: opencode --agent OpenCoder > "Create user auth system"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Tip: Update context as project evolves
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When you:
  Add library → /add-context --update
  Change patterns → /add-context --update
  Migrate tech → /add-context --update

Agents stay synced!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Tip: Global patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Want the same patterns across ALL your projects?
  /add-context --global
  → Saves to ~/.config/opencode/context/project-intelligence/
  → Acts as fallback for projects without local context

Already have global patterns? Bring them into this project:
  /context migrate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Learn More
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Project Intelligence: .opencode/context/core/standards/project-intelligence.md
- MVI Principles: .opencode/context/core/context-system/standards/mvi.md
- Context System: CONTEXT_SYSTEM_GUIDE.md
```

---

## 6. The 6 Wizard Questions — Exact Prompts & Capture

The wizard runs during **Stage 2** and is titled "Interactive Wizard (for new patterns)".

### Q1: Tech Stack (verbatim)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q 1/6: What's your tech stack?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Examples:
  1. Next.js + TypeScript + PostgreSQL + Tailwind
  2. React + Python + MongoDB + Material-UI
  3. Vue + Go + MySQL + Bootstrap
  4. Other (describe)

Your tech stack: _
```

**Capture**: Framework, Language, Database, Styling

### Q2: API Pattern (verbatim)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q 2/6: API endpoint example?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Paste API endpoint from YOUR project (matches your API style).

Example (Next.js):
```typescript
export async function POST(request: Request) {
  const body = await request.json()
  const validated = schema.parse(body)
  return Response.json({ success: true })
}
```

Your API pattern (paste or 'skip'): _
```

**Capture**: API endpoint, error handling, validation, response format

### Q3: Component Pattern (verbatim)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q 3/6: Component example?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Paste component from YOUR project.

Example (React):
```typescript
interface UserCardProps { name: string; email: string }
export function UserCard({ name, email }: UserCardProps) {
  return <div className="rounded-lg border p-4">
    <h3>{name}</h3><p>{email}</p>
  </div>
}
```

Your component (paste or 'skip'): _
```

**Capture**: Component structure, props pattern, styling, TypeScript

### Q4: Naming Conventions (verbatim)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q 4/6: Naming conventions?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Examples:
  Files: kebab-case (user-profile.tsx)
  Components: PascalCase (UserProfile)
  Functions: camelCase (getUserProfile)
  Database: snake_case (user_profiles)

Your conventions:
  Files: _
  Components: _
  Functions: _
  Database: _
```

**Capture**: Four naming convention fields (Files, Components, Functions, Database)

### Q5: Code Standards (verbatim)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q 5/6: Code standards?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Examples:
  - TypeScript strict mode
  - Validate w/ Zod
  - Use Drizzle for DB queries
  - Prefer server components

Your standards (one/line, 'done' when finished):
  1. _
```

**Capture**: List of strings (code standards, one per line)

### Q6: Security Requirements (verbatim)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Q 6/6: Security requirements?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Examples:
  - Validate all user input
  - Use parameterized queries
  - Sanitize before rendering
  - HTTPS only

Your requirements (one/line, 'done' when finished):
  1. _
```

**Capture**: List of strings (security requirements, one per line)

---

## 7. The `--update` Flag

The `--update` flag is used to update existing patterns. Here's how it flows:

### Invocation

```bash
/add-context --update        # Update existing context
```

### Flow with `--update`

When `--update` is specified, the wizard goes to **Stage 1** (Detect Existing Context). Since existing PI will be found, the user is presented with the four options:

1. Review and update patterns (show each one)
2. Add new patterns (keep all existing)
3. Replace all patterns (start fresh)
4. Cancel

**Option 1 — Review and update**: This triggers **Stage 1.5** where each of the 6 patterns is shown individually with Keep/Update/Remove options. After review, a summary is shown with version bump (e.g., `1.2 → 1.3`), and the user confirms.

**Option 2 — Add new patterns**: Keeps all existing patterns and allows adding new ones. The wizard runs Stage 2 for the new patterns only.

**Option 3 — Replace all**: Creates a backup of existing files to `.tmp/backup/project-intelligence-{timestamp}/`, then DELETES and RECREATES files starting at Version 1.0.

**Option 4 — Cancel**: Exits.

### Additional Update Flags

There are also targeted update flags:

- `--tech-stack`: Add/update tech stack only (bumps version MINOR, e.g., `1.4 → 1.5`)
- `--patterns`: Add/update code patterns only

### Version Behavior on Update

From **Stage 1.5** (verbatim):

> Version: 1.2 → 1.3 (content update per @version_tracking)

Content updates get MINOR bumps. Structural changes get MAJOR bumps.

### Implementation Details for Pattern Detection (Stage 1 — used by --update)

The process reads and parses existing files:
1. Check: `ls $CONTEXT_DIR/`
2. Read: `cat technical-domain.md` (if exists)
3. Parse existing patterns by section:
   - Frontmatter → version, updated date
   - "Primary Stack" table → tech stack
   - "Code Patterns" section → API/Component
   - "Naming Conventions" table → naming
   - "Code Standards" section → standards
   - "Security Requirements" section → security
4. Display summary
5. Offer options: Review/Add/Replace/Cancel

---

## 8. The `--global` Flag

### Invocation

```bash
/add-context --global        # Save to global config (~/.config/opencode/) instead of project
```

### Behavior

The `--global` flag is resolved in **Stage 0.5** (Resolve Context Location), which runs BEFORE anything else.

**Default behavior**: Always use local `.opencode/context/project-intelligence/`.

**Override**: `--global` flag saves to `~/.config/opencode/context/project-intelligence/` instead.

**Resolution logic** (verbatim):
1. If `--global` flag → `$CONTEXT_DIR = ~/.config/opencode/context/project-intelligence/`
2. Otherwise → `$CONTEXT_DIR = .opencode/context/project-intelligence/` (always local)

The `$CONTEXT_DIR` variable, once set in Stage 0.5, is used in ALL subsequent stages. So every reference to `$CONTEXT_DIR` in Stages 1-5 resolves to either the local or global path.

### Global vs Local (from Troubleshooting section, verbatim)

> **Q: Local vs global?**
> A: Local (`.opencode/`) = project-specific, committed to git, team-shared. Global (`~/.config/opencode/`) = personal defaults across all projects. Local overrides global.

> **Q: Installed globally but want project patterns?**
> A: Run `/add-context` (defaults to local). Creates `.opencode/context/project-intelligence/` in your project even if OAC was installed globally.

### Global Patterns Tip (from Stage 5 output, verbatim)

> Want the same patterns across ALL your projects?
> `/add-context --global`
> → Saves to ~/.config/opencode/context/project-intelligence/
> → Acts as fallback for projects without local context

---

## 9. Existing Context Detection & Offer to Review/Update/Add/Replace/Cancel

This is the core of **Stage 1** and **Stage 1.5**.

### Detection

The command checks `$CONTEXT_DIR/` (resolved in Stage 0.5). If `technical-domain.md` exists, it parses:
- Frontmatter: version, updated date
- Tech stack: "Primary Stack" table
- API/Component: "Code Patterns" section
- Naming: "Naming Conventions" table
- Standards: "Code Standards" section
- Security: "Security Requirements" section

### The Four Options

When existing PI is found, the user gets exactly these 4 options:

| Option | Label | Behavior |
|--------|-------|----------|
| 1 | Review and update patterns (show each one) | Enters Stage 1.5: shows each of 6 patterns one by one, asks Keep/Update/Remove |
| 2 | Add new patterns (keep all existing) | Keeps all existing, adds new ones via Stage 2 |
| 3 | Replace all patterns (start fresh) | Backs up existing to `.tmp/backup/project-intelligence-{timestamp}/`, deletes and recreates at Version 1.0 |
| 4 | Cancel | Exits the wizard |

### Replace All Detail

When "Replace all" is chosen, a preview is shown:

```
Will BACKUP existing files to:
  .tmp/backup/project-intelligence-{timestamp}/
    ← technical-domain.md (Version: 1.2)
    ← business-domain.md (Version: 1.0)
    ← navigation.md

Will DELETE and RECREATE:
  $CONTEXT_DIR/technical-domain.md (new Version: 1.0)
  $CONTEXT_DIR/navigation.md (new Version: 1.0)

Existing files backed up → you can restore from .tmp/backup/ if needed.

Proceed? [y/n]: _
```

Key points about "Replace all":
- All existing files are backed up before deletion
- Backups go to `.tmp/backup/project-intelligence-{timestamp}/`
- New files start at Version 1.0
- Both `technical-domain.md` AND `navigation.md` are recreated

### Add New Patterns Detail

Option 2 preserves all existing content and runs the Stage 2 wizard for any new patterns the user wants to add. Existing patterns remain untouched.

---

## 10. Validation Rules (MVI, Frontmatter, etc.)

### MVI Compliance

From the `@mvi_compliance` critical rule:

> Files MUST be <200 lines, scannable <30s. MVI formula: 1-3 sentence concept, 3-5 key points, 5-10 line example, ref link

The Stage 4 validation checks:
```
✅ <200 lines (@mvi_compliance)
✅ MVI compliant (<30s scannable)
```

If a file exceeds 200 lines, the error message is (verbatim):

```
⚠️ Exceeds 200 lines (@mvi_compliance)
Current: 245 | Limit: 200

Simplify patterns or split into multiple files.
```

### Frontmatter Validation

From `@frontmatter_required`:

> ALL files MUST start w/ HTML frontmatter: `<!-- Context: {category}/{function} | Priority: {level} | Version: X.Y | Updated: YYYY-MM-DD -->`

Stage 4 checks:
```
✅ Has HTML frontmatter (@frontmatter_required)
```

### Metadata Validation

Stage 4 checks:
```
✅ Has metadata (Purpose, Last Updated)
```

The generated `technical-domain.md` includes:
```
**Purpose**: Tech stack, architecture, development patterns for this project.
**Last Updated**: 2026-01-29
```

### Codebase References Validation

From `@codebase_refs`:

> ALL files MUST include "📂 Codebase References" section linking context→actual code implementation

Stage 4 checks:
```
✅ Has codebase refs (@codebase_refs)
```

The generated `technical-domain.md` includes:
```
## 📂 Codebase References
**Implementation**: `{detected_files}` - {desc}
**Config**: package.json, tsconfig.json
```

### Priority Assignment Validation

From `@priority_assignment`:

> MUST assign priority based on usage: critical (80%) | high (15%) | medium (4%) | low (1%)

Stage 4 checks:
```
✅ Priority assigned: critical (@priority_assignment)
```

For the primary `technical-domain.md` generated by `/add-context`, the priority is always `critical` (matching the 80% use case weight).

### Version Tracking Validation

From `@version_tracking`:

> MUST track versions: New file→1.0 | Content update→MINOR (1.1, 1.2) | Structure change→MAJOR (2.0, 3.0)

Stage 4 checks:
```
✅ Version set: 1.0 (@version_tracking)
```

### No Duplication Check

Stage 4 also validates:
```
✅ No duplication
```

### Complete Validation Checklist

The 8-point validation checklist in Stage 4:

1. ✅ <200 lines (@mvi_compliance)
2. ✅ Has HTML frontmatter (@frontmatter_required)
3. ✅ Has metadata (Purpose, Last Updated)
4. ✅ Has codebase refs (@codebase_refs)
5. ✅ Priority assigned: critical (@priority_assignment)
6. ✅ Version set: 1.0 (@version_tracking)
7. ✅ MVI compliant (<30s scannable)
8. ✅ No duplication

### Error: Invalid Input

```
⚠️ Invalid input
Expected: Tech stack description
Got: [empty]

Example: Next.js + TypeScript + PostgreSQL + Tailwind
```

### Error: Invalid Syntax

```
⚠️ Invalid code syntax in API pattern
Error: Unexpected token line 3

Check code & retry.
```

---

## 11. Navigation.md Update Process

### When Updated

From `@navigation_update` critical rule:

> MUST update navigation.md when creating/modifying files (add to Quick Routes or Deep Dives table)

Navigation.md is updated in two scenarios:
1. **Creation**: When `/add-context` creates new files, `navigation.md` is created/updated alongside them.
2. **Modification**: When `/add-context --update` modifies existing files, `navigation.md` is updated to reflect changes.

### What Gets Updated

In **Stage 4**, navigation.md is created/updated alongside technical-domain.md:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Preview: navigation.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Project Intelligence

| File | Description | Priority |
|------|-------------|----------|
| technical-domain.md | Tech stack & patterns | critical |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### The Template navigation.md

The actual navigation.md template from the repository has this structure:

```html
<!-- Context: project-intelligence/nav | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Project Intelligence

> Start here for quick project understanding. These files bridge business and technical domains.

## Structure
[directory tree]

## Quick Routes
[table mapping needs → files]

## Usage
[new team member / agent instructions]

## Integration
[references to standards and system files]

## Maintenance
[update triggers and guide references]
```

The key table that `/add-context` adds rows to is the **Quick Routes** table, with columns: `What You Need`, `File`, `Description` — plus a `Priority` column in the Stage 4 preview.

For new file creation, the generation plan always includes BOTH files:

```
CREATE  $CONTEXT_DIR/technical-domain.md ({line_count} lines)
CREATE  $CONTEXT_DIR/navigation.md ({nav_line_count} lines)
```

### From the Management Guide

The project-intelligence-management.md states the process for adding new files:
1. Create file in `project-intelligence/`
2. Add frontmatter with `project-intelligence/{filename}`
3. Follow existing file patterns
4. Keep under 200 lines
5. Add to `navigation.md`

---

## 12. Version Tracking

### Version Rules (from project-intelligence-management.md)

| Change Type | Version Bump |
|-------------|-------------|
| New file | 1.0 |
| Content addition/update | MINOR (e.g., 1.1, 1.2) |
| Structure change | MAJOR (e.g., 2.0, 3.0) |
| Typo fix | PATCH |

### Frontmatter Version Format

```html
<!-- Context: {category} | Priority: {level} | Version: {MAJOR.MINOR} | Updated: {YYYY-MM-DD} -->
```

### How /add-context Applies Versioning

**New files**: Always start at `1.0`.

**Content updates** (via Stage 1.5 — Review and Update):
- Example: `Version: 1.2 → 1.3 (content update per @version_tracking)`
- Each pattern that is updated increments the MINOR version.

**Quick update** (via `--tech-stack` or `--patterns`):
- Also results in MINOR bump. Example from the docs: `Version 1.4 → 1.5`

**Replace all** (Option 3 in Stage 1):
- Resets to `1.0`.

**Structure changes**:
- Trigger a MAJOR bump (e.g., `1.x → 2.0`). This would happen if the file's format/structure fundamentally changes.

### Date Format

Always `YYYY-MM-DD` per the management guide.

---

## 13. Frontmatter Format — Exact Specification

### HTML Frontmatter (used by /add-context output files)

The frontmatter format required by `@frontmatter_required`:

```html
<!-- Context: {category}/{function} | Priority: {level} | Version: {X.Y} | Updated: {YYYY-MM-DD} -->
```

**Fields explained**:

| Field | Description | Example Values |
|-------|-------------|----------------|
| `Context` | Category and function, using path-like notation | `project-intelligence/technical`, `project-intelligence/business`, `project-intelligence/bridge`, `project-intelligence/decisions`, `project-intelligence/notes`, `project-intelligence/nav` |
| `Priority` | Usage frequency classification | `critical` (80%), `high` (15%), `medium` (4%), `low` (1%) |
| `Version` | Semantic version MAJOR.MINOR | `1.0` for new, `1.1`, `1.2` for content updates, `2.0` for structure changes |
| `Updated` | Last update date | `2026-01-29` (YYYY-MM-DD) |

### Actual Frontmatter Examples from Repository Files

**technical-domain.md**:
```html
<!-- Context: project-intelligence/technical | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->
```

**business-domain.md**:
```html
<!-- Context: project-intelligence/business | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->
```

**business-tech-bridge.md**:
```html
<!-- Context: project-intelligence/bridge | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->
```

**decisions-log.md**:
```html
<!-- Context: project-intelligence/decisions | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->
```

**living-notes.md**:
```html
<!-- Context: project-intelligence/notes | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->
```

**navigation.md**:
```html
<!-- Context: project-intelligence/nav | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->
```

**NOTE**: The `add-context.md` command itself uses `Priority: critical` for `technical-domain.md` in its preview:

```html
<!-- Context: project-intelligence/technical | Priority: critical | Version: 1.0 | Updated: 2026-01-29 -->
```

But the actual template file `technical-domain.md` has `Priority: high`. The command's Stage 3 preview uses `critical` per the `@priority_assignment` rule that tech stack/core patterns should be `critical` (80% usage).

---

## 14. Template/Format for Each Project Intelligence File

### technical-domain.md (created by /add-context)

The template generated by `/add-context` Stage 3:

```html
<!-- Context: project-intelligence/technical | Priority: critical | Version: 1.0 | Updated: {date} -->

# Technical Domain

**Purpose**: Tech stack, architecture, development patterns for this project.
**Last Updated**: {date}

## Quick Reference
**Update Triggers**: Tech stack changes | New patterns | Architecture decisions
**Audience**: Developers, AI agents

## Primary Stack
| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Framework | {framework} | {version} | {why} |
| Language | {language} | {version} | {why} |
| Database | {database} | {version} | {why} |
| Styling | {styling} | {version} | {why} |

## Code Patterns
### API Endpoint
```{language}
{user_api_pattern}
```

### Component
``` {language}
{user_component_pattern}
```

## Naming Conventions
| Type | Convention | Example |
|------|-----------|---------|
| Files | {file_naming} | {example} |
| Components | {component_naming} | {example} |
| Functions | {function_naming} | {example} |
| Database | {db_naming} | {example} |

## Code Standards
{user_code_standards}

## Security Requirements
{user_security_requirements}

## 📂 Codebase References
**Implementation**: `{detected_files}` - {desc}
**Config**: package.json, tsconfig.json

## Related Files
- Business Domain (example: business-domain.md)
- Decisions Log (example: decisions-log.md)
```

Key structural elements:
- HTML frontmatter with `Context: project-intelligence/technical`
- `# Technical Domain` heading
- `**Purpose**` and `**Last Updated**` metadata lines
- `## Quick Reference` with Update Triggers and Audience
- `## Primary Stack` — 4-column table (Layer/Technology/Version/Rationale)
- `## Code Patterns` — two sub-sections: API Endpoint and Component
- `## Naming Conventions` — 3-column table (Type/Convention/Example) with 4 rows
- `## Code Standards` — user-provided list
- `## Security Requirements` — user-provided list
- `## 📂 Codebase References` — Implementation and Config links
- `## Related Files` — cross-references to other PI files

### navigation.md (created/updated by /add-context)

The `add-context` command creates a minimal navigation.md:

```markdown
# Project Intelligence

| File | Description | Priority |
|------|-------------|----------|
| technical-domain.md | Tech stack & patterns | critical |
```

But the full template from the repository is much richer:

```html
<!-- Context: project-intelligence/nav | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Project Intelligence

> Start here for quick project understanding. These files bridge business and technical domains.

## Structure
[directory tree showing all PI files]

## Quick Routes
[table mapping needs → files with descriptions]

## Usage
[New Team Member / Agent instructions]

## Integration
[References to standards and system files]

## Maintenance
[Update triggers and management guide reference]
```

### business-domain.md (template, NOT created by /add-context by default)

```
<!-- Context: project-intelligence/business | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Business Domain

> Document the business context, problems solved, and value created.

## Quick Reference
- **Purpose**: Understand why this project exists
- **Update When**: Business direction changes, new features shipped, pivot
- **Audience**: Developers needing context, stakeholders, product team

## Project Identity
[Project Name, Tagline, Problem Statement, Solution]

## Target Users
[Table: User Segment / Who They Are / What They Need / Pain Points]

## Value Proposition
[For Users: key benefits]
[For Business: key value]

## Success Metrics
[Table: Metric / Definition / Target / Current]

## Business Model
[Revenue Model, Pricing Strategy, Unit Economics, Market Position]

## Key Stakeholders
[Table: Role / Name / Responsibility / Contact]

## Roadmap Context
[Current Focus / Next Milestone / Long-term Vision]

## Business Constraints
[Constraint list with reasons]

## Onboarding Checklist
[Checkboxes]

## Related Files
- `technical-domain.md`
- `business-tech-bridge.md`
- `decisions-log.md`
```

### technical-domain.md (full repository template, for reference)

The repository's own template file is more comprehensive than what `/add-context` generates. It includes sections for:

- Quick Reference (Purpose, Update When, Audience)
- Primary Stack (4-column table)
- Architecture Pattern (Type/Pattern/Diagram + "Why This Architecture?")
- Project Structure (directory tree + Key Directories)
- Key Technical Decisions (3-column table pointing to decisions-log.md)
- Integration Points (4-column table: System/Purpose/Protocol/Direction)
- Technical Constraints (3-column table: Constraint/Origin/Impact)
- Development Environment (Setup/Requirements/Local Dev/Testing)
- Deployment (Environment/Platform/CI/CD/Monitoring)
- Onboarding Checklist
- Related Files

The `/add-context` wizard produces a simpler version focusing on the 6 captured patterns (tech stack, API, component, naming, standards, security).

### business-tech-bridge.md (template)

```
<!-- Context: project-intelligence/bridge | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Business ↔ Tech Bridge

> Document how business needs translate to technical solutions.

## Quick Reference
- **Purpose**: Show stakeholders technical choices serve business goals
- **Purpose**: Show developers business constraints drive architecture
- **Update When**: New features, refactoring, business pivot

## Core Mapping
[Table: Business Need / Technical Solution / Why This Mapping / Business Value]

## Feature Mapping Examples
[Per-feature sections with Business Context / Technical Implementation / Connection]

## Trade-off Decisions
[Table: Situation / Business Priority / Technical Priority / Decision Made / Rationale]

## Common Misalignments
[Table: Misalignment / Warning Signs / Resolution Approach]

## Stakeholder Communication
[For Business Stakeholders / For Technical Stakeholders]

## Onboarding Checklist
[Checkboxes]

## Related Files
- `business-domain.md`
- `technical-domain.md`
- `decisions-log.md`
- `living-notes.md`
```

### decisions-log.md (template)

```
<!-- Context: project-intelligence/decisions | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Decisions Log

> Record major architectural and business decisions with full context.

## Quick Reference
- **Purpose**: Document decisions so future team members understand context
- **Format**: Each decision as a separate entry
- **Status**: Decided | Pending | Under Review | Deprecated

## Decision Template
[Full template with Date/Status/Owner/Context/Decision/Rationale/Alternatives Considered/Impact/Related]

## Decision: [Title]
[Filled-in decision entries]

## Decision: [Title]
[Filled-in decision entries]

## Deprecated Decisions
[Table: Decision / Date / Replaced By / Why]

## Onboarding Checklist
[Checkboxes]

## Related Files
- `technical-domain.md`
- `business-tech-bridge.md`
- `living-notes.md`
```

Each decision entry has:
- Date, Status, Owner
- Context, Decision, Rationale
- Alternatives Considered (table)
- Impact (Positive/Negative/Risk)
- Related links

### living-notes.md (template)

```
<!-- Context: project-intelligence/notes | Priority: high | Version: 1.0 | Updated: 2025-01-12 -->

# Living Notes

> Active issues, technical debt, open questions, and insights. Keep this alive.

## Quick Reference
- **Purpose**: Capture current state, problems, and open questions
- **Update**: Weekly or when status changes
- **Archive**: Move resolved items to bottom with status

## Technical Debt
[Table: Item / Impact / Priority / Mitigation]
[Details sub-section per item]

## Open Questions
[Table: Question / Stakeholders / Status / Next Action]
[Details sub-section per question]

## Known Issues
[Table: Issue / Severity / Workaround / Status]
[Details sub-section per issue]

## Insights & Lessons Learned
[What Works Well / What Could Be Better / Lessons Learned]

## Patterns & Conventions
[Code Patterns Worth Preserving / Gotchas for Maintainers]

## Active Projects
[Table: Project / Goal / Owner / Timeline]

## Archive (Resolved Items)
[Moved resolved items.]

## Onboarding Checklist
[Checkboxes]

## Related Files
- `decisions-log.md`
- `business-domain.md`
- `technical-domain.md`
- `business-tech-bridge.md`
```

---

## 15. Relationship Between technical-domain.md and Other PI Files

### The PI System as a Whole

From `project-intelligence.md` (the standard):

```
.opencode/context/
├── project-intelligence/              # Project-specific context
│   ├── navigation.md                  # Quick overview & routes
│   ├── business-domain.md             # Business context, problems solved
│   ├── technical-domain.md            # Stack, architecture, decisions
│   ├── business-tech-bridge.md        # How business needs → solutions
│   ├── decisions-log.md               # Decisions with rationale
│   └── living-notes.md                # Active issues, technical debt
└── core/                              # Universal standards
```

### Quick Reference Table (from the standard)

| What You Need | File | Description |
|---------------|------|-------------|
| Understand the "why" | `business-domain.md` | Problem, users, value |
| Understand the "how" | `technical-domain.md` | Stack, architecture |
| See the connection | `business-tech-bridge.md` | Business → technical mapping |
| Know the context | `decisions-log.md` | Why decisions were made |
| Current state | `living-notes.md` | Active issues, debt, questions |

### technical-domain.md Specifically

**technical-domain.md** is the **primary output** of the `/add-context` wizard. It captures:
- The 6 wizard answers (tech stack, API pattern, component pattern, naming, standards, security)
- Links to codebase references and configuration files

**Its relationship to other files**:

1. **navigation.md** — The index/overview. `technical-domain.md` must be listed in navigation.md's Quick Routes table. When `/add-context` creates/updates `technical-domain.md`, it simultaneously creates/updates `navigation.md`.

2. **business-domain.md** — The "why" to technical-domain's "how". technical-domain.md references business-domain.md in its "Related Files" section. The standard states: Read business-domain.md to understand the "why", then technical-domain.md to understand the "how".

3. **business-tech-bridge.md** — Maps business needs to technical solutions. technical-domain.md provides the technical side of this mapping. The bridge file has "Core Mapping" and "Feature Mapping" tables that connect business needs from business-domain.md to technical solutions in technical-domain.md.

4. **decisions-log.md** — Contains the full decision history with alternatives considered. technical-domain.md has a "Key Technical Decisions" table that summarizes decisions, with a link pointing to decisions-log.md for full context. Cross-referenced in both files' "Related Files" sections.

5. **living-notes.md** — Contains active issues, technical debt, and open questions. technical-domain.md is referenced in living-notes.md's "Related Files". Living notes may contain technical issues that relate to patterns documented in technical-domain.md.

### The Onboarding Flow (from the standard)

For new team members or agents:
1. Read `navigation.md` (overview)
2. Read `business-domain.md` (understand the "why")
3. Read `technical-domain.md` (understand the "how")
4. Review `business-tech-bridge.md` (see the connection)
5. Check `decisions-log.md` (context on key choices)
6. Review `living-notes.md` (current state)
7. Explore codebase with this context loaded

### How `/add-context` Creates the Relationship

The `/add-context` wizard specifically:
- Creates `technical-domain.md` with a "Related Files" section that links to business-domain.md and decisions-log.md
- Creates/updates `navigation.md` with an entry for `technical-domain.md`
- The Stage 5 "What's next?" output suggests: "Add business context: /add-context --business"

This means that `/add-context` by default only creates the technical domain and navigation. The other PI files (business-domain.md, business-tech-bridge.md, decisions-log.md, living-notes.md) are created either:
- Manually by the user
- Via `/add-context --business` (referenced in next steps)
- Via the `/context harvest` command

---

## 16. Delegation to ContextOrganizer

The command delegates file creation/update to the `context-organizer` subagent (listed as a dependency). The delegation specification:

```yaml
operation: create | update
template: technical-domain  # Project Intelligence template
target_directory: project-intelligence

# For create/update operations
user_responses:
  tech_stack: {framework, language, database, styling}
  api_pattern: string | null
  component_pattern: string | null
  naming_conventions: {files, components, functions, database}
  code_standards: string[]
  security_requirements: string[]
  
frontmatter:
  context: project-intelligence/technical
  priority: critical  # @priority_assignment (80% use cases)
  version: {calculated}  # @version_tracking
  updated: {current_date}

validation:
  max_lines: 200  # @mvi_compliance
  has_frontmatter: true  # @frontmatter_required
  has_codebase_references: true  # @codebase_refs
  navigation_updated: true  # @navigation_update
```

Key points about delegation:
- The `operation` parameter is either `create` or `update`
- The `template` specifies `technical-domain` as the Project Intelligence template
- The `target_directory` is `project-intelligence`
- `user_responses` captures all 6 wizard questions as structured data
- `frontmatter` is auto-generated with `context: project-intelligence/technical`, `priority: critical`, calculated `version`, and current `date`
- `validation` enforces: max 200 lines, has frontmatter, has codebase refs, and navigation updated
- `api_pattern` and `component_pattern` can be `null` (if user skips Q2 or Q3)

---

## 17. Error Handling

### Invalid Input

```
⚠️ Invalid input
Expected: Tech stack description
Got: [empty]

Example: Next.js + TypeScript + PostgreSQL + Tailwind
```

### File Too Large

```
⚠️ Exceeds 200 lines (@mvi_compliance)
Current: 245 | Limit: 200

Simplify patterns or split into multiple files.
```

### Invalid Syntax

```
⚠️ Invalid code syntax in API pattern
Error: Unexpected token line 3

Check code & retry.
```

---

## 18. Success Criteria Checklist

### User Experience

- [ ] Wizard complete <5 min
- [ ] Next steps clear
- [ ] Update process understood

### File Quality

- [ ] @mvi_compliance (<200 lines, <30s scannable)
- [ ] @frontmatter_required (HTML frontmatter)
- [ ] @codebase_refs (codebase references section)
- [ ] @priority_assignment (critical for tech stack)
- [ ] @version_tracking (1.0 new, incremented updates)

### System Integration

- [ ] @project_intelligence (technical-domain.md in project-intelligence/)
- [ ] @navigation_update (navigation.md updated)
- [ ] Agents load & use patterns
- [ ] No duplication

---

## Appendix A: Complete Stage Flow Summary

```
Stage 0.5: Resolve Context Location
  ↓ Sets $CONTEXT_DIR (local or global)

Stage 0: Check for External Context Files
  ↓ If found → offer to Continue or Manage (/context harvest)

Stage 1: Detect Existing Context
  ↓ If found → Review/Add/Replace/Cancel
  ↓ If not found → Confirm creation

Stage 1.5: Review Existing Patterns (if "Review and update" chosen)
  ↓ Show each of 6 patterns → Keep/Update/Remove
  ↓ Calculate version bump (MINOR for content, MAJOR for structure)

Stage 2: Interactive Wizard (for new or updated patterns)
  ↓ Q1: Tech Stack → Capture framework, language, database, styling
  ↓ Q2: API Pattern → Capture endpoint, error handling, validation, response
  ↓ Q3: Component Pattern → Capture structure, props, styling, TypeScript
  ↓ Q4: Naming Conventions → Capture files, components, functions, database naming
  ↓ Q5: Code Standards → Capture list of standards
  ↓ Q6: Security Requirements → Capture list of requirements

Stage 3: Generate/Update Context
  ↓ Preview technical-domain.md
  ↓ Confirm/Edit/Update

Stage 4: Validation & Creation
  ↓ 8-point MVI/frontmatter/metadata/codebase-refs/priority/version/duplication check
  ↓ Preview navigation.md
  ↓ Show creation plan
  ↓ Confirm

Stage 5: Confirmation & Next Steps
  ↓ Show success message
  ↓ Show "What's next?" guidance
  ↓ Show tips for updating and global patterns
  ↓ Show "Learn More" references
```

## Appendix B: File Structure Inference

When `/add-context` detects a tech stack, it infers common project structure:

| Stack | Inferred Structure |
|-------|-------------------|
| Next.js | `src/app/ components/ lib/ db/` |
| React | `src/components/ hooks/ utils/ api/` |
| Express | `src/routes/ controllers/ models/ middleware/` |

This drives the "📂 Codebase References" section in the generated technical-domain.md.

## Appendix C: Tips (from the command)

> **Keep Simple**: Focus on most common patterns, add more later
> **Use Real Examples**: Paste actual code from YOUR project
> **Update Regularly**: Run `/add-context --update` when patterns change
> **Test After**: Build something simple to verify agents use patterns correctly

## Appendix D: Troubleshooting (from the command)

| Question | Answer |
|----------|--------|
| Agents not using patterns? | Check file exists, <200 lines. Run `/context validate` |
| See what's in context? | `cat .opencode/context/project-intelligence/technical-domain.md` (local) or `cat ~/.config/opencode/context/project-intelligence/technical-domain.md` (global) |
| Multiple context files? | Yes! Create in your project-intelligence directory. Agents load all. |
| Remove pattern? | Edit directly: `nano .opencode/context/project-intelligence/technical-domain.md` |
| Share w/ team? | Yes! Use local install (`.opencode/context/project-intelligence/`) and commit to repo. Team members get your patterns automatically. |
| Local vs global? | Local (`.opencode/`) = project-specific, committed to git, team-shared. Global (`~/.config/opencode/`) = personal defaults across all projects. Local overrides global. |
| Installed globally but want project patterns? | Run `/add-context` (defaults to local). Creates `.opencode/context/project-intelligence/` in your project even if OAC was installed globally. |
| Have external context files in .tmp/? | Run `/context harvest` to extract and organize them into permanent context |
| Want to clean up .tmp/ files? | Run `/context harvest` to extract knowledge and clean up temporary files |
| Move .tmp/ files to permanent context? | Run `/context harvest` to extract and organize them |
| Update external context files? | Edit directly: `nano .tmp/external-context.md` then run `/context harvest` |
| Remove specific external file? | Delete directly: `rm .tmp/external-context.md` then run `/context harvest` |
