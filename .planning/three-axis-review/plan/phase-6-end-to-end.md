# Phase 6: `/three-axis-review` runs end-to-end

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

Deliver `skills/three-axis-review/SKILL.md` — the orchestrator protocol, five numbered steps — plus the README
pipeline entry. This lands last so the skill only ever references artifacts that already exist and passed their
checks: the gate script (phase 1), the baseline (phase 2), the return contract and three prompt templates
(phases 3–5). Slices 3–5 already proved the templates and contract standalone, so this phase's dry-run tests
orchestration wiring only.

## Context

- **Frontmatter** (decision 12): `name: three-axis-review`; `disable-model-invocation: true`; description states
  the three axes and trigger phrases ("review a branch", "review since <ref>", "three-axis review") — no collision
  with built-in `/code-review` or `/review`.
- **Skill-relative paths**: at invocation the harness supplies "Base directory for this skill: <path>". SKILL.md
  references its own files relative to that base — `scripts/file_size_gate.py`,
  `references/{return-contract,structure-prompt,spec-prompt,standards-prompt,structure-baseline}.md` — and derives
  the absolute `{BASELINE_PATH}` from it.
- **The orchestrator protocol** — five numbered steps (decision 1):
  1. **Pin and gate.** The fixed point comes from the user; if absent, ask. Verify `git rev-parse <fixed-point>`
     and a non-empty `git diff <fixed-point>...HEAD` — fail here, not inside three sub-agents. Capture the diff
     command string and `git log <fixed-point>..HEAD --oneline`. Run
     `python3 <skill-dir>/scripts/file_size_gate.py <fixed-point>` (Contract A) — its TSV pre-seeds Structure
     findings labelled `blocker (presumptive)` (decision 6). Detect lint/format config filenames at the repo root
     (e.g. `.editorconfig`, `.eslintrc*`, `.prettierrc*`, `ruff.toml`, ktlint/detekt configs) for
     `{LINT_CONFIG_FILENAMES}`, `none detected` when empty (decision 8).
  2. **Find the spec** (decision 7): ① user-passed path — the only no-confirmation route; ② `.planning/<slug>/`
     matching the branch/feature, preference `plan/index.md` + phase files → `structure.md` → `design.md`, best
     match confirmed with the user; ③ ticket keys in commit messages → forge CLI inferred from session context
     (CLAUDE.md / AGENTS.md instructions, loaded skills) — definitive proof → use it, else ask; inferred matches
     confirmed; ④ ask the user. Nothing → the Spec axis is marked `skipped` and its sub-agent is never spawned
     (Contract C). Handover (decision 14): tracker-fetched content is pasted into `{SPEC_SOURCE}`; repo-file specs
     pass as `Read this spec file first: <path>`. A missing forge CLI is never installed — ask the user instead.
  3. **Fan out.** Read the three prompt files under `references/`; fill exactly each template's placeholder set
     (Contract D) and change nothing else (decision 10); `{RETURN_CONTRACT}` is the pasted contents of
     `references/return-contract.md` (decision 15). Spawn all sub-agents in one message, `general-purpose` type
     (decision 1) — three Agent calls, or two when Spec is skipped.
  4. **Verify returns** (Contract C, amended 2026-07-10 — the index carries the full amended text; SKILL.md
     encodes that version). Hard checks per axis: usability floor (non-empty; a sentinel or ≥1 legally-labelled
     bullet); paths-in-diff for Structure and Standards; pre-seed preservation for Structure; illegal `SKIPPED:`
     from Spec or Structure. A hard failure → repair-rerun: original filled prompt + previous return verbatim +
     the defect list + "Repair the listed defects. Keep every finding whose substance is sound. Do not re-review
     from scratch." (floor failures rerun the original prompt — nothing to repair) → second failure → the axis
     renders `not reviewed`. Advisory only, pasted through with a one-line orchestrator note, never a rerun: Spec
     paths absent from diff and repo, unknown labels, format noise. `skipped` (no source) and `not reviewed`
     (failed twice) are distinct states and both appear in the report; sub-agents never emit `not reviewed`. Gate
     fallback: if Structure ends `not reviewed`, render the pre-seeded TSV crossings as Contract B findings under
     `## Structure` directly — script findings cannot be lost to a dead axis.
  5. **Aggregate** (decision 3, Contract E): the report is the orchestrator's final message; no file is written.
     Under each of `## Spec`, `## Standards`, `## Structure`: the axis's findings verbatim (already blockers-first
     per the return contract), or its sentinel/state — labels never re-derived, findings never merged or reranked
     across axes. Each axis closes with a composed one-line summary: finding count (= bullet count) and the top
     blocker, if any.
- **A "Why three axes" closing section**, three sentences: a change can pass one axis and fail another; reporting
  them separately stops one axis from masking another; that separation is why findings are never reranked across
  axes.
- **Style constraints**: each rule stated exactly once; no first person anywhere; instructions only, no
  provenance; target ≤ 120 lines of SKILL.md (templates and contract are external files). Dead concepts must not
  appear: PRD, word caps, `issue-tracker.md`, `setup-matt-pocock`.
- **README entry** (decision 12, user decision 2026-07-10): a `####` entry physically between `#### /implement`
  and `#### /open-pr` in the Workflow pipeline section of `README.md`, explicitly marked an optional quality gate
  rather than a seventh phase, noting the Spec axis consumes `.planning/<feature>/` artifacts
  (`plan/` → `structure.md` → `design.md`). Match the surrounding entries' format and length; touch nothing else
  in the file — in particular, "A typical run" stays as-is.
- **Validator**: `python3 skills/skill-creator/scripts/quick_validate.py skills/three-axis-review`.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The skill file

**File**: `skills/three-axis-review/SKILL.md`
**Change**: create the orchestrator skill implementing the protocol above.

```markdown
---
name: three-axis-review
description: Review the diff since a fixed point along three orthogonal axes — Spec (does it
  do the right thing), Standards (does it follow documented repo rules), Structure (is it
  well built) — as parallel sub-agents reporting labelled findings, never a verdict. Use when
  the user wants to review a branch, review since <ref>, or asks for a three-axis review.
disable-model-invocation: true
---

# Three-Axis Review

Intro: the three axes in one line each; parallel sub-agents; findings labelled
`blocker (presumptive)` or `suggestion`, blockers first within an axis, never
reranked across axes.

## 1. Pin and gate       ← rev-parse + non-empty-diff gate, diff cmd + commit list captured,
                            file_size_gate.py run (TSV → pre-seeds), lint-config detection
## 2. Find the spec      ← the four-route chain with confirmation rules; nothing → Spec
                            `skipped`, never spawned; path vs pasted handover
## 3. Fan out            ← read references/<axis>-prompt.md per axis, fill exactly its
                            placeholder set, paste return-contract.md into {RETURN_CONTRACT};
                            one message, all Agent calls, general-purpose
## 4. Verify returns     ← Contract C (amended) tiered checks; repair-rerun once; skipped vs
                            not reviewed; gate fallback for Structure
## 5. Aggregate          ← final message; three headings, findings verbatim, per-axis
                            one-line summary

## Why three axes        ← the masking rationale, three sentences
```

### 2. README pipeline entry

**File**: `README.md`
**Change**: insert one entry between the `#### /implement` and `#### /open-pr` entries (currently ending at
`README.md:86` and starting at `README.md:88` respectively). Match the surrounding entries' voice and length;
change nothing else in the file.

```markdown
#### `/three-axis-review` (optional)

An optional quality gate between `/implement` and `/open-pr` — not a pipeline phase; nothing invokes it but you.
Reviews the diff since a fixed point along three orthogonal axes, each a parallel sub-agent: **Spec** (does it do
the right thing — consuming the `.planning/<feature>/` artifacts: `plan/` → `structure.md` → `design.md`),
**Standards** (documented repo rules only), and **Structure** (a merged smell baseline plus a deterministic
1k-line file gate). Reports labelled findings per axis — blockers first, never reranked across axes — and no
overall verdict.
```

## Success criteria

### Automated verification

- [ ] Skill validates: `python3 skills/skill-creator/scripts/quick_validate.py skills/three-axis-review`
- [ ] Frontmatter flag present: `grep -q 'disable-model-invocation: true' skills/three-axis-review/SKILL.md`
- [ ] Every artifact the skill references exists:
      `for f in scripts/file_size_gate.py references/return-contract.md references/structure-baseline.md references/structure-prompt.md references/spec-prompt.md references/standards-prompt.md; do test -f "skills/three-axis-review/$f" || echo "MISSING: $f"; done`
      prints nothing.
- [ ] SKILL.md names every file it orchestrates (including the baseline, whose absolute path it derives for
      `{BASELINE_PATH}`):
      `for f in file_size_gate.py return-contract.md structure-baseline.md structure-prompt.md spec-prompt.md standards-prompt.md; do grep -q "$f" skills/three-axis-review/SKILL.md || echo "UNREFERENCED: $f"; done`
      prints nothing.
- [ ] No first person: `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/SKILL.md` finds nothing.
- [ ] No dead concepts:
      `grep -inE 'PRD|word cap|issue-tracker\.md|setup-matt-pocock' skills/three-axis-review/SKILL.md` finds
      nothing.
- [ ] Size: `wc -l < skills/three-axis-review/SKILL.md` ≤ 120.
- [ ] README entry sits between `/implement` and `/open-pr`:
      `awk '/^#### .\/implement/,/^#### .\/open-pr/' README.md | grep -c 'three-axis-review'` prints ≥ 1, and
      `grep -c 'three-axis-review' README.md` prints exactly the number of mentions the new entry introduces (no
      strays elsewhere).

### Manual verification

- [ ] The user deep-reads SKILL.md against the index's durable decisions — in particular the five steps, the
      per-template placeholder fill duties (Contract D), the verify step (Contract C, including the gate
      fallback), and the aggregation rules (Contract E).
- [ ] Wiring-only dry-run on a small real branch: invoke `/three-axis-review` and observe — a bad ref or empty
      diff fails at step 1 before any fan-out; the spec chain asks/confirms exactly as specified; the sub-agents
      launch in one message; the report has three sections, blockers first within each, correct
      `skipped`/`not reviewed` states if any axis couldn't run, and a one-line summary per axis.

A phase with manual steps is a pause point: the orchestrator must wait for the user to confirm them before starting
the next phase.

## Dependencies

- **Depends on**: 1, 2, 3, 4, 5
- **Blocks**: None
