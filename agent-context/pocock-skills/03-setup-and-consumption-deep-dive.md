# Deep Dive: Setup and Consumption in Pocock Skills

This document traces, in exhaustive detail, how the `/setup-matt-pocock-skills` skill bootstraps per-repo configuration, and how every other engineering skill consumes that configuration — specifically `CONTEXT.md`, ADRs, the issue tracker, and triage labels.

---

## Table of Contents

1. [The Bootstrap Problem](#1-the-bootstrap-problem)
2. [Exact Step-by-Step Flow of `/setup-matt-pocock-skills`](#2-exact-step-by-step-flow-of-setup-matt-pocock-skills)
3. [The `domain.md` Template — Full Verbatim Content](#3-the-domainmd-template--full-verbatim-content)
4. [The Issue Tracker Templates](#4-the-issue-tracker-templates)
5. [The `triage-labels.md` Template — Full Verbatim Content](#5-the-triage-labelsmd-template--full-verbatim-content)
6. [The `## Agent skills` Block — The Entry Point](#6-the-agent-skills-block--the-entry-point)
7. [How Each Consuming Skill References and Uses Context](#7-how-each-consuming-skill-references-and-uses-context)
8. [Hard vs. Soft Dependencies](#8-hard-vs-soft-dependencies)
9. [Bootstrapping from Nothing — End-to-End Sequence](#9-bootstrapping-from-nothing--end-to-end-sequence)
10. [What Happens When Context Files Are Missing vs. Present](#10-what-happens-when-context-files-are-missing-vs-present)
11. [The Producer Side: `/grill-with-docs`](#11-the-producer-side-grill-with-docs)

---

## 1. The Bootstrap Problem

The Pocock Skills system has a chicken-and-egg problem: the engineering skills (`tdd`, `diagnose`, `triage`, `to-prd`, `to-issues`, `improve-codebase-architecture`, `zoom-out`) need per-repo configuration to function properly. That configuration includes:

- **Issue tracker** — where issues live and how to interact with them (GitHub, GitLab, local markdown, or custom)
- **Triage label vocabulary** — mapping canonical role names (`needs-triage`, `needs-info`, etc.) to actual label strings in the issue tracker
- **Domain docs** — whether the repo has a single `CONTEXT.md` at the root, or a `CONTEXT-MAP.md` pointing to multiple per-context `CONTEXT.md` files, plus the location of ADR directories

None of this exists in a fresh repo. The `/setup-matt-pocock-skills` skill exists to solve exactly this problem: it is a **prompt-driven, interactive skill** that explores the repo, asks the user three questions, and then writes the configuration files that the other skills will consume.

---

## 2. Exact Step-by-Step Flow of `/setup-matt-pocock-skills`

The setup skill is described in `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/SKILL.md`. Its frontmatter declares `disable-model-invocation: true`, meaning it is triggered by the user explicitly running `/setup-matt-pocock-skills` — it is not auto-invoked by other skills.

The skill description in the frontmatter states:

> Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitHub or local markdown), triage label vocabulary, and domain doc layout. Run before first use of `to-issues`, `to-prd`, `triage`, `diagnose`, `tdd`, `improve-codebase-architecture`, or `zoom-out` — or if those skills appear to be missing context about the issue tracker, triage labels, or domain docs.

### Step 1: Explore

The skill first **reads the current repo state**. It looks at:

- `git remote -v` and `.git/config` — to determine if this is a GitHub repo, GitLab repo, or neither. This informs the default posture for the issue tracker question.
- `AGENTS.md` and `CLAUDE.md` at the repo root — to check if either exists and whether either already contains an `## Agent skills` section.
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root — to detect if domain documentation already exists.
- `docs/adr/` and any `src/*/docs/adr/` directories — to check for existing ADR structure.
- `docs/agents/` — to check if this skill has been run before (its prior output would be here).
- `.scratch/` — to detect if a local-markdown issue tracker convention is already in use.

The explicit instruction is: "Read whatever exists; don't assume."

### Step 2: Present Findings and Ask (Three Questions, One at a Time)

The skill **summarises what's present and what's missing**, then walks the user through three decisions **one at a time**. The instruction is explicit: "Don't dump all three at once."

Each section starts with an **explainer** — a short paragraph that explains what the concept is, why the skills need it, and what changes depending on the choice. The user is assumed to not know the terminology.

#### Section A — Issue Tracker

Explainer verbatim from SKILL.md:

> The "issue tracker" is where issues live for this repo. Skills like `to-issues`, `triage`, `to-prd`, and `qa` read from and write to it — they need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

The default posture is inferred from `git remote`:
- If the remote points at GitHub, propose GitHub.
- If the remote points at GitLab (`gitlab.com` or self-hosted), propose GitLab.
- Otherwise, offer all options.

The four choices are:
1. **GitHub** — issues live in the repo's GitHub Issues (uses `gh` CLI)
2. **GitLab** — issues live in the repo's GitLab Issues (uses `glab` CLI)
3. **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
4. **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; record it as freeform prose

#### Section B — Triage Label Vocabulary

Explainer verbatim from SKILL.md:

> When the `triage` skill processes an incoming issue, it moves it through a state machine — needs evaluation, waiting on reporter, ready for an AFK agent to pick up, ready for a human, or won't fix. To do that, it needs to apply labels (or the equivalent in your issue tracker) that match strings *you've actually configured*. If your repo already uses different label names (e.g. `bug:triage` instead of `needs-triage`), map them here so the skill applies the right ones instead of creating duplicates.

The five canonical roles and their defaults:
- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, AFK-ready
- `ready-for-human` — needs human implementation
- `wontfix` — will not be actioned

Default: each role's string equals its name. The user is asked if they want to override any.

#### Section C — Domain Docs

Explainer verbatim from SKILL.md:

> Some skills (`improve-codebase-architecture`, `diagnose`, `tdd`) read a `CONTEXT.md` file to learn the project's domain language, and `docs/adr/` for past architectural decisions. They need to know whether the repo has one global context or multiple (e.g. a monorepo with separate frontend/backend contexts) so they look in the right place.

Two choices:
1. **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
2. **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

### Step 3: Confirm and Edit

The skill shows the user a **draft** of:
- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, and `docs/agents/domain.md`

The user can edit before writing.

### Step 4: Write

#### Choosing the target file

The selection rules are strict:
1. If `CLAUDE.md` exists, edit it.
2. Else if `AGENTS.md` exists, edit it.
3. If neither exists, **ask the user which one to create** — don't pick for them.

The constraint is: "Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there."

If an `## Agent skills` block already exists in the chosen file, it is **updated in-place** rather than appending a duplicate. Surrounding sections are not overwritten.

#### The `## Agent skills` block format

The block written to CLAUDE.md or AGENTS.md follows this exact template:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

#### The three docs files

The skill writes three files under `docs/agents/` using seed templates from its own skill folder as starting points:

- `docs/agents/issue-tracker.md` — written from `issue-tracker-github.md`, `issue-tracker-gitlab.md`, or `issue-tracker-local.md` (or from scratch for "other")
- `docs/agents/triage-labels.md` — written from `triage-labels.md`
- `docs/agents/domain.md` — written from `domain.md`

For "other" issue trackers, the skill writes `docs/agents/issue-tracker.md` from scratch using the user's one-paragraph description.

### Step 5: Done

The skill tells the user:
- Setup is complete
- Which engineering skills will now read from these files
- They can edit `docs/agents/*.md` directly later
- Re-running this skill is only necessary if they want to switch issue trackers or restart from scratch

---

## 3. The `domain.md` Template — Full Verbatim Content

Source: `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/domain.md`

```markdown
# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
```

### Key behaviors encoded in domain.md

1. **Silent degradation**: "If any of these files don't exist, **proceed silently**." This is the core graceful-degradation mechanism.
2. **Lazy creation**: The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved.
3. **Vocabulary enforcement**: Consumer skills must use the glossary's defined terms and avoid synonyms that the glossary explicitly marks as "Avoid."
4. **ADR conflict flagging**: If a skill's output contradicts an existing ADR, it must surface the conflict explicitly rather than silently overriding.
5. **Multi-context awareness**: If `CONTEXT-MAP.md` exists, skills must read the relevant per-context `CONTEXT.md` files and check context-scoped ADR directories.

---

## 4. The Issue Tracker Templates

### GitHub Template — Full Verbatim Content

Source: `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md`

```markdown
# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.
```

### GitLab Template — Full Verbatim Content

Source: `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md`

```markdown
# Issue tracker: GitLab

Issues and PRDs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions. Pass `--description -` to open an editor.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list --state opened -F json` with appropriate `--label` filters. Note that GitLab uses `opened` (not `open`) for the state value.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment, so post the explanation first with `glab issue note <number> --message "..."`, then close.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`, `glab mr view`, `glab mr note`, etc. — the same shape as `gh pr ...` with `mr` in place of `pr` and `note`/`--message` in place of `comment`/`--body`.

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitLab issue.

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.
```

### Local Markdown Template — Full Verbatim Content

Source: `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md`

```markdown
# Issue tracker: Local Markdown

Issues and PRDs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The PRD is `.scratch/<feature-slug>/PRD.md`
- Implementation issues are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.
```

### Design pattern across issue tracker templates

All three templates share the same structural pattern:
1. A header declaring the tracker type
2. A one-liner summary of where issues live
3. A `## Conventions` section with specific CLI commands for each operation
4. Two standardized directives: `"publish to the issue tracker"` and `"fetch the relevant ticket"`

These last two directives are the **integration contract**. Other skills use the phrases "publish to the issue tracker" and "fetch the relevant ticket" as abstract operations. The `docs/agents/issue-tracker.md` file translates those abstract operations into concrete CLI commands. This is an instance of the **adapter pattern**: the consuming skill is the caller, the issue tracker template is the adapter, and the CLI tool (`gh`, `glab`, or filesystem conventions) is the concrete implementation.

---

## 5. The `triage-labels.md` Template — Full Verbatim Content

Source: `/home/codey/Dev/pocock-skills/skills/engineering/setup-matt-pocock-skills/triage-labels.md`

```markdown
# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.
```

The right-hand column defaults to the canonical names. The user overrides them during setup if their issue tracker already uses different label strings. The instruction "Edit the right-hand column to match whatever vocabulary you actually use" is left in the file so future human edits are also supported.

---

## 6. The `## Agent skills` Block — The Entry Point

### How it works

The `## Agent skills` block is written into whichever file the agent reads for instructions — `CLAUDE.md` (preferred) or `AGENTS.md`. This file is the **entry point** for every new agent session. Every time an agent starts, it reads `CLAUDE.md` (or `AGENTS.md`) at the repo root.

The block contains three subsections, each with a one-line summary and a pointer to the detailed configuration file:

```markdown
## Agent skills

### Issue tracker

[one-line summary]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary]. See `docs/agents/domain.md`.
```

### Why this pattern works

The `## Agent skills` block is deliberately **terse**. It contains only one-line summaries and file paths. The reasoning is:

1. **Token efficiency**: The top-level instruction file (`CLAUDE.md` or `AGENTS.md`) is loaded on every agent invocation. Keeping it short saves tokens.
2. **Progressive disclosure**: The agent reads the one-liner and, if it needs details, follows the `See docs/agents/...` pointer. This means the agent only loads the full issue tracker CLI commands when it actually needs to create or read an issue.
3. **Single source of truth**: All three config files live under `docs/agents/`. The user can edit them directly without re-running setup, and they're version-controlled alongside the code.

### The CLAUDE.md of the pocock-skills repo itself

The pocock-skills repo's own `CLAUDE.md` does **not** contain an `## Agent skills` block. It contains only repo-organization instructions:

```markdown
Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used
- `personal/` — tied to my own setup, not promoted
- `deprecated/` — no longer used

Every skill in `engineering/`, `productivity/`, or `misc/` must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`. Skills in `personal/` and `deprecated/` must not appear in either.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.
```

This is because the pocock-skills repo **is the source of the skills themselves**, not a target repo that consumes them. The `docs/agents/` directory does not exist in this repo, confirming that setup has not been run here — and doesn't need to be, since this repo produces skills, it doesn't consume them in the same way.

---

## 7. How Each Consuming Skill References and Uses Context

### 7a. `/tdd` (Soft Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/tdd/SKILL.md`

**Relevant section** (line 47, under "1. Planning"):

> When exploring the codebase, use the project's domain glossary so that test names and interface vocabulary match the project's language, and respect ADRs in the area you're touching.

This is a **soft reference** — no explicit pointer to `docs/agents/domain.md` or `/setup-matt-pocock-skills`. It says "use the project's domain glossary" and "respect ADRs" without specifying where to find them. If the files don't exist, the skill proceeds without complaint.

The `tdd` skill also references three local supporting files:
- `[tests.md](tests.md)` — examples of good and bad tests
- `[mocking.md](mocking.md)` — mocking guidelines
- `[deep-modules.md](deep-modules.md)` — deep module concepts
- `[interface-design.md](interface-design.md)` — testability interface design
- `[refactoring.md](refactoring.md)` — refactoring candidates

None of these are context-related; they are skill-internal reference materials.

### 7b. `/diagnose` (Soft Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/diagnose/SKILL.md`

**Relevant section** (line 10):

> When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

Another **soft reference** — the same phrasing as `tdd`. The skill assumes the agent knows where to find the domain glossary and ADRs (via `docs/agents/domain.md` if setup has been run, or by searching the repo if not).

The `diagnose` skill does **not** contain a fallback instruction for when context files are missing. It simply says "use the glossary" and "check ADRs" — if they're absent, the agent operates without them.

### 7c. `/to-prd` (Hard Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/to-prd/SKILL.md`

**Relevant section** (lines 8-9):

> The issue tracker and triage label vocabulary should have been provided to you — run `/setup-matt-pocock-skills` if not.

Then in the Process section (line 12):

> Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

And in the publishing step (line 20):

> Write the PRD using the template below, then publish it to the project issue tracker. Apply the `needs-triage` triage label so it enters the normal triage flow.

This is a **hard dependency** with an explicit fallback. The skill:
1. **Asserts** that the issue tracker and triage labels should already be available
2. **Provides a recovery command**: `run /setup-matt-pocock-skills if not`
3. **Uses abstract operation names** ("publish it to the project issue tracker", "Apply the `needs-triage` triage label") that map to concrete operations defined in `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`

### 7d. `/triage` (Hard Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/triage/SKILL.md`

**Relevant section** (lines 35-37, under "Roles"):

> These are canonical role names — the actual label strings used in the issue tracker may differ. The mapping should have been provided to you - run `/setup-matt-pocock-skills` if not.

And in the Gather context step (line 63):

> Explore the codebase using the project's domain glossary, respecting ADRs in the area. Read `.out-of-scope/*.md` and surface any prior rejection that resembles this issue.

The triage skill is heavily dependent on **both** the issue tracker configuration and the triage labels configuration:
- It needs to query the issue tracker for unlabeled and labeled issues
- It needs to apply/remove specific label strings
- It needs to create comments on issues
- It needs to close issues

Without `docs/agents/issue-tracker.md`, it literally cannot function — it wouldn't know whether to use `gh`, `glab`, filesystem operations, or something else.

Without `docs/agents/triage-labels.md`, it would apply the canonical label names (`needs-triage`, `ready-for-agent`) which might not match what the user's issue tracker actually uses, creating duplicate labels or applying the wrong labels.

### 7e. `/to-issues` (Hard Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/to-issues/SKILL.md`

**Relevant section** (line 10):

> The issue tracker and triage label vocabulary should have been provided to you — run `/setup-matt-pocock-skills` if not.

This is the same hard-dependency pattern as `to-prd`. The skill also says (line 20):

> Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

And (line 54-55):

> For each approved slice, publish a new issue to the issue tracker. Use the issue body template below. Apply the `needs-triage` triage label so each issue enters the normal triage flow.

### 7f. `/improve-codebase-architecture` (Soft Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/improve-codebase-architecture/SKILL.md`

**Relevant section** (line 29):

> This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate.

And in the Process section (line 35):

> Read the project's domain glossary and any ADRs in the area you're touching first.

And when presenting candidates (line 56):

> **Use CONTEXT.md vocabulary for the domain, and [LANGUAGE.md](LANGUAGE.md) vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

And (line 58):

> **ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR.

This skill **also** has an active producer role with `CONTEXT.md`:

> **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md` — same discipline as `/grill-with-docs` (see CONTEXT-FORMAT.md). Create the file lazily if it doesn't exist.

> **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.

So `improve-codebase-architecture` both **consumes** domain context and **produces** it.

### 7g. `/zoom-out` (Soft Dependency)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/zoom-out/SKILL.md`

**Entire content** (this is a very short skill):

> I don't know this area of code well. Go up a layer of abstraction. Give me a map of all the relevant modules and callers, using the project's domain glossary vocabulary.

The only reference to context is "the project's domain glossary vocabulary" — no explicit pointer to `CONTEXT.md`, no reference to ADRs, no setup pointer. This is the softest possible dependency.

### 7h. `/grill-with-docs` (Both Consumer and Producer)

Source: `/home/codey/Dev/pocock-skills/skills/engineering/grill-with-docs/SKILL.md`

This skill is the **primary producer** of `CONTEXT.md` and ADRs. Its relevant sections:

**File structure** (lines 24-52) — it describes exactly where `CONTEXT.md` and ADRs live, and that they should be **created lazily**:

> Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

**During the session** — multiple active consumption and production actions:
- **Challenge against the glossary**: "When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately."
- **Sharpen fuzzy language**: "When the user uses vague or overloaded terms, propose a precise canonical term."
- **Update CONTEXT.md inline**: "When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen."
- **Offer ADRs sparingly**: Only when the decision is hard to reverse, surprising without context, and the result of a real trade-off.

### Summary table: Context references by skill

| Skill | Hard/Soft Dep | References CONTEXT.md? | References ADRs? | References issue tracker? | References triage labels? | Setup pointer? |
|---|---|---|---|---|---|---|
| `tdd` | Soft | Yes ("domain glossary") | Yes ("ADRs in the area") | No | No | No |
| `diagnose` | Soft | Yes ("domain glossary") | Yes ("ADRs in the area") | No | No | No |
| `to-prd` | **Hard** | Yes | Yes | Yes ("project issue tracker") | Yes ("needs-triage triage label") | **Yes** |
| `to-issues` | **Hard** | Yes | Yes | Yes ("issue tracker") | Yes ("needs-triage triage label") | **Yes** |
| `triage` | **Hard** | Yes | Yes | Yes (heavily) | Yes (heavily) | **Yes** |
| `improve-codebase-architecture` | Soft | Yes (explicitly `CONTEXT.md`) | Yes (explicitly `docs/adr/`) | No | No | No |
| `zoom-out` | Soft | Yes ("domain glossary vocabulary") | No | No | No | No |
| `grill-with-docs` | Soft (but is the **producer**) | Yes (reads + writes) | Yes (reads + writes) | No | No | No |

---

## 8. Hard vs. Soft Dependencies

### ADR-0001: The Formal Definition

The repo's single ADR (`docs/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`) formally defines the split:

```markdown
# Explicit `/setup-matt-pocock-skills` pointer only for hard dependencies

Engineering skills depend on per-repo config (issue tracker, triage label vocabulary, domain doc layout) seeded by `/setup-matt-pocock-skills`. Some skills cannot meaningfully function without that config — they have to publish to a specific issue tracker or apply a specific label string. Others only use it to sharpen output (vocabulary, ADR awareness) and degrade gracefully without it.

We split these into **hard-dependency** and **soft-dependency** skills:

- **Hard dependency** (`to-issues`, `to-prd`, `triage`) — include an explicit one-liner: _"… should have been provided to you — run `/setup-matt-pocock-skills` if not."_ Without the mapping, output is wrong, not just fuzzy.
- **Soft dependency** (`diagnose`, `tdd`, `improve-codebase-architecture`, `zoom-out`) — reference "the project's domain glossary" and "ADRs in the area you're touching" in vague prose only. If the docs aren't there, the skill still works; output is just less sharp.

The split keeps soft-dependency skills token-light and avoids cargo-culting the setup pointer into places where it isn't load-bearing.
```

### The Decision Criterion

The test is simple: **If the config is missing, is the output wrong, or just less sharp?**

- **Wrong output** = hard dependency. Example: `triage` trying to apply label strings that don't exist in the issue tracker; `to-prd` trying to create an issue with `gh issue create` on a repo that uses GitLab or local markdown.
- **Less sharp output** = soft dependency. Example: `diagnose` running without a domain glossary — it can still reproduce, hypothesize, instrument, and fix, but its output might use synonyms or miss important ADRs.

### The Asymmetry in Referencing Style

**Hard dependencies** use the explicit phrasing:
> The issue tracker and triage label vocabulary should have been provided to you — run `/setup-matt-pocock-skills` if not.

**Soft dependencies** use vague, context-agnostic phrasing:
> Use the project's domain glossary vocabulary
> Respect ADRs in the area you're touching

The hard-dependency phrasing is a **recovery mechanism**: if the config is missing, the agent is told exactly how to get it. The soft-dependency phrasing is a **graceful degradation**: the agent will look for `CONTEXT.md` if it exists, and proceed without it if it doesn't.

---

## 9. Bootstrapping from Nothing — End-to-End Sequence

Here is the complete bootstrap sequence for a brand-new repo that has never used Pocock Skills:

### Phase 0: Empty Repo

The repo has:
- No `CLAUDE.md` or `AGENTS.md`
- No `CONTEXT.md` or `CONTEXT-MAP.md`
- No `docs/adr/` directory
- No `docs/agents/` directory
- No `docs/agents/issue-tracker.md`
- No `docs/agents/triage-labels.md`
- No `docs/agents/domain.md`

### Phase 1: User runs `/setup-matt-pocock-skills`

The skill:
1. Runs `git remote -v` — detects, say, `origin https://github.com/user/repo.git`
2. Checks for `CLAUDE.md` — not found
3. Checks for `AGENTS.md` — not found
4. Asks the user: "Which file should I create — `CLAUDE.md` or `AGENTS.md`?"
5. Walks the user through Section A (issue tracker → user picks "GitHub"), Section B (triage labels → user keeps defaults), Section C (domain docs → user confirms "single-context")
6. Shows drafts of the three `docs/agents/` files and the `## Agent skills` block
7. User approves
8. Writes:
   - `CLAUDE.md` (or `AGENTS.md`) with the `## Agent skills` block
   - `docs/agents/issue-tracker.md` (from `issue-tracker-github.md` template)
   - `docs/agents/triage-labels.md` (from `triage-labels.md` template)
   - `docs/agents/domain.md` (from `domain.md` template)

### Phase 2: User runs a hard-dependency skill (e.g., `/to-prd`)

The agent:
1. Reads `CLAUDE.md` at session start
2. Sees `## Agent skills` → `### Issue tracker` → `See docs/agents/issue-tracker.md`
3. When the skill needs to publish a PRD, reads `docs/agents/issue-tracker.md` and learns to use `gh issue create`
4. Reads `docs/agents/triage-labels.md` and learns to apply `needs-triage` as the label
5. Reads `docs/agents/domain.md` → learns to read `CONTEXT.md` for domain vocabulary
6. Checks for `CONTEXT.md` — **doesn't exist yet** → per `domain.md`: "proceed silently"
7. Checks for `docs/adr/` — **doesn't exist yet** → per `domain.md`: "proceed silently"
8. Publishes the PRD using `gh issue create` with the `needs-triage` label

### Phase 3: User runs `/grill-with-docs` (or `/improve-codebase-architecture`)

Now the **producer** side kicks in:
1. The skill prompts the user to clarify domain terms
2. When a term is resolved, it **creates `CONTEXT.md`** lazily (per `grill-with-docs`: "If no `CONTEXT.md` exists, create one when the first term is resolved")
3. If an architectural decision meets all three ADR criteria (hard to reverse, surprising, real trade-off), it **creates `docs/adr/0001-*.md`**

### Phase 4: Later consumer skills now find context

The next time `/diagnose`, `/tdd`, `/to-prd`, etc. run:
1. They read `docs/agents/domain.md`
2. They find `CONTEXT.md` at the repo root → **use the glossary**
3. They find `docs/adr/` → **check ADRs in the area**
4. Output is sharper: domain terms match the glossary, ADR conflicts are flagged

---

## 10. What Happens When Context Files Are Missing vs. Present

### Missing `CONTEXT.md`

Per `domain.md`:
> If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront.

This means:
- **Soft-dependency skills** (`tdd`, `diagnose`, `zoom-out`): Proceed normally. They mention "use the project's domain glossary" but if there's no glossary, they simply don't use one. Output is less sharp but still functional.
- **Hard-dependency skills** (`to-prd`, `to-issues`, `triage`): Proceed with issue tracker and label operations. The domain glossary is not load-bearing for them.
- **Producer skills** (`grill-with-docs`, `improve-codebase-architecture`): Create `CONTEXT.md` lazily when the first term is resolved.

### Missing `CONTEXT-MAP.md`

If `CONTEXT-MAP.md` doesn't exist, the skill assumes single-context and reads only `CONTEXT.md` at the root. Per `domain.md`:
> - `CONTEXT-MAP.md` at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
> Confirm the layout:
> - **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
> - **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files.

### Missing `docs/adr/`

Same silent-degradation rule applies. Skills that reference ADRs will simply skip the ADR check. Per `domain.md`: "proceed silently."

### Missing `docs/agents/` files

This is the **hard failure** case. If `docs/agents/issue-tracker.md` is missing:
- `to-prd`, `to-issues`, and `triage` **cannot determine how to publish or read issues**
- The hard-dependency fallback kicks in: "run `/setup-matt-pocock-skills` if not"

If `docs/agents/triage-labels.md` is missing:
- `triage` and any skill that applies labels will use the canonical names by convention, but they may create duplicate labels or apply the wrong ones
- The hard-dependency fallback kicks in

If `docs/agents/domain.md` is missing:
- Skills won't know whether to look for `CONTEXT.md` at the root or follow `CONTEXT-MAP.md`
- They'll probably look for both and pick whichever exists
- This is the softest of the three — degradation is graceful

### All context files present

When all files exist, the system works as designed:
1. Agent reads `CLAUDE.md`/`AGENTS.md` → sees `## Agent skills` block
2. Follows pointers to `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`
3. `domain.md` tells the agent to read `CONTEXT.md` (or `CONTEXT-MAP.md` + per-context `CONTEXT.md` files) and `docs/adr/`
4. The agent uses the domain glossary, checks ADRs, applies correct label strings, and uses the correct CLI commands

### Partial `CONTEXT.md` (some terms defined, gaps exist)

Per `domain.md`:
> If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

This creates a **feedback loop**:
1. A consumer skill encounters a domain concept not in the glossary
2. It notes the gap
3. The user can then run `/grill-with-docs` to resolve the gap
4. The next consumer skill finds the term and uses it

---

## 11. The Producer Side: `/grill-with-docs`

While this document focuses on consumption, it's important to understand the production side that creates the context files the consumers depend on.

### `CONTEXT.md` Production

The `/grill-with-docs` skill is the primary producer. It uses the format defined in `CONTEXT-FORMAT.md`:

**Structure**: A `CONTEXT.md` contains:
- A title and description
- A `## Language` section with term definitions (canonical name, description, "Avoid:" list)
- A `## Relationships` section linking terms
- A `## Flagged ambiguities` section for resolved ambiguities
- Optional: `## Example dialogue` showing terms in use

**Key rules** from `CONTEXT-FORMAT.md`:
> - **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
> - **Flag conflicts explicitly.** If a term is used ambiguously, call it out in "Flagged ambiguities" with a clear resolution.
> - **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
> - **Show relationships.** Use bold term names and express cardinality where obvious.
> - **Only include terms specific to this project's context.** General programming concepts don't belong.
> - **Write an example dialogue.**

**Lazy creation**: `/grill-with-docs` creates `CONTEXT.md` only "when the first term is resolved" — not upfront, not speculatively.

### ADR Production

ADRs are offered **sparingly** — only when all three criteria are met:
1. Hard to reverse
2. Surprising without context
3. Result of a real trade-off

"If any of the three is missing, skip the ADR."

The ADR format is defined in `grill-with-docs/ADR-FORMAT.md` (not read for this document).

### Multi-context detection

The system infers single vs. multi-context:
- If `CONTEXT-MAP.md` exists at root → multi-context
- If only `CONTEXT.md` exists at root → single-context
- If neither exists → create a root `CONTEXT.md` lazily when first needed

### The feedback loop closes here

The `/improve-codebase-architecture` skill also produces context:
> **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md` — same discipline as `/grill-with-docs`.

This means the domain model can grow from two sources:
1. `/grill-with-docs` sessions — explicit term resolution
2. `/improve-codebase-architecture` sessions — terms discovered during architecture work

Both follow the same format (`CONTEXT-FORMAT.md`) and the same lazy-creation principle.

---

## Summary: The Complete Data Flow

```
                        ┌─────────────────────────────────┐
                        │   /setup-matt-pocock-skills      │
                        │                                  │
                        │  Writes:                         │
                        │  ├── CLAUDE.md/AGENTS.md         │
                        │  │   (## Agent skills block)      │
                        │  ├── docs/agents/                │
                        │  │   ├── issue-tracker.md         │
                        │  │   ├── triage-labels.md         │
                        │  │   └── domain.md               │
                        └──────────────┬──────────────────┘
                                       │
                                       │ creates
                                       ▼
    ┌──────────────────────────────────────────────────────────────┐
    │                  PER-REPO CONFIG FILES                       │
    │                                                              │
    │   CLAUDE.md / AGENTS.md                                      │
    │   ├── ## Agent skills                                        │
    │   │   ├── Issue tracker → See docs/agents/issue-tracker.md    │
    │   │   ├── Triage labels → See docs/agents/triage-labels.md    │
    │   │   └── Domain docs → See docs/agents/domain.md             │
    │   │                                                           │
    │   docs/agents/issue-tracker.md  ← CLI adapter for gh/glab/fs │
    │   docs/agents/triage-labels.md  ← label string mapping table  │
    │   docs/agents/domain.md         ← CONTEXT.md/ADR access rules│
    └──────────────────────────────────────────────────────────────┘
                                       │
           ┌───────────────────────────┼───────────────────────────┐
           │                           │                           │
           │  reads                    │  reads                    │  reads
           ▼                           ▼                           ▼
    ┌──────────────┐     ┌─────────────────────┐     ┌──────────────────────┐
    │ Hard deps    │     │ Soft deps            │     │ Producers            │
    │              │     │                      │     │                      │
    │ to-issues    │     │ diagnose             │     │ grill-with-docs      │
    │ to-prd       │     │ tdd                  │     │ improve-codebase-    │
    │ triage       │     │ improve-codebase-    │     │   architecture       │
    │              │     │   architecture       │     │                      │
    │ NEEDS:       │     │ zoom-out             │     │ WRITES:              │
    │ issue tracker│     │                      │     │ CONTEXT.md           │
    │ triage labels│     │ USES (optional):     │     │ docs/adr/           │
    │              │     │ CONTEXT.md           │     │                      │
    │ FALLBACK:    │     │ docs/adr/            │     │ FORMAT:              │
    │ "run         │     │                      │     │ CONTEXT-FORMAT.md    │
    │  /setup-matt-│     │ FALLBACK:            │     │ ADR-FORMAT.md        │
    │  pocock-     │     │ Proceed silently     │     │                      │
    │  skills      │     │                      │     │                      │
    │  if not"     │     │                      │     │                      │
    └──────────────┘     └─────────────────────┘     └──────────────────────┘
                                       │
                                       │ also reads
                                       ▼
                              ┌──────────────────┐
                              │ DOMAIN CONTEXT    │
                              │                  │
                              │ CONTEXT.md       │
                              │ CONTEXT-MAP.md   │
                              │ docs/adr/        │
                              └──────────────────┘
```

The architecture is a clean **producer-consumer** pattern with **adapter** indirection:

1. **Setup** creates the adapter layer (`docs/agents/`) that translates abstract operations ("publish to the issue tracker") into concrete commands (`gh issue create`, `glab issue create`, or filesystem writes)
2. **Consumers** read the adapter layer to know how to interact with the issue tracker and where to find domain context
3. **Producers** create domain context (`CONTEXT.md`, ADRs) lazily, following a defined format
4. **The `domain.md` file** is the crucial **bridge document** — it tells consumers both WHERE to find context AND how to BEHAVE when context is missing (proceed silently, don't suggest creating it)
5. **The `## Agent skills` block** is the **index** — a minimal pointer structure that keeps the top-level instruction file short while making the full config discoverable
6. **Hard dependencies** get an explicit recovery path (`/setup-matt-pocock-skills`); **soft dependencies** degrade gracefully by design
