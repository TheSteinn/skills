# Phase 3: Structure template reviews a real diff standalone

> Source: [index.md](index.md). Self-contained: implement from this file + the index only.

## Overview

Deliver the shared return contract (`references/return-contract.md`) and the Structure sub-agent template
(`references/structure-prompt.md`), then prove the template⇄contract pair with no orchestrator: hand-fill the
placeholders, spawn one `general-purpose` sub-agent on real diffs, and judge the returns against Contract C's
acceptance checklist. This phase carries the return contract because Structure is the axis that exercises every
part of it — findings, labels, pre-seeded blockers, and the clean sentinel.

## Context

- **Both files are verbatim payloads, not prose the orchestrator paraphrases** (decision 10). At review time the
  orchestrator reads `structure-prompt.md`, fills exactly its placeholder set, and changes nothing else. The
  placeholder set for this template (Contract D): `{DIFF_CMD}` — the literal `git diff <fixed-point>...HEAD`
  string, which the sub-agent runs itself; `{COMMIT_LIST}` — pasted `git log <fixed-point>..HEAD --oneline`
  output; `{RETURN_CONTRACT}` — the pasted contents of `references/return-contract.md`, placed at the end of the
  template; `{BASELINE_PATH}` — absolute path to `references/structure-baseline.md`, read-first (decision 9);
  `{PRESEEDED_FINDINGS}` — the gate script's TSV verbatim (`path<TAB>before<TAB>after` per line), or `none`.
- **The return contract is single-sourced and pasted, never path-referenced** (decision 15): sub-agents must not
  be asked to look it up. It states, once: the finding schema, the exact sentinels, the label rule, and the
  ordering duty (Contract B, restated in the sketch below). Axis-specific cite content lives in each template, not
  in the shared file — for Structure: name the baseline entry and quote the anchoring hunk.
- **What the template must encode** (each stated once, in the template, no first person anywhere):
  - Explicit Skill-tool invocation of `codebase-designing` (decision 5), using the house wording pattern from
    `skills/design/SKILL.md:23-24`: "actually invoke … with the Skill tool; mentioning a skill in prose loads
    nothing".
  - Baseline read-first: read `{BASELINE_PATH}` fully before reading code; it is the complete heuristic set —
    flag nothing outside it except a gated judo finding (decisions 2, 9).
  - Pre-seeded crossings: each TSV line comes back as a finding with its `blocker (presumptive)` label kept
    intact; the sub-agent adds context only (is decomposition sensible, does the change justify the size) — never
    re-derives, relabels, or drops one (decision 6).
  - Judo gate (decision 4): a reframing that deletes complexity is reportable only with all three of (a) a
    concrete sketch — what disappears, what replaces it; (b) a behaviour-preservation argument; (c) a complexity
    argument in `codebase-designing` terms — fewer concepts a reader must hold, fewer dependencies, less obscurity
    (the criterion from `.planning/review/nuclear-review.md:94`). Always `suggestion`. No "assume one exists".
  - Read scope (decision 13): reading touched files and their surroundings is allowed; every finding still quotes
    the hunk it anchors to.
  - Posture: prefer a few high-conviction findings over a flood of nits
    (`.planning/review/nuclear-review.md:166-167`).
- **The harness** (this phase's checkpoint): the filled template is itself the entire sub-agent prompt — spawn one
  `general-purpose` agent via the Agent tool with that prompt as its task, and check the return against
  Contract C: accept iff the return is exactly one sentinel line OR contains ≥1 finding bullet matching the
  Contract B shape with a cite line. If the phase subagent has no Agent tool, these runs fall to the `/implement`
  orchestrator's own verification pass.
- Harness fills may use `git -C <path>` diff commands to target a fixture repo — a harness liberty; the
  orchestrator's real fill (phase 6) is always the literal `git diff <fixed-point>...HEAD`.
- Prerequisites already landed: the gate script (phase 1, source of real TSV) and the baseline (phase 2, the file
  `{BASELINE_PATH}` points at).

## Changes

Sketches are targets, not prescriptions: write the failing test first; if reality disagrees with a sketch, follow the
mismatch protocol rather than improvising.

### 1. The shared return contract

**File**: `skills/three-axis-review/references/return-contract.md`
**Change**: create the ~10-line shared return format (Contract B). Its entire content is pasted into every
template via `{RETURN_CONTRACT}`, so it must read as direct instructions to a sub-agent and contain no
placeholders of its own.

```markdown
Report each finding as one bullet in exactly this shape, every blocker listed before the first suggestion:

- `blocker (presumptive)` | `suggestion` — `path:line` — <one-sentence finding>
  cite: <axis-specific citation with a short quote>
  <free-form detail; any code in fenced blocks; no length cap>

Label rule: `blocker (presumptive)` only on an objective trigger or a documented-rule breach; otherwise
`suggestion`. When unsure, `suggestion`.

Nothing to report → the entire return is exactly this one line:
NO FINDINGS: <one line — what was reviewed>

Only if the instructions above authorise skipping and the skip condition holds → the entire return is exactly:
SKIPPED: <reason>
```

### 2. The Structure template

**File**: `skills/three-axis-review/references/structure-prompt.md`
**Change**: create the verbatim Structure sub-agent template. Placeholders in `{CAPS}` are the only fillable
parts; everything else ships to the sub-agent exactly as written.

````markdown
# Structure sub-agent prompt

Fill `{DIFF_CMD}`, `{COMMIT_LIST}`, `{BASELINE_PATH}`, `{PRESEEDED_FINDINGS}`, and `{RETURN_CONTRACT}`; change
nothing else.

```
You are the Structure reviewer in a three-axis code review. Judge one thing: is the change well built?
Spec fidelity and documented-repo-rule compliance belong to other reviewers — do not report on them.

Set up in this order:

1. Invoke the `codebase-designing` skill with the Skill tool — actually invoke it; mentioning a skill in prose
   loads nothing. Its vocabulary (module, interface, seam, depth, complexity) is the language for every finding
   below.
2. Read the baseline at {BASELINE_PATH} in full before reading any code. It is the complete heuristic set for
   this review: match the change against its entries, and flag nothing outside them except a judo finding that
   passes the gate below.
3. Run exactly this command and read the whole diff: {DIFF_CMD}
   The commits under review:
   {COMMIT_LIST}

Read scope: reading the touched files and their surroundings is allowed and encouraged where an entry needs
context (ownership, duplication, inheritance) — but every finding must anchor to and quote a hunk from the diff.

Pre-seeded findings — file-size crossings detected by a deterministic gate (one TSV line per file: path, lines
before, lines after), or `none`:
{PRESEEDED_FINDINGS}
Return each TSV line as a finding keeping its label `blocker (presumptive)` intact. Add context only — is
decomposition sensible here, does anything in the change justify the size — never re-derive, relabel, or drop one.

Judo findings — a reframing of the change that deletes complexity rather than rearranging it. Report one only
when all three parts are present: (a) a concrete sketch — what disappears and what replaces it; (b) why behaviour
is preserved; (c) why complexity drops, in codebase-designing terms — fewer concepts a reader must hold, fewer
dependencies, less obscurity. A judo finding is always a `suggestion`. Missing any part → do not report it.

cite line for this axis: name the baseline entry and quote the anchoring hunk.
Prefer a few high-conviction findings over a flood of nits.

{RETURN_CONTRACT}
```
````

## Success criteria

### Automated verification

- [x] Placeholder set is exact:
      `grep -oE '\{[A-Z_]+\}' skills/three-axis-review/references/structure-prompt.md | sort -u` prints exactly
      `{BASELINE_PATH}`, `{COMMIT_LIST}`, `{DIFF_CMD}`, `{PRESEEDED_FINDINGS}`, `{RETURN_CONTRACT}`; the same grep
      on `return-contract.md` prints nothing.
- [x] Exact sentinels present in the contract: `grep -c 'NO FINDINGS: <one line' ...return-contract.md` and
      `grep -c 'SKIPPED: <reason>' ...return-contract.md` each print 1.
- [x] Explicit Skill invocation present: `grep -q 'Skill tool' skills/three-axis-review/references/structure-prompt.md`.
- [x] No first person in either file:
      `grep -inE '\b(i|we|our|let'"'"'s)\b' skills/three-axis-review/references/return-contract.md skills/three-axis-review/references/structure-prompt.md`
      finds nothing.
- [x] **Harness run A — preseeds survive**: rebuild the phase 1 fixture repo in `$TMPDIR` (same script, branches
      `main`/`feature`), run the gate script against `main` there to get real TSV. Fill the template:
      `{DIFF_CMD}` = `git -C <fixture> diff main...feature`, `{COMMIT_LIST}` = pasted
      `git -C <fixture> log main..feature --oneline`, `{BASELINE_PATH}` = absolute path to
      `structure-baseline.md`, `{PRESEEDED_FINDINGS}` = the TSV verbatim, `{RETURN_CONTRACT}` = pasted contract.
      Spawn one `general-purpose` agent with the filled prompt. Accept iff: return passes Contract C; every
      pre-seeded TSV line comes back as a finding still labelled `blocker (presumptive)`; blockers appear before
      any suggestion.
- [x] **Harness run B — real branch**: same fill against this repo — `{DIFF_CMD}` = `git diff main...HEAD`,
      `{COMMIT_LIST}` from the same range, `{PRESEEDED_FINDINGS}` = output of the gate script run on this repo
      (or `none` if empty). Accept iff the return passes Contract C: schema-shaped bullets whose cite lines name a
      baseline entry and quote a hunk, blockers first — or exactly `NO FINDINGS: <one line>`.
- [x] **Harness run C — clean diff**: scratch repo in `$TMPDIR` whose branch makes one trivial change (a one-line
      typo fix in a text file); fill and spawn as above with `{PRESEEDED_FINDINGS}` = `none`. Accept iff the
      entire return is exactly `NO FINDINGS: <one line>`.

### Manual verification

- [x] The user deep-reads `structure-prompt.md` against decisions 4 (judo gate wording — all three parts required,
      always `suggestion`), 5 (explicit Skill-tool invocation), and 13 (read scope) — and `return-contract.md`
      against Contract B. *(Confirmed by the user 2026-07-10, including the user-approved contract addition:
      "Return only the findings (or the sentinel) — no preamble, no headers, no closing commentary.")*

A phase with manual steps is a pause point: the orchestrator must wait for the user to confirm them before starting
the next phase.

## Dependencies

- **Depends on**: 1 (real TSV to pre-seed), 2 (baseline to read)
- **Blocks**: 4, 5, 6
