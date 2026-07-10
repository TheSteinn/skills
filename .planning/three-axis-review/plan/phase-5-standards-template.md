# Phase 5: Standards template discovers rules and judges standalone

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

Deliver `references/standards-prompt.md` — the verbatim Standards sub-agent template, including its nested
haiku-explorer delegation — and prove it with the phase 3 harness on two targets: a real standards-bearing repo
(positive case: rule-cited findings) and a bare fixture repo (skip case: the exact `SKIPPED` sentinel). This
isolates the skill's riskiest novel mechanism — nested delegation — before any orchestrator exists. Independent of
phase 4; needs only the return contract from phase 3.

## Context

- **The Standards axis judges one thing**: does the change follow this repo's *documented* rules? No documented
  rule, no finding — the smell baseline lives on Structure, not here (decision 2). A documented-rule breach is an
  objective trigger, so it labels `blocker (presumptive)` under the pasted label rule.
- **Discovery is delegated** (decision 8): the Standards sub-agent spawns one exploration sub-agent via the Agent
  tool — `general-purpose` type, `model: haiku` — so the reviewer's own context stays clean. The explorer prompt is
  **static text inside the template** with no orchestrator-filled placeholders (Contract D). It covers the fixed,
  closed candidate set — project `CLAUDE.md` / `AGENTS.md` at the repo root; root-level CONTRIBUTING /
  CODING_STANDARDS / STYLE docs; the root `docs/` directory scanned for similarly named files (contributing,
  coding standards, style, code-style, conventions) — with an explicit stopping rule: no repo-wide crawl. The
  explorer returns found paths only; the Standards agent reads them itself.
- **Repo-root anchor** (planning refinement, noted for the user): the explorer needs to know which repository to
  scan, and in a harness the diff command may carry `git -C <path>`. The template therefore tells the Standards
  agent to substitute the repo root — the directory the diff command targets — for `<repo-root>` in the explorer
  prompt before spawning. This substitution is the Standards agent's own duty, not an orchestrator placeholder,
  so Contract D's "no placeholders" rule holds.
- **Nothing found → explicit skip** (decision 8, Contract B): the entire return is exactly
  `SKIPPED: no documented standards`. This template is the only one that authorises the pasted contract's
  `SKIPPED` sentinel.
- **Tooling filter, grounded** (decision 8): the orchestrator detects lint/format config filenames at the repo
  root and fills `{LINT_CONFIG_FILENAMES}` (or `none detected`). The sub-agent skips only findings those named
  tools would catch themselves; with `none detected`, nothing is skipped on tooling grounds.
- **Placeholder set** (Contract D): `{DIFF_CMD}`, `{COMMIT_LIST}`, `{RETURN_CONTRACT}` (pasted, at the end), plus
  `{LINT_CONFIG_FILENAMES}`. Nothing else is fillable.
- **Cite content for this axis** (Contract B): name the rule's file and quote the breaching hunk.
- **Read scope** (decision 13): the diff plus the discovered rule files — no exploratory reading beyond them.
- **The harness** (same as phase 3): the filled template is the entire prompt for one `general-purpose` agent
  spawned via the Agent tool; returns judged against Contract C in the index (amended 2026-07-10: tiered
  axis-aware validation — hard checks are the usability floor, paths-in-diff, and illegal skip; failures get a
  repair-rerun feeding back the previous return plus the defect list; format noise is advisory only). If the
  phase subagent has no Agent tool, these runs fall to the `/implement` orchestrator's own verification pass.
- **Harness targets** (user decision 2026-07-10): the positive case runs read-only against
  `/Users/codey.byrne/dev/kotlin.applications` — root `CLAUDE.md`, `AGENTS.md`, a root `docs/` directory, and
  `.editorconfig` (all verified present 2026-07-10). This repo itself has no standards docs at all, so it cannot
  host the positive case. If the nested Agent-tool delegation turns out to be unavailable to a sub-agent, that
  invalidates decision 8 — stop and report it as a mismatch, do not adapt around it.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The Standards template

**File**: `skills/three-axis-review/references/standards-prompt.md`
**Change**: create the verbatim Standards sub-agent template, nested explorer prompt included. Placeholders in
`{CAPS}` are the only orchestrator-fillable parts.

````markdown
# Standards sub-agent prompt

Fill `{DIFF_CMD}`, `{COMMIT_LIST}`, `{LINT_CONFIG_FILENAMES}`, and `{RETURN_CONTRACT}`; change nothing else. Fill
`{LINT_CONFIG_FILENAMES}` with `none detected` when no lint/format configs were found.

```
You are the Standards reviewer in a three-axis code review. Judge one thing: does the change follow this repo's
documented rules? General code quality and spec fidelity belong to other reviewers. No documented rule, no
finding.

First, discover the rule sources without spending your own context on the search. Determine the repo root — the
directory the diff command below targets — then spawn one exploration sub-agent with the Agent tool
(`general-purpose` type, model `haiku`), substituting the root for <repo-root> in exactly this prompt:

  In the repository at <repo-root>, report which of these files exist — paths only, no file contents, no
  commentary: CLAUDE.md and AGENTS.md at the repo root; any root-level file named like CONTRIBUTING,
  CODING_STANDARDS, or STYLE (any case, any extension); and, looking only inside the root docs/ directory, any
  file whose name resembles those (contributing, coding standards, style, code-style, conventions). Search
  nowhere else and stop after these checks. If none exist, reply with exactly: NONE

If the explorer reports NONE, skip this review: the entire return is exactly the SKIPPED sentinel below, with
reason `no documented standards`.

Otherwise read every reported file yourself, then run exactly this command and read the whole diff: {DIFF_CMD}
The commits under review:
{COMMIT_LIST}

Report every place the diff breaches a rule those documents state. A documented-rule breach is an objective
trigger. Tooling filter — lint/format configs detected at the repo root: {LINT_CONFIG_FILENAMES}. Skip only
findings those named tools would catch themselves; if the list is `none detected`, skip nothing on tooling
grounds.

cite line for this axis: name the rule's file and quote the breaching hunk.

{RETURN_CONTRACT}
```
````

## Success criteria

### Automated verification

- [ ] Placeholder set is exact:
      `grep -oE '\{[A-Z_]+\}' skills/three-axis-review/references/standards-prompt.md | sort -u` prints exactly
      `{COMMIT_LIST}`, `{DIFF_CMD}`, `{LINT_CONFIG_FILENAMES}`, `{RETURN_CONTRACT}`.
- [ ] The explorer prompt is static and closed: it names the full candidate set, contains no `{CAPS}`
      placeholders, and carries the stopping rule:
      `grep -q 'stop after these checks' skills/three-axis-review/references/standards-prompt.md`.
- [ ] The skip sentinel wiring is present: `grep -q 'no documented standards' skills/three-axis-review/references/standards-prompt.md`.
- [ ] No first person and no dead concepts:
      `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/references/standards-prompt.md` and
      `grep -inE 'PRD|word cap|issue-tracker\.md' skills/three-axis-review/references/standards-prompt.md` find
      nothing.
- [ ] **Harness run A — positive case, real repo (read-only)**: use the last two commits in
      `/Users/codey.byrne/dev/kotlin.applications` (user decision 2026-07-10: `HEAD~2...HEAD`, non-empty diff).
      Fill: `{DIFF_CMD}` = `git -C /Users/codey.byrne/dev/kotlin.applications diff HEAD~2...HEAD`,
      `{COMMIT_LIST}` = pasted `git -C ... log HEAD~2..HEAD --oneline`, `{LINT_CONFIG_FILENAMES}` = the config
      filenames actually present at that repo's root (at minimum `.editorconfig`), `{RETURN_CONTRACT}` = pasted
      contract. Spawn one `general-purpose` agent with the filled prompt. Accept iff: the agent delegated
      discovery to a haiku explorer (visible in its report or transcript); discovery found at least `CLAUDE.md`
      and `AGENTS.md`; and the return passes Contract C — findings whose cites name a rule file and quote a hunk,
      blockers first, or exactly `NO FINDINGS: <one line>`. The run must not write to that repo.
- [ ] **Harness run B — skip case, bare fixture**: scratch repo in `$TMPDIR` with no standards docs and a small
      two-commit diff; fill with `{LINT_CONFIG_FILENAMES}` = `none detected` and a `git -C <fixture> diff ...`
      command. Accept iff the entire return is exactly `SKIPPED: no documented standards`.

### Manual verification

None

## Dependencies

- **Depends on**: 3 (return contract)
- **Blocks**: 6
