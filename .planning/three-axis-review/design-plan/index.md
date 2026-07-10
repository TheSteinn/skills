# Design: three-axis-review — index

> Status: ready for further refinment. Audience: the implementing agent; humans spot-check.

## Overview

Build `skills/three-axis-review/`, a review skill that diffs the current branch against a user-pinned fixed point and
reviews it along three orthogonal axes — **Spec** (does it do the right thing), **Standards** (does it follow
documented repo rules), **Structure** (is it well built) — each as a parallel sub-agent. The design merges the good
heuristics of `.planning/review/nuclear-review.md` into the deterministic 5-step macro shape of
`.planning/review/two-axes-review.md`. Three phases, in the user's priority order: the deterministic line-count gate
script, the merged smell baseline (the Fowler×nuclear dedup mapping), then the SKILL.md itself.

## Current state

- `skills/three-axis-review/` does not exist. The two source documents live in `.planning/review/` alongside three
  adversarial-findings documents (`findings-nuclear-review.md`, `findings-two-axes-review.md`,
  `findings-comprehensive.md`).
- All design decisions are resolved in `.planning/decisions-three-axis-review.md` — no open design questions remain.
- House conventions this build must follow:
  - Verbatim prompt templates: `skills/implement/SKILL.md:34` — "Build every prompt from this template, filling the
    placeholders and changing nothing else".
  - Reference payloads live in `references/` (`skills/research/references/subagent-prompts.md` is the precedent).
  - Skill scripts live in `scripts/` and are Python 3 with usage docstrings (`skills/skill-creator/scripts/` is the
    precedent).
  - Process skills carry `disable-model-invocation: true` (e.g. `skills/implement/SKILL.md:4`).
  - Skill voice: never first person — "you"/"the user" only; sweep templates too (repo memory).
  - Composed skills use explicit Skill-tool invocation wording (`skills/design/SKILL.md:23-29` is the pattern:
    "actually invoke each one with the Skill tool; mentioning a skill in prose loads nothing").
  - No history/provenance in skill bodies or references — instructions only (repo memory). Mapping provenance stays in
    this plan, not in the baseline file.

## Desired end state

`/three-axis-review <fixed-point>` is invocable and produces a three-section report (`## Spec`, `## Standards`,
`## Structure`), findings labelled `blocker (presumptive)` or `suggestion`, blockers sorted first within each axis,
never reranked across axes, closed by a one-line per-axis summary. Each axis that cannot run reports `skipped` (no
source) or `not reviewed` (failed twice) rather than appearing clean. Verified by: the fixture-repo script tests
(phase 1), grep completeness checks on the baseline (phase 2), `quick_validate.py` plus a human dry-run (phase 3).

## Key discoveries

- The two source skills fail in opposite directions — nuclear is content without process, two-axes is process with
  broken wiring (`.planning/review/findings-comprehensive.md`, "Headline").
- Nuclear's ~120 instructions reduce to ~7 concerns; the sevenfold restatement is the drift hazard
  (`findings-nuclear-review.md` §2).
- Two-axes' Fowler baseline (`.planning/review/two-axes-review.md:45-56`) and nuclear's concerns
  (`.planning/review/nuclear-review.md:23-69`) overlap on at least four smells — the reason the merged baseline lives
  on one axis (`decisions-three-axis-review.md` §2).
- Sub-agents share the filesystem, so baselines pass by path, not transcription
  (`decisions-three-axis-review.md` §9).
- `codebase-designing` supplies the canonical vocabulary: deletion test (`skills/codebase-designing/SKILL.md:85-86`),
  hypothetical seam (`:89`), complexity/held-concepts (`:46-48`, `:91-93`).
- Pipeline artifacts for the Spec axis, in preference order: `plan/index.md` + `plan/phase-N-<slug>.md`, then
  `structure.md`, then `design.md`, all under `.planning/<slug>/` (`skills/write-plan/SKILL.md:33`,
  `skills/structure/SKILL.md:46`, `skills/design/SKILL.md:9`).

## Durable decisions

All from `.planning/decisions-three-axis-review.md`; numbers below are cited by the phase files. Violating one fails
the phase.

1. **Macro shape**: pin fixed point → `git rev-parse` + non-empty-diff gate before fan-out → three-dot diff
   (`git diff <fixed-point>...HEAD`) → one message, three parallel Agent calls → aggregate (record §1).
2. **One merged baseline on Structure**; Standards is documented-rules-only; the repo-overrides precedence rule moves
   with the baseline (record §2).
3. **Output contract**: findings only; labels `blocker (presumptive)` / `suggestion` from objective triggers where
   possible; aggregator sorts blockers-first within an axis, never re-derives labels, never reranks across axes;
   one-line per-axis summary (record §3).
4. **Judo is validation-gated**: sketch + behaviour-preservation argument + complexity argument in
   `codebase-designing` terms; always `suggestion`; no "assume one exists" (record §4).
5. **Structure template explicitly invokes `codebase-designing`** via the Skill tool; the baseline is written in its
   vocabulary (record §5).
6. **1k gate is script-owned**: the orchestrator runs `scripts/file_size_gate.py`; crossings arrive as pre-seeded
   Structure findings auto-labelled `blocker (presumptive)`; the sub-agent adds context only (record §6).
7. **Spec discovery chain**: user path (no confirmation) → `.planning/<slug>/` artifacts (`plan/` → `structure.md` →
   `design.md`, best match confirmed with the user) → ticket keys + forge CLI inferred from session context (definitive
   proof → use; else ask; inferred matches confirmed) → ask; no spec → axis skips and says so (record §7).
8. **Standards discovery**: fixed closed candidate set (project CLAUDE.md/AGENTS.md; root CONTRIBUTING /
   CODING_STANDARDS / STYLE; root `docs/` scan for similar names); the scan is delegated by the Standards sub-agent to
   a haiku exploration sub-agent; nothing found → explicit skip; tooling filter grounded by orchestrator-supplied
   config filenames (record §8).
9. **Baseline delivery by absolute path** in the template, with a read-first instruction (record §9).
10. **Three verbatim fenced templates**, placeholders only; label definitions live inside template text (record §10).
11. **No word caps** — original detail wanted; citations mandatory; failed/empty axis → rerun once → `not reviewed`
    (record §11).
12. **Identity**: `skills/three-axis-review/`, `disable-model-invocation: true`; standalone; README documents it as an
    optional gate between `/implement` and `/open-pr` (record §12).
13. **Read scope** (derived from 2: adopting Feature Envy, Refused Bequest, and the deletion test): the Structure
    sub-agent may read the touched files and their surroundings, not just hunks — but every finding still quotes the
    hunk it anchors to. The Spec and Standards sub-agents work from the diff plus their supplied sources.
14. **Spec handover rule** (derived from 7): spec content fetched from a tracker is pasted into the prompt; specs that
    are repo files are passed as paths.

## What we're NOT doing

- No overall approve/block verdict, no reranking across axes (record §3).
- No word caps on sub-agent reports (record §11 — supersedes the earlier 400/600 proposal).
- No PRD references anywhere — superseded by the pipeline artifacts (record §7).
- No smells on the Standards axis, no repo-wide standards crawl (record §2, §8).
- No "assume a judo move exists", no missed-judo blockers (record §4).
- No import of nuclear's sevenfold restatement, tone-phrase library, or approval bar — the skill states each rule
  once.
- No huge-diff handling in v1 — the gate covers only bad-ref/empty-diff (record, Open items).
- No install instructions for missing tools; missing forge CLI → ask the user (repo memories).

## Implementation approach

Bottom-up, artifacts first: the script (phase 1) and the baseline (phase 2) are self-contained deliverables inside
`skills/three-axis-review/` that can be tested and reviewed before any skill prose exists; the SKILL.md (phase 3)
then references both by path, so the skill file lands last and never points at anything unverified. Phases 1 and 2
are independent of each other; the order between them is the user's priority call.

## Testing strategy

- **Phase 1**: automated fixture-repo tests — a scratch git repo in `$TMPDIR` exercising each crossing/non-crossing
  case; assertions on the script's TSV output and exit codes. No test framework is added; the checks are shell
  commands in the phase's success criteria.
- **Phase 2**: automated completeness greps (every Fowler smell name present; no first person; no provenance) plus
  human review of the mapping against the mapping table in the phase file.
- **Phase 3**: `python3 skills/skill-creator/scripts/quick_validate.py skills/three-axis-review` plus greps for
  frontmatter and referenced paths; then a human deep-read and an optional dry-run on a real branch.

## Phase index

| Phase | Title | End-to-end behaviour | Depends on | Document |
|---|---|---|---|---|
| 1 | Line-count gate script | `file_size_gate.py <fixed-point>` prints exactly the files a branch pushes past 1,000 lines | — | [phase-1-line-count-gate-script.md](phase-1-line-count-gate-script.md) |
| 2 | Merged structure baseline | `references/structure-baseline.md` holds the deduplicated Fowler×nuclear what→fix baseline | — | [phase-2-structure-baseline.md](phase-2-structure-baseline.md) |
| 3 | Skill drafting | `/three-axis-review` runs end-to-end: gate, discovery, three sub-agents, aggregated report | 1, 2 | [phase-3-skill-drafting.md](phase-3-skill-drafting.md) |

## References

- [task.md](../task.md)
- [decisions-three-axis-review.md](../decisions-three-axis-review.md) — the resolved design (grill record)
- `.planning/review/nuclear-review.md`, `.planning/review/two-axes-review.md` — source skills
- `.planning/review/findings-comprehensive.md` — the adversarial map both phases draw on
