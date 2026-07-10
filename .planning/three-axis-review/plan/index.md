# Plan: three-axis-review — index

> Status: ready for implementation. Audience: the implementing agent; humans spot-check.

## Overview

Build `skills/three-axis-review/` — a review skill invoked as `/three-axis-review` that diffs the current branch
against a user-pinned fixed point and reviews it along three orthogonal axes, each a parallel sub-agent: **Spec**
(does it do the right thing), **Standards** (does it follow documented repo rules), **Structure** (is it well
built). The skill combines the heuristics of `.planning/review/nuclear-review.md` with the deterministic macro
shape of `.planning/review/two-axes-review.md`. Six phases mirror the six approved structure slices: the
deterministic line-count gate script, the merged smell baseline, the Structure template plus the shared return
contract, the Spec template, the Standards template, and finally the orchestrator SKILL.md with its README entry.

## Current state

- `skills/three-axis-review/` does not exist. The two source skills live in `.planning/review/`
  (`nuclear-review.md`, `two-axes-review.md`) alongside three adversarial-findings documents.
- All design decisions are resolved in `.planning/three-axis-review/decisions-three-axis-review.md`, including the
  2026-07-09 Amendment (markdown-only sub-agent returns). The approved slicing is
  `.planning/three-axis-review/structure.md`; its Contracts §A–§E are restated below as binding contracts.
- House conventions this build must follow:
  - Verbatim prompt templates — fill placeholders, change nothing else: `skills/implement/SKILL.md:34`.
  - Reference payloads live in `references/` (`skills/research/references/subagent-prompts.md` is the precedent).
  - Skill scripts live in `scripts/`, Python 3, `#!/usr/bin/env python3`, module docstring with a Usage section,
    stdlib only (`skills/skill-creator/scripts/` is the precedent).
  - Process skills carry `disable-model-invocation: true` (`skills/implement/SKILL.md:4`).
  - Skill voice: never first person — "you"/"the user" only; templates and sketches included (repo memory).
  - Composed skills use explicit Skill-tool invocation wording (`skills/design/SKILL.md:23-24`: "actually invoke
    each one with the Skill tool; mentioning a skill in prose loads nothing").
  - No history or provenance in skill bodies or references — instructions only (repo memory). Provenance stays in
    the planning artifacts.
- This repo's root has **no** project `CLAUDE.md`, `AGENTS.md`, CONTRIBUTING/CODING_STANDARDS/STYLE doc, and no
  lint/format configs (verified 2026-07-10) — on this repo, Standards discovery finds nothing. Phase 5's
  positive-case harness therefore runs read-only against `/Users/codey.byrne/dev/kotlin.applications` (user
  decision 2026-07-10), which has root `CLAUDE.md`, `AGENTS.md`, a root `docs/` directory, and `.editorconfig`.
- `README.md`'s Workflow pipeline section holds one `####` entry per pipeline skill, `/research` through
  `/open-pr`, followed by "A typical run" (`README.md:49-114`).
- Validator: `python3 skills/skill-creator/scripts/quick_validate.py <skill-dir>` checks SKILL.md frontmatter.

## Desired end state

`/three-axis-review <fixed-point>` produces a three-section report — `## Spec`, `## Standards`, `## Structure` —
of findings labelled `blocker (presumptive)` or `suggestion`, blockers before suggestions within each axis, labels
never re-derived, findings never merged or reranked across axes, each axis closed by a one-line summary. An axis
that cannot run renders `skipped` (no source) or `not reviewed` (failed twice) rather than appearing clean.
Verified by: fixture-repo script tests (phase 1), completeness greps plus user review (phase 2), standalone
template harnesses driven through the Agent tool (phases 3–5), and `quick_validate.py` plus a wiring-only dry-run
(phase 6).

## Key discoveries

- The two source skills fail in opposite directions — nuclear is content without process, two-axes is process with
  broken wiring (`.planning/review/findings-comprehensive.md`, "Headline").
- Nuclear's ~120 instructions reduce to ~7 concerns; the sevenfold restatement is the drift hazard
  (`.planning/review/findings-nuclear-review.md` §2).
- Two-axes' Fowler baseline (`.planning/review/two-axes-review.md:45-56`) and nuclear's concerns
  (`.planning/review/nuclear-review.md:23-69`) overlap on at least four smells — why the merged baseline lives on
  one axis (decision 2).
- Sub-agents share the filesystem, so the baseline passes by path, not transcription (decision 9) — but the return
  contract is pasted, not path-referenced, because it must be un-skippable (decision 15).
- `codebase-designing` supplies the canonical vocabulary: deletion test (`skills/codebase-designing/SKILL.md:85-86`),
  hypothetical seam (`:89`), interface as everything-a-caller-must-know (`:21-23`), complexity as dependencies +
  obscurity (`:46-48`, `:91-93`).
- Pipeline artifacts for the Spec axis, in preference order: `plan/index.md` + `plan/phase-N-<slug>.md` →
  `structure.md` → `design.md`, all under `.planning/<slug>/` (`skills/write-plan/SKILL.md`,
  `skills/structure/SKILL.md`, `skills/design/SKILL.md`).
- The skill's own files are referenced relative to its base directory, which the harness supplies at invocation
  ("Base directory for this skill: <path>") — SKILL.md can derive absolute paths from it.

## Durable decisions

All from `decisions-three-axis-review.md` (§refs) and `structure.md`. Violating one fails the phase.

1. **Macro shape** (§1): pin fixed point → `git rev-parse` + non-empty-diff gate *before* fan-out → three-dot diff
   (`git diff <fixed-point>...HEAD`) → one message, parallel Agent calls → aggregate.
2. **One merged baseline on Structure** (§2): Standards is documented-rules-only; the precedence rule — a
   documented repo standard always wins — travels with the baseline.
3. **Output contract** (§3): findings only, no overall verdict; labels `blocker (presumptive)` / `suggestion`,
   driven by objective triggers where possible; blockers before suggestions within an axis; labels never
   re-derived; findings never merged or reranked across axes; one-line per-axis summary closes each section.
4. **Judo is validation-gated** (§4): a simplification-reframing finding is reportable only with a concrete sketch
   (what disappears, what replaces it) + a behaviour-preservation argument + a complexity argument in
   `codebase-designing` terms; always `suggestion`; no "assume a judo move exists".
5. **`codebase-designing` coupling** (§5): the Structure template explicitly invokes it with the Skill tool; the
   baseline is written in its vocabulary. Definitions stay canonical in one place.
6. **1k gate is script-owned** (§6): the orchestrator runs `scripts/file_size_gate.py` at step 1; crossings arrive
   as pre-seeded Structure findings auto-labelled `blocker (presumptive)`; the sub-agent adds context only.
7. **Spec discovery chain** (§7): ① user-passed path — the only no-confirmation route; ② `.planning/<slug>/`
   matching the branch/feature, preference `plan/index.md` + phase files → `structure.md` → `design.md`, best match
   confirmed with the user; ③ ticket keys in commit messages → forge CLI inferred from session context — definitive
   proof → use it, else ask, inferred matches confirmed; ④ ask the user. Nothing → the Spec axis is `skipped`. No
   PRD references anywhere.
8. **Standards discovery** (§8): fixed, closed candidate set — project CLAUDE.md / AGENTS.md; root-level
   CONTRIBUTING / CODING_STANDARDS / STYLE docs; root `docs/` scanned for similarly named files — explicit stopping
   rule, no repo-wide crawl. The scan is delegated by the Standards sub-agent to a haiku exploration sub-agent.
   Nothing found → explicit skip. Tooling filter grounded by orchestrator-detected config filenames.
9. **Baseline delivery by absolute path** (§9): passed in the Structure template with a read-first instruction.
10. **Verbatim templates, placeholders only** (§10): three separate prompt files under `references/` (user decision
    in `structure.md`, superseding an inline layout); per axis the orchestrator reads that file, fills exactly its
    placeholder set (Contract D), and changes nothing else.
11. **No word caps; citations mandatory** (§11): original detail is wanted. An empty or failed axis → rerun once →
    then reported as `not reviewed`, distinct from "no findings".
12. **Identity** (§12): `skills/three-axis-review/` (SKILL.md + `references/` + `scripts/`); frontmatter
    `disable-model-invocation: true`; standalone — no other skill invokes it. The README documents it as an
    optional quality gate between `/implement` and `/open-pr`, the entry placed physically between those two
    entries in the pipeline section (user decision 2026-07-10).
13. **Read scope** (§13): the Structure sub-agent may read the touched files and their surroundings, not just
    hunks — but every finding still quotes the hunk it anchors to. Spec and Standards work from the diff plus their
    supplied sources.
14. **Spec handover** (§14): spec content fetched from a tracker is pasted into the prompt; specs that are repo
    files are passed as paths.
15. **Markdown-only returns** (Amendment 2026-07-09): no JSON contract, no validator/parser script, no MCP/custom
    tool, no Workflow-based fan-out. The return format is single-sourced in `references/return-contract.md` and
    pasted into every template via a common `{RETURN_CONTRACT}` placeholder — sub-agents are never asked to look it
    up by path. Sentinels are exact strings. Each sub-agent orders its own findings blockers-first, so aggregation
    is pure concatenation plus a composed per-axis summary line (finding count = bullet count).

### Binding contracts (carry the same force as the numbered decisions; phase files cite them by letter)

**A. Gate script CLI** — `python3 skills/three-axis-review/scripts/file_size_gate.py <fixed-point>`.
Comparison: line count at the merge-base of `<fixed-point>` and `HEAD` versus at `HEAD` (never the working tree).
Threshold fixed at 1,000: a crossing is `before ≤ 1000 and after > 1000`; new files count `before = 0`; deleted
files never cross. Diff enumeration: `git diff --name-status -M -z <merge-base> HEAD`; statuses `A` → (None, path);
`M` → (path, path); `D` → skip; `R<n>` → (old, new); any other status (`T`, …) → treat as `M` at the after path; no
`-C`, so copies surface as adds. Binary = blob contains a NUL byte → skip the file. Line count = count of `b"\n"`,
+1 if the file is non-empty and lacks a trailing newline. Output: one TSV line per crossing —
`path<TAB>before<TAB>after` — sorted by path; empty stdout = no crossings; no headers, no prose. Exit codes: 0 on
success (with or without crossings); 2 on usage error or any git failure (unresolvable ref, no merge-base, not a
repo), reason on stderr. Stdlib only.

**B. Return contract** (`references/return-contract.md`, pasted via `{RETURN_CONTRACT}` at the end of each
template). The shared file states, once: the finding schema, the exact sentinels, the label rule, and the ordering
duty.

```
- `blocker (presumptive)` | `suggestion` — `path:line` — <one-sentence finding>
  cite: <axis-specific citation with a short quote>
  <free-form detail; any code in fenced blocks; no length cap>
```

Label rule: `blocker (presumptive)` only on an objective trigger or documented-rule breach; otherwise
`suggestion`; when unsure, `suggestion`. Ordering duty: blockers before suggestions, so aggregation never
reorders. Sentinels — exact strings, each the entire return: `NO FINDINGS: <one line — what was reviewed>` for a
clean axis; `SKIPPED: <reason>` for Standards with no discovered sources. Cite content per axis — Spec: quoted
spec line; Standards: rule file + quoted hunk; Structure: baseline entry name + quoted hunk — stated in each
template, not in the shared file.

**C. Validation and failure handling** (operationalises decision 11; lives in SKILL.md's verify step and drives
the phase 3–5 harnesses. Amended 2026-07-10, user decision: tiered axis-aware validation with repair-reruns
replaces the strict format gate — format enforcement via reruns proved non-convergent and expensive).

Hard checks — any failure triggers a repair-rerun:
- *Usability floor* (all axes): the return is non-empty and contains either a sentinel or ≥1 bullet starting with
  a legal label. A floor failure has nothing to repair — its rerun is a full rerun of the original prompt.
- *Paths in diff* (Structure and Standards only): every finding's `path` appears in
  `git diff --name-only <fixed-point>...HEAD`.
- *Pre-seed preservation* (Structure only): every gate TSV path reappears in a `blocker (presumptive)` finding.
- *Illegal skip*: `SKIPPED:` from Spec or Structure is invalid; only Standards may emit it.

Advisory — pasted through with a one-line orchestrator note under the axis, never a rerun: a Spec finding path
absent from both the diff and the repo (legitimate for missing-requirement findings), unknown labels, and format
noise (preamble, headers, closing commentary, first person).

Repair-rerun prompt: the original filled prompt + the previous return verbatim + the explicit defect list + the
instruction "Repair the listed defects. Keep every finding whose substance is sound. Do not re-review from
scratch." Second failure → axis rendered `not reviewed`. `not reviewed` is orchestrator-side only; sub-agents
never emit it. Spec with no discovered source is never spawned — the orchestrator marks the axis `skipped`
itself. Standards skips via its sentinel. Structure never skips. Gate fallback: if Structure ends `not reviewed`,
the orchestrator itself renders the pre-seeded crossings as §B findings under `## Structure` — script findings
cannot be lost to a dead axis.

**D. Placeholder sets** (exact; nothing else is fillable). Common to all three templates: `{DIFF_CMD}` — the
literal `git diff <fixed-point>...HEAD` string, which the sub-agent runs itself; `{COMMIT_LIST}` — pasted output of
`git log <fixed-point>..HEAD --oneline`; `{RETURN_CONTRACT}` — the pasted contents of
`references/return-contract.md`, placed at the end of each template. `spec-prompt.md` adds `{SPEC_SOURCE}` —
either `Read this spec file first: <path>` or pasted tracker content. `standards-prompt.md` adds
`{LINT_CONFIG_FILENAMES}` — orchestrator-detected config filenames grounding the tooling filter, filled
`none detected` when empty; its nested haiku-explorer prompt is static text with no orchestrator-filled
placeholders — fixed candidate set; the explorer returns found paths only, the Standards agent reads them itself.
`structure-prompt.md` adds `{BASELINE_PATH}` — absolute path, read-first — and `{PRESEEDED_FINDINGS}` — the gate
TSV verbatim, or `none`.

**E. Aggregation** (pure combination — no transformation step exists). The aggregated report is the orchestrator's
final message; no file is written. Under each of `## Spec`, `## Standards`, `## Structure`: the axis's findings
verbatim (already blockers-first per §B), or its sentinel/state (`skipped` / `not reviewed`) — labels never
re-derived, findings never merged or reranked across axes. Each axis closes with a composed one-line summary:
finding count (= bullet count) and the top blocker, if any.

## What we're NOT doing

- No overall approve/block verdict, no reranking across axes (decision 3).
- No word caps on sub-agent reports (decision 11 — supersedes an earlier 400/600-word proposal).
- No PRD references anywhere — superseded by the pipeline artifacts (decision 7).
- No smells on the Standards axis, no repo-wide standards crawl (decisions 2, 8).
- No "assume a judo move exists", no missed-judo blockers (decision 4).
- No import of nuclear's sevenfold restatement, tone-phrase library, or approval bar — each rule stated once.
- No JSON return contract, no validator/parser script, no MCP/custom tool, no Workflow fan-out (decision 15).
- No huge-diff handling in v1 — the gate covers only bad-ref/empty-diff.
- No install instructions for missing tools; missing forge CLI → ask the user (repo memories).
- No `/implement` integration in this build — the user intends to wire this skill into `/implement`'s verification
  later; v1 is standalone and nothing here prepares that integration.

## Implementation approach

Bottom-up, artifacts first, each proven standalone before anything references it: the script (1) and baseline (2)
are self-contained deliverables; the shared return contract lands with the Structure template (3) and is proven by
driving a real sub-agent through the filled template with no orchestrator; the Spec (4) and Standards (5) templates
reuse that proven contract and harness, independent of each other; the SKILL.md (6) lands last so it only ever
points at verified artifacts, and its dry-run tests orchestration wiring only.

## Testing strategy

- **Phase 1**: automated fixture-repo shell test — a scratch git repo in `$TMPDIR` exercising every crossing and
  non-crossing case; assertions on exact sorted TSV output and exit codes 0/2. No test framework; the checks are
  shell commands in the phase's success criteria.
- **Phase 2**: automated completeness greps (all Fowler names and nuclear-only entries present; no first person; no
  provenance; size cap) plus the user's content review of the mapping — a pause point.
- **Phases 3–5**: the standalone template harness — hand-fill the template's placeholders, spawn one
  `general-purpose` agent with the filled prompt via the Agent tool, and judge the return against Contract C's
  acceptance checklist. Phase 3 proves the return contract itself; phases 4–5 reuse the harness. If the phase
  subagent has no Agent tool, these runs fall to the `/implement` orchestrator's own verification pass.
- **Phase 6**: `quick_validate.py`, structural greps (frontmatter flag, referenced paths exist, placeholder sets,
  no first person, no dead concepts), then a human wiring-only dry-run on a real branch.

## Phase index

| Phase | Title | End-to-end behaviour | Depends on | Document |
|---|---|---|---|---|
| 1 | Gate script reports size crossings | `file_size_gate.py <fixed-point>` prints exactly the files the branch pushes past 1,000 lines | — | [phase-1-gate-script.md](phase-1-gate-script.md) |
| 2 | Structure baseline stands alone | `references/structure-baseline.md` holds the 17-entry merged what→fix baseline | — | [phase-2-structure-baseline.md](phase-2-structure-baseline.md) |
| 3 | Structure template reviews a real diff standalone | a hand-filled `structure-prompt.md` + pasted return contract drive one sub-agent to a checklist-accepted return | Phases 1, 2 | [phase-3-structure-template.md](phase-3-structure-template.md) |
| 4 | Spec template judges a diff against a spec standalone | a hand-filled `spec-prompt.md` passes the checklist in both spec-handover modes | Phase 3 | [phase-4-spec-template.md](phase-4-spec-template.md) |
| 5 | Standards template discovers rules and judges standalone | a hand-filled `standards-prompt.md` yields rule-cited findings on a standards-bearing repo and the SKIPPED sentinel on a bare one | Phase 3 | [phase-5-standards-template.md](phase-5-standards-template.md) |
| 6 | `/three-axis-review` runs end-to-end | five-step orchestration: pin/gate → spec chain → parallel fan-out → verify → aggregated three-section report; README entry | Phases 1–5 | [phase-6-end-to-end.md](phase-6-end-to-end.md) |

## References

- [task.md](../task.md)
- [decisions-three-axis-review.md](../decisions-three-axis-review.md) — the resolved design, including the
  2026-07-09 Amendment
- [structure.md](../structure.md) — the approved slicing and binding contracts
- `.planning/three-axis-review/design-plan/` — the earlier three-phase design refinement (its slicing and inline
  layout are superseded; its context and mapping table are carried into these phase files)
- `.planning/review/nuclear-review.md`, `.planning/review/two-axes-review.md` — source skills
- `.planning/review/findings-comprehensive.md` — the adversarial map
