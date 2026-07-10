# Design 3: Skill drafting

> Source: [index.md](index.md). Self-contained: refine from this file + the index only.

## Overview

Deliver `skills/three-axis-review/SKILL.md` — the orchestrator protocol and the three verbatim sub-agent templates —
plus the README pipeline mention. This lands last so the skill only ever references artifacts that already exist and
passed their checks: the gate script (phase 1) and the baseline (phase 2).

## Context

Everything the SKILL.md encodes is a durable decision; this section restates them as the document's required shape.

**Frontmatter** (durable decision 12): `name: three-axis-review`; `disable-model-invocation: true`; description states
the three axes and trigger phrases ("review a branch", "review since <ref>", "three-axis review") — no collision with
built-in `/code-review` or `/review`.

**Orchestrator protocol** — five numbered steps (durable decision 1), the two-axes macro shape
(`.planning/review/two-axes-review.md:17-80`) with the repaired wiring:

1. **Pin and gate.** The fixed point comes from the user; if absent, ask. Verify `git rev-parse <fixed-point>` and a
   non-empty `git diff <fixed-point>...HEAD` — fail here, not inside three sub-agents. Capture the diff command and
   `git log <fixed-point>..HEAD --oneline`. Run
   `python3 <skill-dir>/scripts/file_size_gate.py <fixed-point>` (contract: phase 1) — its TSV output pre-seeds
   Structure findings labelled `blocker (presumptive)` (durable decision 6). Detect lint/format config filenames at
   the repo root (e.g. `.eslintrc*`, `.prettierrc*`, `ruff.toml`, `.editorconfig`, `ktlint`/`detekt` configs) for the
   Standards template (durable decision 8).
2. **Find the spec** (durable decision 7): ① user-passed path — the only no-confirmation route; ② `.planning/<slug>/`
   matching the branch/feature, preference `plan/index.md` + phase files → `structure.md` → `design.md`, best match
   confirmed with the user; ③ ticket keys in commit messages → forge CLI inferred from session context (CLAUDE.md /
   AGENTS.md instructions, loaded skills) — definitive proof → use it, else ask; inferred matches confirmed; ④ ask.
   Nothing → the Spec axis is marked `skipped`. Handover rule (durable decision 14): tracker-fetched content is pasted
   into the prompt; repo-file specs pass as paths.
3. **Spawn all three sub-agents in one message** (durable decision 1), `general-purpose` type, prompts built from the
   three templates below — filling the placeholders and changing nothing else (durable decision 10).
4. **Verify returns** (durable decision 11): an axis that errors or returns empty → rerun once with the failure noted;
   a second failure → the axis reports `not reviewed`. `skipped` (no source) and `not reviewed` (failed) are distinct
   states and both appear in the report.
5. **Aggregate** (durable decision 3): three sections — `## Spec`, `## Standards`, `## Structure` — findings verbatim,
   blockers sorted before suggestions within each axis, labels never re-derived, findings never merged or reranked
   across axes (one axis must not mask another). Close with a one-line per-axis summary: finding count and the top
   blocker, if any.

**The three templates** — fenced, verbatim, placeholders in `{CAPS}`. Common to all three: the diff command and commit
list; the label rule stated inside the template ("label each finding `blocker (presumptive)` — objective trigger or
documented-rule breach — or `suggestion`; when unsure, `suggestion`"); mandatory citations; no word caps (durable
decisions 3, 10, 11).

- **Spec template**: `{SPEC_CONTENT_OR_PATH}`; brief per `two-axes-review.md:72` — missing/partial requirements, scope
  creep, implemented-but-wrong; quote the spec line for each finding.
- **Standards template**: instructs the sub-agent to first delegate source discovery to a haiku exploration sub-agent
  (Agent tool, `model: haiku`) over the fixed candidate set — project CLAUDE.md / AGENTS.md; root CONTRIBUTING /
  CODING_STANDARDS / STYLE; root `docs/` scan for similar names — explicit stopping rule, no crawl (durable decision
  8). `{LINT_CONFIG_FILENAMES}` grounds the tooling filter: skip only findings those named tools would catch. Nothing
  found → return `skipped: no documented standards`. Cite rule file + quote the hunk per finding.
- **Structure template**: read `{BASELINE_PATH}` (= `references/structure-baseline.md`) first (durable decision 9);
  invoke `codebase-designing` with the Skill tool — the explicit-invocation wording from `skills/design/SKILL.md:23`
  ("actually invoke … with the Skill tool; mentioning a skill in prose loads nothing") (durable decision 5).
  `{PRESEEDED_FINDINGS}` carries the gate-script TSV — contextualize only, never re-derive. Read scope: touched files
  and surroundings, findings still quote the anchoring hunk (durable decision 13). Judo posture (durable decision 4):
  look for reframings that delete complexity, reportable **only** with a concrete sketch (what disappears, what
  replaces it), a behaviour-preservation argument, and a complexity argument in `codebase-designing` terms — fewer
  held concepts, dependencies, or obscurity (`nuclear-review.md:94`'s criterion); always `suggestion`. Prefer few
  high-conviction findings over nit floods (`nuclear-review.md:166-167`).

**Style constraints**: each rule stated exactly once (no import of nuclear's sevenfold restatement or tone-phrase
library); no first person anywhere, templates included; instructions only, no provenance; target ≤ 120 lines of
SKILL.md prose excluding the three fenced templates.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The skill file

**File**: `skills/three-axis-review/SKILL.md`
**Change**: create the skill implementing the protocol and templates above.

```markdown
---
name: three-axis-review
description: Review the diff since a fixed point along three axes — Spec …,
  Standards …, Structure … . Use when the user wants to review a branch …
disable-model-invocation: true
---

Intro: the three axes in one line each; parallel sub-agents; findings labelled,
never reranked across axes.

## Process
### 1. Pin and gate        ← rev-parse + non-empty gate, diff cmd, commit list,
                              file_size_gate.py run, lint-config detection
### 2. Find the spec       ← the four-route chain, confirmation rules, skip state
### 3. Spawn the sub-agents ← one message, three Agent calls; templates below
### 4. Verify returns      ← rerun-once; skipped vs not-reviewed
### 5. Aggregate           ← three headings, blockers-first, per-axis summary

## Spec sub-agent prompt
```(fenced template, placeholders only)```
## Standards sub-agent prompt
```(fenced template, incl. haiku-explorer delegation)```
## Structure sub-agent prompt
```(fenced template, incl. baseline path read-first, codebase-designing
    Skill invocation, pre-seeded findings, judo gate)```

## Why three axes        ← the masking rationale, three sentences
```

### 2. README pipeline mention

**File**: `README.md`
**Change**: one short entry documenting `/three-axis-review` as an optional quality gate between `/implement` and
`/open-pr` (durable decision 12), noting its Spec axis consumes `.planning/<feature>/` artifacts (`plan/` →
`structure.md` → `design.md`). Match the surrounding entries' format and length; touch nothing else in the file.

## Success criteria

### Automated verification

- [ ] Skill validates: `python3 skills/skill-creator/scripts/quick_validate.py skills/three-axis-review`
- [ ] Frontmatter flag present: `grep -q 'disable-model-invocation: true' skills/three-axis-review/SKILL.md`
- [ ] Every path the skill references exists — at minimum:
      `test -f skills/three-axis-review/scripts/file_size_gate.py && test -f skills/three-axis-review/references/structure-baseline.md`
- [ ] Exactly three fenced sub-agent templates: `grep -c '^## .* sub-agent prompt' skills/three-axis-review/SKILL.md`
      prints 3.
- [ ] Explicit Skill invocation present: `grep -q 'Skill tool' skills/three-axis-review/SKILL.md`
- [ ] No first person: `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/SKILL.md` finds nothing.
- [ ] No dead concepts: `grep -inE 'PRD|word cap|issue-tracker\.md|setup-matt-pocock' skills/three-axis-review/SKILL.md`
      finds nothing.
- [ ] README mentions the skill once: `grep -c 'three-axis-review' README.md` ≥ 1.

### Manual verification

- [ ] The user deep-reads SKILL.md against the durable decisions (index) — in particular the five steps, the three
      templates' placeholder sets, and the judo gate wording.
- [ ] Dry-run: invoke `/three-axis-review` on a small real branch; observe the gate firing on a bad ref, the spec
      chain asking/confirming as specified, three parallel sub-agents, and a report with three sections,
      blocker-first ordering, and a per-axis summary line.

A phase with manual steps is a pause point: the orchestrator must wait for the user to confirm them before starting
the next phase.

## Dependencies

- **Depends on**: 1, 2
- **Blocks**: None
