# Phase 4: Spec template judges a diff against a spec standalone

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

Deliver `references/spec-prompt.md` — the verbatim Spec sub-agent template — and prove it with the same standalone
harness as phase 3, run twice to cover both spec-handover modes (decision 14): the spec as a repo path with a
read-first instruction, and the spec as pasted content. Spec is independent of Standards (phase 5); both need only
the return contract from phase 3.

## Context

- **The Spec axis judges one thing**: does the change do what the spec asks? Its brief (from
  `.planning/review/two-axes-review.md:72`, the surviving wording): report (a) requirements the spec asked for
  that are missing or partial; (b) behaviour in the diff that wasn't asked for — scope creep; (c) requirements
  that look implemented but where the implementation looks wrong. Every finding's cite quotes the spec line it is
  judged against (decision 11; Contract B's per-axis cite content).
- **Placeholder set** (Contract D): `{DIFF_CMD}`, `{COMMIT_LIST}`, `{RETURN_CONTRACT}` (pasted contents of
  `references/return-contract.md`, at the end), plus `{SPEC_SOURCE}` — filled either
  `Read this spec file first: <path>` (repo-file spec; may list more than one path for a `plan/` spec) or the
  pasted tracker content (decision 14). Nothing else is fillable.
- **No skip instruction in this template**: a Spec review with no discovered source is never spawned — the
  orchestrator marks the axis `skipped` itself (Contract C). The template therefore never mentions skipping, and
  the pasted return contract's `SKIPPED` sentinel stays inert ("only if the instructions above authorise
  skipping").
- **Read scope** (decision 13): Spec works from the diff plus its supplied spec — no exploratory reading beyond
  them.
- **Label rule and sentinels** arrive via `{RETURN_CONTRACT}` — the template states neither; it states only the
  axis's cite content (decision 15: the contract is stated once, pasted everywhere).
- **No word caps** (decision 11). No PRD references anywhere (decision 7). No first person anywhere.
- **The harness** (same as phase 3): the filled template is the entire prompt for one `general-purpose` agent
  spawned via the Agent tool; returns are judged against Contract C in the index (amended 2026-07-10: tiered
  axis-aware validation — hard checks are the usability floor and illegal skip; Spec paths absent from diff and
  repo are advisory, legitimate for missing-requirement findings; failures get a repair-rerun feeding back the
  previous return plus the defect list; format noise is advisory only). If the phase subagent has no Agent tool,
  these runs fall to the `/implement` orchestrator's own verification pass.
- **Real spec fixtures exist in this repo**: `.planning/three-axis-review/structure.md` (the approved slicing this
  very build implements) and `.planning/three-axis-review/task.md`. By this phase the branch's diff against `main`
  contains phases 1–3 — a genuinely reviewable diff against those specs.

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The Spec template

**File**: `skills/three-axis-review/references/spec-prompt.md`
**Change**: create the verbatim Spec sub-agent template. Placeholders in `{CAPS}` are the only fillable parts.

````markdown
# Spec sub-agent prompt

Fill `{DIFF_CMD}`, `{COMMIT_LIST}`, `{SPEC_SOURCE}`, and `{RETURN_CONTRACT}`; change nothing else. `{SPEC_SOURCE}`
is either `Read this spec file first: <path>` (repo-file spec — one path per line if several) or the spec content
pasted in full (tracker-fetched spec).

```
You are the Spec reviewer in a three-axis code review. Judge one thing: does the change do what the spec asks?
Code structure and documented-repo-rule compliance belong to other reviewers — do not report on them.

The spec:
{SPEC_SOURCE}

Run exactly this command and read the whole diff: {DIFF_CMD}
The commits under review:
{COMMIT_LIST}

Work from the diff and the spec only. Report three kinds of finding:

- a requirement the spec asks for that is missing or only partially implemented
- behaviour the diff adds that the spec does not ask for (scope creep)
- a requirement that looks implemented, where the implementation looks wrong

cite line for this axis: quote the exact spec line the finding is judged against.

{RETURN_CONTRACT}
```
````

## Success criteria

### Automated verification

- [x] Placeholder set is exact:
      `grep -oE '\{[A-Z_]+\}' skills/three-axis-review/references/spec-prompt.md | sort -u` prints exactly
      `{COMMIT_LIST}`, `{DIFF_CMD}`, `{RETURN_CONTRACT}`, `{SPEC_SOURCE}`.
- [x] No skip wording of its own: `grep -i 'skip' skills/three-axis-review/references/spec-prompt.md` finds
      nothing (the only skip wording a filled prompt carries comes from the pasted return contract).
- [x] No first person and no dead concepts:
      `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/references/spec-prompt.md` and
      `grep -inE 'PRD|word cap|issue-tracker\.md' skills/three-axis-review/references/spec-prompt.md` find
      nothing.
- [x] **Harness run A — spec as path**: fill with `{DIFF_CMD}` = `git diff main...HEAD` (this repo),
      `{COMMIT_LIST}` from the same range, `{SPEC_SOURCE}` =
      `Read this spec file first: <absolute path>/.planning/three-axis-review/structure.md`,
      `{RETURN_CONTRACT}` = pasted contract. Spawn one `general-purpose` agent with the filled prompt. Accept iff
      the return passes Contract C and every finding's cite quotes a line from `structure.md` — or the return is
      exactly `NO FINDINGS: <one line>`.
- [x] **Harness run B — spec as pasted content**: same fill except `{SPEC_SOURCE}` = the full contents of
      `.planning/three-axis-review/task.md` pasted inline (standing in for tracker-fetched content). Accept under
      the same Contract C test, cites quoting the pasted spec.

### Manual verification

None

## Dependencies

- **Depends on**: 3 (return contract)
- **Blocks**: 6
